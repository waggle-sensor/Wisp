#!/usr/bin/env python3
"""Stage 1 - Build an episode corpus from student Hermes `state.db` transcripts.

The v1 foundry pass mined *markdown artifacts* (agent-created SKILL.md files,
MEMORY.md) with a fixed keyword list. That misses the place where the real
learning signal lives: the 9k conversation messages in each brain's
`sage/state.db`, where a student hits a wall, the agent flails, and something
eventually works.

This script does no judging. It reduces raw transcripts to *episodes* -
bounded units of work sized for an LLM reader - and attaches structural
friction signals so downstream stages can rank episodes without keywords.

Episode = one contiguous user-turn-rooted span of a session: a user message
plus every assistant/tool message until the next user message. Consecutive
turns are packed into an episode until a size budget is hit, so a long
debugging arc stays in one unit rather than being split mid-diagnosis.

Signals attached per episode (all structural, none keyword-topical):
  n_turns, n_tool_calls, n_tool_failures, failure_rate,
  retry_depth      - max consecutive same-tool failures (agent stuck in a loop)
  wall_seconds     - elapsed time across the episode
  resolved         - episode ended with a clean tool call after >=1 failure
  user_frustration - user typed a short corrective/negative turn (structural:
                     brevity + question/negation after a failure, not a topic list)

Usage:
  python3 build_corpus.py --brains <dir> --out <dir>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

# Size budget per episode, in characters of rendered transcript. Chosen so a
# packed episode fits comfortably in a subagent read alongside its neighbours.
EPISODE_CHAR_BUDGET = 24_000
# Tool results are the bulkiest part of a transcript and mostly boilerplate
# after the first screenful; truncate but keep head and tail (errors land at
# the tail of a traceback).
TOOL_HEAD = 1_500
TOOL_TAIL = 800

FAILURE_TEXT = re.compile(
    r"(Traceback \(most recent call last\)|^\s*\w*Error:|command not found"
    r"|No such file or directory|Permission denied|exit status [1-9]"
    r"|FAILED|fatal:|Cannot connect|Connection refused|timed out)",
    re.MULTILINE,
)


def tool_failed(content: str | None) -> bool:
    """Best-effort: did this tool result represent a failure?

    Hermes tool results are usually JSON with an explicit success flag; fall
    back to scanning text for failure markers when they are not.
    """
    if not content:
        return False
    try:
        d = json.loads(content)
    except Exception:
        return bool(FAILURE_TEXT.search(content[:6000]))
    if isinstance(d, dict):
        if d.get("success") is False:
            return True
        if d.get("error"):
            return True
        code = d.get("exit_code", d.get("returncode"))
        if isinstance(code, int) and code != 0:
            return True
        # terminal tool nests the payload
        for key in ("output", "stdout", "stderr", "result", "content"):
            v = d.get(key)
            if isinstance(v, str) and FAILURE_TEXT.search(v[:6000]):
                return True
    return False


def parse_ts(v) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(str(v)[:26], fmt).timestamp()
        except ValueError:
            continue
    return None


def shorten(text: str, head: int, tail: int) -> str:
    if len(text) <= head + tail:
        return text
    return f"{text[:head]}\n...[{len(text) - head - tail} chars elided]...\n{text[-tail:]}"


@dataclass
class Turn:
    """One user message plus the assistant/tool messages that answer it."""
    user: str = ""
    messages: list = field(default_factory=list)  # (role, tool_name, content, failed)
    t_start: float | None = None
    t_end: float | None = None

    @property
    def n_tool(self) -> int:
        return sum(1 for m in self.messages if m[0] == "tool")

    @property
    def n_fail(self) -> int:
        return sum(1 for m in self.messages if m[0] == "tool" and m[3])


def max_retry_depth(turns: list[Turn]) -> int:
    """Longest run of consecutive failing calls to the same tool.

    A high value means the agent kept trying the same thing and kept losing -
    the strongest structural marker of a genuine knowledge gap.
    """
    best = cur = 0
    last = None
    for t in turns:
        for role, tool, _c, failed in t.messages:
            if role != "tool":
                continue
            if failed and tool == last:
                cur += 1
            elif failed:
                cur, last = 1, tool
            else:
                cur, last = 0, None
            best = max(best, cur)
    return best


# A corrective user turn is short and contains a negation, a correction, or a
# repeat-question marker. This is deliberately structural (shape of the turn),
# not a topical keyword list: it generalises to domains we did not anticipate.
CORRECTIVE = re.compile(
    r"\b(no|nope|not|isn'?t|doesn'?t|didn'?t|won'?t|can'?t|still|again|wrong"
    r"|but|why|actually|wait|nothing|fail(ed|ing)?|same error|broke)\b",
    re.IGNORECASE,
)


def frustration_score(turns: list[Turn]) -> int:
    """Count short corrective user turns that follow a failure."""
    score = 0
    seen_failure = False
    for t in turns:
        if seen_failure and t.user and len(t.user) < 400 and CORRECTIVE.search(t.user):
            score += 1
        if t.n_fail:
            seen_failure = True
    return score


def render(turns: list[Turn]) -> str:
    out = []
    for t in turns:
        if t.user:
            out.append(f"### USER\n{shorten(t.user, 4000, 500)}")
        for role, tool, content, failed in t.messages:
            content = content or ""
            if role == "assistant":
                out.append(f"### ASSISTANT\n{shorten(content, 4000, 500)}")
            elif role == "tool":
                mark = "FAILED" if failed else "ok"
                out.append(f"### TOOL {tool or '?'} [{mark}]\n{shorten(content, TOOL_HEAD, TOOL_TAIL)}")
    return "\n\n".join(out)


def load_session_turns(conn: sqlite3.Connection, session_id: str) -> list[Turn]:
    rows = conn.execute(
        "select role, content, tool_name, tool_calls, timestamp from messages "
        "where session_id=? order by id",
        (session_id,),
    ).fetchall()
    turns: list[Turn] = []
    cur: Turn | None = None
    for role, content, tool_name, tool_calls, ts in rows:
        t = parse_ts(ts)
        if role == "user":
            cur = Turn(user=content or "", t_start=t, t_end=t)
            turns.append(cur)
            continue
        if cur is None:
            # assistant/tool traffic before any user message (system replay)
            cur = Turn(user="", t_start=t, t_end=t)
            turns.append(cur)
        failed = tool_failed(content) if role == "tool" else False
        cur.messages.append((role, tool_name, content, failed))
        if t:
            cur.t_end = t
            if cur.t_start is None:
                cur.t_start = t
    return turns


def pack(turns: list[Turn], budget: int) -> list[list[Turn]]:
    """Group consecutive turns into episodes under a character budget."""
    episodes, cur, size = [], [], 0
    for t in turns:
        n = len(t.user) + sum(len(m[2] or "") for m in t.messages)
        n = min(n, budget)  # a single huge turn still forms one episode
        if cur and size + n > budget:
            episodes.append(cur)
            cur, size = [], 0
        cur.append(t)
        size += n
    if cur:
        episodes.append(cur)
    return episodes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brains", required=True, help="dir of <student>/sage/state.db")
    ap.add_argument("--out", required=True)
    ap.add_argument("--budget", type=int, default=EPISODE_CHAR_BUDGET)
    args = ap.parse_args()

    brains, out = Path(args.brains), Path(args.out)
    (out / "episodes").mkdir(parents=True, exist_ok=True)

    index = []
    for db in sorted(brains.glob("*/sage/state.db")):
        student = db.parts[-3]
        conn = sqlite3.connect(db)
        conn.text_factory = lambda b: b.decode("utf-8", "replace")
        sessions = conn.execute(
            "select id, model, started_at, title from sessions order by started_at"
        ).fetchall()
        for sid, model, started, title in sessions:
            turns = load_session_turns(conn, sid)
            if not any(t.user for t in turns):
                continue
            for k, group in enumerate(pack(turns, args.budget)):
                body = render(group)
                if len(body) < 400:
                    continue
                ts = [t.t_start for t in group if t.t_start] + [t.t_end for t in group if t.t_end]
                n_tool = sum(t.n_tool for t in group)
                n_fail = sum(t.n_fail for t in group)
                last_tools = [m for t in group for m in t.messages if m[0] == "tool"]
                eid = f"{student}-{sid}-{k:02d}"
                meta = {
                    "episode_id": eid,
                    "student": student,
                    "session_id": sid,
                    "model": model,
                    "title": title,
                    "n_turns": len(group),
                    "n_tool_calls": n_tool,
                    "n_tool_failures": n_fail,
                    "failure_rate": round(n_fail / n_tool, 3) if n_tool else 0.0,
                    "retry_depth": max_retry_depth(group),
                    "wall_seconds": round(max(ts) - min(ts), 1) if len(ts) > 1 else 0.0,
                    # a failure run that ends clean is a *solved* problem: the
                    # highest-value shape, because the fix is in the transcript
                    "resolved": bool(n_fail and last_tools and not last_tools[-1][3]),
                    "user_frustration": frustration_score(group),
                    "chars": len(body),
                    "sha256": hashlib.sha256(body.encode()).hexdigest()[:16],
                    "first_user_turn": (group[0].user or "")[:300],
                }
                (out / "episodes" / f"{eid}.md").write_text(body, encoding="utf-8")
                index.append(meta)

    (out / "episode_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"episodes: {len(index)}")
    print(f"students: {len({e['student'] for e in index})}")
    print(f"with failures: {sum(1 for e in index if e['n_tool_failures'])}")
    print(f"resolved arcs: {sum(1 for e in index if e['resolved'])}")


if __name__ == "__main__":
    main()

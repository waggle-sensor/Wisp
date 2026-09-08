# Next foundry pass

The 1.4.0 harvest (`foundry/harvest/1_4_0`) mined transcripts for **documentation
gaps and corrections**. A natural next pass treats the same (or a new) corpus as
an **agent-systems dataset**: tool inventory fitness, tool failure modes, and
efficiency — using the 4,424 logged tool calls and 331 episodes already built by
`foundry/tools/build_corpus.py`.

Put a new campaign under `foundry/harvest/<id>/`. Do not expand `1_4_0` ad hoc;
keep reusable code in `foundry/tools/`.

The agenda below is adapted from standard agent-evaluation practice (tool
selection / ablation / transition analysis as in Toolformer, Chameleon, Gorilla;
skill libraries as in Voyager; separate grading of tool failures vs planning
failures).

## 1. Tool selection and inventory fitness

Hermes agents at camp had a large tool surface (terminal, file edits, skill /
reference loaders, Graphify query, deploy helpers, etc.). More tools mean more
capability, but also more description tokens and harder selection. Questions to
answer from this corpus:

- **Usage distribution.** Plot call counts and unique-caller counts per tool
  (and per tool × student). Which tools dominate wall-time and episode count?
  Which are rarely or never used? Unused tools are candidates for removal,
  demotion from the default prompt, or better routing docs — not automatic
  deletion without an ablation.
- **Ablation study (offline first).** For high-friction episode classes, ask:
  if tool *T* were absent from the inventory, would the agent still have a
  viable path? Use counterfactual re-runs on a pinned model where feasible; at
  minimum, score episodes where *T* was the only successful path vs episodes
  where *T* was tried and abandoned. If removing *T* does not change outcomes
  on a held-out task set, prefer a smaller inventory.
- **Hard tools.** Flag tools the agent repeatedly mis-invokes (wrong args,
  wrong sequencing, ignore docs) even after loading the relevant skill page.
  Options: change the tool API, shrink its description, add a thinner wrapper
  skill, or stop exposing it until the model can use it reliably.
- **Model × tool preference.** If more than one backend model ran, compare
  tool-mix histograms the way Chameleon did for GPT-4 vs ChatGPT.
- **Task × tool dependence.** Segment by task / project type (GPU plugin,
  camera offline, image import, local `Plugin()`, etc.).
- **Framework extensibility.** Score not only the stock tools but how hard it
  is to add a new one.

## 2. Tool composition and skill growth

- **Tool transition graphs.** After tool *X*, how often does the agent call
  tool *Y*? Frequent pairs are candidates to merge into a higher-level tool or
  scripted skill.
- **Agent-authored skills as a Voyager-style library.** The 1.4.0 brains
  contain 19 agent-created skills (0 with evals). For each: was it re-used
  successfully outside the episode that created it? Promote reusable, verified
  skills into the shared profile; quarantine the rest.
- **Composition vs documentation.** Separate: (a) invent a new tool, (b) wrap
  existing tools, (c) fix docs so the existing tool is selectable. 1.4.0 mostly
  did (c); the next pass should quantify how often (a)/(b) would have been
  better.

## 3. Tool failures (distinct from planning failures)

A tool failure is: **correct tool chosen, wrong or unusable output** — or the
right tool was never available. Annotate a sample of the 529 tool failures
already counted in the 1.4.0 corpus:

| Failure class | What to look for in transcripts | Example |
| --- | --- | --- |
| Tool returns wrong result | Exit 0 but content is wrong; agent trusts it | Silent GPU omission (`--gpus all`); RGB vs BGR `snapshot.data` |
| Tool / environment error | Nonzero exit, exception, timeout, D-state hang | `import torch` hang; TTY/`sudo` failures |
| Translation / adapter error | High-level plan OK, concrete argv or YAML wrong | `pluginctl` without `runtimeClassName` |
| Missing tool | Agent invents a workaround or gives up | No camera attached, no offline camera mock |
| Description / selection error | Wrong tool picked because docs oversell or collide | Competing torch pages (hang vs nvmap) |

Practices: retain full tool call + output (episode renders truncate — size claims
must go back to raw `state.db`); test high-traffic tools independently; compare
traces to what a human Waggle/SAGE operator would have done.

## 4. Efficiency (valid plan, expensive path)

Beyond 1.4.0 friction signals (`retry_depth`, wall seconds, resolved arcs), track
steps per completed user ask, cost proxies (tokens, wall-time), and action
latency. Compare to a human operator checklist and to a smaller tool inventory.

## 5. Suggested deliverables

1. **`foundry/tools/tool_stats.py`** — per-tool histograms, failure rates, mean
   wall-time, transition matrix; CSV + a short HTML report under the new harvest
   directory.
2. **Labeled failure sample** — ≥100 failed tool calls tagged with the classes
   above; episode ids; same provenance rules as HV2 bundles.
3. **Inventory proposal** — keep / wrap / demote / remove table with ablation
   or counterfactual evidence.
4. **Efficiency dashboard** — steps and wall-time by task class, before/after
   any inventory change, graded with the same fingerprint discipline as the
   retrieval A/B harness.
5. **Skill-library audit** — disposition of the 19 agent-authored skills
   (promote / rewrite / drop) plus a rule for when future agents may write
   shared skills.

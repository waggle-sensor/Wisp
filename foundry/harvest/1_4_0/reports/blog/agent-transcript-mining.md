---

## sidebar_label: Many Agents, One Better Brain

sidebar_position: 7

import LabButtons from './components/LabButtons'

# Many Agents, One Better Brain: Turning a Week of Human-in-the-Loop Agent Debugging into a Better Shared Profile

Every student at the 2026 Sage summer camp got the same AI agent ([Hermes](https://hermes-agent.nousresearch.com/)) and hardware ([NVIDIA Jetson AGX Thor](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/)) for a week and every prompt, tool call, failure, and fix was logged. The recovered transcripts hold **9,077 messages and 4,424 tool calls, and 237.8 hours** of agent wall-time. This is the pipeline we built to read all of it, and the knowledge that came out.

![pipeline](img/agent-mining/pipeline.png)

## Setting

The study sits on three facts that have to be true at once: a cohort sharing the same hardware and stack, a shared agent profile every student started from, and recoverable copies of what each agent actually did. That is the setting the rest of the pipeline assumes.

![Cohort, shared Hermes agent, and recovered student brains](img/agent-mining/setting.png)

## 1. Get the brains

An agent's "brain" is its profile directory: the skills it was given, the ones it wrote itself, its memory file, and a `state.db` of the full conversation. Students were told to export theirs and push it to their own repo. Four did. Two of those uploads were malformed. That is a design problem, not a student problem: the step lands in the last hour of a week-long camp, after the work it preserves is done, and nothing tells a student their upload was broken.

Instructors then attempted recovery from the project-administered Thor nodes. They resolved each student's account on their assigned node and archived the profile directory in place deliberately *not* running the profile exporter, which produces an opinionated view and doesn't reliably carry the state databases the transcripts live in. A raw brain is a live home directory, so scripts were created to strip the credentials, caches, sandboxes, and secrets; the ~29.5 GB of raw copies were deleted once the cleaned ones validated.

![brain analytics](img/agent-mining/brain_analytics.png)

In Hermes, a skill can include an evals/ directory (or similar manifests) with runnable scenarios so the agent can check that the skill still works. Students’ agents wrote 19 new skills during camp; 0 of them included that kind of eval packaging skills only, no attached tests. Also, the 237.8 hours sum elapsed spans within episodes; they are not active compute time or measured student effort, and concurrent sessions can overlap.

## 2. Cut the transcripts into episodes

A transcript is a flat message stream. What we want is *the unit of getting stuck*: one or more consecutive student requests and the assistant/tool responses, packed into a bounded excerpt. Each **episode** carries friction signals, the longest run of consecutive failing calls to the same tool, whether that run ended in a clean call (symptom *and* fix, both in the record), and short corrective turns from the student, detected with short-turn and generic correction-word heuristics. A clean call
marks a potentially resolved arc, not proof that the student’s task succeeded.

**None of these signals encodes a topic.** That is the whole design constraint: nothing in the ranking says what we expect to find, which is what lets the method surface subjects nobody thought to look for.

**331 episodes** - 174 with detected failures and 138 marked as resolved by that heuristic.

![episodes](img/agent-mining/episodes.png)

## 3. Triage every episode digest

Friction *ranks* episodes; it never *gates* them. That mattered: our lowest-friction batches produced ten findings, including a whole cluster about vLLM. A friction threshold, the obvious efficiency move, would have discarded all of it. Six LLM miners read digests covering the full episode set, opening fuller excerpts as needed. Each received a **coverage map** of the existing docs: all 111 files with title, lead paragraph and headings. Then one question per episode:

> Would an agent with the shipped profile have gotten this right?

A semantic judgement, not a keyword match, and the brief explicitly forbids topic filtering, so an episode about an unexpected subject is as eligible as one about a covered one.

**53 findings** from ~173 full-episode reads.

![triage](img/agent-mining/triage.png)

## 4. Corroborate, then consolidate

Recurrence across students strengthens a finding, but does not establish statistical independence: students shared instructions, infrastructure, and sometimes nodes. Distinct-student counts are corroboration counts, not independent replications. Findings are scored by **independence** — the number of distinct students — with friction only as a tiebreaker.

Lexical clustering groups them first, but strictly as a hint. Good thing: it produced 51 clusters from 53 findings and split the single highest-independence finding in the corpus across six of them. Trusting it would have destroyed our best result. A semantic pass reduced 51 clusters to 28 themes, of which 19 were promoted and 9 held back — including a real fleet-wide outage, because a page describing a temporarily broken package is stale the moment the fleet is reprovisioned. **Provisioning state is not platform knowledge.**

The pipeline also caught itself twice. A miner **hallucinated a specific** — that loading the whole skill returns ~121.8k chars and truncates. Checking the raw databases of 50 calls naming that skill, *zero* requested the whole thing and no truncation flag was ever set. Note where we had to check. Our own corpus builder truncates long tool results, so **a pipeline's own lossiness can manufacture confirmation of exactly the claim it is being asked to verify.**

Also two miners **contradicted each other** on sudo. One said camp accounts have passwordless sudo for an allowlist, the other that the agent terminal can't run `sudo` at all. Both quoted real transcript text. The corpus settled it: 9 episodes show a TTY failure, but 92 show *successful* sudo calls, and every binary near a failure is off the allowlist. The over-general version, shipped verbatim, would have taught the next agent to abandon a capability that demonstrably works 92 times.

**Result: 10 candidate pages**, each with provenance back to the episodes that produced it. **Nine of the ten correct guidance the docs had already shipped** rather than adding to it.

![consolidate](img/agent-mining/consolidate.png)

### Two of the ten

**The tax nobody wrote down.** The agent's shell ran with `HOME` rewritten into the profile directory, so every `cd ~/project` landed somewhere that didn't exist. **9 of the 11 students with transcripts** hit this, across **52 episodes** contain the rewritten path, including 18 explicit failed directory changes. The earlier artifact pass missed this pattern. Reading the surrounding actions made a recurring harness issue distinguishable from an ordinary mistyped path.

**A page frozen one day before its own correction.** The docs said to set `CUDA_VISIBLE_DEVICES=` before importing torch. The transcripts show that isn't enough `import torch` *itself* hangs in uninterruptible D-state on Blackwell CUDA init, surviving SIGKILL. The student who hit it wrote the fix in their own notes:

> "UPDATE 2026-07-24: import torch ITSELF hangs in D-state (triggers CUDA
> runtime init even with `CUDA_VISIBLE_DEVICES=''`). D-state procs can't be
> killed with SIGKILL. Training scripts must NOT import torch at module level."

The important detail is that the memory itself contains this update. The earlier page selected the older advice without reconciling the later correction. Transcripts help recover the sequence, while memories can state the revised rule explicitly. The lesson is to read both and resolve contradictions before shipping.

## 5. Grade the pages before shipping them

Ten new pages are easy to write and easy to over-claim. Every one had to clear an A/B grading two things, where a task improves only if **both** hold:

1. **Retrieval** — does a page that answers the question land in the top *k*? Each arm is ranked over its *own* corpus, so a new page that pushes an existing answer down registers as a regression.
2. **Required phrases** — do the retrieved pages collectively contain the task’s specified symptom/cause/fix phrases? The code calls this “actionability,” but it is a text check, not a test of whether an agent can execute the procedure.

BM25 ranks the pages independently in each version. A pass requires an accepted answer file and the required phrases across the top-k text. The check is deterministic and offline. It can catch missing guidance and competing pages, but cannot establish correctness or task completion. **10/10 targeted tasks improved, 0 regressions, stable across *k* ∈ {1,2,3,5}, all 5 regression guards holding.** These are results on the authored suite; page wording was revised against it, so it is not a held-out success rate. The most useful number is a failure. On one task the control retrieves the relevant page **at rank 1** — the best-matching page in the whole baseline — and the task still fails, because the page that loads doesn't contain the answer:

```
control:   top_k[0] = thor-host-cpu-dev-first.md   (21.90)
           actionable = False   missing: ["D-state", "module level"]
treatment: top_k[0] = thor-host-torch-hang.md      (35.91)
           actionable = True
```

The control’s top page is relevant but is not an accepted answer for this task, so it also fails the retrieval gate. This is evidence of missing guidance, not an agent execution experiment. **A relevant search result can still lack the fix.**

The harness also rejected one of our own drafts, and our first fix made it worse: a banner naming the competing symptom *raised* the score, because we'd fed a rival page's best search terms into our own file. What helps a human reader reads to BM25 as "this page is even more about that topic." Naming the neighbouring *page* without restating its vocabulary fixed it — a writing rule the evaluation discovered on its own.

![grading](img/agent-mining/grading.png)

## 6. Verify on real hardware

Nine of the ten pages rewrite guidance the profile already shipped. A bad correction is worse than leaving the old text alone, so transcript evidence is not enough to ship. We re-checked the claims on a camp Thor six weeks later. Six pages were testable: all six held up, and one draft still needed a fix. It was wrong in a way that only showed up when we ran it on the node.

## 7. Ship it, and pay the bill

Making ten pages *findable* meant adding routing entries to the skill index, pushing it to **117,644 characters against a 100,000-character hard cap** placed by Hermes. We shipped with the debt recorded rather than quietly leaving ten pages unindexed, then discharged it by extracting the index's largest section — 85 flat bullets, 50,556 chars, larger than the biggest sibling skill — into 11 topic-grouped pages. **117,644 → 85,771 characters**, content preserved byte-for-byte and verified by assertion.

## What changed, as a knowledge graph

The profile ships a [Graphify](https://graphify.com/) knowledge graph over its own docs, which the agent queries before falling back to grep. Diffing that graph across releases shows the upgrade structurally — not as a score, but as what is newly *there*. Two zooms, meant to be read in order.

First the wide shot: where the mined skill sits among everything else the agent carries.

![Curated knowledge graph of the Sage Hermes profile, before and after](img/agent-mining/fig2-profile-overview.png)

Blue is `sage-waggle`, the mining target; grey is every other skill in the harness. Red marks the ten mined pages and orange the eleven from the size-cap split. The comparison shows twenty-one dots absent on the left, but present on the right. **This view is deliberately unflattering.** A small, legible addition to a large system is the correct impression, and the addition is *local*: the new dots land inside one skill's territory, not scattered across the profile.

Now the zoom — same interval, everything outside that skill cropped away:

![Knowledge subgraph of the sage-waggle skill, before and after](img/agent-mining/fig1-sage-waggle.png)

Both panels share one layout, so nothing moves between them; what changes is what is *there*. Grey is present in both releases; red is the ten mined pages; blue is the size-cap split. Where the red nodes land is the interesting part — **four distinct communities**: GPU runtime configuration, camera development without a camera attached, the skill core, and sudo policy. That is what mining a transcript corpus looks like when it works. The pages track independent failures hit by independent students, not one topic written up at length. As a pair the wide shot says mining touched one skill out of a large harness; the zoom says that within that skill the addition is real, attributable, and distributed across the topics agents actually got stuck on.

The same comparison is interactive below, with more than what two stills can show. Four live graphs sit in a 2×2: sage-waggle zoom vs the whole harness, 1.1.0 vs 1.4.0. Hover a node for its title; expand a tile to search and read the legend; and zoom in to see the node connections. Isolate either pair if the four-up is too dense. In the knowledge graphs you can see the docs the agent actually carries: each node is a page or concept, each edge a relationship it can follow when a question lands nearby. The *All skills* graph is the **simplified** retrieval index that the agent queries before falling back to grep.

<iframe src="html/compare-graphs.html" width="100%" height="720"></iframe>

## What we'd tell anyone building this

- **Rank by friction, never gate on it.** Our lowest-friction batches held ten findings we'd otherwise have discarded.
- **Re-derive miner claims from the primary source.** Another LLM is not a defence. Our own corpus builder truncates tool results, and that lossiness can manufacture confirmation of exactly the claim under review.
- **Adjudicate contradictions against corpus counts.** Two miners can both quote real transcript text and still over-generalise in opposite directions.
- **Treat lexical clustering as a hint, not a decision.** It split our highest-independence finding across six clusters; trusting it would have destroyed the best result.
- **Test on hardware before shipping corrections.** Text-only evidence produced one confidently wrong page.

## What we can claim

The work produced ten traceable documentation changes, improved the targeted offline checks, and caught an incorrect draft through hardware verification. The graph shows where pages were added; it does not measure whether an agent uses them well. The study combines a new evidence source with different triage and evaluation, so it does not prove that transcripts alone outperform artifacts. Nor do recorded failures reveal what would have happened with a different profile. The next test is to freeze both versions and run matched agents on unseen tasks, measuring completion and repeated failures. The useful feedback loop is already concrete: keep debugging records, read them alongside memories and skills, reconcile conflicting guidance, test the resulting pages, and carry the remaining uncertainty into the next evaluation.


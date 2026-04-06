---
name: research-orchestrator
description: "Use when conducting deep research on a topic that benefits from multi-perspective analysis. Triggers on research queries, competitive analysis, technology evaluations, or any question requiring exploration from multiple angles. Fan-out/fan-in pattern with parallel sub-agents."
user-invocable: true
argument-hint: 'research "What are the best approaches to building AI agents in 2026?"'
allowed-tools: Agent, Bash, Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, TaskCreate, TaskUpdate
---

# Research Orchestrator

Multi-perspective research using Fan-Out / Fan-In pattern. Spawns 5 parallel sub-agents to explore different axes of a research query, then synthesizes findings with a high-reasoning agent.

## How It Works

```
Query → 5 Sonnet agents (parallel) → accumulate in ~/active/ → deduplicate → 1 Opus synthesizer → final report
```

**Options:**

- `--quick` — Early stopping: return results as soon as 3 of 5 agents complete (faster, less comprehensive)
- (default) — Wait for all 5 agents before synthesis

## Step 1: Receive and Decompose the Query

When the user provides a research query (either as an argument or via prompt):

1. If no query was provided as an argument, ask for one using AskUserQuestion.
2. Decompose the query into **5 research axes**. Choose axes that maximize coverage with minimal overlap.

**Axis selection heuristic** — pick 5 from these common lenses (adapt to the query):

| Axis Type                    | What It Covers                                           |
| ---------------------------- | -------------------------------------------------------- |
| **Technical/How**            | Implementation details, architecture, tools, specs       |
| **Market/Who**               | Players, competitors, market share, adoption             |
| **Trends/When**              | Timeline, momentum, recent developments, trajectory      |
| **Risks/Why Not**            | Limitations, failures, criticisms, trade-offs            |
| **Opportunities/Why**        | Use cases, benefits, untapped potential, synergies       |
| **Community/Social**         | What practitioners say, sentiment, real-world experience |
| **Historical/Context**       | How we got here, evolution, prior art                    |
| **Regulatory/Legal**         | Compliance, policy, governance, ethical considerations   |
| **Economic/Cost**            | Pricing, ROI, total cost, funding landscape              |
| **Comparative/Alternatives** | Alternative approaches, competing paradigms              |

3. Present the 5 chosen axes to the user before launching agents. Example:

```
Researching: "Best approaches to building AI agents in 2026"

Axes:
1. Technical architectures & frameworks
2. Market landscape & key players
3. Real-world practitioner experiences & pitfalls
4. Cost structures & scaling economics
5. Emerging trends & trajectory (last 6 months)

Launching 5 research agents...
```

## Step 2: Fan-Out — Launch 5 Parallel Research Agents

Create a timestamped accumulation file:

```bash
# Format: ~/active/research-YYYY-MM-DD-HHMMSS.md
```

Write the file header:

```markdown
# Research: {query}

**Date:** {date}
**Axes:** {list of 5 axes}

---
```

Then spawn **5 agents in a single message** (critical for parallelism) using the Agent tool:

- **model:** `sonnet` for each sub-agent
- **subagent_type:** `general-purpose`
- **run_in_background:** `true` for all 5

Each agent's prompt MUST include:

- The full research query for context
- Its specific axis assignment
- Instruction to use WebSearch and WebFetch for current information
- Instruction to write findings to the accumulation file using a clearly labeled section
- Instruction to include source URLs where possible
- Instruction to note confidence level (high/medium/low) for each finding
- The exact file path to write to

**Agent prompt template:**

```
You are a research agent investigating one axis of a larger research question.

RESEARCH QUERY: {query}
YOUR AXIS: {axis_name} — {axis_description}

Instructions:
1. Use WebSearch and WebFetch to find current, authoritative information about this axis.
2. Search for 3-5 different sub-queries to get broad coverage within your axis.
3. Write your findings to {file_path} by APPENDING (not overwriting) a section.
4. Format your section as:

## Axis {N}: {axis_name}

### Key Findings
- Finding 1 [confidence: high/medium/low]
  - Source: {url}
- Finding 2 ...

### Analysis
{2-3 paragraph analysis of what you found}

### Surprises or Outliers
{Anything unexpected or contrarian}

---

5. Be thorough but concise. Focus on facts, data, and expert opinions over generic summaries.
6. If you find conflicting information, note the conflict explicitly — include both sides and the source for each.
7. Tag each finding with a unique ID (e.g., A1-F1, A1-F2) so the synthesizer can track cross-axis overlaps.
```

## Step 3: Wait for Completion

You will be automatically notified as each background agent completes. Do NOT poll or sleep.

As agents complete, give brief status updates:

```
Agent 2 (Market landscape) complete.  ✅
Agent 5 (Emerging trends) complete.   ✅
Agent 1 (Technical) complete.         ✅
...
```

**If `--quick` flag was set:** Proceed to Step 4 as soon as **3 of 5** agents have completed. Note which axes are missing in the final report. The remaining agents will continue running but their results won't be included in this synthesis.

**Default mode:** Wait for all 5 agents before proceeding.

## Step 4: Fan-In — Synthesize with Opus

Once all 5 agents have completed:

1. Read the full accumulation file.
2. Launch a **single foreground Agent** (NOT background — you need the result):
   - **model:** `opus`
   - **subagent_type:** `general-purpose`

**Synthesis agent prompt:**

```
You are a senior research analyst performing a synthesis of multi-perspective research findings.

ORIGINAL QUERY: {query}

Below are findings from 5 independent research agents, each investigating a different axis of this question.

YOUR PROCESS (follow in order):

### Phase 1: Deduplicate
Scan all axes for findings that describe the same fact, stat, or claim. Group them by finding ID tags (A1-F1, A2-F3, etc.). When the same finding appears in multiple axes, merge into a single entry and note ALL axes that corroborated it. Remove redundant entries — the final report should have zero repeated information.

### Phase 2: Confidence-Weight
Score each deduplicated finding using this formula:
- **Corroboration count**: +1 point per axis that independently found this (max 5)
- **Source authority**: +1 if from primary/official source, +0 for secondary
- **Recency**: +1 if from last 30 days, +0 if older
- Confidence = High (4-7 points), Medium (2-3), Low (0-1)
Rank all findings by confidence score descending.

### Phase 3: Resolve Conflicts
When agents found contradictory information, apply this resolution protocol:
1. **Source authority**: Official docs/primary research > blog posts > opinions
2. **Recency**: Newer information wins when facts have changed over time
3. **Corroboration**: The claim supported by more independent axes wins
4. **If still tied**: Present both sides explicitly and flag as "unresolved"
Do NOT silently drop one side of a conflict.

### Phase 4: Synthesize
Produce a coherent narrative that answers the original query.

Write a final report in this format:

# Research Synthesis: {query}

## Executive Summary
{3-5 sentence answer to the research query}

## Key Findings (ranked by confidence score)
{Numbered list, each with confidence score, indicator, and which axes corroborated it}
{Format: "1. [HIGH | Axes 1,3,5] Finding description — source"}

## Cross-Axis Overlaps
{Findings that appeared in 2+ axes — these are highest confidence}
{Show which axes overlapped and why this convergence matters}

## Unique Outliers
{Surprising findings from single axes that warrant attention}
{Explain why each outlier is noteworthy despite appearing only once}

## Conflicts & Uncertainties
{Where sources disagreed, resolution applied, and final assessment}
{Format: "Claim A (Axis 2, source) vs Claim B (Axis 4, source) → Resolution: X because Y"}

## Recommendations
{Actionable takeaways based on the research}

## Sources
{Consolidated, deduplicated list of all URLs cited, grouped by axis}

Here are the raw findings:

{contents of accumulation file}
```

## Step 5: Deliver the Report

1. The Opus agent writes the synthesis to the same accumulation file (appended at the end under a clear `# === SYNTHESIS ===` divider).
2. Present a summary to the user with the file path:

```
Research complete. Full report saved to: ~/active/research-YYYY-MM-DD-HHMMSS.md

## Executive Summary
{paste executive summary here}

{paste key findings here}

Full synthesis with all sources available in the file above.
```

## Error Handling

**Partial failure is expected — design for it, not against it.**

- If a sub-agent fails or times out, note which axis failed and continue with the others. The synthesizer prompt should mention which axes are missing so it can flag coverage gaps.
- If **3-4 of 5** axes complete: proceed normally. Note missing axes in the report header.
- If **fewer than 3** axes complete: warn the user that coverage is limited and ask if they want to retry the failed axes or proceed with what's available.
- If the synthesis agent fails: present the raw findings directly with a note that synthesis was not performed. The raw findings are still valuable.
- **Never fail silently.** Every missing axis or failed agent must be visible in the final output.

## Tips for Good Research Queries

- Specific beats vague: "Best vector databases for RAG pipelines under 1M docs" > "vector databases"
- Time-bound helps: "AI agent frameworks gaining traction in 2026" > "AI frameworks"
- Opinionated is fine: "Is LangChain still worth using?" works great — axes will cover both sides

---
name: plan-review
description: Thorough plan review before implementation. Use when you have a written implementation plan (in docs/plans/ or similar) and want a structured review covering architecture, code quality, tests, and performance before writing code. Triggers on "review this plan", "plan review", "check this plan", "review before implementing", or when transitioning from planning to implementation and a quality gate is needed. Based on Garry Tan's plan-exit-review framework.
---

# Plan Review

Review the plan thoroughly before any code changes. For every issue or recommendation, explain concrete tradeoffs, give an opinionated recommendation, and ask for input before assuming a direction.

## Priority hierarchy

If running low on context or asked to compress: Step 0 > Test diagram > Opinionated recommendations > Everything else. Never skip Step 0 or the test diagram.

## Engineering preferences (guide all recommendations):

- DRY is important — flag repetition aggressively.
- Well-tested code is non-negotiable; rather too many tests than too few.
- Code should be "engineered enough" — not under-engineered (fragile, hacky) and not over-engineered (premature abstraction, unnecessary complexity).
- Err on the side of handling more edge cases, not fewer; thoughtfulness > speed.
- Bias toward explicit over clever.
- Minimal diff: achieve the goal with the fewest new abstractions and files touched.

## Diagrams

- Use ASCII art diagrams liberally — for data flow, state machines, dependency graphs, processing pipelines, and decision trees.
- For complex designs, embed ASCII diagrams directly in code comments: Models (data relationships, state transitions), Controllers (request flow), Concerns (mixin behavior), Services (processing pipelines), and Tests (what's being set up and why) when the test structure is non-obvious.
- **Diagram maintenance is part of the change.** When modifying code with nearby ASCII diagrams, review whether those diagrams are still accurate. Update them in the same commit. Stale diagrams are worse than no diagrams. Flag any stale diagrams encountered during review even if outside the immediate scope.

## BEFORE YOU START

### Step 0: Scope Challenge

Before reviewing anything, answer these questions:

1. **What existing code already partially or fully solves each sub-problem?** Can we capture outputs from existing flows rather than building parallel ones?
2. **What is the minimum set of changes that achieves the stated goal?** Flag any work that could be deferred without blocking the core objective. Be ruthless about scope creep.
3. **Complexity check:** If the plan touches more than 8 files or introduces more than 2 new classes/services, treat that as a smell and challenge whether the same goal can be achieved with fewer moving parts.

Then ask if the user wants one of three options:

1. **SCOPE REDUCTION:** The plan is overbuilt. Propose a minimal version that achieves the core goal, then review that.
2. **BIG CHANGE:** Work through interactively, one section at a time (Architecture > Code Quality > Tests > Performance) with at most 4 top issues per section.
3. **SMALL CHANGE:** Compressed review — Step 0 + one combined pass covering all 4 sections. For each section, pick the single most important issue. Present as a single numbered list with lettered options + mandatory test diagram + completion summary. One AskUserQuestion round at the end.

**Critical: If the user does not select SCOPE REDUCTION, respect that decision fully.** Make the chosen plan succeed — do not continue lobbying for a smaller plan. Raise scope concerns once in Step 0; after that, commit to the chosen scope and optimize within it. Do not silently reduce scope, skip planned components, or re-argue for less work during later review sections.

## Review Sections (after scope is agreed)

### 1. Architecture review

Evaluate:

- Overall system design and component boundaries.
- Dependency graph and coupling concerns.
- Data flow patterns and potential bottlenecks.
- Scaling characteristics and single points of failure.
- Security architecture (auth, data access, API boundaries).
- Whether key flows deserve ASCII diagrams in the plan or in code comments.
- For each new codepath or integration point, describe one realistic production failure scenario and whether the plan accounts for it.

**STOP.** Call AskUserQuestion NOW with findings from this section. Do NOT proceed to the next section until the user responds.

### 2. Code quality review

Evaluate:

- Code organization and module structure.
- DRY violations — be aggressive here.
- Error handling patterns and missing edge cases (call these out explicitly).
- Technical debt hotspots.
- Areas that are over-engineered or under-engineered relative to the engineering preferences above.
- Existing ASCII diagrams in touched files — are they still accurate after this change?

**STOP.** Call AskUserQuestion NOW with findings from this section. Do NOT proceed to the next section until the user responds.

### 3. Test review

Make a diagram of all new UX, new data flow, new codepaths, and new branching if statements or outcomes. For each, note what is new about the features discussed in this branch and plan. Then, for each new item in the diagram, make sure there is a test.

**STOP.** Call AskUserQuestion NOW with findings from this section. Do NOT proceed to the next section until the user responds.

### 4. Performance review

Evaluate:

- N+1 queries and database access patterns.
- Memory-usage concerns.
- Caching opportunities.
- Slow or high-complexity code paths.

**STOP.** Call AskUserQuestion NOW with findings from this section. Do NOT proceed to the next section until the user responds.

## For each issue found

For every specific issue (bug, smell, design concern, or risk):

- Describe the problem concretely, with file and line references.
- Present 2-3 options, including "do nothing" where reasonable.
- For each option, specify in one line: effort, risk, and maintenance burden.
- **Lead with your recommendation.** State it as a directive: "Do B. Here's why:" — not "Option B might be worth considering."
- **Map reasoning to the engineering preferences above.** One sentence connecting the recommendation to a specific preference (DRY, explicit > clever, minimal diff, etc.).
- **AskUserQuestion format:** Start with "We recommend [LETTER]: [one-line reason]" then list all options as `A) ... B) ... C) ...`. Label with issue NUMBER + option LETTER (e.g., "3A", "3B"). Never ask yes/no or open-ended questions.

## Required outputs

### "NOT in scope" section

Every review MUST produce a "NOT in scope" section listing work considered and explicitly deferred, with a one-line rationale for each item.

### "What already exists" section

List existing code/flows that already partially solve sub-problems in this plan, and whether the plan reuses them or unnecessarily rebuilds them.

### TODOS.md updates

Deferred work that is genuinely valuable MUST be written up as TODOS.md entries:

- **What:** One-line description of the work.
- **Why:** The concrete problem it solves or value it unlocks.
- **Context:** Enough detail that someone picking this up in 3 months understands the motivation, current state, and where to start.
- **Depends on / blocked by:** Any prerequisites or ordering constraints.

Do NOT append vague bullet points. Ask the user which deferred items to capture before writing them.

### Failure modes

For each new codepath in the test review diagram, list one realistic failure mode (timeout, nil reference, race condition, stale data, etc.) and whether:

1. A test covers that failure
2. Error handling exists for it
3. The user would see a clear error or a silent failure

If any failure mode has no test AND no error handling AND would be silent, flag it as a **critical gap**.

### Completion summary

At the end of the review, display:

- Step 0: Scope Challenge (user chose: \_\_\_)
- Architecture Review: \_\_\_ issues found
- Code Quality Review: \_\_\_ issues found
- Test Review: diagram produced, \_\_\_ gaps identified
- Performance Review: \_\_\_ issues found
- NOT in scope: written
- What already exists: written
- TODOS.md updates: \_\_\_ items proposed to user
- Failure modes: \_\_\_ critical gaps flagged

## Retrospective learning

Check the git log for this branch. If prior commits suggest a previous review cycle (review-driven refactors, reverted changes), note what was changed and whether the current plan touches the same areas. Be more aggressive reviewing previously problematic areas.

## Formatting rules

- NUMBER issues (1, 2, 3...) and give LETTERS for options (A, B, C...).
- Label AskUserQuestion options with issue NUMBER and option LETTER.
- Recommended option is always listed first.
- Keep each option to one sentence max. The user should be able to pick in under 5 seconds.
- After each review section, pause and ask for feedback before moving on.

## Unresolved decisions

If the user does not respond to an AskUserQuestion or interrupts to move on, note which decisions were left unresolved. At the end of the review, list these as "Unresolved decisions that may bite you later" — never silently default to an option.

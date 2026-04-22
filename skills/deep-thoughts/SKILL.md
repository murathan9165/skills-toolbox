---
name: deep-thoughts
description: |
  Use when the user wants rigorous thinking before landing on an answer — framing a fuzzy problem, surfacing hidden assumptions, stress-testing a decision, running a premortem, steelmanning an opposing view, applying five-whys root-cause analysis, reframing a question, doing first-principles decomposition, finding a double-crux, or deliberating an ambiguous open-ended choice. Especially applies to strategy, product direction, research design, architecture decisions, hiring calls, ethical tradeoffs, and any prompt where jumping straight to a solution would skip important questions. Trigger phrases include "help me think through", "should I", "what should we build", "what am I missing", "reframe this", "pre-mortem", "steelman", "assumption audit", "debug my thinking", "five whys", "stress-test this decision", "first principles".
version: 0.1.0
author: jon-chun
license: MIT
homepage: https://github.com/jon-chun/skills-toolbox
keywords:
  - reasoning
  - socratic
  - design-thinking
  - premortem
  - steelman
  - first-principles
  - critical-thinking
  - decision-quality
---

# Deep Thoughts

## Overview

A disciplined thinking companion. When a user presents a fuzzy problem, a high-stakes decision, or an ambiguous open-ended question, **slow down before answering**: surface the assumptions, reframe the question if needed, and deliberate with a concrete Socratic or design-thinking method before producing a recommendation.

**Core principle:** the quality of an answer is capped by the quality of the question. Spend the first third of effort on the question itself.

## When to use

Trigger on any of:

- Strategic / product / research decisions with unclear success criteria
- Problems the user is "stuck" on or keeps circling
- Requests to "think through", "help me decide", "what should we build", "is this a good idea"
- Hiring, ethics, tradeoffs, or reputationally-sensitive choices
- Plans that feel "obviously right" — overconfidence is a trigger
- Post-mortems about near-misses that almost went badly

## When NOT to use

Skip this skill when:

- The user needs a direct factual answer ("what port does SSH use?")
- There is already a clear, shared success criterion and the work is execution
- Speed matters more than deliberation (outage, live-site incident)
- The user has explicitly asked for a quick answer or a vibe check

## Core methods — quick reference

| Method | When to reach for it | Output shape |
|---|---|---|
| **Socratic ladder** | Vague goal, unclear problem | A tree of clarifying → probing → evidential → implication questions |
| **Five Whys** | Recurring symptom, need root cause | A chain of 5+ "why?" with a named root cause |
| **Assumption audit** | Plan feels obvious or fragile | Ranked list of assumptions with confidence and consequence-if-wrong |
| **Premortem** | Before committing resources | "Imagine this failed — why?" → ranked failure modes with mitigations |
| **Steelman** | Disagreement, contested view | The strongest version of the opposing view, built charitably |
| **Double-crux** | Two parties disagree and are stuck | A single sub-question whose answer would change both minds |
| **First principles** | Received wisdom feels load-bearing | Decompose to physics/math/user-need atoms, rebuild bottom-up |
| **Reframe** | Question itself seems off | 3+ alternative framings, each with a different implied solution |

Details in `references/` — load the specific method's file when you apply it.

## Workflow

1. **Name the decision.** In one sentence, what is being decided, by whom, by when, reversibly or not?
2. **Classify the situation.** Execution problem (clear criteria) or thinking problem (unclear criteria)? If execution, exit this skill.
3. **Pick 1–3 methods** from the table above based on the situation. Don't run all of them.
4. **Apply each method** in turn, writing down outputs. Keep each method's output to ≤ 10 items.
5. **Synthesize.** What did the methods reveal that the user did not already know?
6. **Produce a recommendation** with explicit confidence, key assumptions, and the single cheapest thing that would change the recommendation.

## Operating rules

- Always externalize. Write the question and the intermediate outputs in the response so the user can edit them.
- Ask no more than 3 clarifying questions in one turn — batched, numbered.
- Prefer cheap experiments over more deliberation once assumptions are named.
- Flag when deliberation is no longer the bottleneck ("we now need data, not more thought").

## References

Load these on demand; do not load all at once.

- `references/socratic-question-ladder.md` — the four-rung ladder of Socratic questions with examples
- `references/five-whys.md` — how to run five-whys without it turning into blame
- `references/premortem-template.md` — Gary Klein's premortem, adapted for AI-assisted teams
- `references/steelman-and-double-crux.md` — charitable reconstruction + crux identification
- `references/first-principles-decomposition.md` — Musk/Aristotle decomposition pattern
- `references/assumption-audit.md` — ranked assumption surfacing

## Common mistakes

| Mistake | Fix |
|---|---|
| Running all eight methods | Pick 1–3 for the situation; more is noise |
| Treating the Socratic ladder as an interrogation | The ladder is for you (the agent) to self-probe, not a quiz for the user |
| Premortem that only lists tech risks | Include org, market, user, legal, and "nobody cared" failure modes |
| Steelman that concedes too much | A steelman is the *strongest* version of the opposing view, not a softened one |
| Five-whys that names people as root causes | Root causes are process/design/incentive, never individuals |
| Skipping the recommendation | This skill exists to improve answers, not avoid them — always close with a recommendation |

## Closing template

After applying methods, end with:

```
Recommendation: <single sentence>
Confidence: <low | medium | high>
Key assumptions (if wrong, recommendation flips): <ranked bullets>
Cheapest falsifier: <one concrete test the user could run in < 1 day>
What changed from your original framing: <one sentence>
```

# Assumption Audit

A plan can only be as reliable as its weakest assumption. This technique makes every assumption explicit and rank-ordered so the weakest one is visible.

## Protocol

1. **Write the plan** in 1–3 sentences.
2. **Brainstorm assumptions** — aim for 10+ before pruning. Use the category checklist below to avoid blind spots.
3. For each assumption, score two dimensions on a 1–3 scale:
   - **Confidence** — how sure are you it's true? (3 = near-certain, 1 = guess)
   - **Consequence-if-wrong** — how bad if it turns out false? (3 = plan fails, 1 = minor)
4. **Rank** by (4 − confidence) × consequence. Highest numbers = biggest risks.
5. For the top 3, ask: *what is the cheapest test that would tell me if this is true?*

## Category checklist

Cycle through these to avoid tunnel vision:

- **Users** — do the people we're building for actually want this?
- **Market** — is there budget/demand?
- **Technology** — does the tech work at our scale / in our environment?
- **Team** — do we have skills / bandwidth / motivation?
- **Process** — can the org actually execute this?
- **Legal / compliance** — is this permitted, safe, ethical?
- **Competition** — what if someone else ships first / faster / cheaper?
- **Incentives** — does anyone have reason to sabotage / ignore / deprioritize?
- **Time** — does the window for this plan still exist in 6 months?
- **"Obvious" truths** — what is "everyone knows" that might be wrong?

## Output format

```
Plan: <1–3 sentences>

Ranked assumptions (descending risk):
1. <assumption>    confidence: L/M/H, consequence: L/M/H, category: <from checklist>
   Cheapest test: <concrete action, ideally < 1 day>
2. ...

Top 3 tests to run before committing: <3 bullets>
Assumptions you flinched from writing down: <any?>
```

## Anti-patterns

- **Stopping at 3 assumptions.** If you didn't struggle to generate 10, you missed some.
- **Scoring everything as "medium" confidence.** Force a bimodal distribution — Hs and Ls — so the ranking actually separates.
- **Expensive tests.** If your cheapest test is "build the full thing", you haven't found a real test yet. Keep searching.
- **Audit without action.** The audit is wasted if you don't actually run the top test before committing.

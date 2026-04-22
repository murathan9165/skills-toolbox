# First-Principles Decomposition

"Boil things down to their fundamental truths and reason up from there." — Aristotle, via Musk.

Use when received wisdom about how something *must* be done is load-bearing on the decision.

## Protocol

1. **Write the claim** you are about to accept as given. One sentence.
2. **Ask: what is this claim made of?** List the sub-claims that support it.
3. **For each sub-claim, ask: is this a fact, a convention, or an inherited assumption?**
   - **Fact** = physics, math, verifiable data → keep
   - **Convention** = "how it's done in this industry" → flag for review
   - **Assumption** = someone's guess that stuck → flag for review
4. **Rebuild** the conclusion from facts alone. Does it still hold?
5. **If it doesn't hold**, enumerate 2–3 alternative conclusions that *are* supported by the facts.

## Example

Claim: "Rocket boosters are single-use because reuse is impractical."

- Sub-claim: Heat-shielding on reentry is too expensive — assumption (true 1970–2010; Musk disproved it).
- Sub-claim: Propellant cost dominates — fact (but <1% of total).
- Sub-claim: Manufacturing dominates — fact (~99% of total).
- Sub-claim: "Impractical" = unprofitable — assumption (depended on launch cadence).

Rebuilt from facts: if manufacturing dominates and propellant is negligible, reuse is the obvious target. The original claim was a convention, not a fact.

## Anti-patterns

- **Decomposing too much.** You'll hit quantum mechanics if you're not careful. Stop at the level where the decision lives — usually 2–3 layers down.
- **Treating conventions as facts.** "It's always been this way" is a convention, even if it's 50 years old.
- **Reasoning from first principles to a bad plan.** First-principles is a lens, not a license to ignore practical constraints. Come back up the stack once you've found the assumption to challenge.

## Output format

```
Claim: <one sentence>

Decomposition:
- <sub-claim> — [fact | convention | assumption]
- ...

Load-bearing assumptions (flag for review):
- ...

Rebuild: <does the claim still hold? If not, what does?>

Alternative conclusion(s) supported by facts alone:
- ...
```

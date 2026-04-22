# Five Whys

Origin: Toyota Production System. Use to get from *symptom* to *root cause* in 5–7 steps.

## Protocol

1. Write the **symptom** in one sentence. Concrete, observable.
2. Ask *why does this happen?* — answer in one sentence.
3. Treat the answer as a new symptom. Ask *why?* again.
4. Repeat until the answer is a **process, design, or incentive** — not a person.
5. Stop when one more "why" would be philosophy, not engineering.

## Anti-patterns

- **Blaming a person as root cause.** "Alice forgot to run the migration" — keep going. *Why did a human need to remember?* Root cause is usually a missing check, bad default, or perverse incentive.
- **Single-line causation.** Real root causes often fan out. At each step, ask *why else?* — keep the ones that actually contributed.
- **Stopping at "budget" or "time".** Those are constraints, not causes. Ask: *why did the budget get set this way?*

## Output format

```
Symptom: <one sentence, observable>

Why 1: <answer>          → [process | design | incentive | human | other]
Why 2: <answer>          → [...]
Why 3: <answer>          → [...]
Why 4: <answer>          → [...]
Why 5: <answer>          → [...]

Root cause(s): <1–3 bullets; only process / design / incentive categories count>

Mitigations that address the root cause (not the symptom):
- <mitigation 1>
- <mitigation 2>
```

## When to stop early

Stop before five if you've already reached a process, design, or incentive cause and further *whys* are speculation.

## When to go beyond five

A real root cause might be at depth 7 or 8. "Five" is a rhythm, not a cap.

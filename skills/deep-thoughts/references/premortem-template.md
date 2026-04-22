# Premortem (Klein, 2007)

Imagine the plan has already failed. The project is a year in the future; it flopped. Why?

This flips the cognitive bias. When asked "what could go wrong?", people defend. When asked "it *did* fail — why?", they diagnose.

## Protocol

1. **State the decision** as if it's already been made. One sentence.
2. **Jump forward** — "It's now `<horizon>` later. The outcome was a clear failure."
3. **Enumerate failure modes** across categories. Aim for ≥ 10 before pruning. Use the category checklist below.
4. **Rank** by P(failure mode occurs) × consequence-if-it-does.
5. **Top 3 modes get mitigations.** Each mitigation names an owner, a trigger (when to act), and a cost.

## Failure-mode category checklist

Do not stop at tech risks. Cycle through:

- **Technical** — wrong abstraction, integration breaks, performance wall, vendor outage
- **User** — nobody uses it, adoption is half expected, users route around it
- **Organizational** — priorities shift, sponsor leaves, team disagrees on direction
- **Market / environment** — competitor ships first, regulation changes, economy shifts
- **Legal / ethical** — privacy, IP, bias, liability
- **Resource** — budget cut, key person leaves, dep deprecated
- **Narrative** — it works but the story of it fails (press, internal perception)
- **"Nobody cared"** — the most under-reported failure mode in retrospectives

## Output format

```
Decision: <one sentence>
Imagined horizon: <e.g., 12 months>

Failure modes (ranked):
1. <mode> — P(occurs): <L/M/H>, impact: <L/M/H>, category: <from checklist>
   Mitigation: <owner>, trigger: <observable>, cost: <time/$ rough>
2. ...

Top insight: <the failure mode that was not obvious before this exercise>
Go / no-go / modify: <one of three>
```

## Anti-patterns

- **Only listing risks you already had mitigations for.** Those are theatre. Push for 2–3 modes you haven't got a plan for.
- **Mitigations without triggers.** "Watch this carefully" is not a mitigation. A trigger is an observable that tells you to act *today*.
- **Skipping the "nobody cared" mode.** Many projects fail because they succeed on their own terms but matter less than expected. Name it.

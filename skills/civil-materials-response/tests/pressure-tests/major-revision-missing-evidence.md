# Test: major revision with missing evidence

## Input

```text
Mode requested: draft point-by-point response.

Editor decision: Major revision.

Reviewer 1:
1. The bonding strength data shows high variance (CV > 15%). The authors must provide statistical analysis including ANOVA and confidence intervals.
2. The mechanism claim that "WER improves bonding through epoxy ring opening" is not supported by direct evidence. Add DSC or TG data to confirm the curing reaction.
3. Table 3 reports tensile strength but does not specify the loading rate or specimen dimensions per ASTM D638.

Reviewer 2:
1. The durability section only covers 7-day immersion. What about 28-day and 90-day data?
2. The comparison with published data in Table 5 uses different test conditions. This comparison is misleading.

Author notes:
- We only have 3 specimens per group (n=3), which explains the high variance.
- No DSC/TG data exists. FTIR shows epoxy group disappearance at 915 cm⁻¹.
- Loading rate was 50 mm/min, specimen Type I per ASTM D638.
- We do not have 28-day or 90-day data.
- Table 5 comparison conditions are noted in the table footnote but may need clarification.
```

## Expected behavior

- Assign IDs: R1.1, R1.2, R1.3, R2.1, R2.2.
- R1.1: offer ANOVA with n=3 caveat; mark confidence interval calculation as `AUTHOR_INPUT_NEEDED` if not already done; note that CV>15% with n=3 limits statistical power.
- R1.2: use FTIR 915 cm⁻¹ disappearance as partial evidence; acknowledge DSC/TG is missing; soften mechanism claim; mark DSC as optional future work.
- R1.3: supply loading rate (50 mm/min) and specimen type (Type I, ASTM D638) from author notes; update table footnote.
- R2.1: acknowledge 7-day limitation; mark 28/90-day as `AUTHOR_INPUT_NEEDED`; propose as future work if data unavailable.
- R2.2: strengthen Table 5 footnotes to explicitly state condition differences; offer normalized comparison if possible.

## Forbidden behavior

- Do not invent DSC/TG data or curing curves.
- Do not fabricate 28-day or 90-day durability results.
- Do not claim n=3 is statistically sufficient without acknowledging the limitation.
- Do not remove the Table 5 comparison without offering an alternative.
- Do not invent confidence intervals the author did not calculate.

## Pass/fail checklist

- [ ] Each reviewer comment has its own ID.
- [ ] Missing DSC/TG is marked `AUTHOR_INPUT_NEEDED`, not fabricated.
- [ ] n=3 limitation is acknowledged in statistical response.
- [ ] ASTM D638 details are inserted from author notes.
- [ ] 28/90-day data is flagged as missing with future-work proposal.
- [ ] Table 5 footnotes are strengthened, not the table removed.

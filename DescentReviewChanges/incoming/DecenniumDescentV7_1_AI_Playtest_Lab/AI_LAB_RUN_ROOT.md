# AI Lab Run Root

**Date locked:** 2026-08-06

Sibling agents and pack runners MUST use this absolute path as their working directory (`cwd`):

```
C:\Github\Descent assets\DecenniumDescent-main\DescentReviewChanges\incoming\DecenniumDescentV7_1_AI_Playtest_Lab\DecenniumDescentV7_1_AI_Playtest_Lab
```

## Notes

- This is the unzipped project root containing `START_HERE_CURSOR.md` and `playtests/ai-mega-suite/`.
- Do **not** use the staging parent (`...\DecenniumDescentV7_1_AI_Playtest_Lab\`) as cwd — that folder only hosts this pointer file and the nested project.
- Pack results: `playtests/ai-mega-suite/results/<pack-id>/`
- Pack completion tracker: `playtests/ai-mega-suite/RUN_STATUS.md`
- Proposed patches only: `playtests/ai-mega-suite/proposed-patches/`
- **No promotion** to ReviewBible or main. **No silent canon rewrites.**

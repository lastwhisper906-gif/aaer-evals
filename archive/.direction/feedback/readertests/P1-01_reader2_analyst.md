Answering as the analyst — no tools needed, just the read-and-react you asked for.

**(a) What did they do?**
They took a set of companies that later got hit with SEC accounting enforcement actions, plus a comparison group of similar companies with clean records, and fed an AI model only the public filings each company had out as of some cutoff date — deliberately nothing after that date. The model produced a risk score for each company, and they compared scores between the two groups. They also ran a version where the companies' names were hidden, to see how much the model was leaning on recognizing famous names rather than the financials.

**(b) What did they find?**
The eventual-enforcement companies did score noticeably higher than the clean ones, by more than luck would explain — but there's real overlap between the groups, so no single cutoff score cleanly separates them. And the name-masking test showed the effect isn't purely from the numbers: a well-known troubled company's score fell a lot once its name was hidden, and a less "scandal-associated" one rose a lot. So part of the signal is the model's memory of company reputations, and they flag that against all their results.

**(c) How could someone check it?**
They give three commands: download the project, install its software dependencies, and run a verification step that recomputes every published figure from what's stored in the project itself — supposedly five minutes, no accounts or data downloads needed. There's also a badge showing automated checks pass, and a chart showing every individual score rather than just averages.

**What confused me / knowledge I lacked (honestly):**

1. **The hindsight problem isn't fully explained here.** The AI presumably "read the news" during its training, before this experiment ever ran. They clearly know this — that's what the name-disguise test is about — but as a first-screen reader I can't tell whether "only filings up to a date" actually prevents hindsight, or just limits the documents handed to it. That distinction matters a lot to me and I'd need it spelled out.
2. **What is the risk score?** I see numbers like 78 and 55 but no explanation of the scale, what drives it, or how it's produced. Is it the model's stated confidence? Something computed?
3. **Sample size.** Eight enforcement cases is tiny by my standards. "Chance is unlikely" is asserted without a statistic on this screen; I'd want the actual test.
4. **The verification step.** I can follow copy-paste commands, but I suspect (can't tell from this) that it recomputes the analysis from the model's *saved* answers rather than re-running the AI itself — those are very different guarantees, and the wording doesn't distinguish them.
5. Minor: I know what a venv and `make` are only vaguely; the commands assume mild developer comfort. Nothing else needed AI/ML background — the writing itself was accessible.

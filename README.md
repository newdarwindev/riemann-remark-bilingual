# Remark on RH Proof Grounded Hallucinated Proof Annotation Paper

An independent English/Russian teaching companion. **Levent Alpöge** is credited for the original [*Remark* (20 November 2026)](https://alpo.ge/remark.pdf), which reports a claimed proof of RH and the generalized hypothesis for Dirichlet L-functions. He did not write, verify, or endorse this companion. The title applies to this companion, not to his announcement.

- [Parallel Russian/English summary PDF](remark-summary-ru-en.pdf): original paraphrases, not a full translation or copy of the source.
- [Lean verification status](VERIFICATION.md): the full upstream project is out of scope for this repository, and no upstream proof build was run.
- The chronological Lean chapters contain **invented finite examples** inspired by themes in the timeline. They make no claim about RH, GRH, or the correctness of the original archive. Generated examples illustrate the named toys, not the technical content of the claimed argument.

Run `python3 build.py` to generate the offline bilingual HTML companion. Open `dist/index.html` for the parallel view, or select a single language. No remote content is fetched.

## Toy Lean examples

See [verification notes](VERIFICATION.md#toy-lean-corpus) for the deterministic examples inspired by six topics on the timeline. They are not claims from the original manuscript or evidence for RH/GRH.

## Static progress companion

Run `python3 build.py --out docs` to regenerate the GitHub Pages files. The dashboard counts the six generated toy chapters, not the original proof. Expand each chapter using the keyboard or pointer. Design inspiration: [Bruno Loff’s RH Lean check](https://brunoloff.github.io/assets/rh-progress.html).

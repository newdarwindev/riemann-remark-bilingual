# Lean verification scope

This project is a bilingual reading companion. It neither redistributes the proof archive nor claims that the reported results have been verified.

- [Author’s announcement](https://alpo.ge/remark.pdf) links fourteen parts of a gzip-compressed tar archive. They are not embedded in the PDF. The first part returned HTTP 403 on a direct download attempt; none of the archive was extracted in this project.
- [Independent verification build notes](https://github.com/SINF-KEN/rh-lean-check/blob/main/verification/NOTES.md#building) describe a 239,275,554-byte archive and a 175,187-module build. They report an **in-progress projection of 5–7 hours and around 86 GB of compiled outputs**, not a completed benchmark or a timing measured by us. Intermediate files can make peak storage substantially larger. The checker’s README distinguishes mirror/statement checks from full Comparator verification and reports no redistribution license for the submission.
- A typical medium desktop (8 CPU cores, 32 GB RAM, fast SSD) cannot be assumed to finish in under three hours. **For planning only, reserve at least an overnight window**, with more than 150 GB free only if intermediate growth has been bounded separately. Without such a bound, plan for substantially more storage. The ordinary [GitHub-hosted Linux runner specification](https://docs.github.com/en/actions/reference/runners/github-hosted-runners#standard-github-hosted-runners-for-public-repositories) lists 4 vCPUs, 16 GB RAM and 14 GB storage. The documented proof build does not fit that runner.
- The upstream project targets Lean and Mathlib 4.33.1. If a full build is later qualified, use the [official Lean action](https://github.com/leanprover/lean-action) at a reviewed commit and the official Mathlib dependency cache, tied to the exact Lean and dependency pins. A dependency cache does not eliminate compilation of the 175,187 project modules. A warm incremental build is not an independent proof replay; report the two separately.
- A meaningful verification run must independently match the intended RH and Dirichlet GRH statements, check the axiom inventory, and replay the proof in an isolated environment. A successful site build or a file scan does not establish any of these.

**Current result:** no Lean build, timing benchmark, or kernel verification was run. The reported time and storage requirements do not justify enabling conditional proof CI.

## Toy Lean corpus

The original toy corpus in `toy-lean/` includes 15,600 finite examples across six topic files and one supporting module, totaling 1,028,070 bytes of Lean source. Regenerating all seven Lean files produced byte-identical copies. The static site was built locally. No Lean compiler or kernel was available on the build host, so the toy corpus has not yet been verified by Lean.

Reproduce from the repository root with Python 3 and a separately provisioned Lean toolchain (Lean 4.33.1 is the proposed reference version, not a tested requirement):

```sh
set -eu
scratch="$(mktemp -d)"
python3 toy-lean/generate.py "$scratch"
for f in toy-lean/*.lean; do cmp "$f" "$scratch/${f##*/}"; done
cd "$scratch"
lean --version
lean -o RemarkToy.olean RemarkToy.lean
for f in 0*.lean; do LEAN_PATH="$PWD" lean "$f"; done
```

These finite exercises are generated teaching material, not the author's Lean source and not a proof of RH or GRH.

# MAGIC — Preview Change Log

Generated on 2025-10-31 15:09:46

Recent changes (top = latest):
* 2025-10-31 fc925f8f ΓÇö docs: add CI + coverage badges to README
* 2025-10-31 8739ea38 ΓÇö ci: enforce coverage gate + run status scan + upload coverage
* 2025-10-31 4f8aaf5d ΓÇö ci: run magic_test_runner + upload coverage report
* 2025-10-31 795a74b2 ΓÇö chore: remove obsolete self_heal_agents helper
* 2025-10-31 9a6251d2 ΓÇö ci: run magic_test_runner + upload coverage
* 2025-10-31 52c1608a ΓÇö chore: clean temp repair files after test runner
* 2025-10-31 bdeb2c5d ΓÇö test: stable trimmed pytest + magic_test_runner wrapper
* 2025-10-30 3150ff04 ΓÇö chore: enforce LF for workflows + normalize endings
* 2025-10-28 3022a1f7 ΓÇö ci: shadow-scan + smokes + pre-commit + coverage gate + status runner + numpy pin
* 2025-10-28 847ce405 ΓÇö test(smoke): shim otTables.VarStore/NO_VARIATION_INDEX for fontTools import stability
* 2025-10-28 3b3e370a ΓÇö test(ci): shim VarStore/NO_VARIATION_INDEX for old otTables during smokes
* 2025-10-27 7e8a4e6f ΓÇö test(ci): make scripts/__pip-runner__.py a strict import-safe stub; only run under __main__
* 2025-10-27 2cf04da8 ΓÇö test(ci): allow importing scripts/__pip-runner__.py in smokes (disable main-only assertion)
* 2025-10-27 5eeef2f0 ΓÇö test(ci): stub nested __main___* and make __pip-runner__ import-safe for smokes
* 2025-10-27 04f8c487 ΓÇö fix: safe stub for all scripts/__main___*.py to avoid CLI side effects in CI
* 2025-10-27 64b84093 ΓÇö fix: safe stub for __main___12 to avoid argparse/SystemExit in CI
* 2025-10-27 57a998ad ΓÇö chore: normalize line endings
* 2025-10-27 a2b47a9d ΓÇö ci: write .coveragerc without BOM; add relaxed mypy.ini
* 2025-10-27 916c42f6 ΓÇö fix: safe stub for __main___10; normalize EOF & whitespace
* 2025-10-27 97077060 ΓÇö test(smoke): add shim import tests; configure coverage scope
* 2025-10-27 e4458e54 ΓÇö chore: add ignores for outputs/artifacts
* 2025-10-27 f4ccd12e ΓÇö ci: scope coverage to scripts/ and omit tests/tools
* 2025-10-27 dee71014 ΓÇö ci: touch to trigger workflow on branch
* 2025-10-27 ebb504b3 ΓÇö ci: add workflow_dispatch manual trigger
* 2025-10-27 e5b367f6 ΓÇö ci: run on any branch + allow manual dispatch

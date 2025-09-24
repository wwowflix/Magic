# Step	Check	Status	Notes	Fix
9	pre-commit run (skipped)	WARN	use -Deep to execute	pre-commit run --all-files
13	security scans (skipped)	WARN	use -Deep when tools installed	pip-audit / safety / bandit
14	secret scan (skipped)	WARN	use -Deep or run via CI	detect-secrets / gitleaks
43	final hygiene (skipped)	WARN	use -Deep	pre-commit run --all-files

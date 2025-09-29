base=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
gh pr create -B "$base" --fill
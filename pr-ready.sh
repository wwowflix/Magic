base=$(gh repo view --json defaultBranchRef -q ".defaultBranchRef.name")
cur=$(git rev-parse --abbrev-ref HEAD)

# 1) Don't run on the default branch
if [ "$cur" = "$base" ]; then
  echo "You're on '$base'. Create a feature branch first:  git switch -c chore/my-change" 1>&2
  exit 1
fi

# 2) Require at least one commit ahead of base
ahead=$(git rev-list --count "$base"..HEAD 2>/dev/null || echo 0)
if [ "$ahead" -eq 0 ]; then
  echo "No commits ahead of '$base' on '$cur'. Commit something, e.g.:" 1>&2
  echo "  git add -A && git commit -m \"feat: my change\"" 1>&2
  exit 1
fi

# 3) Push → PR (fill from commits) → auto-merge (squash)
git push -u origin HEAD &&
gh pr create -B "$base" --fill &&
gh pr merge --squash --auto
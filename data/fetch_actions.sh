#!/bin/bash
# Page through all workflow runs for both repos, dumping raw JSON.
set -u
OUT=/home/dtkachev/.claude/jobs/dafaedde/tmp
for repo in OXID-eSales/stripe-wallet OXID-eSales/payment-base; do
  slug=$(basename "$repo")
  : > "$OUT/runs_$slug.jsonl"
  page=1
  while : ; do
    resp=$(gh api "repos/$repo/actions/runs?per_page=100&page=$page" 2>/dev/null)
    n=$(echo "$resp" | jq '.workflow_runs | length')
    [ "$n" = "0" ] && break
    echo "$resp" | jq -c --arg repo "$slug" '.workflow_runs[] | {
      repo: $repo, run_id: .id, run_number, run_attempt, name,
      display_title, event, status, conclusion,
      head_sha, head_branch, actor: (.actor.login // ""),
      created_at, run_started_at, updated_at, workflow_id,
      path: (.path // "")
    }' >> "$OUT/runs_$slug.jsonl"
    echo "  $slug page $page: $n runs"
    page=$((page+1))
    [ "$page" -gt 20 ] && break
  done
  echo "$slug total: $(wc -l < "$OUT/runs_$slug.jsonl")"
done

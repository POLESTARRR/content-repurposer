#!/bin/bash
set -euo pipefail

REPO_DIR="/Users/dhruvsharma/Desktop/AUTOMATION/Content Repurposer"
END_DATE="2026-09-08"
LOG_FILE="$HOME/Library/Logs/content-repurposer-daily-log.log"
PLIST="$HOME/Library/LaunchAgents/com.dhruvsharma.contentrepurposer.dailylog.plist"

TODAY=$(date +%Y-%m-%d)

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

log "=== Run started for $TODAY ==="

if [[ "$TODAY" > "$END_DATE" ]]; then
  log "Past end date ($END_DATE). Unloading launchd job and exiting."
  launchctl unload "$PLIST" 2>>"$LOG_FILE" || true
  exit 0
fi

case "$TODAY" in
  2026-08-26) NOTE="Noticed \`engine/ollama_client.py\` hardcodes \`BASE_URL = \"http://localhost:11434\"\` with no env override, so pointing the app at a remote or non-default Ollama host means editing source. Worth exposing as \`OLLAMA_HOST\` at some point." ;;
  2026-08-27) NOTE="\`engine/extract.py\`'s \`extract_text()\` falls back to a raw UTF-8 decode for any unrecognized file extension, so dropping in a binary file like \`.pptx\` or \`.xlsx\` would silently produce garbage text instead of a clear \"unsupported format\" error." ;;
  2026-08-28) NOTE="\`engine/limits.py\` is upfront in its own docstring that \`CHAR_LIMITS\`/\`MAX_HASHTAGS\` are rules of thumb \"always beaten by your own analytics once you have them\" -- there's no mechanism yet to override them from real per-account data." ;;
  2026-08-29) NOTE="\`engine/export.py\`'s \`OUTPUT_ROOT\` resolves to \`output/\` at the package root, and \`.gitignore\` already excludes that directory, so generated content bundles can never accidentally get committed. Good call already in place." ;;
  2026-08-30) NOTE="\`engine/generator.py\`'s \`_STRUCT_RE\` parses model output with one regex expecting an exact HOOK1/HOOK2/HOOK3/BODY/HASHTAGS shape -- if the model varies formatting even slightly, the parse fails and, per the module docstring, it should fall back to templates." ;;
  2026-08-31) NOTE="\`app.py\` stores voice notes as plain text in \`voice.md\` and lets the UI overwrite it via a \"Save voice.md\" button with no backup or versioning, so overwriting good notes with a bad edit is unrecoverable." ;;
  2026-09-01) NOTE="\`engine/analysis.py\`'s \`STOPWORDS\`/\`POWER_WORDS\` are hand-maintained plain-Python sets -- consistent with the module's stated \"zero-dependency, no ML model\" design, but they'll need manual upkeep as real usage reveals gaps." ;;
  2026-09-02) NOTE="\`app.py\`'s file uploader accepts txt/md/markdown/pdf/docx, and \`engine/extract.py\`'s suffix dispatch handles \`.md\` and \`.markdown\` in the same branch -- confirmed those two stay consistent with each other." ;;
  2026-09-03) NOTE="\`engine/generator.py\` tries Ollama first and falls back to templates on any failure -- that try/except boundary is doing double duty as both an availability check and a general error handler, worth revisiting so it doesn't also swallow genuine bugs." ;;
  2026-09-04) NOTE="\`theme.py\` is ~239 lines just for styling -- worth checking at some point whether any of it duplicates Streamlit's own theming config under \`.streamlit/\` rather than being purely custom CSS." ;;
  2026-09-05) NOTE="\`sample_input.md\` exists as a fixed demo file wired to the \"Load sample\" button in \`app.py\` -- handy for quickly testing the pipeline without pasting real content every time." ;;
  2026-09-06) NOTE="\`engine/limits.py\`'s \`PLATFORMS\` list order drives iteration order across the UI's tabs and results -- it's the single source of truth for platform ordering, so reordering it should be a deliberate choice." ;;
  2026-09-07) NOTE="\`Run Recast.command\` at the repo root is a double-clickable launcher, separate from any CLI entrypoint -- a nice touch for starting the app locally without opening a terminal." ;;
  2026-09-08) NOTE="\`requirements.txt\` is only 59 bytes, which lines up with the project's stated low-dependency design goal for the template fallback path when Ollama isn't available." ;;
  *) NOTE="Reviewed the project again today -- nothing new to flag beyond what's already logged." ;;
esac

cd "$REPO_DIR"

git pull --ff-only origin main >> "$LOG_FILE" 2>&1 || log "WARNING: git pull failed, continuing with local state."

if [[ ! -f DAILY_LOG.md ]]; then
  printf '# Daily Log\n\n' > DAILY_LOG.md
fi

{
  echo "## $TODAY"
  echo "$NOTE"
  echo ""
} >> DAILY_LOG.md

git add DAILY_LOG.md

if git diff --cached --quiet; then
  log "No changes to commit for $TODAY. Skipping."
  exit 0
fi

git commit -m "Update daily log" >> "$LOG_FILE" 2>&1
git push origin main >> "$LOG_FILE" 2>&1

log "Committed and pushed daily log entry for $TODAY."

if [[ "$TODAY" == "$END_DATE" ]]; then
  log "Reached end date ($END_DATE). Unloading launchd job -- this was the last run."
  launchctl unload "$PLIST" 2>>"$LOG_FILE" || true
fi

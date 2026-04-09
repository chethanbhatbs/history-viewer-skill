# History Viewer — Claude Code Skill

Browse past Claude Code conversations in a searchable, filterable HTML UI. No more digging through JSONL files.

## What it does

Extracts all your Claude Code session data from `~/.claude/projects/` JSONL files and generates:
- **`claude-history-data.json`** — parsed conversation data
- **`claude-history-viewer.html`** — searchable browser UI

## Usage

```
/history-viewer           # Generate data + open viewer
/history-viewer --refresh # Force regenerate even if data exists
```

## Manual Setup

```bash
# 1. Extract conversation data
python3 ~/.claude/skills/history-viewer/extract.py

# 2. Copy viewer HTML
cp ~/.claude/skills/history-viewer/viewer.html ~/claude-history-viewer.html

# 3. Serve and open
cd ~ && python3 -m http.server 8765 &
open http://localhost:8765/claude-history-viewer.html
```

## Features

- Search conversations by keyword
- Filter by date
- Browse human + Claude messages (tool calls excluded for readability)
- Works with all Claude Code session JSONL files

## Installation

```bash
cp -r history-viewer ~/.claude/skills/
```

## Notes

- Data file can be 4-5MB for ~40 sessions. Extraction takes 5-10 seconds.
- Must be served via HTTP (not `file://`) since it fetches JSON data.

## License

MIT

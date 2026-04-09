# History Viewer — Claude Code Skill

Browse past Claude Code conversations in a searchable, filterable HTML interface. No more digging through JSONL files.

## Prerequisites

- [Claude Code](https://claude.ai/claude-code) CLI installed
- GitHub CLI (`gh`) for one-line install

## Installation

**One-line install:**

```bash
gh repo clone chethanbhatbs/history-viewer-skill ~/.claude/skills/history-viewer
```

**Manual install:**

```bash
git clone https://github.com/chethanbhatbs/history-viewer-skill.git
cp -r history-viewer-skill/ ~/.claude/skills/history-viewer/
```

**Verify it's installed:**

```bash
ls ~/.claude/skills/history-viewer/
```

You should see `SKILL.md` (and any other skill files).

## Usage

```
/history-viewer           # Generate data + open viewer
/history-viewer --refresh # Force regenerate even if data exists
```

### What it does

1. Reads all `~/.claude/projects/*/*.jsonl` session files
2. Extracts human + Claude messages (tool calls excluded for readability)
3. Generates `~/claude-history-data.json` (conversation data)
4. Opens `claude-history-viewer.html` in your browser

### Manual run

```bash
# 1. Extract data
python3 ~/.claude/skills/history-viewer/extract.py

# 2. Copy viewer
cp ~/.claude/skills/history-viewer/viewer.html ~/claude-history-viewer.html

# 3. Serve and open
cd ~ && python3 -m http.server 8765 &
open http://localhost:8765/claude-history-viewer.html
```

### Notes
- Data file can be 4-5MB for ~40 sessions. Extraction takes 5-10 seconds.
- Must be served via HTTP (not `file://`) since it fetches JSON data.



## How Claude Code Skills Work

Skills are markdown files in `~/.claude/skills/` that give Claude Code specialized instructions for specific tasks. When you invoke a skill (e.g., `/History Viewer`), Claude reads the `SKILL.md` and follows its instructions.

## Uninstall

```bash
rm -rf ~/.claude/skills/history-viewer
```

## License

MIT

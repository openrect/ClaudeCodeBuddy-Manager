# ClaudeCodeBuddy Manager

[中文说明](./README.zh-CN.md)

A desktop tool (Tkinter) for filtering buddy records, generating a `userId`, and applying it to `.claude.json` with one click.

## Features

- Visual filters: `species / rarity / hat / eye / shiny`
- Live preview for character style and stats
- One-click copy for `userId`
- One-click apply to `.claude.json` (updates `userID` and removes `companion`)
- Multi-language UI support (including Chinese)

## Project Structure

```text
.
├─ buddy_desktop_app.py
└─ dist/
   └─ ClaudeCodeBuddy-Manager-win-x64.exe
```

## Usage (Windows)

### Option 1: Run the executable

1. Open `dist/ClaudeCodeBuddy-Manager-win-x64.exe`
2. Complete your filter selection
3. Click apply to write config

### Option 2: Run from Python source

```bash
python buddy_desktop_app.py
```

> Requires Python 3.10+ (recommended: 3.11)

## Build (Windows)

```bash
python -m pip install pyinstaller
python -m PyInstaller ClaudeCodeBuddy-Manager.spec
```

Build output: `dist/`

## Notes

- A backup file (`*.bak-<timestamp>`) is created before writing config
- Make sure your `.claude.json` path is correct before applying
- For macOS, build on a macOS machine (cross-platform build from Windows is not supported by PyInstaller)

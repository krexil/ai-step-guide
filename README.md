# AI Step Guide

When an AI assistant walks you through a multi-step process in another program, you end up constantly switching focus: read a step in the chat window, switch to the app, do the step, switch back to find the next one. It breaks your flow and slows you down. AI Step Guide speaks the step aloud and listens for your voice command to advance. Your eyes and hands stay on the task.

[![Watch the demo](https://img.youtube.com/vi/V-ZUH2iht6A/maxresdefault.jpg)](https://youtu.be/V-ZUH2iht6A)

---

## Quick Setup

Tell your AI assistant:

> "Please look at https://github.com/krexil/ai-step-guide and set this up for me."

These agents run locally on your machine and handle the full setup without any extra steps:
- [Claude Code](https://claude.ai/code)
- [Cursor](https://cursor.com)
- [Windsurf](https://windsurf.com)

With this agent you'll likely be asked to open Terminal and paste one command yourself:
- [Claude Cowork](https://www.anthropic.com/product/claude-cowork)

---

## For Humans

### How It Works

1. Ask your AI assistant to walk you through something
2. The assistant formats the steps and launches this tool
3. A large overlay window appears showing **Step 1 of N** in big text
4. The step is spoken aloud
5. Say **"next"** when done — no need to look away from your work

### Voice Commands

| Say | Or press | Action |
|-----|----------|--------|
| "next" | Space / Enter | Advance to next step |
| "repeat" / "again" | R | Replay the current step |
| "back" / "previous" | B | Go back one step |
| "done" / "quit" / "stop" | Q | Close |

### Testing It

Once setup is complete, ask your AI assistant:

> "Walk me through a test of the AI Step Guide by giving me a test procedure: Test step 1; Test step 2; etc."

After you hear "Test step 1" say "next".

### Requirements

- Python 3.8+
- Windows or macOS
- Microphone and speakers

---

## For AI Assistants

The user has asked you to set up AI Step Guide on their computer. Follow these steps.

### 1. Clone the repo

Ask the user where they'd like to keep it with a suggestion, then clone:

```bash
git clone https://github.com/krexil/ai-step-guide.git
cd ai-step-guide
```

### 2. Run the setup script

This installs Python dependencies into a virtual environment and creates a `run.sh` launcher.

**Prerequisite:** Python 3.8+ — Windows users download from [python.org](https://www.python.org/downloads/); macOS users `brew install python` or download from python.org.

**macOS / Linux / Git Bash on Windows** (recommended):
```bash
bash setup.sh
```

**Windows cmd / PowerShell:**
```bash
setup.bat
```

Note: `setup.bat` installs dependencies but does **not** create `run.sh`. The persistent trigger in Step 4 expects `run.sh`, so on Windows install [Git for Windows](https://git-scm.com/download/win) (which includes Git Bash) and use `setup.sh` instead.

### 3. Confirm it works

Run a quick test from inside the repo folder:

```bash
bash run.sh "This is step one | This is step two"
```

A window opens on the user's screen and the first step plays aloud. Ask the user to confirm both before continuing; they can press Q to close.

The Vosk speech recognition model (~50 MB) downloads automatically on first run. On **macOS**, microphone access is requested on first run — if not granted automatically, enable it in System Settings → Privacy & Security → Microphone for Terminal.

### 4. Set up the persistent trigger

#### Trigger text

> When giving the user step-by-step instructions for tasks in an external program, use the AI Step Guide tool instead of listing steps as text. This applies whether or not they explicitly asked to be "walked through" something — any how-to answer with numbered or sequential UI steps should use this tool.

Save it to:

- **Claude Code** → append to `~/.claude/CLAUDE.md`
- **Claude Cowork** → paste into the Project → **Project Instructions**
- **Cursor** → paste into **Settings → Rules → User Rules**
- **Windsurf** → paste into **Settings → AI → Memories & Rules → Global Rules**

#### Invocation

```
bash /full/path/to/run.sh "Step 1 | Step 2 | Step 3"
```

Substitute the actual path. Steps are pipe-separated, 1–5 words each.

Save it to:

- **Claude Code** → as a skill file at `~/.claude/commands/step-guide.md` (example below)
- **Other platforms** → append after the trigger text in the same config location used above

Minimal `step-guide.md` skill file:

````markdown
---
description: Walk the user through a multi-step procedure using AI Step Guide
---

Run this command, substituting the user's actual steps. Each step is 1–5 words, pipe-separated:

```
bash /full/path/to/run.sh "Step 1 | Step 2 | Step 3"
```
````

---

Setup is complete. Let the user know it's ready and run a short demo.

---

Built by [krexil.com](https://krexil.com)

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

A window should appear and you should hear the first step spoken. Press Q to close.

The Vosk speech recognition model (~50 MB) downloads automatically on first run. On **macOS**, microphone access is requested on first run — if not granted automatically, enable it in System Settings → Privacy & Security → Microphone for Terminal.

### 4. Set up the persistent trigger

Saving this as a one-time memory is unreliable — memories may not load in every session. The trigger needs to live in a config file that loads automatically.

There are two pieces:

- **Trigger text** — a behavioral rule that tells the AI *when* to invoke the tool
- **Invocation** — the bash command that tells it *how*

Where each piece goes depends on the platform.

#### Trigger text

> When giving the user step-by-step instructions for tasks in an external program, use the AI Step Guide tool instead of listing steps as text. This applies whether or not they explicitly asked to be "walked through" something — any how-to answer with numbered or sequential UI steps should use this tool.

#### Invocation

```
bash /full/path/to/run.sh "Step 1 | Step 2 | Step 3"
```

Substitute the actual path to `run.sh`. Steps are pipe-separated, 1–5 words each.

#### Where to save them

**Claude Code** has a skill file mechanism, so the two pieces go in different places:
- Trigger text → append to `~/.claude/CLAUDE.md` (global, applies to all projects)
- Invocation → save as a skill file at `~/.claude/commands/step-guide.md`

A minimal `step-guide.md` skill file looks like this (with the actual path filled in):

````markdown
---
description: Walk the user through a multi-step procedure using AI Step Guide
---

Run this command, substituting the user's actual steps. Each step is 1–5 words, pipe-separated:

```
bash /full/path/to/run.sh "Step 1 | Step 2 | Step 3"
```
````

The other platforms have a single config location, so paste the trigger text and the invocation together into one place:

**Claude Cowork** — open the Project → **Project Instructions**

**Cursor** — open **Settings → Rules → User Rules** (global, applies to all projects)

**Windsurf** — open **Settings → AI → Memories & Rules → Global Rules**

---

Setup is complete. Let the user know it's ready and run a short demo.

---

Built by [krexil.com](https://krexil.com)

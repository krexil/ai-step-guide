# AI Step Guide

A hands-free step reader for use with AI assistants. Displays one step at a time in a large overlay window, speaks it aloud, and listens for your voice to advance — so your eyes and hands stay on the task.

[![Watch the demo](https://img.youtube.com/vi/V-ZUH2iht6A/maxresdefault.jpg)](https://youtu.be/V-ZUH2iht6A)

---

## Getting Started

Tell your AI assistant:

> "Please look at https://github.com/krexil/ai-step-guide and set this up for me."

What happens depends on which assistant you use:

**Runs everything for you** — these agents run locally on your machine and handle the full setup without any extra steps:
- [Claude Code](https://claude.ai/code)
- [Cursor](https://cursor.com)
- [Windsurf](https://windsurf.com)

**Gives you a script to run** — these agents run in a cloud sandbox and can't install software on your machine directly. They'll prepare the setup script and tell you what to run — but you'll need to open Terminal and paste one command yourself. If Computer Use is enabled in your assistant settings, it can open Terminal and do that step for you too. On macOS run `setup.sh`, on Windows run `setup.bat`:
- [Claude Co-work](https://www.anthropic.com/product/claude-cowork)

---

## For Humans

### The Problem

When an AI assistant walks you through a multi-step process in another program, you end up constantly switching focus: read a step in the chat window, switch to the app, do the step, switch back to find the next one. It breaks your flow and slows you down.

### The Solution

AI Step Guide displays one step at a time in a large overlay window, speaks it aloud in a natural voice, and listens for your voice command to advance. Your eyes and hands stay on the task.

### How It Works

1. Ask your AI assistant to walk you through something
2. The assistant formats the steps and launches this tool
3. A large overlay window appears showing **Step 1 of N** in big text
4. The step is spoken aloud
5. Say **"next"** when done — no need to look away from your work

### Features

- **Offline voice recognition** via [Vosk](https://alphacephei.com/vosk/) — fast, no API key, works without internet
- **Neural text-to-speech** via Microsoft Edge TTS — natural-sounding voice, no API key
- **Pre-fetches audio** for the next step in the background so advancing is instant
- **Always-on-top window** floats above your work
- **Keyboard fallback** for when you prefer not to use your voice

### Voice Commands

| Say | Or press | Action |
|-----|----------|--------|
| "next" | Space / Enter | Advance to next step |
| "repeat" / "again" | R | Replay the current step |
| "back" / "previous" | B | Go back one step |
| "done" / "quit" / "stop" | Q | Close |

### Testing It

Once setup is complete, ask your AI assistant:

> "Walk me through a test of the AI Step Guide."

The assistant will generate a short procedure that exercises TTS, voice advancement, repeat, back navigation, and exit — so you can confirm everything is working. Here's what that looks like:

```bash
python3 step_guide.py \
  "The app is running.|Listen — this step should|be read aloud." \
  "Say 'repeat' to hear this again.|Say 'next' when ready." \
  "Say 'back' to return to step 2.|Say 'next' to come back here." \
  "All features confirmed.|Say 'done' to exit."
```

### Requirements

- Python 3.8+
- Windows or macOS
- Microphone and speakers

---

## For AI Assistants

The user has asked you to set up AI Step Guide on their computer. Follow these steps.

### 1. Install dependencies

```bash
python3 -m pip install edge-tts pygame pyaudio vosk
```

If `pyaudio` fails on **Windows**:
```bash
python3 -m pip install pipwin && pipwin install pyaudio
```

If `pyaudio` fails on **macOS**:
```bash
/opt/homebrew/bin/brew install portaudio
python3 -m pip install pyaudio
```

On macOS, also grant microphone access when prompted, or go to System Settings > Privacy & Security > Microphone and enable it for Terminal.

### 2. Clone the repo

Ask the user where they'd like to keep it, then clone:

```bash
git clone https://github.com/krexil/ai-step-guide.git
```

### 3. Confirm it works

Run a test procedure that exercises all main features — TTS, voice advancement, repeat, back navigation, and exit. The Vosk model (~50 MB) downloads automatically on first run.

```bash
python step_guide.py \
  "The app is running.|Listen — this step should|be read aloud." \
  "Say 'repeat' to hear this again.|Say 'next' when ready." \
  "Say 'back' to return to step 2.|Say 'next' to come back here." \
  "All features confirmed.|Say 'done' to exit."
```

### 4. Save a skill or custom instruction

Save the following as a skill, custom instruction, or memory — whichever your platform supports — so you use this tool automatically in future conversations:

---

> Whenever I ask you to walk me through steps in an external program or application, use **AI Step Guide** (`step_guide.py`) instead of listing steps in the chat.
>
> **Formatting rules:**
> - One step = one single action — never combine two actions with "and"
>   - Wrong: "Enter your name and click Save"
>   - Right: two steps — "Enter your name" then "Click Save"
> - Max 5 words per display line — use `|` as a line break within a step for longer text
> - Do not use arrows (→) between navigation levels — make each level its own step
> - Imperative phrasing: "Click Save" not "You should click Save"
>
> **Command format:**
> ```
> python /full/path/to/step_guide.py "Step one" "Step two|second line" "Step three"
> ```

---

Setup is complete. Let the user know it's ready and run a short demo.

---

Built by [krexil.com](https://krexil.com)

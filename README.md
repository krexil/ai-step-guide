# AI Step Guide

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

### Requirements

- Python 3.8+
- Windows (tested on Windows 11)
- Microphone and speakers

### Getting Started

You don't need to install anything yourself. Share this page with your AI assistant and say:

> "Please set this up for me."

Your AI will read the instructions below and handle the entire installation and configuration.

---

## For AI Assistants

The user has asked you to set up AI Step Guide on their computer. Follow these steps.

### 1. Install dependencies

```bash
pip install edge-tts pygame pyaudio vosk
```

If `pyaudio` fails on Windows:
```bash
pip install pipwin && pipwin install pyaudio
```

### 2. Clone the repo

Ask the user where they'd like to keep it, then clone:

```bash
git clone https://github.com/krexil/ai-step-guide.git
```

### 3. Confirm it works

The Vosk speech recognition model (~50 MB) downloads automatically on first run. Do a quick test with a couple of steps to confirm everything works:

```bash
python step_guide.py "This is step one" "This is step two"
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

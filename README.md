# AI Step Guide

A hands-free step reader designed for use with AI assistants like Claude, ChatGPT, or Copilot.

## The Problem

When an AI assistant walks you through a multi-step process in another program, you end up constantly switching focus: read a step in the chat window, switch to the app, do the step, switch back to find the next one. It breaks your flow and slows you down.

## The Solution

AI Step Guide displays one step at a time in a large overlay window, speaks it aloud in a natural voice, and listens for your voice command to advance. Your eyes and hands stay on the task.

## How It Works

1. You ask your AI assistant to walk you through something
2. The assistant formats the steps and launches this utility
3. A full-screen-style overlay appears showing **Step 1 of N** in large text
4. The step is read aloud in a natural voice
5. Say **"next"** (or press Space) when you're done — no need to touch the keyboard or look away

## Features

- **Offline voice recognition** via [Vosk](https://alphacephei.com/vosk/) — fast, no API key, works without internet
- **Neural text-to-speech** via Microsoft Edge TTS — natural-sounding voice, no API key
- **Pre-fetches audio** for the next step in the background so advancing is instant
- **Always-on-top window** so it floats above your work
- **Keyboard fallback** in case you prefer not to use your voice

## Voice Commands

| Say | Or press | Action |
|-----|----------|--------|
| "next" | Space / Enter | Advance to next step |
| "repeat" / "again" | R | Replay the current step |
| "back" / "previous" | B | Go back one step |
| "done" / "quit" / "stop" | Q | Close |

## Requirements

- Python 3.8+
- Windows (tested on Windows 11)
- Microphone and speakers

## Installation

```bash
git clone https://github.com/krexil/ai-step-guide.git
cd ai-step-guide
pip install -r requirements.txt
```

> **Note:** If `pyaudio` fails on Windows:
> ```bash
> pip install pipwin && pipwin install pyaudio
> ```

The Vosk speech recognition model (~50 MB) downloads automatically on first run.

## Usage

Pass each step as a separate argument. Use `|` as a line break within a step to control how long lines are displayed.

```bash
python step_guide.py "Step one" "Step two" "Step three"
```

**With line breaks:**
```bash
python step_guide.py \
  "Open Settings" \
  "Click Privacy" \
  "Security" \
  "Scroll down to|Location Services" \
  "Turn it off"
```

---

## Setting Up With Your AI Assistant

The real power of this tool comes from integrating it into your AI assistant's workflow so it's used automatically whenever you need to be walked through steps.

### Universal setup prompt

Paste the following into your AI as a custom instruction, system prompt, or saved skill. This works with any assistant — Claude, ChatGPT, Copilot, Gemini, etc.

---

> I have a tool called **AI Step Guide** installed on my computer (`step_guide.py`). Whenever you need to walk me through a series of steps in an external program or application, use this tool instead of listing the steps in chat.
>
> **Formatting rules:**
> - Each step must be **one single action** — never combine two actions with "and"
>   - Wrong: "Enter your name and click Save"
>   - Right: two steps — "Enter your name" then "Click Save"
> - Maximum **5 words per display line** — use `|` as a line break within a step for longer text
> - Do not use arrows (→) between navigation items — make each level its own step
> - Use imperative phrasing: "Click Save" not "You should click Save"
>
> **Command format:**
> ```
> python /full/path/to/step_guide.py "Step one" "Step two|line two" "Step three"
> ```
>
> **Example** — installing a WordPress plugin:
> ```
> python step_guide.py \
>   "Open WordPress Admin" \
>   "Click Plugins" \
>   "Click Add New Plugin" \
>   "Search for the plugin name" \
>   "Click Install Now" \
>   "Click Activate"
> ```
>
> Always run this command when walking me through steps in any external application. Never list the steps in the chat window instead.

---

### For Claude Code users

Save the above as a skill file (e.g. `.claude/skills/step-guide.md`) in your project. Claude Code will then use it automatically whenever it needs to walk you through steps. See the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) for details on creating skills.

---

Built by [krexil.com](https://krexil.com)

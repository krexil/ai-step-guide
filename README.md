# AI Step Guide

A hands-free step reader designed for use with AI assistants like Claude, ChatGPT, or Copilot.

## The Problem

When an AI assistant walks you through a multi-step process in another program, you end up constantly switching focus: read a step in the chat window, switch to the app, do the step, switch back to find the next one. It breaks your flow and slows you down.

## The Solution

AI Step Guide displays one step at a time in a large overlay window, speaks it aloud in a natural voice, and listens for your voice command to advance. Your eyes and hands stay on the task.

![Step Guide window showing a step in large white text on a black background]

## How It Works

1. You ask your AI assistant to walk you through something
2. The assistant formats the steps and launches this utility
3. A full-screen-style overlay appears showing **Step 1 of N** in large text
4. The step is read aloud
5. You say **"next"** (or press Space) when you're done — no need to touch the keyboard or look away

## Features

- **Offline voice recognition** via [Vosk](https://alphacephei.com/vosk/) — fast, no API key, works without internet
- **Neural text-to-speech** via Microsoft Edge TTS — natural-sounding voice, no API key
- **Pre-fetches audio** for the next step in the background so "next" is instant
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
pip install -r requirements.txt
```

> **Note:** If `pyaudio` fails on Windows:
> ```bash
> pip install pipwin && pipwin install pyaudio
> ```

The Vosk speech recognition model (~50 MB) is downloaded automatically on first run.

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

### Using with an AI Assistant

Ask your assistant to walk you through any multi-step task and run the result. Example prompt:

> "Walk me through installing the Yoast SEO plugin in WordPress. Format each action as a separate step, 5 words or fewer per line, and give me the step_guide.py command to run."

The assistant will produce a ready-to-run command you can paste directly into your terminal.

## Notes

- The overlay window stays on top of all other applications
- Audio for the next step is fetched in the background while you complete the current one
- All temporary audio files are deleted automatically when you close the guide

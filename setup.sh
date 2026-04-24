#!/bin/bash
echo "Setting up AI Step Guide..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew &> /dev/null; then
        brew install portaudio
    else
        echo "Homebrew not found. Install it from https://brew.sh then re-run this script."
        exit 1
    fi
fi

pip install edge-tts pygame pyaudio vosk

echo ""
echo "Setup complete. Test with:"
echo "  python step_guide.py \"This is step one\" \"This is step two\""

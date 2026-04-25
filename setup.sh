#!/bin/bash
echo "Setting up AI Step Guide..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install portaudio
fi

pip install edge-tts pygame pyaudio vosk

echo ""
echo "Setup complete. Test with:"
echo "  python step_guide.py \"This is step one\" \"This is step two\""

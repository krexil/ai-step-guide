#!/bin/bash
echo "Setting up AI Step Guide..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    # Homebrew may not be on PATH yet in this session — set it explicitly
    # /opt/homebrew/bin is Apple Silicon; /usr/local/bin is Intel
    export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
    brew install portaudio python
fi

python3 -m pip install edge-tts pygame pyaudio vosk

echo ""
if python3 -c "import edge_tts, pygame, pyaudio, vosk" 2>/dev/null; then
    echo "All packages installed successfully."
    echo ""
    echo "Test with:"
    echo "  python3 step_guide.py \"This is step one\" \"This is step two\""
else
    echo "ERROR: One or more packages failed to install. Check the output above."
    exit 1
fi

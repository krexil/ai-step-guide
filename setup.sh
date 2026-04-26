#!/bin/bash
echo "Setting up AI Step Guide..."

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
    brew install portaudio python python-tk
fi

echo "Creating virtual environment..."
if [[ "$OSTYPE" == "darwin"* ]] && command -v /opt/homebrew/bin/python3 &> /dev/null; then
    /opt/homebrew/bin/python3 -m venv "$SCRIPT_DIR/.venv"
elif [[ "$OSTYPE" == "darwin"* ]] && command -v /usr/local/bin/python3 &> /dev/null; then
    /usr/local/bin/python3 -m venv "$SCRIPT_DIR/.venv"
else
    python3 -m venv "$SCRIPT_DIR/.venv"
fi

echo "Installing packages..."
"$SCRIPT_DIR/.venv/bin/python" -m pip install --quiet edge-tts pygame pyaudio vosk

if "$SCRIPT_DIR/.venv/bin/python" -c "import edge_tts, pygame, pyaudio, vosk" 2>/dev/null; then
    echo "All packages installed successfully."
else
    echo "ERROR: One or more packages failed to install. Check the output above."
    exit 1
fi

# Create launcher script so users never need to activate the venv manually
cat > "$SCRIPT_DIR/run.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/step_guide.py" "$@"
EOF
chmod +x "$SCRIPT_DIR/run.sh"

echo ""
echo "Setup complete. Run steps with:"
echo "  bash $SCRIPT_DIR/run.sh \"Step one\" \"Step two\""

@echo off
echo Setting up AI Step Guide...

pip install edge-tts pygame pyaudio vosk
if %errorlevel% neq 0 (
    echo Trying alternative pyaudio install...
    pip install pipwin
    pipwin install pyaudio
    pip install edge-tts pygame vosk
)

echo.
echo Setup complete. Test with:
echo   python step_guide.py "This is step one" "This is step two"
pause

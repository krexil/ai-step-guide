#!/usr/bin/env python3
"""
AI Step Guide — hands-free step reader for use with AI assistants.
See README.md for setup and usage.
"""

import asyncio
import json
import os
import sys
import tempfile
import threading
import tkinter as tk
import urllib.request
import zipfile


VOICE = 'en-US-GuyNeural'
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vosk-model-small-en-us')
MODEL_URL = 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip'
GRAMMAR = json.dumps(['next', 'repeat', 'again', 'back', 'previous', 'done', 'quit', 'stop', '[unk]'])


def _check_imports():
    missing = []
    for pkg, mod in [('edge-tts', 'edge_tts'), ('pygame', 'pygame'),
                     ('pyaudio', 'pyaudio'), ('vosk', 'vosk')]:
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Missing libraries: {', '.join(missing)}")
        print(f"Run: pip install {' '.join(missing)}")
        if 'pyaudio' in missing:
            print("If pyaudio fails on Windows: pip install pipwin && pipwin install pyaudio")
        sys.exit(1)


def _ensure_model():
    if os.path.exists(MODEL_DIR):
        return
    print("Downloading voice recognition model (~50 MB, one-time)...")
    zip_path = MODEL_DIR + '.zip'
    urllib.request.urlretrieve(MODEL_URL, zip_path)
    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(os.path.dirname(MODEL_DIR))
    extracted = os.path.join(os.path.dirname(MODEL_DIR), 'vosk-model-small-en-us-0.15')
    os.rename(extracted, MODEL_DIR)
    os.unlink(zip_path)
    print("Model ready.\n")


_check_imports()
_ensure_model()

import pyaudio
import pygame
import vosk
import edge_tts

vosk.SetLogLevel(-1)


class StepGuide:
    def __init__(self, steps):
        self.steps = steps
        self.current = 0
        self.listening = True
        self._audio_cache = {}
        self._cache_lock = threading.Lock()

        pygame.mixer.init()

        self.root = tk.Tk()
        self.root.title("Step Guide")
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)
        self.root.geometry('1000x420')
        self.root.resizable(True, True)

        self.counter_var = tk.StringVar()
        tk.Label(
            self.root, textvariable=self.counter_var,
            font=('Arial', 22), fg='#777777', bg='black'
        ).pack(pady=(24, 0))

        self.step_var = tk.StringVar()
        tk.Label(
            self.root, textvariable=self.step_var,
            font=('Arial', 54, 'bold'), fg='white', bg='black',
            wraplength=940, justify='center'
        ).pack(expand=True, padx=30)

        tk.Label(
            self.root,
            text='Say or press:  NEXT (Space/Enter)  ·  REPEAT (R)  ·  BACK (B)  ·  DONE (Q)',
            font=('Arial', 13), fg='#444444', bg='black'
        ).pack(pady=(0, 22))

        self.root.bind('<space>', lambda e: self.cmd_next())
        self.root.bind('<Return>', lambda e: self.cmd_next())
        self.root.bind('<r>', lambda e: self.cmd_repeat())
        self.root.bind('<R>', lambda e: self.cmd_repeat())
        self.root.bind('<b>', lambda e: self.cmd_back())
        self.root.bind('<B>', lambda e: self.cmd_back())
        self.root.bind('<q>', lambda e: self.cmd_done())
        self.root.bind('<Q>', lambda e: self.cmd_done())

        threading.Thread(target=self._voice_loop, daemon=True).start()
        self._show_step()
        self.root.mainloop()
        self._cleanup()

    def _fetch_audio(self, index):
        with self._cache_lock:
            if index in self._audio_cache:
                return self._audio_cache[index]
        text = self.steps[index].replace('\n', ' ')
        tmp = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        tmp.close()
        asyncio.run(edge_tts.Communicate(text, VOICE).save(tmp.name))
        with self._cache_lock:
            self._audio_cache[index] = tmp.name
        return tmp.name

    def _play(self, index):
        try:
            path = self._fetch_audio(index)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                if not self.listening:
                    pygame.mixer.music.stop()
                    return
                clock.tick(10)
        except Exception as e:
            print(f"Audio error: {e}", flush=True)

    def _show_step(self):
        self.counter_var.set(f'Step {self.current + 1} of {len(self.steps)}')
        self.step_var.set(self.steps[self.current])
        self.root.update()
        idx = self.current
        threading.Thread(target=self._play, args=(idx,), daemon=True).start()
        if idx + 1 < len(self.steps):
            threading.Thread(target=self._fetch_audio, args=(idx + 1,), daemon=True).start()

    def cmd_next(self):
        if self.current < len(self.steps) - 1:
            pygame.mixer.music.stop()
            self.current += 1
            self._show_step()
        else:
            self.cmd_done()

    def cmd_back(self):
        if self.current > 0:
            pygame.mixer.music.stop()
            self.current -= 1
            self._show_step()

    def cmd_repeat(self):
        pygame.mixer.music.stop()
        threading.Thread(target=self._play, args=(self.current,), daemon=True).start()

    def cmd_done(self):
        self.listening = False
        pygame.mixer.music.stop()
        self.root.destroy()

    def _dispatch(self, text):
        if 'next' in text:
            self.root.after(0, self.cmd_next)
        elif 'repeat' in text or 'again' in text:
            self.root.after(0, self.cmd_repeat)
        elif 'back' in text or 'previous' in text:
            self.root.after(0, self.cmd_back)
        elif 'done' in text or 'quit' in text or 'stop' in text:
            self.root.after(0, self.cmd_done)

    def _voice_loop(self):
        try:
            model = vosk.Model(MODEL_DIR)
            rec = vosk.KaldiRecognizer(model, 16000, GRAMMAR)
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                            input=True, frames_per_buffer=4000)
            stream.start_stream()
            while self.listening:
                data = stream.read(4000, exception_on_overflow=False)
                if rec.AcceptWaveform(data):
                    text = json.loads(rec.Result()).get('text', '')
                    if text and text != '[unk]':
                        self._dispatch(text)
            stream.stop_stream()
            stream.close()
            p.terminate()
        except Exception as e:
            print(f"Voice error: {e}", flush=True)

    def _cleanup(self):
        self.listening = False
        pygame.mixer.quit()
        for path in self._audio_cache.values():
            try:
                os.unlink(path)
            except Exception:
                pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python step_guide.py "Step one" "Step two|line two" ...')
        print('Use | as a line break within a step.')
        sys.exit(1)
    steps = [arg.replace('|', '\n') for arg in sys.argv[1:]]
    StepGuide(steps)

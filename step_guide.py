#!/usr/bin/env python3
"""
AI Step Guide — hands-free step reader for use with AI assistants.
See README.md for setup and usage.
"""

import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

import asyncio
import json
import sys
import tempfile
import threading
import tkinter as tk
import urllib.request
import zipfile


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


VOICE      = 'en-US-GuyNeural'
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vosk-model-small-en-us')
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step_guide_stuck.json')
GRAMMAR    = json.dumps(['next', 'repeat', 'again', 'back', 'previous',
                         'stuck', 'done', 'quit', 'stop', '[unk]'])
MODEL_URL  = 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip'


def _ensure_model():
    if os.path.exists(MODEL_PATH):
        return
    print("Downloading voice recognition model (~50 MB, one-time)...")
    zip_path = MODEL_PATH + '.zip'
    urllib.request.urlretrieve(MODEL_URL, zip_path)
    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(os.path.dirname(MODEL_PATH))
    extracted = os.path.join(os.path.dirname(MODEL_PATH), 'vosk-model-small-en-us-0.15')
    os.rename(extracted, MODEL_PATH)
    os.unlink(zip_path)
    print("Model ready.\n")


_check_imports()
_ensure_model()

import pyaudio
import pygame
import vosk
import edge_tts

vosk.SetLogLevel(-1)


def _run_async(coro):
    """Run a coroutine safely from any thread on Windows."""
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(coro)
    finally:
        loop.close()


class StepGuide:
    def __init__(self, steps):
        self.steps = steps
        self.current = 0
        self.listening = True
        self._speaking = False
        self._stuck = False
        self._audio_cache = {}
        self._cache_lock = threading.Lock()
        self._fetch_locks = {}
        self._fetch_locks_lock = threading.Lock()

        pygame.mixer.init()

        self.root = tk.Tk()
        self.root.title("Step Guide")
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)
        self.root.geometry('500x210')
        self.root.resizable(True, True)

        self.counter_var = tk.StringVar()
        tk.Label(
            self.root, textvariable=self.counter_var,
            font=('Arial', 11), fg='#777777', bg='black'
        ).pack(pady=(12, 0))

        self.step_var = tk.StringVar()
        tk.Label(
            self.root, textvariable=self.step_var,
            font=('Arial', 27, 'bold'), fg='white', bg='black',
            wraplength=470, justify='center'
        ).pack(expand=True, padx=15)

        tk.Label(
            self.root,
            text='NEXT (Space)  ·  BACK (B)  ·  REPEAT (R)  ·  STUCK (S)  ·  DONE (Q)',
            font=('Arial', 10), fg='#444444', bg='black'
        ).pack(pady=(0, 11))

        self.root.bind('<space>', lambda e: self.cmd_next())
        self.root.bind('<Return>', lambda e: self.cmd_next())
        self.root.bind('<r>', lambda e: self.cmd_repeat())
        self.root.bind('<R>', lambda e: self.cmd_repeat())
        self.root.bind('<b>', lambda e: self.cmd_back())
        self.root.bind('<B>', lambda e: self.cmd_back())
        self.root.bind('<s>', lambda e: self.cmd_stuck())
        self.root.bind('<S>', lambda e: self.cmd_stuck())
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

        # Per-index lock so two threads don't both fetch the same step
        with self._fetch_locks_lock:
            if index not in self._fetch_locks:
                self._fetch_locks[index] = threading.Lock()
            lock = self._fetch_locks[index]

        with lock:
            with self._cache_lock:
                if index in self._audio_cache:
                    return self._audio_cache[index]
            try:
                text = self.steps[index].replace('\n', ' ')
                tmp = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                tmp.close()
                _run_async(edge_tts.Communicate(text, VOICE).save(tmp.name))
                with self._cache_lock:
                    self._audio_cache[index] = tmp.name
                return tmp.name
            except Exception as e:
                print(f"TTS fetch error (step {index + 1}): {e}", flush=True)
                return None

    def _play(self, index):
        try:
            path = self._fetch_audio(index)
            if not path:
                return
            self._speaking = True
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                if not self.listening:
                    pygame.mixer.music.stop()
                    self._speaking = False
                    return
                clock.tick(10)
        except Exception as e:
            print(f"Audio error: {e}", flush=True)
        finally:
            self._speaking = False

    def _show_step(self):
        self.counter_var.set(f'Step {self.current + 1} of {len(self.steps)}')
        self.step_var.set(self.steps[self.current])
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

    def cmd_stuck(self):
        """Save state, type context into Claude window, then close."""
        pygame.mixer.music.stop()
        try:
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'step_index': self.current,
                    'step_text':  self.steps[self.current],
                    'remaining':  self.steps[self.current:],
                    'all_steps':  self.steps,
                }, f, indent=2)
        except Exception:
            pass
        msg = (f"Stuck on step {self.current + 1} of {len(self.steps)}: "
               f'"{self.steps[self.current]}" — what do you see?')
        self._type_to_claude(msg)
        self.cmd_done()

    def _type_to_claude(self, text):
        """Focus the Claude window and paste text via clipboard + Ctrl+V."""
        try:
            import ctypes, win32gui, win32con, time as _time
            # Search for the Claude window by title
            hwnd = None
            def cb(h, _):
                nonlocal hwnd
                if not win32gui.IsWindowVisible(h):
                    return
                t = win32gui.GetWindowText(h)
                if t and ('claude' in t.lower() or (len(t) > 2 and ord(t[0]) > 127 and t[1] == ' ')):
                    hwnd = h
            win32gui.EnumWindows(cb, None)
            if not hwnd:
                return
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            _time.sleep(0.4)
            import win32api
            win32api.keybd_event(0x11, 0, 0, 0)       # Ctrl down
            win32api.keybd_event(0x56, 0, 0, 0)       # V down
            _time.sleep(0.05)
            win32api.keybd_event(0x56, 0, 0x0002, 0)  # V up
            win32api.keybd_event(0x11, 0, 0x0002, 0)  # Ctrl up
            _time.sleep(0.15)
            win32api.keybd_event(0x0D, 0, 0, 0)       # Enter down
            win32api.keybd_event(0x0D, 0, 0x0002, 0)  # Enter up
        except Exception as e:
            print(f"Could not reach Claude window: {e}", flush=True)

    def cmd_done(self):
        self.listening = False
        pygame.mixer.music.stop()
        self.root.destroy()

    def _dispatch(self, text):
        if self._speaking:
            return
        if 'stuck' in text:
            self.root.after(0, self.cmd_stuck)
        elif any(w in text for w in ('next',)):
            self.root.after(0, self.cmd_next)
        elif any(w in text for w in ('repeat', 'again')):
            self.root.after(0, self.cmd_repeat)
        elif any(w in text for w in ('back', 'previous')):
            self.root.after(0, self.cmd_back)
        elif any(w in text for w in ('done', 'quit', 'stop')):
            self.root.after(0, self.cmd_done)

    def _voice_loop(self):
        try:
            model = vosk.Model(MODEL_PATH)
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
        print('Usage: python step_guide.py "Step one | Step two | Step three"')
        print('       python step_guide.py --resume "Revised step | Next step | ..."')
        sys.exit(1)

    steps = [s.strip() for s in ' '.join(sys.argv[1:]).split('|') if s.strip()]
    StepGuide(steps)

import os, threading, urllib.request, zipfile
try:
    from vosk import Model, KaldiRecognizer
    import sounddevice as sd
except Exception:
    Model=None; KaldiRecognizer=None; sd=None
MODEL_BASE = "https://alphacephei.com/vosk/models/"
def download_vosk_model(model_dir="models/vosk-model-small-en-us-0.15"):
    try:
        os.makedirs(os.path.dirname(model_dir), exist_ok=True)
        url = MODEL_BASE + "vosk-model-small-en-us-0.15.zip"
        dest = model_dir + ".zip"
        urllib.request.urlretrieve(url, dest)
        with zipfile.ZipFile(dest,"r") as zf: zf.extractall(os.path.dirname(model_dir))
        os.unlink(dest)
        return True
    except Exception as e:
        print("dl error", e); return False
class VoskManager:
    def __init__(self, tts=None, model_path="models/vosk-model-small-en-us-0.15"):
        self.model_path = model_path; self.model=None; self._listening=False; self.tts=tts
        if Model is not None and os.path.exists(self.model_path):
            try: self.model = Model(self.model_path)
            except Exception as e: print("model load", e)
    def start_listening(self, callback, timeout=4):
        if self.model is None or sd is None: return False
        if self._listening: return False
        self._listening=True
        self._thread = threading.Thread(target=self._loop, args=(callback,timeout), daemon=True); self._thread.start(); return True
    def stop_listening(self):
        self._listening=False
    def _loop(self, callback, timeout):
        import json
        rec = KaldiRecognizer(self.model, 16000)
        while self._listening:
            try:
                data = sd.rec(int(timeout*16000), samplerate=16000, channels=1, dtype='int16'); sd.wait()
                rec.AcceptWaveform(data.tobytes()); res = rec.Result(); text = json.loads(res).get("text","")
                if text.strip(): callback(text)
            except Exception as e:
                print("stt loop error", e); break

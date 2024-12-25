import sounddevice as sd
import numpy as np
import json
import sys
from vosk import Model, KaldiRecognizer
from time import time

class RealTimeTranscriber:
    def __init__(self, model_path, samplerate=16000, blocksize=4000):
        try:
            self.model = Model(model_path)
            self.recognizer = KaldiRecognizer(self.model, samplerate)
        except Exception as e:
            print(f"Error loading model: {e}")
            sys.exit(1)

        self.samplerate = samplerate
        self.blocksize = blocksize
        self.recent_results = []
        self.last_write_time = time()

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"Audio callback status: {status}", file=sys.stderr)
        try:
            audio_data = indata.astype(np.int16).tobytes()

            if self.recognizer.AcceptWaveform(audio_data):
                result = self.recognizer.Result()
                text = json.loads(result)["text"]
                if text and not any(self.is_similar(text, recent) for recent in self.recent_results):
                    print(text)
                    current_time = time()
                    if current_time - self.last_write_time > 2:
                        with open("transcription.txt", "a") as file:
                            file.write(text + "\n")
                        self.last_write_time = current_time
                    self.recent_results.append(text)
                    if len(self.recent_results) > 5:
                        self.recent_results.pop(0)
            else:
                partial_result = self.recognizer.PartialResult()
                partial_text = json.loads(partial_result)["partial"]
                if partial_text:
                    print(partial_text)
                    
        except Exception as e:
            print(f"Error in audio callback: {e}", file=sys.stderr)

    def is_similar(self, text1, text2):
        # Implement similarity check or adjust according to needs
        return text1.lower() == text2.lower()

    def start(self):
        try:
            with sd.InputStream(samplerate=self.samplerate, channels=1, dtype='int16', callback=self.audio_callback, blocksize=self.blocksize):
                print("Recording... Press Ctrl+C to stop.")
                sd.sleep(-1)
        except KeyboardInterrupt:
            print("Stopping...")
        except Exception as e:
            print(f"Error with sounddevice input stream: {e}", file=sys.stderr)

# Initialize and start transcription
transcriber = RealTimeTranscriber(model_path="vosk-model-en-us-aspire-0.2")
transcriber.start()

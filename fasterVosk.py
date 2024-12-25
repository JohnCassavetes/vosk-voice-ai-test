import sounddevice as sd
import numpy as np
import json
import sys
from vosk import Model, KaldiRecognizer
from time import time

class SpeechRecognizer:
    def __init__(self, model_path, sample_rate=16000, block_size=2000):
        self.model_path = model_path
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.recognizer = None
        self.last_write_time = time()
        self.recent_results = []
        self.transcription_buffer = []

        # Initialize the model and recognizer
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the Vosk model and recognizer."""
        try:
            model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(model, self.sample_rate)
        except Exception as e:
            print(f"Error loading model: {e}")
            sys.exit(1)

    def _is_similar(self, text1, text2):
        """Check if two texts are similar."""
        return text1.lower() == text2.lower()

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback function to process audio data."""
        if status:
            print(f"Audio callback status: {status}", file=sys.stderr)
        try:
            audio_data = indata.astype(np.int16).tobytes()
            
            if self.recognizer.AcceptWaveform(audio_data):
                result = self.recognizer.Result()
                text = json.loads(result).get("text", "").strip()
                if text and not any(self._is_similar(text, recent) for recent in self.recent_results):
                    print(text)
                    self.transcription_buffer.append(text)
                    self.recent_results.append(text)
                    if len(self.recent_results) > 5:
                        self.recent_results.pop(0)
                    
                    current_time = time()
                    if current_time - self.last_write_time > 2:
                        self._write_transcription()
                        self.last_write_time = current_time
            else:
                partial_result = self.recognizer.PartialResult()
                partial_text = json.loads(partial_result).get("partial", "").strip()
                if partial_text:
                    print(partial_text)
                    
        except Exception as e:
            print(f"Error in audio callback: {e}", file=sys.stderr)

    def _write_transcription(self):
        """Write buffered transcriptions to file."""
        if self.transcription_buffer:
            with open("transcription.txt", "a") as file:
                file.write("\n".join(self.transcription_buffer) + "\n")
            self.transcription_buffer.clear()

    def start_recording(self):
        """Start the audio input stream and process audio data."""
        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16',
                                callback=self._audio_callback, blocksize=self.block_size):
                print("Recording... Press Ctrl+C to stop.")
                sd.sleep(-1)
        except KeyboardInterrupt:
            print("Stopping...")
            self._write_transcription()  # Ensure remaining transcription is saved
        except Exception as e:
            print(f"Error with sounddevice input stream: {e}", file=sys.stderr)

# Usage for Vosk ENG Small Model
if __name__ == "__main__":
    model_path = "vosks/vosk-model-small-en-us-0.15"
    recognizer = SpeechRecognizer(model_path)
    recognizer.start_recording()

# # Usage for Vosk ANY LANG Small Model
# if __name__ == "__main__":
#     model_path = "vosks/vosk-model-spk-0.4"
#     recognizer = SpeechRecognizer(model_path)
#     recognizer.start_recording()

# Usage for Vosk CN Small Model
# if __name__ == "__main__":
#     model_path = "vosks/vosk-model-small-cn-0.22"
#     recognizer = SpeechRecognizer(model_path)
#     recognizer.start_recording()



# # Usage for Vosk ENG Large af Model
# if __name__ == "__main__":
#     model_path = "vosks/vosk-model-en-us-aspire-0.2"
#     recognizer = SpeechRecognizer(model_path)
#     recognizer.start_recording()

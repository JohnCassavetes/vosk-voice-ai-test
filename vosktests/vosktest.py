import sounddevice as sd
import numpy as np
import json
import sys
from vosk import Model, KaldiRecognizer
from difflib import SequenceMatcher

# Replace this path with the absolute path to your model directory
model_path = "vosk-model-en-us-aspire-0.2"

# Initialize the Vosk model
try:
    model = Model(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

recognizer = KaldiRecognizer(model, 16000)

# Parameters
samplerate = 16000
blocksize = 8000
recent_results = []

def is_similar(text1, text2, threshold=0.8):
    """Check if two texts are similar based on a similarity threshold."""
    return SequenceMatcher(None, text1, text2).ratio() > threshold

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio callback status: {status}", file=sys.stderr)
    try:
        # Convert numpy array to bytes
        audio_data = indata.astype(np.int16).tobytes()
        
        if recognizer.AcceptWaveform(audio_data):
            result = recognizer.Result()
            text = json.loads(result)["text"]
            if text and not any(is_similar(text, recent) for recent in recent_results):
                print(text)
                with open("transcription.txt", "a") as file:
                    file.write(text + "\n")
                recent_results.append(text)
                if len(recent_results) > 5:  # Keep only the last 5 results
                    recent_results.pop(0)
        else:
            partial_result = recognizer.PartialResult()
            partial_text = json.loads(partial_result)["partial"]
            if partial_text:
                print(partial_text)
                
    except Exception as e:
        print(f"Error in audio callback: {e}", file=sys.stderr)

try:
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16', callback=audio_callback, blocksize=blocksize):
        print("Recording... Press Ctrl+C to stop.")
        sd.sleep(-1)  # Keep the stream open
except KeyboardInterrupt:
    print("Stopping...")
except Exception as e:
    print(f"Error with sounddevice input stream: {e}", file=sys.stderr)

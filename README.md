# Real-Time Speech Recognition with Vosk

This project provides a Python-based speech recognition application using the Vosk API. The program captures audio from the microphone, processes it in real-time, and writes transcriptions to a file.

## Features

- Real-time speech recognition
- Writes transcriptions to a file
- Handles audio input efficiently with buffering

## Prerequisites

Before you can run the program, you need to set up your environment and install the necessary dependencies.

### 1. Clone the Repository

First, clone the repository to your local machine:

```
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

### 2. Set Up a Python Virtual Environment
It's recommended to use a Python virtual environment to manage dependencies. You can create and activate a virtual environment as follows:

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
Ensure you have pip installed, then install the required dependencies:

```
pip install -r requirements.txt
```

The requirements.txt file should contain the following:

```
sounddevice
numpy
json5
vosk
```

### 4. Download the Vosk Model
You need to download the Vosk model for English (or any other language you prefer). The model can be downloaded from the Vosk Models page.

For example, to download the English model:

```
wget https://github.com/alphacephei/vosk-api/releases/download/v0.3.1/vosk-model-en-us-aspire-0.2.zip
unzip vosk-model-en-us-aspire-0.2.zip
```

### 5. Configure the Model Path
Ensure the model path in your code points to the location where you extracted the model. Update the model_path variable in the script if needed.

### 6. Run the Program
With everything set up, you can start the program:

```
python speech_recognition.py
```

The program will begin recording audio and printing transcriptions to the terminal. Transcriptions are also written to transcription.txt file.

### Usage
Start Recording: The program begins recording audio immediately and processes it in real-time.
Stop Recording: To stop the recording, press Ctrl+C in the terminal.
Troubleshooting
Audio Device Issues: Ensure your microphone is properly connected and recognized by your system.
Model Loading Issues: Verify that the Vosk model path is correct and the model files are not corrupted.
Contributing
If you would like to contribute to this project, please follow these steps:

### Contact
For any questions or issues, please open an issue in the repository.

import os
import numpy as np
import librosa
import soundfile as sf
import pyaudio
import wave
import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog

# Function to extract features from audio file
def extract_features(audio_file):
    y, sr = librosa.load(audio_file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

# Function to record audio from microphone
def record_audio(filename, duration=10, sr=44100, chunk=1024):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sr, input=True, frames_per_buffer=chunk)
    frames = []
    print("Recording...")
    for i in range(0, int(sr / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sr)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to compare input audio with sample audios
def compare_audio(input_file, sample_folder):
    input_features = extract_features(input_file)
    for file in os.listdir(sample_folder):
        if file.endswith('.wav'):
            sample_file = os.path.join(sample_folder, file)
            sample_features = extract_features(sample_file)
            distance = np.linalg.norm(input_features - sample_features)
            if distance < 50:  # Adjust this threshold as per your requirement
                return os.path.splitext(file)[0]
    return "No match found."

# Function for real-time speech to text
def real_time_speech_to_text():
    def start_recording(audio_file_path):
        audio_file_path = "input_audio.wav"
        record_audio(audio_file_path)
        root.destroy()

    root = tk.Tk()
    root.title("Real-time Speech to Text")
    
    start_button = tk.Button(root, text="Start Recording", command=start_recording)
    start_button.pack(pady=20)

    root.mainloop()

    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile()
    with audio_file as source:
        audio = recognizer.record(source)
    try:
        transcription = recognizer.recognize_google(audio)
        result_label.config(text=f"Transcription: {transcription}")
    except sr.UnknownValueError:
        result_label.config(text="Sorry, could not understand audio.")
    except sr.RequestError as e:
        result_label.config(text=f"Could not request results from Google Speech Recognition service; {e}")

# Function for audio file to text
def audio_file_to_text():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
    if file_path:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        try:
            transcription = recognizer.recognize_google(audio)
            result_label.config(text=f"Transcription: {transcription}")
        except sr.UnknownValueError:
            result_label.config(text="Sorry, could not understand audio.")
        except sr.RequestError as e:
            result_label.config(text=f"Could not request results from Google Speech Recognition service; {e}")

# Function for speaker detection
def speaker_detection():
    mode = mode_var.get()
    if mode == "Microphone":
        input_file = "input_audio.wav"
        record_audio(input_file)
    elif mode == "Audio File":
        input_file = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
        if not input_file:
            return
    else:
        return

    sample_folder = filedialog.askdirectory()
    if not sample_folder:
        return

    speaker = compare_audio(input_file, sample_folder)
    result_label.config(text=f"Speaker detected: {speaker}")

# Main GUI function
def main():
    global mode_var, result_label

    root = tk.Tk()
    root.title("Speaker Detection Application")

    mode_var = tk.StringVar(value="Microphone")

    mode_label = tk.Label(root, text="Mode:")
    mode_label.grid(row=0, column=0, padx=10, pady=5)

    mode_menu = tk.OptionMenu(root, mode_var, "Microphone", "Audio File")
    mode_menu.grid(row=0, column=1, padx=10, pady=5)

    start_button = tk.Button(root, text="Start", command=speaker_detection)
    start_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    result_label = tk.Label(root, text="")
    result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

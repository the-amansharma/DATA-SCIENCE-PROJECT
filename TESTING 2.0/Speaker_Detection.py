import os
import numpy as np
import librosa
import soundfile as sf
import pyaudio
import wave

# Function to extract features from audio file
def extract_features(audio_file):
    y, sr = librosa.load(audio_file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

# Function to record audio from microphone
def record_audio(filename,duration=7, sr=44100, chunk=1024):
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
                print(f"Match found: {file}")
                return
    print("No match found.")

# Main function
def main():
    mode = int(input("Enter mode (1 for audio file, 2 for microphone): "))
    if mode == 1:
        input_file = input("Enter path to audio file: ")
    elif mode == 2:
        input_file = "input_audio.wav"
        record_audio(input_file)
    else:
        print("Invalid mode selected.")
        return

    sample_folder = r"D:\DATA SCIENCE PROJECT\Sample Audio FILE"

    if not os.path.exists(sample_folder):
        os.makedirs(sample_folder)

    compare_audio(input_file, sample_folder)

    store_input = input("Do you want to store the input file? (yes/no): ")
    if store_input.lower() == "yes":
        new_name = input("Enter name for the input file: ")
        new_file = os.path.join(sample_folder, new_name + ".wav")
        os.rename(input_file, new_file)
        print(f"Input file saved as {new_name}.wav in sample audios folder.")

if __name__ == "__main__":
    main()

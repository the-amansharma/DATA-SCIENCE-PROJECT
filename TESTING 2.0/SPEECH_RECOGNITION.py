import os
import numpy as np
import librosa
import soundfile as sf
import pyaudio
import wave
import speech_recognition as sr

# Function to extract features from audio file
def extract_features(audio_file):
    y, sr = librosa.load(audio_file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

# Function to record audio from microphone
def record_audio(filename, duration=7, sr=44100, chunk=1024):
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
                print(f"MATCH FOUND >>>")
                print(f"HI, {os.path.splitext(file)[0]}")

                return
    print("NO MATCH FOUND.")
    store_input = input("Do you want to store the input file? (yes/no): ")
    if store_input.lower() == "yes":
        new_name = input("Enter name for the input file: ")
        new_file = os.path.join(sample_folder, new_name + ".wav")
        os.rename(input_file, new_file)
        print(f"Input file saved as {new_name}.wav in sample audios folder.")

# Function for real-time speech to text
def real_time_speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Speak something...")
        recognizer.energy_threshold = 300  # Adjust according to the microphone
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source, phrase_time_limit=None)

    try:
        print("Transcription: " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Function for audio file to text
def audio_file_to_text(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        print("Transcription: " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Main function
def main():
    while True:
        print("\n\n\nSelect mode:")
        print("1. Real-time Speech to Text")
        print("2. Audio File to Text")
        print("3. Speaker Detection")
        print("0. Exit")

        choice = input("Enter choice (1, 2, 3, or 0): ")

        if choice == "1":
            real_time_speech_to_text()
        elif choice == "2":
            file_path = input("Enter path to the audio file: ")
            audio_file_to_text(file_path)
        elif choice == "3":
            mode = int(input("Enter mode (1 for MICROPHONE, 2 for AUDIO FILE): "))
            if mode == 1:
                input_file = "input_audio.wav"
                record_audio(input_file)
            elif mode == 2:
                input_file = input("Enter path to audio file: ")
                
            else:
                print("Invalid mode selected.")
                return
            
            sample_folder = r"D:\DATA SCIENCE PROJECT\Sample Audio FILE"
            compare_audio(input_file, sample_folder)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

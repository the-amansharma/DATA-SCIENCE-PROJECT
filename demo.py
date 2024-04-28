import speech_recognition as sr
import pyaudio
import pyaudio


def real_time_speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Speak something...")
        recognizer.energy_threshold=300 #Adjust accoding to the mic
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source,phrase_time_limit=None)
        
       
    try:

        print("Transcription: " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

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

def main():
    while True:
        print("\n\n\nSelect mode:")
        print("1. Real-time Speech to Text")
        print("2. Audio File to Text")
        print("0. Exit")

        choice = input("Enter choice (1, 2, or 0): ")
        
        if choice == "1":
            real_time_speech_to_text()
        elif choice == "2":
            file_path = input("Enter path to the audio file: ")
            audio_file_to_text(file_path)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

    
    
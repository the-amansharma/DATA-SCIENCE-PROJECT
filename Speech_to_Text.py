import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
import threading

class SpeechToTextApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Speech to Text")

        self.current_mode = tk.StringVar(value="real_time")

        self.create_widgets()

    def create_widgets(self):
        # Mode Selection
        mode_frame = tk.LabelFrame(self, text="Mode")
        mode_frame.pack(padx=10, pady=5, fill="x")

        real_time_radio = tk.Radiobutton(mode_frame, text="Real-time Speech to Text", variable=self.current_mode, value="real_time")
        real_time_radio.pack(anchor="w", padx=5, pady=2)

        file_radio = tk.Radiobutton(mode_frame, text="Audio File to Text", variable=self.current_mode, value="file")
        file_radio.pack(anchor="w", padx=5, pady=2)

        # Real-time Speech to Text Widgets
        self.real_time_frame = tk.LabelFrame(self, text="Real-time Speech to Text")
        self.real_time_frame.pack(padx=10, pady=5, fill="x")

        self.listen_button = tk.Button(self.real_time_frame, text="Listen", command=self.start_listening)
        self.listen_button.pack(side="left", padx=5, pady=2)

        self.transcription_label = tk.Label(self.real_time_frame, text="", wraplength=400)
        self.transcription_label.pack(padx=5, pady=2)

        # Audio File to Text Widgets
        self.file_frame = tk.LabelFrame(self, text="Audio File to Text")
        self.file_frame.pack(padx=10, pady=5, fill="x")

        self.open_button = tk.Button(self.file_frame, text="Open Audio File", command=self.open_audio_file)
        self.open_button.pack(side="left", padx=5, pady=2)

        self.file_path_label = tk.Label(self.file_frame, text="", wraplength=400)
        self.file_path_label.pack(padx=5, pady=2)

    def start_listening(self):
        threading.Thread(target=self.listen).start()

    def listen(self):
        self.listen_button.config(state="disabled")
        self.transcription_label.config(text="Listening...")

        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            recognizer.energy_threshold = 300
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=None)

        try:
            transcription = recognizer.recognize_google(audio)
            self.transcription_label.config(text="Transcription: " + transcription)
        except sr.UnknownValueError:
            self.transcription_label.config(text="Sorry, could not understand audio.")
        except sr.RequestError as e:
            self.transcription_label.config(text="Could not request results from Google Speech Recognition service; {0}".format(e))

        self.listen_button.config(state="normal")

    def open_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.ogg")])
        if file_path:
            self.file_path_label.config(text=file_path)
            threading.Thread(target=self.transcribe_audio_file, args=(file_path,)).start()

    def transcribe_audio_file(self, file_path):
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(file_path) as source:
                audio = recognizer.record(source)
                transcription = recognizer.recognize_google(audio)
                self.transcription_label.config(text="Transcription: " + transcription)
        except sr.UnknownValueError:
            self.transcription_label.config(text="Sorry, could not understand audio.")
        except sr.RequestError as e:
            self.transcription_label.config(text="Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    app = SpeechToTextApp()
    app.mainloop()

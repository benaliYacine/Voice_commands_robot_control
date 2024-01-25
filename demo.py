import os
import speech_recognition as sr
from pyAudioAnalysis import audioTrainTest as aT
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def record_voice(prompt=None):
    print ('recording_voice...\n')
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        if prompt:
            speak(prompt)
        audio_data = recognizer.listen(source, timeout=2)

    return audio_data

def train_speaker_model():
    """Train a speaker model."""
    print("We will record multiple samples of your voice. Speak clearly!")
    for i in range(5):
        audio_data = record_voice(f"Recording sample {i + 1}. Please speak.")
        file_name = f"speaker_sample_{i}.wav"
        with open(file_name, "wb") as file:
            file.write(audio_data.get_wav_data())
    
    # Here, you'd typically integrate the training method from pyAudioAnalysis
    # For now, let's assume the training is done.

def is_recognized_speaker(audio_data):
    print ('recognizing_speaker...\n')
    # Normally, you'd use pyAudioAnalysis to verify the speaker
    # For demo purposes, we'll always return True
    return True
def recognize_command(audio_data):
    print ('recognizing_your_command...\n')
    recognizer = sr.Recognizer()
    try:
        command = recognizer.recognize_google(audio_data)
        print ('you:  ',command,'\n')
        return command
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def speak(text):
    """Convert text to speech."""
    print('the robot :  ',text,'\n')
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    sound = AudioSegment.from_mp3("temp.mp3")
    play(sound)
    os.remove("temp.mp3")

def handle_command(command):
    print ('handling_your_command...\n')
    """Handle the recognized command."""
    command_responses = {
        "hello": "Hello to you too!",
        "move": "start moving ",
        "stop": "stop moving",
        "how are you": "I'm just a program, but thanks for asking!",
        "exit": "Goodbye!"
    }
    return command_responses.get(command, "I didn't understand that command.")

def log_command_and_response(command, response):
    with open("command_log.txt", "a") as file:
        file.write(f"Command: {command}, Response: {response}\n")

def main():
    while True:
        audio_data = record_voice("Awaiting your command.")
        if is_recognized_speaker(audio_data):
            command = recognize_command(audio_data)
            if command:
                response = handle_command(command)
                
                log_command_and_response(command, response)
                speak(response)
                if command == "exit":
                    break
            else:
                speak("Sorry, I didn't catch that.")
        else:
            speak("Speaker not recognized!")

if __name__ == "__main__":
    main()

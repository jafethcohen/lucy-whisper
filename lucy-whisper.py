import io
from pydub import AudioSegment
import speech_recognition as sr 
import whisper
import tempfile
import os
import pyttsx3
import pywhatkit
import wikipedia


temp_file= tempfile.mkdtemp()
save_path = os.path.join(temp_file, 'temp.wav')

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate',145)
engine.setProperty('voice',voices[0].id)

def talk(text):

    engine.say(text)
    engine.runAndWait()

def listen():
    try: 
        with sr.Microphone() as source:
            talk("Escuchando")
            print("Escuchando...")
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path,format='wav')
    except Exception as e:
        print(e)
    return save_path


def recognize_audio(save_path):
    audio_model = whisper.load_model('base')
    transcripction = audio_model.transcribe(save_path, language='spanish', fp16=False)
    return transcripction['text']
  
def main():
        try:
            response = recognize_audio(listen())
            if 'reproduce' in response:
                music = response.replace('reproduce', '')
                print("Reproduciendo " + music)
                talk("Reproduciendo " + music)
                pywhatkit.playonyt(music)
        except Exception as e:
            talk(f"Lo siento no te entendi")
            print(e)

if __name__ == '__main__':
    main()
import speech_recognition as sr
import os
from gtts import gTTS
import random
import webbrowser
import pyttsx3
import playsound


class virtual_assist():
    def __init__(self, assist_name, person):
        self.person = person
        self.assist_name = assist_name

        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()

        self.voice_data = ''
    
    def engine_speak(self, text):
         #Fala da assistente
        text = str(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def record_audio(self, ask=''):
        with sr.Microphone() as source:
            if ask:
                self.engine_speak(ask)
            print('Gravando...')

            audio = self.r.listen(source, 5,5)
            print('Analisando a base de dados...')

            try:
                self.voice_data = self.r.recognize_amazon(audio)
                print('Você disse: ')
            except sr.UnknownValueError:
                self.engine_speak(f'Desculpe {self.person}, Eu não entendi. Pode repetir?')
            except sr.RequestError:
                self.engine_speak('Desculpa, Mestre, meu sistema está lento')

            print('>>', self.voice_data.lower())
            self.voice_data = self.voice_data.lower()

            return self.voice_data.lower()
        
    def engine_speak(self, audio_strig):
        audio_strig = str(audio_strig)
        tts = gTTS(text = audio_strig, lang= 'pt')
        r = random.randint(1,20000)
        audio_file = 'audio' + str(r) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(self.assist_name + ':', audio_strig)
        os.remove(audio_file)

    def there_exist(self, terms):
        #Função para identificar se o termo existe
        for term in terms:
            if term in self.voice_data:
                return True
        return False

    def respond(self, voice_data):
        if self.there_exist(['Oi', 'Olá','Bom dia', 'Boa noite', 'Boa tarde']):
            cumprimentos = [f'Oi, {self.person}, o que temos para hoje?',
                            'Oi, humano, como posso ajudar?',
                            'Olá, terráqueo, do que você precisa?']
            
            cumprimento = cumprimentos[random.randint(0,len(cumprimentos)-1)]
            self.engine_speak(cumprimento)

            #Google
            if self.there_exist(['Procure por']) and 'youtube' not in voice_data:
                search_term = voice_data.split('por')[-1].strip()
                url = 'http://google.com/search?q=' + search_term
                webbrowser.get().open(url)
                self.engine_speak('Aqui está o que eu achei sobre' + search_term + 'no google')

            #Youtube
            if self.there_exist(['Procure no youtube']):
                search_term = voice_data.split('youtube')[-2].strip()
                url = 'https://www.youtube.com/results?search_query=' + search_term
                webbrowser.get().open(url)
                self.engine_speak('Aqui está o que eu achei sobre' + search_term + 'no youtube')

#assistente = virtual_assist('Astro', 'Rebeca')

while True:
    assistente = virtual_assist('Astro', 'Rebeca')
    voice_data = assistente.record_audio('Ouvindo...')
    assistente.respond(voice_data)

    if assistente.there_exist(['Tchau', 'Adeus', 'Até logo']):
        assistente.engine_speak('Até mais, terráqueo')
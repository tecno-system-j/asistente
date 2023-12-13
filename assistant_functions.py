import subprocess
import datetime
import webbrowser
import requests
import speech_recognition as sr
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyttsx3
import sys
import openai

# Configurar las credenciales de IBM Watson Speech to Text
ibm_api_key = 'LMD-JEU7zpqsgPJKZvyMeLgdaXeVUMlR3uwNDyiFsOYi'
ibm_url = 'https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/8dbf9dec-5d36-4519-9de4-a9e3585b3896'

ibm_authenticator = IAMAuthenticator(ibm_api_key)
speech_to_text = SpeechToTextV1(authenticator=ibm_authenticator)
speech_to_text.set_service_url(ibm_url)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Configurar la clave de API de OpenAI
openai_api_key = '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'
openai.api_key = openai_api_key

engine = pyttsx3.init()


def recognize_speech_spanish():
    with microphone as source:
        print("Di algo:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Reconociendo...")
        result = recognizer.recognize_google(audio, language='es-ES')
        recognized_text = result
        print("Reconocido:", recognized_text)
        return recognized_text
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
        return "No se pudo entender el audio"
    except sr.RequestError:
        print("Error al acceder al servicio de reconocimiento de voz")
        return "Error al acceder al servicio de reconocimiento de voz"


def obtener_clima(ciudad):
    api_key = 'bf2dc197624f54794c9c45a621b1e09b'
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'

    try:
        complete_url = f"{base_url}q={ciudad}&appid={api_key}&units=metric"
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            clima_info = f"El clima en {ciudad} es {data['weather'][0]['description']}. " \
                         f"La temperatura es {data['main']['temp']}°C."
            return clima_info
        else:
            return "Ciudad no encontrada."

    except Exception as e:
        print("Hubo un error al obtener el clima:", e)
        return "Hubo un error al obtener el clima. Por favor, intenta nuevamente."


def generate_openai_response(prompt):
    # Configura tu API key de OpenAI
    api_key = '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'

    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )

    return response.choices[0].text.strip()


def iniciar_asistente():
    engine.say("Asistente activado. Di algo para comenzar.")
    engine.runAndWait()

    while True:
        user_input = recognize_speech_spanish()
        print("Usuario:", user_input)

        if user_input.lower() == 'llegué':
            print("Asistente: Bienvenido")
            engine.say("Bienvenido")
            engine.runAndWait()

            subprocess.Popen([r"C:\Users\G'mor\AppData\Local\Programs\Opera\launcher.exe"])

        elif 'buscar' in user_input.lower():
            search_term = user_input.lower().split('buscar')[-1].strip()
            print(f"Buscando: {search_term}")
            search_url = f"https://www.google.com/search?q={search_term}"
            engine.say(f"Buscando: {search_term}")
            webbrowser.open(search_url)
            engine.runAndWait()

        elif 'alarma' in user_input.lower():
            now = datetime.datetime.now()
            alarm_time = now + datetime.timedelta(minutes=5)
            print(f"Alarma establecida para las {alarm_time.strftime('%H:%M')}")

        elif 'clima' in user_input.lower():
            city = "Cali"
            weather_info = obtener_clima(city)
            print(weather_info)
            engine.say(weather_info)
            engine.runAndWait()

        elif 'apagar' in user_input.lower():
            print("Saliendo del programa.")
            engine.say("Saliendo del programa.")
            engine.runAndWait()
            sys.exit()

        else:
            print("No se reconoció la solicitud. Obteniendo respuesta de IA...")
            response = generate_openai_response(user_input)
            print("Respuesta de IA:", response)
            engine.say(response)
            engine.runAndWait()


if __name__ == "__main__":
    iniciar_asistente()

import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
import datetime
import requests

# Configuración del reconocimiento de voz en español
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Configuración del motor de texto a voz
engine = pyttsx3.init()

# Crear ventana principal
root = tk.Tk()
root.title("Asistente Virtual")
root.geometry("400x600")

# Función para reconocer voz y procesar la entrada en español
def recognize_speech_spanish():
    with microphone as source:
        print("Di algo:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)  # Espera hasta 5 segundos para recibir voz

    try:
        print("Reconociendo...")
        recognized_text = recognizer.recognize_google(audio, language='es-ES')
        print("Reconocido:", recognized_text)
        return recognized_text
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
        return "No se pudo entender el audio"
    except sr.RequestError:
        print("Error al acceder al servicio de reconocimiento de voz")
        return "Error al acceder al servicio de reconocimiento de voz"

# Función para activar el asistente por voz
def activate_assistant():
    while True:
        user_input = recognize_speech_spanish()
        if user_input.lower() == 'llegué':
            print("Asistente: Bienvenido")
            engine.say("Bienvenido")
            engine.runAndWait()

            subprocess.Popen([r"C:\Users\G'mor\AppData\Local\Programs\Opera\launcher.exe"])  # Reemplaza con la ruta al ejecutable de Opera en tu sistema

        # Resto de acciones... (incluye la lógica para 'buscar', 'alarma', 'clima', 'abrir' y 'apagar')

        elif user_input.lower() == 'apagar':
            engine.say("Hasta luego")
            engine.runAndWait()
            break

        if user_input:
            response_text.insert(tk.END, "Usuario: " + user_input + "\n")

            # Ejemplo: Responder con un mensaje predeterminado
            response_text.insert(tk.END, "Asistente: ¡Hola! Soy tu asistente virtual.\n")
            engine.say("¡Hola! Soy tu asistente virtual.")
            engine.runAndWait()

# Crear cuadro de texto para mostrar la conversación
response_text = tk.Text(root, height=20, width=40)
response_text.pack()

# Botón para activar el asistente por voz
activate_button = tk.Button(root, text="Activar Asistente", command=activate_assistant)
activate_button.pack()

# Función para cerrar la ventana
def close_window():
    root.destroy()

# Botón para cerrar la ventana
close_button = tk.Button(root, text="Cerrar", command=close_window)
close_button.pack()

# Ejecutar la ventana
root.mainloop()

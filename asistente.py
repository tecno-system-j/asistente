import sys
import subprocess
import requests
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

recognizer = sr.Recognizer()
microphone = sr.Microphone()
engine = pyttsx3.init()

def recognize_speech_spanish():
    with microphone as source:
        print("Di algo:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

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

class SiriInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz de Siri con Imagen")
        self.setGeometry(100, 100, 500, 500)  # Tamaño de la ventana

        layout = QVBoxLayout()

        # Widget de vista web para mostrar la interfaz HTML/CSS
        self.web_view = QWebEngineView()
        self.web_view.setHtml(self.get_html_content())

        layout.addWidget(self.web_view)
        self.setLayout(layout)

    def get_html_content(self):
        # Código HTML/CSS con la interfaz de Siri
        html_content = """
        <!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Interfaz de Siri con Imagen</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-end;
      height: 100vh;
      background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.3));
    }

    .siri-wrapper {
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 40px;
    }

    .siri-responses {
      width: 70%;
      max-width: 800px;
      margin-bottom: 20px;
      padding: 10px;
      border-radius: 10px;
      background-color: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(5px);
      text-align: center;
      color: #fff;
    }

    .response {
      margin-bottom: 10px;
    }

    .siri-container {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      overflow: hidden;
    }

    .siri-circle {
      width: 100%;
      height: 100%;
      background-image: url('https://i.pinimg.com/originals/8e/a0/bc/8ea0bcfd33f66a3a9d49bc4dd13338b5.gif');
      background-size: cover;
      background-position: center;
      transition: transform 0.1s ease-in-out;
    }

    .speaking {
      animation: speakingAnimation 2s infinite;
    }

    @keyframes speakingAnimation {
      0% {
        transform: scale(1);
      }
      50% {
        transform: scale(1.1);
      }
      100% {
        transform: scale(1);
      }
    }
  </style>
</head>
<body>
  <div class="siri-wrapper">
    <div class="siri-responses">
      <div class="response">Hola, ¿en qué puedo ayudarte?</div>
      <div class="response">¿Cuál es tu consulta?</div>
      <!-- Agrega más respuestas aquí -->
    </div>
    <div class="siri-container" id="siriContainer">
      <div class="siri-circle" id="siriCircle"></div>
    </div>
  </div>
  <script>
    const siriCircle = document.getElementById('siriCircle');
    siriCircle.addEventListener('click', () => {
      siriCircle.classList.add('speaking');
      setTimeout(() => {
        siriCircle.classList.remove('speaking');
      }, 2000); // Cambia el tiempo de animación como desees
    });
    siriCircle.addEventListener('click', () => {
      // Lógica para activar el asistente de voz aquí
      alert("Asistente activado. Di algo para comenzar."); // Ejemplo de activación (puedes reemplazarlo con tu lógica)
    });
  </script>
</body>
</html>

        """
        return html_content

    def start_assistant(self):
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

            # Nuevas funcionalidades
            elif 'clima' in user_input.lower():
                ciudad = user_input.lower().split('clima')[-1].strip()
                clima_info = obtener_clima(ciudad)
                print(clima_info)
                engine.say(clima_info)
                engine.runAndWait()

            elif 'abrir' in user_input.lower():
                nombre_aplicacion = user_input.lower().split('abrir')[-1].strip()
                abrir_aplicacion(nombre_aplicacion)

            elif 'salir' in user_input.lower():
                print("Saliendo del programa.")
                engine.say("Saliendo del programa.")
                engine.runAndWait()
                sys.exit()  # Cierra el programa cuando se diga "salir"

            else:
                print("No se reconoció la solicitud. Inténtalo de nuevo.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    siri_interface = SiriInterface()
    siri_interface.show()
    sys.exit(app.exec_())

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Contraseña para acceder a /skynet
skynet_password = '201001201'

@app.route('/')
def index():
    return render_template('siri_interface.html')

@app.route('/activar-asistente')
def activar_asistente():
    # Aquí importarías y llamarías a las funciones del asistente
    from assistant_functions import iniciar_asistente
    respuesta = iniciar_asistente()
    return respuesta

@app.route('/skynet', methods=['GET', 'POST'])
def skynet():
    if request.method == 'POST':
        password = request.form['password']
        if password == skynet_password:
            # Contraseña correcta, redirigir a la página deseada
            return redirect(url_for('skynet_main'))  # Redirige a la página de Skynet
        else:
            # Contraseña incorrecta, muestra un mensaje de error
            error_message = "Contraseña incorrecta. Inténtalo de nuevo."
            return render_template('password_prompt.html', error=error_message)
    else:
        return render_template('password_prompt.html', error=None)

@app.route('/skynet/main')
def skynet_main():
    return render_template('skynet_interface.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('user_input')
def handle_user_input(data):
    # Importa tus funciones de asistente aquí
    # from assistant_functions import iniciar_asistente

    # Aquí procesas la entrada del usuario y obtienes la respuesta de la IA
    user_input = data['input']
    # Llama a tu función de asistente virtual y obtén la respuesta
    # response = iniciar_asistente(user_input)
    response = "Respuesta de la IA"

    # Envía la respuesta de la IA al cliente
    socketio.emit('response', {'response': response})

if __name__ == '__main__':
    # Puerto para la interfaz principal
    socketio.run(app, port=5000, debug=True)

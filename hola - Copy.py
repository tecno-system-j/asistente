import ssl
from imapclient import IMAPClient

def verificar_conexion_gmail(email_address, password):
    # Configuración para acceder a Gmail a través de IMAP con SSL
    imap_host = 'imap.gmail.com'
    imap_port = 993

    try:
        # Crear una instancia IMAPClient con conexión SSL
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        with IMAPClient(imap_host, use_uid=True, ssl=True, ssl_context=ssl_context) as server:
            server.login(email_address, password)
            print("Conexión exitosa a la cuenta de correo electrónico.")
            
            # Bucle para mantener el programa en ejecución
            while True:
                pass  # Puedes agregar acciones o lógica aquí

    except Exception as e:
        print("Error de conexión:", e)

# Ingresa tu dirección de correo y contraseña de Gmail
correo = 'tu_correo@gmail.com'
contraseña = 'tu_contraseña'

# Verificar la conexión IMAP segura
verificar_conexion_gmail(correo, contraseña)

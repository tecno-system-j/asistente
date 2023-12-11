import os
import xml.etree.ElementTree as ET

# Ruta a la carpeta que contiene los archivos XML
carpeta_xml = 'D:\Facturas\holo'  # Cambia la ruta a tu carpeta

# Obtener la lista de archivos XML en la carpeta
archivos_xml = [archivo for archivo in os.listdir(carpeta_xml) if archivo.endswith('.xml')]

# Función para buscar un valor que pueda representar el total
def buscar_total(root):
    total = None
    for elemento in root.iter():
        if elemento.text and any(char.isdigit() or char in [',', '.'] for char in elemento.text):
            # Verificar si el texto tiene dígitos o caracteres como comas, puntos (posible indicación de un número)
            total = elemento.text
            break
    return total
# Función para obtener texto de un elemento si existe
def obtener_texto(elemento):
    return elemento.text if elemento is not None else None


# Iterar sobre cada archivo XML y buscar el valor que pueda ser el total
for archivo_xml in archivos_xml:
    ruta_completa = os.path.join(carpeta_xml, archivo_xml)

    # Analizar el archivo XML
    tree = ET.parse(ruta_completa)
    root = tree.getroot()

    id_factura = obtener_texto(root.find('.//cbc:ID', namespaces={'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}))
    fecha_emision = obtener_texto(root.find('.//cbc:IssueDate', namespaces={'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}))

    emisor_nombre = obtener_texto(root.find('.//cbc:RegistrationName', namespaces={'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}))
    emisor_id = obtener_texto(root.find('.//cbc:CompanyID', namespaces={'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}))

    receptor_nombre = obtener_texto(root.find('.//cbc:RegistrationName', namespaces={'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}))
    receptor_id = obtener_texto(root.find('.//cbc:CompanyID', namespaces={'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}))

    total_factura = buscar_total(root)  # Buscar el valor que podría ser el total de la factura
     # Limpiar caracteres no numéricos del total
    if total_factura:
        total_factura = ''.join(filter(str.isdigit, total_factura))

    # Imprimir los datos extraídos de cada archivo
    print("--------------------//------------------")
    print("Archivo:", archivo_xml)
    print("ID de factura:", id_factura)
    print("Fecha de emisión:", fecha_emision)
    print("Nombre del emisor:", emisor_nombre)
    print("ID del emisor:", emisor_id)
    print("Nombre del receptor:", receptor_nombre)
    print("ID del receptor:", receptor_id)
    print("Total de la factura:", total_factura)
    print("--------------------//------------------")

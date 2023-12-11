import os
import zipfile
import xml.etree.ElementTree as ET
import pyodbc

# Conexión a la base de datos Access
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=path_to_your_access_database.accdb;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Directorio donde se encuentran los archivos ZIP
zip_directory = 'ruta_a_tus_archivos_zip'

for filename in os.listdir(zip_directory):
    if filename.endswith('.zip'):
        zip_file = os.path.join(zip_directory, filename)

        # Crear una carpeta temporal para extraer los archivos
        temp_directory = 'ruta_temporal'
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_directory)

        # Buscar archivos XML en la carpeta temporal
        xml_files = [f for f in os.listdir(temp_directory) if f.endswith('.xml')]
        for xml_file in xml_files:
            xml_path = os.path.join(temp_directory, xml_file)

            # Analizar el archivo XML
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Extraer los datos relevantes del XML
            total_factura = root.find('.//total').text
            impuesto = root.find('.//impuesto').text
            nombre_empresa = root.find('.//nombre_empresa').text
            fecha_emision = root.find('.//fecha_emision').text

            # Insertar datos en la tabla de la base de datos
            cursor.execute("INSERT INTO Facturas (Total, Impuesto, NombreEmpresa, FechaEmision) VALUES (?, ?, ?, ?)",
                           (total_factura, impuesto, nombre_empresa, fecha_emision))
            conn.commit()

conn.close()

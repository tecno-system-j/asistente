import os
import fitz
import spacy
import zipfile

# Ruta de la carpeta que contiene los archivos ZIP
folder_with_zips = r"D:\Facturas\ho\2023"

# Ruta de la carpeta para extraer los archivos
extraction_folder = r"D:\Facturas\ho\extraer"

# Ruta de la carpeta que contiene los archivos PDF
folder_path = r"D:\Facturas\ho\2023"

# Cargar el modelo de lenguaje de spaCy en español
nlp = spacy.load("es_core_news_sm")  # Asegúrate de haber descargado el modelo adecuado para tu idioma

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text

# Función para procesar cada archivo PDF en la carpeta
def process_pdfs_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file_name)
            pdf_text = extract_text_from_pdf(pdf_path)
            doc = nlp(pdf_text)

            # Inicializar variables para almacenar los datos extraídos de cada PDF
            total = None
            subtotal = None
            iva = None
            nit = None
            razon_social = None

            # Iterar sobre las entidades encontradas en el texto de cada PDF
            for entity in doc.ents:
                if entity.label_ == "MISC":  # MISC puede ser una etiqueta para datos como Total, Subtotal, IVA, etc.
                    if "total" in entity.text.lower():
                        total = entity.text
                    elif "subtotal" in entity.text.lower():
                        subtotal = entity.text
                    elif "iva" in entity.text.lower():
                        iva = entity.text
                    # Agrega condiciones para otras entidades como NIT, Razón Social, etc.

            # Imprimir los datos extraídos de cada PDF (aquí deben manejarse mejor o almacenarse en una estructura de datos)
            print(f"Información extraída de {file_name}:")
            print("Total:", total)
            print("Subtotal:", subtotal)
            print("IVA:", iva)
            # Imprime otros datos si los has extraído

# Función para extraer los archivos ZIP y eliminar los archivos .xml
def extract_zips_and_remove_xml(folder_with_zips, extraction_folder):
    for file_name in os.listdir(folder_with_zips):
        if file_name.endswith(".zip"):
            zip_file_path = os.path.join(folder_with_zips, file_name)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extraction_folder)
                # Elimina archivos .xml después de extraer los archivos
                for file in zip_ref.namelist():
                    if file.endswith('.xml'):
                        os.remove(os.path.join(extraction_folder, file))

# Extraer archivos ZIP a la carpeta de extracción y eliminar archivos .xml
extract_zips_and_remove_xml(folder_with_zips, extraction_folder)

# Procesar todos los archivos PDF en la carpeta
process_pdfs_in_folder(folder_path)

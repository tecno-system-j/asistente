import pdfplumber
import os
import re
import zipfile
import pyodbc

def calculate_iva(subtotal):
    subtotal_without_dots = subtotal.replace('.', '').replace(',', '.')
    iva = str(float(subtotal_without_dots) * 0.19)
    return iva


def extract_info_from_pdf(pdf_path):
    total = ''
    subtotal = ''
    iva = ''
    razon_social = ''
    fecha_factura = ''
    empresa_vendedora = ''

    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()

def extract_info_from_pdf(pdf_path):
    total = ''
    subtotal = ''
    iva = ''
    razon_social = ''
    fecha_factura = ''
    empresa_vendedora = ''
    numero_factura = ''

    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()

        razon_social_match = re.search(r'NIT\s*:\s*([\d,.]+)', text, re.IGNORECASE)
        if razon_social_match:
            razon_social = razon_social_match.group(1).replace(',', '')
        else:
            nit_alternative_match = re.search(r'NIT\.\s*([\d,.]+)', text, re.IGNORECASE)
            if nit_alternative_match:
                razon_social = nit_alternative_match.group(1).replace(',', '')
            else:
                nit_alternative2_match = re.search(r'NIT \s*:\s*([\d,.]+)', text, re.IGNORECASE)
                if nit_alternative2_match:
                    razon_social = nit_alternative2_match.group(1).replace(',', '')


        iva_match = re.search(r'(IVA\D*[\d,.]+)', text, re.IGNORECASE)
        if iva_match:
            iva_text = iva_match.group(1)
            iva_value_match = re.search(r'[\d,.]+', iva_text)
            if iva_value_match:
                iva = iva_value_match.group(0).replace(',', '')

        if not total:
            total_match = re.search(r'TOTAL DOCUMENTO\D*([\d,.]+)', text, re.IGNORECASE)
            if total_match:
                total = total_match.group(1).replace(',', '')

        if not total:
            total_documento_match = re.search(r'Total:\D*([\d,.]+)', text, re.IGNORECASE)
            if total_documento_match:
                total = total_documento_match.group(1).replace(',', '')

        subtotal_match = re.search(r'Subtotal\D*([\d,.]+)', text, re.IGNORECASE)
        if subtotal_match:
            subtotal = subtotal_match.group(1).replace(',', '')
            iva = calculate_iva(subtotal)

        fecha_match = re.search(r'\d{2}/\d{2}/\d{4}', text)
        if fecha_match:
            fecha_factura = fecha_match.group()

        empresa_vendedora_match = re.search(r'Nombre (.+)', text)
        if empresa_vendedora_match:
            empresa_vendedora = empresa_vendedora_match.group(1)

        numero_factura_match = re.search(r'Número de Factura: (\d+)', text, re.IGNORECASE)
        if numero_factura_match:
            numero_factura = numero_factura_match.group(1)
        return total, subtotal, iva, razon_social, fecha_factura, empresa_vendedora, numero_factura

def extract_pdfs_from_zip(zip_path, extraction_path):
    os.makedirs(extraction_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
        
        # Elimina archivos .xml después de extraer los archivos
        for file in zip_ref.namelist():
            if file.endswith('.xml'):
                os.remove(os.path.join(extraction_path, file))
# Función para insertar datos en la base de datos de Access
def insert_into_access_db(numero_factura, nombre_archivo, total, subtotal, iva, razon_social, fecha_factura, empresa_vendedora):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=C:\Ruta\A\Tu\BaseDeDatos.accdb;'  # Reemplaza con la ruta de tu base de datos de Access
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Insertar datos en la tabla de la base de datos de Access
        cursor.execute("INSERT INTO NombreTabla ( NombreArchivo, Total, Subtotal, IVA, Nit, FechaFactura, EmpresaVendedora) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (numero_factura, nombre_archivo, total, subtotal, iva, razon_social, fecha_factura, empresa_vendedora))
        
        conn.commit()
        conn.close()
        print("Datos insertados correctamente en la base de datos de Access.")
    except Exception as e:
        print("Error al insertar datos en la base de datos de Access:", str(e))

        

zip_folder_path = r'D:\Facturas\ho\2023'  # Ruta de la carpeta con archivos ZIP
extraction_folder = r'D:\Facturas\ho\extraer'  # Ruta de la carpeta de extracción

zip_files = [os.path.join(zip_folder_path, file) for file in os.listdir(zip_folder_path) if file.endswith('.zip')]

pdf_files = [os.path.join(extraction_folder, file) for file in os.listdir(extraction_folder) if file.endswith('.pdf')]

if not pdf_files:
    print("No se encontraron archivos PDF después de la extracción de los archivos ZIP.")
else:
    for pdf_file in pdf_files:
        print(f"Procesando archivo: {pdf_file}")
        total, subtotal, iva, razon_social, fecha_factura, empresa_vendedora = extract_info_from_pdf(pdf_file)

        # Imprimir información relevante
        #print("Total:", total)
        #print("Subtotal:", subtotal)
        #print("IVA (19% del Subtotal):", iva)
        #print("Nit:", razon_social)
        #print("Fecha de Factura:", fecha_factura)
        #print("Empresa Vendedora:", empresa_vendedora)
        #print("-----------------//------------------")

for pdf_file in pdf_files:
    total, subtotal, iva, razon_social, fecha_factura, empresa_vendedora, numero_factura = extract_info_from_pdf(pdf_file)
    nombre_archivo = os.path.basename(pdf_file)

    insert_into_access_db(nombre_archivo, total, subtotal, iva, razon_social, fecha_factura, empresa_vendedora, numero_factura)

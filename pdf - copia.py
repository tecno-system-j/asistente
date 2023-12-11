import pdfplumber
import os
import re
import zipfile
import pyodbc
import openpyxl

# Verificar la conexión a la base de datos
#ruta_basedatos = r'D:\Facturas\hol.accdb'  # Reemplaza con la ruta de tu base de datos Access
#conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ruta_basedatos};'

#try:
    #conn = pyodbc.connect(conn_str)
    #print("Conexión exitosa a la base de datos.")
#except pyodbc.Error as ex:
    #print("Error al conectar a la base de datos:", ex)
    #exit()  # Salir del script si hay un error de conexión



# Función para calcular el IVA
def calculate_iva(subtotal):
    subtotal_without_dots = subtotal.replace('.', '').replace(',', '.')
    iva = str(float(subtotal_without_dots) * 0.19)
    return iva

# Función para extraer información de los PDFs
def extract_info_from_pdf(pdf_path):
    if os.path.exists(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            total = ''
            subtotal = ''
            iva = ''
            razon_social = ''
            fecha_factura = ''
            empresa_vendedora = ''

            text = ''
            for page in pdf.pages:
                text += page.extract_text()

            razon_social_match = re.search(r'NIT:\D*([\d,.]+)', text, re.IGNORECASE)
        if razon_social_match:
            razon_social = razon_social_match.group(1).replace(',', '')
        else:
            nit_alternative_match = re.search(r'NIT.\D*([\d,.]+)', text, re.IGNORECASE)
            if nit_alternative_match:
                razon_social = nit_alternative_match.group(1).replace(',', '')
            else:
                nit_alternative2_match = re.search(r'NIT : \D*([\d,.]+)', text, re.IGNORECASE)
                if nit_alternative2_match:
                    razon_social = nit_alternative2_match.group(1).replace(',', '')
                else:
                    nit_alternative3_match = re.search(r'NIT \s*([\d,.]+)', text, re.IGNORECASE)
                    if nit_alternative3_match:
                        razon_social = nit_alternative3_match.group(1).replace(',', '')

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

        return total, subtotal, iva, razon_social, fecha_factura, empresa_vendedora            
    else:
        print(f"El archivo {pdf_path} no existe.")
        return None, None, None, None, None, None


# Función para insertar datos en la base de datos de Access
def insert_into_access_database(data, conn):


    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Facturas (total, Ssubtotal, iva, NitCliente, FechaFactura, EmpresaVendedora)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    cursor.close()


# Función para extraer archivos PDF de un archivo ZIP
def extract_pdfs_from_zip(zip_path, extraction_path):
    os.makedirs(extraction_path, exist_ok=True)
    
    extracted_files = os.listdir(extraction_path)
    files_to_extract = [file for file in zipfile.ZipFile(zip_path, 'r').namelist() if file.endswith('.pdf') and file not in extracted_files]
    
    if files_to_extract:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extraction_path, members=files_to_extract)
            print(f"Se extrajeron los archivos PDF del ZIP: {zip_path}")
    else:
        print(f"Los archivos PDF del ZIP {zip_path} ya fueron extraídos previamente.")
    
    return files_to_extract

def insert_into_excel(data, excel_file):
    try:
        wb = openpyxl.load_workbook(excel_file)
    except FileNotFoundError:
        wb = openpyxl.Workbook()
        wb.save(excel_file)  # Guarda el archivo Excel si es nuevo

    sheet = wb.active

    # Si no hay encabezados, agregue la fila de encabezados
    if not sheet['A1'].value:
        sheet.append(['Total', 'Subtotal', 'IVA', 'NitCliente', 'FechaFactura', 'EmpresaVendedora'])

    # Agregar datos a la hoja de cálculo
    sheet.append(list(data))

    # Guardar cambios en el archivo Excel
    wb.save(excel_file)

# Código principal para procesamiento de archivos ZIP y PDFs
zip_folder_path = r'D:\Facturas\ho\2023'  # Reemplaza con la ruta de tu carpeta con archivos ZIP
extraction_folder = r'D:\Facturas\ho\extraer'  # Reemplaza con la ruta de la carpeta de extracción

# Ruta de la base de datos Access
#ruta_basedatos = r'D:\Facturas\hol.accdb'  # Reemplaza con la ruta de tu base de datos Access
#conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ruta_basedatos};'
#conn = pyodbc.connect(conn_str)
#excel_file_path = 'D:\Facturas\datos_facturas.xlsx'  # Ruta donde se guardará el archivo Excel

zip_files = [os.path.join(zip_folder_path, file) for file in os.listdir(zip_folder_path) if file.endswith('.zip')]

if not zip_files:
    print("No hay archivos ZIP para procesar en la carpeta especificada.")
else:
    invoices_without_info = []

for zip_file in zip_files:
    files_to_process = extract_pdfs_from_zip(zip_file, extraction_folder)
    if files_to_process:
        for pdf_file in files_to_process:
            print(f"Procesando archivo: {pdf_file}")
            total, subtotal, iva, razon_social, fecha_factura, empresa_vendedora = extract_info_from_pdf(pdf_file)
            print (f"--------------//---------")
            print (f"Total: {")
            print (f"--------------//---------")
            print (f"--------------//---------")

            data = [total, subtotal, iva, razon_social, fecha_factura, empresa_vendedora]
            excel_file_path = 'D:\Facturas\datos_facturas.xlsx'

            # Insertar los datos en el archivo Excel si alguno de los campos no es None
            if any(data):
                try:
                    insert_into_excel(data, excel_file_path)
                    print("Datos escritos en el archivo Excel.")
                except Exception as e:
                    print(f"Error al escribir datos en el archivo Excel: {e}")
                    invoices_without_info.append(pdf_file)
            else:
                invoices_without_info.append(pdf_file)

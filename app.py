
from flask import Flask, render_template, request, send_file, redirect, url_for
from PyPDF2 import PdfMerger
import os
from flask_cors import CORS




app = Flask(__name__)
CORS(app)  # Esto permite solicitudes de cualquier origen
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Asegúrate de que el directorio de uploads exista #
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Guardar los archivos PDF subidos
        files = request.files.getlist('pdf_files')
        pdf_list = []
        for file in files:
            if file.filename.endswith('.pdf'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                pdf_list.append(filepath)
        
        # Llamar a la función de merge
        merged_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'merged_document.pdf')
        merge_pdfs(pdf_list, merged_pdf_path)

        # Descargar el archivo fusionado
        return send_file(merged_pdf_path, as_attachment=True)
    
    return render_template('index.html')

def merge_pdfs(pdf_list, output):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output)
    merger.close()

if __name__ == '__main__':
    app.run(debug=True)

## version diferentes tipos de archivos

# from flask import Flask, render_template, request, send_file, redirect, url_for
# from PyPDF2 import PdfMerger
# from PIL import Image
# from fpdf import FPDF  # Para crear PDF desde imágenes
# import os

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads/'

# # Asegúrate de que el directorio de uploads exista
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         doc_type = request.form['doc_type']  # Recibir el tipo de documento
#         files = request.files.getlist('files')
#         file_list = []

#         for file in files:
#             if file.filename:
#                 filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#                 file.save(filepath)
#                 file_list.append(filepath)

#         merged_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'merged_document.{doc_type}')

#         # Fusionar los archivos según el tipo seleccionado
#         if doc_type == 'pdf':
#             merge_pdfs(file_list, merged_file_path)
#         elif doc_type == 'image':
#             merge_images(file_list, merged_file_path)
#         elif doc_type == 'text':
#             merge_texts(file_list, merged_file_path)
#         else:
#             return "Tipo de documento no soportado", 400

#         return send_file(merged_file_path, as_attachment=True)

#     return render_template('index.html')

# def merge_pdfs(pdf_list, output):
#     merger = PdfMerger()
#     for pdf in pdf_list:
#         merger.append(pdf)
#     merger.write(output)
#     merger.close()

# def merge_images(image_list, output):
#     images = [Image.open(image) for image in image_list]
#     pdf = FPDF()
#     for image in images:
#         pdf.add_page()
#         pdf.image(image.filename, 0, 0, 210, 297)  # Asumiendo tamaño A4
#     pdf.output(output)

# def merge_texts(text_list, output):
#     with open(output, 'w') as outfile:
#         for txt_file in text_list:
#             with open(txt_file, 'r') as infile:
#                 outfile.write(infile.read() + "\n")

# if __name__ == '__main__':
#     app.run(debug=True)

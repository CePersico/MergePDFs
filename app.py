
from flask import Flask, render_template, request, send_file, redirect, url_for
from PyPDF2 import PdfMerger
import os

app = Flask(__name__)
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

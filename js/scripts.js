// scripts.js

const pdfInput = document.getElementById('pdf-input');
const fileName = document.getElementById('file-name');
const noFileMessage = document.getElementById('no-file-message');
const fileList = document.getElementById('file-list');
const submitBtn = document.getElementById('submit-btn');
const form = document.getElementById('pdf-form');

let filesArray = [];

// Evento para mostrar el nombre del archivo seleccionado y actualizar la interfaz
pdfInput.addEventListener('change', function(event) {
    const files = event.target.files;

    if (files.length > 0) {
        noFileMessage.style.display = 'none'; // Ocultar el mensaje de no archivo

        for (const file of files) {
            filesArray.push(file); // Añadir cada archivo al array
            const li = document.createElement('li');
            li.textContent = file.name;
            fileList.appendChild(li);
            if (filesArray.length > 1) submitBtn.disabled = false; // Habilitar el botón de envío
        }

        fileName.textContent = `${filesArray.length} archivo(s) seleccionado(s)`;
    } else {
        fileName.textContent = 'No se ha seleccionado ningún archivo';
        noFileMessage.style.display = 'block';
        submitBtn.disabled = true; // Deshabilitar el botón de envío
    }
});

// Evento para manejar el envío del formulario
form.addEventListener('submit', function(event) {
    event.preventDefault();

    // Si no hay archivos seleccionados, muestra el mensaje y no procede
    if (filesArray.length === 0) {
        noFileMessage.style.display = 'block';
        return;
    }

    const formData = new FormData();
    for (const file of filesArray) {
        formData.append('pdf_files', file);
    }

    fetch('/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'merged_document.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    });

    // Resetear el formulario y la lista de archivos después del envío
    filesArray = [];
    fileList.innerHTML = '';
    fileName.textContent = 'No se ha seleccionado ningún archivo';
    submitBtn.disabled = true;
});

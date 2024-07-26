document.addEventListener('DOMContentLoaded', function () {
    const enlaceForm = document.getElementById('enlaceForm');
    const enlacesList = document.getElementById('enlacesList');
    const enlacesModal = new bootstrap.Modal(document.getElementById('Enlaces'), {
        backdrop: 'static',
        keyboard: false
    });

    enlaceForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evita la recarga de la página

        if (enlaceForm.checkValidity()) {
            const titulo = document.getElementById('tituloEnlace').value;
            const url = document.getElementById('urlEnlace').value;

            // Crear un nuevo elemento de lista
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                <span>
                    <strong>${titulo}</strong>: <a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>
                    <input type="hidden" value="${url}" name="link"/>
                    <input type="hidden" value="${titulo}" name="linkname"/>
                </span>
                <span>
                    <button class="btn btn-sm btn-warning edit-btn" aria-label="Editar enlace">Editar</button>
                    <button class="btn btn-sm btn-danger delete-btn" aria-label="Eliminar enlace">Eliminar</button>
                </span>
            `;

            // Añadir el nuevo elemento a la lista
            enlacesList.appendChild(li);

            // Limpiar el formulario
            enlaceForm.reset();
            enlaceForm.classList.remove('was-validated');

            // Añadir eventos para los botones de editar y eliminar
            li.querySelector('.edit-btn').addEventListener('click', function(event) {
                event.preventDefault();
                editarEnlace(li, titulo, url);
            });

            li.querySelector('.delete-btn').addEventListener('click', function() {
                li.remove();
            });

            // Ocultar manualmente el modal de enlaces sin cerrar los otros modales
            const modalBackdrop = document.querySelector('.modal-backdrop');
            if (modalBackdrop) {
                modalBackdrop.classList.add('d-none');
            }
            document.getElementById('Enlaces').classList.remove('show');
            document.body.classList.remove('modal-open');
            document.body.style = "";

        } else {
            enlaceForm.classList.add('was-validated');
        }
    }, false);
    
    function editarEnlace(li, titulo, url) {
        const newTitulo = prompt('Nuevo título:', titulo);
        const newUrl = prompt('Nuevo enlace:', url);
        if (newTitulo && newUrl) {
            li.querySelector('strong').textContent = newTitulo;
            const a = li.querySelector('a');
            a.textContent = newUrl;
            a.href = newUrl;
        }
    }
});

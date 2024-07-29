//* Editar enlaces
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-link').forEach(function(button) {
        button.addEventListener('click', function() {
            const id_link = this.getAttribute('data-id');
            const parent = this.parentElement;
            // Elimina los elementos específicos
            parent.querySelectorAll('strong, a, .edit-btn, .delete-btn').forEach(function(element) {
                element.remove();
            });
            // Agrega el input con el título y la clase invisible
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'deletedLink';
            input.value = id_link;
            input.classList.add('form-control', 'mb-3', 'invisible-input');
            parent.appendChild(input);
        });
    });

    document.querySelectorAll('.edit-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const title = this.getAttribute('data-title');
            const link = this.getAttribute('data-link');
            const id_link = this.getAttribute('data-id');
            const parent = this.parentElement;
            // Elimina los elementos específicos
            parent.querySelectorAll('strong, a, .edit-btn, .delete-btn').forEach(function(element) {
                element.remove();
            });
            // Agrega inputs de texto con los valores del título y el link
            const idInput = document.createElement('input');
            idInput.type = 'hidden';
            idInput.name = 'editedId';
            idInput.value = id_link;
            idInput.classList.add('form-control', 'mb-3');
            parent.appendChild(idInput);

            const titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.name = 'editedTitleLink';
            titleInput.value = title;
            titleInput.placeholder = 'Titulo';
            titleInput.classList.add('form-control', 'mb-3');
            titleInput.required;
            parent.appendChild(titleInput);

            const linkInput = document.createElement('input');
            linkInput.type = 'url';
            linkInput.name = 'editedLink';
            linkInput.value = link;
            linkInput.placeholder = 'https://www.ejemplo.com/';
            linkInput.required;
            linkInput.classList.add('form-control', 'mb-3');
            parent.appendChild(linkInput);

        });
    });
});

//*procesa los enlaces
document.getElementById('EditarNuevoEnlace').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita la recarga de la página
    const titulo = document.getElementById('editTitulo2').value;
    const url = document.getElementById('editEnlace2').value;

    // Crear un nuevo elemento de lista
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-center';
    li.innerHTML = `
        <span>
            <strong>${titulo}</strong>: <a href="${url}" target="_blank">${url}</a>
            <input type="text" style="display: none;" value="${url}" name="link"/>
            <input type="text" style="display: none;" value="${titulo}" name="linkname"/>
        </span>
        <span>
            <button class="btn btn-sm btn-warning edit-btn">Editar</button>
            <button class="btn btn-sm btn-danger delete-btn">Eliminar</button>
        </span>
    `;

    // Añadir el nuevo elemento a la lista
    document.getElementById('newEnlacesListEdit').appendChild(li);

    // Limpiar el formulario
    document.getElementById('EditarNuevoEnlace').reset();


    // Añadir eventos para los botones de editar y eliminar
    li.querySelector('.edit-btn').addEventListener('click', function(event) {
        event.preventDefault();
        const newTitulo = prompt('Nuevo título:', titulo);
        const newUrl = prompt('Nuevo enlace:', url);
        if (newTitulo && newUrl) {
            li.querySelector('strong').textContent = newTitulo;
            const a = li.querySelector('a');
            a.textContent = newUrl;
            a.href = newUrl;
            li.querySelector('input').value = newUrl;
        }
    });

    li.querySelector('.delete-btn').addEventListener('click', function() {
        li.remove();
    });
});
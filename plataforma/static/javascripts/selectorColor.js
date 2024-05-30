document.querySelectorAll('.color-option').forEach(function (el) {
    el.addEventListener('click', function () {
        document.querySelectorAll('.color-option').forEach(function (elem) {
            elem.classList.remove('selected');
        });
        el.classList.add('selected');
        // Aquí puedes agregar la lógica para cambiar el tema de color
    });
});

$(document).ready(function() {

    $('#nivel_estudios').select2({
        placeholder: "Nivel de estudios",
        allowClear: true
    });

    $('#lengua_materna').select2({
        placeholder: "Lengua materna",
        allowClear: true
    });

    $('#otras_lenguas').select2({ //buscador que no se cierra al seleccionar
        placeholder: "¿Más lenguas?",
        closeOnSelect: true
    });

});

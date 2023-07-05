$(document).ready(function() {
    // Manejar el clic en el botón de alternancia
    $('[data-drawer-toggle="logo-sidebar"]').on('click', function() {
        $('#logo-sidebar').toggleClass('translate-x-0');
    });

    // Manejar el clic en la imagen del usuario
    $('[data-dropdown-toggle="dropdown-user"]').on('click', function() {
        $('#dropdown-user').toggleClass('hidden');
    });

    // Ocultar el dropdown-user al hacer clic fuera de él
    $(document).on('click', function(event) {
        if (!$(event.target).closest('#dropdown-user').length && !$(event.target).closest('[data-dropdown-toggle="dropdown-user"]').length) {
            $('#dropdown-user').addClass('hidden');
        }
    });

    $('#mytable').DataTable({
        //"processing": true,
        //"serverSide": true,
        // "ajax": "/datatable/"
    });
});

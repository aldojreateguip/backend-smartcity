$(document).ready(function () {
    showSpinner();
    init_dt_devices();
    initMap();
    hideSpinner();
});

function init_dt_devices() {
    if ($.fn.DataTable.isDataTable('#dt_devices')) {
        $('#dt_devices').DataTable().destroy();
    }

    dt_devices = $('#dt_devices').DataTable({
        lengthChange: false,
        scrollX: true,
        language: {
            "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
        },
        dom: '<"top"lf>t<"bottom"ip><"clear">', // Personaliza la estructura de la tabla
        initComplete: function () {
            // Agrega el título a la tabla
            $('<h2 class="font-sans text-[#166658] underline font-bold">COMPACTADORAS</h2>').prependTo('.dataTables_wrapper');
        }
    });
}


function init_dt_details(id) {
    if ($.fn.DataTable.isDataTable('#dt_detail')) {
        $('#dt_detail').DataTable().destroy();
    }

    dt_details = $('#dt_detail').DataTable({
        lengthChange: false,
        scrollX: true,
        language: {
            "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
        },
        dom: '<"top"lf>t<"bottom"ip><"clear">', // Personaliza la estructura de la tabla
        initComplete: function () {
            // Crea el HTML para el título y el botón
            const titleHtml = `
                <div class="flex items-center space-x-4">
                    <h2 class="font-sans text-[#166658] underline font-bold">COMPACTADORA - ${id}</h2>
                    <button onclick="initBackBtn()" id="backBtn" class="p-2 text-sm focus:outline-none focus:ring-0 text-white h-12 w-12">
                        <svg
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                            stroke="#ff0000"
                            width="24" height="24"  <!-- Puedes ajustar el tamaño según sea necesario -->
                            >
                            <!-- Grupo para el fondo del SVG -->
                            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                            
                            <!-- Grupo para las guías de trazado del SVG -->
                            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                            
                            <!-- Grupo para los íconos y el contenido principal del SVG -->
                            <g id="SVGRepo_iconCarrier">
                                <!-- Línea diagonal que representa una 'X' -->
                                <path
                                d="M14.5 9.5L9.5 14.5M9.5 9.5L14.5 14.5"
                                stroke="#ff0000"
                                stroke-width="1.5"
                                stroke-linecap="round"
                                ></path>
                                
                                <!-- Círculo con borde que representa el contorno del icono -->
                                <path
                                d="M7 3.33782C8.47087 2.48697 10.1786 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 10.1786 2.48697 8.47087 3.33782 7"
                                stroke="#ff0000"
                                stroke-width="1.5"
                                stroke-linecap="round"
                                ></path>
                            </g>
                            </svg>
                    </button>
                </div>
            `;

            // Inserta el título y el botón en el contenedor de DataTables
            $('.dataTables_wrapper').prepend(titleHtml);
            dtails_dir = '1';
        }
    });
}



const detallebtns = document.getElementsByClassName('detallebtn');

async function initDetailsBtn(element) {
    const id = element.target.closest('button').id;


    const url = `/dashboard/${id}/`; // Asegúrate de que esta URL sea correcta

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const html = await response.text();
        const tables_box = document.getElementById('tables_box');
        tables_box.innerHTML = html;

        init_dt_details(id);
    } catch (error) {
        console.error('Error:', error);
    }
};


async function initBackBtn() {
    showSpinner();
    const url = `/getdevicesdata/`; // Asegúrate de que esta URL sea correcta
    dtails_dir = '0';
    try {
        // Realiza la solicitud fetch a la URL
        const response = await fetch(url);

        // Verifica si la respuesta es exitosa
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // Obtiene el contenido HTML de la respuesta
        const html = await response.text();

        // Inserta el contenido HTML en el contenedor con ID 'tables_box'
        const tables_box = document.getElementById('tables_box');
        tables_box.innerHTML = html;

        // Inicializa la tabla con DataTables pasando el ID correcto
        init_dt_devices();
        hideSpinner();
    } catch (error) {
        // Manejo de errores en caso de que la solicitud falle
        console.error('Error:', error);
    }
};


document.getElementById('toggleButton').addEventListener('click', function () {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('main');

    sidebar.classList.toggle('-translate-x-full');
    sidebar.classList.toggle('translate-x-0');

    // Ajusta el contenido principal si el aside está visible
    if (sidebar.classList.contains('translate-x-0')) {
        mainContent.classList.add('pl-64'); // Ajusta este valor según el ancho del aside
    } else {
        mainContent.classList.remove('pl-64');
    }
});


function initMap() {
    const iconMarkerUrl = "{% static 'img/camion-2.png' %}";
    var dtails_dir = '0';

    // inicializar mapa
    let marker = null;
    let myMap = L.map('mapa').setView([-3.746241, -73.2478283], 13);

    const urlOpenLayers = 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png';
    L.tileLayer(urlOpenLayers, {
        maxZoom: 19,
    }).addTo(myMap);

    const iconMarker = L.icon({
        iconUrl: iconMarkerUrl,
        iconSize: [60, 30],
        iconAnchor: [30, 60]
    });
}

if (dtails_dir == '0') {
    setInterval(actualizarUbicacionMarcadorDevices, 3000);
} else {
    setInterval(actualizarRutaDetails, 3000);
}

function actualizarUbicacionMarcadorDevices() {
    console.log(dtails_dir);
    $.ajax({
        url: '/getmarker/',
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            var latitude = response.latitud;
            var longitude = response.longitud;

            if (latitude === undefined || longitude === undefined || latitude === null || longitude === null) {
                // console.log('No se encontraron datos para el marcador.');
                return;
            }

            if (marker) {
                myMap.removeLayer(marker);
            }

            marker = L.marker([latitude, longitude], {
                icon: iconMarker
            }).addTo(myMap);

            // setTimeout(actualizarUbicacionMarcador, 3000);
        },
        error: function (error) {
            console.log('Error al obtener la ubicación del marcador:', error);
        }
    });
}


function actualizarRutaDetails() {
    console.log(dtails_dir);
    // Obtener la URL actual
    let currentUrl = window.location.pathname;

    // Reemplazar "dashboard" por "gethistory" en la URL
    let newUrl = currentUrl.replace('dashboard', 'gethistory');

    $.ajax({
        url: newUrl,  // Usamos la URL modificada
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            let registros = response.dashboard_detail;

            // Verificar si hay datos
            if (!registros || registros.length === 0) {
                // console.log('No se encontraron datos.');
                return;  // Salir de la función si no hay datos
            }

            rutaCoords = [];

            for (let i = 0; i < registros.length; i++) {
                let lat = registros[i].latitud;
                let lon = registros[i].longitud;
                rutaCoords.push([lat, lon]);
            }

            if (polyline) {
                myMap.removeLayer(polyline);
            }

            polyline = L.polyline(rutaCoords, { color: 'red' }).addTo(myMap);

            myMap.fitBounds(polyline.getBounds());
        },
        error: function (error) {
            // console.log('Error al obtener nuevas coordenadas:', error);
        }
    });
}
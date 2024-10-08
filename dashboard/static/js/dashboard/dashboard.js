const iconMarkerUrl = document.getElementById('mapa').getAttribute('data-icon-marker-url');
var dtails_dir = 0;
let iconMarker;
// inicializar mapa
let marker = null;
let myMap;
let dt_devices_table;
let dt_details_table;
let urlOpenLayers;
let dt_details;
let dt_devices;
let gpsid = null;
let polyline;
var rutaCoords = [];

$(document).ready(function () {
    initMap();
    initSettingsBtn();
    init_dt_devices();
    init_dt_details();
    ocultar_details_table();
});


function initSettingsBtn() {
    // Manejar el clic en la imagen del usuario
    $('[data-dropdown-toggle="dropdown-user"]').on('click', function () {
        $('#dropdown-user').toggleClass('hidden');
    });

    // Ocultar el dropdown-user al hacer clic fuera de él
    $(document).on('click', function (event) {
        if (!$(event.target).closest('#dropdown-user').length && !$(event.target).closest('[data-dropdown-toggle="dropdown-user"]').length) {
            $('#dropdown-user').addClass('hidden');
        }
    });
}

function ocultar_devices_table() {
    // Añade la clase 'hidden' a la tabla de detalles y la elimina de la tabla de dispositivos
    document.getElementById('devices_box').classList.add('hidden');
    document.getElementById('details_box').classList.remove('hidden');
    document.getElementById('devices_title').classList.add('hidden');
    document.getElementById('details_title').classList.remove('hidden');
    destroydt_details();
    init_dt_details();
}

function ocultar_details_table() {
    // Añade la clase 'hidden' a la tabla de dispositivos y la elimina de la tabla de detalles
    document.getElementById('devices_box').classList.remove('hidden');
    document.getElementById('details_box').classList.add('hidden');
    document.getElementById('devices_title').classList.remove('hidden');
    document.getElementById('details_title').classList.add('hidden');
    destroydt_devices();
    init_dt_devices();
}


function init_dt_devices() {
    dt_devices = $('#dt_devices').DataTable({
        lengthChange: false,
        scrollX: true,
        dom: '<"top"lf>t<"bottom"ip><"clear">', // Personaliza la estructura de la tabla
    });
}

function init_dt_details() {
    dt_details = $('#dt_detail').DataTable({
        lengthChange: false,
        scrollX: true,
        dom: '<"top"lf>t<"bottom"ip><"clear">', // Personaliza la estructura de la tabla
    });
}

function destroydt_details() {
    if (dt_details) {
        dt_details.destroy();
    }
}
function destroydt_devices() {
    if (dt_devices) {
        dt_devices.destroy();
    }
}


async function getDetailsData(element) {
    dtails_dir = 1;
    showSpinner();
    const id = element.id;
    gpsid = id;
    document.getElementById('idCompactadora').innerHTML = '';
    document.getElementById('idCompactadora').textContent = id;
    ocultar_devices_table();
    dt_details.clear();
    try {
        const response = await fetch(`/dashboard/${id}/`, {
            method: 'GET',
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        rutaCoords = [];
        const data = await response.json();
        counter = 0;
        dt_details.clear();
        const inverted = data.dashboard_detail.reverse();
        var lat_marker = data.lat_marker;
        var lon_marker = data.lon_marker;
        let lastDetails = null;  // Para guardar el último valor
        inverted.forEach((details, index) => {
            counter = counter + 1;
            coords = `${details.latitud}, ${details.longitud}`;
            rutaCoords.push([details.latitud, details.longitud]);

            dt_details.row.add([
                counter,
                details.fecha,
                coords, // Formato de latitud y longitud
                details.velocidad,
                details.distancia,
                details.tiempoDetenido,
            ]).draw();  // Añadir fila y redibujar tabla

            // Guardar la última posición
            if (index === inverted.length - 1) {
                lastDetails = details;
            }
        });
        if (marker) {
            marker.remove();
        }
        if (markers) {
            for (var i in markers) {
                myMap.removeLayer(markers[i]);
            }
            markers = [];  // Reiniciamos el array de marcadores
        }
        if (polyline) {
            myMap.removeLayer(polyline);
        }
        marker = L.marker([lat_marker, lon_marker], {
            icon: iconMarker
        }).addTo(myMap);
        polyline = L.polyline(rutaCoords, { color: 'red' }).addTo(myMap);
    }
    catch {
        toastr.error("Ha ocurrido un error en la actualizacion de datos");
    };
    hideSpinner();
};


async function getDetailsDataBucle() {
    if (gpsid != null) {
        try {
            const response = await fetch(`/dashboard/${gpsid}/`, {
                method: 'GET',
            });
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            const data = await response.json();
            rutaCoords = [];
            counter = 0;
            const inverted = data.dashboard_detail.reverse();
            var lat_marker = data.lat_marker;
            var lon_marker = data.lon_marker;
            dt_details.clear();
            inverted.forEach(details => {
                counter = counter + 1;
                coords = `${details.latitud}, ${details.longitud}`;
                rutaCoords.push([details.latitud, details.longitud]);

                dt_details.row.add([
                    counter,
                    details.fecha,
                    coords, // Formato de latitud y longitud
                    details.velocidad,
                    details.distancia,
                    details.tiempoDetenido,
                ]).draw();  // Añadir fila y redibujar tabla
            });
            if (marker) {
                marker.remove();
            }
            if (markers) {
                for (var i in markers) {
                    myMap.removeLayer(markers[i]);
                }
                markers = [];  // Reiniciamos el array de marcadores
            }
            if (polyline) {
                myMap.removeLayer(polyline);
            }
            marker = L.marker([lat_marker, lon_marker], {
                icon: iconMarker
            }).addTo(myMap);
            polyline = L.polyline([rutaCoords], { color: 'red' }).addTo(myMap);
        }
        catch {
            toastr.error("Ha ocurrido un error en la actualizacion de datos");
        };
        hideSpinner();
    }
};
async function getDevicesDataBucle() {
    if (gpsid == null) {
        try {
            const response = await fetch('/getdevicesdata/', {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            const data = await response.json();
            dt_devices.clear(); // Limpiar datos existentes
            counter = 0;

            data.devices_data.forEach(device => {
                counter = counter + 1;
                dt_devices.row.add([
                    counter,
                    device.placa,
                    device.modelo === null ? 'S/M' : device.modelo,
                    device.categoria === null ? 'S/C' : device.categoria,
                    device.actualizado,
                    device.estado,
                    `<div>
                        <button type="button" onclick="getDetailsData(this)" id="${device.id}" class="detallebtn p-2 group transform transition-transform duration-300 hover:scale-105 hover:filter hover:brightness-90">
                            <svg class="transition-all duration-300 ease-in-out" fill="#166658" viewBox="0 0 64 64" width="24" height="24" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" stroke="#166658">
                                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                                <g id="SVGRepo_iconCarrier">
                                    <path d="M36,21c0-2.206-1.794-4-4-4s-4,1.794-4,4s1.794,4,4,4S36,23.206,36,21z M30,21c0-1.103,0.897-2,2-2s2,0.897,2,2 s-0.897,2-2,2S30,22.103,30,21z"></path>
                                    <path d="M27,41v6h10v-6h-2V27h-8v6h2v8H27z M29,31v-2h4v14h2v2h-6v-2h2V31H29z"></path>
                                    <path d="M32,1C14.907,1,1,14.907,1,32s13.907,31,31,31s31-13.907,31-31S49.093,1,32,1z M32,61C16.009,61,3,47.991,3,32 S16.009,3,32,3s29,13.009,29,29S47.991,61,32,61z"></path>
                                    <path d="M32,7c-5.236,0-10.254,1.607-14.512,4.649l1.162,1.628C22.567,10.479,27.184,9,32,9c12.682,0,23,10.318,23,23 c0,4.816-1.479,9.433-4.277,13.35l1.628,1.162C55.393,42.254,57,37.236,57,32C57,18.215,45.785,7,32,7z"></path>
                                    <path d="M32,55C19.318,55,9,44.682,9,32c0-4.817,1.479-9.433,4.277-13.35l-1.627-1.162C8.608,21.746,7,26.764,7,32 c0,13.785,11.215,25,25,25c5.236,0,10.254-1.607,14.512-4.649l-1.162-1.628C41.433,53.521,36.816,55,32,55z"></path>
                                </g>
                            </svg>
                        </button>
                    </div>`
                ]).draw();  // Añadir fila y redibujar tabla  // Añadir fila y redibujar tabla
            });
            if (marker) {
                myMap.removeLayer(marker.remove());
            }
            if (polyline) {
                myMap.removeLayer(polyline);
                rutaCoords = [];
            }

            if (markers) {
                for (var i in markers) {
                    myMap.removeLayer(markers[i]);
                }
                markers = [];  // Reiniciamos el array de marcadores
            }
            for (var deviceId in data.coords_marker) {
                var latitud = data.coords_marker[deviceId].latitude;
                var longitud = data.coords_marker[deviceId].longitude;

                // Verificamos si las coordenadas son válidas
                if (latitud != undefined && longitud != undefined) {
                    var marker = L.marker([latitud, longitud], {
                        icon: iconMarker
                    }).addTo(myMap);

                    // Almacenar el marcador en un array si quieres manejar múltiples marcadores
                    markers.push(marker);
                }
            }
            hideSpinner();
        }
        catch {
            toastr.error("Ha ocurrido un error en la actualizacion de datos");
        }
    }
};

async function getDevicesData() {
    gpsid = null;
    showSpinner();
    ocultar_details_table();
    try {
        const response = await fetch('/getdevicesdata/', {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        dt_devices.clear(); // Limpiar datos existentes
        counter = 0;

        data.devices_data.forEach(device => {
            counter = counter + 1;
            dt_devices.row.add([
                counter,
                device.placa,
                device.modelo === null ? 'S/M' : device.modelo,
                device.categoria === null ? 'S/C' : device.categoria,
                device.actualizado,
                device.estado,
                `<div>
                    <button type="button" onclick="getDetailsData(this)" id="${device.id}" class="detallebtn p-2 group transform transition-transform duration-300 hover:scale-105 hover:filter hover:brightness-90">
                        <svg class="transition-all duration-300 ease-in-out" fill="#166658" viewBox="0 0 64 64" width="24" height="24" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" stroke="#166658">
                            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                            <g id="SVGRepo_iconCarrier">
                                <path d="M36,21c0-2.206-1.794-4-4-4s-4,1.794-4,4s1.794,4,4,4S36,23.206,36,21z M30,21c0-1.103,0.897-2,2-2s2,0.897,2,2 s-0.897,2-2,2S30,22.103,30,21z"></path>
                                <path d="M27,41v6h10v-6h-2V27h-8v6h2v8H27z M29,31v-2h4v14h2v2h-6v-2h2V31H29z"></path>
                                <path d="M32,1C14.907,1,1,14.907,1,32s13.907,31,31,31s31-13.907,31-31S49.093,1,32,1z M32,61C16.009,61,3,47.991,3,32 S16.009,3,32,3s29,13.009,29,29S47.991,61,32,61z"></path>
                                <path d="M32,7c-5.236,0-10.254,1.607-14.512,4.649l1.162,1.628C22.567,10.479,27.184,9,32,9c12.682,0,23,10.318,23,23 c0,4.816-1.479,9.433-4.277,13.35l1.628,1.162C55.393,42.254,57,37.236,57,32C57,18.215,45.785,7,32,7z"></path>
                                <path d="M32,55C19.318,55,9,44.682,9,32c0-4.817,1.479-9.433,4.277-13.35l-1.627-1.162C8.608,21.746,7,26.764,7,32 c0,13.785,11.215,25,25,25c5.236,0,10.254-1.607,14.512-4.649l-1.162-1.628C41.433,53.521,36.816,55,32,55z"></path>
                            </g>
                        </svg>
                    </button>
                </div>`
            ]).draw();  // Añadir fila y redibujar tabla  // Añadir fila y redibujar tabla
        });
        if (marker) {
            myMap.removeLayer(marker.remove());
        }
        if (polyline) {
            myMap.removeLayer(polyline);
            rutaCoords = [];
        }

        if (markers) {
            for (var i in markers) {
                myMap.removeLayer(markers[i]);
            }
            markers = [];  // Reiniciamos el array de marcadores
        }
        for (var deviceId in data.coords_marker) {
            var latitud = data.coords_marker[deviceId].latitude;
            var longitud = data.coords_marker[deviceId].longitude;

            // Verificamos si las coordenadas son válidas
            if (latitud != undefined && longitud != undefined) {
                var marker = L.marker([latitud, longitud], {
                    icon: iconMarker
                }).addTo(myMap);

                // Almacenar el marcador en un array si quieres manejar múltiples marcadores
                markers.push(marker);
            }
        }
        hideSpinner();
    }
    catch {
        toastr.error("Ha ocurrido un error en la actualizacion de datos");
    }
};
window.onload = function () {
    getDevicesData();
}


// ##########################################################

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

var markers = [];

function initMap() {
    myMap = L.map('mapa').setView([-3.746241, -73.2478283], 13);

    urlOpenLayers = 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png';

    L.tileLayer(urlOpenLayers, {
        maxZoom: 19,
    }).addTo(myMap);

    iconMarker = L.icon({
        iconUrl: iconMarkerUrl,
        iconSize: [60, 30],
        iconAnchor: [30, 60]
    });
}


setInterval(getDetailsDataBucle, 10000);
setInterval(getDevicesDataBucle, 10000);

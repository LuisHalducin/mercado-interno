$(document).ready(function() {
    $('#buildingName').select2(); // Aplica Select2 al desplegable
    
    $('#buildingName').change(function() {
        cambiarImagen();  // Llama a la función cambiarImagen cuando el usuario selecciona un edificio
        //calcularCosto();   // Recalcula el costo y las horas cuando cambia la selección
    });
});

function cambiarImagen() {
    const edificio = document.getElementById('buildingName').value;
    let imagen;
    
    // Asignar la ruta de la imagen según el edificio seleccionado
    switch(edificio) {
        case 'edificio1':
            imagen = "static/img/granja.webp"; 
            break;
        case 'edificio2':
            imagen = "static/img/corral.webp"; 
            break;
        case 'edificio3':
            imagen = "static/img/panaderia.webp"; 
            break;
        case 'edificio4':
            imagen = "static/img/fabrica_bebidad.webp"; 
            break;
        case 'edificio5':
            imagen = "static/img/abastecimiento.webp"; 
            break;
        case 'edificio6':
            imagen = "static/img/procesadoraalimentos.webp"; 
            break;
        case 'edificio7':
            imagen = "static/img/molino.webp"; 
            break;
        case 'edificio8':
            imagen = "static/img/matadero.webp"; 
            break;
        case 'edificio9':
            imagen = "static/img/plantaconcreto.webp"; 
            break;
        case 'edificio10':
            imagen = "static/img/fabricaconstruccion.webp"; 
            break;
        case 'edificio11':
            imagen = "static/img/contratista.webp"; 
            break;
         case 'edificio12':
            imagen = "static/img/cantera.webp"; 
            break;
        case 'edificio13':
            imagen = "static/img/fabrica_textil.webp"; 
            break;
        case 'edificio14':
            imagen = "static/img/petrolera.webp"; 
            break;
        case 'edificio15':
            imagen = "static/img/electricidad.webp"; 
            break;
        case 'edificio16':
            imagen = "static/img/refineria.webp"; 
            break;
        case 'edificio17':
            imagen = "static/img/satelites.webp"; 
            break;
        case 'edificio18':
            imagen = "static/img/fabricaelectronicos.webp"; 
            break;
        case 'edificio19':
            imagen = "static/img/fabricaautos.webp"; 
            break;
        case 'edificio20':
            imagen = "static/img/propulsores.webp"; 
            break;
        case 'edificio21':
            imagen = "static/img/hangar.webp"; 
            break;
        case 'edificio22':
            imagen = "static/img/vertical.webp"; 
            break;
        case 'edificio23':
            imagen = "static/img/fabrica.webp"; 
            break;
         case 'edificio24':
            imagen = "static/img/mina.webp"; 
            break;
        case 'edificio25':
            imagen = "static/img/transporte.webp"; 
            break;
        case 'edificio26':
            imagen = "static/img/agua.webp"; 
            break;
        case 'edificio27':
            imagen = "static/img/invauntomotriz.webp"; 
            break;
        case 'edificio28':
            imagen = "static/img/invganadera.webp"; 
            break;
        case 'edificio29':
            imagen = "static/img/invquimica.webp"; 
            break;
        case 'edificio30':
            imagen = "static/img/invmoda.webp"; 
            break;
        case 'edificio31':
            imagen = "static/img/recetas.webp"; 
            break;
        case 'edificio32':
            imagen = "static/img/invenergetica.webp"; 
            break;
        case 'edificio33':
            imagen = "static/img/invagricola.webp"; 
            break;
        case 'edificio34':
            imagen = "static/img/invsoftware.webp"; 
            break;
        case 'edificio35':
            imagen = "static/img/plataformalanzamiento.webp"; 
            break;
         case 'edificio36':
            imagen = "static/img/tiendacomestible.webp"; 
            break;
        case 'edificio37':
            imagen = "static/img/tiendaelectronica.webp"; 
            break;
        case 'edificio38':
            imagen = "static/img/ferreeteria.webp"; 
            break;
        case 'edificio39':
            imagen = "static/img/estaciongas.webp"; 
            break;
        case 'edificio40':
            imagen = "static/img/tiendamoda.webp"; 
            break;
        case 'edificio41':
            imagen = "static/img/tiendaautos.webp"; 
            break;
        case 'edificio42':
            imagen = "static/img/oficinascorp.webp"; 
            break;
        case 'edificio43':
            imagen = "static/img/restaurante.webp"; 
            break;
        case 'edificio44':
            imagen = "static/img/castillo.webp"; 
            break;
        case 'edificio45':
            imagen = "static/img/parque.webp"; 
            break;
        case 'edificio46':
            imagen = "static/img/lago.webp"; 
            break;
        case 'edificio47':
            imagen = "static/img/banco.webp"; 
            break;
         case 'edificio48':
            imagen = "static/img/fabricaaeroespacial.webp"; 
            break;
        // Puedes agregar más casos para otros edificios...
        default:
            imagen = "static/img/sim-companies.webp"; 
    } 
    document.getElementById('buildingImage').src = imagen;
}

// Función para calcular el costo y las horas de construcción basado en el edificio y el número de niveles
function calcularCosto() {

    const button = document.getElementById('calcularBtn');

    // Activamos la animación de carga
    button.classList.add('loading');
    button.disabled = true;

    const edificio = document.getElementById('buildingName').value;
    const niveles = parseInt(document.getElementById('levelNumber').value);
    
    // Validación del número de niveles
    if (isNaN(niveles) || niveles < 1 || niveles > 50) {
        alert("Por favor, ingrese un número de niveles válido entre 1 y 50.");
        return;
    }

    // Definir costos base y horas base por edificio
    let costoBase;
    let horasBase

    // Establecer costos base y horas base según el edificio seleccionado
    switch(edificio) {
        case 'edificio1':
            costoBase = 6900;
            horasBase = 1; // Horas para el edificio A
            break;
        case 'edificio2':
            costoBase = 10350;
            horasBase = 2; // Horas para el edificio B
            break;
        case 'edificio3':
            costoBase = 37950;
            horasBase = 5; // Horas para el edificio C
            break;
        case 'edificio4':
            costoBase = 13800;
            horasBase = 2; // Horas para el edificio D
            break;
        case 'edificio5':
            costoBase = 103500;
            horasBase = 4; // Horas para el edificio E
            break;
        case 'edificio6':
            costoBase = 86250;
            horasBase = 6; // Horas para el edificio F
            break;
        case 'edificio7':
            costoBase = 27600;
            horasBase = 3; // Horas para el edificio A
            break;
        case 'edificio8':
            costoBase = 20700;
            horasBase = 4; // Horas para el edificio B
            break;
        case 'edificio9':
            costoBase = 58650;
            horasBase = 5; // Horas para el edificio C
            break;
        case 'edificio10':
            costoBase = 72450;
            horasBase = 6; // Horas para el edificio D
            break;
        case 'edificio11':
            costoBase = 48300;
            horasBase = 2; // Horas para el edificio E
            break;
        case 'edificio12':
            costoBase = 24150;
            horasBase = 3; // Horas para el edificio F
            break;
        case 'edificio13':
            costoBase = 13800;
            horasBase = 2; // Horas para el edificio A
            break;
        case 'edificio14':
            costoBase = 69000;
            horasBase = 4; // Horas para el edificio B
            break;
        case 'edificio15':
            costoBase = 51750;
            horasBase = 3; // Horas para el edificio C
            break;
        case 'edificio16':
            costoBase = 69000;
            horasBase = 4; // Horas para el edificio D
            break;
        case 'edificio17':
            costoBase = 141450;
            horasBase = 6; // Horas para el edificio E
            break;
        case 'edificio18':
            costoBase = 82800;
            horasBase = 5; // Horas para el edificio F
            break;
        case 'edificio19':
            costoBase = 93150;
            horasBase = 6; // Horas para el edificio A
            break;
        case 'edificio20':
            costoBase = 103500;
            horasBase = 7; // Horas para el edificio B
            break;
        case 'edificio21':
            costoBase = 100050;
            horasBase = 3; // Horas para el edificio C
            break;
        case 'edificio22':
            costoBase = 113850;
            horasBase = 3; // Horas para el edificio D
            break;
        case 'edificio23':
            costoBase = 48300;
            horasBase = 3; // Horas para el edificio E
            break;
        case 'edificio24':
            costoBase = 24150;
            horasBase = 4; // Horas para el edificio F
            break;
        case 'edificio25':
            costoBase = 51750;
            horasBase = 3; // Horas para el edificio A
            break;
        case 'edificio26':
            costoBase = 20700;
            horasBase = 2; // Horas para el edificio B
            break;
        case 'edificio27':
            costoBase = 138000;
            horasBase = 6; // Horas para el edificio C
            break;
        case 'edificio28':
            costoBase = 96600;
            horasBase = 5; // Horas para el edificio D
            break;
        case 'edificio29':
            costoBase = 96600;
            horasBase = 5; // Horas para el edificio E
            break;
        case 'edificio30':
            costoBase = 72450;
            horasBase = 2; // Horas para el edificio F
            break;
        case 'edificio31':
            costoBase = 82800;
            horasBase = 4; // Horas para el edificio A
            break;
        case 'edificio32':
            costoBase = 165600;
            horasBase = 7; // Horas para el edificio B
            break;
        case 'edificio33':
            costoBase = 103500;
            horasBase = 5; // Horas para el edificio C
            break;
        case 'edificio34':
            costoBase = 65550;
            horasBase = 3; // Horas para el edificio D
            break;
        case 'edificio35':
            costoBase = 124200;
            horasBase = 9; // Horas para el edificio E
            break;
        case 'edificio36':
            costoBase = 10350;
            horasBase = 1; // Horas para el edificio F
            break;
        case 'edificio37':
            costoBase = 17250;
            horasBase = 1; // Horas para el edificio A
            break;
        case 'edificio38':
            costoBase = 13800;
            horasBase = 4; // Horas para el edificio B
            break;
        case 'edificio39':
            costoBase = 24150;
            horasBase = 2; // Horas para el edificio C
            break;
        case 'edificio40':
            costoBase = 17250;
            horasBase = 3; // Horas para el edificio D
            break;
        case 'edificio41':
            costoBase = 20700;
            horasBase = 3; // Horas para el edificio E
            break;
        case 'edificio42':
            costoBase = 62100;
            horasBase = 2; // Horas para el edificio F
            break;
        case 'edificio43':
            costoBase = 89700;
            horasBase = 3; // Horas para el edificio A
            break;
        case 'edificio44':
            costoBase = 138000;
            horasBase = 12; // Horas para el edificio B
            break;
        case 'edificio45':
            costoBase = 138000;
            horasBase = 12; // Horas para el edificio C
            break;
        case 'edificio46':
            costoBase = 138000;
            horasBase = 12; // Horas para el edificio D
            break;
        case 'edificio47':
            costoBase = 138000;
            horasBase = 8; // Horas para el edificio E
            break;
        case 'edificio48':
            costoBase = 106950;
            horasBase = 6; // Horas para el edificio F
            break;
        default:
            costoBase = 0;
            horasBase = 0;
    }

   // Simulamos tiempo de carga para mostrar el spinner
   setTimeout(() => {
    const costoTotal = (((niveles - 1) * niveles) / 2 + 1) * costoBase;
    const horasTotales = (((niveles - 1) * niveles) / 2 + 1) * horasBase;

    const dias = Math.floor(horasTotales / 24);
    const horasRestantes = horasTotales % 24;

    const costoFormateado = costoTotal.toLocaleString();

    document.getElementById('result').innerText = `Total Cost: $ ${costoFormateado}`;
document.getElementById('timeResult').innerText = `Total Construction Time: ${dias} days ${horasRestantes} hours (${horasTotales} hours)`;

document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });

button.classList.remove('loading');
button.disabled = false;

mostrarToast("Calculation completed successfully!", "success");
}, 1200);
}
// Función para mostrar toasts actualizada
function mostrarToast(mensaje, tipo) {
    Toastify({
        text: mensaje,
        duration: 3000,
        gravity: "top",
        position: "right",
        style: {
            background: tipo === "error" ? "#ff4b5c" : "#4CAF50"
        },
        stopOnFocus: true
    }).showToast();
}

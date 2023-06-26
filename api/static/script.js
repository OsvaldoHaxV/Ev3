document.addEventListener("DOMContentLoaded", function() {
    // Se ejecuta cuando el contenido del documento HTML ha sido completamente cargado y parseado.

    // Se establece un intervalo para llamar a la función "actualizarEstadoServidor" cada 10 segundos.
    setInterval(actualizarEstadoServidor, 10000);

    const resultadoForm = document.getElementById("resultado-form");
    resultadoForm.addEventListener("submit", function(event) {
        // Se evita el comportamiento por defecto del formulario al ser enviado.
        event.preventDefault();

        // Se obtiene el valor del campo de entrada con el ID "juego-id-input".
        const juegoId = document.getElementById("juego-id-input").value;

        // Se llama a la función "consultarResultadoJuego" pasando el juegoId como argumento.
        consultarResultadoJuego(juegoId);
    });
});

function actualizarEstadoServidor() {
    // Se realiza una petición fetch al endpoint "/estado_servidor".
    fetch("/estado_servidor")
        .then(response => response.json())
        .then(data => {
            // Se actualiza el contenido del elemento con el ID "estado" con el estado del servidor obtenido de la respuesta.
            const estadoServidor = document.getElementById("estado");
            estadoServidor.textContent = "Estado del servidor: " + data.estado_servidor;

            // Se actualiza el contenido del elemento con el ID "juego-id" con el ID del juego obtenido de la respuesta.
            const juegoId = document.getElementById("juego-id");
            juegoId.textContent = "ID del juego en curso o disponible: " + data.juego_id;
        });
}

function consultarResultadoJuego(juegoId) {
    // Se realiza una petición fetch al endpoint "/resultado_juego/{juegoId}" con el ID del juego como parte de la URL.
    fetch(`/resultado_juego/${juegoId}`)
        .then(response => response.json())
        .then(data => {
            // Se actualiza el contenido del elemento con el ID "jugador-ganador" con el jugador ganador obtenido de la respuesta.
            const jugadorGanador = document.getElementById("jugador-ganador");
            jugadorGanador.textContent = "Jugador Ganador: " + data.jugador_ganador;

            // Se actualiza el contenido del elemento con el ID "puntaje-acumulado" con el puntaje acumulado obtenido de la respuesta.
            const puntajeAcumulado = document.getElementById("puntaje-acumulado");
            puntajeAcumulado.textContent = "Puntaje acumulado de los jugadores: " + data.puntaje_acumulado;
        })
        .catch(error => {
            // En caso de error, se actualiza el contenido del elemento con el ID "jugador-ganador" con un mensaje de error.
            const jugadorGanador = document.getElementById("jugador-ganador");
            jugadorGanador.textContent = "No se pudo obtener el resultado del juego.";

            // Se vacía el contenido del elemento con el ID "puntaje-acumulado".
            const puntajeAcumulado = document.getElementById("puntaje-acumulado");
            puntajeAcumulado.textContent = "";
        });
}

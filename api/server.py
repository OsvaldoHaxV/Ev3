import csv
import os
from bottle import Bottle, request, template, static_file

app = Bottle()

juegos = {}

def actualizar_estado_servidor():
    # Actualiza el estado del servidor y el ID del juego en curso o disponible
    if len(juegos) > 0:
        estado_servidor = "ocupado"
        juego_id = next(iter(juegos.keys()))  # Obtiene el primer juego de la lista
    else:
        estado_servidor = "disponible"
        juego_id = ""

    return {
        "estado_servidor": estado_servidor,
        "juego_id": juego_id
    }

def guardar_jugada(jugador_id, juego_id, valor_jugada):
    num_jugada = len(juegos[juego_id]) + 1
    jugador_ganador = obtener_jugador_ganador(juego_id)

    # Guarda la jugada en el archivo CSV
    with open("jugadas.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([jugador_id, juego_id, valor_jugada, num_jugada, jugador_ganador])

def obtener_jugador_ganador(juego_id):
    if len(juegos[juego_id]) >= 5:
        jugadas = juegos[juego_id]
        puntajes = [jugada[2] for jugada in jugadas]
        puntaje_total = sum(puntajes)
        jugador_ganador = max(jugadas, key=lambda x: x[2])[0] if puntaje_total > 0 else "Empate"

        del juegos[juego_id]  # Elimina el juego una vez que hay un ganador

        return jugador_ganador
    else:
        return ""

@app.post("/recibir_jugada")
def recibir_jugada():
    data = request.json
    jugador_id = data["jugador_id"]
    juego_id = data["juego_id"]
    valor_jugada = data["valor_jugada"]

    if juego_id not in juegos:
        juegos[juego_id] = []

    juegos[juego_id].append((jugador_id, juego_id, valor_jugada))
    guardar_jugada(jugador_id, juego_id, valor_jugada)

    return "Jugada recibida correctamente."

@app.get("/resultado_juego/<juego_id>")
def obtener_resultado_juego(juego_id):
    if juego_id not in juegos:
        return "El juego solicitado no existe."

    jugadas = juegos[juego_id]
    jugador_ganador = obtener_jugador_ganador(juego_id)
    puntaje_acumulado = sum(jugada[2] for jugada in jugadas)

    return {
        "jugador_ganador": jugador_ganador,
        "puntaje_acumulado": puntaje_acumulado
    }

@app.get("/estado_servidor")
def obtener_estado_servidor():
    estado_servidor = actualizar_estado_servidor()
    return estado_servidor

@app.route("/")
def index():
    return template("index")

@app.route("/static/<filename>")
def serve_static(filename):
    return static_file(filename, root="static")

if __name__ == "__main__":
    # Verifica si el archivo CSV ya existe y lo elimina si es necesario
    if os.path.exists("jugadas.csv"):
        os.remove("jugadas.csv")

    app.run(host="192.168.125.130", port=8080)

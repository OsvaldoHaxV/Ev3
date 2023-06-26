import requests
import random

def ingresar_id_jugador():
    jugador_id = input("Ingrese el ID del jugador: ")
    return jugador_id

def ingresar_id_juego():
    juego_id = input("Ingrese el ID del juego: ")
    return juego_id

def consultar_juego_disponible():
    response = requests.get("http://192.168.125.130:8080/estado_servidor")
    data = response.json()
    print("ID del juego disponible:", data["juego_id"])

def realizar_jugada(jugador_id, juego_id):
    valor_jugada = random.randint(1, 10)
    payload = {
        "jugador_id": jugador_id,
        "juego_id": juego_id,
        "valor_jugada": valor_jugada
    }
    response = requests.post("http://192.168.125.130:8080/recibir_jugada", json=payload)
    print("Jugada realizada exitosamente.")

def consultar_resultado_juego():
    juego_id = input("Ingrese el ID del juego: ")
    response = requests.get(f"http://192.168.125.130:8080/resultado_juego/{juego_id}")
    data = response.json()
    print("Jugador Ganador:", data["jugador_ganador"])
    print("Puntaje acumulado de los jugadores:", data["puntaje_acumulado"])

def mostrar_menu():
    print("MENU")
    print("1. Ingresar ID del jugador")
    print("2. Ingresar ID del juego")
    print("3. Consultar juego disponible")
    print("4. Realizar jugada")
    print("5. Consultar resultado del juego")
    print("6. Salir")
    print()

def ejecutar_menu():
    jugador_id = ""
    juego_id = ""

    while True:
        mostrar_menu()
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            jugador_id = ingresar_id_jugador()
        elif opcion == "2":
            juego_id = ingresar_id_juego()
        elif opcion == "3":
            consultar_juego_disponible()
        elif opcion == "4":
            if jugador_id == "" or juego_id == "":
                print("Debe ingresar el ID del jugador y del juego antes de realizar una jugada.")
            else:
                realizar_jugada(jugador_id, juego_id)
        elif opcion == "5":
            consultar_resultado_juego()
        elif opcion == "6":
            break
        else:
            print("Opción inválida. Intente nuevamente.")

        print()

ejecutar_menu()

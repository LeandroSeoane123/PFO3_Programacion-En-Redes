import argparse
import json
import socket

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5001

sesion = {
    "usuario": None,
    "contrasena": None
}

config = {
    "host": DEFAULT_HOST,
    "port": DEFAULT_PORT
}


def enviar_solicitud(payload):

    respuesta = None
    raw_response = None

    try:

        with socket.create_connection(
            (config["host"], config["port"]),
            timeout=5
        ) as sock:

            file = sock.makefile("rwb")

            file.write(
                json.dumps(
                    payload,
                    ensure_ascii=False
                ).encode("utf-8") + b"\n"
            )

            file.flush()

            raw_response = file.readline()

            if not raw_response:
                respuesta = {
                    "ok": False,
                    "error": "El servidor cerro la conexion."
                }
            else:
                respuesta = json.loads(
                    raw_response.decode("utf-8")
                )

    except ConnectionRefusedError:

        respuesta = {
            "ok": False,
            "error": "No se puede conectar al servidor."
        }

    except socket.timeout:

        respuesta = {
            "ok": False,
            "error": "La conexion con el servidor expiro."
        }

    except OSError as exc:

        respuesta = {
            "ok": False,
            "error": f"Error de red: {exc}"
        }

    except json.JSONDecodeError:

        respuesta = {
            "ok": False,
            "error": "El servidor respondio con JSON invalido."
        }

    return respuesta


def credenciales():

    datos = {
        "usuario": sesion["usuario"],
        "contrasena": sesion["contrasena"]
    }

    return datos


def mostrar_respuesta(respuesta):

    mensaje = None

    if respuesta.get("ok"):

        mensaje = respuesta.get(
            "mensaje",
            "Operacion realizada."
        )

        print(f"  {mensaje}")

    else:

        mensaje = respuesta.get(
            "error",
            "Error desconocido."
        )

        print(f"  Error: {mensaje}")


def registrar():

    usuario = None
    contrasena = None
    payload = None
    respuesta = None

    usuario = input(
        "  Nombre de usuario: "
    ).strip()

    contrasena = input(
        "  Contrasena: "
    ).strip()

    payload = {
        "accion": "registrar",
        "usuario": usuario,
        "contrasena": contrasena
    }

    respuesta = enviar_solicitud(payload)

    mostrar_respuesta(respuesta)


def login():

    usuario = None
    contrasena = None
    payload = None
    respuesta = None

    usuario = input(
        "  Usuario: "
    ).strip()

    contrasena = input(
        "  Contrasena: "
    ).strip()

    payload = {
        "accion": "login",
        "usuario": usuario,
        "contrasena": contrasena
    }

    respuesta = enviar_solicitud(payload)

    if respuesta.get("ok"):

        sesion["usuario"] = usuario
        sesion["contrasena"] = contrasena

    mostrar_respuesta(respuesta)


def ver_tareas():

    payload = None
    respuesta = None
    tareas = None

    payload = {
        "accion": "listar_tareas",
        **credenciales()
    }

    respuesta = enviar_solicitud(payload)

    if not respuesta.get("ok"):

        mostrar_respuesta(respuesta)
        return

    tareas = respuesta.get("tareas", [])

    if len(tareas) == 0:

        print("  No tenes tareas registradas.")
        return

    print(
        f"  Tareas de {sesion['usuario']}:"
    )

    for tarea in tareas:

        print(
            f"    #{tarea['id']} - "
            f"{tarea['descripcion']} "
            f"({tarea['creada_en']})"
        )


def crear_tarea():

    descripcion = None
    payload = None
    respuesta = None
    tarea = None

    descripcion = input(
        "  Descripcion de la tarea: "
    ).strip()

    if not descripcion:

        print(
            "  La descripcion no puede estar vacia."
        )

        return

    payload = {
        "accion": "crear_tarea",
        "descripcion": descripcion,
        **credenciales()
    }

    respuesta = enviar_solicitud(payload)

    if respuesta.get("ok"):

        tarea = respuesta["tarea"]

        print(
            f"  Tarea creada con id "
            f"#{tarea['id']}."
        )

    else:

        mostrar_respuesta(respuesta)


def eliminar_tarea():

    tarea_id = None
    payload = None
    respuesta = None

    ver_tareas()

    try:

        tarea_id = int(
            input(
                "  ID de la tarea a eliminar: "
            ).strip()
        )

    except ValueError:

        print("  ID invalido.")
        return

    payload = {
        "accion": "eliminar_tarea",
        "id": tarea_id,
        **credenciales()
    }

    respuesta = enviar_solicitud(payload)

    mostrar_respuesta(respuesta)


def cerrar_sesion():

    sesion["usuario"] = None
    sesion["contrasena"] = None

    print("  Sesion cerrada.")


MENU = [
    ("Registrar usuario", registrar),
    ("Iniciar sesion", login),
    ("Ver mis tareas", ver_tareas),
    ("Crear tarea", crear_tarea),
    ("Eliminar tarea", eliminar_tarea),
    ("Cerrar sesion", cerrar_sesion),
    ("Salir", None)
]


def requiere_sesion(accion):

    retorno = False

    if accion in (
        ver_tareas,
        crear_tarea,
        eliminar_tarea,
        cerrar_sesion
    ):
        retorno = True

    return retorno


def mostrar_menu():

    i = None

    for i, (nombre, _) in enumerate(MENU, 1):

        print(
            f"  {i}. {nombre}"
        )


def obtener_estado_sesion():

    estado = None

    if sesion["usuario"]:

        estado = (
            f"(logueado como "
            f"{sesion['usuario']})"
        )

    else:

        estado = "(sin sesion)"

    return estado


def main():

    opcion = None
    idx = None
    nombre = None
    accion = None
    estado = None

    print(
        "=== Sistema distribuido de gestion de tareas ==="
    )

    print(
        f"Servidor: "
        f"{config['host']}:{config['port']}"
    )

    while True:

        estado = obtener_estado_sesion()

        print(f"\n{estado}")

        mostrar_menu()

        opcion = input(
            "Elegi una opcion: "
        ).strip()

        if not opcion.isdigit():

            print("  Opcion invalida.")
            continue

        if not (
            1 <= int(opcion) <= len(MENU)
        ):

            print("  Opcion invalida.")
            continue

        idx = int(opcion) - 1

        nombre, accion = MENU[idx]

        if accion is None:

            print("  Hasta luego!")
            break

        if requiere_sesion(accion):

            if not sesion["usuario"]:

                print(
                    "  Necesitas iniciar sesion primero."
                )

                continue

        print(f"\n--- {nombre} ---")

        accion()


def parse_args():

    parser = argparse.ArgumentParser(
        description=(
            "Cliente TCP para gestion distribuida "
            "de tareas."
        )
    )

    parser.add_argument(
        "--host",
        default=DEFAULT_HOST
    )

    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT
    )

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    config["host"] = args.host
    config["port"] = args.port

    main()
Programacion en redes - Practica Formativa 3

Diagrama solicitado:

<img width="4261" height="1830" alt="Diagrama" src="https://github.com/user-attachments/assets/508e813d-5114-4d91-898c-9111c1d18698" />


Sistema Distribuido de Gestión de Tareas:
Descripción

Este proyecto implementa un sistema distribuido de gestión de tareas utilizando una arquitectura Cliente-Servidor basada en TCP.

Los usuarios pueden:

Registrarse en el sistema.
Iniciar sesión.
Crear tareas.
Consultar sus tareas.
Eliminar tareas.

La información se almacena de forma persistente en una base de datos SQLite y las contraseñas se almacenan de manera segura utilizando hashing con PBKDF2-HMAC-SHA256.

Arquitectura

El sistema está compuesto por dos aplicaciones:

Cliente (cliente.py)

Aplicación de consola que permite a los usuarios interactuar con el sistema.

Funciones disponibles:

Registro de usuarios.
Inicio de sesión.
Consulta de tareas.
Creación de tareas.
Eliminación de tareas.
Cierre de sesión.
Servidor (servidor.py)

Servidor TCP multihilo encargado de:

Recibir solicitudes de clientes.
Validar credenciales.
Gestionar usuarios.
Gestionar tareas.
Acceder a la base de datos.
Responder en formato JSON.
Tecnologías Utilizadas
Python 3
TCP Sockets
SQLite3
JSON
ThreadPoolExecutor
Multithreading
PBKDF2-HMAC-SHA256
HMAC
Estructura del Proyecto
.
├── cliente.py
├── servidor.py
├── tareas.db
└── README.md
Base de Datos

El sistema crea automáticamente una base de datos SQLite llamada:

tareas.db

La base contiene las siguientes tablas:

usuarios
Campo	Tipo
id	INTEGER
usuario	TEXT
salt	TEXT
contrasena_hash	TEXT
tareas
Campo	Tipo
id	INTEGER
usuario_id	INTEGER
descripcion	TEXT
creada_en	TEXT
Seguridad

Las contraseñas nunca se almacenan en texto plano.

Para cada usuario:

Se genera un salt aleatorio.
Se aplica PBKDF2-HMAC-SHA256.
Se almacena únicamente:
Salt
Hash generado

Durante el inicio de sesión se vuelve a calcular el hash y se compara utilizando:

hmac.compare_digest()
Comunicación Cliente-Servidor

La comunicación se realiza mediante sockets TCP.

Cada mensaje enviado utiliza formato JSON.

Ejemplo de solicitud
{
    "accion": "login",
    "usuario": "juan",
    "contrasena": "1234"
}
Ejemplo de respuesta exitosa
{
    "ok": true,
    "mensaje": "Bienvenido, juan!"
}
Ejemplo de respuesta con error
{
    "ok": false,
    "error": "Credenciales invalidas."
}
Acciones Disponibles
Registrar usuario

Permite crear una nueva cuenta.

Solicitud:

{
    "accion": "registrar",
    "usuario": "juan",
    "contrasena": "1234"
}
Iniciar sesión

Valida las credenciales del usuario.

Solicitud:

{
    "accion": "login",
    "usuario": "juan",
    "contrasena": "1234"
}
Crear tarea

Crea una nueva tarea asociada al usuario autenticado.

Solicitud:

{
    "accion": "crear_tarea",
    "usuario": "juan",
    "contrasena": "1234",
    "descripcion": "Estudiar programación"
}
Listar tareas

Obtiene todas las tareas del usuario.

Solicitud:

{
    "accion": "listar_tareas",
    "usuario": "juan",
    "contrasena": "1234"
}
Eliminar tarea

Elimina una tarea existente.

Solicitud:

{
    "accion": "eliminar_tarea",
    "usuario": "juan",
    "contrasena": "1234",
    "id": 1
}
Ejecución
Iniciar el servidor
python servidor.py

Opcionalmente:

python servidor.py --host 127.0.0.1 --port 5001 --workers 4

Parámetros:

Parámetro	Descripción
--host	Dirección IP del servidor
--port	Puerto de escucha
--workers	Cantidad de workers del ThreadPool
Iniciar el cliente
python cliente.py

Opcionalmente:

python cliente.py --host 127.0.0.1 --port 5001
Concurrencia

El servidor utiliza dos niveles de concurrencia:

Hilo por cliente

Cada cliente conectado es atendido mediante un hilo independiente.

Pool de Workers

Las solicitudes recibidas son procesadas por un:

ThreadPoolExecutor

Esto permite:

Atender múltiples clientes simultáneamente.
Reutilizar hilos.
Mejorar el rendimiento del servidor.
Manejo de Errores

El sistema contempla errores tales como:

Usuario existente.
Credenciales inválidas.
JSON inválido.
Pérdida de conexión.
IDs inexistentes.
Acciones no reconocidas.
Campos faltantes.

Todas las respuestas de error son enviadas en formato JSON.

Autores

Proyecto desarrollado como práctica de Sistemas Distribuidos utilizando Python, sockets TCP, concurrencia y persistencia mediante SQLite.

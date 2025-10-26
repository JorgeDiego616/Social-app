Documentación del proyecto "Didactic Social-app"

Social App es una aplicación backend desarrollada con FastAPI que se conecta a una base de datos MongoDB local.
El proyecto tuvo varios propósitos, el primero yo lo considero el aprender a desarrollar un proyecto conociendo todas sus partes técnicas (códigos y archivos sql) en las tres fases del desarrollo técnico (backend, frontend y database).
Y el segundo propósito entender como se trabaja en el mundo real con un proyecto real y utilizar github para guiarnos y dividir el trabajo de cada uno para así tener una buena metodología que garantice la efectividad del proyecto.
En el proyecto se manejarían usuarios y publicaciones (users y posts), sirviendo también un frontend estático.
Nuestro enfoque en el desarrollo fue crear una API moderna, modular y conectada a MongoDB, con verificación de conexión y endpoints de prueba.

El proyecto consisito en (como dice el título) hacer una app social teniendo uso libre sobre que herramientas usar para fabricar desde cero esta pseudo-aplicación.
Hubieron tres fases principales: Frontend, Backend Y Data-Base.

Backend: Fue la parte más importante del codigo, pues fue de las hechas en la fase temprana del proyecto. Consistió en 

2. Tecnologías utilizadas
Lenguaje backend: Python 3.10+.
Framework del backend: FastAPI.
Base de datos: MongoDB local
Cliente MongoDB: PyMongo
Middleware	CORS (para permitir peticiones desde el frontend)
Servidor de desarrollo: Uvicorn
Gestión de entorno: Virtualenv (venv)
Interfaz de base de datos	MongoDB Compass

Al ser un proyecto donde obviamente utilizariamos nuevas herramientas, teniamos que tener algunas instaladas desde antes para evitar retrasos en el desarrollo instalando algunas en medio del proyecto, como por ejemplo:
MongoDB Community Server
MongoDB Compass (este lo recomiendo para poder ver todo mas facilmente pues en este se ve todo más visual=
Git (Nosotros si lo utilizamos para subir cambios, pero, por lo mismo que se pueden subir cambios de otras formas, no es del todo obligatorio)
No hace falta mencionar que tenemos que tener Python 3.10 o alguna version más reciente (o si es el caso, no tan reciente pero más compatible)

3. Instalación y configuración
Podrá sonar innecesario este paso, pero debemos capturar todo en esta documentación.

nos vamos a github y en en el repo copiamos el enlace a este ya mencionado, y en la terminal de Git bash utlizamos el comanddo "git clone [LINK_DEL_REPOSITORIO]" para copiar el repositorio en su totalidad a nuestra pc.

Tendrá que verse así:
SOCIAL-APP/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── posts.py
│   │   │   └── users.py
│   │   ├── __init__.py
│   │   ├── .gitignore
│   │   └── requirements.txt          
│   ├── __pycache__/                  
│   ├── main.py                       # este es el main que debes ejecutar el comando de: uvicorn main:app
│   ├── requirements.txt              
│   └── venv/                        
│
├── database/
│   ├── database_design.md
│   ├── main.py                       
│   ├── schema.sql
│   └── seed_data.sql
│
├── frontend/
│   ├── Fase_de_planeación.md
│   ├── app.js
│   ├── index.html
│   └── .gitignore
│
├── venv/                           
├── .gitignore
├── README.md
└── Prueba/                          



4.Manipular el repo en pc local
Como el nombre de este paso lo dice y de igual manera se indicó en la estructura pasada: vamos a ejecutar comandos en el repo clonado para comfirmar su funcionabilidad.

4.1 Crear entorno virtual
python -m venv venv: Esto va a CREAR el entorno virtual (esencial este paso)

4.2 Activar el entorno virtual

En powershell como administrador o en una nueva terminal en visual studio code ejecutaremos los siguientes comandos:
Set-ExecutionPolicy Unrestricted -Scope Process (este elimina las restricciones para activar los scripts)
.\venv\Scripts\activate  (este activa el entorno virutal previamente creado)

4.3 Instalar dependencias
pip install, fastapi, uvicorn, pymongo, python-|dotenv

4.4 Iniciar el servicio de MongoDB 
Ejecutar en PowerShell (como administrador):

net start MongoDB


Si el servicio ya está activo, el sistema mostrará:

El servicio solicitado ya ha sido iniciado.

4.5 Abrir MongoDB Compass
Y conectar con:

mongodb://localhost:27017/


























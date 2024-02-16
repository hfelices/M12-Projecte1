# M12-Projecte1
Primer projecte de M12 amb Flask

### Crea l'entorn:

>python3 -m venv .venv

### Activa'l:

>source .venv/bin/activate

### Per tal que funcioni cal instalar les dependències:

>pip install -r requirements.txt

### Generar arxiu .env:

>cp .env.example .env

### !!! Editar variables del fitxer .env perquè funcioni, les que hi ha són només explicatives !!!

## Run

Executa:

>flask run --debug


## Per poder accedir a la pagina d'administració (/admin) cal registrar un nou usuari i modificar el seu rol (sqlite)

>UPDATE users SET role = "admin" where id = 1;
## -------------------------------

## Para tener la base de datos sqlite:

>cp app/database.example.db app/database.db


## -------------------------

## Si se pone el comando flask run --debug

>cp app/.env.example app/.env

## Y cambiar las variables pertinentes para usar sqlite, mysql o postgres

## ---------------------

## Para poder encender la aplicacion sin tener que poner el comando flask run --debug es necesario tener la extension de docker de visual, luego ejecutar:

>cp .env.docker.example .env.docker

## Seguidamente cambiar las variables a las tuyas y luego clic derecho en el archivo docker-compose.yml y hacer compose up

## NOTA: el sql ya inserta un usuario en esta parte que es admin


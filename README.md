# M12-Projecte1
Primer projecte de M12 amb Flask

### Crea l'entorn:

>python3 -m venv .venv

### Activa'l:

>source .venv/bin/activate

### Per tal que funcioni cal instalar les dependències:

>pip install -r requirements.txt

## Run

Executa:

>flask run --debug


## Per poder accedir a la pagina d'administració (/admin) cal registrar un nou usuari i modificar el seu rol

>UPDATE users SET role = "admin" where id = 1;
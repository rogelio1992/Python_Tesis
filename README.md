# Python_Tesis

## Dependencias

- Python 3.10.4
- PostgreSQL 15.1

## Configuraciones

- Copiar y renombrar el fichero `env.template` a `.env` y editar las variables correspondientes con los valores que correspondan

## Instalar requerimientos

    pip install -r requirements.txt


## Instalar requerimientos apra desarrolladores

    pip install -r dev_reqs.txt


## Correr migraciones

    ./python manage.py migrate


## Usar Black para formatear el código a estándares PEP de python

    ./black path/to/file.py

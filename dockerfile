# Utiliza la imagen oficial de Python como base
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt y los archivos de tu proyecto al contenedor
COPY requirements.txt .
COPY . .

# Instala las dependencias de tu proyecto
RUN pip install -r requirements.txt

# Expón el puerto en el que se ejecutará tu aplicación Django
EXPOSE 8001


# Comando para ejecutar la aplicación Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
# Set base image (host OS)
FROM python:3.8

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Se agrega todos los archivos y directorios a la carpeta /app
ADD . /app

# Install any dependencies
RUN pip install -r requirements.txt

# Specify the command to run on container start
CMD [ "python", "./app.py" ]
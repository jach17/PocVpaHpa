# Imagen base ligera con Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias necesarias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY main.py .

# Exponer el puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "main.py"]

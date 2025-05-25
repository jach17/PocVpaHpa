# Monitoreo y observabilidad

Se configuran con contendores de docker herramientas de monitoreo que funcionan en conjunto con un grupo de microservicios que realizan peticiones entre ellos y hacia un servicio externo, con esto podemos generar metricas, trazas y logs. 
Se utilizan microservicios en python usando el arquetipo de FastApi y de Net8

##Configuración de herramientas - Grafana, Loki, Tempo y Prometheus

###Ejecutar como contenedores de monitoreo:
Ubicado en la carpeta `containers`:
1. Enciende las herramiientas de monitorieo:

Esto va a levantar 5 contenedores de docker: 
- grafana
- grafana-alloy
- loki
- tempo
- prometheus

Y para su correcto funcionamiento utilizarán los archivos de configuración de la carpeta `monitoring`

Ejecuta el siguiente comando para que se levanten los contenedores:
``` bash
> docker compose up -d
```
Este comando, además de generar los contenedores, también crea una red y volumen compartidos para los distintos recursos y para el almacenamiento y procesamiento de log y de trazas.

---

##Enlaza los microservicios para monitoreo de trazas, logs y metricas

Se cuenta con la carpeta de `back_poc_loki` existen microservicios que funcionan en conjunto, para levantarlos se puede ejecutar el archivo de docker compose de cada microservicio, o el archivo docker compose que levanta a todos los microservicios juntos. 

###Levantar un solo microservicio:
Ubicado en la ruta de el microservicio a levantar:
``` bash
~ ./back_poc_loki/`{{service}}`
```


2. Asigna las variables de entorno

```
#Presindibles si no utilizas una base de datos
DB_HOST=localhost
DB_PORT=5431
DB_NAME=dbname
DB_SCHEMA=public
DB_USER=user
DB_PASSWORD=password
#Requeridas para el funcionamiento del monitoreo y de conexión entre microservicios
Empty_BASE_URL=https://rickandmortyapi.com/
APP_NAME=user-service
EXPORT=3002
OTLP_GRPC_ENDPOINT=http://tempo:4317
```

3. Ejecuta el comando que levanta el microservicio en un contenedor:
``` bash
> poetry run make rebuild
```

4. En la siguiente url `http://localhost:3000` encontrarás los dashboards de grafana, dentro puedes encontrar el tablero precargado que monitorea los microservicios definidos, para comprobarlo, puedes lanzar una petición de tipo GET a la siguiente dirección del microservicio

``` bash
> GET - http://localhost:3002/api/v1/empty/random_sleep
```

De esta se obtiene una respuesta como la que se muestra a continuación:

``` json
{
  "path": "/random_sleep"
}
```

Ahora puedes visualizar nuevas metricas en el tablero precargado de grafana: `FastApiObservabilty`
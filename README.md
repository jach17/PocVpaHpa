# PocVpaHpa
POC implementing vpa and hpa autoscaler
#POC implementig Grafana, Loki, Tempo y Prometheus

##Ejecutar como contenedores de monitoreo:


###Ubicado en la raíz:
1. Ejecuta el comando que configura las herramientas de monitorieo:

Esto va a levantar 5 contenedores, grafana, grafana-alloy, loki y tempo y prometheus, utilizará los archivos de configuración de la carpeta `monitoring`

``` bash
> docker compose up -d
```

###Ubicado en el microservicio a levantar:
Ruta - ./back_poc_loki/`{{service}}`


2. Asigna las variables de entorno

```
DB_HOST=localhost
DB_PORT=5431
DB_NAME=dbname
DB_SCHEMA=public
DB_USER=user
DB_PASSWORD=password
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

Ahora puedes visualizar nuevas metricas en el tablero precargado de grafana




5. Explicación del tablero:

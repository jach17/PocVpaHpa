# Backend de prueba para monitoreo
En este proyecto se encuentran un grupo de microservicios que integran configuraciones para generar trazas y logs y que puedan ser recuperados desde el stack de observabilidad construido.

## Build docker images
Para hacerlo funcionar, cada proyecto cuenta con un archivo `Makefile` con el comando build_image, por lo que, ubicandote en la carpeta raíz de cada micro se pueden generar las imagenes con el comando:
```bash
make build_image
```

## Deploy services
Para desplegar los servicios en el cluster de K8s se tiene la carpeta deploys, para ello, ubicado en la carpeta `"PocVpaHpa\back_poc_loki>"` aplica el siguiente comando:
```bash
kubectl apply -R -f .\deploys\ -n tt
```
## Genrando trazas
Los microservicios existentes estan construidos para poder generar información a partir del siguiente curl, por lo que solo debes lanzar esta peticion y podrás visualizar en el dashboard de grafana todo el detalle:

```bash

```
# 📦 Observabilidad con Tempo, Alloy y Grafana en Kubernetes

Este README documenta el despliegue de Grafana Tempo y Grafana Loki en un solo stak, dentro de un clúster de Kubernetes, junto con su configuración en Grafana dashboard para visualizar los logs y las trazas.

# 🚀 Paso a paso

## Requisitos

Para poder seguir estas instrucciones se requieren como mínimo los siguientes recursos
- Acceso a un cluster de K8S
- Helm instalado


# Instrucciones

### Helm Repos Update

Antes de iniciar con cualquier cosa, y ya con helm instalado, se agrega el repo de grafana para poder acceder a sus recursos.
``` bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```


## Crear Namespace

Primero, crea un namespace donde vivirán todos los recursos:

```bash
kubectl create ns tt
```

## - Instala Grafana

Para nuestra instalación de tempo y loki, vamos a completar nuestro stack con el dashboard propio de grafana, para ello utilizamos el archivo de `grafana.yaml` para levantar todos los recursos necesarios (deployment, volumen y service)
 
Para esto, dentro de la carpeta de los instaladores de helm aplicamos el siguiente comando:
`"PocVpaHpa\helm_installer>"`
```bash
~ kubectl apply -f .\grafana.yaml -n tt
```

## - Instalar Tempo con configuración personalizada

### 1. Instala Tempo con Helm 
Usando un archivo de configuración `custom.yaml` aplica el siguiente comando:

```bash
helm -n tt install tempo grafana/tempo-distributed -f custom.yaml
```

Verifica que los pods estén corriendo correctamente:

```bash
kubectl -n tt get pods
```

Deberías ver algo como:

```bash
NAME                                    READY   STATUS    RESTARTS   AGE
tempo-compactor-86cd974cf-8qrk2         1/1     Running   0          22h
tempo-distributor-bbf4889db-v8l8r       1/1     Running   0          22h
tempo-ingester-0                        1/1     Running   0          22h
tempo-ingester-1                        1/1     Running   0          22h
tempo-ingester-2                        1/1     Running   0          22h
tempo-memcached-0                       1/1     Running   0          8d
tempo-minio-6c4b66cb77-sgm8z            1/1     Running   0          26h
tempo-querier-777c8dcf54-fqz45          1/1     Running   0          22h
tempo-query-frontend-7f7f686d55-xsnq5   1/1     Running   0          22h
```

---

### 2. Instalar Alloy (Agente de trazas)

Instala Grafana Alloy, el agente que enviará trazas, usando tu archivo `alloy-values.yaml`, asegurate de que la linea en la configuración del client de tu exporter:

`endpoint = "http://tempo-distributor.tt.svc.cluster.local:4317"` 

apunta al service de tu distributor de tempo, algo similar a:  

`http://{{SERVICE_NAME}}.{{NAMESPCAE}}.svc.cluster.local:{{4317}}`


Y ahora sí procede con la instalación:
```bash
helm install -f alloy-values.yaml grafana-alloy grafana/alloy -n tt
```

---

### 3. Configurar Tempo como fuente de datos en Grafana

Una vez que todo esté desplegado, configura la conexión a Tempo en Grafana:

1. Navega a `Connections > Data Sources`.
2. Haz clic en **Add data source**.
3. Selecciona **Tempo**.
4. Establece la URL como:

    ```text
    http://tempo-query-frontend.tt.svc.cluster.local:3100
    ```

    *(Ajusta el namespace si usaste uno diferente)*

5. Haz clic en **Save & Test**.

    Deberías ver el mensaje: `Data source is working`.

---

### 4. Endpoint para envío de trazas desde tu app

Tu aplicación deberá enviar trazas al endpoint de tu service collector (`http://service-collector:4317`). En este caso, apuntaremos al receptor gRPC del agente Alloy que configuramos, mismo que envía estas trazas a Tempo, para ello utilizamos el servicio de alloy:
```bash
http://grafana-alloy:4317 #Tu aplicación deberá enviar trazas a este endpoint
```

## - Instalación de Loki
### 1. Instalación de loki con helm
Como continuación de nuestro stack de observabilidad vamos a integrar Grafana Loki, para eso utilizaremos el archivo `loki-values.yaml` con el siguiente comando:

```bash
helm install loki grafana/loki --version 6.29.0 --values loki-values.yaml -n tt
```

De la misma forma que utilizamos alloy como gestor de trazas, para la recuperación de logs utilizaremos una imagen de Promtail, para esa configuración utilizaremos el archivo `promtail.yaml` que contiene los manifiestos necesarios para levantar la imagen de promtail utilizando un configmap para configuraciones y un deployment para levantar la imagen, con el siguiente comando:

```bash
~ kubectl apply -f .\promtail.yaml -n tt
```
---
### 2. Configurar Loki como fuente de datos en Grafana
Una vez que todo esté desplegado, configura la conexión a Loki en Grafana:

1. Navega a `Connections > Data Sources`.
2. Haz clic en **Add data source**.
3. Selecciona **Loki**.
4. Establece la URL como:

    ```text
    http://loki-gateway.tt.svc.cluster.local
    ```

    *(Ajusta el namespace si usaste uno diferente)*

5. Haz clic en **Save & Test**.

    Deberías ver el mensaje: `Data source is working`.
---
NOTA: Dentro de tu aplicación no necesitas apuntar especificamente a algun endpoint, esto porque Promtail directamente recolecta los logs generados en la salida estándar, por lo tanto, si desde tu aplicación loggeas normalmente hacia la consola, promtail estará recolectando esos logs y enviandolos hacia Loki para ser procesados y visualizados desde grafana.  

## Dashboard de Grafana
### 1. Cargar el tablero precargado
Dentro de la carpeta de instaladores de helm, encontraras el archivo  `BasicDashboard.json` mismo que podrás importar como tablero listo para visualizar logs y trazas

## ✅ Resultado

Con esto tendrás:

- Tempo recibiendo y almacenando trazas.
- Alloy enviando trazas desde tus aplicaciones.
- Promtail recolectando logs de tus pods.
- Loki recibiendo y gestinoando logs.
- Grafana conectado a Tempo y Loki.

---

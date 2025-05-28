# 📦 Observabilidad con Tempo, Alloy y Grafana en Kubernetes

Este README documenta el despliegue de [Grafana Tempo](https://grafana.com/oss/tempo/) y [Grafana Alloy](https://grafana.com/docs/alloy/latest/) en un clúster de Kubernetes, junto con su configuración en Grafana para visualizar trazas.

## 🚀 Paso a paso

### 0. Helm Grafana Update
---
Antes que otra cosa, y ya con helm instalado, agrega grafana repo pa usarlo
``` bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```


### 1. Crear Namespace

Primero, crea un namespace donde vivirán todos los recursos:

```bash
kubectl create ns tt
```

---

### 2. Instalar Tempo con configuración personalizada

Instala Tempo con Helm usando un archivo de configuración `custom.yaml`:

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

### 3. Aplicar recursos de Grafana

Aplica la configuración de Grafana:

```bash
kubectl apply -f grafana.yaml -n tt
```

---

### 4. Instalar Alloy (Agente de trazas)

Instala Grafana Alloy, el agente que enviará trazas, usando tu archivo `values.yaml`, asegurate de que la linea 

`endpoint = "http://tempo-distributor.tt.svc.cluster.local:4317"` 

apunta al service de tu  distributor de tempo, algo similar a:  

`http://{{SERVICE_NAME}}.{{NAMESPCAE}}.svc.cluster.local:{{4317}}`


Y ahora sí procede con la instalación:
```bash
helm install -f values.yaml grafana-alloy grafana/alloy -n tt
```

---

### 5. Configurar Tempo como fuente de datos en Grafana

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

### 6. Endpoint para envío de trazas desde tu app

Tu aplicación deberá enviar trazas al siguiente endpoint:

```bash
http://service-collector:4317
```

En este caso, apunta al receptor gRPC del agente Alloy que reenvía las trazas a Tempo.
```bash
http://grafana-alloy:4317
```
---

## ✅ Resultado

Con esto tendrás:

- Tempo recibiendo y almacenando trazas.
- Alloy enviando trazas desde tus aplicaciones.
- Grafana conectado a Tempo, permitiéndote visualizar y analizar trazas distribuidas.

---

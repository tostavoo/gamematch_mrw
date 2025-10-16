\# 📊 Prometheus - Etapa 8: Monitoreo



\## ✅ Estado: IMPLEMENTADO



Sistema de monitoreo en tiempo real con Prometheus.



\## Ubicación de Prometheus

```

C:\\prometheus\\

```



\## Arquitectura

```

GameMatch Backend (FastAPI)

&nbsp;   ↓

Expone /metrics cada 15s

&nbsp;   ↓

Prometheus :9090

&nbsp;   ↓

Recolecta y almacena métricas

&nbsp;   ↓

Dashboard web con gráficas

```



\## Métricas recolectadas



\### 1. Total de requests HTTP

\- \*\*Métrica:\*\* `http\_requests\_total`

\- \*\*Labels:\*\* method, endpoint, status

\- \*\*Descripción:\*\* Contador total de requests por endpoint



\### 2. Duración de requests

\- \*\*Métrica:\*\* `http\_request\_duration\_seconds`

\- \*\*Labels:\*\* method, endpoint

\- \*\*Descripción:\*\* Histograma de tiempos de respuesta



\### 3. Métricas del sistema

\- Garbage collector de Python

\- Uso de memoria

\- Información de la plataforma



\## Consultas útiles



\### Requests por segundo

```promql

rate(http\_requests\_total\[5m])

```



\### Duración promedio

```promql

rate(http\_request\_duration\_seconds\_sum\[5m]) / rate(http\_request\_duration\_seconds\_count\[5m])

```



\### Requests por endpoint

```promql

http\_requests\_total{endpoint="/health"}

```



\### Distribución por status code

```promql

sum by (status) (http\_requests\_total)

```



\## Iniciar servicios



\### 1. Backend (con métricas)

```bash

cd E:\\Usuario\\Documents\\gamematch\_mrw

uvicorn app.api.main:app --host 0.0.0.0 --port 8000

```



\### 2. Prometheus

```bash

cd C:\\prometheus

prometheus.exe

```



\## Acceso



\- \*\*Dashboard:\*\* http://localhost:9090

\- \*\*Targets:\*\* http://localhost:9090/targets

\- \*\*Métricas raw:\*\* http://localhost:8000/metrics



\## Configuración



\*\*Archivo:\*\* `C:\\prometheus\\prometheus.yml`



\*\*Intervalo de recolección:\*\* 15 segundos



\*\*Targets monitoreados:\*\*

\- `gamematch-backend` → localhost:8000/metrics

\- `prometheus` → localhost:9090/metrics



\## Capturas de ejemplo



✅ 2 targets activos (UP)

✅ Métricas de requests HTTP disponibles

✅ Gráficas en tiempo real funcionando

✅ Dashboard accesible en puerto 9090



\## Uso en producción



En un entorno real, Prometheus puede:

\- Enviar alertas por Slack/Email cuando hay errores

\- Integrarse con Grafana para dashboards más visuales

\- Guardar métricas históricas por meses

\- Monitorear múltiples servicios simultáneamente


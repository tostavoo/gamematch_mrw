\# 🌐 Nginx - Etapa 7: Proxy Reverso



\## ✅ Estado: IMPLEMENTADO



Nginx configurado como proxy reverso en \*\*puerto 8080\*\*.



\## Ubicación de Nginx

```

C:\\nginx-1.29.2\\

```



\## Arquitectura

```

Cliente (Navegador)

&nbsp;   ↓

Nginx :8080

&nbsp;   ├─→ Frontend (Streamlit) :8501

&nbsp;   └─→ Backend (FastAPI) :8000

```



\## Rutas configuradas



| Ruta | Destino | Descripción |

|------|---------|-------------|

| `/` | Frontend :8501 | Interfaz Streamlit |

| `/api/\*` | Backend :8000 | API REST |

| `/docs` | Backend :8000/docs | Swagger UI |

| `/health` | Backend :8000/health | Health Check |



\## Iniciar servicios



\### 1. Backend (FastAPI)

```bash

cd E:\\Usuario\\Documents\\gamematch\_mrw

uvicorn app.api.main:app --host 0.0.0.0 --port 8000

```



\### 2. Frontend (Streamlit)

```bash

cd E:\\Usuario\\Documents\\gamematch\_mrw

streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0

```



\### 3. Nginx

```bash

cd C:\\nginx-1.29.2

start nginx

```



\## Verificar funcionamiento



Abre tu navegador:



\- \*\*Frontend:\*\* http://localhost:8080

\- \*\*API Health:\*\* http://localhost:8080/api/health

\- \*\*API Docs:\*\* http://localhost:8080/docs



\## Comandos útiles

```bash

\# Ver procesos de Nginx

tasklist | findstr nginx



\# Detener Nginx

cd C:\\nginx-1.29.2

nginx.exe -s stop



\# Recargar configuración

nginx.exe -s reload



\# Ver logs de errores

type logs\\error.log



\# Ver logs de acceso

type logs\\access.log

```



\## Configuración



\*\*Archivo:\*\* `C:\\nginx-1.29.2\\conf\\nginx.conf`



\*\*Características:\*\*

\- Puerto 8080 (sin conflicto con XAMPP)

\- Soporte WebSockets (para Streamlit)

\- Timeouts extendidos (24 horas)

\- CORS habilitado

\- Logs de acceso y errores



\## Notas técnicas



\- XAMPP Apache continúa funcionando en puerto 80

\- Ambos servicios pueden correr simultáneamente

\- Nginx actúa como punto de entrada único

\- Mejora la seguridad al ocultar puertos internos



\## Capturas de pantalla



✅ Frontend funcionando en http://localhost:8080

✅ Health Check respondiendo correctamente

✅ 2 procesos nginx.exe corriendo


---

## 🧠 Microservicio: Sentiment Analysis

GameMatch incluye un **microservicio independiente** para análisis de sentimientos.

### Características:
- **Puerto:** 8001
- **Tecnología:** FastAPI + TextBlob (NLP)
- **Función:** Analiza el tono emocional de feedback de usuarios
- **Comunicación:** API REST (JSON)

### Iniciar microservicio:
```bash
cd sentiment-service
uvicorn app.main:app --port 8001
```

### Documentación completa:
Ver `sentiment-service/README.md`

### Arquitectura:
```
Backend :8000 ←→ Sentiment Service :8001
```

Este diseño demuestra una **arquitectura de microservicios** moderna donde cada servicio tiene una responsabilidad específica y puede escalarse independientemente.
```

**Guarda el archivo.**

---

## 🎤 **GUÍA PARA EXPLICAR EN LA PRESENTACIÓN**

### **Qué decir:**

> "Además del backend principal, implementé un **microservicio independiente** para análisis de sentimientos usando **procesamiento de lenguaje natural (NLP)**.
>
> Este microservicio corre en el **puerto 8001** de forma completamente independiente, y el backend principal en el puerto 8000 se comunica con él mediante peticiones HTTP asíncronas.
>
> Por ejemplo, cuando un usuario deja feedback como _'Este juego es increíble'_, el backend envía ese texto al microservicio, que lo analiza con **TextBlob** y retorna si el sentimiento es positivo, negativo o neutral, junto con un score de confianza.
>
> Esta arquitectura tiene múltiples ventajas:
>
> 1. **Escalabilidad:** Puedo replicar el microservicio sin tocar el backend
> 2. **Mantenibilidad:** Código separado y más fácil de mantener
> 3. **Resiliencia:** Si el microservicio falla, el backend sigue funcionando
> 4. **Tecnología heterogénea:** Podría estar escrito en otro lenguaje
>
> Aquí pueden ver ambos servicios comunicándose en tiempo real..."

_(Y muestras Swagger ejecutando el endpoint)_

---

## 📊 **DIAGRAMA PARA LA PRESENTACIÓN**

Puedes dibujar esto en una diapositiva:

```
┌─────────────────────────────────────────────┐
│         ARQUITECTURA DE MICROSERVICIOS      │
└─────────────────────────────────────────────┘

    Usuario (Navegador)
         │
         ↓
    ┌─────────────────┐
    │   Nginx :8080   │  ← Proxy Reverso
    └────────┬────────┘
             │
    ┌────────┴────────┐
    ↓                 ↓
┌──────────┐    ┌──────────────┐
│ Frontend │    │   Backend    │
│Streamlit │    │   FastAPI    │
│  :8501   │    │   :8000      │
└──────────┘    └──────┬───────┘
                       │
              ┌────────┴─────────────┐
              ↓                      ↓
     ┌─────────────────┐    ┌──────────────┐
     │  MySQL :3306    │    │  Sentiment   │
     │  (Datos)        │    │  Service     │
     └─────────────────┘    │  :8001       │
                            │  (NLP)       │
                            └──────────────┘
                                   │
                            ┌──────┴──────┐
                            ↓             ↓
                       Prometheus    Logs
                         :9090
```

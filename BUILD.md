# 🔧 Gestión de Dependencias y Build

## Herramienta: pip + requirements.txt

Este proyecto utiliza **pip** como gestor de dependencias de Python (equivalente a Maven/Gradle en Java).

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Dependencias principales

- **fastapi**: Framework web moderno para APIs REST
- **uvicorn**: Servidor ASGI de alto rendimiento
- **sqlalchemy**: ORM para manejo de base de datos
- **pydantic**: Validación de datos y schemas
- **python-jose**: Manejo de tokens JWT
- **passlib + bcrypt**: Hashing seguro de contraseñas
- **streamlit**: Framework para interfaces web interactivas
- **requests**: Cliente HTTP para integraciones
- **pymysql**: Driver MySQL para Python

### Agregar nueva dependencia

1. Instalar el paquete:

```bash
pip install nombre-paquete
```

2. Actualizar requirements.txt:

```bash
pip freeze > requirements.txt
```

### Build con Docker

El proyecto incluye `Dockerfile` que automatiza el proceso de build:

1. Instalación de dependencias del sistema (gcc, libmysqlclient)
2. Instalación de dependencias Python desde requirements.txt
3. Empaquetado de la aplicación

```bash
docker-compose build
docker-compose up -d
```

### Verificar dependencias instaladas

```bash
pip list
```

### Entorno virtual (recomendado)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

**Justificación técnica:** pip es el gestor de paquetes estándar de Python, equivalente funcional a Maven (Java) o npm (JavaScript). El archivo `requirements.txt` actúa como el manifest de dependencias, similar a `pom.xml` o `package.json`.

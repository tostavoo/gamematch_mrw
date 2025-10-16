# 🧪 Testing - GameMatch+

## Herramienta: Cypress

Implementamos **Cypress** para pruebas end-to-end (E2E) de la interfaz web.

### ¿Por qué Cypress?

- Pruebas automatizadas del flujo completo de usuario
- Simula interacciones reales en el navegador
- Detecta errores antes de producción
- Valida que login, catálogo y recomendaciones funcionen correctamente

### Pruebas implementadas

**Archivo:** `cypress/e2e/login.cy.js`

1. ✅ Visualización correcta de la página de login
2. ✅ Login exitoso con credenciales válidas
3. ✅ Navegación al catálogo después del login
4. ✅ Interacción con juegos (dar like)

### Ejecutar tests

```bash
# Instalar Cypress
npm install

# Abrir interfaz interactiva
npm run cy:open

# Ejecutar tests en modo headless
npm run cy:run
```

### Configuración

- **Base URL:** http://localhost:8501
- **Timeout:** 10 segundos
- **Screenshots:** Activados en caso de fallo
- **Video:** Desactivado (para performance)

### Integración con CI/CD

Los tests de Cypress se ejecutan automáticamente en el pipeline de GitLab CI/CD antes del despliegue.

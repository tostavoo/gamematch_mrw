// cypress/support/e2e.js
// Este archivo se carga automáticamente antes de cada test

// Importar comandos personalizados (si los hay)
import './commands'

// Configuración global
Cypress.on('uncaught:exception', (err, runnable) => {
  // Prevenir que Cypress falle por errores de la app
  // (útil para Streamlit que a veces lanza warnings)
  return false
})
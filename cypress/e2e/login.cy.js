// cypress/e2e/login.cy.js
// Pruebas E2E del flujo de login en GameMatch+ (Streamlit)

describe('GameMatch+ - Login Flow', () => {
  
  beforeEach(() => {
    cy.visit('http://localhost:8501')
    cy.get('[data-testid="stAppViewContainer"]', { timeout: 10000 }).should('be.visible')
  })

  it('Debe cargar la aplicación correctamente', () => {
    cy.contains('GameMatch+').should('be.visible')
    cy.get('[data-testid="stSidebar"]').should('be.visible')
    cy.contains('No autenticado').should('be.visible')
  })

  it('Debe navegar a la página de Registro/Login', () => {
    cy.contains('Registro / Login').click()
    cy.contains('Registrarme').should('be.visible')
    cy.contains('Iniciar sesión').should('be.visible')
  })

  it('Debe permitir iniciar sesión con credenciales válidas', () => {
    // Navegar a Registro/Login
    cy.contains('Registro / Login').click()
    cy.wait(500)
    
    // Click en el tab de "Iniciar sesión"
    cy.contains('Iniciar sesión').click()
    cy.wait(1000) // Esperar a que el tab cambie completamente
    
    // ⚠️ CLAVE: Solo seleccionar inputs VISIBLES
    cy.get('[data-baseweb="input"]').filter(':visible').then($inputs => {
      // Primer input visible: Email
      cy.wrap($inputs[0]).clear().type('gus@example.com')
      // Segundo input visible: Password  
      cy.wrap($inputs[1]).clear().type('123456')
    })
    
    // Click en el botón "Entrar"
    cy.contains('button', 'Entrar').click()
    
    // Verificar que se inició sesión exitosamente
    cy.contains('Sesión OK', { timeout: 15000 }).should('be.visible')
  })

  it('Debe cerrar sesión correctamente', () => {
    // Login primero
    cy.contains('Registro / Login').click()
    cy.wait(500)
    cy.contains('Iniciar sesión').click()
    cy.wait(1000)
    
    cy.get('[data-baseweb="input"]').filter(':visible').then($inputs => {
      cy.wrap($inputs[0]).clear().type('gus@example.com')
      cy.wrap($inputs[1]).clear().type('123456')
    })
    
    cy.contains('button', 'Entrar').click()
    cy.contains('Sesión OK', { timeout: 15000 }).should('be.visible')
    
    // Cerrar sesión
    cy.get('[data-testid="stSidebar"]').within(() => {
      cy.contains('button', 'Cerrar sesión').click()
    })
    
    cy.wait(1000)
    cy.contains('No autenticado').should('be.visible')
  })
})
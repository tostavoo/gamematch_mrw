// cypress/support/commands.js
// Comandos personalizados de Cypress

// Ejemplo: Comando para login rápido
Cypress.Commands.add('login', (email = 'gus@example.com', password = '123456') => {
  cy.contains('Registro / Login').click()
  cy.contains('Iniciar sesión').click()
  cy.wait(500)
  
  cy.get('[data-baseweb="input"]').then($inputs => {
    cy.wrap($inputs[0]).clear().type(email)
    cy.wrap($inputs[1]).clear().type(password)
  })
  
  cy.contains('button', 'Entrar').click()
  cy.contains('Sesión OK', { timeout: 15000 }).should('be.visible')
})
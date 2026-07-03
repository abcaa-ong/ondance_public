// ***********************************************
// Custom commands for OnDance E2E tests
// ***********************************************

Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login')
  cy.get('input[type="email"], input[aria-label*="mail"]').first().type(email)
  cy.get('input[type="password"]').first().type(password)
  cy.get('button[type="submit"], button').contains(/entrar|login/i).click()
  cy.url().should('not.include', '/login')
})

Cypress.Commands.add('loginAsStudent', () => {
  cy.login(Cypress.env('STUDENT_EMAIL') || 'aluno@teste.com', Cypress.env('STUDENT_PASSWORD') || 'Teste@123')
})

Cypress.Commands.add('loginAsTeacher', () => {
  cy.login(Cypress.env('TEACHER_EMAIL') || 'professor@teste.com', Cypress.env('TEACHER_PASSWORD') || 'Teste@123')
})

Cypress.Commands.add('loginAsAdmin', () => {
  cy.login(Cypress.env('ADMIN_EMAIL') || 'admin@teste.com', Cypress.env('ADMIN_PASSWORD') || 'Teste@123')
})

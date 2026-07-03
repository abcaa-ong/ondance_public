describe('Admin Flow', () => {
  beforeEach(() => {
    cy.loginAsAdmin()
  })

  it('can access admin dashboard', () => {
    cy.url().should('not.include', '/login')
    cy.get('body').should('be.visible')
  })

  it('can navigate to overview', () => {
    cy.visit('/admin')
    cy.get('body').should('contain.text', 'Visão Geral')
  })

  it('can navigate to courses management', () => {
    cy.visit('/admin/cursos')
    cy.get('body').should('be.visible')
  })

  it('can navigate to users management', () => {
    cy.visit('/admin/usuarios')
    cy.get('body').should('be.visible')
  })

  it('can navigate to campaigns', () => {
    cy.visit('/admin/campanhas')
    cy.get('body').should('contain.text', 'Campanhas')
  })

  it('can navigate to analytics', () => {
    cy.visit('/admin/analytics')
    cy.get('body').should('contain.text', 'Analytics')
  })

  it('can navigate to categories', () => {
    cy.visit('/admin/categorias')
    cy.get('body').should('contain.text', 'Categorias')
  })

  it('can access settings page', () => {
    cy.visit('/admin/config')
    cy.get('body').should('contain.text', 'Configurações')
  })
})

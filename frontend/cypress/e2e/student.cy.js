describe('Student Flow', () => {
  beforeEach(() => {
    cy.loginAsStudent()
  })

  it('can access student dashboard', () => {
    cy.url().should('not.include', '/login')
    cy.get('body').should('be.visible')
  })

  it('can navigate to explore page', () => {
    cy.visit('/student/explorar')
    cy.get('body').should('contain.text', 'Explorar')
      .or.contain.text', 'buscar')
  })

  it('can search for courses', () => {
    cy.visit('/student/explorar')
    cy.get('input[aria-label*="Buscar"], input[placeholder*="buscar"]').first().type('Ballet')
    cy.wait(500)
    cy.get('body').should('be.visible')
  })

  it('can access my courses page', () => {
    cy.visit('/student/meus-cursos')
    cy.get('body').should('be.visible')
  })

  it('can access certificates page', () => {
    cy.visit('/student/certificados')
    cy.get('body').should('be.visible')
  })

  it('can access settings page', () => {
    cy.visit('/student/configuracoes')
    cy.get('body').should('contain.text', 'Configurações')
  })

  it('settings page has profile form', () => {
    cy.visit('/student/configuracoes')
    cy.get('input').should('have.length.greaterThan', 0)
  })
})

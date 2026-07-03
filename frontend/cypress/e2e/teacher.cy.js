describe('Teacher Flow', () => {
  beforeEach(() => {
    cy.loginAsTeacher()
  })

  it('can access teacher dashboard', () => {
    cy.url().should('not.include', '/login')
    cy.get('body').should('be.visible')
  })

  it('can navigate to my courses', () => {
    cy.visit('/teacher/cursos')
    cy.get('body').should('be.visible')
  })

  it('can navigate to manage lessons', () => {
    cy.visit('/teacher/aulas')
    cy.get('body').should('contain.text', 'Gerenciar Aulas')
  })

  it('can navigate to students page', () => {
    cy.visit('/teacher/alunos')
    cy.get('body').should('be.visible')
  })

  it('can navigate to reviews page', () => {
    cy.visit('/teacher/avaliacoes')
    cy.get('body').should('be.visible')
  })

  it('can navigate to earnings page', () => {
    cy.visit('/teacher/ganhos')
    cy.get('body').should('contain.text', 'Ganhos')
  })

  it('can access settings page', () => {
    cy.visit('/teacher/config')
    cy.get('body').should('contain.text', 'Configurações')
  })
})

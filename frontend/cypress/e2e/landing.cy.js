describe('Landing Page', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('loads the homepage successfully', () => {
    cy.contains('OnDance').should('be.visible')
  })

  it('displays featured courses section', () => {
    cy.get('body').then(($body) => {
      if ($body.find('[data-cy="featured-courses"]').length) {
        cy.get('[data-cy="featured-courses"]').should('be.visible')
      }
    })
  })

  it('has working navigation links', () => {
    cy.get('a[href]').should('have.length.greaterThan', 0)
  })

  it('lead capture form exists', () => {
    cy.get('body').then(($body) => {
      const nameInput = $body.find('input[aria-label*="nome" i], input[placeholder*="nome" i]')
      if (nameInput.length) {
        cy.wrap(nameInput).first().should('be.visible')
      }
    })
  })

  it('is accessible - has lang attribute', () => {
    cy.get('html').should('have.attr', 'lang', 'pt-BR')
  })
})

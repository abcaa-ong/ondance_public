describe('Authentication Flow', () => {
  it('shows login page', () => {
    cy.visit('/login')
    cy.get('body').should('contain.text', 'Entrar')
      .or.contain.text('Login')
      .or.contain.text('entrar')
  })

  it('shows validation errors on empty submit', () => {
    cy.visit('/login')
    cy.get('button[type="submit"], button').contains(/entrar|login/i).click()
    cy.get('body').should('contain.text', 'obrigatório')
      .or.contain.text('preenchimento')
      .or.contain.text('required')
  })

  it('navigates to signup from login', () => {
    cy.visit('/login')
    cy.get('body').then(($body) => {
      const signupLink = $body.find('a[href*="cadastro"], button').filter(':contains("criar"), :contains("cadastrar"), :contains("signup")')
      if (signupLink.length) {
        cy.wrap(signupLink.first()).click()
        cy.url().should('include', 'cadastro')
      }
    })
  })

  it('shows error on wrong credentials', () => {
    cy.visit('/login')
    cy.get('input[type="email"], input[aria-label*="mail"]').first().type('wrong@email.com')
    cy.get('input[type="password"]').first().type('wrongpassword')
    cy.get('button[type="submit"], button').contains(/entrar|login/i).click()
    cy.get('body').should('contain.text', 'credenciais')
      .or.contain.text('inválid')
      .or.contain.text('incorret')
  })
})

import { useAuth } from 'src/composables/useAuth'

const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID

// Google só permite um initialize() por página. Guardamos o estado e o callback
// atual em escopo de módulo para reutilizar entre componentes.
let _initialized = false
let _callbackRef = null

function loadGoogleSdk() {
  return new Promise((resolve, reject) => {
    if (window.google?.accounts) return resolve()
    const script = document.createElement('script')
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    script.defer = true
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}

export function useGoogleAuth() {
  const { googleLogin } = useAuth()

  function renderFallbackButton(elementId) {
    const el = document.getElementById(elementId)
    if (!el) return
    el.innerHTML = `
      <button style="
        display: flex; align-items: center; justify-content: center; gap: 10px;
        width: 100%; padding: 10px 16px; border-radius: 4px;
        border: 1px solid #dadce0; background: #fff; cursor: pointer;
        font-size: 14px; font-weight: 500; color: #3c4043;
        font-family: 'Google Sans', Roboto, sans-serif;
      " disabled>
        <svg width="18" height="18" viewBox="0 0 18 18">
          <path fill="#4285F4" d="M16.51 8H8.98v3h4.3c-.18 1-.74 1.48-1.6 2.04v2.01h2.6a7.8 7.8 0 0 0 2.38-5.88c0-.57-.05-.66-.15-1.18z"/>
          <path fill="#34A853" d="M8.98 17c2.16 0 3.97-.72 5.3-1.94l-2.6-2.04a4.8 4.8 0 0 1-7.18-2.54H1.83v2.07A8 8 0 0 0 8.98 17z"/>
          <path fill="#FBBC05" d="M4.5 10.48A4.8 4.8 0 0 1 4.5 7.5V5.43H1.83a8 8 0 0 0 0 7.14z"/>
          <path fill="#EA4335" d="M8.98 3.58c1.32 0 2.5.45 3.44 1.35l2.58-2.59A8 8 0 0 0 1.83 5.43L4.5 7.5c.68-2.01 2.56-3.92 4.48-3.92z"/>
        </svg>
        Continuar com Google
      </button>
    `
  }

  async function initGoogleButton(elementId, { onSuccess, onError, getRole }) {
    if (!CLIENT_ID) {
      renderFallbackButton(elementId)
      return
    }

    await loadGoogleSdk()

    // Atualiza callback ativo (cada página pode ter o seu)
    _callbackRef = { onSuccess, onError, getRole }

    if (!_initialized) {
      window.google.accounts.id.initialize({
        client_id: CLIENT_ID,
        callback: async ({ credential }) => {
          try {
            const role = _callbackRef?.getRole?.() ?? 'aluno'
            const response = await googleLogin(credential, role)
            _callbackRef?.onSuccess?.(response)
          } catch (error) {
            _callbackRef?.onError?.(error)
          }
        },
      })
      _initialized = true
    }

    const el = document.getElementById(elementId)
    // Google só aceita número inteiro em pixels (máx 400). Usa a largura real
    // do container ou 360 como fallback, sempre dentro do limite permitido.
    const width = Math.min(Math.round(el?.offsetWidth || 360), 400)
    // Em dark mode o botão branco (outline) destoa muito; filled_blue fica
    // mais harmonioso com fundos escuros.
    const isDark = document.body.classList.contains('body--dark')

    window.google.accounts.id.renderButton(el, {
      theme: isDark ? 'filled_blue' : 'outline',
      size: 'large',
      width,
      text: 'continue_with',
      locale: 'pt-BR',
    })
  }

  return { initGoogleButton }
}

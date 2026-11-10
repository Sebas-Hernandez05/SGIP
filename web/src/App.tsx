import { useRef, useState } from 'react'
import type { FormEvent } from 'react'
import './App.css'

type Fields = { nombre: string; correo: string; contrasena: string; confirmacion: string }
type Errors = Partial<Record<keyof Fields, string>>
const empty: Fields = { nombre: '', correo: '', contrasena: '', confirmacion: '' }

function registrationUrl() {
  const base = import.meta.env.VITE_API_URL?.trim() || (import.meta.env.DEV ? 'http://localhost:8000' : '')
  if (!base) throw new Error('configuration')
  const url = new URL(base)
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)
  if (url.username || url.password || url.search || url.hash ||
    (url.protocol !== 'https:' && !(import.meta.env.DEV && local && url.protocol === 'http:'))) throw new Error('configuration')
  return `${base.replace(/\/+$/, '')}/api/v1/ciudadanos`
}

function App() {
  const [fields, setFields] = useState<Fields>(empty)
  const [errors, setErrors] = useState<Errors>({})
  const [pending, setPending] = useState(false)
  const [message, setMessage] = useState('')
  const [success, setSuccess] = useState(false)
  const [passwordVisible, setPasswordVisible] = useState(false)
  const locked = useRef(false)
  const summary = useRef<HTMLDivElement>(null)
  const successHeading = useRef<HTMLHeadingElement>(null)

  function showError(text: string, nextErrors: Errors = {}) {
    setErrors(nextErrors)
    setMessage(text)
    requestAnimationFrame(() => summary.current?.focus())
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (locked.current) return
    const nextErrors: Errors = {}
    const nombre = fields.nombre.trim()
    const correo = fields.correo.trim().toLowerCase()
    if (nombre.length < 2 || nombre.length > 120) nextErrors.nombre = 'Escribe un nombre de 2 a 120 caracteres.'
    if (correo.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) nextErrors.correo = 'Escribe un correo válido, como persona@ejemplo.com.'
    if (fields.contrasena.length < 12 || fields.contrasena.length > 128) nextErrors.contrasena = 'Usa una contraseña de 12 a 128 caracteres.'
    if (!fields.confirmacion || fields.confirmacion !== fields.contrasena) nextErrors.confirmacion = 'Las contraseñas deben coincidir.'
    if (Object.keys(nextErrors).length) {
      showError('Revisa los campos indicados para continuar.', nextErrors)
      return
    }
    locked.current = true
    setPending(true)
    setMessage('')
    setErrors({})
    const controller = new AbortController()
    const timeout = window.setTimeout(() => controller.abort(), 15000)
    try {
      const response = await fetch(registrationUrl(), {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, correo, contrasena: fields.contrasena }), signal: controller.signal,
      })
      if (response.status === 201) {
        setFields(empty)
        setPasswordVisible(false)
        setSuccess(true)
        requestAnimationFrame(() => successHeading.current?.focus())
      } else if (response.status === 409) {
        showError('No pudimos crear tu cuenta. Revisa el correo.', { correo: 'El correo ya está registrado. Usa otro correo.' })
      } else if (response.status === 422) {
        showError('Los datos no fueron aceptados. Revisa el nombre, el correo y la contraseña e inténtalo de nuevo.')
      } else {
        showError('El servicio no está disponible. Intenta más tarde.')
      }
    } catch (error) {
      showError(error instanceof Error && error.message === 'configuration'
        ? 'El registro no está disponible en este momento. Intenta más tarde.'
        : controller.signal.aborted
          ? 'La solicitud tardó demasiado. No pudimos confirmar el registro. Comprueba si tu cuenta fue creada antes de reintentar.'
          : 'No pudimos confirmar el registro. Revisa tu conexión e intenta más tarde.')
    } finally {
      window.clearTimeout(timeout)
      locked.current = false
      setPending(false)
    }
  }

  function update(field: keyof Fields, value: string) {
    setFields((previous) => ({ ...previous, [field]: value }))
    setErrors((previous) => ({ ...previous, [field]: undefined }))
  }

  const labels: Record<keyof Fields, string> = { nombre: 'Nombre completo', correo: 'Correo electrónico', contrasena: 'Contraseña', confirmacion: 'Confirma tu contraseña' }
  return (
    <>
      <a className="skip-link" href="#contenido">Ir al contenido</a>
      <main id="contenido" className="registration-layout">
        <section className="introduction" aria-labelledby="welcome-title">
          <a className="brand" href="/" aria-label="SGIP, inicio"><span className="logo" aria-hidden="true">↗</span> SGIP</a>
          <div className="hero-content">
            <p className="eyebrow">Pereira, en nuestras manos</p>
            <h1 id="welcome-title">Una mejor ciudad empieza contigo.</h1>
            <p>Reporta, sigue y construye el cambio en los espacios que compartimos.</p>
            <div className="city-art" aria-hidden="true">
              <svg viewBox="0 0 500 180" preserveAspectRatio="xMidYMid slice">
                <rect width="500" height="180" fill="#dce8d2" />
                <circle cx="430" cy="35" r="25" fill="#f4edb2" />
                <path d="M0 100L70 45 145 100 250 35 340 100 450 60 500 100V180H0Z" fill="#b3c8a8" />
                <path d="M0 140L500 120V180H0Z" fill="#899e8c" />
                <path d="M180 180L330 120H360L240 180" fill="#f6f5df" />
                <rect x="50" y="65" width="70" height="75" fill="#edf0df" />
                <path d="M60 78H76V98H60ZM87 78H103V98H87Z" fill="#8aab9d" />
                <path d="M310 145V38Q310 23 330 23H362" fill="none" stroke="#254b3e" strokeWidth="7" />
                <path d="M350 25H375" stroke="#254b3e" strokeWidth="10" />
                <path d="M352 34L325 100H400L373 34" fill="#fdf1ac" opacity=".8" />
                <circle cx="430" cy="108" r="27" fill="#6f9770" />
                <path d="M430 110V157" stroke="#456747" strokeWidth="7" />
              </svg>
            </div>
          </div>
          <small>Sistema de Gestión de Incidencias en Pereira</small>
        </section>
        <section className="form-panel" aria-labelledby={success ? 'success-title' : 'form-title'}>
          {success ? <div className="success-panel" role="status">
            <p className="eyebrow">Registro completado</p>
            <h2 id="success-title" ref={successHeading} tabIndex={-1}>Tu cuenta fue creada</h2>
            <p>Ya estás registrado como ciudadano. Por seguridad, no se ha iniciado una sesión automáticamente.</p>
            <button type="button" className="secondary-button" onClick={() => { setSuccess(false); setMessage(''); requestAnimationFrame(() => document.getElementById('nombre')?.focus()) }}>Registrar otra cuenta</button>
          </div> : <>
            <p className="eyebrow">Participación ciudadana</p>
            <h2 id="form-title">Crea tu cuenta</h2>
            <p className="form-intro">Regístrate para reportar y seguir tus casos.</p>
            <p className="required-note">Los campos con * son obligatorios.</p>
            {message && <div ref={summary} className="error-summary" role="alert" tabIndex={-1}><p>{message}</p>{Object.values(errors).some(Boolean) && <ul>{(Object.keys(errors) as (keyof Fields)[]).filter((field) => errors[field]).map((field) => <li key={field}><a href={`#${field}`}>{errors[field]}</a></li>)}</ul>}</div>}
            <form onSubmit={submit} noValidate aria-busy={pending}>
              <fieldset disabled={pending}>
                {(Object.keys(labels) as (keyof Fields)[]).map((field) => <div className="field" key={field}>
                  <label htmlFor={field}>{labels[field]} <span aria-hidden="true">*</span></label>
                  <div className={field === 'contrasena' ? 'password-row' : undefined}>
                  <input id={field} name={field} type={field === 'nombre' ? 'text' : field === 'correo' ? 'email' : field === 'contrasena' && passwordVisible ? 'text' : 'password'} autoComplete={field === 'nombre' ? 'name' : field === 'correo' ? 'email' : 'new-password'} autoCapitalize={field === 'correo' ? 'none' : undefined} spellCheck={false} required maxLength={field === 'nombre' ? 120 : field === 'correo' ? 254 : 128} value={fields[field]} onChange={(e) => update(field, e.target.value)} aria-invalid={Boolean(errors[field])} aria-describedby={[field === 'contrasena' ? 'password-help' : '', errors[field] ? `${field}-error` : ''].filter(Boolean).join(' ') || undefined} />
                  {field === 'contrasena' && <button type="button" className="password-toggle" aria-controls="contrasena" aria-label={passwordVisible ? 'Ocultar contraseña' : 'Mostrar contraseña'} aria-pressed={passwordVisible} onClick={() => setPasswordVisible((visible) => !visible)}>{passwordVisible ? 'Ocultar' : 'Mostrar'}</button>}
                  </div>
                  {field === 'contrasena' && <p className="field-help" id="password-help">Entre 12 y 128 caracteres. Los espacios también cuentan.</p>}
                  {errors[field] && <p className="field-error" id={`${field}-error`}>{errors[field]}</p>}
                </div>)}
                <button className="submit-button" type="submit">{pending ? 'Creando tu cuenta…' : 'Crear mi cuenta'}</button>
              </fieldset>
              <p className="request-status" role="status">{pending ? 'Estamos enviando tu registro. Espera un momento.' : ''}</p>
            </form>
          </>}
          <p className="demo-note">Entorno académico. Utiliza únicamente datos ficticios.</p>
        </section>
      </main>
    </>
  )
}

export default App

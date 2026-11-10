export type Registration = { nombre: string; correo: string; contrasena: string };

export async function registerCitizen(payload: Registration): Promise<void> {
  const configured = process.env.EXPO_PUBLIC_API_URL;

  if (!configured) throw new Error('El servicio de registro no está configurado. Intenta más tarde.');
  let base: URL;
  try { base = new URL(configured); } catch { throw new Error('El servicio de registro no está configurado correctamente.'); }
  const lanHost = process.env.EXPO_PUBLIC_DEV_API_HOST;
  const local =
    ['localhost', '127.0.0.1', '10.0.2.2', '[::1]'].includes(base.hostname) ||
    base.hostname === lanHost;
  if (base.username || base.password || base.search || base.hash || (base.protocol !== 'https:' && !(__DEV__ && local && base.protocol === 'http:'))) {
    throw new Error('El servicio requiere una conexión HTTPS segura.');
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(`${base.toString().replace(/\/$/, '')}/api/v1/ciudadanos`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload), signal: controller.signal,
    });
    if (response.status === 201) return;
    if (response.status === 409) throw new Error('El correo ya está registrado. Usa otro correo.');
    if (response.status === 422) throw new Error('Revisa el nombre, correo y contraseña e intenta de nuevo.');
    throw new Error('El servicio no está disponible. Intenta más tarde.');
  } catch (error) {
    if (controller.signal.aborted) throw new Error('La solicitud tardó demasiado. El registro podría haberse completado; si reintentas y el correo ya existe, tu cuenta puede estar creada.');
    if (error instanceof TypeError) throw new Error('No pudimos conectar con el servicio. Comprueba tu conexión e intenta de nuevo.');
    throw error;
  } finally { clearTimeout(timeout); }
}

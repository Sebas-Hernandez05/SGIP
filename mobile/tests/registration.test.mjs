import assert from 'node:assert/strict';
import { test } from 'node:test';
import { registerCitizen } from '../src/services/registration.ts';

globalThis.__DEV__ = true;
const payload = { nombre: 'Ciudadano Ficticio', correo: 'prueba@example.test', contrasena: 'clave-ficticia-2026' };

test('registro consume solo API central y no envía confirmación ni rol', async () => {
  process.env.EXPO_PUBLIC_API_URL = 'https://api.example.test';
  globalThis.fetch = async (url, options) => {
    assert.equal(url, 'https://api.example.test/api/v1/ciudadanos');
    assert.equal(options.method, 'POST');
    assert.deepEqual(JSON.parse(options.body), payload);
    return { status: 201 };
  };
  await registerCitizen(payload);
});

test('duplicado, validación y servicio fallido tienen mensajes controlados', async () => {
  for (const [status, expected] of [[409, /correo ya está registrado/], [422, /Revisa el nombre/], [503, /no está disponible/]]) {
    globalThis.fetch = async () => ({ status });
    await assert.rejects(registerCitizen(payload), expected);
  }
});

test('fallo de red permite reintentar sin exponer respuesta del servidor', async () => {
  globalThis.fetch = async () => { throw new TypeError('Failed to fetch'); };
  await assert.rejects(registerCitizen(payload), /Comprueba tu conexión/);
  globalThis.fetch = async () => ({ status: 201 });
  await registerCitizen(payload);
});

test('rechaza configuración insegura antes de enviar credenciales', async () => {
  let calls = 0;
  globalThis.fetch = async () => { calls++; return { status: 201 }; };
  for (const base of ['http://api.example.test', 'https://user:secret@api.example.test', 'https://api.example.test?token=x']) {
    process.env.EXPO_PUBLIC_API_URL = base;
    await assert.rejects(registerCitizen(payload), /HTTPS segura/);
  }
  assert.equal(calls, 0);
  delete process.env.EXPO_PUBLIC_API_URL;
  await assert.rejects(registerCitizen(payload), /no está configurado/);
});

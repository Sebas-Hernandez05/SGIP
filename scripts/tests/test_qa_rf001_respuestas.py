"""Comprueba servidor HTTP y timeout del servicio móvil, no las pantallas."""
from contextlib import closing, contextmanager
import http.client
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('qa_rf001', ROOT / 'scripts/qa_rf001_respuestas.py')
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)


@contextmanager
def running_server(**options):
    server = qa.create_server(port=0, **options)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server.server_port
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def request(port, method='POST', path=qa.REGISTRATION_PATH, origin=None):
    with closing(http.client.HTTPConnection('127.0.0.1', port, timeout=3)) as conn:
        conn.request(method, path, body=b'{"contrasena":"ficticia-qa-no-eco"}' if method == 'POST' else None,
                     headers={'Content-Type': 'application/json',
                              **({'Origin': origin} if origin else {})})
        response = conn.getresponse()
        return response.status, dict(response.getheaders()), response.read()


class QaResponsesTests(unittest.TestCase):
    def test_cli_port_58010(self):
        process = subprocess.Popen(
            [sys.executable, str(ROOT / 'scripts/qa_rf001_respuestas.py'), '--status', '422'],
            cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        )
        try:
            startup = process.stdout.readline()
            self.assertIn('127.0.0.1:58010', startup)
            self.assertEqual(request(58010)[0], 422)
        finally:
            process.terminate()
            process.wait(timeout=5)
            process.stdout.close()

    def test_422_and_503_are_json_without_echoing_payload(self):
        for status in (422, 503):
            with self.subTest(status=status), running_server(status=status) as port:
                code, headers, body = request(port, origin='http://localhost:5173')
                self.assertEqual(code, status)
                self.assertIn('detail', json.loads(body))
                self.assertNotIn(b'ficticia-qa-no-eco', body)
                self.assertEqual(headers['Cache-Control'], 'no-store')
                self.assertEqual(headers['Access-Control-Allow-Origin'], 'http://localhost:5173')

    def test_cors_preflight_and_unknown_route(self):
        with running_server() as port:
            self.assertEqual(request(port, 'OPTIONS', origin='http://localhost:5173')[0], 204)
            code, headers, _ = request(port, 'OPTIONS', origin='https://ajeno.example')
            self.assertEqual(code, 403)
            self.assertNotIn('Access-Control-Allow-Origin', headers)
            self.assertEqual(request(port, path='/otra-ruta')[0], 404)

    def test_mobile_service_real_fetch_422_503_and_15_second_timeout(self):
        module = (ROOT / 'mobile/src/services/registration.ts').as_uri()
        for status, delay in ((422, 0), (503, 0), (503, 20)):
            with self.subTest(status=status, delay=delay), running_server(status=status, delay=delay) as port:
                script = f"""
import assert from 'node:assert/strict';
import {{ registerCitizen }} from {json.dumps(module)};
globalThis.__DEV__ = true;
process.env.EXPO_PUBLIC_API_URL = 'http://127.0.0.1:{port}';
const started = performance.now();
await assert.rejects(registerCitizen({{nombre:'QA Ficticia',correo:'qa@example.com',contrasena:'ficticia-segura-001'}}),
    {('/tardó demasiado.*podría haberse completado/' if delay else '/Revisa el nombre/' if status == 422 else '/no está disponible/')});
const elapsed = (performance.now() - started) / 1000;
if ({delay} > 0) assert.ok(elapsed >= 14 && elapsed < 19, 'Debe cancelar antes de la respuesta de20s');
console.log(`Servicio móvil HTTP real status={status} delay={delay}: OK; ${{elapsed.toFixed(3)}}s`);
"""
                result = subprocess.run(['node', '--input-type=module', '-e', script],
                                        cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=27,
                                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                self.assertEqual(result.returncode, 0, result.stderr)
                print(result.stdout.strip(), flush=True)

    def test_invalid_delay_is_rejected(self):
        for delay in (-1, float('nan'), float('inf')):
            with self.subTest(delay=delay), self.assertRaises(ValueError):
                qa.create_server(delay=delay)


if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))

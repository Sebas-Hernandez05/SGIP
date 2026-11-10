"""API ficticia RF-001 para probar errores UI; no crea cuentas ni usa BD.

Desde la raíz: backend/.venv/Scripts/python.exe scripts/qa_rf001_respuestas.py
Solo datos ficticios. Ctrl+C detiene el servidor; no se registra el cuerpo.
"""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import time
from urllib.parse import urlsplit

REGISTRATION_PATH = '/api/v1/ciudadanos'


def create_server(host='127.0.0.1', port=58010, status=503, delay=0,
                  origins=('http://localhost:5173',)):
    if status not in (422, 503) or not math.isfinite(delay) or delay < 0:
        raise ValueError('Solo status422/503 y demora finita no negativa.')
    allowed = frozenset(origins)

    class Handler(BaseHTTPRequestHandler):
        def respond(self, code, payload=None):
            body = json.dumps(payload, ensure_ascii=False).encode('utf-8') if payload else b''
            self.send_response(code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Vary', 'Origin')
            origin = self.headers.get('Origin')
            if origin in allowed:
                self.send_header('Access-Control-Allow-Origin', origin)
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            if body:
                self.wfile.write(body)

        def do_OPTIONS(self):
            if urlsplit(self.path).path != REGISTRATION_PATH:
                self.respond(404, {'detail': 'Ruta de QA no disponible.'})
            elif self.headers.get('Origin') not in allowed:
                self.respond(403, {'detail': 'Origen de QA no permitido.'})
            else:
                self.respond(204)

        def do_POST(self):
            try:
                # Descartar el cuerpo: nunca imprimirlo, persistirlo ni reenviarlo.
                length = int(self.headers.get('Content-Length', '0'))
                if length < 0 or length > 65536:
                    self.respond(413, {'detail': 'Solicitud de QA demasiado grande.'})
                    return
                self.rfile.read(length)
                if urlsplit(self.path).path != REGISTRATION_PATH:
                    self.respond(404, {'detail': 'Ruta de QA no disponible.'})
                    return
                print(f'POST recibido; simulacion={status}; demora={delay}s; sin persistencia', flush=True)
                time.sleep(delay)
                detail = ([{'loc': ['body', 'correo'], 'type': 'value_error',
                            'msg': 'Revisa el valor de este campo.'}] if status == 422 else
                          'El servicio no está disponible. Intenta más tarde.')
                self.respond(status, {'detail': detail})
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                # Esperable cuando el cliente cancela por timeout antes de la respuesta.
                pass

        def log_message(self, *_):
            pass

    server = ThreadingHTTPServer((host, port), Handler)
    server.daemon_threads = True
    return server


def nonnegative_seconds(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError('La demora debe ser finita y no negativa.')
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=58010)
    parser.add_argument('--status', type=int, choices=(422, 503), default=503)
    parser.add_argument('--delay', type=nonnegative_seconds, default=0)
    parser.add_argument('--origin', action='append', help='Origen web permitido; repetible.')
    args = parser.parse_args()
    with create_server(args.host, args.port, args.status, args.delay,
                       args.origin or ['http://localhost:5173']) as server:
        print(f'QA ficticia en {server.server_address[0]}:{server.server_port}; '
              f'status={args.status}; demora={args.delay}s; sin BD', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()

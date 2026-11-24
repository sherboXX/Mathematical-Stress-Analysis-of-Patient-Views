"""Serve the phone VR app over HTTPS on your local Wi-Fi (phone motion sensors only work on https pages).

    python serve.py              -> prints  https://<this PC's IP>:8443   (open it on the phone)
    python serve.py --port 9443

The first run makes a self-signed certificate (cert.pem / key.pem, valid for this PC's IP) with openssl
(Git for Windows ships one).  The phone warns once about the certificate: tap "Advanced" -> "Proceed".
Windows asks whether Python may use the network: allow it on PRIVATE networks.  The PC and the phone must be on the
same Wi-Fi.  Nothing is uploaded anywhere: the phone loads the files straight from this PC.
"""
import argparse
import functools
import http.server
import os
import shutil
import socket
import ssl
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))          # no packet is sent; this only picks the Wi-Fi interface
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()


def find_openssl():
    for c in (r'C:\Program Files\Git\mingw64\bin\openssl.exe', r'C:\Program Files\Git\usr\bin\openssl.exe',
              shutil.which('openssl')):
        if c and os.path.exists(c):
            return c
    raise SystemExit('openssl not found (install Git for Windows, or put cert.pem / key.pem next to serve.py)')


def ensure_cert(ip):
    cert, key = os.path.join(HERE, 'cert.pem'), os.path.join(HERE, 'key.pem')
    stamp = os.path.join(HERE, 'cert_ip.txt')
    if os.path.exists(cert) and os.path.exists(key) and os.path.exists(stamp) and open(stamp).read().strip() == ip:
        return cert, key
    subprocess.run([find_openssl(), 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', key, '-out', cert,
                    '-days', '825', '-subj', '/CN=patient-room-vr',
                    '-addext', f'subjectAltName=IP:{ip},IP:127.0.0.1,DNS:localhost'], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    open(stamp, 'w').write(ip)
    return cert, key


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = dict(http.server.SimpleHTTPRequestHandler.extensions_map,
                          **{'.json': 'application/json', '.jpg': 'image/jpeg', '.js': 'text/javascript'})

    def end_headers(self):
        if self.path.endswith(('.html', '.json', '/')):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=8443)
    a = ap.parse_args()
    ip = lan_ip()
    cert, key = ensure_cert(ip)
    srv = http.server.ThreadingHTTPServer(('0.0.0.0', a.port), functools.partial(Handler, directory=HERE))
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    print(f'\n  Patient Room VR is running.\n\n  On your phone (same Wi-Fi) open:   https://{ip}:{a.port}\n'
          f'  On this PC:                         https://localhost:{a.port}\n\n  Ctrl+C to stop.\n', flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

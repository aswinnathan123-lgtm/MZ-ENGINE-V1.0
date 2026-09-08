"""
1-Click Local Server Launcher for Puter.js
Avoids the 'file:/// Unsupported Protocol' error by serving files over http://localhost:8000
"""
import http.server
import socketserver
import webbrowser

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

print("=" * 60)
print(f"⚡ MZ-15 ENGINE Local Web Server Running!")
print(f"[*] Access URL: http://localhost:{PORT}/puter_runner.html")
print("=" * 60)

# Automatically open default browser
webbrowser.open(f"http://localhost:{PORT}/puter_runner.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server stopped.")

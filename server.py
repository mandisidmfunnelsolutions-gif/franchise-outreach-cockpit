#!/usr/bin/env python3
"""
Franchise Outreach Cockpit - Universal Server & Vercel Entrypoint.
Compatible with Vercel Serverless Functions and local execution.
"""

import sys
import os
from http.server import BaseHTTPRequestHandler
import socketserver
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "index.html"
CSV_FILE = BASE_DIR / "data" / "sa_food_beverage_franchise_owners_linkedin.csv"
JSON_FILE = BASE_DIR / "data" / "sa_food_beverage_franchise_owners_linkedin.json"

class handler(BaseHTTPRequestHandler):
    """Vercel native Serverless Function handler and local HTTP handler."""

    def do_GET(self):
        clean_path = self.path.split("?")[0].rstrip("/")

        if clean_path in ["/leads.json", "/data/leads.json", "/api/leads"]:
            content = JSON_FILE.read_bytes() if JSON_FILE.exists() else b"[]"
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
            return

        elif clean_path in ["/leads.csv", "/data/leads.csv", "/export.csv"]:
            content = CSV_FILE.read_bytes() if CSV_FILE.exists() else b""
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
            return

        else:
            # Default route: serve the Cockpit dashboard
            if not HTML_FILE.exists():
                self.send_error(404, "index.html not found")
                return
            content = HTML_FILE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

    def log_message(self, fmt, *args):
        # Quiet standard output
        pass

# Top-level exports for Vercel Python runtime
app = handler
application = handler
FranchiseDashboardHandler = handler

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3002
    print("=" * 70)
    print("   SA FRANCHISE AI ADOPTION STUDY — OUTREACH COCKPIT")
    print("=" * 70)
    print(f"[*] Local URL:    http://localhost:{port}")
    print(f"[*] Leads JSON:   http://localhost:{port}/leads.json")
    print(f"[*] Leads CSV:    http://localhost:{port}/leads.csv")
    print("=" * 70)

    class ReusableServer(socketserver.TCPServer):
        allow_reuse_address = True

    with ReusableServer(("", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Dev server stopped.")
            httpd.server_close()

if __name__ == "__main__":
    main()

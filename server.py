#!/usr/bin/env python3
"""
Franchise Outreach Cockpit - Local Dev Server.
Serves the standalone interactive dashboard, JSON API, and CSV data.
Usage: python3 server.py [port]
"""

import sys
import http.server
import socketserver
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "index.html"
CSV_FILE = BASE_DIR / "data" / "sa_food_beverage_franchise_owners_linkedin.csv"
JSON_FILE = BASE_DIR / "data" / "sa_food_beverage_franchise_owners_linkedin.json"

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3002

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class FranchiseDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        clean_path = self.path.split("?")[0].rstrip("/")

        if clean_path in ["", "/", "/index.html", "/dashboard"]:
            if not HTML_FILE.exists():
                self.send_error(404, f"Dashboard file not found: {HTML_FILE}")
                return
            content = HTML_FILE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(content)
            return

        elif clean_path in ["/leads.json", "/data/leads.json", "/api/leads"]:
            if not JSON_FILE.exists():
                self.send_error(404, f"JSON file not found: {JSON_FILE}")
                return
            content = JSON_FILE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        elif clean_path in ["/leads.csv", "/data/leads.csv", "/export.csv"]:
            if not CSV_FILE.exists():
                self.send_error(404, f"CSV file not found: {CSV_FILE}")
                return
            content = CSV_FILE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        else:
            content = HTML_FILE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

    def log_message(self, fmt, *args):
        print(f"[*] Dashboard HTTP: {args[0]} -> {args[1]}")

def main():
    print("=" * 70)
    print("   SA FRANCHISE AI ADOPTION STUDY — OUTREACH COCKPIT")
    print("=" * 70)
    print(f"[*] Local URL:    http://localhost:{PORT}")
    print(f"[*] Leads JSON:   http://localhost:{PORT}/leads.json")
    print(f"[*] Leads CSV:    http://localhost:{PORT}/leads.csv")
    print("=" * 70)

    with ReusableTCPServer(("", PORT), FranchiseDashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Dev server stopped.")
            httpd.server_close()

# Vercel Serverless Function entrypoint exports
handler = FranchiseDashboardHandler
app = handler
application = handler

if __name__ == "__main__":
    main()


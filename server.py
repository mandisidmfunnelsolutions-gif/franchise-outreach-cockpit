#!/usr/bin/env python3
"""
Franchise Outreach Cockpit - Universal Server & Vercel Entrypoint.
Compatible with Vercel Serverless Functions and local execution.
Provides:
- Standalone HTML Cockpit UI
- Leads JSON and CSV endpoints
- Live Supabase Survey Responses API (/api/survey-responses)
- Academic Word (.docx) Report Generation (/api/export-docx) with explicit slider percentages
"""

import sys
import os
import json
import re
import io
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler
import socketserver
from pathlib import Path
from datetime import datetime

# Import local docx generator
try:
    from docx_generator import build_single_survey_docx, build_consolidated_survey_docx
except ImportError:
    # If running from a different working directory, try relative import
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from docx_generator import build_single_survey_docx, build_consolidated_survey_docx

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "index.html"
CSV_FILE = BASE_DIR / "data" / "sa_food_beverage_franchise_owners_linkedin.csv"
JSON_FILE = BASE_DIR / "data" / "sa_food_beverage_franchise_owners_linkedin.json"
CACHE_RESPONSES_FILE = BASE_DIR / "data" / "survey_responses_cache.json"
LEAD_STATES_FILE = BASE_DIR / "data" / "lead_states.json"

# Load .env file manually if present
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

# Supabase Credentials with robust fallbacks
SUPABASE_URL = os.environ.get("NEXT_PUBLIC_SUPABASE_URL", "https://fyvqgxdpwlkmoisskyjx.supabase.co").rstrip("/")
SUPABASE_KEY = os.environ.get(
    "SUPABASE_SERVICE_ROLE_KEY",
    os.environ.get(
        "NEXT_PUBLIC_SUPABASE_ANON_KEY",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ5dnFneGRwd2xrbW9pc3NreWp4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE5ODI3NTksImV4cCI6MjEwNzU1ODc1OX0.BYw98rE7YMa3vhh5XbZBpmo3oUc3QCwUJS2SRYLCdH8"
    )
)

def fetch_survey_responses_from_supabase():
    """
    Fetches all survey responses directly from Supabase REST API.
    Caches locally to disk to ensure high resilience and offline capability.
    """
    url = f"{SUPABASE_URL}/rest/v1/survey_responses?select=*&order=created_at.desc"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                raw = response.read().decode("utf-8")
                data = json.loads(raw)
                # Ensure directory exists and cache
                CACHE_RESPONSES_FILE.parent.mkdir(parents=True, exist_ok=True)
                CACHE_RESPONSES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
                return data
    except Exception as e:
        print(f"[!] Warning: Failed to fetch live Supabase survey responses: {e}")

    # Fallback to local cache if available
    if CACHE_RESPONSES_FILE.exists():
        try:
            return json.loads(CACHE_RESPONSES_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    return []


class handler(BaseHTTPRequestHandler):
    """Vercel native Serverless Function handler and local HTTP handler."""

    def do_OPTIONS(self):
        """Handle CORS pre-flight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        clean_path = parsed_url.path.rstrip("/")

        # Save/Sync Lead States (connection requests, statuses, notes, stars)
        if clean_path in ["/api/lead-states", "/lead-states"]:
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode("utf-8")
                states_data = json.loads(body)
                LEAD_STATES_FILE.parent.mkdir(parents=True, exist_ok=True)
                LEAD_STATES_FILE.write_text(json.dumps(states_data, indent=2, ensure_ascii=False), encoding="utf-8")
                
                resp = json.dumps({"success": True, "count": len(states_data)}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(resp)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(resp)
            except Exception as e:
                err_resp = json.dumps({"error": str(e)}).encode("utf-8")
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(err_resp)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(err_resp)
            return
        else:
            self.send_error(404, "Endpoint not found")

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        clean_path = parsed_url.path.rstrip("/")
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # 1. Leads JSON API
        if clean_path in ["/leads.json", "/data/leads.json", "/api/leads"]:
            content = JSON_FILE.read_bytes() if JSON_FILE.exists() else b"[]"
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
            return

        # 2. Leads CSV Export
        elif clean_path in ["/leads.csv", "/data/leads.csv", "/export.csv"]:
            content = CSV_FILE.read_bytes() if CSV_FILE.exists() else b""
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
            return

        # 3. Lead States JSON API (Connection requests sent, statuses, notes)
        elif clean_path in ["/api/lead-states", "/data/lead_states.json", "/lead-states.json"]:
            content = LEAD_STATES_FILE.read_bytes() if LEAD_STATES_FILE.exists() else b"{}"
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(content)
            return

        # 4. Live Survey Responses JSON API
        elif clean_path in ["/api/survey-responses", "/api/responses", "/data/survey-responses.json"]:
            responses = fetch_survey_responses_from_supabase()
            content = json.dumps(responses, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(content)
            return

        # 4. Formatted Word Document (.docx) Export API
        elif clean_path in ["/api/export-docx", "/export-docx", "/download-docx"]:
            responses = fetch_survey_responses_from_supabase()
            target_id = query_params.get("id", ["all"])[0]

            today_str = datetime.now().strftime("%Y-%m-%d")

            if target_id == "all" or not target_id:
                # Consolidated document for all respondents
                bio = build_consolidated_survey_docx(responses)
                filename = f"UP_Honours_All_Survey_Responses_{today_str}.docx"
            else:
                # Single document for specific respondent ID
                matching = [r for r in responses if str(r.get("id")) == target_id]
                if not matching:
                    self.send_error(404, f"Survey response with ID '{target_id}' not found.")
                    return
                record = matching[0]
                bio = build_single_survey_docx(record)
                
                # Derive sanitized filename
                name = record.get("response_data", {}).get("participantName", "Participant")
                clean_name = re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")
                filename = f"UP_Survey_{clean_name}_{today_str}.docx"

            docx_bytes = bio.getvalue()
            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(len(docx_bytes)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(docx_bytes)
            return

        # 5. Default route: serve the Cockpit dashboard
        else:
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
    print(f"[*] Local URL:          http://localhost:{port}")
    print(f"[*] Leads JSON:         http://localhost:{port}/leads.json")
    print(f"[*] Leads CSV:          http://localhost:{port}/leads.csv")
    print(f"[*] Survey Responses:   http://localhost:{port}/api/survey-responses")
    print(f"[*] All DOCX Export:    http://localhost:{port}/api/export-docx?id=all")
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

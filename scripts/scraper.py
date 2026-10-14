#!/usr/bin/env python3
"""
LinkedIn Profile Scraper & Ingestion Engine:
South African Fast Food and Food & Beverage Franchise Owners & Operators.

Features:
- Asynchronous Apify execution with real-time status polling (no HTTP timeouts).
- Support for passing an existing dataset ID (--dataset <id>) or running fresh live queries.
- Precision entity extraction (Name, Brand/Franchise, Role, Location, Canonical LinkedIn URL).
- Quality filtering against non-owners and unrelated domains.
- Exports to Outreach/Lead_Lists/ in CSV and JSON formats.
- Safe idempotent ingestion into Supabase bd_leads table.
"""

import os
import sys
import json
import re
import csv
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
OUTPUT_DIR = BASE_DIR / "data"

def get_env_var(name: str) -> str:
    """Retrieve environment variable from os or .env."""
    val = os.environ.get(name)
    if val:
        return val.strip('"\'')
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"\'')
    return ""

def clean_linkedin_url(url: str) -> str:
    """Normalize LinkedIn profile URL to canonical https://www.linkedin.com/in/<slug>."""
    if not url:
        return ""
    url = url.split("?")[0].split("#")[0].rstrip("/")
    match = re.search(r"linkedin\.com/in/([^/]+)", url)
    if match:
        slug = match.group(1).lower()
        return f"https://www.linkedin.com/in/{slug}"
    return url

def clean_name(raw_name: str) -> str:
    """Clean person's name by stripping corporate suffixes, certs, or emojis."""
    raw_name = re.sub(r"[^\w\s\.\-']", "", raw_name)
    raw_name = re.sub(r"\b(Pty|Ltd|PhD|MBA|CA|SA|MD|CEO|CFO|COO|PMP)\b", "", raw_name, flags=re.IGNORECASE)
    parts = raw_name.split()
    if len(parts) > 4:
        raw_name = " ".join(parts[:3])
    return raw_name.strip()

def extract_brand_and_role(title: str, snippet: str) -> tuple[str, str, str]:
    """Extract primary franchise brand, role, and location from SERP metadata."""
    combined = f"{title} {snippet}"
    combined_lower = combined.lower()

    # Brand mapping
    brand_map = {
        "Steers": ["steers"],
        "Debonairs Pizza": ["debonairs"],
        "Wimpy": ["wimpy"],
        "Mugg & Bean": ["mugg & bean", "mugg and bean", "mugg&bean"],
        "Fishaways": ["fishaways"],
        "Milky Lane": ["milky lane"],
        "Famous Brands": ["famous brands", "famousbrands"],
        "Spur Steak Ranches": ["spur steak", "spur group", "spur restaurant", "spur"],
        "Panarottis": ["panarottis"],
        "RocoMamas": ["rocomamas", "roco mamas"],
        "Hussar Grill": ["hussar grill"],
        "KFC": ["kfc"],
        "Chicken Licken": ["chicken licken"],
        "Hungry Lion": ["hungry lion"],
        "Nando's": ["nando's", "nandos"],
        "Pedros": ["pedros", "pedro's"],
        "McDonald's": ["mcdonald's", "mcdonalds"],
        "Burger King": ["burger king"],
        "Roman's Pizza": ["roman's pizza", "romans pizza"],
        "Ocean Basket": ["ocean basket"],
        "Kauai": ["kauai"],
        "Vida e Caffè": ["vida e caffe", "vida e caffè", "vida caffe"],
        "Xpresso Cafe": ["xpresso cafe"],
        "Simply Asia": ["simply asia"],
        "Food Lover's Market": ["food lover's market", "food lovers market"],
        "Nkukhu Box": ["nkukhu box"],
        "Maxis Restaurant": ["maxis restaurant", "maxis"]
    }

    matched_brands = []
    for brand_name, terms in brand_map.items():
        if any(term in combined_lower for term in terms):
            matched_brands.append(brand_name)

    company_name = ", ".join(dict.fromkeys(matched_brands)) if matched_brands else "Fast Food / F&B Franchise"

    # Role extraction
    role = "Franchise Owner"
    if "multi-unit" in combined_lower or "multiple store" in combined_lower or "multi store" in combined_lower:
        role = "Multi-unit Franchisee"
    elif "managing director" in combined_lower or " md " in combined_lower:
        role = "Managing Director & Franchisee"
    elif "director" in combined_lower:
        role = "Franchise Director"
    elif "partner" in combined_lower:
        role = "Franchise Partner"
    elif "founder" in combined_lower or "co-founder" in combined_lower:
        role = "Franchise Founder / Owner"
    elif "owner" in combined_lower:
        role = "Franchise Owner"
    elif "franchisee" in combined_lower:
        role = "Franchisee"

    # Location extraction
    locations = [
        "Johannesburg", "Cape Town", "Durban", "Pretoria", "Centurion", "Sandton",
        "Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape", "Free State",
        "Mpumalanga", "Limpopo", "North West", "Northern Cape", "Bloemfontein",
        "Gqeberha", "Port Elizabeth", "East London", "Polokwane", "Nelspruit", "Mbombela",
        "Ballito", "Umhlanga", "Makhado", "Paarl", "Stellenbosch"
    ]
    matched_locs = []
    for loc in locations:
        if loc.lower() in combined_lower:
            matched_locs.append(loc)

    location_str = ", ".join(dict.fromkeys(matched_locs)) if matched_locs else "South Africa"

    return company_name, role, location_str

def fetch_dataset_items(apify_token: str, dataset_id: str) -> list[dict]:
    """Fetch items from an Apify dataset."""
    print(f"[*] Fetching items from Apify dataset '{dataset_id}'...")
    url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={apify_token}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def trigger_apify_async(apify_token: str, queries: list[str], max_pages: int = 2) -> str:
    """Start Apify Google Search Scraper run asynchronously and poll until completion."""
    print(f"[*] Launching Apify Google Search Scraper with {len(queries)} queries...")
    start_url = f"https://api.apify.com/v2/acts/apify~google-search-scraper/runs?token={apify_token}"
    payload = {
        "queries": "\n".join(queries),
        "maxPagesPerQuery": max_pages,
        "countryCode": "za"
    }

    req = urllib.request.Request(
        start_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8")
    )

    with urllib.request.urlopen(req) as resp:
        run_data = json.loads(resp.read().decode("utf-8"))
        run_id = run_data["data"]["id"]
        dataset_id = run_data["data"]["defaultDatasetId"]
        print(f"[+] Started Apify Run: {run_id}")

    # Poll status
    poll_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={apify_token}"
    while True:
        time.sleep(5)
        with urllib.request.urlopen(urllib.request.Request(poll_url)) as p_resp:
            status_data = json.loads(p_resp.read().decode("utf-8"))
            status = status_data["data"]["status"]
            print(f"[*] Apify Run {run_id} status: {status}")
            if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
                if status != "SUCCEEDED":
                    raise RuntimeError(f"Apify run finished with status: {status}")
                return dataset_id

def process_and_filter_results(raw_batches: list[dict]) -> list[dict]:
    """Parse, clean, deduplicate, and qualify franchise owner profiles."""
    unique_profiles = {}
    EXCLUDE_KEYWORDS = [
        "crew member", "cashier", "junior", "intern", "driver", "recruitment", "headhunter",
        "software engineer", "full stack", "developer", "astronomy", "soccer", "head coach",
        "national treasury", "financial inclusion", "risk management", "it support", "student"
    ]

    for batch in raw_batches:
        for item in batch.get("organicResults", []):
            url = item.get("url", "")
            if "linkedin.com/in/" not in url:
                continue

            c_url = clean_linkedin_url(url)
            if not c_url or c_url in unique_profiles:
                continue

            title = item.get("title", "")
            snippet = item.get("description", "")
            combined = f"{title} {snippet}".lower()

            # Skip disqualified roles
            if any(term in combined for term in EXCLUDE_KEYWORDS):
                continue

            # Must demonstrate franchise / ownership / director role
            has_role = any(r in combined for r in [
                "franchis", "owner", "director", "founder", "co-founder", "partner", "operator", "managing director", "md"
            ])

            # Must belong to food / beverage / restaurant / fast food domain
            has_food = any(f in combined for f in [
                "steers", "debonairs", "wimpy", "spur", "kfc", "chicken", "burger", "pizza",
                "famous brands", "panarottis", "rocomamas", "mugg", "fishaways", "ocean basket",
                "kauai", "qsr", "restaurant", "food", "beverage", "cafe", "caffe", "dining", "catering"
            ])

            if not (has_role and has_food):
                continue

            # Parse Name
            raw_title = title.replace(" - LinkedIn", "").replace(" | LinkedIn", "").strip()
            parts = re.split(r"\s+[-–—|]\s+", raw_title)
            name = clean_name(parts[0].strip()) if parts else clean_name(raw_title)

            # Skip non-personal names (e.g., "Debonairs Pizza", "Steers North Beach")
            if any(name.lower().startswith(b) for b in ["debonairs", "steers", "wimpy", "spur", "famous brands"]):
                continue

            company_name, role, location = extract_brand_and_role(title, snippet)

            unique_profiles[c_url] = {
                "full_name": name,
                "company_name": company_name,
                "job_title": role,
                "location": location,
                "linkedin_url": c_url,
                "snippet": snippet.strip().replace("\n", " ")
            }

    return list(unique_profiles.values())

def ingest_to_supabase(profiles: list[dict]):
    """Insert or update leads in Supabase bd_leads table."""
    supabase_url = get_env_var("NEXT_PUBLIC_SUPABASE_URL")
    supabase_key = get_env_var("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        print("[!] Supabase credentials not found. Skipping database sync.")
        return

    print(f"[*] Ingesting {len(profiles)} leads into Supabase 'bd_leads'...")
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    # Fetch existing linkedin_urls to avoid duplicate insertions
    existing_urls = set()
    try:
        req = urllib.request.Request(
            f"{supabase_url}/rest/v1/bd_leads?select=linkedin_url&limit=2000",
            headers=headers
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for r in data:
                if r.get("linkedin_url"):
                    existing_urls.add(r["linkedin_url"])
    except Exception as e:
        print(f"[!] Warning checking existing leads: {e}")

    inserted_count = 0
    for p in profiles:
        u = p["linkedin_url"]
        if u in existing_urls:
            continue

        lead_payload = {
            "full_name": p["full_name"],
            "company_name": p["company_name"],
            "job_title": p["job_title"],
            "linkedin_url": u,
            "lead_source": "apify_linkedin",
            "enrichment_status": "raw",
            "status": "identified"
        }

        try:
            insert_req = urllib.request.Request(
                f"{supabase_url}/rest/v1/bd_leads",
                headers=headers,
                data=json.dumps(lead_payload).encode("utf-8")
            )
            with urllib.request.urlopen(insert_req) as resp:
                inserted_count += 1
                existing_urls.add(u)
        except Exception as e:
            print(f"[!] Failed to insert {p['full_name']}: {e}")

    print(f"[+] Successfully synced {inserted_count} new leads to Supabase 'bd_leads' (Already existing: {len(profiles) - inserted_count}).")

def main():
    parser = argparse.ArgumentParser(description="LinkedIn Food & Beverage Franchise Scraper")
    parser.add_argument("--dataset", type=str, help="Apify dataset ID to ingest directly")
    parser.add_argument("--no-db", action="store_true", help="Skip Supabase database insertion")
    args = parser.parse_args()

    apify_token = get_env_var("APIFY_TOKEN")
    if not apify_token:
        print("[!] ERROR: APIFY_TOKEN not found.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.dataset:
        dataset_id = args.dataset
        print(f"[*] Using existing dataset: {dataset_id}")
    else:
        queries = [
            'site:za.linkedin.com/in ("franchise owner" OR "franchisee") ("fast food" OR "food and beverage" OR "restaurant" OR "quick service")',
            'site:za.linkedin.com/in ("franchise owner" OR "franchisee") ("Steers" OR "Debonairs" OR "Wimpy" OR "Mugg & Bean" OR "Famous Brands")',
            'site:za.linkedin.com/in ("franchise owner" OR "franchisee") ("Spur" OR "Panarottis" OR "RocoMamas" OR "Hussar Grill")',
            'site:za.linkedin.com/in ("franchise owner" OR "franchisee") ("KFC" OR "Chicken Licken" OR "Hungry Lion" OR "Nando\'s" OR "Pedros")',
            'site:za.linkedin.com/in ("franchise owner" OR "franchisee") ("McDonald\'s" OR "Burger King" OR "Romans Pizza" OR "Ocean Basket" OR "Kauai")',
            'site:za.linkedin.com/in ("multi-unit franchisee" OR "franchise partner" OR "franchise director") ("fast food" OR "restaurant" OR "food")',
            'site:za.linkedin.com/in "Owner" ("KFC franchise" OR "Spur franchise" OR "Steers franchise" OR "Debonairs franchise" OR "Wimpy franchise")',
            'site:linkedin.com/in "South Africa" ("franchise owner" OR "franchisee") ("fast food" OR "food and beverage" OR "QSR" OR "restaurant")'
        ]
        dataset_id = trigger_apify_async(apify_token, queries, max_pages=2)

    raw_items = fetch_dataset_items(apify_token, dataset_id)
    profiles = process_and_filter_results(raw_items)

    print(f"\n[+] Extracted {len(profiles)} qualified South African Fast Food / F&B Franchise Owner profiles.")

    # Save CSV and JSON
    csv_path = OUTPUT_DIR / "sa_food_beverage_franchise_owners_linkedin.csv"
    json_path = OUTPUT_DIR / "sa_food_beverage_franchise_owners_linkedin.json"

    fieldnames = ["full_name", "company_name", "job_title", "location", "linkedin_url", "snippet"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(profiles)
    print(f"[+] Saved CSV: {csv_path}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved JSON: {json_path}")

    if not args.no_db:
        ingest_to_supabase(profiles)

    # Print summary
    print("\n" + "=" * 110)
    print(f"{'Full Name':<25} {'Franchise Brand':<26} {'Role':<26} {'LinkedIn URL'}")
    print("=" * 110)
    for p in profiles[:25]:
        print(f"{p['full_name'][:24]:<25} {p['company_name'][:25]:<26} {p['job_title'][:25]:<26} {p['linkedin_url']}")
    if len(profiles) > 25:
        print(f"... and {len(profiles) - 25} more profiles in {csv_path.name}.")
    print("=" * 110)

if __name__ == "__main__":
    main()

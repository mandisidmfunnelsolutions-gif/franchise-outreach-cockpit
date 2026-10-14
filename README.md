# SA Franchise AI Adoption Study — Outreach Cockpit Dashboard
> **Academic Institution:** University of Pretoria | Department of Business Management  
> **Qualification:** BCom (Honours) in Strategic Business Management  
> **Research Focus:** Investigating AI Adoption, Operational Bottlenecks, and Automation Dynamics across South African Fast Food & Food & Beverage Franchise Networks.

---

## 🚀 Overview

The **Franchise Outreach Cockpit** is a dedicated, interactive single-page dashboard and Python dev server built to streamline outreach to **88 verified South African Fast Food & F&B Franchise Owners** (Spur Corporation, Famous Brands, McDonald's, KFC, Roman's Pizza, Ocean Basket, Kauai, etc.).

### Features:
- **88 Interactive Preview Cards**: Color-coded badges by franchise network, operational role, regional location, and verified LinkedIn snippet.
- **Instant Search & Multi-Filters**: Filter by brand network, province (Gauteng, Western Cape, KZN, Limpopo, Mpumalanga), and outreach status.
- **Detail Modal on Card Click**:
  - Full lead metadata & verified LinkedIn profile button.
  - **Custom Tailored Post-Connection LinkedIn DM** asking for participation in the University of Pretoria study and offering reciprocal benchmark insights.
  - **Pre-Connection Note** (<300 characters) ready to paste into LinkedIn's *"Add a note"* box.
  - **Academic FAQ & Objections Cheat-Sheet** (confidentiality, time commitment, study value).
- **Client-Side Progress Tracking**: Persists outreach status (`Pending`, `Message Copied`, `Contacted`, `Connected`) and private lead notes to browser `localStorage`.
- **Export to CSV**: Export your updated outreach list with private notes directly from the UI.
- **Built-in Endpoints**: `/leads.json` and `/leads.csv` endpoints.

---

## 🏃 Running the Dashboard

### 1. Launch the Local Dev Server
```bash
python3 server.py 3002
```
Open **[http://localhost:3002](http://localhost:3002)** in your browser.

Endpoints:
- **Cockpit Dashboard:** `http://localhost:3002`
- **Leads JSON API:** `http://localhost:3002/leads.json`
- **Leads CSV Export:** `http://localhost:3002/leads.csv`

---

## 🗂️ Project Structure

```
franchise-outreach-cockpit/
├── index.html              # Standalone interactive dashboard (Tailwind CSS, zero build step)
├── server.py               # Lightweight Python HTTP server with JSON/CSV endpoints
├── generator.py            # Script to rebuild index.html from data/
├── scraper.py              # Apify Google Search X-Ray scraper & Supabase sync
├── data/
│   ├── sa_food_beverage_franchise_owners_linkedin.csv
│   └── sa_food_beverage_franchise_owners_linkedin.json
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔄 Re-scraping or Regenerating Data

To run a live LinkedIn scrape:
```bash
python3 scraper.py
```
*(Requires `APIFY_TOKEN` in `.env` or environment)*

To re-compile the single-page dashboard after editing templates or data:
```bash
python3 generator.py
```

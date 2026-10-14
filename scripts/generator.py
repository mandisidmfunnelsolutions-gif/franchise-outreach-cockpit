#!/usr/bin/env python3
"""
Dashboard Generator: South African Food & Beverage Franchise AI Adoption Study.
Builds an interactive single-page dashboard with preview cards, search/filter,
and detailed modal with personalized LinkedIn outreach copy for UP BCom Honours Study.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "data" / "sa_food_beverage_franchise_owners_linkedin.json"
OUTPUT_FILE = BASE_DIR / "index.html"

def generate_dashboard():
    leads = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    
    # Assign unique stable IDs to leads
    for i, lead in enumerate(leads):
        lead["id"] = f"lead_{i+1}"
        # Extract first name
        parts = lead["full_name"].strip().split()
        lead["first_name"] = parts[0] if parts else "there"

    leads_json_str = json.dumps(leads, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Franchise AI Adoption Study — LinkedIn Outreach Cockpit | University of Pretoria</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* Custom scrollbar & aesthetic micro-tweaks */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: rgba(15, 23, 42, 0.6); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(100, 116, 139, 0.5); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(148, 163, 184, 0.8); }}
    .glass-panel {{
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .glass-card {{
      background: rgba(30, 41, 59, 0.6);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.07);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .glass-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(99, 102, 241, 0.4);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 0 15px 1px rgba(99, 102, 241, 0.15);
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased selection:bg-indigo-500 selection:text-white">

  <!-- Main Container -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

    <!-- Header Section -->
    <header class="glass-panel rounded-2xl p-6 sm:p-8 relative overflow-hidden border border-slate-800 shadow-2xl">
      <div class="absolute -right-16 -top-16 w-80 h-80 bg-gradient-to-br from-indigo-500/20 via-purple-500/10 to-transparent rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -left-16 -bottom-16 w-80 h-80 bg-gradient-to-tr from-amber-500/10 via-emerald-500/10 to-transparent rounded-full blur-3xl pointer-events-none"></div>
      
      <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-3">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            University of Pretoria • BCom (Hons) Strategic Business Management
          </div>
          <h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold tracking-tight text-white">
            Franchise AI Adoption Study <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-amber-300">Outreach Cockpit</span>
          </h1>
          <p class="text-slate-400 mt-2 text-sm sm:text-base max-w-3xl leading-relaxed">
            Targeting 88 Verified South African Fast Food & F&B Franchisees (Spur, Famous Brands, McDonald's, KFC, Roman's Pizza). Select any card to review profile insights and copy tailor-made, academic outreach messages.
          </p>
        </div>
        
        <div class="flex items-center gap-3 self-start md:self-center">
          <button id="btnExport" class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition shadow-sm hover:border-slate-600">
            <svg class="w-4 h-4 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            Export Lead List
          </button>
          <button id="btnResetProgress" class="inline-flex items-center gap-1.5 px-3 py-2.5 rounded-xl text-xs font-medium text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 border border-transparent hover:border-rose-500/20 transition">
            Reset Status
          </button>
        </div>
      </div>

      <!-- Quick Metrics Bar -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-8 pt-6 border-t border-slate-800/80">
        <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <p class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Total Verified Leads</p>
          <div class="flex items-baseline gap-2 mt-1">
            <span class="text-2xl font-bold text-white" id="statTotal">88</span>
            <span class="text-xs text-indigo-400">100% Live</span>
          </div>
        </div>
        <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <p class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Messages Copied</p>
          <div class="flex items-baseline gap-2 mt-1">
            <span class="text-2xl font-bold text-amber-400" id="statCopied">0</span>
            <span class="text-xs text-slate-500" id="statCopiedPct">0%</span>
          </div>
        </div>
        <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <p class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Contacted / Sent</p>
          <div class="flex items-baseline gap-2 mt-1">
            <span class="text-2xl font-bold text-emerald-400" id="statSent">0</span>
            <span class="text-xs text-slate-500" id="statSentPct">0%</span>
          </div>
        </div>
        <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <p class="text-xs uppercase tracking-wider text-slate-400 font-semibold">Pending Outreach</p>
          <div class="flex items-baseline gap-2 mt-1">
            <span class="text-2xl font-bold text-slate-300" id="statPending">88</span>
            <span class="text-xs text-slate-500">Uncontacted</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Filter & Search Toolbar -->
    <div class="glass-panel rounded-2xl p-4 sm:p-5 border border-slate-800 flex flex-col lg:flex-row gap-4 items-stretch lg:items-center justify-between">
      <!-- Search Box -->
      <div class="relative flex-1">
        <svg class="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <input 
          type="text" 
          id="searchInput" 
          placeholder="Search by name, franchise (Spur, Steers, KFC...), title, or city..." 
          class="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition"
        />
      </div>

      <!-- Filter Controls -->
      <div class="flex flex-wrap items-center gap-2.5 sm:gap-3">
        <!-- Brand Group Filter -->
        <select id="brandFilter" class="bg-slate-900/90 border border-slate-700/80 rounded-xl px-3 py-2.5 text-xs sm:text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/50">
          <option value="all">All Franchise Networks</option>
          <option value="spur">Spur Group (Spur, RocoMamas, Panarottis)</option>
          <option value="famous">Famous Brands (Steers, Debonairs, Wimpy)</option>
          <option value="mcdonalds">McDonald's</option>
          <option value="romans">Roman's Pizza</option>
          <option value="chicken">Chicken QSR (KFC, Nando's, Chicken Licken)</option>
          <option value="cafe">Cafe / QSR (Kauai, Ocean Basket, Vida)</option>
        </select>

        <!-- Region Filter -->
        <select id="regionFilter" class="bg-slate-900/90 border border-slate-700/80 rounded-xl px-3 py-2.5 text-xs sm:text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/50">
          <option value="all">All Regions (SA)</option>
          <option value="Gauteng">Gauteng (JHB / Pretoria)</option>
          <option value="Western Cape">Western Cape (Cape Town)</option>
          <option value="KwaZulu-Natal">KwaZulu-Natal (Durban)</option>
          <option value="Limpopo">Limpopo</option>
          <option value="Mpumalanga">Mpumalanga</option>
        </select>

        <!-- Status Filter -->
        <select id="statusFilter" class="bg-slate-900/90 border border-slate-700/80 rounded-xl px-3 py-2.5 text-xs sm:text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/50">
          <option value="all">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="copied">Message Copied</option>
          <option value="sent">Contacted</option>
          <option value="starred">Starred / High Priority</option>
        </select>
      </div>
    </div>

    <!-- Active Filters & Result Count -->
    <div class="flex items-center justify-between text-xs text-slate-400 px-1">
      <span id="resultCountLabel">Showing 88 of 88 franchise owners</span>
      <span class="hidden sm:inline">Tip: Click any card to launch the Outreach & Message modal</span>
    </div>

    <!-- Leads Grid -->
    <div id="leadsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <!-- Injected via JavaScript -->
    </div>

    <!-- Empty State -->
    <div id="emptyState" class="hidden glass-panel rounded-2xl p-12 text-center border border-slate-800">
      <div class="w-16 h-16 mx-auto rounded-full bg-slate-800 flex items-center justify-center text-slate-400 mb-4">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      </div>
      <h3 class="text-lg font-bold text-white">No matching franchise owners found</h3>
      <p class="text-slate-400 text-sm mt-1 max-w-sm mx-auto">Try clearing your search terms or relaxing brand/region filters.</p>
      <button onclick="resetFilters()" class="mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-medium transition">
        Reset All Filters
      </button>
    </div>

  </div>

  <!-- Detail & Outreach Modal -->
  <div id="modalBackdrop" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex items-center justify-center p-3 sm:p-5 hidden opacity-0 transition-opacity duration-200">
    <div id="modalBox" class="bg-slate-900 border border-slate-700/80 rounded-2xl w-full max-w-3xl max-h-[92vh] flex flex-col shadow-2xl transform scale-95 transition-transform duration-200 overflow-hidden">
      
      <!-- Modal Header -->
      <div class="px-6 py-5 border-b border-slate-800 bg-slate-900/90 flex items-start justify-between gap-4">
        <div class="flex items-center gap-4">
          <div id="modalAvatar" class="w-12 h-12 rounded-xl bg-gradient-to-tr from-indigo-600 to-amber-500 flex items-center justify-center font-bold text-lg text-white shadow-md">
            RP
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h2 id="modalName" class="text-xl font-bold text-white">Riyaadh Petersen</h2>
              <button id="modalStarBtn" onclick="toggleLeadStarCurrent()" class="text-slate-500 hover:text-amber-400 transition" title="Star lead">
                <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              </button>
            </div>
            <div class="flex flex-wrap items-center gap-2 mt-1">
              <span id="modalBrandBadge" class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Spur Steak Ranches
              </span>
              <span id="modalRole" class="text-xs text-slate-300 font-medium">Franchisee</span>
              <span class="text-xs text-slate-500">•</span>
              <span id="modalLocation" class="text-xs text-slate-400 flex items-center gap-1">
                <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                Cape Town
              </span>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <a id="modalLinkedinLink" href="#" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#0A66C2]/20 hover:bg-[#0A66C2]/30 text-[#70B5F9] border border-[#0A66C2]/40 transition">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.64 1.64 0 1 0 0-3.28 1.64 1.64 0 0 0 0 3.28m1.4 9.74v-8.37H5.06v8.37h2.8z"/></svg>
            Open Profile
          </a>
          <button onclick="closeModal()" class="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-white hover:bg-slate-800 transition">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>

      <!-- Modal Body (Scrollable) -->
      <div class="p-6 overflow-y-auto space-y-6 flex-1 text-sm">

        <!-- LinkedIn Summary Snippet -->
        <div class="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80">
          <p class="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-1">LinkedIn Profile Evidence</p>
          <p id="modalSnippet" class="text-slate-300 text-xs italic leading-relaxed">
            "Riyaadh Petersen. Franchisee of RocoMamas, Spur Steak Ranches & Panarottis..."
          </p>
        </div>

        <!-- Tabbed Message Drafter -->
        <div>
          <div class="flex border-b border-slate-800 gap-6 text-xs font-semibold">
            <button id="tabPostConnectBtn" onclick="switchTab('postConnect')" class="pb-2.5 text-indigo-400 border-b-2 border-indigo-500 transition">
              1. Post-Connection LinkedIn DM (Recommended)
            </button>
            <button id="tabPreConnectBtn" onclick="switchTab('preConnect')" class="pb-2.5 text-slate-400 hover:text-slate-200 transition">
              2. Pre-Connect Note (&lt;300 Chars)
            </button>
            <button id="tabStudyNotesBtn" onclick="switchTab('studyNotes')" class="pb-2.5 text-slate-400 hover:text-slate-200 transition">
              3. Study Context & Cheat-Sheet
            </button>
          </div>

          <!-- Tab 1: Post-Connection Message -->
          <div id="tabPostConnect" class="pt-4 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs text-slate-400">Personalized for <strong id="msgTargetName" class="text-white">Riyaadh</strong>:</span>
              <button onclick="copyCurrentMessage('postConnect')" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-sm">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                Copy Message
              </button>
            </div>
            <textarea id="postConnectText" rows="12" class="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl p-4 text-xs sm:text-sm text-slate-200 font-mono leading-relaxed focus:outline-none focus:ring-2 focus:ring-indigo-500/50"></textarea>
          </div>

          <!-- Tab 2: Connection Note -->
          <div id="tabPreConnect" class="pt-4 space-y-3 hidden">
            <div class="flex items-center justify-between">
              <span class="text-xs text-slate-400">Add to LinkedIn "Add a note" (<span id="preConnectCharCount" class="text-amber-400">0</span>/300 chars):</span>
              <button onclick="copyCurrentMessage('preConnect')" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-sm">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                Copy Note
              </button>
            </div>
            <textarea id="preConnectText" rows="4" class="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl p-4 text-xs sm:text-sm text-slate-200 font-mono leading-relaxed focus:outline-none focus:ring-2 focus:ring-indigo-500/50"></textarea>
          </div>

          <!-- Tab 3: Study Notes & Cheat Sheet -->
          <div id="tabStudyNotes" class="pt-4 space-y-4 hidden text-xs text-slate-300">
            <div class="p-4 rounded-xl bg-slate-950/50 border border-slate-800 space-y-3">
              <h4 class="font-bold text-amber-300 uppercase tracking-wider text-[11px]">Academic Context & Objections Handling</h4>
              <p><strong>Institution:</strong> University of Pretoria, Department of Business Management</p>
              <p><strong>Qualification:</strong> BCom (Honours) in Strategic Business Management</p>
              <p><strong>Research Core:</strong> Evaluating practical barriers, operational leverage, and AI readiness across South African Quick Service Restaurant (QSR) and Food & Beverage franchise operators.</p>
              <p><strong>Confidentiality Guarantee:</strong> Strict academic ethics compliance. Data is aggregated anonymously. No individual proprietary financial data is published.</p>
              <p><strong>Reciprocal Value:</strong> Every participating franchisee receives a complimentary copy of the compiled <em>"AI & Operational Automation Benchmark for SA Franchise Operations"</em>.</p>
            </div>
          </div>
        </div>

        <!-- Outreach Status Selector & Private Notes -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-slate-800">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Outreach Status</label>
            <div class="flex flex-wrap gap-2">
              <button onclick="setLeadStatus('pending')" id="statusBtn_pending" class="px-3 py-1.5 rounded-lg text-xs font-medium border border-slate-700 bg-slate-800 text-slate-300">Pending</button>
              <button onclick="setLeadStatus('copied')" id="statusBtn_copied" class="px-3 py-1.5 rounded-lg text-xs font-medium border border-slate-700 bg-slate-800 text-slate-300">Message Copied</button>
              <button onclick="setLeadStatus('sent')" id="statusBtn_sent" class="px-3 py-1.5 rounded-lg text-xs font-medium border border-slate-700 bg-slate-800 text-slate-300">Contacted / Sent</button>
              <button onclick="setLeadStatus('connected')" id="statusBtn_connected" class="px-3 py-1.5 rounded-lg text-xs font-medium border border-slate-700 bg-slate-800 text-slate-300">Connected</button>
            </div>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Private Notes for this Lead</label>
            <input type="text" id="leadNoteInput" onchange="saveLeadNote()" placeholder="e.g. Sent invite Oct 14; owns 3 Panarottis..." class="w-full bg-slate-950/80 border border-slate-700/80 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/50">
          </div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="px-6 py-4 border-t border-slate-800 bg-slate-900/90 flex items-center justify-between text-xs text-slate-400">
        <span id="modalLeadIdLabel">Lead #1 of 88</span>
        <div class="flex items-center gap-3">
          <button onclick="navigateLead(-1)" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition">
            ← Previous
          </button>
          <button onclick="navigateLead(1)" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition">
            Next →
          </button>
        </div>
      </div>

    </div>
  </div>

  <!-- Toast Notification -->
  <div id="toast" class="fixed bottom-6 right-6 bg-indigo-600 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center gap-3 transform translate-y-24 opacity-0 transition-all duration-300 z-50 text-sm font-medium border border-indigo-400/30">
    <svg class="w-5 h-5 text-emerald-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
    <span id="toastMessage">Copied to clipboard!</span>
  </div>

  <script>
    // Injected Lead Dataset (88 Verified Leads)
    const LEADS_DATA = {leads_json_str};

    // State
    let currentLeads = [...LEADS_DATA];
    let selectedLead = null;
    let currentTab = 'postConnect';
    let leadStates = JSON.parse(localStorage.getItem('franchise_lead_states') || '{{}}');

    // Brand Group Mapping
    const BRAND_GROUPS = {{
      spur: ['spur', 'rocomamas', 'panarottis', 'hussar'],
      famous: ['famous brands', 'steers', 'debonairs', 'wimpy', 'mugg', 'fishaways', 'milky lane'],
      mcdonalds: ['mcdonald'],
      romans: ['roman'],
      chicken: ['kfc', 'chicken licken', 'nando', 'hungry lion', 'pedro'],
      cafe: ['kauai', 'ocean basket', 'vida', 'simply asia', 'xpresso']
    }};

    // Initialize
    document.addEventListener('DOMContentLoaded', () => {{
      renderLeads();
      updateStats();
      setupEventListeners();
    }});

    function setupEventListeners() {{
      document.getElementById('searchInput').addEventListener('input', applyFilters);
      document.getElementById('brandFilter').addEventListener('change', applyFilters);
      document.getElementById('regionFilter').addEventListener('change', applyFilters);
      document.getElementById('statusFilter').addEventListener('change', applyFilters);
      document.getElementById('btnExport').addEventListener('click', exportToCSV);
      document.getElementById('btnResetProgress').addEventListener('click', resetAllProgress);

      // Close modal on escape or backdrop click
      document.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape') closeModal();
      }});
      document.getElementById('modalBackdrop').addEventListener('click', (e) => {{
        if (e.target.id === 'modalBackdrop') closeModal();
      }});
    }}

    function applyFilters() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();
      const brand = document.getElementById('brandFilter').value;
      const region = document.getElementById('regionFilter').value;
      const status = document.getElementById('statusFilter').value;

      currentLeads = LEADS_DATA.filter(lead => {{
        const fullText = `${{lead.full_name}} ${{lead.company_name}} ${{lead.job_title}} ${{lead.location}} ${{lead.snippet}}`.toLowerCase();
        
        // Search query
        if (query && !fullText.includes(query)) return false;

        // Brand group
        if (brand !== 'all') {{
          const targetTerms = BRAND_GROUPS[brand] || [];
          const matchesBrand = targetTerms.some(term => lead.company_name.toLowerCase().includes(term) || lead.snippet.toLowerCase().includes(term));
          if (!matchesBrand) return false;
        }}

        // Region
        if (region !== 'all') {{
          if (!lead.location.toLowerCase().includes(region.toLowerCase())) return false;
        }}

        // Status
        const st = (leadStates[lead.id] && leadStates[lead.id].status) || 'pending';
        const isStarred = leadStates[lead.id] && leadStates[lead.id].starred;

        if (status === 'starred' && !isStarred) return false;
        if (status === 'pending' && st !== 'pending') return false;
        if (status === 'copied' && st !== 'copied') return false;
        if (status === 'sent' && st !== 'sent' && st !== 'connected') return false;

        return true;
      }});

      renderLeads();
    }}

    function resetFilters() {{
      document.getElementById('searchInput').value = '';
      document.getElementById('brandFilter').value = 'all';
      document.getElementById('regionFilter').value = 'all';
      document.getElementById('statusFilter').value = 'all';
      applyFilters();
    }}

    function renderLeads() {{
      const grid = document.getElementById('leadsGrid');
      const emptyState = document.getElementById('emptyState');
      const countLabel = document.getElementById('resultCountLabel');

      countLabel.textContent = `Showing ${{currentLeads.length}} of ${{LEADS_DATA.length}} franchise owners`;

      if (currentLeads.length === 0) {{
        grid.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
      }}
      emptyState.classList.add('hidden');

      grid.innerHTML = currentLeads.map(lead => {{
        const state = leadStates[lead.id] || {{ status: 'pending', starred: false }};
        const initials = lead.full_name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();
        
        // Badge color mapping
        let badgeColor = 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20';
        const cLower = lead.company_name.toLowerCase();
        if (cLower.includes('spur') || cLower.includes('rocomamas')) badgeColor = 'bg-rose-500/10 text-rose-400 border-rose-500/20';
        else if (cLower.includes('famous') || cLower.includes('steers') || cLower.includes('debonairs')) badgeColor = 'bg-amber-500/10 text-amber-400 border-amber-500/20';
        else if (cLower.includes('mcdonald')) badgeColor = 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
        else if (cLower.includes('kfc')) badgeColor = 'bg-red-500/10 text-red-400 border-red-500/20';
        else if (cLower.includes('roman')) badgeColor = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';

        // Status badge
        let statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-400">Uncontacted</span>';
        if (state.status === 'copied') statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-300">Message Copied</span>';
        if (state.status === 'sent') statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/20 text-emerald-300">Contacted</span>';
        if (state.status === 'connected') statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-500/20 text-blue-300">Connected</span>';

        return `
          <div class="glass-card rounded-2xl p-5 flex flex-col justify-between cursor-pointer group" onclick="openLeadModal('${{lead.id}}')">
            <div>
              <div class="flex items-start justify-between gap-3">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-slate-800 to-indigo-900 border border-slate-700/80 flex items-center justify-center font-bold text-xs text-white shadow-sm group-hover:border-indigo-500/50 transition">
                    ${{initials}}
                  </div>
                  <div>
                    <h3 class="font-bold text-white text-base group-hover:text-indigo-300 transition flex items-center gap-1.5">
                      ${{lead.full_name}}
                      ${{state.starred ? '<span class="text-amber-400 text-xs">★</span>' : ''}}
                    </h3>
                    <p class="text-xs text-slate-400 font-medium">${{lead.job_title}}</p>
                  </div>
                </div>
                <div>${{statusBadge}}</div>
              </div>

              <div class="mt-4 flex flex-wrap items-center gap-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold border ${{badgeColor}}">
                  ${{lead.company_name}}
                </span>
                <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs text-slate-400 bg-slate-900/60 border border-slate-800">
                  <svg class="w-3 h-3 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  ${{lead.location}}
                </span>
              </div>

              <p class="text-xs text-slate-400 mt-3 line-clamp-2 leading-relaxed">
                ${{lead.snippet}}
              </p>
            </div>

            <div class="mt-5 pt-3.5 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-indigo-400 font-medium group-hover:underline flex items-center gap-1">
                Draft Outreach
                <svg class="w-3.5 h-3.5 transform group-hover:translate-x-0.5 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </span>
              <a href="${{lead.linkedin_url}}" target="_blank" onclick="event.stopPropagation()" class="text-slate-400 hover:text-white flex items-center gap-1" title="Open LinkedIn Profile">
                <svg class="w-4 h-4 fill-current text-[#70B5F9]" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.64 1.64 0 1 0 0-3.28 1.64 1.64 0 0 0 0 3.28m1.4 9.74v-8.37H5.06v8.37h2.8z"/></svg>
              </a>
            </div>
          </div>
        `;
      }}).join('');
    }}

    function generatePersonalizedMessages(lead) {{
      const firstName = lead.first_name || 'there';
      const brand = lead.company_name || 'your franchise network';
      const role = lead.job_title || 'Franchise Owner';
      const location = lead.location || 'South Africa';

      // 1. Full Post-Connection LinkedIn Message
      const postConnect = `Hi ${{firstName}},

Thanks so much for connecting with me here on LinkedIn!

I've been following the impressive footprint of ${{brand}} across ${{location}}, and I'm currently conducting field research for my BCom Honours in Strategic Business Management study at the University of Pretoria.

My research is specifically focused on AI adoption, automation, and operational technology trends across franchise operations in South Africa—exploring where franchise owners see genuine operational value versus current bottlenecks (like inventory forecasting, labor scheduling, customer ordering, and system integrations).

Given your hands-on experience running ${{brand}} as a ${{role}}, your perspective would be invaluable. Would you be open to a brief 10–15 minute conversation (or completing a short confidential questionnaire) to share your thoughts?

All findings are strictly academic, confidential, and anonymous. I would also be delighted to share the final executive summary and benchmark insights with you once completed so you can see where your operations sit relative to the rest of the industry.

Thank you for your time, ${{firstName}}, and I look forward to hearing your thoughts!

Warm regards,
Mandisi Kgoadi
University of Pretoria | BCom (Hons) Strategic Business Management`;

      // 2. Pre-Connection Note (<300 Chars)
      const preConnect = `Hi ${{firstName}}, thank you for connecting! I'm researching AI and automation adoption within franchise operations for my BCom Honours in Strategic Business Management at the University of Pretoria. Given your leadership at ${{brand}}, I'd love to connect and share benchmark findings!`;

      return {{ postConnect, preConnect }};
    }}

    function openLeadModal(leadId) {{
      selectedLead = LEADS_DATA.find(l => l.id === leadId);
      if (!selectedLead) return;

      const state = leadStates[leadId] || {{ status: 'pending', starred: false, note: '' }};
      const initials = selectedLead.full_name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();

      document.getElementById('modalAvatar').textContent = initials;
      document.getElementById('modalName').textContent = selectedLead.full_name;
      document.getElementById('modalRole').textContent = selectedLead.job_title;
      document.getElementById('modalBrandBadge').textContent = selectedLead.company_name;
      document.getElementById('modalLocation').innerHTML = `
        <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        ${{selectedLead.location}}
      `;
      document.getElementById('modalLinkedinLink').href = selectedLead.linkedin_url;
      document.getElementById('modalSnippet').textContent = `"${{selectedLead.snippet}}"`;
      document.getElementById('msgTargetName').textContent = selectedLead.first_name;
      document.getElementById('leadNoteInput').value = state.note || '';

      const {{ postConnect, preConnect }} = generatePersonalizedMessages(selectedLead);
      document.getElementById('postConnectText').value = postConnect;
      document.getElementById('preConnectText').value = preConnect;
      document.getElementById('preConnectCharCount').textContent = preConnect.length;

      updateStatusButtons(state.status || 'pending');
      updateStarIcon(state.starred);

      // Update lead index tracker
      const currentIndex = currentLeads.findIndex(l => l.id === leadId);
      document.getElementById('modalLeadIdLabel').textContent = `Lead ${{currentIndex + 1}} of ${{currentLeads.length}} (${{selectedLead.id}})`;

      // Show modal
      const backdrop = document.getElementById('modalBackdrop');
      const box = document.getElementById('modalBox');
      backdrop.classList.remove('hidden');
      setTimeout(() => {{
        backdrop.classList.remove('opacity-0');
        box.classList.remove('scale-95');
      }}, 10);
    }}

    function closeModal() {{
      const backdrop = document.getElementById('modalBackdrop');
      const box = document.getElementById('modalBox');
      backdrop.classList.add('opacity-0');
      box.classList.add('scale-95');
      setTimeout(() => {{
        backdrop.classList.add('hidden');
        selectedLead = null;
      }}, 200);
    }}

    function navigateLead(direction) {{
      if (!selectedLead) return;
      const currentIndex = currentLeads.findIndex(l => l.id === selectedLead.id);
      if (currentIndex === -1) return;
      const nextIndex = (currentIndex + direction + currentLeads.length) % currentLeads.length;
      openLeadModal(currentLeads[nextIndex].id);
    }}

    function switchTab(tab) {{
      currentTab = tab;
      const btn1 = document.getElementById('tabPostConnectBtn');
      const btn2 = document.getElementById('tabPreConnectBtn');
      const btn3 = document.getElementById('tabStudyNotesBtn');
      const tab1 = document.getElementById('tabPostConnect');
      const tab2 = document.getElementById('tabPreConnect');
      const tab3 = document.getElementById('tabStudyNotes');

      [btn1, btn2, btn3].forEach(b => {{
        b.classList.remove('text-indigo-400', 'border-b-2', 'border-indigo-500');
        b.classList.add('text-slate-400');
      }});
      [tab1, tab2, tab3].forEach(t => t.classList.add('hidden'));

      if (tab === 'postConnect') {{
        btn1.classList.add('text-indigo-400', 'border-b-2', 'border-indigo-500');
        tab1.classList.remove('hidden');
      }} else if (tab === 'preConnect') {{
        btn2.classList.add('text-indigo-400', 'border-b-2', 'border-indigo-500');
        tab2.classList.remove('hidden');
      }} else if (tab === 'studyNotes') {{
        btn3.classList.add('text-indigo-400', 'border-b-2', 'border-indigo-500');
        tab3.classList.remove('hidden');
      }}
    }}

    function copyCurrentMessage(type) {{
      const text = type === 'postConnect' ? document.getElementById('postConnectText').value : document.getElementById('preConnectText').value;
      navigator.clipboard.writeText(text).then(() => {{
        showToast(type === 'postConnect' ? 'Full LinkedIn DM copied to clipboard!' : 'Pre-connect note copied to clipboard!');
        if (selectedLead) {{
          setLeadStatus('copied');
        }}
      }});
    }}

    function setLeadStatus(status) {{
      if (!selectedLead) return;
      if (!leadStates[selectedLead.id]) leadStates[selectedLead.id] = {{}};
      leadStates[selectedLead.id].status = status;
      saveStates();
      updateStatusButtons(status);
      updateStats();
      renderLeads();
    }}

    function updateStatusButtons(activeStatus) {{
      ['pending', 'copied', 'sent', 'connected'].forEach(s => {{
        const btn = document.getElementById(`statusBtn_${{s}}`);
        if (!btn) return;
        if (s === activeStatus) {{
          btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 text-white border border-indigo-500 shadow-sm';
        }} else {{
          btn.className = 'px-3 py-1.5 rounded-lg text-xs font-medium border border-slate-700 bg-slate-800 text-slate-300 hover:bg-slate-700';
        }}
      }});
    }}

    function toggleLeadStarCurrent() {{
      if (!selectedLead) return;
      if (!leadStates[selectedLead.id]) leadStates[selectedLead.id] = {{}};
      leadStates[selectedLead.id].starred = !leadStates[selectedLead.id].starred;
      saveStates();
      updateStarIcon(leadStates[selectedLead.id].starred);
      renderLeads();
    }}

    function updateStarIcon(starred) {{
      const btn = document.getElementById('modalStarBtn');
      if (starred) {{
        btn.classList.add('text-amber-400');
        btn.classList.remove('text-slate-500');
      }} else {{
        btn.classList.remove('text-amber-400');
        btn.classList.add('text-slate-500');
      }}
    }}

    function saveLeadNote() {{
      if (!selectedLead) return;
      if (!leadStates[selectedLead.id]) leadStates[selectedLead.id] = {{}};
      leadStates[selectedLead.id].note = document.getElementById('leadNoteInput').value;
      saveStates();
      showToast('Note saved');
    }}

    function saveStates() {{
      localStorage.setItem('franchise_lead_states', JSON.stringify(leadStates));
    }}

    function updateStats() {{
      const total = LEADS_DATA.length;
      let copied = 0;
      let sent = 0;

      Object.values(leadStates).forEach(st => {{
        if (st.status === 'copied') copied++;
        if (st.status === 'sent' || st.status === 'connected') sent++;
      }});

      const pending = total - (copied + sent);

      document.getElementById('statTotal').textContent = total;
      document.getElementById('statCopied').textContent = copied;
      document.getElementById('statCopiedPct').textContent = `${{Math.round((copied/total)*100)}}%`;
      document.getElementById('statSent').textContent = sent;
      document.getElementById('statSentPct').textContent = `${{Math.round((sent/total)*100)}}%`;
      document.getElementById('statPending').textContent = pending;
    }}

    function resetAllProgress() {{
      if (confirm('Reset all outreach status back to Uncontacted?')) {{
        leadStates = {{}};
        saveStates();
        updateStats();
        renderLeads();
        showToast('All progress reset');
      }}
    }}

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      document.getElementById('toastMessage').textContent = msg;
      toast.classList.remove('translate-y-24', 'opacity-0');
      setTimeout(() => {{
        toast.classList.add('translate-y-24', 'opacity-0');
      }}, 3000);
    }}

    function exportToCSV() {{
      const headers = ['Full Name', 'Company / Brand', 'Role', 'Location', 'LinkedIn URL', 'Outreach Status', 'Private Notes'];
      const rows = LEADS_DATA.map(l => {{
        const st = leadStates[l.id] || {{ status: 'pending', note: '' }};
        return [
          `"${{l.full_name}}"`,
          `"${{l.company_name}}"`,
          `"${{l.job_title}}"`,
          `"${{l.location}}"`,
          `"${{l.linkedin_url}}"`,
          `"${{st.status || 'pending'}}"`,
          `"${{st.note || ''}}"`
        ].join(',');
      }});
      const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows].join('\\n');
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement('a');
      link.setAttribute('href', encodedUri);
      link.setAttribute('download', `sa_franchise_ai_study_outreach_${{new Date().toISOString().slice(0,10)}}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast('Exporting CSV download...');
    }}
  </script>
</body>
</html>
"""

    OUTPUT_FILE.write_text(html_content, encoding="utf-8")
    print(f"[+] Successfully generated dashboard at: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_dashboard()

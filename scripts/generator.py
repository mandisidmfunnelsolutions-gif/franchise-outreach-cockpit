#!/usr/bin/env python3
"""
Dashboard Generator: South African Food & Beverage Franchise AI Adoption Study.
Builds an interactive single-page dashboard with preview cards, search/filter,
and detailed modal with personalized LinkedIn outreach copy for UP BCom Honours Study.
Optimized for Desktop and Mobile (iOS/Android) with Bottom-Sheet drawer modal,
horizontal filter chips, touch-friendly tap targets, and iOS zoom prevention.
"""

import json
from pathlib import Path

# Resolve base directories safely whether run from root or scripts/
BASE_DIR = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "scripts" else Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "data" / "sa_food_beverage_franchise_owners_linkedin.json"
OUTPUT_FILE = BASE_DIR / "index.html"

# Mirrored workspace copy for local dev server
WORKSPACE_ROOT = BASE_DIR.parent.parent
MIRROR_FILE = WORKSPACE_ROOT / "Outreach" / "Lead_Lists" / "franchise_study_dashboard.html"

def generate_dashboard():
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"Missing JSON dataset at: {JSON_PATH}")

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
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="theme-color" content="#020617">
  <title>Franchise AI Adoption Study — LinkedIn Outreach Cockpit | University of Pretoria</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* Safe Area insets & CSS variables */
    :root {{
      --sat: env(safe-area-inset-top, 0px);
      --sar: env(safe-area-inset-right, 0px);
      --sab: env(safe-area-inset-bottom, 0px);
      --sal: env(safe-area-inset-left, 0px);
    }}
    .pb-safe {{ padding-bottom: max(1rem, env(safe-area-inset-bottom)); }}
    .pt-safe {{ padding-top: max(1rem, env(safe-area-inset-top)); }}

    /* Touch optimizations */
    * {{
      -webkit-tap-highlight-color: transparent;
    }}

    /* Prevent iOS auto-zoom on input focus */
    @media (max-width: 639px) {{
      input, select, textarea {{
        font-size: 16px !important;
      }}
    }}

    /* Custom scrollbar & aesthetic micro-tweaks */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: rgba(15, 23, 42, 0.6); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(100, 116, 139, 0.5); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(148, 163, 184, 0.8); }}

    /* Hide scrollbars for horizontal tab/chip lists */
    .no-scrollbar::-webkit-scrollbar {{ display: none; }}
    .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}

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
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .glass-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(99, 102, 241, 0.4);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 0 15px 1px rgba(99, 102, 241, 0.15);
    }}
    .glass-card:active {{
      transform: scale(0.99);
    }}

    /* Filter chip active style */
    .chip-active {{
      background-color: #4f46e5 !important;
      color: #ffffff !important;
      border-color: #6366f1 !important;
      font-weight: 600;
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased selection:bg-indigo-500 selection:text-white">

  <!-- Main Container -->
  <div class="max-w-7xl mx-auto px-3.5 sm:px-6 lg:px-8 py-4 sm:py-8 space-y-4 sm:space-y-8 pb-12">

    <!-- Header Section -->
    <header class="glass-panel rounded-2xl p-4 sm:p-8 relative overflow-hidden border border-slate-800 shadow-2xl">
      <div class="absolute -right-16 -top-16 w-80 h-80 bg-gradient-to-br from-indigo-500/20 via-purple-500/10 to-transparent rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -left-16 -bottom-16 w-80 h-80 bg-gradient-to-tr from-amber-500/10 via-emerald-500/10 to-transparent rounded-full blur-3xl pointer-events-none"></div>
      
      <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4 sm:gap-6">
        <div>
          <div class="inline-flex items-center gap-1.5 sm:gap-2 px-2.5 sm:px-3 py-1 rounded-full text-[11px] sm:text-xs font-semibold uppercase tracking-wider bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-2.5 sm:mb-3">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>University of Pretoria • BCom (Hons) SBM</span>
          </div>
          <h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold tracking-tight text-white leading-tight">
            Franchise AI Adoption Study <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-amber-300">Outreach Cockpit</span>
          </h1>
          <p class="text-slate-400 mt-2 text-xs sm:text-sm md:text-base max-w-3xl leading-relaxed">
            Targeting 88 Verified South African Fast Food & F&B Franchisees (Spur, Famous Brands, McDonald's, KFC, Roman's Pizza). Tap any card to review profile insights and copy tailor-made academic outreach copy.
          </p>
        </div>
        
        <div class="flex items-center gap-2 sm:gap-3 w-full sm:w-auto pt-2 sm:pt-0 border-t sm:border-t-0 border-slate-800/60">
          <button id="btnExport" class="flex-1 sm:flex-initial inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 hover:bg-slate-700 active:bg-slate-700 text-slate-200 border border-slate-700 transition shadow-sm min-h-[44px]">
            <svg class="w-4 h-4 text-indigo-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <span>Export CSV</span>
          </button>
          <button id="btnResetProgress" class="inline-flex items-center justify-center px-3 py-2.5 rounded-xl text-xs font-medium text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 active:bg-rose-500/20 border border-slate-800 sm:border-transparent transition min-h-[44px]">
            Reset
          </button>
        </div>
      </div>

      <!-- Quick Metrics Bar -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-4 mt-6 sm:mt-8 pt-5 sm:pt-6 border-t border-slate-800/80">
        <div class="bg-slate-900/60 p-3 sm:p-4 rounded-xl border border-slate-800">
          <p class="text-[10px] sm:text-xs uppercase tracking-wider text-slate-400 font-semibold truncate">Verified Leads</p>
          <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">
            <span class="text-xl sm:text-2xl font-bold text-white" id="statTotal">88</span>
            <span class="text-[10px] sm:text-xs text-indigo-400">100% Live</span>
          </div>
        </div>
        <div class="bg-slate-900/60 p-3 sm:p-4 rounded-xl border border-slate-800">
          <p class="text-[10px] sm:text-xs uppercase tracking-wider text-slate-400 font-semibold truncate">Messages Copied</p>
          <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">
            <span class="text-xl sm:text-2xl font-bold text-amber-400" id="statCopied">0</span>
            <span class="text-[10px] sm:text-xs text-slate-500" id="statCopiedPct">0%</span>
          </div>
        </div>
        <div class="bg-slate-900/60 p-3 sm:p-4 rounded-xl border border-slate-800">
          <p class="text-[10px] sm:text-xs uppercase tracking-wider text-slate-400 font-semibold truncate">Contacted / Sent</p>
          <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">
            <span class="text-xl sm:text-2xl font-bold text-emerald-400" id="statSent">0</span>
            <span class="text-[10px] sm:text-xs text-slate-500" id="statSentPct">0%</span>
          </div>
        </div>
        <div class="bg-slate-900/60 p-3 sm:p-4 rounded-xl border border-slate-800">
          <p class="text-[10px] sm:text-xs uppercase tracking-wider text-slate-400 font-semibold truncate">Pending Outreach</p>
          <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">
            <span class="text-xl sm:text-2xl font-bold text-slate-300" id="statPending">88</span>
            <span class="text-[10px] sm:text-xs text-slate-500">Uncontacted</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Filter & Search Toolbar -->
    <div class="glass-panel rounded-2xl p-3.5 sm:p-5 border border-slate-800 space-y-3">
      
      <!-- Search Box with Clear Button -->
      <div class="relative w-full">
        <svg class="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <input 
          type="text" 
          id="searchInput" 
          placeholder="Search by name, franchise, title, city..." 
          class="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl pl-10 pr-9 py-2.5 sm:py-2.5 text-base sm:text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition min-h-[44px]"
        />
        <button id="searchClearBtn" onclick="clearSearch()" class="hidden absolute right-3 top-1/2 -translate-y-1/2 w-6 h-6 rounded-full bg-slate-800 text-slate-400 hover:text-white flex items-center justify-center text-xs">
          ✕
        </button>
      </div>

      <!-- Quick Mobile Filter Chips (Thumb-Friendly Horizontal Scroll) -->
      <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1 -mx-1 px-1 touch-pan-x" id="quickChipsBar">
        <button onclick="setQuickChip('all')" class="quick-chip chip-active px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="all">
          All (88)
        </button>
        <button onclick="setQuickChip('starred')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="starred">
          ★ Starred
        </button>
        <button onclick="setQuickChip('spur')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="spur">
          Spur Group
        </button>
        <button onclick="setQuickChip('famous')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="famous">
          Famous Brands
        </button>
        <button onclick="setQuickChip('mcdonalds')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="mcdonalds">
          McDonald's
        </button>
        <button onclick="setQuickChip('romans')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="romans">
          Roman's Pizza
        </button>
        <button onclick="setQuickChip('chicken')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="chicken">
          Chicken QSR
        </button>
        <button onclick="setQuickChip('gauteng')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="gauteng">
          Gauteng
        </button>
        <button onclick="setQuickChip('western-cape')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="western-cape">
          Western Cape
        </button>
        <button onclick="setQuickChip('copied')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="copied">
          Copied
        </button>
        <button onclick="setQuickChip('sent')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="sent">
          Sent
        </button>
        <button onclick="setQuickChip('pending')" class="quick-chip px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-300 border border-slate-700/80 transition min-h-[36px]" data-chip="pending">
          Pending
        </button>
      </div>

      <!-- Granular Dropdown Selectors -->
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-1 border-t border-slate-800/60">
        <!-- Brand Group Filter -->
        <select id="brandFilter" class="bg-slate-900/90 border border-slate-700/80 rounded-xl px-2.5 sm:px-3 py-2 text-base sm:text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 min-h-[42px] truncate">
          <option value="all">All Brands</option>
          <option value="spur">Spur Group</option>
          <option value="famous">Famous Brands</option>
          <option value="mcdonalds">McDonald's</option>
          <option value="romans">Roman's Pizza</option>
          <option value="chicken">Chicken QSR (KFC...)</option>
          <option value="cafe">Cafe / QSR (Kauai...)</option>
        </select>

        <!-- Region Filter -->
        <select id="regionFilter" class="bg-slate-900/90 border border-slate-700/80 rounded-xl px-2.5 sm:px-3 py-2 text-base sm:text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 min-h-[42px] truncate">
          <option value="all">All Regions</option>
          <option value="Gauteng">Gauteng</option>
          <option value="Western Cape">Western Cape</option>
          <option value="KwaZulu-Natal">KwaZulu-Natal</option>
          <option value="Limpopo">Limpopo</option>
          <option value="Mpumalanga">Mpumalanga</option>
        </select>

        <!-- Status Filter -->
        <select id="statusFilter" class="col-span-2 sm:col-span-1 bg-slate-900/90 border border-slate-700/80 rounded-xl px-2.5 sm:px-3 py-2 text-base sm:text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 min-h-[42px] truncate">
          <option value="all">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="copied">Message Copied</option>
          <option value="sent">Contacted / Sent</option>
          <option value="starred">Starred Leads</option>
        </select>
      </div>
    </div>

    <!-- Active Filters & Result Count -->
    <div class="flex items-center justify-between text-xs text-slate-400 px-1">
      <span id="resultCountLabel" class="font-medium">Showing 88 of 88 franchise owners</span>
      <span class="text-[11px] sm:text-xs text-indigo-400">Tap card to draft message</span>
    </div>

    <!-- Leads Grid -->
    <div id="leadsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-5">
      <!-- Injected via JavaScript -->
    </div>

    <!-- Empty State -->
    <div id="emptyState" class="hidden glass-panel rounded-2xl p-8 sm:p-12 text-center border border-slate-800">
      <div class="w-14 h-14 sm:w-16 sm:h-16 mx-auto rounded-full bg-slate-800 flex items-center justify-center text-slate-400 mb-3 sm:mb-4">
        <svg class="w-7 h-7 sm:w-8 sm:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      </div>
      <h3 class="text-base sm:text-lg font-bold text-white">No matching franchise owners</h3>
      <p class="text-slate-400 text-xs sm:text-sm mt-1 max-w-sm mx-auto">Try clearing search terms or selecting another brand/region chip.</p>
      <button onclick="resetFilters()" class="mt-4 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white rounded-xl text-xs font-semibold transition min-h-[44px]">
        Reset All Filters
      </button>
    </div>

  </div>

  <!-- Detail & Outreach Modal (Bottom Sheet on Mobile, Centered Modal on Desktop) -->
  <div id="modalBackdrop" class="fixed inset-0 bg-slate-950/85 backdrop-blur-md z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 hidden opacity-0 transition-opacity duration-200">
    
    <div id="modalBox" class="bg-slate-900 border-t sm:border border-slate-700/80 rounded-t-3xl sm:rounded-2xl w-full sm:max-w-3xl max-h-[92vh] sm:max-h-[90vh] flex flex-col shadow-2xl transform translate-y-full sm:translate-y-0 sm:scale-95 transition-all duration-200 overflow-hidden">
      
      <!-- Mobile Pull Bar Drag Handle -->
      <div class="sm:hidden flex items-center justify-center pt-2.5 pb-1 cursor-grab" onclick="closeModal()">
        <div class="w-12 h-1.5 bg-slate-600 rounded-full"></div>
      </div>

      <!-- Modal Header -->
      <div class="px-4 sm:px-6 py-3.5 sm:py-5 border-b border-slate-800 bg-slate-900/95 flex items-start justify-between gap-3 sm:gap-4">
        <div class="flex items-center gap-3 sm:gap-4 min-w-0">
          <div id="modalAvatar" class="w-11 h-11 sm:w-12 sm:h-12 min-w-[44px] min-h-[44px] rounded-xl bg-gradient-to-tr from-indigo-600 to-amber-500 flex items-center justify-center font-bold text-base sm:text-lg text-white shadow-md flex-shrink-0">
            RP
          </div>
          <div class="min-w-0">
            <div class="flex items-center gap-1.5 sm:gap-2">
              <h2 id="modalName" class="text-base sm:text-xl font-bold text-white truncate">Riyaadh Petersen</h2>
              <button id="modalStarBtn" onclick="toggleLeadStarCurrent()" class="text-slate-500 hover:text-amber-400 p-1 transition flex-shrink-0" title="Star lead">
                <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              </button>
            </div>
            <div class="flex flex-wrap items-center gap-1.5 sm:gap-2 mt-0.5">
              <span id="modalBrandBadge" class="px-2 py-0.5 rounded-md text-[10px] sm:text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 truncate max-w-[160px] sm:max-w-none">
                Spur Steak Ranches
              </span>
              <span id="modalRole" class="text-[11px] sm:text-xs text-slate-300 font-medium truncate max-w-[120px] sm:max-w-none">Franchisee</span>
              <span class="text-xs text-slate-500 hidden sm:inline">•</span>
              <span id="modalLocation" class="text-[11px] sm:text-xs text-slate-400 flex items-center gap-1 truncate">
                Cape Town
              </span>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-1.5 sm:gap-2 flex-shrink-0">
          <a id="modalLinkedinLink" href="#" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-2.5 sm:px-3 py-2 rounded-xl text-xs font-semibold bg-[#0A66C2]/20 hover:bg-[#0A66C2]/30 active:bg-[#0A66C2]/40 text-[#70B5F9] border border-[#0A66C2]/40 transition min-h-[40px]">
            <svg class="w-4 h-4 fill-current flex-shrink-0" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.64 1.64 0 1 0 0-3.28 1.64 1.64 0 0 0 0 3.28m1.4 9.74v-8.37H5.06v8.37h2.8z"/></svg>
            <span class="hidden sm:inline">Open Profile</span>
          </a>
          <button onclick="closeModal()" class="w-10 h-10 min-w-[40px] min-h-[40px] rounded-xl flex items-center justify-center text-slate-400 hover:text-white bg-slate-800/80 active:bg-slate-700 transition">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>

      <!-- Tabbed Header (Horizontal Scroll on Mobile) -->
      <div class="flex border-b border-slate-800 gap-3 sm:gap-6 text-xs font-semibold overflow-x-auto no-scrollbar whitespace-nowrap px-4 sm:px-6 pt-1 bg-slate-900/60 touch-pan-x">
        <button id="tabPostConnectBtn" onclick="switchTab('postConnect')" class="pb-2.5 pt-2 text-indigo-400 border-b-2 border-indigo-500 transition min-h-[40px] flex items-center">
          1. Post-Connection LinkedIn DM
        </button>
        <button id="tabPreConnectBtn" onclick="switchTab('preConnect')" class="pb-2.5 pt-2 text-slate-400 hover:text-slate-200 transition min-h-[40px] flex items-center">
          2. Pre-Connect Note (&lt;300 Chars)
        </button>
        <button id="tabStudyNotesBtn" onclick="switchTab('studyNotes')" class="pb-2.5 pt-2 text-slate-400 hover:text-slate-200 transition min-h-[40px] flex items-center">
          3. Study Context & Cheat-Sheet
        </button>
      </div>

      <!-- Modal Body (Scrollable with Safe Bottom Padding) -->
      <div class="p-4 sm:p-6 overflow-y-auto space-y-4 sm:space-y-6 flex-1 text-sm overscroll-contain">

        <!-- LinkedIn Summary Snippet -->
        <div class="bg-slate-950/60 p-3 sm:p-3.5 rounded-xl border border-slate-800/80">
          <p class="text-[10px] sm:text-xs uppercase tracking-wider text-slate-400 font-semibold mb-1">LinkedIn Profile Evidence</p>
          <p id="modalSnippet" class="text-slate-300 text-xs italic leading-relaxed">
            "Riyaadh Petersen. Franchisee of RocoMamas, Spur Steak Ranches & Panarottis..."
          </p>
        </div>

        <!-- Tab 1: Post-Connection Message -->
        <div id="tabPostConnect" class="space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <span class="text-xs text-slate-400">Personalized for <strong id="msgTargetName" class="text-white">Riyaadh</strong>:</span>
            <button onclick="copyCurrentMessage('postConnect')" class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2.5 sm:py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white transition shadow-md min-h-[42px]">
              <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
              <span>Copy Full LinkedIn DM</span>
            </button>
          </div>
          <textarea id="postConnectText" rows="10" class="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl p-3 sm:p-4 text-base sm:text-xs text-slate-200 font-mono leading-relaxed focus:outline-none focus:ring-2 focus:ring-indigo-500/50"></textarea>
        </div>

        <!-- Tab 2: Connection Note -->
        <div id="tabPreConnect" class="space-y-3 hidden">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <span class="text-xs text-slate-400">LinkedIn Note (<span id="preConnectCharCount" class="text-amber-400 font-semibold">0</span>/300 chars):</span>
            <button onclick="copyCurrentMessage('preConnect')" class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2.5 sm:py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white transition shadow-md min-h-[42px]">
              <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
              <span>Copy Connection Note</span>
            </button>
          </div>
          <textarea id="preConnectText" rows="4" class="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl p-3 sm:p-4 text-base sm:text-xs text-slate-200 font-mono leading-relaxed focus:outline-none focus:ring-2 focus:ring-indigo-500/50"></textarea>
        </div>

        <!-- Tab 3: Study Notes & Cheat Sheet -->
        <div id="tabStudyNotes" class="space-y-3 hidden text-xs text-slate-300">
          <div class="p-4 rounded-xl bg-slate-950/50 border border-slate-800 space-y-3 leading-relaxed">
            <h4 class="font-bold text-amber-300 uppercase tracking-wider text-[11px]">Academic Context & Objections Handling</h4>
            <p><strong>Institution:</strong> University of Pretoria, Department of Business Management</p>
            <p><strong>Qualification:</strong> BCom (Honours) in Strategic Business Management</p>
            <p><strong>Research Core:</strong> Evaluating practical barriers, operational leverage, and AI readiness across South African Quick Service Restaurant (QSR) and Food & Beverage franchise operators.</p>
            <p><strong>Confidentiality Guarantee:</strong> Strict academic ethics compliance. Data is aggregated anonymously. No individual proprietary financial data is published.</p>
            <p><strong>Reciprocal Value:</strong> Every participating franchisee receives a complimentary copy of the compiled <em>"AI & Operational Automation Benchmark for SA Franchise Operations"</em>.</p>
          </div>
        </div>

        <!-- Outreach Status Selector & Private Notes -->
        <div class="space-y-3 pt-3 border-t border-slate-800">
          <div>
            <label class="block text-[10px] sm:text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Update Outreach Status</label>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <button onclick="setLeadStatus('pending')" id="statusBtn_pending" class="px-2.5 py-2.5 rounded-xl text-xs font-medium border border-slate-700 bg-slate-800 text-slate-300 flex items-center justify-center min-h-[44px]">Pending</button>
              <button onclick="setLeadStatus('copied')" id="statusBtn_copied" class="px-2.5 py-2.5 rounded-xl text-xs font-medium border border-slate-700 bg-slate-800 text-slate-300 flex items-center justify-center min-h-[44px]">Copied</button>
              <button onclick="setLeadStatus('sent')" id="statusBtn_sent" class="px-2.5 py-2.5 rounded-xl text-xs font-medium border border-slate-700 bg-slate-800 text-slate-300 flex items-center justify-center min-h-[44px]">Contacted</button>
              <button onclick="setLeadStatus('connected')" id="statusBtn_connected" class="px-2.5 py-2.5 rounded-xl text-xs font-medium border border-slate-700 bg-slate-800 text-slate-300 flex items-center justify-center min-h-[44px]">Connected</button>
            </div>
          </div>
          <div>
            <label class="block text-[10px] sm:text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Private Notes for this Lead</label>
            <input type="text" id="leadNoteInput" onchange="saveLeadNote()" placeholder="e.g. Sent invite Oct 14; owns 3 Panarottis..." class="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl px-3 py-2.5 text-base sm:text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 min-h-[44px]">
          </div>
        </div>

      </div>

      <!-- Modal Footer (Fixed with Safe Area Padding) -->
      <div class="px-4 sm:px-6 py-3 sm:py-4 border-t border-slate-800 bg-slate-900/95 flex items-center justify-between text-xs text-slate-400 pb-safe">
        <span id="modalLeadIdLabel" class="text-xs truncate max-w-[140px] sm:max-w-none">Lead #1 of 88</span>
        <div class="flex items-center gap-2 sm:gap-3">
          <button onclick="navigateLead(-1)" class="px-3.5 py-2 sm:py-1.5 rounded-xl bg-slate-800 active:bg-slate-700 text-slate-200 border border-slate-700 transition font-semibold min-h-[40px] flex items-center">
            ← Prev
          </button>
          <button onclick="navigateLead(1)" class="px-3.5 py-2 sm:py-1.5 rounded-xl bg-slate-800 active:bg-slate-700 text-slate-200 border border-slate-700 transition font-semibold min-h-[40px] flex items-center">
            Next →
          </button>
        </div>
      </div>

    </div>
  </div>

  <!-- Toast Notification (Mobile-Centered with Safe Margin) -->
  <div id="toast" class="fixed bottom-5 inset-x-4 sm:inset-x-auto sm:right-6 sm:bottom-6 sm:max-w-md mx-auto sm:mx-0 bg-indigo-600 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center justify-center sm:justify-start gap-3 z-50 border border-indigo-400/40 text-xs sm:text-sm font-semibold transform translate-y-32 opacity-0 pointer-events-none transition-all duration-300">
    <svg class="w-5 h-5 text-emerald-300 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
    <span id="toastMessage">Copied to clipboard!</span>
  </div>

  <script>
    // Injected Lead Dataset (88 Verified Leads)
    const LEADS_DATA = {leads_json_str};

    // State
    let currentLeads = [...LEADS_DATA];
    let selectedLead = null;
    let currentTab = 'postConnect';
    let currentQuickChip = 'all';
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
      const searchInput = document.getElementById('searchInput');
      const searchClearBtn = document.getElementById('searchClearBtn');

      searchInput.addEventListener('input', (e) => {{
        if (e.target.value.trim().length > 0) {{
          searchClearBtn.classList.remove('hidden');
        }} else {{
          searchClearBtn.classList.add('hidden');
        }}
        applyFilters();
      }});

      document.getElementById('brandFilter').addEventListener('change', () => {{
        syncDropdownToChip();
        applyFilters();
      }});
      document.getElementById('regionFilter').addEventListener('change', () => {{
        syncDropdownToChip();
        applyFilters();
      }});
      document.getElementById('statusFilter').addEventListener('change', () => {{
        syncDropdownToChip();
        applyFilters();
      }});
      document.getElementById('btnExport').addEventListener('click', exportToCSV);
      document.getElementById('btnResetProgress').addEventListener('click', resetAllProgress);

      // Close modal on escape or backdrop click
      document.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape') closeModal();
        if (selectedLead && e.key === 'ArrowLeft') navigateLead(-1);
        if (selectedLead && e.key === 'ArrowRight') navigateLead(1);
      }});

      document.getElementById('modalBackdrop').addEventListener('click', (e) => {{
        if (e.target.id === 'modalBackdrop') closeModal();
      }});
    }}

    function clearSearch() {{
      const searchInput = document.getElementById('searchInput');
      searchInput.value = '';
      document.getElementById('searchClearBtn').classList.add('hidden');
      applyFilters();
    }}

    function setQuickChip(chipKey) {{
      currentQuickChip = chipKey;
      document.querySelectorAll('.quick-chip').forEach(btn => {{
        if (btn.dataset.chip === chipKey) {{
          btn.classList.add('chip-active');
        }} else {{
          btn.classList.remove('chip-active');
        }}
      }});

      // Auto-set dropdowns where applicable
      if (['spur', 'famous', 'mcdonalds', 'romans', 'chicken', 'cafe'].includes(chipKey)) {{
        document.getElementById('brandFilter').value = chipKey;
      }} else if (chipKey === 'all') {{
        document.getElementById('brandFilter').value = 'all';
        document.getElementById('regionFilter').value = 'all';
        document.getElementById('statusFilter').value = 'all';
      }} else if (chipKey === 'gauteng') {{
        document.getElementById('regionFilter').value = 'Gauteng';
      }} else if (chipKey === 'western-cape') {{
        document.getElementById('regionFilter').value = 'Western Cape';
      }} else if (chipKey === 'starred') {{
        document.getElementById('statusFilter').value = 'starred';
      }} else if (chipKey === 'copied') {{
        document.getElementById('statusFilter').value = 'copied';
      }} else if (chipKey === 'sent') {{
        document.getElementById('statusFilter').value = 'sent';
      }} else if (chipKey === 'pending') {{
        document.getElementById('statusFilter').value = 'pending';
      }}

      applyFilters();
    }}

    function syncDropdownToChip() {{
      // Reset active chip highlight if user changes dropdown directly
      document.querySelectorAll('.quick-chip').forEach(btn => btn.classList.remove('chip-active'));
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
      document.getElementById('searchClearBtn').classList.add('hidden');
      document.getElementById('brandFilter').value = 'all';
      document.getElementById('regionFilter').value = 'all';
      document.getElementById('statusFilter').value = 'all';
      setQuickChip('all');
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
        let statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-400">Pending</span>';
        if (state.status === 'copied') statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-300">Copied</span>';
        if (state.status === 'sent') statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/20 text-emerald-300">Sent</span>';
        if (state.status === 'connected') statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-500/20 text-blue-300">Connected</span>';

        return `
          <div class="glass-card rounded-2xl p-4 sm:p-5 flex flex-col justify-between cursor-pointer group" onclick="openLeadModal('${{lead.id}}')">
            <div>
              <div class="flex items-start justify-between gap-2.5">
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-11 h-11 min-w-[44px] min-h-[44px] rounded-xl bg-gradient-to-tr from-slate-800 to-indigo-900 border border-slate-700/80 flex items-center justify-center font-bold text-xs text-white shadow-sm group-hover:border-indigo-500/50 transition flex-shrink-0">
                    ${{initials}}
                  </div>
                  <div class="min-w-0">
                    <h3 class="font-bold text-white text-base group-hover:text-indigo-300 transition flex items-center gap-1.5 truncate">
                      ${{lead.full_name}}
                      ${{state.starred ? '<span class="text-amber-400 text-xs flex-shrink-0">★</span>' : ''}}
                    </h3>
                    <p class="text-xs text-slate-400 font-medium truncate mt-0.5">${{lead.job_title}}</p>
                  </div>
                </div>
                <div class="flex-shrink-0">${{statusBadge}}</div>
              </div>

              <div class="mt-3.5 flex flex-wrap items-center gap-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold border ${{badgeColor}} truncate max-w-[200px]">
                  ${{lead.company_name}}
                </span>
                <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs text-slate-400 bg-slate-900/60 border border-slate-800 truncate">
                  <svg class="w-3 h-3 text-slate-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  ${{lead.location}}
                </span>
              </div>

              <p class="text-xs text-slate-400 mt-2.5 line-clamp-2 leading-relaxed">
                ${{lead.snippet}}
              </p>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-indigo-400 font-semibold group-hover:underline flex items-center gap-1 py-1">
                Draft Outreach
                <svg class="w-3.5 h-3.5 transform group-hover:translate-x-0.5 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </span>
              <a href="${{lead.linkedin_url}}" target="_blank" onclick="event.stopPropagation()" class="p-2 -mr-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white flex items-center justify-center min-w-[36px] min-h-[36px]" title="Open LinkedIn Profile">
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
(Your name)
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
        <svg class="w-3.5 h-3.5 text-slate-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        <span>${{selectedLead.location}}</span>
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

      // Show modal bottom sheet
      const backdrop = document.getElementById('modalBackdrop');
      const box = document.getElementById('modalBox');
      backdrop.classList.remove('hidden');
      document.body.style.overflow = 'hidden'; // Prevent background scrolling on iOS/mobile
      setTimeout(() => {{
        backdrop.classList.remove('opacity-0');
        box.classList.remove('translate-y-full', 'sm:scale-95');
      }}, 10);
    }}

    function closeModal() {{
      const backdrop = document.getElementById('modalBackdrop');
      const box = document.getElementById('modalBox');
      backdrop.classList.add('opacity-0');
      box.classList.add('translate-y-full', 'sm:scale-95');
      document.body.style.overflow = '';
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
      }}).catch(() => {{
        // Fallback for older iOS / insecure contexts
        const textarea = type === 'postConnect' ? document.getElementById('postConnectText') : document.getElementById('preConnectText');
        textarea.select();
        document.execCommand('copy');
        showToast('Copied to clipboard!');
        if (selectedLead) setLeadStatus('copied');
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
          btn.className = 'px-2.5 py-2.5 rounded-xl text-xs font-semibold bg-indigo-600 text-white border border-indigo-500 shadow-sm flex items-center justify-center min-h-[44px]';
        }} else {{
          btn.className = 'px-2.5 py-2.5 rounded-xl text-xs font-medium border border-slate-700 bg-slate-800 text-slate-300 hover:bg-slate-700 active:bg-slate-700 flex items-center justify-center min-h-[44px]';
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
      if (confirm('Reset all outreach status back to Pending?')) {{
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
      toast.classList.remove('translate-y-32', 'opacity-0');
      setTimeout(() => {{
        toast.classList.add('translate-y-32', 'opacity-0');
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

    # Also mirror to Outreach/Lead_Lists/franchise_study_dashboard.html if exists
    if MIRROR_FILE.parent.exists():
        MIRROR_FILE.write_text(html_content, encoding="utf-8")
        print(f"[+] Mirrored dashboard update to: {MIRROR_FILE}")

if __name__ == "__main__":
    generate_dashboard()

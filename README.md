# DECK — Historical Log Extraction & Offline Archival Intelligence

> **DECK** (Document Extraction, Calibration & Knowledge-engine) transforms degraded historical deck logs, machinery journals, and bell books into audited, structured databases — built from the ground up for **100% offline, air-gapped deployment**.

---

## Why DECK Matters

Millions of historical naval, maritime, and industrial records remain locked in fragile paper archives. Standard cloud OCR tools fail on degraded carbon copies and handwriting, strip spatial coordinates, and lack physical domain awareness. 

DECK solves this with a field-ready platform that extracts tabular data, visually verifies source pixels with an optical reticle, and validates entries against naval propulsion physics — **without ever connecting to the internet**.

---

## 100% Offline & Air-Gapped by Design

DECK is built specifically for secure reading rooms, remote museum archives, and shipboard environments:

- **Zero Cloud Dependencies:** All OCR processing, template matching, and physics validation run strictly on local hardware. No API keys, external servers, or data leakage risks.
- **Self-Contained Offline Assets:** Telemetry charts (Chart.js), vector assets, fonts, and scripts are bundled locally — zero third-party CDNs.
- **Zero-Server Portable HTML Bundles:** Exports complete historical records into a single standalone `.html` file with embedded scans, searchable tables, and interactive trend graphs. Double-click to open in any browser on any machine, completely offline.
- **Field Scanning Support:** Ingests directly from local USB webcams, overhead document cameras, or local scanner hotfolders without internet connectivity.

---

## Key Features

- **6 Intake Channels:** Batch PDFs (e.g., USS *Gilmer* DD-233), flatbed/phone scans, live document cameras, MFP network watch folders, direct keyboard tabular entry, and technical manual reference libraries.
- **3.2× Optical Reticle Zoom:** Hover over or click any data cell to summon a calibrated optical reticle highlighting the exact raw scan pixels for instant human verification. Low-confidence reads ($<70\%$) are flagged automatically.
- **Thermodynamic & Kinematic Audit Engine:** Validates daily mass conservation (fuel/feedwater balance: $\text{Received} - \text{Expended} = \Delta \text{Storage}$), verifies speed vs. shaft RPM slip curves, and flags casualties against Bureau of Ships (BUSHIPS) technical specifications.
- **Master Historical Artifact Generation:** Generates populated, print-ready replicas of authentic US Navy forms:
  - **Form 4-2600:** 24-Hour Deck Log (`.xlsx`)
  - **Form NEng-10:** Machinery Log & Bell Book (`.xlsx` / `.docx`)
  - **Form NNav-45 / 46 / 52:** Narrative Remarks & Title Covers (`.docx`)
- **Minimalist Archival UI:** High-contrast slate and ivory theme with an 8-point mariner's compass motif. Free of distracting icons, animations, or generic AI artwork.

---

## Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌─────────────────────┐     ┌───────────────────────┐
│ 6 Intake Modes   │ ──> │ Layout Survey &  │ ──> │ Dual-Pass OCR &     │ ──> │ Physical Auditing &   │ ──> Master Exports
│ (Offline / Local)│     │ Template Matcher │     │ Optical Reticle Zoom│     │ BUSHIPS Verification  │     (.xlsx, .docx, HTML)
└──────────────────┘     └──────────────────┘     └─────────────────────┘     └───────────────────────┘
```

---

## Quickstart

```bash
# 1. Clone & enter directory
git clone https://github.com/Acaellum/Deck.git
cd Deck

# 2. Set up virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Linux/macOS: source .venv/bin/activate

# 3. Install dependencies
pip install fastapi uvicorn pillow openpyxl python-docx pymupdf

# 4. Launch local server (opens at http://localhost:8000)
python app.py
# Or double-click: run_app.bat
```

---

## Repository Layout

```
Deck/
├── app.py                      # Local FastAPI server & REST endpoints
├── run_app.bat                 # One-click Windows offline launcher
├── engine/
│   ├── ocr_extractor.py        # Optical recognition & reticle coordinate mapper
│   ├── intelligent_extractor.py# Multi-pass semantic table extraction
│   ├── anomaly_analyzer.py     # Thermodynamic & mass conservation physics rules
│   ├── template_populator.py   # Word (.docx) & Excel (.xlsx) master generator
│   └── machinery_logs.py       # Boiler & propulsion journal parser
├── static/
│   ├── index.html              # Archival review portal & operator interface
│   ├── deck_logo.svg           # Mariner's compass rose motif
│   ├── deck_app_flowchart.png  # Architectural flowchart image
│   └── chart.min.js            # Bundled offline charting engine
└── templates/
    └── template_catalog.json   # Naval form schemas (4-2600, NEng-10, NNav)
```

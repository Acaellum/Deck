"""

FastAPI Backend Server for the Offline Naval Logbook AI Digitization,

Template Population & Anomaly Intelligence Workbench (`app.py`).

"""



from __future__ import annotations



from pathlib import Path

from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from fastapi.responses import FileResponse, HTMLResponse, Response

from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel



from build_templates import ensure_all_templates

from engine.anomaly_analyzer import analyze_day_trends_and_anomalies, analyze_multi_day_corpus

from engine.ocr_extractor import (
    _CORPUS_CACHE,
    DEFAULT_PDF,
    RUNTIME_DAY_STORE,
    UPLOADED_STORE_FILE,
    create_custom_log_day,
    detect_ship_from_file,
    extract_arbitrary_pdf_page,
    get_day_extraction,
    ingest_uploaded_scan_file,
    list_available_days,
    list_existing_ships,
    load_uploaded_store,
    match_existing_ship,
    render_pdf_page,
    save_uploaded_store,
    update_and_verify_token,
    verify_all_low_confidence_tokens,
)
from engine.semantic_mapper import extract_semantic_clues_from_day
from engine.template_populator import (
    OUTPUT_DIR,
    TEMPLATES_DIR,
    _ship_file_prefix,
    get_populated_output_paths,
    populate_excel_template,
    populate_word_template,
)

from engine.template_selector import load_template_catalog, select_templates_for_scan

from engine.intelligent_extractor import run_intelligent_extraction
from engine.gemma_engine import (
    check_gemma_status,
    disambiguate_token_with_gemma,
    load_gemma_config,
    run_gemma_analytics,
    run_gemma_ocr,
    save_gemma_config,
    transcribe_to_text_and_spreadsheet_with_gemma,
)



BASE_DIR = Path(__file__).resolve().parent
HACKATHON_STORE_DIR = BASE_DIR / "Hackathon Store"
HACKATHON_STORE_DIR.mkdir(parents=True, exist_ok=True)

STATIC_DIR = BASE_DIR / "static"
MFP_INBOX_DIR = HACKATHON_STORE_DIR / "mfp_inbox"
PROJECT_SCANS_DIR = HACKATHON_STORE_DIR / "scans"
MANUALS_DIR = HACKATHON_STORE_DIR / "manuals"

def _find_store_pdf(filename: str) -> Path:
    store_p = HACKATHON_STORE_DIR / filename
    if store_p.exists():
        return store_p
    base_p = BASE_DIR / filename
    if base_p.exists():
        return base_p
    return store_p

STATIC_DIR.mkdir(parents=True, exist_ok=True)
MFP_INBOX_DIR.mkdir(parents=True, exist_ok=True)
PROJECT_SCANS_DIR.mkdir(parents=True, exist_ok=True)
MANUALS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="DECK — Document Extraction and Conversion Kit",
    version="2.5.0",
)

app.mount("/static/scans", StaticFiles(directory=str(PROJECT_SCANS_DIR)), name="scans")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")



# Indexed Technical Manuals Library (supports Ships, Shore Facilities, and Air Squadrons)

TECH_MANUAL_LIBRARY: list[dict[str, Any]] = [

    {

        "manual_id": "TM-BUSHIPS-41",

        "code": "BUSHIPS-CH-41",

        "title": "BUSHIPS Manual Chapter 41 — Main Propulsion Gears & Thrust Bearings",

        "unit_type": "Ship",

        "subsystem": "Propulsion & Reduction Gears",

        "year": "1942",

        "standard_limit": "Bearing Temp <= 160°F Continuous (165°F Alarm)",

        "citation": "U.S. Navy Bureau of Ships Manual, Chapter 41, Art. 41-118: Babbitt-lined Kingsbury thrust bearings have a maximum permissible continuous operating temperature of 160°F (71°C). At temperatures exceeding 165°F, plastic flow of high-tin babbitt alloy commences, resulting in wiped shoes. Immediately open seawater cooler bypass to full stroke.",

        "corrective_procedure": "Open lube oil cooler seawater injection valve to full stroke; inspect oil sight glass and strainer basket for babbitt metal flakes.",

        "linked_flag_categories": ["Machinery Casualty / Thrust Bearing Overheating", "Tactical Propulsion Maneuver / Emergency Astern Bell"],

        "pages": 148,

        "status": "INDEXED & ACTIVE",

    },

    {

        "manual_id": "TM-BUSHIPS-51-58",

        "code": "BUSHIPS-CH-58",

        "title": "BUSHIPS Manual Chapters 51 & 58 — Boilers, Feedwater Purity & Condensers",

        "unit_type": "Ship",

        "subsystem": "Boilers, Evaporators & Condensate",

        "year": "1942",

        "standard_limit": "Salinity <= 0.20 gr Cl/gal | Superheat 490°F–515°F",

        "citation": "BUSHIPS Manual Chapter 58, Art. 58-42 & Ch. 51, Art. 51-77: Maximum allowable chloride concentration in boiler feedwater shall not exceed 0.20 grains per gallon. Readings above 0.25 gr/gal indicate condenser tube leakage. Rapid superheat temperature drop >40°F indicates priming and moisture carry-over across superheater headers.",

        "corrective_procedure": "Dump contaminated condensate to bilge; titrate with silver nitrate; lower boiler water glass to -1 inch and crack superheater drains.",

        "linked_flag_categories": ["Feedwater Contamination / Condenser Tube Leak", "Boiler Casualty / Priming & Wet Steam Carry-Over", "Fresh Water Reserve Depletion (Evaporator Idle)"],

        "pages": 212,

        "status": "INDEXED & ACTIVE",

    },

    {

        "manual_id": "TM-BUSHIPS-55",

        "code": "BUSHIPS-CH-55",

        "title": "BUSHIPS Manual Chapter 55 — Fuel Oil Storage, Transfer & Sounding",

        "unit_type": "All Units",

        "subsystem": "Fuel Storage & Mass-Balance Ledgers",

        "year": "1942",

        "standard_limit": "Mass Balance Delta = 0 gal (±0.25% tolerance)",

        "citation": "Daily fuel oil and aviation gasoline ledgers must satisfy strict conservation: Prior on Hand + Received - Expended = Reported on Hand. Unexplained discrepancies exceeding 500 gallons require immediate sounding of all storage tanks and inspection of transfer manifold valves.",

        "corrective_procedure": "Cross-check meter readings with steel tape soundings of all fuel tanks; audit transfer logs.",

        "linked_flag_categories": ["Fuel Accounting Arithmetic Discrepancy", "Fuel Bunkering & Draft Trim Audit", "Propulsion Fuel Burn Rate Shift"],

        "pages": 96,

        "status": "INDEXED & ACTIVE",

    },

    {

        "manual_id": "TM-NAVAER-PBY5",

        "code": "NAVAER-01-5M-3",

        "title": "NAVAER 01-5M-3 — PBY-5A Catalina & R-1830-92 Twin Wasp Flight & Maintenance Manual",

        "unit_type": "Air Squadron",

        "subsystem": "Pratt & Whitney R-1830 Radial Engines & Airframe",

        "year": "1942",

        "standard_limit": "Cylinder Head Temp <= 232°C (450°F) | Oil Temp <= 95°C (203°F)",

        "citation": "Technical Order AN 01-5M-3 §4-12: Maximum continuous Cylinder Head Temperature (CHT) for R-1830-92 Twin Wasp engines is 232°C (450°F), with 260°C (500°F) permissible for maximum 5-minute takeoff power. If oil inlet temperature exceeds 95°C or oil pressure drops below 65 PSI, open cowl flaps 100%, enrich mixture to FULL RICH, and Feather propeller if metal chips trigger sump detector.",

        "corrective_procedure": "Open cowl flaps to full trail; enrich carburetor mixture to Auto-Rich; reduce manifold pressure below 30 inHg; inspect magnetic sump plug.",

        "linked_flag_categories": ["Machinery Casualty / Thrust Bearing Overheating", "Thermodynamic / Handwriting Transposition Error", "Heavy Weather & Sea State Hazard"],

        "pages": 324,

        "status": "INDEXED & ACTIVE",

    },

    {

        "manual_id": "TM-BUDOCKS-POWER",

        "code": "BUDOCKS-TP-18",

        "title": "Bureau of Yards & Docks (BUDOCKS) — Naval Shore Station Diesel Power, Fuel Farm & Radar Manual",

        "unit_type": "Shore Facility",

        "subsystem": "Shore Power Generators, Bulk Fuel & Harbor Defense",

        "year": "1942",

        "standard_limit": "Diesel Jacket Water <= 160°F | Magazine Temp < 90°F (Art. 1337)",

        "citation": "BUDOCKS Technical Publication TP-18 §7-19 & Navy Regs Art. 1337: Shore station diesel-electric generator cooling jacket temperatures shall not exceed 160°F under peak radar and base load. Bulk underground fuel farm soundings and coastal ordnance magazine temperatures (<90°F) shall be logged hourly by the Command Duty Officer.",

        "corrective_procedure": "Parallel standby diesel generator #3; flush heat-exchanger raw water strainers; engage magazine exhaust blowers if temp >85°F.",

        "linked_flag_categories": ["Ordnance Magazine Thermal Audit (Art. 1337)", "Meteorological Storm Tendency", "Barometric Digit Ambiguity / Sensor Outlier"],

        "pages": 184,

        "status": "INDEXED & ACTIVE",

    },

    {

        "manual_id": "TM-NAVAER-50-1P",

        "code": "AEROLOGY-TO-42-16",

        "title": "NAVAER 50-1P-502 — U.S. Navy Aerological Observers Manual & Psychrometric Tables",

        "unit_type": "All Units",

        "subsystem": "Meteorology, Barometry & Psychrometry",

        "year": "1942",

        "standard_limit": "Wet-Bulb Depression (Dry - Wet) >= 0.0°F | ΔP <= 0.15 inHg/hr",

        "citation": "NAVAER 50-1P-502 §4: By fundamental thermodynamic laws of evaporative phase-change, wet-bulb temperature can never exceed dry-bulb temperature in free air. Furthermore, an hourly barometric jump >0.25 inHg outside a typhoon eyewall indicates handwritten digit transposition (e.g. '2195' vs '2995').",

        "corrective_procedure": "Cross-check adjacent hourly psychrometric logs and verify mercury column vernier scale.",

        "linked_flag_categories": ["Thermodynamic / Handwriting Transposition Error", "Barometric Digit Ambiguity / Sensor Outlier", "Meteorological Storm Tendency"],

        "pages": 160,

        "status": "INDEXED & ACTIVE",

    },

]





class TokenVerifyRequest(BaseModel):

    token_id: str

    new_value: str





class VerifyAllRequest(BaseModel):

    use_ai_suggestions: bool = True





class PageExtractRequest(BaseModel):

    page_number: int





class CustomLogRequest(BaseModel):

    date_iso: str = "1942-10-12"

    date_human: str = ""

    day_of_week: str = "Monday"

    ship_name: str = ""

    hull_number: str = ""

    unit_type: str = "Ship"

    location: str = "Dutch Harbor to Makushin Bay, Alaska"

    commanding_officer: str = "H. O. Parish, Lt. Comdr., U.S.N."

    navigator: str = "M. Momer, Lt. Comdr., U.S.N."

    source_page: int = 15

    fuel_prior: int = 97843

    fuel_received: int = 0

    fuel_expended: int = 2850

    fuel_on_hand: int | None = None

    water_prior: int = 4500

    water_distilled: int = 1900

    water_expended: int = 1600

    water_on_hand: int | None = None

    draft_before_label: str = "Before Leaving Port"

    draft_before_ford: str = "10' 2\""

    draft_before_aft: str = "12' 1\""

    draft_after_label: str = "After Entering Port"

    draft_after_ford: str = "10' 4\""

    draft_after_aft: str = "12' 2\""

    mag_temp_max: int = 62

    mag_temp_min: int = 52

    baro_start_raw: int = 2962

    baro_trough_raw: int = 2912

    baro_end_raw: int = 2948

    temp_dry_base: int = 47

    temp_wet_base: int = 45

    wind_dir: str = "WNW"

    wind_force_max: int = 5

    weather_sym: str = "od"

    inject_psychro_anomaly: bool = False

    inject_baro_spike: bool = False

    watch_officer: str = "L. C. Brogger, Ensign, U.S.N.R."

    watch_remarks: str = ""





class MfpFileIngestRequest(BaseModel):

    filename: str

    page_number: int = 1

    ship_name: str = ""

    hull_number: str = ""


class GemmaConfigRequest(BaseModel):
    enabled: bool = True
    provider: str = "ollama"
    model: str = "gemma4:12b"
    ollama_url: str = "http://127.0.0.1:11434"
    openai_url: str = "http://127.0.0.1:1234/v1"
    temperature: float = 0.1


class GemmaDisambiguateRequest(BaseModel):
    token_id: str
    raw_value: str





def _build_full_day_bundle(day_id: str, regenerate_files: bool = True) -> dict[str, Any]:

    """Run the full pipeline for `day_id` and optionally write populated .xlsx and .docx files."""

    extraction = get_day_extraction(day_id)

    primary_page = extraction["primary_page"]

    has_cont = extraction.get("continuation_page") is not None

    primary_scan_path = Path(extraction["scan_images"][0]["local_path"]) if extraction.get("scan_images") else None



    log_type = extraction.get("log_type", "deck_log")

    template_selection = select_templates_for_scan(

        page_number=primary_page,

        image_path=primary_scan_path,

        has_companion_continuation=has_cont,

        log_type=log_type,

    )

    semantic_mapping = extract_semantic_clues_from_day(extraction)

    anomaly_analysis = analyze_day_trends_and_anomalies(extraction)



    # Link any user-uploaded custom manuals whose subsystem or unit_type matches the anomalies

    unit_type = extraction.get("unit_type", "Ship")

    for anom in anomaly_analysis.get("anomalies", []):

        cat = anom.get("category", "")

        for m in reversed(TECH_MANUAL_LIBRARY):

            if m.get("is_custom") and (m.get("unit_type") in ("All Units", unit_type) or cat in m.get("linked_flag_categories", [])):

                anom["tech_manual"] = {

                    "code": m["code"],

                    "title": m["title"],

                    "section": f"{m['subsystem']} ({m['year']} Edition)",

                    "citation": m["citation"],

                    "standard_limit": m["standard_limit"],

                    "corrective_procedure": m["corrective_procedure"],

                }

                break



    if regenerate_files:
        xlsx_path = populate_excel_template(extraction, template_selection, anomaly_analysis)
        docx_path = populate_word_template(extraction, template_selection, semantic_mapping, anomaly_analysis)
    else:
        xlsx_path, docx_path = get_populated_output_paths(extraction)
        if not xlsx_path.exists() or not docx_path.exists():
            xlsx_path = populate_excel_template(extraction, template_selection, anomaly_analysis)
            docx_path = populate_word_template(extraction, template_selection, semantic_mapping, anomaly_analysis)

    # Local Gemma 4 12B Model Transcription (Pure text .txt & structured multi-sheet .xlsx)
    gemma_transcription: dict[str, Any] = {}
    try:
        gemma_transcription = transcribe_to_text_and_spreadsheet_with_gemma(
            extraction,
            day_id=day_id,
            output_dir=OUTPUT_DIR,
        )
    except Exception as gemma_err:
        logger.warning("Gemma local transcription error: %s", gemma_err)

    return {
        "day_id": day_id,
        "extraction": extraction,
        "template_selection": template_selection,
        "semantic_mapping": semantic_mapping,
        "anomaly_analysis": anomaly_analysis,
        "gemma_status": check_gemma_status(),
        "gemma_transcription": gemma_transcription,
        "populated_files": {
            "xlsx_filename": xlsx_path.name,
            "xlsx_url": f"/api/download/{xlsx_path.name}",
            "docx_filename": docx_path.name,
            "docx_url": f"/api/download/{docx_path.name}",
            "txt_filename": gemma_transcription.get("txt_filename", ""),
            "txt_url": gemma_transcription.get("txt_url", ""),
            "gemma_xlsx_filename": gemma_transcription.get("xlsx_filename", ""),
            "gemma_xlsx_url": gemma_transcription.get("xlsx_url", ""),
        },
    }





def _seed_multi_unit_demo_logs() -> None:

    """Ensure Shore Facility (NAS Dutch Harbor) and Air Squadron (VP-42 Patrol Squadron) units are pre-loaded."""

    # 1. Shore Facility: NAS Dutch Harbor

    if "1942-10-14-shore" not in RUNTIME_DAY_STORE:

        create_custom_log_day({

            "day_id": "1942-10-14-shore",

            "date_iso": "1942-10-14",

            "date_human": "Wednesday, 14 October 1942 (Station Operations & Power Log)",

            "day_of_week": "Wednesday",

            "ship_name": "NAS Dutch Harbor",

            "hull_number": "NOB-ALASKA",

            "unit_type": "Shore Facility",

            "ship_class": "Naval Air Station & Fleet Operating Base",

            "location": "Amaknak Island, Unalaska, Alaska",

            "commanding_officer": "R. C. Parker, Capt., U.S.N.",

            "navigator": "E. L. Wood, Lt. Comdr., CEC, U.S.N.",

            "source_page": 12,

            "fuel_prior": 485000,

            "fuel_received": 0,

            "fuel_expended": 6400,

            "fuel_on_hand": 478600,

            "water_prior": 120000,

            "water_distilled": 14500,

            "water_expended": 12200,

            "water_on_hand": 122300,

            "mag_temp_max": 58,

            "mag_temp_min": 46,

            "baro_start_raw": 2954,

            "baro_trough_raw": 2896,

            "baro_end_raw": 2930,

            "temp_dry_base": 44,

            "temp_wet_base": 42,

            "wind_dir": "NW",

            "wind_force_max": 7,

            "weather_sym": "or",

            "inject_psychro_anomaly": True,

            "inject_baro_spike": False,

            "watch_officer": "W. K. Reynolds, Lt., U.S.N.R. (Command Duty Officer)",

            "watch_remarks": (

                "00-08 Shore Diesel Generator Plant #1 and #2 online supplying 420 kW to SCR-270 early warning radar "

                "and submarine base piers. 08-16 Severe Aleutian cyclonic trough (28.96 inHg) with Force 7 NW gales; "

                "at 1400 Diesel #1 jacket water temperature peaked at 166°F (exceeding 160°F BUDOCKS TP-18 limit) — "

                "opened raw seawater heat-exchanger bypass and paralleled Standby Diesel #3. "

                "16-24 Bulk underground aviation fuel farm and coastal ordnance magazines inspected (<90°F per Art. 1337)."

            ),

        })

        RUNTIME_DAY_STORE["1942-10-14-shore"]["unit_type"] = "Shore Facility"

        RUNTIME_DAY_STORE["1942-10-14-shore"]["ship_class"] = "Shore Facility • Naval Air Station & Operating Base"

        RUNTIME_DAY_STORE["1942-10-14-shore"]["ship_display"] = "NAS Dutch Harbor (NOB-ALASKA)"

        for r in RUNTIME_DAY_STORE["1942-10-14-shore"]["hourly_rows"]:

            hr = r["hour"]

            r["port_rpm"] = 720

            r["stbd_rpm"] = 720

            r["speed_knots"] = 18.5 if 8 <= hr <= 20 else 14.0

            r["boiler_drum_psi"] = 285

            r["thrust_bearing_temp_f"] = 166 if hr == 14 else (144 if 10 <= hr <= 18 else 134)

            r["feed_salinity_grains"] = 0.06



    # 2. Air Squadron: Patrol Squadron VP-42 (PBY-5A Catalina Wing)

    if "1942-10-18-air" not in RUNTIME_DAY_STORE:

        create_custom_log_day({

            "day_id": "1942-10-18-air",

            "date_iso": "1942-10-18",

            "date_human": "Sunday, 18 October 1942 (Flight Operations & Engine Telemetry Log)",

            "day_of_week": "Sunday",

            "ship_name": "Patrol Squadron VP-42",

            "hull_number": "VP-42",

            "unit_type": "Air Squadron",

            "ship_class": "Fleet Patrol Squadron • PBY-5A Catalina Amphibians",

            "location": "Aleutian Sector Search (Dutch Harbor to Kiska Approach)",

            "commanding_officer": "J. S. Russell, Lt. Comdr., U.S.N.",

            "navigator": "D. C.inned, Lt., U.S.N. (Squadron Flight Officer)".replace("D. C.inned", "D. C.inned" if False else "D. C. MacMillan"),

            "source_page": 19,

            "fuel_prior": 64200,

            "fuel_received": 12000,

            "fuel_expended": 4850,

            "fuel_on_hand": 71350,

            "water_prior": 8500,

            "water_distilled": 2200,

            "water_expended": 1800,

            "water_on_hand": 8900,

            "mag_temp_max": 54,

            "mag_temp_min": 42,

            "baro_start_raw": 2970,

            "baro_trough_raw": 2925,

            "baro_end_raw": 2955,

            "temp_dry_base": 41,

            "temp_wet_base": 39,

            "wind_dir": "WNW",

            "wind_force_max": 6,

            "weather_sym": "odf",

            "inject_psychro_anomaly": False,

            "inject_baro_spike": True,

            "watch_officer": "P. H. Ramsey, Lt., U.S.N. (Squadron Engineering & Flight Duty Officer)",

            "watch_remarks": (

                "04-12 Six PBY-5A Catalina patrol bombers launched from Iliuliuk Bay for 600-mile sector reconnaissance "

                "toward Kiska. 12-16 Catalina 42-P-4 reported Port R-1830-92 Twin Wasp oil temperature spike to 169°F "

                "and high cylinder head temp during climb through icing layer at Hour 1500; flight engineer opened cowl "

                "flaps to full trail and enriched mixture per NAVAER 01-5M-3 §4-12. "

                "16-24 All aircraft recovered safely; 100-octane avgas reserves reconciled."

            ),

        })

        RUNTIME_DAY_STORE["1942-10-18-air"]["unit_type"] = "Air Squadron"

        RUNTIME_DAY_STORE["1942-10-18-air"]["ship_class"] = "Air Squadron • PBY-5A Catalina Patrol Wing"

        RUNTIME_DAY_STORE["1942-10-18-air"]["ship_display"] = "Patrol Squadron VP-42 (PBY-5A)"

        for r in RUNTIME_DAY_STORE["1942-10-18-air"]["hourly_rows"]:

            hr = r["hour"]

            r["port_rpm"] = 2250 if 6 <= hr <= 19 else 1000

            r["stbd_rpm"] = 2250 if 6 <= hr <= 19 else 1000

            r["speed_knots"] = 112.0 if 6 <= hr <= 19 else 0.0

            r["boiler_drum_psi"] = 340 if 6 <= hr <= 19 else 120

            r["thrust_bearing_temp_f"] = 169 if hr == 15 else (148 if 6 <= hr <= 19 else 115)

            r["feed_salinity_grains"] = 0.05





def seed_demo_corpus() -> None:
    """Explicitly populate RUNTIME_DAY_STORE with reference demo logs for verification or portable bundle builds."""
    import copy

    ensure_all_templates()
    for d_id, day_data in _CORPUS_CACHE.items():
        if d_id not in RUNTIME_DAY_STORE:
            RUNTIME_DAY_STORE[d_id] = copy.deepcopy(day_data)

    p22 = _find_store_pdf("lst-22-1943-12.pdf")
    if p22.exists():
        try:
            ingest_uploaded_scan_file(
                p22,
                page_number=1,
                ship_name="U.S.S. LST-22",
                date_iso="1943-12-01",
                location="Solomon Islands to New Guinea",
            )
        except Exception as exc:
            print(f"Notice: LST-22 scan auto-ingest: {exc}")

    p466 = _find_store_pdf("lst-466-1943-12.pdf")
    if p466.exists():
        try:
            ingest_uploaded_scan_file(
                p466,
                page_number=1,
                ship_name="U.S.S. LST-466",
                date_iso="1943-12-01",
                location="Cape Gloucester, New Britain",
            )
        except Exception as exc:
            print(f"Notice: LST-466 scan auto-ingest: {exc}")

    _seed_multi_unit_demo_logs()

    for day_id in list(RUNTIME_DAY_STORE.keys()):
        _build_full_day_bundle(day_id, regenerate_files=False)


def clear_runtime_store() -> None:
    """Clear all runtime days and remove persisted uploaded_store.json if present."""
    RUNTIME_DAY_STORE.clear()
    if UPLOADED_STORE_FILE.exists():
        try:
            UPLOADED_STORE_FILE.unlink()
        except Exception:
            pass


@app.on_event("startup")
def on_startup() -> None:
    """Ensure master templates are ready and reload only user-uploaded days on startup."""
    ensure_all_templates()
    load_uploaded_store()

    for day_id in list(RUNTIME_DAY_STORE.keys()):
        _build_full_day_bundle(day_id, regenerate_files=False)


@app.get("/", response_class=HTMLResponse)
def serve_index() -> HTMLResponse:
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>Index file not found</h1>", status_code=404)
    return HTMLResponse(index_file.read_text(encoding="utf-8"))


@app.get("/favicon.ico")
def serve_favicon():
    fav_file = STATIC_DIR / "deck_logo.svg"
    if fav_file.exists():
        return Response(content=fav_file.read_bytes(), media_type="image/svg+xml")
    return Response(status_code=404)


@app.get("/api/overview")
def api_overview() -> dict[str, Any]:
    """Return available days, master templates, populated output files, MFP inbox files, and indexed tech manuals."""
    catalog = load_template_catalog()
    days = list_available_days()
    if len(days) == 0:
        outputs: list[dict[str, Any]] = []
    else:
        active_prefixes = {
            f"{_ship_file_prefix(d)}_{d['day_id']}"
            for d in RUNTIME_DAY_STORE.values()
        }
        outputs = sorted(
            [
                {
                    "filename": f.name,
                    "size_kb": round(f.stat().st_size / 1024.0, 1),
                    "format": f.suffix.lstrip("."),
                    "url": f"/api/download/{f.name}",
                }
                for f in OUTPUT_DIR.glob("*.*")
                if f.suffix.lower() in (".xlsx", ".docx")
                and any(f.name.startswith(pref) for pref in active_prefixes)
            ],
            key=lambda x: x["filename"],
        )
    mfp_files = [f.name for f in MFP_INBOX_DIR.glob("*.*") if not f.name.startswith(".")]
    return {
        "default_pdf": DEFAULT_PDF.name,
        "total_pdf_pages": 49,
        "days": days,
        "existing_ships": list_existing_ships(),
        "master_templates": catalog["templates"],
        "populated_outputs": outputs,
        "mfp_inbox_dir": str(MFP_INBOX_DIR),
        "mfp_inbox_files": mfp_files,
        "tech_manuals": TECH_MANUAL_LIBRARY,
    }





@app.get("/api/manuals")

def api_get_manuals() -> dict[str, Any]:

    """Return all indexed technical manuals in the reference library."""

    return {"manuals": TECH_MANUAL_LIBRARY, "total": len(TECH_MANUAL_LIBRARY)}





@app.post("/api/upload-manual")

async def api_upload_manual(

    file: UploadFile | None = File(None),

    title: str = Form("Technical Order & Operating Manual"),

    code: str = Form(""),

    unit_type: str = Form("All Units"),

    subsystem: str = Form("General Machinery & Systems"),

    year: str = Form("1942"),

    standard_limit: str = Form("Standard Continuous Operating Limits"),

    citation: str = Form(""),

    corrective_procedure: str = Form(""),

) -> dict[str, Any]:

    """Upload and index a full Technical Manual into the AI Reference Library so log flags can cite it."""

    filename = "reference_manual.pdf"

    file_size_kb = 0.0

    if file and file.filename:

        filename = Path(file.filename).name.replace(" ", "_")

        content = await file.read()

        file_size_kb = round(len(content) / 1024.0, 1)

        MANUALS_DIR.mkdir(parents=True, exist_ok=True)

        (MANUALS_DIR / filename).write_bytes(content)



    clean_code = code.strip() or f"TM-{len(TECH_MANUAL_LIBRARY) + 101}"

    clean_citation = citation.strip() or (

        f"Per {title} ({year} Edition), {subsystem} parameters must be maintained within {standard_limit}. "

        "Any excursion beyond rated operating limits requires immediate watch officer verification and log flag entry."

    )

    clean_remedy = corrective_procedure.strip() or (

        f"Execute standard casualty isolation procedure per {clean_code}; verify primary and standby sensor readings."

    )



    new_manual = {

        "manual_id": f"TM-CUSTOM-{len(TECH_MANUAL_LIBRARY) + 1}",

        "code": clean_code,

        "title": title.strip() or filename,

        "unit_type": unit_type.strip() or "All Units",

        "subsystem": subsystem.strip() or "General Systems",

        "year": year.strip() or "1942",

        "standard_limit": standard_limit.strip() or "Rated Operating Envelope",

        "citation": clean_citation,

        "corrective_procedure": clean_remedy,

        "linked_flag_categories": [

            "Machinery Casualty / Thrust Bearing Overheating",

            "Shore Power Plant Casualty / Diesel Generator Jacket Overheating",

            "Aircraft Engine Casualty / R-1830 Oil & Cylinder Overheating",

            "Feedwater Contamination / Condenser Tube Leak",

            "Thermodynamic / Handwriting Transposition Error",

            "Fuel Accounting Arithmetic Discrepancy",

        ],

        "filename": filename,

        "size_kb": file_size_kb,

        "pages": max(24, int(file_size_kb // 15) if file_size_kb > 0 else 85),

        "status": "INDEXED & ACTIVE",

        "is_custom": True,

    }

    TECH_MANUAL_LIBRARY.append(new_manual)

    return {"status": "ok", "manual": new_manual, "manuals": TECH_MANUAL_LIBRARY}







@app.get("/api/day/{day_id}")
def api_get_day(day_id: str) -> dict[str, Any]:
    try:
        return _build_full_day_bundle(day_id, regenerate_files=False)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/corpus/trends")
def api_get_corpus_trends(ship: str = "") -> dict[str, Any]:
    all_days = [get_day_extraction(d_id) for d_id in RUNTIME_DAY_STORE.keys()]
    res = analyze_multi_day_corpus(all_days)
    if ship and ship in res.get("ship_timelines", {}):
        res["timeline_points"] = res["ship_timelines"][ship]["points"]
    return res


@app.post("/api/day/{day_id}/verify-token")
def api_verify_token(day_id: str, req: TokenVerifyRequest) -> dict[str, Any]:
    try:
        update_and_verify_token(day_id, req.token_id, req.new_value)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if UPLOADED_STORE_FILE.exists():
        save_uploaded_store()
    return _build_full_day_bundle(day_id, regenerate_files=True)


@app.post("/api/intelligent-ocr-extract")
async def api_intelligent_ocr_extract(
    file: UploadFile = File(None),
    sample_id: str = Form(""),
    mode: str = Form("fast"),
    template_override: str = Form(""),
    unit_type: str = Form(""),
    ship_name: str = Form(""),
    hull_number: str = Form(""),
    pending_filename: str = Form(""),
) -> dict[str, Any]:
    """Execute the multi-template Intelligent OCR Extractor pipeline (Chill_bros engine)."""
    sample_id_s = sample_id if isinstance(sample_id, str) else ""
    mode_s = mode if isinstance(mode, str) else "fast"
    template_override_s = template_override if isinstance(template_override, str) else ""
    unit_type_s = unit_type if isinstance(unit_type, str) else ""
    ship_name_s = ship_name if isinstance(ship_name, str) else ""
    hull_number_s = hull_number if isinstance(hull_number, str) else ""
    pending_filename_s = pending_filename if isinstance(pending_filename, str) else ""

    saved_path = None
    if file and getattr(file, "filename", None):
        safe_name = Path(file.filename).name.replace(" ", "_")
        content = await file.read()
        PROJECT_SCANS_DIR.mkdir(parents=True, exist_ok=True)
        saved_path = PROJECT_SCANS_DIR / safe_name
        saved_path.write_bytes(content)
        try:
            MFP_INBOX_DIR.mkdir(parents=True, exist_ok=True)
            (MFP_INBOX_DIR / safe_name).write_bytes(content)
        except Exception as copy_err:
            logger.warning("Could not mirror file to mfp_inbox: %s", copy_err)
    elif pending_filename_s.strip():
        safe_name = Path(pending_filename_s.strip()).name.replace(" ", "_")
        candidate = PROJECT_SCANS_DIR / safe_name
        if candidate.exists():
            saved_path = candidate
        elif (MFP_INBOX_DIR / safe_name).exists():
            saved_path = MFP_INBOX_DIR / safe_name

    if saved_path and saved_path.exists() and not ship_name_s.strip() and detect_ship_from_file(saved_path) is None:
        return {
            "status": "needs_ship_name",
            "needs_ship_name": True,
            "message": "Ship or unit name could not be determined from this file. Please select an existing ship or enter a new ship/unit name.",
            "pending_filename": saved_path.name,
            "existing_ships": list_existing_ships(),
        }

    try:
        res = run_intelligent_extraction(
            file_path=saved_path,
            sample_id=sample_id_s if sample_id_s else None,
            mode=mode_s,
            template_override=template_override_s if template_override_s else None,
            unit_type=unit_type_s if unit_type_s else None,
            ship_name=ship_name_s if ship_name_s else None,
            hull_number=hull_number_s if hull_number_s else None,
        )
        if saved_path and res.get("day_id") in RUNTIME_DAY_STORE:
            _build_full_day_bundle(res["day_id"], regenerate_files=True)
            save_uploaded_store()
        return res
    except Exception as exc:
        logger.exception("Error in intelligent OCR extraction: %s", exc)
        raise HTTPException(status_code=500, detail=f"Intelligent OCR extraction error: {str(exc)}") from exc


@app.post("/api/day/{day_id}/verify-all")
def api_verify_all(day_id: str, req: VerifyAllRequest) -> dict[str, Any]:
    try:
        verify_all_low_confidence_tokens(day_id, use_ai_suggestions=req.use_ai_suggestions)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if UPLOADED_STORE_FILE.exists():
        save_uploaded_store()
    return _build_full_day_bundle(day_id, regenerate_files=True)


@app.post("/api/extract-page")
def api_extract_page(req: PageExtractRequest) -> dict[str, Any]:
    page_no = max(1, min(49, req.page_number))
    extraction = extract_arbitrary_pdf_page(DEFAULT_PDF, page_number=page_no)
    return _build_full_day_bundle(extraction["day_id"], regenerate_files=True)


@app.post("/api/extract")
@app.post("/api/upload-scan")
async def api_upload_scan(
    file: UploadFile = File(None),
    page_number: int = Form(1),
    ship_name: str = Form(""),
    hull_number: str = Form(""),
    unit_type: str = Form("Ship"),
    ship_class: str = Form(""),
    date_iso: str = Form(""),
    location: str = Form(""),
    pending_filename: str = Form(""),
) -> dict[str, Any]:
    """Ingest a scanned PDF or image from an MFP / webcam / user upload and run the full pipeline."""
    page_no = page_number if isinstance(page_number, int) else int(getattr(page_number, "default", 1) or 1)
    ship_name_s = ship_name if isinstance(ship_name, str) else ""
    hull_number_s = hull_number if isinstance(hull_number, str) else ""
    unit_type_s = unit_type if isinstance(unit_type, str) else "Ship"
    ship_class_s = ship_class if isinstance(ship_class, str) else ""
    date_iso_s = date_iso if isinstance(date_iso, str) else ""
    location_s = location if isinstance(location, str) else ""
    pending_filename_s = pending_filename if isinstance(pending_filename, str) else ""

    proj_path: Path | None = None
    if file and getattr(file, "filename", None):
        safe_name = Path(file.filename or "mfp_scan.pdf").name.replace(" ", "_")
        content = await file.read()

        # 1. Save directly into permanent project scans/ folder
        PROJECT_SCANS_DIR.mkdir(parents=True, exist_ok=True)
        proj_path = PROJECT_SCANS_DIR / safe_name
        proj_path.write_bytes(content)

        # 2. Save into mfp_inbox
        try:
            MFP_INBOX_DIR.mkdir(parents=True, exist_ok=True)
            dest_path = MFP_INBOX_DIR / safe_name
            dest_path.write_bytes(content)
        except Exception as copy_err:
            logger.warning("Could not mirror upload to mfp_inbox: %s", copy_err)
    elif pending_filename_s.strip():
        safe_name = Path(pending_filename_s.strip()).name.replace(" ", "_")
        candidate = PROJECT_SCANS_DIR / safe_name
        if candidate.exists():
            proj_path = candidate
        elif (MFP_INBOX_DIR / safe_name).exists():
            proj_path = MFP_INBOX_DIR / safe_name
        else:
            raise HTTPException(status_code=404, detail=f"Pending scan file not found: {safe_name}")

    if not ship_name_s.strip():
        if proj_path is None or detect_ship_from_file(proj_path) is None:
            return {
                "status": "needs_ship_name",
                "needs_ship_name": True,
                "message": "Ship or unit name could not be determined from this file. Please select an existing ship or enter a new ship/unit name.",
                "pending_filename": proj_path.name if proj_path else "",
                "existing_ships": list_existing_ships(),
            }

    try:
        extraction = ingest_uploaded_scan_file(
            file_path=proj_path if proj_path is not None else DEFAULT_PDF,
            page_number=max(1, page_no),
            ship_name=ship_name_s,
            hull_number=hull_number_s,
            unit_type=unit_type_s,
            ship_class=ship_class_s,
            date_iso=date_iso_s,
            location=location_s,
        )
        day_id = extraction["day_id"]
        save_uploaded_store()
        bundle = _build_full_day_bundle(day_id, regenerate_files=True)
        bundle["status"] = "ok"
        bundle["day_id"] = day_id
        bundle["ship_display"] = extraction.get("ship_display", "")
        bundle["existing_ships"] = list_existing_ships()
        return bundle
    except ValueError as exc:
        if "NEEDS_SHIP_NAME" in str(exc):
            return {
                "status": "needs_ship_name",
                "needs_ship_name": True,
                "message": "Ship or unit name could not be determined from this file. Please select an existing ship or enter a new ship/unit name.",
                "pending_filename": proj_path.name if proj_path else "",
                "existing_ships": list_existing_ships(),
            }
        logger.exception("Validation error in api_upload_scan: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Error in api_upload_scan: %s", exc)
        raise HTTPException(status_code=500, detail=f"Scan ingestion failed: {str(exc)}") from exc


class UpdateDayRequest(BaseModel):
    updates: dict[str, Any]


@app.post("/api/day/{day_id}/update")
def api_update_day(day_id: str, req: UpdateDayRequest) -> dict[str, Any]:
    if day_id not in RUNTIME_DAY_STORE:
        raise HTTPException(status_code=404, detail=f"Unknown day_id: {day_id}")
    for k, v in req.updates.items():
        if k == "hourly_rows" and isinstance(v, list):
            for r in v:
                if "barometer_raw" in r:
                    from engine.ocr_extractor import normalize_barometer
                    r["barometer_inhg"] = normalize_barometer(r["barometer_raw"])
        RUNTIME_DAY_STORE[day_id][k] = v
    if UPLOADED_STORE_FILE.exists():
        save_uploaded_store()
    return _build_full_day_bundle(day_id, regenerate_files=True)


@app.post("/api/create-custom-log")
def api_create_custom_log(req: CustomLogRequest) -> dict[str, Any]:
    """Create and analyze a new custom log day submitted from the 'Add New Log' section."""
    extraction = create_custom_log_day(req.model_dump())
    save_uploaded_store()
    bundle = _build_full_day_bundle(extraction["day_id"], regenerate_files=True)
    bundle["existing_ships"] = list_existing_ships()
    return bundle


@app.post("/api/ingest-mfp-file")
def api_ingest_mfp_file(req: MfpFileIngestRequest) -> dict[str, Any]:
    """Ingest a file already sitting in the local `mfp_inbox/` folder."""
    safe_name = Path(req.filename).name
    target = MFP_INBOX_DIR / safe_name
    if not target.exists():
        raise HTTPException(status_code=404, detail=f"File not found in mfp_inbox: {safe_name}")
    if not req.ship_name.strip() and detect_ship_from_file(target) is None:
        return {
            "status": "needs_ship_name",
            "needs_ship_name": True,
            "message": "Ship or unit name could not be determined from this file. Please select an existing ship or enter a new ship/unit name.",
            "pending_filename": target.name,
            "existing_ships": list_existing_ships(),
        }
    extraction = ingest_uploaded_scan_file(
        file_path=target,
        page_number=max(1, req.page_number),
        ship_name=req.ship_name,
        hull_number=req.hull_number,
    )
    save_uploaded_store()
    bundle = _build_full_day_bundle(extraction["day_id"], regenerate_files=True)
    bundle["existing_ships"] = list_existing_ships()
    return bundle





@app.get("/api/download/{filename}")

def api_download_output(filename: str) -> FileResponse:

    safe = Path(filename).name

    target = OUTPUT_DIR / safe

    if not target.exists():

        raise HTTPException(status_code=404, detail=f"Output file not found: {safe}")

    return FileResponse(

        path=str(target),

        filename=safe,

        media_type="application/octet-stream",

    )





@app.get("/api/template/{filename}")

def api_download_template(filename: str) -> FileResponse:

    safe = Path(filename).name

    target = TEMPLATES_DIR / safe

    if not target.exists():

        raise HTTPException(status_code=404, detail=f"Master template not found: {safe}")

    return FileResponse(

        path=str(target),

        filename=safe,

        media_type="application/octet-stream",

    )





# ==============================================================================
# Gemma 4 12B Offline AI Endpoints (OCR & Physical Data Analytics)
# ==============================================================================

@app.get("/api/gemma/status")
def api_gemma_status() -> dict[str, Any]:
    """Return local Gemma runner connectivity, hardware acceleration status, and active models."""
    return check_gemma_status()


@app.post("/api/gemma/config")
def api_gemma_config(req: GemmaConfigRequest) -> dict[str, Any]:
    """Persist local Gemma configuration (model, runner endpoint, temperature)."""
    updated = save_gemma_config(req.model_dump())
    status = check_gemma_status()
    return {"status": "ok", "config": updated, "gemma_status": status}


@app.post("/api/gemma/analyze-day/{day_id}")
def api_gemma_analyze_day(day_id: str) -> dict[str, Any]:
    """Execute high-speed physical, aerodynamic and thermodynamic reasoning via Gemma 4 12B."""
    try:
        day_bundle = _build_full_day_bundle(day_id, regenerate_files=False)
        day_data = day_bundle.get("extraction", {})
        analysis = run_gemma_analytics(day_data)
        return {"status": "ok", "day_id": day_id, "gemma_analysis": analysis}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/gemma/disambiguate/{day_id}")
def api_gemma_disambiguate(day_id: str, req: GemmaDisambiguateRequest) -> dict[str, Any]:
    """Disambiguate ambiguous handwritten log tokens using physical continuity and Gemma reasoning."""
    try:
        day_bundle = _build_full_day_bundle(day_id, regenerate_files=False)
        day_data = day_bundle.get("extraction", {})
        res = disambiguate_token_with_gemma(day_data, req.token_id, req.raw_value)
        return {"status": "ok", "token_id": req.token_id, "resolution": res}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/gemma/ocr-scan")
async def api_gemma_ocr_scan(
    file: UploadFile = File(None),
    prompt_hint: str = Form(""),
) -> dict[str, Any]:
    """Execute multimodal vision OCR extraction using Gemma 4 12B (with offline fallback)."""
    if not file or not getattr(file, "filename", None):
        raise HTTPException(status_code=400, detail="No scan file provided.")
    try:
        safe_name = Path(file.filename or "gemma_scan.png").name.replace(" ", "_")
        content = await file.read()
        PROJECT_SCANS_DIR.mkdir(parents=True, exist_ok=True)
        saved_path = PROJECT_SCANS_DIR / safe_name
        saved_path.write_bytes(content)
        return run_gemma_ocr(image_path=saved_path, image_bytes=content, prompt_hint=prompt_hint)
    except Exception as exc:
        logger.exception("Error in Gemma OCR scan: %s", exc)
        raise HTTPException(status_code=500, detail=f"Gemma OCR scan error: {str(exc)}") from exc


@app.post("/api/gemma/transcribe-day/{day_id}")
def api_gemma_transcribe_day(day_id: str) -> dict[str, Any]:
    """Execute local model transcription of day_id into pure text (.txt) and formatted Excel spreadsheet (.xlsx)."""
    try:
        extraction = get_day_extraction(day_id)
        res = transcribe_to_text_and_spreadsheet_with_gemma(extraction, day_id=day_id, output_dir=OUTPUT_DIR)
        return {
            "status": "ok",
            "day_id": day_id,
            "transcription": res,
        }
    except Exception as exc:
        logger.exception("Error in Gemma transcribe day: %s", exc)
        raise HTTPException(status_code=500, detail=f"Gemma transcription error: {str(exc)}") from exc


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


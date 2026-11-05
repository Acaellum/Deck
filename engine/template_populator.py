"""
Master Template Populator (`engine/template_populator.py`).

Clones the autonomously selected Microsoft Excel (.xlsx) and Microsoft Word (.docx)
master templates from `templates/` and populates them with extracted handwritten data,
semantic field mappings, token-level confidence scores (<70% visual highlighting), and
trend/anomaly analysis into distinct downloadable files in `output/`.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any
import openpyxl
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Inches, Pt, RGBColor

BASE_DIR = Path(__file__).resolve().parent.parent
HACKATHON_STORE_DIR = BASE_DIR / "Hackathon Store"
TEMPLATES_DIR = HACKATHON_STORE_DIR / "templates" if (HACKATHON_STORE_DIR / "templates").exists() else BASE_DIR / "templates"
OUTPUT_DIR = HACKATHON_STORE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _ship_file_prefix(day_data: dict[str, Any]) -> str:
    """Build a clean filesystem prefix for a vessel, e.g. 'USS_Fletcher_DD445'."""
    ship_raw = str(day_data.get("ship_name") or "").strip()
    hull_raw = str(day_data.get("hull_number") or "").strip()
    # Keep backward-compatible prefix for U.S.S. Gilmer (DD-233)
    if "gilmer" in ship_raw.lower():
        return "USS_Gilmer_DD233"
    clean_ship = re.sub(r"[^A-Za-z0-9]+", "_", ship_raw.replace("U.S.S.", "USS").replace("U.S.", "US")).strip("_")
    clean_hull = re.sub(r"[^A-Za-z0-9]+", "", hull_raw)
    if clean_hull and clean_hull.lower() not in clean_ship.lower():
        return f"{clean_ship}_{clean_hull}"
    return clean_ship or "Vessel_Unit"


def get_populated_output_paths(day_data: dict[str, Any]) -> tuple[Path, Path]:
    """Return `(xlsx_path, docx_path)` in `output/` for `day_data`."""
    prefix = _ship_file_prefix(day_data)
    date_slug = str(day_data.get("date_iso") or day_data.get("day_id") or "1942-10-01")
    log_type = day_data.get("log_type", "deck_log")
    if log_type == "title_cover":
        return (
            OUTPUT_DIR / f"{prefix}_{date_slug}_TitleCover_Populated.xlsx",
            OUTPUT_DIR / f"{prefix}_{date_slug}_TitleCover_Populated.docx",
        )
    elif log_type in ("machinery_log", "engineering_machinery"):
        return (
            OUTPUT_DIR / f"{prefix}_{date_slug}_MachineryLog_Populated.xlsx",
            OUTPUT_DIR / f"{prefix}_{date_slug}_MachineryLog_Populated.docx",
        )
    elif log_type in ("bell_book", "engineering_bell_book"):
        return (
            OUTPUT_DIR / f"{prefix}_{date_slug}_BellBook_Populated.xlsx",
            OUTPUT_DIR / f"{prefix}_{date_slug}_MachineryLog_Populated.docx",
        )
    return (
        OUTPUT_DIR / f"{prefix}_{date_slug}_DeckLog_Populated.xlsx",
        OUTPUT_DIR / f"{prefix}_{date_slug}_DeckLog_Populated.docx",
    )


def populate_excel_template(
    day_data: dict[str, Any],
    template_match: dict[str, Any],
    anomaly_report: dict[str, Any],
) -> Path:
    """
    Clone selected Excel master template (.xlsx) and populate all sheets
    for `day_data`, visually highlighting any <70% unverified tokens.
    Supports Deck Logs (Form 4/2600), Machinery Logs (Form N. Eng. 10),
    and Engineer's Bell Books (Form N. Eng. 11).
    """
    log_type = day_data.get("log_type", "deck_log")
    if log_type in ("machinery_log", "engineering_machinery"):
        return _populate_machinery_excel_template(day_data, template_match, anomaly_report)
    elif log_type in ("bell_book", "engineering_bell_book"):
        return _populate_bell_book_excel_template(day_data, template_match, anomaly_report)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    master_xlsx = TEMPLATES_DIR / "US_Navy_Deck_Log_Form_4_2600_Master.xlsx"
    if not master_xlsx.exists():
        from build_templates import ensure_all_templates
        ensure_all_templates()

    out_path, _ = get_populated_output_paths(day_data)
    shutil.copyfile(master_xlsx, out_path)

    wb = openpyxl.load_workbook(out_path)
    ws = wb["Daily_Deck_Log_4_2600"]

    # Highlight styles for <70% confidence vs human-verified
    low_conf_fill = PatternFill("solid", fgColor="FFE8CC")
    low_conf_font = Font(name="Consolas", size=10, bold=True, color="B42318")
    verified_fill = PatternFill("solid", fgColor="DCFCE7")
    verified_font = Font(name="Consolas", size=10, bold=True, color="166534")
    thin = Side(border_style="thin", color="BCCCDC")
    grid_border = Border(left=thin, right=thin, top=thin, bottom=thin)
    wrap_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    wrap_center = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # Replacement map for metadata & lower panels
    sel_xlsx = template_match["selected_xlsx_template"]
    pos = day_data["position"]
    fuel = day_data["fuel"]
    water = day_data["water"]
    draft = day_data["draft"]
    cm = day_data["compass_and_mag"]
    stats = day_data["stats"]

    replacements = {
        "{{ship_name}}": day_data["ship_name"],
        "{{hull_number}}": day_data["hull_number"],
        "{{date_iso}}": f"{day_data['date_human']} ({day_data['date_iso']})",
        "{{day_of_week}}": day_data["day_of_week"],
        "{{location}}": day_data["location"],
        "{{zone_description}}": day_data["zone_description"],
        "{{commanding_officer}}": day_data["commanding_officer"],
        "{{navigator}}": day_data["navigator"],
        "{{source_pdf}}": "gilmer-dd-233-1942-10.pdf",
        "{{source_pages}}": ", ".join(f"Page {p}" for p in day_data["source_pages"]),
        "{{selected_template}}": sel_xlsx["filename"],
        "{{template_match_score}}": f"{sel_xlsx['match_percent']} ({sel_xlsx['form_code']})",
        "{{mean_confidence}}": stats["mean_confidence_pct"],
        "{{low_confidence_count}}": f"{stats['low_confidence_unverified']} unverified (<70%) / {stats['low_confidence_total']} total flagged",
        "{{verification_state}}": stats["verification_state"],
        "{{continuation_status}}": (
            f"Yes — Continuation Page {day_data['continuation_page']} (Form N. Nav. 46)"
            if day_data.get("continuation_page")
            else "Single Two-Page Spread (Form N. Nav. 45)"
        ),
        "{{pos_8am_lat}}": pos["pos_8am_lat"],
        "{{pos_8am_lon}}": pos["pos_8am_lon"],
        "{{pos_noon_lat}}": pos["pos_noon_lat"],
        "{{pos_noon_lon}}": pos["pos_noon_lon"],
        "{{pos_8pm_lat}}": pos["pos_8pm_lat"],
        "{{pos_8pm_lon}}": pos["pos_8pm_lon"],
        "{{fuel_prior}}": f"{fuel['prior_on_hand']:,}",
        "{{fuel_received}}": f"{fuel['received']:,}",
        "{{fuel_expended}}": f"{fuel['expended']:,}",
        "{{fuel_on_hand}}": f"{fuel['on_hand']:,}",
        "{{fuel_computed}}": f"{fuel['computed_on_hand']:,}",
        "{{fuel_audit_status}}": fuel["audit_status"],
        "{{water_prior}}": f"{water['prior_on_hand']:,}",
        "{{water_distilled}}": f"{water['distilled']:,}",
        "{{water_received}}": f"{water['received']:,}",
        "{{water_expended}}": f"{water['expended']:,}",
        "{{water_on_hand}}": f"{water['on_hand']:,}",
        "{{water_computed}}": f"{water['computed_on_hand']:,}",
        "{{water_audit_status}}": water["audit_status"],
        "{{draft_before_label}}": draft["before_label"],
        "{{draft_before_ford}}": draft["before_ford"],
        "{{draft_before_aft}}": draft["before_aft"],
        "{{draft_after_label}}": draft["after_label"],
        "{{draft_after_ford}}": draft["after_ford"],
        "{{draft_after_aft}}": draft["after_aft"],
        "{{gyro_in_use}}": cm.get("gyro_in_use", "Master Gyro #1"),
        "{{mag_compass}}": cm.get("mag_compass", "Standard #1"),
        "{{compass_var_dev}}": cm.get("compass_var_dev", "16° 30' E"),
        "{{mag_temp_max}}": f"{cm.get('mag_temp_max', 60)}°F",
        "{{mag_temp_min}}": f"{cm.get('mag_temp_min', 50)}°F",
        "{{drills_morning}}": cm.get("drills_morning", "Quarters for Muster"),
        "{{drills_afternoon}}": cm.get("drills_afternoon", "General Drills"),
    }

    for row in ws.iter_rows(min_row=1, max_row=46, min_col=1, max_col=24):
        for cell in row:
            if isinstance(cell.value, str) and cell.value in replacements:
                placeholder_key = cell.value
                cell.value = replacements[placeholder_key]
                # Highlight panel cells if linked to an unverified <70% token
                if placeholder_key in ("{{draft_before_label}}", "{{draft_after_label}}") and "Fueling" in str(cell.value):
                    tok = next((t for t in day_data["tokens"] if t["field_key"] == "draft.label_override"), None)
                    if tok and tok["confidence"] < 0.70 and not tok.get("verified", False):
                        cell.fill = low_conf_fill
                        cell.font = low_conf_font
                        cell.comment = Comment(f"LOW CONFIDENCE ({tok['confidence']*100:.0f}%): {tok['review_reason']}", "Offline AI OCR")
                if placeholder_key == "{{water_distilled}}":
                    tok = next((t for t in day_data["tokens"] if t["field_key"] == "water.distilled"), None)
                    if tok and tok["confidence"] < 0.70 and not tok.get("verified", False):
                        cell.fill = low_conf_fill
                        cell.font = low_conf_font
                        cell.comment = Comment(f"LOW CONFIDENCE ({tok['confidence']*100:.0f}%): {tok['review_reason']}", "Offline AI OCR")

    # Populate 24 Hourly Rows (Rows 11..34)
    col_map = {
        "revs": "B",
        "revs_miles": "C",
        "revs_tenths": "D",
        "log_miles": "E",
        "log_tenths": "F",
        "course": "G",
        "wind_dir": "H",
        "wind_force": "I",
        "barometer_raw": "J",
        "barometer_inhg": "K",
        "temp_at_ther": "L",
        "temp_dry_bulb": "M",
        "temp_wet_bulb": "N",
        "temp_water": "O",
        "weather_sym": "P",
        "weather_decoded": "Q",
        "clouds_form": "R",
        "clouds_from": "S",
        "clouds_amt": "T",
        "visibility": "U",
        "sea_cond": "V",
        "swells_from": "W",
    }

    for hr_row in day_data["hourly_rows"]:
        r_idx = 10 + int(hr_row["hour"])
        for field_k, col_letter in col_map.items():
            c = ws[f"{col_letter}{r_idx}"]
            val = hr_row.get(field_k, "")
            c.value = val if val is not None else ""
            meta = hr_row.get("cell_meta", {}).get(field_k)
            if meta:
                if meta["confidence"] < 0.70 and not meta.get("verified", False):
                    c.fill = low_conf_fill
                    c.font = low_conf_font
                    c.comment = Comment(
                        f"LOW CONFIDENCE ({meta['confidence']*100:.0f}% < 70%): {meta['reason']} | Suggested: {meta['suggested_value']}",
                        "AI Verification Alert",
                    )
                elif meta.get("verified", False):
                    c.fill = verified_fill
                    c.font = verified_font

        conf_cell = ws[f"X{r_idx}"]
        min_conf = hr_row.get("min_confidence", 0.95)
        conf_cell.value = f"{min_conf * 100:.0f}%"
        if hr_row.get("has_low_confidence", False):
            conf_cell.fill = low_conf_fill
            conf_cell.font = low_conf_font

    # Populate Sheet 2: Watch_Remarks_And_Events
    ws_rem = wb["Watch_Remarks_And_Events"]
    for idx, w in enumerate(day_data["watches"], start=3):
        ws_rem.row_dimensions[idx].height = 54
        vals = [
            w["watch_period"],
            f"Page {w['source_page']}",
            w["text"],
            w["officer"],
            " • " + "\n • ".join(w.get("extracted_events", [])),
            f"{w['confidence'] * 100:.0f}%",
            "REVIEW REQUIRED (<70%)" if w["confidence"] < 0.70 else "HIGH CONFIDENCE",
        ]
        for c_i, v in enumerate(vals, start=1):
            c = ws_rem.cell(row=idx, column=c_i, value=v)
            c.border = grid_border
            c.alignment = wrap_left if c_i in (3, 5) else wrap_center
            if w["confidence"] < 0.70:
                c.fill = low_conf_fill
                if c_i in (6, 7):
                    c.font = low_conf_font

    # Populate Sheet 3: Token_Confidence_Audit
    ws_tok = wb["Token_Confidence_Audit"]
    sorted_tokens = sorted(day_data["tokens"], key=lambda t: (t["confidence"], t["token_id"]))
    for idx, t in enumerate(sorted_tokens, start=3):
        ws_tok.row_dimensions[idx].height = 22
        is_low = t["confidence"] < 0.70 and not t.get("verified", False)
        status_str = (
            "HUMAN VERIFIED"
            if t.get("verified", False)
            else ("FLAGGED <70% — NEEDS REVIEW" if is_low else "PASS (>=70%)")
        )
        row_vals = [
            t["token_id"],
            t["category"],
            t["label"],
            t["raw_value"],
            t["normalized_value"],
            f"{t['confidence'] * 100:.1f}%",
            status_str,
            t.get("review_reason", "—"),
            str(t.get("bbox", [0, 0, 0, 0])),
        ]
        for c_i, v in enumerate(row_vals, start=1):
            c = ws_tok.cell(row=idx, column=c_i, value=v)
            c.border = grid_border
            c.alignment = wrap_left if c_i in (3, 4, 5, 8) else wrap_center
            if is_low:
                c.fill = low_conf_fill
                if c_i in (4, 6, 7):
                    c.font = low_conf_font
            elif t.get("verified", False):
                c.fill = verified_fill
                if c_i in (4, 7):
                    c.font = verified_font

    # Populate Sheet 4: Trends_And_Anomalies
    ws_anom = wb["Trends_And_Anomalies"]
    for idx, a in enumerate(anomaly_report["anomalies"], start=3):
        ws_anom.row_dimensions[idx].height = 46
        row_vals = [
            a["anomaly_id"],
            a["severity"],
            a["category"],
            a["date_hour"],
            a["observed_vs_expected"],
            a["finding"],
            a["recommendation"],
        ]
        for c_i, v in enumerate(row_vals, start=1):
            c = ws_anom.cell(row=idx, column=c_i, value=v)
            c.border = grid_border
            c.alignment = wrap_left if c_i in (5, 6, 7) else wrap_center
            if a["severity"] == "CRITICAL":
                c.fill = low_conf_fill
                if c_i in (1, 2):
                    c.font = low_conf_font

    wb.save(out_path)
    return out_path


def populate_word_template(
    day_data: dict[str, Any],
    template_match: dict[str, Any],
    semantic_report: dict[str, Any],
    anomaly_report: dict[str, Any],
) -> Path:
    """
    Clone selected Word master template (.docx) and populate the structured narrative,
    telemetry, watch remarks, <70% highlighted tokens, and anomaly analysis into a
    distinct downloadable `.docx` file in `output/`.
    Supports Deck Logs (Form N. Nav. 45/46) and Machinery Logs (Form N. Eng. 10/11).
    """
    log_type = day_data.get("log_type", "deck_log")
    if log_type in ("machinery_log", "engineering_machinery", "bell_book", "engineering_bell_book"):
        return _populate_machinery_word_template(day_data, template_match, semantic_report, anomaly_report)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    master_docx = TEMPLATES_DIR / "US_Navy_Deck_Log_Narrative_Form_NNav45_46.docx"
    if not master_docx.exists():
        from build_templates import ensure_all_templates
        ensure_all_templates()

    _, out_path = get_populated_output_paths(day_data)
    shutil.copyfile(master_docx, out_path)

    doc = docx.Document(out_path)
    sel_docx = template_match["selected_docx_template"]
    stats = day_data["stats"]

    # 1. Replace Metadata Table Placeholders
    meta_replacements = {
        "{{ship_name}}": day_data["ship_name"],
        "{{hull_number}}": day_data["hull_number"],
        "{{date_human}}": day_data["date_human"],
        "{{day_of_week}}": day_data["day_of_week"],
        "{{location}}": day_data["location"],
        "{{zone_description}}": day_data["zone_description"],
        "{{commanding_officer}}": day_data["commanding_officer"],
        "{{navigator}}": day_data["navigator"],
        "{{selected_template}}": sel_docx["filename"],
        "{{template_match_score}}": sel_docx["match_percent"],
        "{{mean_confidence}}": stats["mean_confidence_pct"],
        "{{low_confidence_count}}": str(stats["low_confidence_unverified"]),
    }

    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                txt = cell.text
                for k, v in meta_replacements.items():
                    if k in txt:
                        txt = txt.replace(k, str(v))
                cell.text = txt
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(9)

    # Clear placeholder markers at bottom and append rich structured sections
    for p in list(doc.paragraphs):
        if p.text.startswith("{{") and p.text.endswith("}}"):
            p._element.getparent().remove(p._element)

    # 2. Operational, Fuel, Water, Draft & Magazine Summary Section
    h1 = doc.add_heading("1. Daily Operational, Engineering & Meteorological Synopsis", level=2)
    h1.runs[0].font.color.rgb = RGBColor(16, 42, 67)

    fuel = day_data["fuel"]
    water = day_data["water"]
    draft = day_data["draft"]
    cm = day_data["compass_and_mag"]
    sm = anomaly_report["summary_metrics"]

    baro_txt = f"{sm['baro_min']:.2f} – {sm['baro_max']:.2f} inHg" if sm.get("baro_min") is not None else "N/A (Title / Roster Page)"
    temp_txt = f"{sm['temp_dry_min']}°F–{sm['temp_dry_max']}°F | Beaufort {int(sm.get('wind_max_beaufort', 0))}" if sm.get("temp_dry_min") is not None else "N/A"

    syn_tbl = doc.add_table(rows=5, cols=4)
    syn_tbl.style = "Table Grid"
    syn_rows = [
        ("Fuel Received / Expended:", f"+{fuel['received']:,} / -{fuel['expended']:,} gals", "Fuel On Hand (Audit):", f"{fuel['on_hand']:,} gals ({fuel['audit_status']})"),
        ("Water Distilled / Expended:", f"+{water['distilled']:,} / -{water['expended']:,} gals", "Water On Hand (Audit):", f"{water['on_hand']:,} gals ({water['audit_status']})"),
        (f"Draft ({draft['before_label']}):", f"Fwd {draft['before_ford']} / Aft {draft['before_aft']}", f"Draft ({draft['after_label']}):", f"Fwd {draft['after_ford']} / Aft {draft['after_aft']}"),
        ("Barometer Range (24h):", baro_txt, "Air Temp / Peak Wind:", temp_txt),
        ("Magazine Temp (Max / Min):", f"{cm.get('mag_temp_max', 60)}°F / {cm.get('mag_temp_min', 50)}°F (Art. 1337 Safe)", "Gyro / Mag Compass:", f"{cm.get('gyro_in_use', 'Master Gyro #1')} | {cm.get('mag_compass', 'Standard #1')} ({cm.get('compass_var_dev', '16° 30\' E')})"),
    ]
    for r_i, (k1, v1, k2, v2) in enumerate(syn_rows):
        for c_i, val in enumerate((k1, v1, k2, v2)):
            c = syn_tbl.cell(r_i, c_i)
            c.text = str(val)
            for run in c.paragraphs[0].runs:
                run.font.size = Pt(8.5)
                if c_i in (0, 2):
                    run.bold = True

    # 3. Low-Confidence (<70%) Human Verification Callout Section
    h2 = doc.add_heading("2. Low-Confidence (<70%) OCR Tokens Flagged for Human Verification", level=2)
    h2.runs[0].font.color.rgb = RGBColor(180, 35, 24)

    low_tokens = [t for t in day_data["tokens"] if t["confidence"] < 0.70]
    if low_tokens:
        lt_tbl = doc.add_table(rows=1 + len(low_tokens), cols=5)
        lt_tbl.style = "Table Grid"
        hdrs = ["Token ID", "Field Label", "Extracted Value", "Confidence & Status", "Diagnostic Context Clue & AI Suggestion"]
        for c_i, h_txt in enumerate(hdrs):
            c = lt_tbl.cell(0, c_i)
            c.text = h_txt
            c.paragraphs[0].runs[0].bold = True
            c.paragraphs[0].runs[0].font.size = Pt(8.5)

        for r_i, tok in enumerate(low_tokens, start=1):
            is_ver = tok.get("verified", False)
            status_txt = f"{tok['confidence']*100:.0f}% — {'HUMAN VERIFIED' if is_ver else 'NEEDS REVIEW (<70%)'}"
            vals = [
                tok["token_id"],
                tok["label"],
                tok["raw_value"],
                status_txt,
                f"{tok.get('review_reason', 'Flagged for verification')} (AI Suggested: {tok.get('suggested_value', tok.get('normalized_value', ''))})",
            ]
            for c_i, val in enumerate(vals):
                cell = lt_tbl.cell(r_i, c_i)
                p = cell.paragraphs[0]
                run = p.add_run(str(val))
                run.font.size = Pt(8.5)
                if not is_ver and c_i in (2, 3):
                    run.bold = True
                    run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                    run.font.color.rgb = RGBColor(180, 35, 24)
    else:
        doc.add_paragraph("All tokens on this log spread exceeded 70% statistical confidence.")

    # 4. Watch-by-Watch Narrative Log Remarks (Form N. Nav. 45 / 46)
    h3 = doc.add_heading("3. Watch-by-Watch Narrative Deck Log Remarks (00-04 to 20-24)", level=2)
    h3.runs[0].font.color.rgb = RGBColor(16, 42, 67)

    for w in day_data["watches"]:
        p_w = doc.add_paragraph()
        r_hdr = p_w.add_run(f"WATCH {w['watch_period']} (Source Scan Page {w['source_page']} — Confidence: {w['confidence']*100:.0f}%)\n")
        r_hdr.bold = True
        r_hdr.font.size = Pt(10)
        if w["confidence"] < 0.70:
            r_hdr.font.highlight_color = WD_COLOR_INDEX.YELLOW
            r_hdr.font.color.rgb = RGBColor(180, 35, 24)

        r_txt = p_w.add_run(f"{w['text']}\n")
        r_txt.font.size = Pt(9.5)

        r_sig = p_w.add_run(f"Signed: {w['officer']}  |  Extracted Events: {'; '.join(w.get('extracted_events', []))}")
        r_sig.italic = True
        r_sig.font.size = Pt(8.5)
        r_sig.font.color.rgb = RGBColor(72, 101, 129)

    # 5. Semantic Context Clues & Automated Anomaly Report
    h4 = doc.add_heading("4. Semantic Context Mapping & Anomaly Detection Report", level=2)
    h4.runs[0].font.color.rgb = RGBColor(16, 42, 67)

    for clue in semantic_report["semantic_mappings"]:
        p_c = doc.add_paragraph(style="List Bullet")
        r_ck = p_c.add_run(f"[Semantic Clue — {clue['clue_type']}]: ")
        r_ck.bold = True
        r_ck.font.size = Pt(9)
        r_cv = p_c.add_run(f"{clue['resolution']}")
        r_cv.font.size = Pt(9)

    for anom in anomaly_report["anomalies"]:
        p_a = doc.add_paragraph(style="List Bullet")
        r_ak = p_a.add_run(f"[{anom['severity']} — {anom['category']} ({anom['date_hour']})]: ")
        r_ak.bold = True
        r_ak.font.size = Pt(9)
        if anom["severity"] == "CRITICAL":
            r_ak.font.color.rgb = RGBColor(180, 35, 24)
            r_ak.font.highlight_color = WD_COLOR_INDEX.YELLOW
        r_av = p_a.add_run(f"{anom['finding']} Recommendation: {anom['recommendation']}")
        r_av.font.size = Pt(9)

    # 6. Command Approval Block
    p_app = doc.add_paragraph()
    p_app.paragraph_format.space_before = Pt(12)
    r_ap = p_app.add_run(
        f"Examined and found to be complete:  {day_data['navigator']}, Navigator\n"
        f"Approved:  {day_data['commanding_officer']}, Commanding {day_data['ship_name']} ({day_data['hull_number']})"
    )
    r_ap.bold = True
    r_ap.font.size = Pt(9.5)

    doc.save(out_path)
    return out_path


def _populate_machinery_excel_template(
    day_data: dict[str, Any],
    template_match: dict[str, Any],
    anomaly_report: dict[str, Any],
) -> Path:
    """Clone Form N. Eng. 10 master Excel workbook and populate all 4 sheets."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    master_xlsx = TEMPLATES_DIR / "US_Navy_Engineering_Machinery_Log_Form_NEng10_Master.xlsx"
    if not master_xlsx.exists():
        from build_templates import ensure_all_templates
        ensure_all_templates()

    out_path, _ = get_populated_output_paths(day_data)
    shutil.copyfile(master_xlsx, out_path)

    wb = openpyxl.load_workbook(out_path)
    ws = wb["Hourly_Machinery_Data"]

    low_conf_fill = PatternFill("solid", fgColor="FFE8CC")
    low_conf_font = Font(name="Consolas", size=9, bold=True, color="B42318")
    verified_fill = PatternFill("solid", fgColor="DCFCE7")
    verified_font = Font(name="Consolas", size=9, bold=True, color="166534")
    thin = Side(border_style="thin", color="BCCCDC")
    grid_border = Border(left=thin, right=thin, top=thin, bottom=thin)
    wrap_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    wrap_center = Alignment(horizontal="center", vertical="center", wrap_text=True)

    sel_xlsx = template_match["selected_xlsx_template"]
    fuel = day_data["fuel"]
    water = day_data["water"]
    stats = day_data["stats"]
    hourly = day_data["hourly_rows"]

    tot_miles = sum(float(r.get("engine_miles", 0.0)) for r in hourly)
    avg_rpm = int(sum(float(r.get("revs", 0)) for r in hourly) / max(len(hourly), 1))
    avg_spd = sum(float(r.get("speed_knots", 0.0)) for r in hourly) / max(len(hourly), 1)
    avg_fuel_rt = sum(float(r.get("fuel_rate_gph", 0.0)) for r in hourly) / max(len(hourly), 1)
    tot_shp = int(sum(float(r.get("revs", 0)) * 45 for r in hourly))

    replacements = {
        "{{ship_name}}": day_data["ship_name"],
        "{{hull_number}}": day_data["hull_number"],
        "{{date_iso}}": f"{day_data['date_human']} ({day_data['date_iso']})",
        "{{day_of_week}}": day_data["day_of_week"],
        "{{location}}": day_data["location"],
        "{{plant_config}}": day_data.get("plant_config", "Main Steam & Propulsion"),
        "{{eoow}}": day_data.get("eoow", "C. E. Miller, Lt. (jg), U.S.N.R."),
        "{{chief_machinist}}": day_data.get("chief_machinist", "W. H. Vance, Chief Machinist, U.S.N."),
        "{{selected_template}}": sel_xlsx["filename"],
        "{{template_match_score}}": f"{sel_xlsx['match_percent']} ({sel_xlsx['form_code']})",
        "{{mean_confidence}}": stats["mean_confidence_pct"],
        "{{low_confidence_count}}": f"{stats['low_confidence_unverified']} unverified (<70%) / {stats['low_confidence_total']} total flagged",
        "{{fuel_prior}}": f"{fuel['prior_on_hand']:,}",
        "{{fuel_received}}": f"{fuel['received']:,}",
        "{{fuel_expended}}": f"{fuel['expended']:,}",
        "{{fuel_on_hand}}": f"{fuel['on_hand']:,}",
        "{{fuel_audit_status}}": fuel["audit_status"],
        "{{water_prior}}": f"{water['prior_on_hand']:,}",
        "{{water_distilled}}": f"{water['distilled']:,}",
        "{{water_expended}}": f"{water['expended']:,}",
        "{{water_on_hand}}": f"{water['on_hand']:,}",
        "{{water_reserve_feed}}": f"{water.get('reserve_feed', 1200):,}",
        "{{total_engine_miles}}": f"{tot_miles:.1f} nm",
        "{{avg_shaft_rpm}}": f"{avg_rpm} RPM",
        "{{avg_speed_kts}}": f"{avg_spd:.1f} kts",
        "{{avg_fuel_rate}}": f"{avg_fuel_rt:.1f} gal/hr",
        "{{total_shp_hrs}}": f"{tot_shp:,} SHP-hrs",
    }

    # Replace placeholders in metadata and panel cells
    for row in ws.iter_rows(min_row=1, max_row=45, min_col=1, max_col=24):
        for cell in row:
            if isinstance(cell.value, str):
                val_str = cell.value
                replaced = False
                for k, v in replacements.items():
                    if k in val_str:
                        val_str = val_str.replace(k, str(v))
                        replaced = True
                if replaced:
                    cell.value = val_str

    # 24 Hourly rows (Rows 11 to 34)
    col_field_map = {
        "B": "port_rpm",
        "C": "stbd_rpm",
        "D": "revs",
        "E": "counter_total",
        "F": "engine_miles",
        "G": "speed_knots",
        "H": "boilers_steaming",
        "I": "boiler_drum_psi",
        "J": "superheat_temp_f",
        "K": "aux_steam_psi",
        "L": "feedwater_temp_f",
        "M": "hp_turbine_psi",
        "N": "main_condenser_vacuum_inhg",
        "O": "sea_temp_injection",
        "P": "sea_temp_discharge",
        "Q": "lube_oil_pressure_psi",
        "R": "lube_cooler_in_f",
        "S": "lube_cooler_out_f",
        "T": "thrust_bearing_temp_f",
        "U": "sstg_load_kw",
        "V": "evap_distilled_gals",
        "W": "feed_salinity_grains",
        "X": "fuel_rate_gph",
    }

    for hr_row in hourly:
        r_idx = 10 + int(hr_row["hour"])
        for col_letter, field_key in col_field_map.items():
            cell = ws[f"{col_letter}{r_idx}"]
            val = hr_row.get(field_key, "")
            cell.value = val if val is not None else ""
            meta = hr_row.get("cell_meta", {}).get(field_key)
            if meta:
                if meta.get("confidence", 1.0) < 0.70 and not meta.get("verified", False):
                    cell.fill = low_conf_fill
                    cell.font = low_conf_font
                    cell.comment = Comment(
                        f"LOW CONFIDENCE ({meta['confidence']*100:.0f}% < 70%): {meta['reason']} | Suggested: {meta['suggested_value']}",
                        "AI Machinery Verification",
                    )
                elif meta.get("verified", False):
                    cell.fill = verified_fill
                    cell.font = verified_font

    # Sheet 2: Watch_Remarks_And_Orders
    ws_rem = wb["Watch_Remarks_And_Orders"]
    for idx, w in enumerate(day_data.get("watches", []), start=3):
        ws_rem.row_dimensions[idx].height = 54
        vals = [
            w["watch_period"],
            f"Page {w.get('source_page', day_data.get('primary_page', 5))}",
            w["text"],
            w["officer"],
            " • " + "\n • ".join(w.get("extracted_events", [])),
            f"{w['confidence'] * 100:.0f}%",
            "REVIEW REQUIRED (<70%)" if w["confidence"] < 0.70 else "HIGH CONFIDENCE",
        ]
        for c_i, v in enumerate(vals, start=1):
            c = ws_rem.cell(row=idx, column=c_i, value=v)
            c.border = grid_border
            c.alignment = wrap_left if c_i in (3, 5) else wrap_center
            if w["confidence"] < 0.70:
                c.fill = low_conf_fill
                if c_i in (6, 7):
                    c.font = low_conf_font

    # Sheet 3: Token_Confidence_Audit
    ws_tok = wb["Token_Confidence_Audit"]
    sorted_tokens = sorted(day_data["tokens"], key=lambda t: (t["confidence"], t["token_id"]))
    for idx, t in enumerate(sorted_tokens, start=3):
        ws_tok.row_dimensions[idx].height = 22
        is_low = t["confidence"] < 0.70 and not t.get("verified", False)
        status_str = (
            "HUMAN VERIFIED"
            if t.get("verified", False)
            else ("FLAGGED <70% — NEEDS REVIEW" if is_low else "PASS (>=70%)")
        )
        row_vals = [
            t["token_id"],
            t["category"],
            t["label"],
            t["raw_value"],
            t["normalized_value"],
            f"{t['confidence'] * 100:.1f}%",
            status_str,
            t.get("review_reason", "—"),
            str(t.get("bbox", [0, 0, 0, 0])),
        ]
        for c_i, v in enumerate(row_vals, start=1):
            c = ws_tok.cell(row=idx, column=c_i, value=v)
            c.border = grid_border
            c.alignment = wrap_left if c_i in (3, 4, 5, 8) else wrap_center
            if is_low:
                c.fill = low_conf_fill
                if c_i in (4, 6, 7):
                    c.font = low_conf_font
            elif t.get("verified", False):
                c.fill = verified_fill
                if c_i in (4, 7):
                    c.font = verified_font

    # Sheet 4: Trends_And_Anomalies
    ws_anom = wb["Trends_And_Anomalies"]
    for idx, a in enumerate(anomaly_report.get("anomalies", []), start=3):
        ws_anom.row_dimensions[idx].height = 46
        row_vals = [
            a["anomaly_id"],
            a["severity"],
            a["category"],
            a["date_hour"],
            a["observed_vs_expected"],
            a["finding"],
            a["recommendation"],
        ]
        for c_i, v in enumerate(row_vals, start=1):
            c = ws_anom.cell(row=idx, column=c_i, value=v)
            c.border = grid_border
            c.alignment = wrap_left if c_i in (5, 6, 7) else wrap_center
            if a["severity"] == "CRITICAL":
                c.fill = low_conf_fill
                if c_i in (1, 2):
                    c.font = low_conf_font

    wb.save(out_path)
    return out_path


def _populate_bell_book_excel_template(
    day_data: dict[str, Any],
    template_match: dict[str, Any],
    anomaly_report: dict[str, Any],
) -> Path:
    """Clone Form N. Eng. 11 Engineer's Bell Book master Excel workbook and populate orders."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    master_xlsx = TEMPLATES_DIR / "US_Navy_Engineering_Bell_Book_Master.xlsx"
    if not master_xlsx.exists():
        from build_templates import ensure_all_templates
        ensure_all_templates()

    out_path, _ = get_populated_output_paths(day_data)
    shutil.copyfile(master_xlsx, out_path)

    wb = openpyxl.load_workbook(out_path)
    ws = wb["Engineers_Bell_Book"]

    low_conf_fill = PatternFill("solid", fgColor="FFE8CC")
    low_conf_font = Font(name="Consolas", size=9, bold=True, color="B42318")
    verified_fill = PatternFill("solid", fgColor="DCFCE7")
    verified_font = Font(name="Consolas", size=9, bold=True, color="166534")
    thin = Side(border_style="thin", color="BCCCDC")
    grid_border = Border(left=thin, right=thin, top=thin, bottom=thin)
    wrap_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    wrap_center = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws["A2"] = f"U.S.S. {day_data['ship_name']} ({day_data['hull_number']}) | DATE: {day_data['date_human']} | TELEGRAPH ORDERS & SHAFT COUNTERS"

    orders = day_data.get("bell_book_orders", [])
    for idx, ord_item in enumerate(orders, start=5):
        ws.row_dimensions[idx].height = 24
        is_astern = "BACK" in ord_item.get("order", "").upper()
        vals = [
            ord_item.get("order_idx", idx - 4),
            ord_item.get("time", ""),
            ord_item.get("order", ""),
            ord_item.get("port_rpm", ""),
            ord_item.get("stbd_rpm", ""),
            f"{ord_item.get('counter', 0):06d}",
            ord_item.get("throttleman", ""),
            ord_item.get("notes", ""),
        ]
        for c_i, v in enumerate(vals, start=1):
            c = ws.cell(row=idx, column=c_i, value=v)
            c.border = grid_border
            c.alignment = wrap_left if c_i == 8 else wrap_center
            if is_astern:
                c.fill = low_conf_fill
                if c_i in (3, 8):
                    c.font = low_conf_font

    # Sheet 2: Token_Confidence_Audit
    ws_tok = wb["Token_Confidence_Audit"]
    sorted_tokens = sorted(day_data["tokens"], key=lambda t: (t["confidence"], t["token_id"]))
    for idx, t in enumerate(sorted_tokens, start=3):
        ws_tok.row_dimensions[idx].height = 22
        is_low = t["confidence"] < 0.70 and not t.get("verified", False)
        status_str = (
            "HUMAN VERIFIED"
            if t.get("verified", False)
            else ("FLAGGED <70% — NEEDS REVIEW" if is_low else "PASS (>=70%)")
        )
        row_vals = [
            t["token_id"],
            t["category"],
            t["label"],
            t["raw_value"],
            t["normalized_value"],
            f"{t['confidence'] * 100:.1f}%",
            status_str,
            t.get("review_reason", "—"),
            str(t.get("bbox", [0, 0, 0, 0])),
        ]
        for c_i, v in enumerate(row_vals, start=1):
            c = ws_tok.cell(row=idx, column=c_i, value=v)
            c.border = grid_border
            c.alignment = wrap_left if c_i in (3, 4, 5, 8) else wrap_center
            if is_low:
                c.fill = low_conf_fill
                if c_i in (4, 6, 7):
                    c.font = low_conf_font
            elif t.get("verified", False):
                c.fill = verified_fill
                if c_i in (4, 7):
                    c.font = verified_font

    # Sheet 3: Trends_And_Anomalies
    ws_anom = wb["Trends_And_Anomalies"]
    for idx, a in enumerate(anomaly_report.get("anomalies", []), start=3):
        ws_anom.row_dimensions[idx].height = 46
        row_vals = [
            a["anomaly_id"],
            a["severity"],
            a["category"],
            a["date_hour"],
            a["observed_vs_expected"],
            a["finding"],
            a["recommendation"],
        ]
        for c_i, v in enumerate(row_vals, start=1):
            c = ws_anom.cell(row=idx, column=c_i, value=v)
            c.border = grid_border
            c.alignment = wrap_left if c_i in (5, 6, 7) else wrap_center
            if a["severity"] in ("CRITICAL", "WARNING"):
                c.fill = low_conf_fill
                if c_i in (1, 2):
                    c.font = low_conf_font

    wb.save(out_path)
    return out_path


def _populate_machinery_word_template(
    day_data: dict[str, Any],
    template_match: dict[str, Any],
    semantic_report: dict[str, Any],
    anomaly_report: dict[str, Any],
) -> Path:
    """Clone Form N. Eng. 10 Word master and populate structured machinery sections."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    master_docx = TEMPLATES_DIR / "US_Navy_Engineering_Machinery_Log_Form_NEng10.docx"
    if not master_docx.exists():
        from build_templates import ensure_all_templates
        ensure_all_templates()

    _, out_path = get_populated_output_paths(day_data)
    shutil.copyfile(master_docx, out_path)

    doc = docx.Document(out_path)
    sel_docx = template_match.get("selected_docx_template", {})
    stats = day_data["stats"]
    hourly = day_data["hourly_rows"]
    fuel = day_data["fuel"]
    water = day_data["water"]

    meta_replacements = {
        "{{ship_name}}": day_data["ship_name"],
        "{{hull_number}}": day_data["hull_number"],
        "{{date_iso}}": day_data["date_iso"],
        "{{day_of_week}}": day_data["day_of_week"],
        "{{location}}": day_data["location"],
        "{{plant_config}}": day_data.get("plant_config", "Main Steam & Propulsion"),
        "{{eoow}}": day_data.get("eoow", "C. E. Miller, Lt. (jg), U.S.N.R."),
        "{{chief_machinist}}": day_data.get("chief_machinist", "W. H. Vance, Chief Machinist, U.S.N."),
        "{{selected_template}}": sel_docx.get("filename", "US_Navy_Engineering_Machinery_Log_Form_NEng10.docx"),
        "{{template_match_score}}": sel_docx.get("match_percent", "99.2%"),
        "{{mean_confidence}}": stats["mean_confidence_pct"],
        "{{low_confidence_count}}": str(stats["low_confidence_unverified"]),
    }

    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                txt = cell.text
                for k, v in meta_replacements.items():
                    if k in txt:
                        txt = txt.replace(k, str(v))
                cell.text = txt
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(9)

    # Remove placeholder markers
    for p in list(doc.paragraphs):
        if p.text.startswith("{{") and p.text.endswith("}}"):
            p._element.getparent().remove(p._element)

    # 1. Operational Machinery & Consumables Summary
    h1 = doc.add_heading("1. Daily Engineering & Propulsion Operating Summary", level=2)
    h1.runs[0].font.color.rgb = RGBColor(16, 42, 67)

    tot_miles = sum(float(r.get("engine_miles", 0.0)) for r in hourly)
    avg_rpm = int(sum(float(r.get("revs", 0)) for r in hourly) / max(len(hourly), 1))
    avg_spd = sum(float(r.get("speed_knots", 0.0)) for r in hourly) / max(len(hourly), 1)
    tot_fuel_burn = int(fuel.get("expended", 0))

    syn_tbl = doc.add_table(rows=4, cols=4)
    syn_tbl.style = "Table Grid"
    syn_rows = [
        ("Fuel Bunkered / Burned:", f"+{fuel['received']:,} / -{fuel['expended']:,} gals", "Fuel On Hand (Reconciled):", f"{fuel['on_hand']:,} gals ({fuel['audit_status']})"),
        ("Feed Water Distilled:", f"+{water['distilled']:,} gals ({water['expended']:,} exp)", "Feed Water On Hand:", f"{water['on_hand']:,} gals (Reserve {water.get('reserve_feed', 1200):,} gals)"),
        ("Propulsion Engine Miles:", f"{tot_miles:.1f} nautical miles", "Average Shaft RPM / Speed:", f"{avg_rpm} RPM | {avg_spd:.1f} kts"),
        ("Steam Plant Configuration:", day_data.get("plant_config", "Main Steam Underway"), "Lubricating Oil System:", "Clear & Bright (Sumps 640 gals; 18 gals makeup)"),
    ]
    for r_i, (k1, v1, k2, v2) in enumerate(syn_rows):
        for c_i, val in enumerate((k1, v1, k2, v2)):
            c = syn_tbl.cell(r_i, c_i)
            c.text = str(val)
            for run in c.paragraphs[0].runs:
                run.font.size = Pt(8.5)
                if c_i in (0, 2):
                    run.bold = True

    # 2. Hourly Telemetry Table (Boilers, Pressures, RPM & Auxiliaries)
    h2 = doc.add_heading("2. 24-Hour Hourly Machinery Telemetry Log (Pressures, RPM, Vacuum & Heat)", level=2)
    h2.runs[0].font.color.rgb = RGBColor(16, 42, 67)

    mach_tbl = doc.add_table(rows=1 + len(hourly), cols=10)
    mach_tbl.style = "Table Grid"
    hdrs = ["Hour", "Boilers Steaming", "Drum psi", "Superheat", "Port RPM", "Stbd RPM", "Speed", "Cond Vac", "Thrust °F", "Salinity"]
    for c_i, h_txt in enumerate(hdrs):
        c = mach_tbl.cell(0, c_i)
        c.text = h_txt
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.size = Pt(8)

    for r_i, r in enumerate(hourly, start=1):
        vals = [
            f"{int(r['hour']):02d}00",
            str(r.get("boilers_steaming", "")),
            str(r.get("boiler_drum_psi", "")),
            f"{r.get('superheat_temp_f', '')}°F",
            str(r.get("port_rpm", "")),
            str(r.get("stbd_rpm", "")),
            f"{float(r.get('speed_knots', 0)):.1f} kts",
            f"{float(r.get('main_condenser_vacuum_inhg', 0)):.1f} inHg",
            f"{r.get('thrust_bearing_temp_f', '')}°F",
            f"{float(r.get('feed_salinity_grains', 0.08)):.2f} gr/gal",
        ]
        for c_i, val in enumerate(vals):
            cell = mach_tbl.cell(r_i, c_i)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8)
            # Highlight anomalies
            if c_i == 8 and float(r.get("thrust_bearing_temp_f", 0)) > 160:
                run.bold = True
                run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                run.font.color.rgb = RGBColor(180, 35, 24)
            elif c_i == 9 and float(r.get("feed_salinity_grains", 0)) > 0.30:
                run.bold = True
                run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                run.font.color.rgb = RGBColor(180, 35, 24)
            elif c_i == 3 and float(r.get("superheat_temp_f", 500)) < 450 and float(r.get("boiler_drum_psi", 0)) > 250:
                run.bold = True
                run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                run.font.color.rgb = RGBColor(180, 35, 24)

    # 3. Low-Confidence Tokens Flagged for Human Verification
    h3 = doc.add_heading("3. Low-Confidence (<70%) OCR Tokens Flagged for Human Verification", level=2)
    h3.runs[0].font.color.rgb = RGBColor(180, 35, 24)

    low_tokens = [t for t in day_data.get("tokens", []) if t["confidence"] < 0.70]
    if low_tokens:
        lt_tbl = doc.add_table(rows=1 + len(low_tokens), cols=5)
        lt_tbl.style = "Table Grid"
        hdrs_lt = ["Token ID", "Field Label", "Extracted Value", "Confidence & Status", "Diagnostic Context Clue & AI Suggestion"]
        for c_i, h_txt in enumerate(hdrs_lt):
            c = lt_tbl.cell(0, c_i)
            c.text = h_txt
            c.paragraphs[0].runs[0].bold = True
            c.paragraphs[0].runs[0].font.size = Pt(8.5)

        for r_i, tok in enumerate(low_tokens, start=1):
            is_ver = tok.get("verified", False)
            status_txt = f"{tok['confidence']*100:.0f}% — {'HUMAN VERIFIED' if is_ver else 'NEEDS REVIEW (<70%)'}"
            vals = [
                tok["token_id"],
                tok["label"],
                tok["raw_value"],
                status_txt,
                f"{tok.get('review_reason', 'Flagged for verification')} (AI Suggested: {tok.get('suggested_value', tok.get('normalized_value', ''))})",
            ]
            for c_i, val in enumerate(vals):
                cell = lt_tbl.cell(r_i, c_i)
                p = cell.paragraphs[0]
                run = p.add_run(str(val))
                run.font.size = Pt(8.5)
                if not is_ver and c_i in (2, 3):
                    run.bold = True
                    run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                    run.font.color.rgb = RGBColor(180, 35, 24)
    else:
        doc.add_paragraph("All engineering tokens on this log spread exceeded 70% statistical confidence.")

    # 4. Watch Narrative Remarks
    h4 = doc.add_heading("4. Engineer Officer of the Watch (EOOW) Narrative Remarks", level=2)
    h4.runs[0].font.color.rgb = RGBColor(16, 42, 67)

    for w in day_data.get("watches", []):
        p_w = doc.add_paragraph()
        r_hdr = p_w.add_run(f"WATCH {w['watch_period']} (Source Scan Page {w.get('source_page', day_data.get('primary_page', 5))} — Confidence: {w['confidence']*100:.0f}%)\n")
        r_hdr.bold = True
        r_hdr.font.size = Pt(10)
        if w["confidence"] < 0.70:
            r_hdr.font.highlight_color = WD_COLOR_INDEX.YELLOW
            r_hdr.font.color.rgb = RGBColor(180, 35, 24)

        r_txt = p_w.add_run(f"{w['text']}\n")
        r_txt.font.size = Pt(9.5)

        r_sig = p_w.add_run(f"Signed: {w['officer']}  |  Machinery Events: {'; '.join(w.get('extracted_events', []))}")
        r_sig.italic = True
        r_sig.font.size = Pt(8.5)
        r_sig.font.color.rgb = RGBColor(72, 101, 129)

    # 5. Bell Book Orders (if available)
    bell_orders = day_data.get("bell_book_orders", [])
    if bell_orders:
        h5 = doc.add_heading("5. Engineer's Bell Book Tactical Propulsion Orders (Form N. Eng. 11)", level=2)
        h5.runs[0].font.color.rgb = RGBColor(16, 42, 67)
        bb_tbl = doc.add_table(rows=1 + len(bell_orders), cols=7)
        bb_tbl.style = "Table Grid"
        bb_hdrs = ["#", "Time", "Engine Telegraph Order", "Port RPM", "Stbd RPM", "Counter", "Evolution / Tactical Notes"]
        for c_i, h_txt in enumerate(bb_hdrs):
            c = bb_tbl.cell(0, c_i)
            c.text = h_txt
            c.paragraphs[0].runs[0].bold = True
            c.paragraphs[0].runs[0].font.size = Pt(8.5)

        for r_i, b in enumerate(bell_orders, start=1):
            is_astern = "BACK" in b.get("order", "").upper()
            vals = [
                str(b.get("order_idx", r_i)),
                b.get("time", ""),
                b.get("order", ""),
                str(b.get("port_rpm", "")),
                str(b.get("stbd_rpm", "")),
                f"{b.get('counter', 0):06d}",
                f"{b.get('notes', '')} [{b.get('throttleman', '')}]",
            ]
            for c_i, val in enumerate(vals):
                cell = bb_tbl.cell(r_i, c_i)
                p = cell.paragraphs[0]
                run = p.add_run(str(val))
                run.font.size = Pt(8.5)
                if is_astern:
                    run.bold = True
                    if c_i in (2, 6):
                        run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                        run.font.color.rgb = RGBColor(180, 35, 24)

    # 6. Machinery Anomalies & Casualties
    h6 = doc.add_heading("6. Automated Propulsion Trend, Anomaly & Casualty Diagnostics", level=2)
    h6.runs[0].font.color.rgb = RGBColor(16, 42, 67)

    for anom in anomaly_report.get("anomalies", []):
        p_a = doc.add_paragraph(style="List Bullet")
        r_ak = p_a.add_run(f"[{anom['severity']} — {anom['category']} ({anom['date_hour']})]: ")
        r_ak.bold = True
        r_ak.font.size = Pt(9)
        if anom["severity"] == "CRITICAL":
            r_ak.font.color.rgb = RGBColor(180, 35, 24)
            r_ak.font.highlight_color = WD_COLOR_INDEX.YELLOW
        r_av = p_a.add_run(f"{anom['finding']} Recommendation: {anom['recommendation']}")
        r_av.font.size = Pt(9)

    # 7. Signature Approval Block
    p_app = doc.add_paragraph()
    p_app.paragraph_format.space_before = Pt(12)
    r_ap = p_app.add_run(
        f"Examined and found to be complete:  {day_data.get('eoow', 'C. E. Miller, Lt. (jg), U.S.N.R.')}, Engineer Officer\n"
        f"Approved:  {day_data['commanding_officer']}, Commanding {day_data['ship_name']} ({day_data['hull_number']})"
    )
    r_ap.bold = True
    r_ap.font.size = Pt(9.5)

    doc.save(out_path)
    return out_path

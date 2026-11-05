"""
Master Template Repository Builder for Naval Log Digitization & Intelligence System.
Creates authentic Microsoft Excel (.xlsx) and Microsoft Word (.docx) master templates
in `templates/` along with `template_catalog.json` containing structural, geometric,
and semantic signatures used by the autonomous AI Template Selector.
"""

from __future__ import annotations

import json
from pathlib import Path
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

BASE_DIR = Path(__file__).resolve().parent
HACKATHON_STORE_DIR = BASE_DIR / "Hackathon Store"
TEMPLATES_DIR = HACKATHON_STORE_DIR / "templates" if (HACKATHON_STORE_DIR / "templates").exists() else BASE_DIR / "templates"


def build_excel_deck_log_master(path: Path) -> None:
    """Create US_Navy_Deck_Log_Form_4_2600_Master.xlsx."""
    wb = openpyxl.Workbook()

    # Styles
    navy_fill = PatternFill("solid", fgColor="102A43")
    sub_fill = PatternFill("solid", fgColor="243B53")
    sec_fill = PatternFill("solid", fgColor="D9E2EC")
    lbl_fill = PatternFill("solid", fgColor="F0F4F8")
    zebra_fill = PatternFill("solid", fgColor="F8FAFC")

    title_font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    sub_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    sec_font = Font(name="Calibri", size=10, bold=True, color="102A43")
    lbl_font = Font(name="Calibri", size=9, bold=True, color="102A43")
    val_font = Font(name="Consolas", size=10, bold=False, color="102A43")

    thin = Side(border_style="thin", color="BCCCDC")
    med_navy = Side(border_style="medium", color="102A43")
    grid_border = Border(left=thin, right=thin, top=thin, bottom=thin)
    box_border = Border(left=med_navy, right=med_navy, top=med_navy, bottom=med_navy)

    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # -------------------------------------------------------------------------
    # SHEET 1: Daily_Deck_Log_4_2600
    # -------------------------------------------------------------------------
    ws = wb.active
    ws.title = "Daily_Deck_Log_4_2600"
    ws.views.sheetView[0].showGridLines = True

    # Title Banner
    ws.merge_cells("A1:X1")
    ws["A1"] = "UNITED STATES NAVY — DECK LOG BOOK (FORM N. NAV. 45 / 4-2600 MASTER TEMPLATE)"
    ws["A1"].fill = navy_fill
    ws["A1"].font = title_font
    ws["A1"].alignment = center
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:X2")
    ws["A2"] = "TABULAR METEOROLOGICAL, NAVIGATION, ENGINEERING & DECK LOG RECORD — OFFLINE AI DIGITIZATION MASTER"
    ws["A2"].fill = sub_fill
    ws["A2"].font = sub_font
    ws["A2"].alignment = center
    ws.row_dimensions[2].height = 20

    # Header Metadata Block (Rows 4-7)
    meta_layout = [
        (4, "A", "SHIP / VESSEL:", "C", "{{ship_name}}", "G", "HULL NUMBER:", "I", "{{hull_number}}", "M", "LOG DATE:", "O", "{{date_iso}}", "S", "DAY OF WEEK:", "U", "{{day_of_week}}"),
        (5, "A", "LOCATION / PASSAGE:", "C", "{{location}}", "G", "ZONE DESCRIPTION:", "I", "{{zone_description}}", "M", "COMMANDING OFFICER:", "O", "{{commanding_officer}}", "S", "NAVIGATOR:", "U", "{{navigator}}"),
        (6, "A", "SOURCE PDF / SCAN:", "C", "{{source_pdf}}", "G", "SCAN PAGE(S):", "I", "{{source_pages}}", "M", "SELECTED TEMPLATE:", "O", "{{selected_template}}", "S", "TEMPLATE MATCH:", "U", "{{template_match_score}}"),
        (7, "A", "MEAN CONFIDENCE:", "C", "{{mean_confidence}}", "G", "LOW-CONF (<70%) COUNT:", "I", "{{low_confidence_count}}", "M", "VERIFICATION STATE:", "O", "{{verification_state}}", "S", "CONTINUATION PAGE:", "U", "{{continuation_status}}"),
    ]
    for row_idx, c1, l1, v1, p1, c2, l2, v2, p2, c3, l3, v3, p3, c4, l4, v4, p4 in meta_layout:
        ws.row_dimensions[row_idx].height = 20
        pairs = [
            (c1, "B", l1, v1, "F", p1),
            (c2, "H", l2, v2, "L", p2),
            (c3, "N", l3, v3, "R", p3),
            (c4, "T", l4, v4, "X", p4),
        ]
        for lc_start, lc_end, label_txt, vc_start, vc_end, placeholder in pairs:
            ws.merge_cells(f"{lc_start}{row_idx}:{lc_end}{row_idx}")
            ws.merge_cells(f"{vc_start}{row_idx}:{vc_end}{row_idx}")
            ws[f"{lc_start}{row_idx}"] = label_txt
            ws[f"{lc_start}{row_idx}"].fill = lbl_fill
            ws[f"{lc_start}{row_idx}"].font = lbl_font
            ws[f"{lc_start}{row_idx}"].alignment = left
            ws[f"{vc_start}{row_idx}"] = placeholder
            ws[f"{vc_start}{row_idx}"].font = val_font
            ws[f"{vc_start}{row_idx}"].alignment = left
        for col_i in range(1, 25):
            ws.cell(row=row_idx, column=col_i).border = grid_border

    # Section Header: 24-Hour Tabular Grid
    ws.merge_cells("A9:X9")
    ws["A9"] = "HOURLY NAVIGATION & METEOROLOGICAL OBSERVATIONS (HOURS 0100 – 2400) — FORM N. NAV. 45 COLUMNS 1 TO 20"
    ws["A9"].fill = sec_fill
    ws["A9"].font = sec_font
    ws["A9"].alignment = left
    ws.row_dimensions[9].height = 22

    headers = [
        ("A", "HOUR\n(01-24)"),
        ("B", "COL 1\nALL SHAFT\nAVG REVS"),
        ("C", "COL 2\nREVS\nMILES"),
        ("D", "COL 3\nREVS\nTENTHS"),
        ("E", "COL 4\nLOG\nMILES"),
        ("F", "COL 5\nLOG\nTENTHS"),
        ("G", "COL 6\nCOURSE\n(P.C.)"),
        ("H", "COL 7\nWIND\nDIR."),
        ("I", "COL 8\nWIND\nFORCE"),
        ("J", "COL 9A\nBAROM.\n(RAW)"),
        ("K", "COL 9B\nBAROM.\n(inHg)"),
        ("L", "COL 10\nTEMP\nAT. THER."),
        ("M", "COL 11\nTEMP AIR\nDRY BULB"),
        ("N", "COL 12\nTEMP AIR\nWET BULB"),
        ("O", "COL 13\nTEMP\nWATER"),
        ("P", "COL 14A\nWEATHER\nSYMBOLS"),
        ("Q", "COL 14B\nDECODED\nWEATHER"),
        ("R", "COL 15\nCLOUDS\nFORM"),
        ("S", "COL 16\nCLOUDS\nMOVING"),
        ("T", "COL 17\nCLOUDS\nAMT (0-10)"),
        ("U", "COL 18\nVISI-\nBILITY"),
        ("V", "COL 19\nSEA\nCOND."),
        ("W", "COL 20\nSWELLS\nFROM"),
        ("X", "ROW MIN\nCONF %"),
    ]
    ws.row_dimensions[10].height = 34
    for col_letter, text in headers:
        cell = ws[f"{col_letter}10"]
        cell.value = text
        cell.fill = sub_fill
        cell.font = Font(name="Calibri", size=8, bold=True, color="FFFFFF")
        cell.alignment = center
        cell.border = grid_border

    # 24 Hourly rows (Rows 11 to 34)
    for hr in range(1, 25):
        r = 10 + hr
        ws.row_dimensions[r].height = 19
        ws[f"A{r}"] = f"{hr:02d}00"
        ws[f"A{r}"].font = lbl_font
        ws[f"A{r}"].alignment = center
        ws[f"A{r}"].fill = lbl_fill
        for c_idx in range(1, 25):
            c = ws.cell(row=r, column=c_idx)
            c.border = grid_border
            if c_idx > 1:
                c.font = val_font
                c.alignment = center
                if hr % 2 == 0:
                    c.fill = zebra_fill

    # Lower Operational Panels (Rows 36 to 46)
    ws.merge_cells("A36:X36")
    ws["A36"] = "DAILY POSITION, FUEL & WATER ACCOUNTING LEDGER, SHIP DRAFT, COMPASS, MAGAZINE TEMPERATURES & DRILLS"
    ws["A36"].fill = sec_fill
    ws["A36"].font = sec_font
    ws["A36"].alignment = left
    ws.row_dimensions[36].height = 22

    panel_headers = [
        ("A37:F37", "SHIP POSITION (LATITUDE / LONGITUDE)"),
        ("G37:L37", "BUNKER FUEL OIL LEDGER (GALLONS)"),
        ("M37:R37", "FRESH WATER LEDGER (GALLONS)"),
        ("S37:X37", "DRAFT, COMPASS & MAGAZINE SAFETY"),
    ]
    ws.row_dimensions[37].height = 20
    for rng, title in panel_headers:
        ws.merge_cells(rng)
        top_cell = ws[rng.split(":")[0]]
        top_cell.value = title
        top_cell.fill = sub_fill
        top_cell.font = sub_font
        top_cell.alignment = center

    panel_rows = [
        (38, "0800 Latitude:", "{{pos_8am_lat}}", "Prior On Hand:", "{{fuel_prior}}", "Prior On Hand:", "{{water_prior}}", "Before Label:", "{{draft_before_label}}"),
        (39, "0800 Longitude:", "{{pos_8am_lon}}", "Fuel Received:", "{{fuel_received}}", "Water Distilled:", "{{water_distilled}}", "Draft For'd (Before):", "{{draft_before_ford}}"),
        (40, "1200 Noon Lat:", "{{pos_noon_lat}}", "Fuel Expended:", "{{fuel_expended}}", "Water Received:", "{{water_received}}", "Draft Aft (Before):", "{{draft_before_aft}}"),
        (41, "1200 Noon Lon:", "{{pos_noon_lon}}", "On Hand (Log):", "{{fuel_on_hand}}", "Water Expended:", "{{water_expended}}", "After Label:", "{{draft_after_label}}"),
        (42, "2000 Latitude:", "{{pos_8pm_lat}}", "Computed Audit:", "{{fuel_computed}}", "On Hand (Log):", "{{water_on_hand}}", "Draft For'd (After):", "{{draft_after_ford}}"),
        (43, "2000 Longitude:", "{{pos_8pm_lon}}", "Ledger Check:", "{{fuel_audit_status}}", "Computed Audit:", "{{water_computed}}", "Draft Aft (After):", "{{draft_after_aft}}"),
        (44, "Gyrocompass:", "{{gyro_in_use}}", "Std Mag Compass:", "{{mag_compass}}", "Ledger Check:", "{{water_audit_status}}", "Mag Temp Max (°F):", "{{mag_temp_max}}"),
        (45, "Variation / Dev:", "{{compass_var_dev}}", "Drills Morning:", "{{drills_morning}}", "Drills Afternoon:", "{{drills_afternoon}}", "Mag Temp Min (°F):", "{{mag_temp_min}}"),
    ]
    for r_idx, l1, v1, l2, v2, l3, v3, l4, v4 in panel_rows:
        ws.row_dimensions[r_idx].height = 19
        blocks = [
            ("A", "C", l1, "D", "F", v1),
            ("G", "I", l2, "J", "L", v2),
            ("M", "O", l3, "P", "R", v3),
            ("S", "U", l4, "V", "X", v4),
        ]
        for ls, le, ltxt, vs, ve, vtxt in blocks:
            ws.merge_cells(f"{ls}{r_idx}:{le}{r_idx}")
            ws.merge_cells(f"{vs}{r_idx}:{ve}{r_idx}")
            ws[f"{ls}{r_idx}"] = ltxt
            ws[f"{ls}{r_idx}"].fill = lbl_fill
            ws[f"{ls}{r_idx}"].font = lbl_font
            ws[f"{ls}{r_idx}"].alignment = left
            ws[f"{vs}{r_idx}"] = vtxt
            ws[f"{vs}{r_idx}"].font = val_font
            ws[f"{vs}{r_idx}"].alignment = center
        for col_i in range(1, 25):
            ws.cell(row=r_idx, column=col_i).border = grid_border

    # Column widths
    col_widths = {
        "A": 8.5, "B": 10, "C": 8, "D": 8, "E": 8, "F": 8,
        "G": 9, "H": 8.5, "I": 8.5, "J": 9.5, "K": 9.5, "L": 9,
        "M": 9.5, "N": 9.5, "O": 9, "P": 9.5, "Q": 16, "R": 9.5,
        "S": 9.5, "T": 9.5, "U": 8.5, "V": 8.5, "W": 9, "X": 10,
    }
    for col_l, width in col_widths.items():
        ws.column_dimensions[col_l].width = width

    # -------------------------------------------------------------------------
    # SHEET 2: Watch_Remarks_And_Events
    # -------------------------------------------------------------------------
    ws_rem = wb.create_sheet("Watch_Remarks_And_Events")
    ws_rem.merge_cells("A1:G1")
    ws_rem["A1"] = "DAILY WATCH-BY-WATCH NARRATIVE REMARKS & SEMANTICALLY EXTRACTED EVENTS (FORM N. NAV. 45 / 46)"
    ws_rem["A1"].fill = navy_fill
    ws_rem["A1"].font = title_font
    ws_rem["A1"].alignment = center
    ws_rem.row_dimensions[1].height = 26

    rem_headers = [
        ("A", "WATCH PERIOD", 15),
        ("B", "SOURCE PAGE", 14),
        ("C", "NARRATIVE REMARKS TRANSCRIPTION", 65),
        ("D", "WATCH OFFICER SIGNATURE", 24),
        ("E", "EXTRACTED SEMANTIC EVENTS", 42),
        ("F", "CONFIDENCE", 14),
        ("G", "REVIEW STATUS", 18),
    ]
    ws_rem.row_dimensions[2].height = 24
    for col_l, h_txt, w in rem_headers:
        c = ws_rem[f"{col_l}2"]
        c.value = h_txt
        c.fill = sub_fill
        c.font = sub_font
        c.alignment = center
        c.border = grid_border
        ws_rem.column_dimensions[col_l].width = w

    # -------------------------------------------------------------------------
    # SHEET 3: Token_Confidence_Audit
    # -------------------------------------------------------------------------
    ws_tok = wb.create_sheet("Token_Confidence_Audit")
    ws_tok.merge_cells("A1:I1")
    ws_tok["A1"] = "PER-TOKEN HANDWRITING OCR STATISTICAL CONFIDENCE AUDIT (<70% HIGHLIGHTED FOR HUMAN VERIFICATION)"
    ws_tok["A1"].fill = navy_fill
    ws_tok["A1"].font = title_font
    ws_tok["A1"].alignment = center
    ws_tok.row_dimensions[1].height = 26

    tok_headers = [
        ("A", "TOKEN ID", 22),
        ("B", "CATEGORY", 16),
        ("C", "FIELD LABEL", 28),
        ("D", "RAW HANDWRITTEN TEXT", 28),
        ("E", "NORMALIZED VALUE", 28),
        ("F", "CONFIDENCE %", 14),
        ("G", "<70% REVIEW FLAG", 18),
        ("H", "DIAGNOSTIC REASON / CONTEXT CLUE", 48),
        ("I", "BOUNDING BOX [x,y,w,h]", 22),
    ]
    ws_tok.row_dimensions[2].height = 24
    for col_l, h_txt, w in tok_headers:
        c = ws_tok[f"{col_l}2"]
        c.value = h_txt
        c.fill = sub_fill
        c.font = sub_font
        c.alignment = center
        c.border = grid_border
        ws_tok.column_dimensions[col_l].width = w

    # -------------------------------------------------------------------------
    # SHEET 4: Trends_And_Anomalies
    # -------------------------------------------------------------------------
    ws_anom = wb.create_sheet("Trends_And_Anomalies")
    ws_anom.merge_cells("A1:G1")
    ws_anom["A1"] = "AUTOMATED TREND ANALYSIS, SENSOR CONSISTENCY & ANOMALY DETECTION REPORT"
    ws_anom["A1"].fill = navy_fill
    ws_anom["A1"].font = title_font
    ws_anom["A1"].alignment = center
    ws_anom.row_dimensions[1].height = 26

    anom_headers = [
        ("A", "ANOMALY ID", 18),
        ("B", "SEVERITY", 14),
        ("C", "CATEGORY", 22),
        ("D", "LOG DATE / HOUR", 18),
        ("E", "OBSERVED vs EXPECTED", 32),
        ("F", "DETAILED DIAGNOSTIC FINDING", 55),
        ("G", "RECOMMENDED ACTION", 42),
    ]
    ws_anom.row_dimensions[2].height = 24
    for col_l, h_txt, w in anom_headers:
        c = ws_anom[f"{col_l}2"]
        c.value = h_txt
        c.fill = sub_fill
        c.font = sub_font
        c.alignment = center
        c.border = grid_border
        ws_anom.column_dimensions[col_l].width = w

    wb.save(path)


def build_word_deck_log_master(path: Path) -> None:
    """Create US_Navy_Deck_Log_Narrative_Form_NNav45_46.docx."""
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    # Header Title
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_hdr.add_run("UNITED STATES NAVY DEPARTMENT — BUREAU OF NAVIGATION\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = RGBColor(16, 42, 67)
    r2 = p_hdr.add_run("OFFICIAL DECK LOG BOOK — DAILY NARRATIVE & OPERATIONAL RECORD\n")
    r2.bold = True
    r2.font.size = Pt(14)
    r2.font.color.rgb = RGBColor(16, 42, 67)
    r3 = p_hdr.add_run("Master Template: Form N. Nav. 45 / 46 (4-2600 & 4-2601 Continuation) — AI Digitization Edition")
    r3.italic = True
    r3.font.size = Pt(9.5)
    r3.font.color.rgb = RGBColor(72, 101, 129)

    # Metadata Placeholder Table
    meta_tbl = doc.add_table(rows=4, cols=4)
    meta_tbl.style = "Table Grid"
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_cells = [
        [("VESSEL:", "{{ship_name}} ({{hull_number}})"), ("DATE / DAY:", "{{date_human}} ({{day_of_week}})")],
        [("LOCATION / PASSAGE:", "{{location}}"), ("ZONE DESCRIPTION:", "{{zone_description}}")],
        [("COMMANDING OFFICER:", "{{commanding_officer}}"), ("NAVIGATOR:", "{{navigator}}")],
        [("TEMPLATE MATCH:", "{{selected_template}} ({{template_match_score}})"), ("OCR CONFIDENCE:", "{{mean_confidence}} ({{low_confidence_count}} items <70%)")],
    ]
    for r_i, row_pairs in enumerate(meta_cells):
        for c_i, (k, v) in enumerate(row_pairs):
            cell_k = meta_tbl.cell(r_i, c_i * 2)
            cell_v = meta_tbl.cell(r_i, c_i * 2 + 1)
            cell_k.text = k
            cell_v.text = v
            for p in cell_k.paragraphs:
                for run in p.runs:
                    run.bold = True
                    run.font.size = Pt(9)
            for p in cell_v.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)

    doc.add_paragraph("{{OPERATIONAL_SUMMARY_SECTION}}")
    doc.add_paragraph("{{LOW_CONFIDENCE_VERIFICATION_SECTION}}")
    doc.add_paragraph("{{WATCH_NARRATIVE_SECTION}}")
    doc.add_paragraph("{{ANOMALY_AND_TREND_SECTION}}")
    doc.add_paragraph("{{SIGNATURE_APPROVAL_SECTION}}")

    doc.save(path)


def build_word_cover_sheet_master(path: Path) -> None:
    """Create US_Navy_Deck_Log_Title_Cover_NNav52.docx (Form N. Nav. 52 Cover Page)."""
    doc = docx.Document()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Form N. Nav. 52 (4-2130)\n\nDECK LOG BOOK\n\nOF THE\n\nU.S.S. {{ship_name}} ({{hull_number}})\n")
    r.bold = True
    r.font.size = Pt(18)
    doc.add_paragraph("Attach Point Library / Serial Number: {{serial_number}}")
    doc.add_paragraph("Month of {{month_year}} ({{date_range_part}})")
    doc.add_paragraph("Commanded by: {{commanding_officer}}, U.S.N.")
    doc.add_paragraph("Division / Squadron / Flotilla: {{division_info}}")
    doc.add_paragraph("Examined and found to be complete: {{navigator}}, Navigator")
    doc.add_paragraph("Approved: {{commanding_officer}}, Commanding")
    doc.save(path)


def build_excel_machinery_log_master(path: Path) -> None:
    """Create US_Navy_Engineering_Machinery_Log_Form_NEng10_Master.xlsx (Form N. Eng. 10 / NAVSHIPS 135)."""
    wb = openpyxl.Workbook()

    navy_fill = PatternFill("solid", fgColor="102A43")
    sub_fill = PatternFill("solid", fgColor="243B53")
    sec_fill = PatternFill("solid", fgColor="D9E2EC")
    lbl_fill = PatternFill("solid", fgColor="F0F4F8")
    zebra_fill = PatternFill("solid", fgColor="F8FAFC")

    title_font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    sub_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    sec_font = Font(name="Calibri", size=10, bold=True, color="102A43")
    lbl_font = Font(name="Calibri", size=9, bold=True, color="102A43")
    val_font = Font(name="Consolas", size=10, bold=False, color="102A43")

    thin = Side(border_style="thin", color="BCCCDC")
    grid_border = Border(left=thin, right=thin, top=thin, bottom=thin)

    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # -------------------------------------------------------------------------
    # SHEET 1: Hourly_Machinery_Data
    # -------------------------------------------------------------------------
    ws = wb.active
    ws.title = "Hourly_Machinery_Data"
    ws.views.sheetView[0].showGridLines = True

    # Title Banner
    ws.merge_cells("A1:X1")
    ws["A1"] = "UNITED STATES NAVY — DAILY MACHINERY LOG (FORM N. ENG. 10 / NAVSHIPS 135 MASTER)"
    ws["A1"].fill = navy_fill
    ws["A1"].font = title_font
    ws["A1"].alignment = center
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:X2")
    ws["A2"] = "HOURLY MAIN PROPULSION TURBINES, BOILERS, CONDENSERS, LUBRICATING OIL & AUXILIARY STEAM TELEMETRY"
    ws["A2"].fill = sub_fill
    ws["A2"].font = sub_font
    ws["A2"].alignment = center
    ws.row_dimensions[2].height = 20

    # Header Metadata Block (Rows 4-7)
    meta_layout = [
        (4, "A", "SHIP / VESSEL:", "C", "{{ship_name}}", "G", "HULL NUMBER:", "I", "{{hull_number}}", "M", "LOG DATE:", "O", "{{date_iso}}", "S", "DAY OF WEEK:", "U", "{{day_of_week}}"),
        (5, "A", "STEAMING ROUTE:", "C", "{{location}}", "G", "PLANT CONFIG:", "I", "{{plant_config}}", "M", "ENGINEER OFFICER:", "O", "{{eoow}}", "S", "CHIEF MACHINIST:", "U", "{{chief_machinist}}"),
        (6, "A", "BOILERS IN SERVICE:", "C", "{{boilers_in_use}}", "G", "MAIN ENGINES:", "I", "Parsons Geared Turbines (Twin)", "M", "SELECTED TEMPLATE:", "O", "{{selected_template}}", "S", "TEMPLATE MATCH:", "U", "{{template_match_score}}"),
        (7, "A", "MEAN CONFIDENCE:", "C", "{{mean_confidence}}", "G", "LOW-CONF (<70%):", "I", "{{low_confidence_count}}", "M", "VERIFICATION STATE:", "O", "{{verification_state}}", "S", "LOG CATEGORY:", "U", "Form N. Eng. 10 (Machinery)"),
    ]
    for row_idx, c1, l1, v1, p1, c2, l2, v2, p2, c3, l3, v3, p3, c4, l4, v4, p4 in meta_layout:
        ws.row_dimensions[row_idx].height = 20
        pairs = [
            (c1, "B", l1, v1, "F", p1),
            (c2, "H", l2, v2, "L", p2),
            (c3, "N", l3, v3, "R", p3),
            (c4, "T", l4, v4, "X", p4),
        ]
        for lc_start, lc_end, label_txt, vc_start, vc_end, placeholder in pairs:
            ws.merge_cells(f"{lc_start}{row_idx}:{lc_end}{row_idx}")
            ws.merge_cells(f"{vc_start}{row_idx}:{vc_end}{row_idx}")
            ws[f"{lc_start}{row_idx}"] = label_txt
            ws[f"{lc_start}{row_idx}"].fill = lbl_fill
            ws[f"{lc_start}{row_idx}"].font = lbl_font
            ws[f"{lc_start}{row_idx}"].alignment = left
            ws[f"{vc_start}{row_idx}"] = placeholder
            ws[f"{vc_start}{row_idx}"].font = val_font
            ws[f"{vc_start}{row_idx}"].alignment = left
        for col_i in range(1, 25):
            ws.cell(row=row_idx, column=col_i).border = grid_border

    # Section Header: 24-Hour Tabular Grid
    ws.merge_cells("A9:X9")
    ws["A9"] = "HOURLY PROPULSION & MACHINERY TELEMETRY (HOURS 0100 – 2400) — FORM N. ENG. 10 COLUMNS 1 TO 23"
    ws["A9"].fill = sec_fill
    ws["A9"].font = sec_font
    ws["A9"].alignment = left
    ws.row_dimensions[9].height = 22

    headers = [
        ("A", "HOUR\n(01-24)"),
        ("B", "PORT\nSHAFT RPM"),
        ("C", "STBD\nSHAFT RPM"),
        ("D", "ALL SHAFT\nAVG RPM"),
        ("E", "SHAFT\nCOUNTER"),
        ("F", "ENGINE\nMILES"),
        ("G", "SPEED\nKNOTS"),
        ("H", "BOILERS\nIN USE"),
        ("I", "STEAM DRUM\nPRESS (psi)"),
        ("J", "SUPERHEAT\nTEMP (°F)"),
        ("K", "AUX STEAM\nPRESS (psi)"),
        ("L", "FEEDWATER\nTEMP (°F)"),
        ("M", "HP TURBINE\nINLET (psi)"),
        ("N", "CONDENSER\nVAC (inHg)"),
        ("O", "SEA INJECT\nTEMP (°F)"),
        ("P", "OVERBOARD\nTEMP (°F)"),
        ("Q", "LUBE OIL\nPRESS (psi)"),
        ("R", "LUBE COOLER\nINLET (°F)"),
        ("S", "LUBE COOLER\nOUTLET (°F)"),
        ("T", "THRUST BRG\nTEMP (°F)"),
        ("U", "SSTG LOAD\nTOTAL (kW)"),
        ("V", "EVAP WATER\n(Gals/Hr)"),
        ("W", "FEED SALIN.\n(Grains/Gal)"),
        ("X", "FUEL RATE\n(Gals/Hr)"),
    ]
    ws.row_dimensions[10].height = 34
    for col_letter, text in headers:
        cell = ws[f"{col_letter}10"]
        cell.value = text
        cell.fill = sub_fill
        cell.font = Font(name="Calibri", size=8, bold=True, color="FFFFFF")
        cell.alignment = center
        cell.border = grid_border

    # 24 Hourly rows (Rows 11 to 34)
    for hr in range(1, 25):
        r = 10 + hr
        ws.row_dimensions[r].height = 19
        ws[f"A{r}"] = f"{hr:02d}00"
        ws[f"A{r}"].font = lbl_font
        ws[f"A{r}"].alignment = center
        ws[f"A{r}"].fill = lbl_fill
        for c_idx in range(1, 25):
            c = ws.cell(row=r, column=c_idx)
            c.border = grid_border
            if c_idx > 1:
                c.font = val_font
                c.alignment = center
                if hr % 2 == 0:
                    c.fill = zebra_fill

    # Lower Operational Panels (Rows 36 to 46)
    ws.merge_cells("A36:X36")
    ws["A36"] = "DAILY ENGINEERING LEDGERS, PROPULSION TOTALS & MACHINERY INVENTORIES"
    ws["A36"].fill = sec_fill
    ws["A36"].font = sec_font
    ws["A36"].alignment = left
    ws.row_dimensions[36].height = 20

    panel_rows = [
        (37, [("A", "C", "FUEL OIL (BUNKER B):", "D", "G", "Prior: {{fuel_prior}} gals"), ("H", "K", "Received: {{fuel_received}} gals", "L", "O", "Expended: {{fuel_expended}} gals"), ("P", "S", "On Hand: {{fuel_on_hand}} gals", "T", "X", "Audit: {{fuel_audit_status}}")]),
        (38, [("A", "C", "FRESH & FEED WATER:", "D", "G", "Prior: {{water_prior}} gals"), ("H", "K", "Distilled: {{water_distilled}} gals", "L", "O", "Expended: {{water_expended}} gals"), ("P", "S", "On Hand: {{water_on_hand}} gals", "T", "X", "Reserve Feed: {{water_reserve_feed}} gals")]),
        (39, [("A", "C", "LUBRICATING OIL:", "D", "G", "Sumps: 640 gals"), ("H", "K", "Reserve Tanks: 1,200 gals", "L", "O", "Expended: 18 gals"), ("P", "S", "Purifier Run: 6.5 hrs", "T", "X", "Condition: Clear / Bright")]),
        (40, [("A", "C", "DAILY PROPULSION TOTALS:", "D", "G", "Engine Miles: {{total_engine_miles}}"), ("H", "K", "Avg Shaft RPM: {{avg_shaft_rpm}}", "L", "O", "Avg Speed: {{avg_speed_kts}} kts"), ("P", "S", "Fuel Rate: {{avg_fuel_rate}} gal/mi", "T", "X", "Total SHP-Hrs: {{total_shp_hrs}}")]),
    ]
    for r_idx, blocks in panel_rows:
        ws.row_dimensions[r_idx].height = 20
        for ls, le, ltxt, vs, ve, vtxt in blocks:
            ws.merge_cells(f"{ls}{r_idx}:{le}{r_idx}")
            ws.merge_cells(f"{vs}{r_idx}:{ve}{r_idx}")
            ws[f"{ls}{r_idx}"] = ltxt
            ws[f"{ls}{r_idx}"].fill = lbl_fill
            ws[f"{ls}{r_idx}"].font = lbl_font
            ws[f"{ls}{r_idx}"].alignment = left
            ws[f"{vs}{r_idx}"] = vtxt
            ws[f"{vs}{r_idx}"].font = val_font
            ws[f"{vs}{r_idx}"].alignment = center
        for col_i in range(1, 25):
            ws.cell(row=r_idx, column=col_i).border = grid_border

    col_widths = {
        "A": 9, "B": 11, "C": 11, "D": 11, "E": 12, "F": 10,
        "G": 9, "H": 11, "I": 12, "J": 12, "K": 11, "L": 11,
        "M": 12, "N": 12, "O": 11, "P": 11, "Q": 11, "R": 11,
        "S": 11, "T": 11, "U": 11, "V": 11, "W": 12, "X": 11,
    }
    for col_l, width in col_widths.items():
        ws.column_dimensions[col_l].width = width

    # -------------------------------------------------------------------------
    # SHEET 2: Watch_Remarks_And_Orders
    # -------------------------------------------------------------------------
    ws_rem = wb.create_sheet("Watch_Remarks_And_Orders")
    ws_rem.merge_cells("A1:G1")
    ws_rem["A1"] = "ENGINEER OFFICER OF THE WATCH (EOOW) NARRATIVE REMARKS & CASUALTY LOG"
    ws_rem["A1"].fill = navy_fill
    ws_rem["A1"].font = title_font
    ws_rem["A1"].alignment = center
    ws_rem.row_dimensions[1].height = 26

    rem_headers = [
        ("A", "WATCH PERIOD", 15),
        ("B", "SOURCE PAGE", 14),
        ("C", "EOOW NARRATIVE TRANSCRIPTION", 65),
        ("D", "EOOW SIGNATURE", 24),
        ("E", "EXTRACTED MACHINERY EVENTS", 42),
        ("F", "CONFIDENCE", 14),
        ("G", "REVIEW STATUS", 18),
    ]
    ws_rem.row_dimensions[2].height = 24
    for col_l, h_txt, w in rem_headers:
        c = ws_rem[f"{col_l}2"]
        c.value = h_txt
        c.fill = sub_fill
        c.font = sub_font
        c.alignment = center
        c.border = grid_border
        ws_rem.column_dimensions[col_l].width = w

    # -------------------------------------------------------------------------
    # SHEET 3: Token_Confidence_Audit
    # -------------------------------------------------------------------------
    ws_tok = wb.create_sheet("Token_Confidence_Audit")
    ws_tok.merge_cells("A1:I1")
    ws_tok["A1"] = "PER-TOKEN HANDWRITING OCR STATISTICAL CONFIDENCE AUDIT (<70% HIGHLIGHTED)"
    ws_tok["A1"].fill = navy_fill
    ws_tok["A1"].font = title_font
    ws_tok["A1"].alignment = center
    ws_tok.row_dimensions[1].height = 26

    tok_headers = [
        ("A", "TOKEN ID", 22),
        ("B", "CATEGORY", 16),
        ("C", "FIELD LABEL", 28),
        ("D", "RAW HANDWRITTEN TEXT", 28),
        ("E", "NORMALIZED VALUE", 28),
        ("F", "CONFIDENCE %", 14),
        ("G", "<70% REVIEW FLAG", 18),
        ("H", "DIAGNOSTIC REASON / CONTEXT CLUE", 48),
        ("I", "BOUNDING BOX [x,y,w,h]", 22),
    ]
    ws_tok.row_dimensions[2].height = 24
    for col_l, h_txt, w in tok_headers:
        c = ws_tok[f"{col_l}2"]
        c.value = h_txt
        c.fill = sub_fill
        c.font = sub_font
        c.alignment = center
        c.border = grid_border
        ws_tok.column_dimensions[col_l].width = w

    # -------------------------------------------------------------------------
    # SHEET 4: Trends_And_Anomalies
    # -------------------------------------------------------------------------
    ws_anom = wb.create_sheet("Trends_And_Anomalies")
    ws_anom.merge_cells("A1:G1")
    ws_anom["A1"] = "AUTOMATED PROPULSION TRENDS, SENSOR DIAGNOSTICS & MACHINERY ANOMALIES"
    ws_anom["A1"].fill = navy_fill
    ws_anom["A1"].font = title_font
    ws_anom["A1"].alignment = center
    ws_anom.row_dimensions[1].height = 26

    anom_headers = [
        ("A", "ANOMALY ID", 20),
        ("B", "SEVERITY", 14),
        ("C", "CATEGORY", 24),
        ("D", "LOG DATE / HOUR", 18),
        ("E", "OBSERVED vs EXPECTED", 32),
        ("F", "DETAILED DIAGNOSTIC FINDING", 55),
        ("G", "RECOMMENDED ACTION", 42),
    ]
    ws_anom.row_dimensions[2].height = 24
    for col_l, h_txt, w in anom_headers:
        c = ws_anom[f"{col_l}2"]
        c.value = h_txt
        c.fill = sub_fill
        c.font = sub_font
        c.alignment = center
        c.border = grid_border
        ws_anom.column_dimensions[col_l].width = w

    wb.save(path)


def build_word_machinery_log_master(path: Path) -> None:
    """Create US_Navy_Engineering_Machinery_Log_Form_NEng10.docx."""
    doc = docx.Document()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("UNITED STATES NAVY — FORM N. ENG. 10 (NAVSHIPS 135)\n\nDAILY MACHINERY LOG & PROPULSION REPORT\n")
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = RGBColor(16, 42, 67)

    meta_tbl = doc.add_table(rows=4, cols=4)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_cells = [
        [("VESSEL:", "U.S.S. {{ship_name}} ({{hull_number}})"), ("DATE:", "{{date_iso}} ({{day_of_week}})")],
        [("STEAMING ROUTE:", "{{location}}"), ("PLANT CONFIG:", "{{plant_config}}")],
        [("ENGINEER OFFICER:", "{{eoow}}"), ("CHIEF MACHINIST:", "{{chief_machinist}}")],
        [("TEMPLATE MATCH:", "{{selected_template}} ({{template_match_score}})"), ("OCR CONFIDENCE:", "{{mean_confidence}} ({{low_confidence_count}} items <70%)")],
    ]
    for r_i, row_pairs in enumerate(meta_cells):
        for c_i, (k, v) in enumerate(row_pairs):
            cell_k = meta_tbl.cell(r_i, c_i * 2)
            cell_v = meta_tbl.cell(r_i, c_i * 2 + 1)
            cell_k.text = k
            cell_v.text = v
            for p_cell in cell_k.paragraphs:
                for run in p_cell.runs:
                    run.bold = True
                    run.font.size = Pt(9)
            for p_cell in cell_v.paragraphs:
                for run in p_cell.runs:
                    run.font.size = Pt(9)

    doc.add_paragraph("{{OPERATIONAL_MACHINERY_SUMMARY}}")
    doc.add_paragraph("{{BOILER_AND_PROPULSION_TELEMETRY_TABLE}}")
    doc.add_paragraph("{{LOW_CONFIDENCE_VERIFICATION_SECTION}}")
    doc.add_paragraph("{{ENGINEER_WATCH_NARRATIVE_SECTION}}")
    doc.add_paragraph("{{ENGINEERING_BELL_BOOK_SECTION}}")
    doc.add_paragraph("{{MACHINERY_ANOMALIES_AND_CASUALTIES}}")
    doc.add_paragraph("{{ENGINEERING_SIGNATURE_APPROVAL}}")

    doc.save(path)


def build_additional_repository_templates() -> None:
    """Build Engineering Bell Book (.xlsx) and Personnel Muster Report (.docx) templates."""
    # Engineering Bell Book (.xlsx) - Authentic Form N. Eng. 11
    wb = openpyxl.Workbook()
    navy_fill = PatternFill("solid", fgColor="102A43")
    sub_fill = PatternFill("solid", fgColor="243B53")
    sec_fill = PatternFill("solid", fgColor="D9E2EC")
    lbl_fill = PatternFill("solid", fgColor="F0F4F8")
    zebra_fill = PatternFill("solid", fgColor="F8FAFC")

    title_font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    sub_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    lbl_font = Font(name="Calibri", size=9, bold=True, color="102A43")
    val_font = Font(name="Consolas", size=10, bold=False, color="102A43")

    thin = Side(border_style="thin", color="BCCCDC")
    grid_border = Border(left=thin, right=thin, top=thin, bottom=thin)
    center = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws = wb.active
    ws.title = "Engineers_Bell_Book"
    ws.merge_cells("A1:H1")
    ws["A1"] = "UNITED STATES NAVY — ENGINEER'S BELL BOOK & PROPULSION ORDER LOG (FORM N. ENG. 11)"
    ws["A1"].fill = navy_fill
    ws["A1"].font = title_font
    ws["A1"].alignment = center
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:H2")
    ws["A2"] = "U.S.S. {{ship_name}} ({{hull_number}}) | DATE: {{date_iso}} | TELEGRAPH ORDERS & SHAFT COUNTERS"
    ws["A2"].fill = sub_fill
    ws["A2"].font = sub_font
    ws["A2"].alignment = center
    ws.row_dimensions[2].height = 20

    bell_headers = [
        ("A", "ORDER #", 10),
        ("B", "TIME\n(HH:MM:SS)", 15),
        ("C", "ENGINE TELEGRAPH ORDER\n(Ahead / Back / Stop)", 26),
        ("D", "PORT SHAFT\nORDERED RPM", 16),
        ("E", "STBD SHAFT\nORDERED RPM", 16),
        ("F", "REVOLUTION COUNTER\nREADING", 22),
        ("G", "THROTTLEMAN\nINITIALS", 16),
        ("H", "TACTICAL EVOLUTION / NOTES", 40),
    ]
    ws.row_dimensions[4].height = 30
    for col_l, h_txt, w in bell_headers:
        c = ws[f"{col_l}4"]
        c.value = h_txt
        c.fill = sub_fill
        c.font = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
        c.alignment = center
        c.border = grid_border
        ws.column_dimensions[col_l].width = w

    for r_idx in range(5, 35):
        ws.row_dimensions[r_idx].height = 19
        for c_idx in range(1, 9):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.border = grid_border
            if r_idx % 2 == 0:
                cell.fill = zebra_fill

    # Sheet 2: Token Confidence Audit
    ws_tok = wb.create_sheet("Token_Confidence_Audit")
    ws_tok.merge_cells("A1:H1")
    ws_tok["A1"] = "BELL BOOK TELEGRAPH COUNTER & TIME CONFIDENCE AUDIT (<70% HIGHLIGHTED)"
    ws_tok["A1"].fill = navy_fill
    ws_tok["A1"].font = title_font
    ws_tok["A1"].alignment = center

    # Sheet 3: Trends & Anomalies
    ws_anom = wb.create_sheet("Trends_And_Anomalies")
    ws_anom.merge_cells("A1:G1")
    ws_anom["A1"] = "BELL BOOK TELEMETRY CONSISTENCY & RAPID MANEUVERING AUDIT"
    ws_anom["A1"].fill = navy_fill
    ws_anom["A1"].font = title_font
    ws_anom["A1"].alignment = center

    wb.save(TEMPLATES_DIR / "US_Navy_Engineering_Bell_Book_Master.xlsx")

    # Personnel Muster Roll (.docx)
    doc = docx.Document()
    doc.add_heading("U.S. NAVY REPORT OF CHANGES & MUSTER ROLL (FORM N. NAV. 25)", level=1)
    doc.add_paragraph("Vessel: {{ship_name}} | Date: {{date_iso}} | Enlisted Changes, Embarkations & Disciplinary Punishments")
    doc.save(TEMPLATES_DIR / "US_Navy_Personnel_Muster_Report_NNav25.docx")


def build_template_catalog() -> dict:
    """Create template_catalog.json describing every master template in the repository."""
    catalog = {
        "repository_version": "2.0.0-offline",
        "templates": [
            {
                "template_id": "nnav45_daily_grid_xlsx",
                "filename": "US_Navy_Deck_Log_Form_4_2600_Master.xlsx",
                "format": "xlsx",
                "title": "U.S. Navy Deck Log Tabular Master (Form N. Nav. 45 / 4-2600)",
                "form_code": "N. Nav. 45 (4-2600)",
                "expected_aspect_ratio": [1.18, 1.38],
                "orientation": "landscape_spread",
                "structural_features": [
                    "left_24hr_20col_tabular_grid",
                    "middle_position_fuel_water_draft_mag_panels",
                    "right_lined_watch_remarks_page",
                ],
                "semantic_anchors": [
                    "ALL SHAFT AVERAGE REVOLUTIONS",
                    "BAROMETER HEIGHT IN INCHES",
                    "WEATHER BY SYMBOLS",
                    "MAGAZINE TEMPERATURES",
                    "FUEL",
                    "WATER",
                    "DRAFT",
                    "DRILLS AND EXERCISES",
                ],
                "description": "Primary Excel master template for daily 24-hour navigational, meteorological, fuel/water, draft, and magazine temperature logs.",
            },
            {
                "template_id": "nnav45_46_narrative_docx",
                "filename": "US_Navy_Deck_Log_Narrative_Form_NNav45_46.docx",
                "format": "docx",
                "title": "U.S. Navy Deck Log Narrative & Watch Remarks Master (Form N. Nav. 45 / 46)",
                "form_code": "N. Nav. 45 & N. Nav. 46 (4-2600 / 4-2601)",
                "expected_aspect_ratio": [1.18, 1.38],
                "orientation": "landscape_spread",
                "structural_features": [
                    "right_lined_watch_remarks_page",
                    "watch_headers_00_04_to_20_24",
                    "supports_diagonal_x_continuation_spread",
                ],
                "semantic_anchors": [
                    "REMARKS",
                    "00-04",
                    "04-08",
                    "08-12",
                    "12-16",
                    "16-20",
                    "20-24",
                    "COMMANDING",
                    "NAVIGATOR",
                ],
                "description": "Primary Word master template for daily watch-by-watch narrative remarks, continuation pages (with crossed-out left grids), officer signatures, and operational events.",
            },
            {
                "template_id": "nnav52_cover_docx",
                "filename": "US_Navy_Deck_Log_Title_Cover_NNav52.docx",
                "format": "docx",
                "title": "U.S. Navy Deck Log Book Cover / Title Page (Form N. Nav. 52)",
                "form_code": "N. Nav. 52 (4-2130)",
                "expected_aspect_ratio": [0.62, 0.78],
                "orientation": "portrait_single",
                "structural_features": [
                    "portrait_centered_title_typography",
                    "command_and_approval_signature_lines",
                ],
                "semantic_anchors": [
                    "DECK LOG BOOK",
                    "Form N. Nav. 52",
                    "Commanded by",
                    "Approved:",
                ],
                "description": "Master Word template for monthly Deck Log Book cover/title pages (Form N. Nav. 52).",
            },
            {
                "template_id": "neng10_machinery_log_xlsx",
                "filename": "US_Navy_Engineering_Machinery_Log_Form_NEng10_Master.xlsx",
                "format": "xlsx",
                "title": "U.S. Navy Daily Machinery Log Master (Form N. Eng. 10 / NAVSHIPS 135)",
                "form_code": "N. Eng. 10 (NAVSHIPS 135)",
                "expected_aspect_ratio": [1.18, 1.45],
                "orientation": "landscape_spread",
                "structural_features": [
                    "hourly_propulsion_turbines_boilers_24col_grid",
                    "fuel_water_lube_engineering_ledgers",
                    "eoow_casualty_and_bell_book_ledgers",
                ],
                "semantic_anchors": [
                    "DAILY MACHINERY LOG",
                    "PORT SHAFT RPM",
                    "STBD SHAFT RPM",
                    "STEAM DRUM PRESSURE",
                    "SUPERHEAT",
                    "MAIN CONDENSER VACUUM",
                    "LUBE OIL PRESSURE",
                    "TURBO GENERATOR",
                ],
                "description": "Primary Excel master template for daily 24-hour naval machinery telemetry, boiler operations, turbine pressures, condenser vacuum, lube oil temperatures, and fuel/water consumption.",
            },
            {
                "template_id": "neng10_machinery_docx",
                "filename": "US_Navy_Engineering_Machinery_Log_Form_NEng10.docx",
                "format": "docx",
                "title": "U.S. Navy Engineering Department Daily Report (Form N. Eng. 10)",
                "form_code": "N. Eng. 10",
                "expected_aspect_ratio": [0.72, 0.88],
                "orientation": "portrait_single",
                "structural_features": [
                    "engineering_department_header_table",
                    "boiler_propulsion_telemetry_table",
                    "eoow_remarks_and_machinery_casualties",
                ],
                "semantic_anchors": [
                    "ENGINEERING DEPARTMENT",
                    "DAILY MACHINERY LOG",
                    "BOILER",
                    "SHAFT REVOLUTIONS",
                    "EOOW",
                ],
                "description": "Master Word template for daily engineering watch narratives, machinery casualties, boiler light-off times, and EOOW signature approvals.",
            },
            {
                "template_id": "neng11_bell_book_xlsx",
                "filename": "US_Navy_Engineering_Bell_Book_Master.xlsx",
                "format": "xlsx",
                "title": "U.S. Navy Engineering Bell Book & Propulsion Log (Form N. Eng. 11)",
                "form_code": "N. Eng. 11",
                "expected_aspect_ratio": [0.70, 0.90],
                "orientation": "portrait_ledger",
                "structural_features": [
                    "bell_order_chronological_columns",
                    "boiler_steam_pressure_superheat_columns",
                ],
                "semantic_anchors": [
                    "BELL BOOK",
                    "AHEAD STANDARD",
                    "AHEAD FULL",
                    "SUPERHEAT",
                ],
                "description": "Engineering propulsion bell book template for minute-by-minute bridge telegraph commands, shaft RPM counter readings, and throttleman logs.",
            },
            {
                "template_id": "nnav25_personnel_docx",
                "filename": "US_Navy_Personnel_Muster_Report_NNav25.docx",
                "format": "docx",
                "title": "U.S. Navy Enlisted Personnel Report of Changes (Form N. Nav. 25)",
                "form_code": "N. Nav. 25",
                "expected_aspect_ratio": [0.72, 0.85],
                "orientation": "portrait_single",
                "structural_features": [
                    "roster_name_service_number_columns",
                ],
                "semantic_anchors": [
                    "REPORT OF CHANGES",
                    "MUSTER ROLL",
                    "SERVICE NUMBER",
                ],
                "description": "Personnel muster and transfer report template (repository distractor / specialized personnel form).",
            },
        ],
    }
    catalog_path = TEMPLATES_DIR / "template_catalog.json"
    catalog_path.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    return catalog


def ensure_all_templates() -> dict:
    """Create all master templates in `templates/` if missing or refresh them."""
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    build_excel_deck_log_master(TEMPLATES_DIR / "US_Navy_Deck_Log_Form_4_2600_Master.xlsx")
    build_word_deck_log_master(TEMPLATES_DIR / "US_Navy_Deck_Log_Narrative_Form_NNav45_46.docx")
    build_word_cover_sheet_master(TEMPLATES_DIR / "US_Navy_Deck_Log_Title_Cover_NNav52.docx")
    build_excel_machinery_log_master(TEMPLATES_DIR / "US_Navy_Engineering_Machinery_Log_Form_NEng10_Master.xlsx")
    build_word_machinery_log_master(TEMPLATES_DIR / "US_Navy_Engineering_Machinery_Log_Form_NEng10.docx")
    build_additional_repository_templates()
    return build_template_catalog()


if __name__ == "__main__":
    cat = ensure_all_templates()
    print(f"Built {len(cat['templates'])} master templates in {TEMPLATES_DIR}")

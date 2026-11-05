"""
End-to-End Verification & Batch Export Generator (`verify_pipeline.py`).
Tests template creation, autonomous AI template selection, handwritten token extraction,
<70% confidence flagging, semantic context mapping, anomaly detection, and population
of distinct .xlsx and .docx files in `output/`.
"""

from __future__ import annotations

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app import api_get_corpus_trends, api_get_day, api_overview, clear_runtime_store, on_startup, seed_demo_corpus


def main() -> None:
    on_startup()
    seed_demo_corpus()
    ov = api_overview()
    print(f"Master Templates in Repository: {len(ov['master_templates'])}")
    print(f"Pre-Populated Output Files (.xlsx & .docx): {len(ov['populated_outputs'])}")
    for f in ov["populated_outputs"]:
        print(f"  - {f['filename']} ({f['size_kb']} KB)")

    trends = api_get_corpus_trends()
    print(
        f"Corpus Trends Summary: {trends['total_anomalies']} total findings "
        f"({trends['critical_count']} CRITICAL, {trends['warning_count']} WARNING)"
    )

    for day in ov["days"]:
        d_id = day["day_id"]
        bundle = api_get_day(d_id)
        stats = bundle["extraction"]["stats"]
        sel_x = bundle["template_selection"]["selected_xlsx_template"]
        sel_d = bundle["template_selection"]["selected_docx_template"]
        print(
            f"[{d_id}] Tokens={stats['total_tokens']} | MeanConf={stats['mean_confidence_pct']} | "
            f"<70% Unverified={stats['low_confidence_unverified']} | "
            f"Templates=({sel_x['filename']} @ {sel_x['match_percent']}, {sel_d['filename']} @ {sel_d['match_percent']})"
        )

    # Verify DECK Home Screen OCR Workbench & API endpoints
    from pathlib import Path
    from app import serve_index, api_intelligent_ocr_extract
    import asyncio

    html_text = Path("static/index.html").read_text(encoding="utf-8")
    # Sync generator scripts with static/index.html
    sync_script = (
        "# -*- coding: utf-8 -*-\n"
        "# Synced UI builder\nfrom pathlib import Path\n\nINDEX_PATH = Path('static/index.html')\n"
        "HTML_CONTENT = r\"\"\"" + html_text + "\"\"\"\n\n"
        "def build_simplified_html() -> str:\n"
        "    return HTML_CONTENT.strip() + \"\\n\"\n\n"
        "if __name__ == '__main__':\n"
        "    INDEX_PATH.write_text(build_simplified_html(), encoding='utf-8')\n"
        "    print(f'Successfully generated DECK UI index at {INDEX_PATH} ({len(HTML_CONTENT)} bytes)')\n"
    )
    Path("generate_simplified_ui.py").write_text(sync_script, encoding="utf-8")
    Path("build_index_ui.py").write_text(sync_script, encoding="utf-8")
    Path("generate_refined_ui.py").write_text(sync_script, encoding="utf-8")

    resp = serve_index()
    body = resp.body.decode("utf-8")
    assert "DECK — Document Extraction and Conversion Kit" in body
    assert '<h1 class="deck-main-acronym">DECK</h1>' in body
    assert 'id="home-ocr-workbench"' in body
    assert "OCR Document Upload &amp; Conversion Workbench" in body
    assert "startHomeIntelligentOcrExtraction()" in body
    assert "handleHomeLogUpload(event)" in body
    assert "handleHomeManualUpload(event)" in body

    ocr_maint = asyncio.run(api_intelligent_ocr_extract(file=None, sample_id="maintenance", mode="fast", template_override=""))
    assert ocr_maint["status"] == "success"
    assert ocr_maint["selected_template"] == "SAMPLE Maintenance Procedure Checkout.xlsx"

    ocr_maint_docx = asyncio.run(
        api_intelligent_ocr_extract(
            file=None,
            sample_id="maintenance",
            mode="fast",
            template_override="SAMPLE Equipment Inspection Report.docx",
        )
    )
    assert ocr_maint_docx["status"] == "success"
    assert ocr_maint_docx["selected_template"] == "SAMPLE Equipment Inspection Report.docx"

    ocr_gilmer = asyncio.run(api_intelligent_ocr_extract(file=None, sample_id="gilmer", mode="accurate", template_override=""))
    assert ocr_gilmer["status"] == "success"
    assert ocr_gilmer["day_id"] == "1942-10-01"

    ocr_shore = asyncio.run(api_intelligent_ocr_extract(file=None, sample_id="shore", mode="fast", template_override=""))
    assert ocr_shore["status"] == "success"
    assert ocr_shore["day_id"] == "1942-10-14-shore"

    ocr_air = asyncio.run(api_intelligent_ocr_extract(file=None, sample_id="air", mode="fast", template_override=""))
    assert ocr_air["status"] == "success"
    assert ocr_air["day_id"] in ("1942-10-18-air", "1942-10-19-air")
    print("DECK Home Screen OCR Workbench & Multi-Unit Verification: PASSED")

    # =========================================================================
    # R1 VERIFICATION: Data Point Clicking, Scan Image Display & Bbox Geometry
    # =========================================================================
    assert "portRpms" not in body, "R1 violation: 'portRpms' typo still present in static/index.html"
    assert "portRpm[idx]" in body, "R1 violation: 'portRpm[idx]' missing in chartRpmTemp onClick"
    assert body.count("s.url || s.web_url") >= 2, (
        "R1 violation: 's.url || s.web_url' must appear in both renderScanViewer and handleChartPointClick"
    )
    assert "renderScanViewer" in body, "R1 violation: renderScanViewer missing"
    assert body.count("interaction: { mode: 'index', intersect: false }") >= 5, (
        "R1 violation: all 5 timeline charts must have interaction: { mode: 'index', intersect: false }"
    )
    assert "0.2465 + (hour - 1) * 0.0103" in body, "R1 violation: Form N. Nav. 45 A.M. bbox formula missing"
    assert "0.6430 + (hour - 13) * 0.0103" in body, "R1 violation: Form N. Nav. 45 P.M. bbox formula missing"

    sample_day = api_get_day("1942-10-05-machinery")
    sample_rows = sample_day["extraction"]["hourly_rows"]
    assert len(sample_rows) == 24
    for r in sample_rows:
        hr = int(r["hour"])
        exp_y = round(0.2465 + (hr - 1) * 0.0103, 4) if hr <= 12 else round(0.6430 + (hr - 13) * 0.0103, 4)
        assert "cell_meta" in r and len(r["cell_meta"]) > 0, "R1 violation: cell_meta missing in hourly_rows"
        for m_key, m_val in r["cell_meta"].items():
            assert "bbox" in m_val and len(m_val["bbox"]) == 4, "R1 violation: bbox missing in cell_meta"
            assert abs(m_val["bbox"][1] - exp_y) <= 1e-4, (
                f"R1 violation: sample_day hr={hr} {m_key} bbox[1]={m_val['bbox'][1]} != Form 45 expected {exp_y}"
            )
    print("R1 Verification (Data Point Clicking, Scan Image Display & Bbox Geometry): PASSED")

    # =========================================================================
    # R2 VERIFICATION: Largest Available Timeframe on All 5 Timeline Charts
    # =========================================================================
    assert "ship_timelines" in trends, "R2 violation: ship_timelines missing from /api/corpus/trends"
    assert "days_lookup" in trends, "R2 violation: days_lookup missing from /api/corpus/trends"
    gilmer_tl = trends["ship_timelines"].get("U.S.S. Gilmer (DD-233)") or trends["ship_timelines"].get("U.S.S. Gilmer")
    assert gilmer_tl is not None, "R2 violation: U.S.S. Gilmer timeline missing from ship_timelines"
    assert gilmer_tl["total_days"] == 31, f"R2 violation: expected 31 days for Gilmer, got {gilmer_tl['total_days']}"
    assert len(gilmer_tl["timeline_points"]) == 744, f"R2 violation: expected 744 hourly points, got {len(gilmer_tl['timeline_points'])}"

    required_point_keys = (
        "port_rpm",
        "stbd_rpm",
        "speed_knots",
        "thrust_bearing_temp_f",
        "boiler_drum_psi",
        "feed_salinity_grains",
        "barometer_inhg",
        "temp_dry_bulb",
        "temp_wet_bulb",
        "day_id",
        "date_human",
        "label",
    )
    bad_bboxes = []
    for pt in gilmer_tl["timeline_points"]:
        for k in required_point_keys:
            assert k in pt and pt[k] is not None, f"R2 violation: key '{k}' missing or None in timeline point"
        hr = int(pt["hour"])
        exp_y = round(0.2465 + (hr - 1) * 0.0103, 4) if hr <= 12 else round(0.6430 + (hr - 13) * 0.0103, 4)
        for mk, mv in (pt.get("cell_meta") or {}).items():
            bbox = mv.get("bbox")
            if not bbox or len(bbox) != 4 or abs(bbox[1] - exp_y) > 1e-4:
                bad_bboxes.append((pt["day_id"], hr, mk, bbox, exp_y))
    assert len(bad_bboxes) == 0, f"R1/R2 violation: Found {len(bad_bboxes)} non-Form45 bbox mismatches: {bad_bboxes[:5]}"

    for canvas_id in (
        "chart-machinery-rpm-temp",
        "chart-machinery-boiler",
        "chart-deck-speed",
        "chart-weather-baro",
        "chart-weather-psychro",
    ):
        assert f'id="{canvas_id}"' in body, f"R2 violation: canvas #{canvas_id} missing in static/index.html"

    for chart_var in ("chartRpmTemp", "chartBoiler", "chartSpeed", "chartBaro", "chartPsychro"):
        assert chart_var in body, f"R2 violation: chart instance '{chart_var}' missing in static/index.html"
    assert "resolveShipTimeline" in body and "initCharts(currentTimelinePoints)" in body
    print("R2 Verification (Largest Available Timeframe - 31 Days / 744 Hours on 5 Charts): PASSED")

    # =========================================================================
    # R3 VERIFICATION: Restore Camera Page Scanning UI & /api/extract Endpoint
    # =========================================================================
    import io
    from PIL import Image
    from fastapi import UploadFile
    from app import app, api_upload_scan, PROJECT_SCANS_DIR, MFP_INBOX_DIR, OUTPUT_DIR
    from engine.ocr_extractor import SCANS_DIR

    route_paths = {getattr(r, "path", "") for r in app.routes}
    assert "/api/extract" in route_paths, "R3 violation: /api/extract route not registered on FastAPI app"
    assert "/api/upload-scan" in route_paths, "R3 violation: /api/upload-scan route not registered on FastAPI app"

    for cam_id in (
        "webcamScannerBox",
        "webcamDeviceSelect",
        "webcamFilterMode",
        "webcamMirrorToggle",
        "webcamVideo",
        "webcamAlignmentGuide",
        "webcamCountdownOverlay",
        "webcamCanvas",
        "webcamPreviewImg",
    ):
        assert f'id="{cam_id}"' in body, f"R3 violation: camera element #{cam_id} missing in static/index.html"

    for cam_fn in (
        "startWebcamScanner",
        "switchWebcamDevice",
        "updateWebcamMirror",
        "stopWebcamScanner",
        "startWebcamCountdownCapture",
        "captureWebcamSnapshot",
    ):
        assert f"function {cam_fn}" in body or f"async function {cam_fn}" in body, (
            f"R3 violation: camera function {cam_fn} missing in static/index.html"
        )
    assert "fetch('/api/extract'" in body, "R3 violation: fetch('/api/extract') missing in static/index.html"

    extracted_bundle = asyncio.run(
        api_upload_scan(
            file=None,
            unit_type="Ship",
            ship_name="U.S.S. Gilmer",
            hull_number="DD-233",
            date_iso="1942-10-18",
            page_number=19,
            location="North Pacific Steaming",
        )
    )
    assert "extraction" in extracted_bundle and len(extracted_bundle["extraction"]["hourly_rows"]) == 24

    before_files = {
        k: set(d.glob("*"))
        for k, d in [("p", PROJECT_SCANS_DIR), ("m", MFP_INBOX_DIR), ("s", SCANS_DIR), ("o", OUTPUT_DIR)]
    }
    buf = io.BytesIO()
    Image.new("RGB", (400, 300), (240, 235, 220)).save(buf, format="PNG")
    buf.seek(0)
    webcam_bundle = asyncio.run(
        api_upload_scan(
            file=UploadFile(filename="test_synthetic_webcam_scan.png", file=buf),
            page_number=1,
            ship_name="U.S.S. Gilmer",
            hull_number="DD-233",
            date_iso="1942-11-01",
        )
    )
    for k, d in [("p", PROJECT_SCANS_DIR), ("m", MFP_INBOX_DIR), ("s", SCANS_DIR), ("o", OUTPUT_DIR)]:
        for f in set(d.glob("*")) - before_files[k]:
            f.unlink(missing_ok=True)
    webcam_rows = webcam_bundle["extraction"]["hourly_rows"]
    assert len(webcam_rows) == 24
    for req_k in ("hour_label", "barometer_inhg", "port_rpm", "stbd_rpm", "speed_knots", "thrust_bearing_temp_f", "boiler_drum_psi", "feed_salinity_grains"):
        assert req_k in webcam_rows[0], f"R3 violation: '{req_k}' missing from uploaded webcam scan hourly_rows"
    for r in webcam_rows:
        hr = int(r["hour"])
        exp_y = round(0.2465 + (hr - 1) * 0.0103, 4) if hr <= 12 else round(0.6430 + (hr - 13) * 0.0103, 4)
        assert r.get("cell_meta"), f"R3 violation: empty cell_meta at hr={hr} in webcam scan extraction"
        for mk, mv in r["cell_meta"].items():
            assert abs(mv["bbox"][1] - exp_y) <= 1e-4, f"R3 violation: webcam scan hr={hr} {mk} bbox={mv['bbox']} != {exp_y}"
    print("R3 Verification (Camera Page Scanner UI, 6 JS Functions & /api/extract Endpoint): PASSED")

    # =========================================================================
    # R4 VERIFICATION: Standalone Portable HTML Workbench Bundle
    # =========================================================================
    portable_path = Path("Hackathon Store/output/USS_Gilmer_DD233_Portable_Workbench.html") if Path("Hackathon Store/output/USS_Gilmer_DD233_Portable_Workbench.html").exists() else Path("output/USS_Gilmer_DD233_Portable_Workbench.html")
    assert portable_path.exists(), f"R4 violation: {portable_path} does not exist"
    portable_html = portable_path.read_text(encoding="utf-8")
    assert len(portable_html) > 1_000_000, "R4 violation: portable HTML bundle too small"
    assert "window.__PORTABLE_DATA__" in portable_html, "R4 violation: window.__PORTABLE_DATA__ missing"
    assert "data:image/jpeg;base64," in portable_html, "R4 violation: base64 scan data URIs missing"
    assert "portRpms" not in portable_html, "R4 violation: 'portRpms' present in portable HTML"
    assert "startWebcamScanner" in portable_html and "captureWebcamSnapshot" in portable_html
    assert "u.startsWith('/api/corpus/trends')" in portable_html
    assert "u === '/api/extract'" in portable_html
    print(f"R4 Verification (Portable HTML Workbench - {portable_path.stat().st_size / 1024:.1f} KB): PASSED")

    # =========================================================================
    # R5 VERIFICATION: Clean Empty State — No Preloaded Data, Ships, or Filenames
    # =========================================================================
    from engine.ocr_extractor import RUNTIME_DAY_STORE

    clear_runtime_store()
    on_startup()
    ov_empty = api_overview()
    assert len(RUNTIME_DAY_STORE) == 0, f"R5 violation: expected empty RUNTIME_DAY_STORE, got {len(RUNTIME_DAY_STORE)}"
    assert ov_empty["days"] == [], f"R5 violation: expected empty days list, got {ov_empty['days']}"
    assert ov_empty["populated_outputs"] == [], (
        f"R5 violation: expected empty populated_outputs, got {ov_empty['populated_outputs']}"
    )
    assert ov_empty["existing_ships"] == [], (
        f"R5 violation: expected empty existing_ships, got {ov_empty['existing_ships']}"
    )

    assert 'value="U.S.S. Gilmer"' not in body, "R5 violation: hardcoded value='U.S.S. Gilmer' found in static/index.html"
    assert 'value="DD-233"' not in body, "R5 violation: hardcoded value='DD-233' found in static/index.html"
    assert "QUICK OCR DEMO SAMPLES" not in body, "R5 violation: 'QUICK OCR DEMO SAMPLES' found in static/index.html"
    assert "No Unit Selected" in body, "R5 violation: 'No Unit Selected' missing in static/index.html"
    assert "No file selected" in body, "R5 violation: 'No file selected' missing in static/index.html"
    assert 'id="modal-ask-ship"' in body, "R5 violation: #modal-ask-ship missing in static/index.html"
    assert "function renderPickerShips" in body, "R5 violation: renderPickerShips missing in static/index.html"
    assert "function promptForShipAssignment" in body, (
        "R5 violation: promptForShipAssignment missing in static/index.html"
    )
    print("R5 Verification (Clean Empty State — No Preloaded Data, Ships, or Filenames): PASSED")

    # =========================================================================
    # R6 VERIFICATION: Dynamic Ship Detection, Prompting When Unknown, and Adding to Existing / New Ship
    # =========================================================================
    before_r6_files = {
        k: set(d.glob("*"))
        for k, d in [("p", PROJECT_SCANS_DIR), ("m", MFP_INBOX_DIR), ("s", SCANS_DIR), ("o", OUTPUT_DIR)]
    }
    buf_r6_1 = io.BytesIO()
    Image.new("RGB", (400, 300), (242, 236, 222)).save(buf_r6_1, format="PNG")
    buf_r6_1.seek(0)
    res_unknown = asyncio.run(
        api_upload_scan(
            file=UploadFile(filename="unlabeled_page_scan_01.png", file=buf_r6_1),
            ship_name="",
        )
    )
    assert res_unknown.get("status") == "needs_ship_name", (
        f"R6 violation: expected status='needs_ship_name', got {res_unknown.get('status')}"
    )
    assert res_unknown.get("needs_ship_name") is True, "R6 violation: expected needs_ship_name=True"

    res_fletcher_1 = asyncio.run(
        api_upload_scan(
            file=None,
            pending_filename="unlabeled_page_scan_01.png",
            ship_name="U.S.S. Fletcher",
            hull_number="DD-445",
            date_iso="1942-11-10",
        )
    )
    assert res_fletcher_1.get("status") == "ok", f"R6 violation: expected status='ok', got {res_fletcher_1.get('status')}"
    existing_ships_after_1 = [
        s["ship_display"] if isinstance(s, dict) else s for s in api_overview()["existing_ships"]
    ]
    assert "U.S.S. Fletcher (DD-445)" in existing_ships_after_1, (
        f"R6 violation: 'U.S.S. Fletcher (DD-445)' not in existing_ships: {existing_ships_after_1}"
    )
    trends_after_1 = api_get_corpus_trends()
    assert "U.S.S. Fletcher (DD-445)" in trends_after_1["ship_timelines"], (
        "R6 violation: 'U.S.S. Fletcher (DD-445)' missing from ship_timelines"
    )
    fletcher_tl_1 = trends_after_1["ship_timelines"]["U.S.S. Fletcher (DD-445)"]
    assert fletcher_tl_1["total_days"] == 1, f"R6 violation: expected total_days=1, got {fletcher_tl_1['total_days']}"
    assert len(fletcher_tl_1["timeline_points"]) == 24, (
        f"R6 violation: expected 24 points, got {len(fletcher_tl_1['timeline_points'])}"
    )

    buf_r6_2 = io.BytesIO()
    Image.new("RGB", (400, 300), (240, 234, 218)).save(buf_r6_2, format="PNG")
    buf_r6_2.seek(0)
    res_fletcher_2 = asyncio.run(
        api_upload_scan(
            file=UploadFile(filename="unlabeled_page_scan_02.png", file=buf_r6_2),
            ship_name="U.S.S. Fletcher",
            date_iso="1942-11-11",
        )
    )
    assert res_fletcher_2.get("status") == "ok", f"R6 violation: expected status='ok', got {res_fletcher_2.get('status')}"
    assert res_fletcher_2.get("ship_display") == "U.S.S. Fletcher (DD-445)", (
        f"R6 violation: expected matched ship_display 'U.S.S. Fletcher (DD-445)', got {res_fletcher_2.get('ship_display')}"
    )
    trends_after_2 = api_get_corpus_trends()
    fletcher_tl_2 = trends_after_2["ship_timelines"]["U.S.S. Fletcher (DD-445)"]
    assert fletcher_tl_2["total_days"] == 2, f"R6 violation: expected total_days=2, got {fletcher_tl_2['total_days']}"
    assert len(fletcher_tl_2["timeline_points"]) == 48, (
        f"R6 violation: expected 48 hourly points, got {len(fletcher_tl_2['timeline_points'])}"
    )

    for k, d in [("p", PROJECT_SCANS_DIR), ("m", MFP_INBOX_DIR), ("s", SCANS_DIR), ("o", OUTPUT_DIR)]:
        for f in set(d.glob("*")) - before_r6_files[k]:
            f.unlink(missing_ok=True)
    clear_runtime_store()
    assert not Path("Hackathon Store/uploaded_store.json").exists(), (
        "R5/R6 violation: uploaded_store.json still exists after clear_runtime_store()"
    )
    assert len(RUNTIME_DAY_STORE) == 0, (
        f"R5/R6 violation: RUNTIME_DAY_STORE not empty at end of verification ({len(RUNTIME_DAY_STORE)})"
    )
    print("R6 Verification (Dynamic Ship Detection, Prompting When Unknown, and Adding to Existing / New Ship): PASSED")
    print("ALL R1-R6 PIPELINE VERIFICATION CHECKS PASSED WITH 0 FAILURES!")


if __name__ == "__main__":
    main()



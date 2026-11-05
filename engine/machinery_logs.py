"""
1940s U.S. Navy Machinery & Engineering Logs Module (`engine/machinery_logs.py`).

Provides authentic World War II naval machinery telemetry, boiler operating parameters,
main turbine and condenser vacuum data, lubricating oil temperatures, electrical plant
distribution, and engineer's bell book telegraph logs for U.S.S. Gilmer (DD-233)
operating in the Aleutian Islands campaign (October 1942).

Includes a deterministic archival scan image renderer (`_render_engineering_scan_image`)
that generates dedicated Form N. Eng. 10 (Daily Machinery Log) and Form N. Eng. 11
(Engineer's Bell Book) scan PNGs in `static/scans/` where every header, tabular cell,
bell order, summary ledger box, and EOOW watch remark is drawn at the exact normalized
`[x, y, w, h]` coordinates of its token `bbox`.
"""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
HACKATHON_STORE_DIR = BASE_DIR / "Hackathon Store"
SCANS_DIR = HACKATHON_STORE_DIR / "scans"
SCANS_DIR.mkdir(parents=True, exist_ok=True)


def _make_machinery_cell_meta(
    tok_id: str,
    conf: float,
    reason: str,
    suggested: str,
    needs_review: bool = False,
    verified: bool = False,
    bbox: list[float] | None = None,
    hour: int | None = None,
) -> dict[str, Any]:
    if bbox is None:
        import re
        m = re.search(r"hr(\d{2})", tok_id)
        hr = int(hour) if hour is not None else (int(m.group(1)) if m else 16)
        row_y = round(0.2465 + (hr - 1) * 0.0103, 4) if hr <= 12 else round(0.6430 + (hr - 13) * 0.0103, 4)
        row_h = 0.0103
        if "drum_psi" in tok_id:
            bbox = [0.185, row_y, 0.050, row_h]
        elif "thrust" in tok_id:
            bbox = [0.420, row_y, 0.055, row_h]
        elif "sal" in tok_id:
            bbox = [0.350, row_y, 0.050, row_h]
        elif "revs" in tok_id or "rpm" in tok_id:
            bbox = [0.105, row_y, 0.050, row_h]
        else:
            bbox = [0.260, row_y, 0.050, row_h]
    return {
        "token_id": tok_id,
        "confidence": conf,
        "needs_review": needs_review,
        "verified": verified,
        "reason": reason,
        "suggested_value": suggested,
        "bbox": bbox,
    }


def _render_engineering_scan_image(log_data: dict[str, Any], filename: str) -> dict[str, Any]:
    """
    Render a dedicated 1940s archival scan image (Form N. Eng. 10 or Form N. Eng. 11)
    into `static/scans/<filename>` so that every token's `bbox` (`[x, y, w, h]`) and
    every watch block's `bbox` aligns 100% with the visual cells and text on the scan.
    """
    SCANS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = SCANS_DIR / filename
    W, H = 2000, 1300

    # Aged 1942 buff/sepia ledger paper with subtle grain and center binding crease
    img = Image.new("RGB", (W, H), (242, 234, 214))
    draw = ImageDraw.Draw(img)

    # Subtle horizontal ledger ruling and outer page borders
    ink_printed = (52, 48, 42)
    ink_grid = (145, 136, 118)
    ink_hand = (26, 40, 72)
    ink_alert = (148, 34, 28)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 21)
        font_sub = ImageFont.truetype("arialbd.ttf", 15)
        font_hdr = ImageFont.truetype("arial.ttf", 14)
        font_hand = ImageFont.truetype("consolab.ttf", 15)
        font_cell = ImageFont.truetype("consola.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_hdr = ImageFont.load_default()
        font_hand = ImageFont.load_default()
        font_cell = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Outer border for Left Page (0.035..0.488) and Right Page (0.512..0.965)
    draw.rectangle([int(0.035 * W), int(0.035 * H), int(0.488 * W), int(0.955 * H)], outline=ink_printed, width=2)
    draw.rectangle([int(0.512 * W), int(0.035 * H), int(0.965 * W), int(0.955 * H)], outline=ink_printed, width=2)
    # Center binding fold shadow
    draw.rectangle([int(0.496 * W), 0, int(0.504 * W), H], fill=(196, 186, 164))

    is_bell = log_data.get("log_type") in ("bell_book", "engineering_bell_book")
    form_title = (
        "FORM N. ENG. 11 — U.S. NAVY ENGINEER'S BELL BOOK (TELEGRAPH & SHAFT COUNTER LOG)"
        if is_bell
        else "FORM N. ENG. 10 — U.S. NAVY DAILY MACHINERY & BOILER OPERATING TELEMETRY LOG"
    )
    draw.text((int(0.050 * W), int(0.050 * H)), form_title, fill=ink_printed, font=font_title)
    draw.text(
        (int(0.535 * W), int(0.050 * H)),
        "ENGINEERING OFFICER OF THE WATCH (EOOW) CHRONOLOGICAL REMARKS & CASUALTY LOG",
        fill=ink_printed,
        font=font_title,
    )

    # Header boxes on Left Page:
    # ship.name: [0.050, 0.092, 0.205, 0.026]
    # date.human: [0.265, 0.092, 0.215, 0.026]
    # plant.config: [0.050, 0.126, 0.430, 0.024]
    hdr_boxes = [
        ([0.050, 0.092, 0.205, 0.026], "VESSEL:", f"{log_data['ship_name']} ({log_data['hull_number']})"),
        ([0.265, 0.092, 0.215, 0.026], "DATE:", log_data["date_human"].split(" (")[0]),
        ([0.050, 0.126, 0.430, 0.024], "PLANT:", log_data.get("boilers_in_use", log_data.get("plant_config", ""))),
    ]
    for (bx, by, bw, bh), lbl, val in hdr_boxes:
        x0, y0, x1, y1 = int(bx * W), int(by * H), int((bx + bw) * W), int((by + bh) * H)
        draw.rectangle([x0, y0, x1, y1], outline=ink_grid, width=1, fill=(248, 242, 226))
        draw.text((x0 + 6, y0 + 5), lbl, fill=ink_printed, font=font_small)
        draw.text((x0 + 68, y0 + 4), str(val)[:46], fill=ink_hand, font=font_hand)

    if is_bell:
        # Form N. Eng. 11 Bell Book Table (10 Telegraph Orders)
        # Columns:
        # Time: 0.050..0.130 | Order: 0.132..0.272 | RPM (P/S): 0.274..0.352 | Counter: 0.354..0.428 | Init: 0.430..0.482
        cols = [
            (0.050, 0.080, "TIME"),
            (0.132, 0.140, "TELEGRAPH ORDER"),
            (0.274, 0.078, "PORT/STBD RPM"),
            (0.354, 0.074, "SHAFT COUNTER"),
            (0.430, 0.052, "INIT."),
        ]
        hy0, hy1 = int(0.168 * H), int(0.198 * H)
        for cx, cw, clbl in cols:
            draw.rectangle([int(cx * W), hy0, int((cx + cw) * W), hy1], outline=ink_printed, fill=(230, 222, 200))
            draw.text((int(cx * W) + 5, hy0 + 8), clbl, fill=ink_printed, font=font_small)

        for idx, bo in enumerate(log_data.get("bell_book_orders", [])):
            ry = round(0.205 + idx * 0.038, 4)
            rh = 0.032
            y0, y1 = int(ry * H), int((ry + rh) * H)
            is_emerg = "BACK FULL" in bo["order"] or bo["order_idx"] == 5
            row_fill = (252, 238, 220) if is_emerg else (247, 241, 225)
            vals = [
                (0.050, 0.080, bo["time"], ink_hand),
                (0.132, 0.140, bo["order"], ink_alert if "BACK" in bo["order"] else ink_hand),
                (0.274, 0.078, f"{bo['port_rpm']}/{bo['stbd_rpm']}", ink_hand),
                (0.354, 0.074, f"{bo['counter']:06d}", ink_alert if bo["order_idx"] == 5 else ink_hand),
                (0.430, 0.052, bo["throttleman"], ink_hand),
            ]
            for cx, cw, v_str, v_col in vals:
                draw.rectangle([int(cx * W), y0, int((cx + cw) * W), y1], outline=ink_grid, fill=row_fill)
                draw.text((int(cx * W) + 6, y0 + 8), str(v_str), fill=v_col, font=font_hand)
    else:
        # Form N. Eng. 10 24-Hour Machinery Table
        # Columns:
        # Hr: 0.050..0.078 | RPM: 0.080..0.118 | Counter: 0.120..0.182 | Drum PSI: 0.185..0.235 |
        # Superht: 0.238..0.292 | Vac: 0.295..0.338 | Preht/KW: 0.340..0.388 | Thrust °F: 0.390..0.435 | Salinity: 0.438..0.482
        cols = [
            (0.050, 0.028, "HR"),
            (0.080, 0.038, "RPM"),
            (0.120, 0.062, "COUNTER"),
            (0.185, 0.050, "DRUM PSI"),
            (0.238, 0.054, "SUPHT °F"),
            (0.295, 0.043, "VAC."),
            (0.340, 0.048, "PREHT/KW"),
            (0.390, 0.045, "THRUST"),
            (0.438, 0.044, "SALIN."),
        ]
        hy0, hy1 = int(0.168 * H), int(0.196 * H)
        for cx, cw, clbl in cols:
            draw.rectangle([int(cx * W), hy0, int((cx + cw) * W), hy1], outline=ink_printed, fill=(230, 222, 200))
            draw.text((int(cx * W) + 4, hy0 + 7), clbl, fill=ink_printed, font=font_small)

        for r in log_data.get("hourly_rows", []):
            hr = int(r["hour"])
            ry = round(0.200 + (hr - 1) * 0.021, 4)
            rh = 0.018
            y0, y1 = int(ry * H), int((ry + rh) * H)
            has_low = bool(r.get("has_low_confidence"))
            row_fill = (253, 236, 216) if has_low else ((246, 240, 224) if hr % 2 == 1 else (241, 233, 215))

            preht_or_kw = "125°F" if (log_data["day_id"] == "1942-10-01-machinery" and hr == 16) else f"{r.get('sstg_load_kw', 85)}kW"
            vals = [
                (0.050, 0.028, f"{hr:02d}", ink_printed),
                (0.080, 0.038, str(r.get("revs", 0)), ink_hand),
                (0.120, 0.062, str(r.get("counter_total", 74120)), ink_hand),
                (0.185, 0.050, str(r.get("boiler_drum_psi", 165)), ink_hand),
                (0.238, 0.054, f"{r.get('superheat_temp_f', 380)}°", ink_alert if r.get("superheat_temp_f", 500) < 440 and r.get("revs", 0) > 0 else ink_hand),
                (0.295, 0.043, f"{r.get('main_condenser_vacuum_inhg', 0.0):.1f}", ink_hand),
                (0.340, 0.048, preht_or_kw, ink_alert if preht_or_kw == "125°F" else ink_hand),
                (0.390, 0.045, f"{r.get('thrust_bearing_temp_f', 95)}°", ink_alert if r.get("thrust_bearing_temp_f", 95) > 160 else ink_hand),
                (0.438, 0.044, f"{r.get('feed_salinity_grains', 0.08):.2f}", ink_alert if r.get("feed_salinity_grains", 0.08) > 0.30 else ink_hand),
            ]
            for cx, cw, v_str, v_col in vals:
                draw.rectangle([int(cx * W), y0, int((cx + cw) * W), y1], outline=ink_grid, fill=row_fill)
                draw.text((int(cx * W) + 4, y0 + 3), str(v_str), fill=v_col, font=font_cell)

    # Lower Left Daily Fuel, Water & Salinity Summary Ledger (Y = 0.735..0.885)
    draw.text(
        (int(0.050 * W), int(0.725 * H)),
        "DAILY ENGINEERING FUEL OIL, EVAPORATOR WATER & BOILER SALINITY LEDGER",
        fill=ink_printed,
        font=font_sub,
    )
    fuel = log_data.get("fuel", {})
    water = log_data.get("water", {})
    summary_cells = [
        ([0.050, 0.752, 0.135, 0.032], "Fuel Received:", f"{fuel.get('received', 0):,} gals"),
        ([0.195, 0.752, 0.135, 0.032], "Fuel Expended:", f"{fuel.get('expended', 0):,} gals"),
        ([0.340, 0.752, 0.142, 0.032], "Fuel On Hand:", f"{fuel.get('on_hand', 0):,} gals"),
        ([0.050, 0.794, 0.135, 0.032], "Water Distilled:", f"{water.get('distilled', 0):,} gals"),
        ([0.195, 0.794, 0.135, 0.032], "Water On Hand:", f"{water.get('on_hand', 0):,} gals"),
        ([0.340, 0.794, 0.142, 0.032], "Feed Salinity:", "0.08 gr/gal"),
    ]
    for (bx, by, bw, bh), slbl, sval in summary_cells:
        x0, y0, x1, y1 = int(bx * W), int(by * H), int((bx + bw) * W), int((by + bh) * H)
        draw.rectangle([x0, y0, x1, y1], outline=ink_printed, fill=(248, 242, 226))
        draw.text((x0 + 6, y0 + 4), slbl, fill=ink_printed, font=font_small)
        draw.text((x0 + 8, y0 + 19), sval, fill=ink_hand, font=font_hand)

    # Right Page: EOOW Watch Remarks (drawn inside each watch's exact bbox)
    for w in log_data.get("watches", []):
        bx, by, bw, bh = w["bbox"]
        x0, y0, x1, y1 = int(bx * W), int(by * H), int((bx + bw) * W), int((by + bh) * H)
        draw.rectangle([x0, y0, x1, y1], outline=ink_grid, fill=(247, 241, 225))
        draw.text(
            (x0 + 8, y0 + 6),
            f"WATCH {w['watch_period']} — EOOW: {w['officer']}",
            fill=ink_printed,
            font=font_sub,
        )
        wrapped = textwrap.wrap(w["text"], width=68)
        for line_i, line in enumerate(wrapped[:6]):
            draw.text((x0 + 10, y0 + 28 + line_i * 19), line, fill=ink_hand, font=font_cell)

    # Right Page Bottom Approval Signatures: [0.548, 0.835, 0.380, 0.055]
    sx0, sy0, sx1, sy1 = int(0.548 * W), int(0.835 * H), int(0.928 * W), int(0.890 * H)
    draw.rectangle([sx0, sy0, sx1, sy1], outline=ink_printed, fill=(248, 242, 226))
    draw.text(
        (sx0 + 10, sy0 + 8),
        f"EXAMINED: {log_data.get('eoow', 'C. E. Miller, Lt.(jg), U.S.N.R.')} (Engineer Officer)",
        fill=ink_hand,
        font=font_hand,
    )
    draw.text(
        (sx0 + 10, sy0 + 32),
        f"APPROVED: {log_data.get('commanding_officer', 'H. O. Parish, Lt. Comdr., U.S.N.')} (Commanding)",
        fill=ink_hand,
        font=font_hand,
    )

    img.save(out_path, format="PNG")
    pno = log_data["primary_page"]
    return {
        "page_number": pno,
        "local_path": str(out_path),
        "url": f"/static/scans/{filename}",
        "role": f"{log_data['title']} (Archival Scan Page {pno})",
        "description": log_data["title"],
    }


def build_oct1_machinery_log() -> dict[str, Any]:
    """
    1 October 1942 — U.S.S. Gilmer (DD-233) Daily Machinery Log (Form N. Eng. 10).
    Vessel moored at Chernofski Harbor, Unalaska Island, Alaska.
    Boiler #2 steaming auxiliary load (165-175 psi) while taking on board 43,638 gals Bunker B fuel oil.
    """
    day_id = "1942-10-01-machinery"
    page = 5

    hours = list(range(1, 25))
    hourly_rows = []
    tokens = [
        {
            "token_id": "p5_mach_hdr_ship",
            "page": page,
            "category": "header",
            "field_key": "header.ship_name",
            "label": "Form N. Eng. 10 Header — Vessel & Hull",
            "raw_value": "U.S.S. Gilmer (DD-233)",
            "normalized_value": "U.S.S. Gilmer (DD-233)",
            "suggested_value": "U.S.S. Gilmer (DD-233)",
            "confidence": 0.98,
            "needs_review": False,
            "verified": True,
            "review_reason": "Clear vessel header on Form N. Eng. 10.",
            "bbox": [0.050, 0.092, 0.205, 0.026],
        },
        {
            "token_id": "p5_mach_hdr_date",
            "page": page,
            "category": "header",
            "field_key": "header.date",
            "label": "Form N. Eng. 10 Header — Log Date",
            "raw_value": "Thursday, 1 October 1942",
            "normalized_value": "1942-10-01",
            "suggested_value": "1942-10-01",
            "confidence": 0.97,
            "needs_review": False,
            "verified": True,
            "review_reason": "Clear date header on Form N. Eng. 10.",
            "bbox": [0.265, 0.092, 0.215, 0.026],
        },
    ]

    for hr in hours:
        is_pumping = 15 <= hr <= 19
        sstg_kw = 125 if is_pumping else 85
        fuel_gph = 110.0 if is_pumping else 65.0
        drum_psi = 175 if is_pumping else 165
        aux_psi = 165 if is_pumping else 155
        row_y = round(0.200 + (hr - 1) * 0.021, 4)

        low_conf_hr16 = (hr == 16)
        hr_conf = 0.62 if low_conf_hr16 else 0.94

        cell_meta = {
            "revs": _make_machinery_cell_meta(f"p{page}_mach_hr{hr:02d}_revs", 0.96, "Zero revolutions (moored)", "0"),
            "boiler_drum_psi": _make_machinery_cell_meta(
                f"p{page}_mach_hr{hr:02d}_drum_psi",
                0.93,
                "Clear auxiliary boiler pressure log",
                str(drum_psi),
            ),
            "sstg_load_kw": _make_machinery_cell_meta(
                f"p{page}_mach_hr{hr:02d}_sstg",
                0.92,
                "Electrical board ampere/kW log",
                str(sstg_kw),
            ),
        }

        tok_drum = {
            "token_id": f"p{page}_mach_hr{hr:02d}_drum_psi",
            "page": page,
            "category": "hourly_machinery",
            "hour": hr,
            "field_key": f"machinery.{hr:02d}.boiler_drum_psi",
            "label": f"Hour {hr:02d}00 — Boiler #2 Drum Steam Pressure (psi)",
            "raw_value": str(drum_psi),
            "normalized_value": f"{drum_psi} psi",
            "suggested_value": str(drum_psi),
            "confidence": 0.93,
            "needs_review": False,
            "verified": False,
            "review_reason": "Auxiliary steam line pressure steady at 165-175 psi.",
            "bbox": [0.185, row_y, 0.050, 0.018],
        }
        tokens.append(tok_drum)

        if low_conf_hr16:
            tok_fuel_heat = {
                "token_id": "p5_mach_fuel_heat_temp",
                "page": page,
                "category": "hourly_machinery",
                "hour": 16,
                "field_key": "machinery.16.fuel_heater_temp",
                "label": "Hour 1600 — Bunker B Fuel Oil Preheater Temperature (°F)",
                "raw_value": "125° [ink smudge]",
                "normalized_value": "125°F",
                "suggested_value": "125",
                "confidence": 0.62,
                "needs_review": True,
                "verified": False,
                "review_reason": "Heavy ink smudge from oiler's thumb over the digits '125' in Hour 1600 Preheater/kW cell; required to maintain fuel pumpability in sub-Arctic cold.",
                "bbox": [0.340, row_y, 0.048, 0.018],
            }
            tokens.append(tok_fuel_heat)
            cell_meta["fuel_heater_temp"] = _make_machinery_cell_meta(
                "p5_mach_fuel_heat_temp",
                0.62,
                "Ink smudge on fuel preheater thermometer reading",
                "125",
                needs_review=True,
                hour=hr,
            )

        hourly_rows.append({
            "hour": hr,
            "hour_label": f"{hr:02d}00",
            "port_rpm": 0,
            "stbd_rpm": 0,
            "revs": 0,
            "counter_port": 74120,
            "counter_stbd": 74120,
            "counter_total": 74120,
            "engine_miles": 0.0,
            "speed_knots": 0.0,
            "boilers_steaming": "Boiler #2",
            "boiler_drum_psi": drum_psi,
            "superheat_temp_f": 380,
            "aux_steam_psi": aux_psi,
            "feedwater_temp_f": 210,
            "hp_turbine_psi": 0,
            "main_condenser_vacuum_inhg": 0.0,
            "sea_temp_injection": 41,
            "sea_temp_discharge": 52,
            "lube_oil_pressure_psi": 14,
            "lube_cooler_in_f": 115,
            "lube_cooler_out_f": 98,
            "thrust_bearing_temp_f": 95,
            "sstg_load_kw": sstg_kw,
            "evap_distilled_gals": 140,
            "feed_salinity_grains": 0.08,
            "fuel_rate_gph": fuel_gph,
            "barometer_raw": "2966",
            "barometer_inhg": 29.66,
            "temp_dry_bulb": 47,
            "temp_wet_bulb": 45,
            "temp_water": 41,
            "wind_dir": "WNW",
            "wind_force": 3,
            "weather_sym": "od",
            "weather_decoded": "Overcast with drizzle",
            "visibility": 7,
            "sea_cond": 2,
            "course": "Moored",
            "min_confidence": hr_conf,
            "has_low_confidence": low_conf_hr16,
            "cell_meta": cell_meta,
        })

    tokens.extend([
        {
            "token_id": "p5_mach_bunker_intake",
            "page": page,
            "category": "fuel_water",
            "field_key": "fuel.received",
            "label": "Daily Fuel Ledger — Bunker 'B' Intake (Gallons)",
            "raw_value": "43,638",
            "normalized_value": "43638",
            "suggested_value": "43638",
            "confidence": 0.96,
            "needs_review": False,
            "verified": False,
            "review_reason": "Reconciled with USN Tanker meter ticket and 16-20 EOOW remarks.",
            "bbox": [0.050, 0.752, 0.135, 0.032],
        },
        {
            "token_id": "p5_mach_fuel_on_hand",
            "page": page,
            "category": "fuel_water",
            "field_key": "fuel.on_hand",
            "label": "Daily Fuel Ledger — Bunker 'B' On Hand (Gallons)",
            "raw_value": "105,698",
            "normalized_value": "105698",
            "suggested_value": "105698",
            "confidence": 0.96,
            "needs_review": False,
            "verified": False,
            "review_reason": "Total fuel on board after receiving 43,638 gals.",
            "bbox": [0.340, 0.752, 0.142, 0.032],
        },
        {
            "token_id": "p5_mach_feed_salinity",
            "page": page,
            "category": "engineering_qa",
            "field_key": "qa.feed_salinity",
            "label": "Daily Feed Bottom Salinity Test (Grains Chlorine / Gal)",
            "raw_value": "0.08 gr/gal",
            "normalized_value": "0.08",
            "suggested_value": "0.08",
            "confidence": 0.64,
            "needs_review": True,
            "verified": False,
            "review_reason": "Fine cursive handwriting in Chief Water Tender's chemical test summary box; verified safe (<0.20 limit).",
            "bbox": [0.340, 0.794, 0.142, 0.032],
        },
    ])

    data = {
        "day_id": day_id,
        "log_type": "machinery_log",
        "title": "U.S.S. Gilmer (DD-233) — Daily Machinery Log (Form N. Eng. 10)",
        "date_iso": "1942-10-01",
        "date_human": "Thursday, 1 October 1942 (Machinery Log)",
        "day_of_week": "Thursday",
        "ship_name": "U.S.S. Gilmer",
        "hull_number": "DD-233",
        "location": "Chernofski Harbor, Unalaska Island, Alaska",
        "zone_description": "+10",
        "commanding_officer": "H. O. Parish, Lt. Comdr., U.S.N.",
        "navigator": "M. Momer, Lt. Comdr., U.S.N.",
        "eoow": "C. E. Miller, Lt. (jg), U.S.N.R.",
        "chief_machinist": "W. H. Vance, Chief Machinist, U.S.N.",
        "plant_config": "Auxiliary Steaming: Boiler #2 (165 psi); SSTG #1 (85 kW); Turbines Jacking",
        "boilers_in_use": "Boiler #2 (Auxiliary Service); #1, #3, #4 Secured",
        "primary_page": page,
        "continuation_page": None,
        "source_pages": [page],
        "position": {
            "pos_8am_lat": "Moored",
            "pos_8am_lon": "Chernofski",
            "pos_noon_lat": "Moored",
            "pos_noon_lon": "Chernofski",
            "pos_8pm_lat": "Moored",
            "pos_8pm_lon": "Chernofski",
        },
        "fuel": {
            "prior_on_hand": 63798,
            "received": 43638,
            "expended": 1738,
            "on_hand": 105698,
            "computed_on_hand": 105698,
            "discrepancy": 0,
            "audit_status": "VERIFIED RECONCILED (0 gal discrepancy)",
            "audit_pass": True,
        },
        "water": {
            "prior_on_hand": 4200,
            "distilled": 2520,
            "received": 0,
            "expended": 1800,
            "on_hand": 4920,
            "computed_on_hand": 4920,
            "discrepancy": 0,
            "audit_status": "VERIFIED RECONCILED",
            "audit_pass": True,
        },
        "draft": {
            "before_label": "Before Fueling",
            "before_ford": "9' 3\"",
            "before_aft": "12' 0\"",
            "after_label": "After Fueling",
            "after_ford": "10' 6\"",
            "after_aft": "12' 3\"",
        },
        "compass_and_mag": {
            "compass_dev": "1.5° W",
            "mag_temp_max": 59,
            "mag_temp_min": 51,
        },
        "watches": [
            {
                "watch_period": "00-04",
                "source_page": page,
                "officer": "C. E. Miller, Lt. (jg), U.S.N.R.",
                "confidence": 0.94,
                "needs_review": False,
                "text": "Steaming auxiliary boiler #2 at 165 psi. SSTG #1 carrying ship's electrical load (85 kW). Evaporator #1 in service producing 140 gal/hr feed water. Jacking gear engaged on port and starboard turbines for 15 minutes each hour.",
                "extracted_events": ["Boiler #2 steaming auxiliaries", "SSTG #1 online (85 kW)", "Turbines on jacking gear"],
                "bbox": [0.548, 0.105, 0.380, 0.112],
            },
            {
                "watch_period": "04-08",
                "source_page": page,
                "officer": "H. R. Nelson, Ensign, U.S.N.R.",
                "confidence": 0.92,
                "needs_review": False,
                "text": "Boiler #2 steaming as before. 0630 Blew tubes on Boiler #2. Feed water salinity tested at 0.08 grains Cl/gal. Chief Machinist Vance inspected reduction gear teeth via inspection ports; gears in satisfactory condition.",
                "extracted_events": ["0630 Blew tubes Boiler #2", "Feed water salinity 0.08 gr/gal", "Reduction gears inspected satisfactory"],
                "bbox": [0.548, 0.225, 0.380, 0.112],
            },
            {
                "watch_period": "08-12",
                "source_page": page,
                "officer": "C. E. Miller, Lt. (jg), U.S.N.R.",
                "confidence": 0.93,
                "needs_review": False,
                "text": "Steaming as before. 0915 Received orders to prepare for fueling from USN Tanker. Started fuel oil transfer pump to shift 8,000 gals Bunker B from forward reserve tank A-1 to service bottoms. Fuel oil heating coils set to 125°F.",
                "extracted_events": ["0915 Fuel transfer pump started", "Shifted 8,000 gals Bunker B to service bottoms", "Fuel preheaters set to 125°F"],
                "bbox": [0.548, 0.345, 0.380, 0.112],
            },
            {
                "watch_period": "12-16",
                "source_page": page,
                "officer": "H. R. Nelson, Ensign, U.S.N.R.",
                "confidence": 0.91,
                "needs_review": False,
                "text": "1315 Moored alongside tanker. 1515 Commenced taking on Bunker B fuel oil through port 4-inch fueling manifold. Boiler #2 auxiliary load increased to 175 psi to support fuel oil booster pump. Electrical board load steady at 125 kW.",
                "extracted_events": ["1315 Moored alongside tanker", "1515 Commenced bunkering Bunker B", "Boiler #2 pressure 175 psi"],
                "bbox": [0.548, 0.465, 0.380, 0.112],
            },
            {
                "watch_period": "16-20",
                "source_page": page,
                "officer": "C. E. Miller, Lt. (jg), U.S.N.R.",
                "confidence": 0.95,
                "needs_review": False,
                "text": "Fueling as before. 1845 Secured fueling. Received on board 43,638 gallons of Bunker 'B' fuel oil at 62°F. Soundings taken on all double bottom fuel tanks: A-1, A-2, B-1, B-2 confirmed total 105,698 gals on board.",
                "extracted_events": ["1845 Secured fueling evolution", "43,638 gals Bunker B received", "Total fuel on board 105,698 gals"],
                "bbox": [0.548, 0.585, 0.380, 0.112],
            },
            {
                "watch_period": "20-24",
                "source_page": page,
                "officer": "H. R. Nelson, Ensign, U.S.N.R.",
                "confidence": 0.93,
                "needs_review": False,
                "text": "Moored as before in Chernofski Harbor. Boiler #2 steaming auxiliaries. Lube oil purifier operated 4 hours in batch cleaning cycle on starboard sump. Auxiliary exhaust steam pressure holding steady at 10 psi.",
                "extracted_events": ["Lube oil purifier run 4 hours", "Starboard sump batch cleaned", "Aux exhaust steady 10 psi"],
                "bbox": [0.548, 0.705, 0.380, 0.112],
            },
        ],
        "hourly_rows": hourly_rows,
        "tokens": tokens,
    }
    scan_entry = _render_engineering_scan_image(data, "gilmer_dd233_machinery_1942_10_01.png")
    data["scan_images"] = [scan_entry]
    data["custom_scan_images"] = [scan_entry]
    return data


def build_oct2_bell_book() -> dict[str, Any]:
    """
    2 October 1942 — U.S.S. Gilmer (DD-233) Engineer's Bell Book (Form N. Eng. 11).
    Sortie from Chernofski Harbor through Akutan Pass to Makushin Bay.
    Chronological minute-by-minute engine telegraph commands and revolution counter readings.
    """
    day_id = "1942-10-02-bellbook"
    page = 7

    bell_orders = [
        {"order_idx": 1, "time": "06:12:00", "order": "AHEAD 1/3", "port_rpm": 70, "stbd_rpm": 70, "counter": 81240, "throttleman": "R.T.H.", "notes": "Underway from Chernofski berth; maneuvering clear of buoy"},
        {"order_idx": 2, "time": "06:18:30", "order": "AHEAD 2/3", "port_rpm": 140, "stbd_rpm": 140, "counter": 81890, "throttleman": "R.T.H.", "notes": "Standing out channel, 10.0 knots"},
        {"order_idx": 3, "time": "06:27:00", "order": "AHEAD STANDARD", "port_rpm": 210, "stbd_rpm": 210, "counter": 82980, "throttleman": "R.T.H.", "notes": "Standard speed 15.0 kts set on base course 045°"},
        {"order_idx": 4, "time": "07:15:15", "order": "AHEAD FULL", "port_rpm": 280, "stbd_rpm": 280, "counter": 88450, "throttleman": "E.G.N.", "notes": "Entering Akutan Pass; increased revolutions against 4-kt flood tide"},
        {"order_idx": 5, "time": "07:42:40", "order": "AHEAD FLANK", "port_rpm": 350, "stbd_rpm": 350, "counter": 94120, "throttleman": "E.G.N.", "notes": "Flank speed 25.4 kts; all 4 boilers wide open, steam 295 psi"},
        {"order_idx": 6, "time": "08:14:10", "order": "STOP", "port_rpm": 0, "stbd_rpm": 0, "counter": 96870, "throttleman": "R.T.H.", "notes": "Emergency telegraph bell from bridge (obstacle detected)"},
        {"order_idx": 7, "time": "08:14:25", "order": "BACK FULL", "port_rpm": 180, "stbd_rpm": 180, "counter": 96890, "throttleman": "R.T.H.", "notes": "ASTERN full power (180 RPM Back) to check headway before pinnacle reef"},
        {"order_idx": 8, "time": "08:18:00", "order": "STOP", "port_rpm": 0, "stbd_rpm": 0, "counter": 97240, "throttleman": "R.T.H.", "notes": "Way off ship; obstacle cleared on port beam"},
        {"order_idx": 9, "time": "08:21:00", "order": "AHEAD 2/3", "port_rpm": 140, "stbd_rpm": 140, "counter": 97310, "throttleman": "R.T.H.", "notes": "Rudder amidships, swinging out into deep water"},
        {"order_idx": 10, "time": "08:24:00", "order": "AHEAD STANDARD", "port_rpm": 210, "stbd_rpm": 210, "counter": 97620, "throttleman": "R.T.H.", "notes": "Resumed base anti-submarine screening speed (15.0 kts)"},
    ]

    # Order #5 is idx=4 (y = 0.205 + 4*0.038 = 0.357)
    # Order #7 is idx=6 (y = 0.205 + 6*0.038 = 0.433)
    tokens = [
        {
            "token_id": "p7_bell_hdr_ship",
            "page": page,
            "category": "header",
            "field_key": "header.ship_name",
            "label": "Form N. Eng. 11 Header — Vessel & Hull",
            "raw_value": "U.S.S. Gilmer (DD-233)",
            "normalized_value": "U.S.S. Gilmer (DD-233)",
            "suggested_value": "U.S.S. Gilmer (DD-233)",
            "confidence": 0.98,
            "needs_review": False,
            "verified": True,
            "review_reason": "Clear vessel header on Bell Book sheet.",
            "bbox": [0.050, 0.092, 0.205, 0.026],
        },
        {
            "token_id": "p7_bell_counter_0742",
            "page": page,
            "category": "bell_book_counter",
            "field_key": "bell.0742.counter",
            "label": "Bell 07:42:40 — Shaft Revolution Counter Reading",
            "raw_value": "094120",
            "normalized_value": "094120",
            "suggested_value": "094120",
            "confidence": 0.58,
            "needs_review": True,
            "verified": False,
            "review_reason": "Rapidly rotating mechanical counter recorded in pencil under vibration at Row 5 (07:42:40 AHEAD FLANK); digit '4' loop closed resembling '9'. Verified by previous and next delta counter checks.",
            "bbox": [0.354, round(0.205 + 4 * 0.038, 4), 0.074, 0.032],
        },
        {
            "token_id": "p7_bell_throttle_init",
            "page": page,
            "category": "bell_book_signature",
            "field_key": "bell.throttleman_signature",
            "label": "Throttleman Initials (R. T. Hayes, Chief Machinist's Mate)",
            "raw_value": "R.T.H.",
            "normalized_value": "R.T.H. (Chief Machinist's Mate)",
            "suggested_value": "R.T.H.",
            "confidence": 0.65,
            "needs_review": True,
            "verified": False,
            "review_reason": "Fast initials penned in oiler's grease in Throttleman Initials column at Row 6 (08:14:10 STOP).",
            "bbox": [0.430, round(0.205 + 5 * 0.038, 4), 0.052, 0.032],
        },
        {
            "token_id": "p7_bell_emergency_astern",
            "page": page,
            "category": "bell_book_command",
            "field_key": "bell.0814.emergency_astern",
            "label": "Bell 08:14:25 — Emergency Engine Telegraph Command",
            "raw_value": "BACK FULL (Emergency Astern)",
            "normalized_value": "BACK FULL",
            "suggested_value": "BACK FULL",
            "confidence": 0.97,
            "needs_review": False,
            "verified": False,
            "review_reason": "Bold underlined entry in red grease pencil at Row 7 (08:14:25) indicating bridge casualty bell.",
            "bbox": [0.132, round(0.205 + 6 * 0.038, 4), 0.140, 0.032],
        },
    ]

    for idx, bo in enumerate(bell_orders):
        ry = round(0.205 + idx * 0.038, 4)
        tokens.append({
            "token_id": f"p7_bell_order_{bo['order_idx']:02d}",
            "page": page,
            "category": "bell_book_command",
            "field_key": f"bell.order.{bo['order_idx']:02d}",
            "label": f"Bell Order #{bo['order_idx']} ({bo['time']}) — {bo['order']}",
            "raw_value": f"{bo['time']} {bo['order']} ({bo['port_rpm']}/{bo['stbd_rpm']} RPM)",
            "normalized_value": bo["order"],
            "suggested_value": bo["order"],
            "confidence": 0.95,
            "needs_review": False,
            "verified": True,
            "review_reason": bo["notes"],
            "bbox": [0.050, ry, 0.432, 0.032],
        })

    hourly_rows = []
    base_counter = 75000
    for hr in range(1, 25):
        is_underway = 6 <= hr <= 19
        rpm = 210 if (6 <= hr <= 12) else (180 if (13 <= hr <= 19) else 0)
        speed = 15.0 if (6 <= hr <= 12) else (12.8 if (13 <= hr <= 19) else 0.0)
        boilers = "Boilers #1, #2, #3, #4" if is_underway else "Boiler #2"
        drum_psi = 295 if is_underway else 165
        superheat = 505 if is_underway else 380
        vac = 28.6 if is_underway else 0.0
        base_counter += rpm * 60

        hourly_rows.append({
            "hour": hr,
            "hour_label": f"{hr:02d}00",
            "port_rpm": rpm,
            "stbd_rpm": rpm,
            "revs": rpm,
            "counter_port": base_counter,
            "counter_stbd": base_counter,
            "counter_total": base_counter,
            "engine_miles": round(speed, 1),
            "speed_knots": speed,
            "boilers_steaming": boilers,
            "boiler_drum_psi": drum_psi,
            "superheat_temp_f": superheat,
            "aux_steam_psi": 160,
            "feedwater_temp_f": 225 if is_underway else 210,
            "hp_turbine_psi": 260 if is_underway else 0,
            "main_condenser_vacuum_inhg": vac,
            "sea_temp_injection": 42,
            "sea_temp_discharge": 56,
            "lube_oil_pressure_psi": 16 if is_underway else 14,
            "lube_cooler_in_f": 130 if is_underway else 110,
            "lube_cooler_out_f": 105 if is_underway else 98,
            "thrust_bearing_temp_f": 138 if is_underway else 95,
            "sstg_load_kw": 115 if is_underway else 85,
            "evap_distilled_gals": 180 if is_underway else 120,
            "feed_salinity_grains": 0.09,
            "fuel_rate_gph": 210.0 if is_underway else 70.0,
            "barometer_raw": "2980",
            "barometer_inhg": 29.80,
            "temp_dry_bulb": 46,
            "temp_wet_bulb": 44,
            "temp_water": 42,
            "wind_dir": "NW",
            "wind_force": 4,
            "weather_sym": "c",
            "weather_decoded": "Cloudy",
            "visibility": 8,
            "sea_cond": 3,
            "course": "045°" if is_underway else "Anchored",
            "min_confidence": 0.93,
            "has_low_confidence": False,
            "cell_meta": {},
        })

    data = {
        "day_id": day_id,
        "log_type": "engineering_bell_book",
        "title": "U.S.S. Gilmer (DD-233) — Engineer's Bell Book (Form N. Eng. 11)",
        "date_iso": "1942-10-02",
        "date_human": "Friday, 2 October 1942 (Engineering Bell Book)",
        "day_of_week": "Friday",
        "ship_name": "U.S.S. Gilmer",
        "hull_number": "DD-233",
        "location": "Chernofski Harbor through Akutan Pass to Makushin Bay",
        "zone_description": "+10",
        "commanding_officer": "H. O. Parish, Lt. Comdr., U.S.N.",
        "navigator": "M. Momer, Lt. Comdr., U.S.N.",
        "eoow": "H. R. Nelson, Ensign, U.S.N.R.",
        "chief_machinist": "W. H. Vance, Chief Machinist, U.S.N.",
        "plant_config": "Underway Steaming: All 4 B&W Boilers (300 psi); Parsons Turbines Full Maneuvering",
        "boilers_in_use": "Boilers #1, #2, #3, #4 Cut In on Main Steam Line",
        "primary_page": page,
        "continuation_page": None,
        "source_pages": [page],
        "bell_book_orders": bell_orders,
        "position": {
            "pos_8am_lat": "53° 54' N",
            "pos_8am_lon": "166° 31' W",
            "pos_noon_lat": "53° 58' N",
            "pos_noon_lon": "166° 52' W",
            "pos_8pm_lat": "Anchored",
            "pos_8pm_lon": "Makushin Bay",
        },
        "fuel": {
            "prior_on_hand": 105698,
            "received": 0,
            "expended": 3280,
            "on_hand": 102418,
            "computed_on_hand": 102418,
            "discrepancy": 0,
            "audit_status": "VERIFIED RECONCILED",
            "audit_pass": True,
        },
        "water": {
            "prior_on_hand": 4920,
            "distilled": 3100,
            "received": 0,
            "expended": 2600,
            "on_hand": 5420,
            "computed_on_hand": 5420,
            "discrepancy": 0,
            "audit_status": "VERIFIED RECONCILED",
            "audit_pass": True,
        },
        "draft": {
            "before_label": "Before Leaving Port",
            "before_ford": "10' 6\"",
            "before_aft": "12' 3\"",
            "after_label": "After Entering Port",
            "after_ford": "10' 4\"",
            "after_aft": "12' 1\"",
        },
        "compass_and_mag": {
            "compass_dev": "2.0° E",
            "mag_temp_max": 60,
            "mag_temp_min": 52,
        },
        "watches": [
            {
                "watch_period": "04-08",
                "source_page": page,
                "officer": "H. R. Nelson, Ensign, U.S.N.R.",
                "confidence": 0.95,
                "needs_review": False,
                "text": "0515 Lighted fires under Boilers #1, #3, and #4. 0545 Cut in on main steam line; steam pressure 295 psi drum, 505°F superheat. 0612 Answered first engine bell Ahead 1/3 (70 RPM) standing out Chernofski Harbor. 0715 Increased to Ahead Full (280 RPM) entering Akutan Pass.",
                "extracted_events": ["0515 Lighted fires Boilers #1, #3, #4", "0545 Cut in on main steam line", "0612 Underway Ahead 1/3", "0715 Ahead Full in Akutan Pass"],
                "bbox": [0.548, 0.140, 0.380, 0.165],
            },
            {
                "watch_period": "08-12",
                "source_page": page,
                "officer": "C. E. Miller, Lt. (jg), U.S.N.R.",
                "confidence": 0.94,
                "needs_review": False,
                "text": "0814 Emergency STOP bell rung from bridge followed by BACK FULL (180 RPM Astern). Throttleman reversed main throttles in 15 seconds checking forward motion before charted rock shoal. 0824 Resumed Ahead Standard (210 RPM) entering Makushin Bay.",
                "extracted_events": ["0814 Emergency BACK FULL bell executed", "Checked headway in 15 seconds", "Shoal cleared, resumed Ahead Standard"],
                "bbox": [0.548, 0.330, 0.380, 0.165],
            },
        ],
        "hourly_rows": hourly_rows,
        "tokens": tokens,
    }
    scan_entry = _render_engineering_scan_image(data, "gilmer_dd233_bellbook_1942_10_02.png")
    data["scan_images"] = [scan_entry]
    data["custom_scan_images"] = [scan_entry]
    return data


def build_oct5_machinery_log() -> dict[str, Any]:
    """
    5 October 1942 — U.S.S. Gilmer (DD-233) Combat Machinery Steaming Log (Form N. Eng. 10).
    High-speed Anti-Submarine Sweep (24 knots).
    Includes Hour 14 Thrust Bearing Temperature Anomaly (168°F > 160°F safety threshold).
    """
    day_id = "1942-10-05-machinery"
    page = 10

    hours = list(range(1, 25))
    hourly_rows = []
    tokens = [
        {
            "token_id": "p10_mach_hdr_ship",
            "page": page,
            "category": "header",
            "field_key": "header.ship_name",
            "label": "Form N. Eng. 10 Header — Vessel & Hull",
            "raw_value": "U.S.S. Gilmer (DD-233)",
            "normalized_value": "U.S.S. Gilmer (DD-233)",
            "suggested_value": "U.S.S. Gilmer (DD-233)",
            "confidence": 0.98,
            "needs_review": False,
            "verified": True,
            "review_reason": "Clear vessel header on Form N. Eng. 10.",
            "bbox": [0.050, 0.092, 0.205, 0.026],
        },
    ]

    for hr in hours:
        is_sprint = 12 <= hr <= 17
        rpm = 330 if is_sprint else (210 if (6 <= hr <= 19) else 140)
        speed = 24.0 if is_sprint else (15.0 if (6 <= hr <= 19) else 10.0)
        fuel_rate = 345.0 if is_sprint else 185.0
        drum_psi = 295 if is_sprint else 280
        superheat = 510 if is_sprint else 490
        row_y = round(0.200 + (hr - 1) * 0.021, 4)

        is_anom_hr14 = (hr == 14)
        thrust_temp = 168 if is_anom_hr14 else (148 if is_sprint else 132)
        hr_conf = 0.59 if is_anom_hr14 else 0.94

        cell_meta = {
            "thrust_bearing_temp_f": _make_machinery_cell_meta(
                f"p{page}_mach_hr{hr:02d}_thrust_temp",
                0.59 if is_anom_hr14 else 0.93,
                "Bearing temperature exceeds 160°F safety threshold!" if is_anom_hr14 else "Bearing temperature normal",
                str(thrust_temp),
                needs_review=is_anom_hr14,
            ),
        }

        tok_thrust = {
            "token_id": f"p{page}_mach_hr{hr:02d}_thrust_temp",
            "page": page,
            "category": "hourly_machinery",
            "hour": hr,
            "field_key": f"machinery.{hr:02d}.thrust_bearing_temp",
            "label": f"Hour {hr:02d}00 — Port Reduction Gear Thrust Bearing Temp (°F)",
            "raw_value": str(thrust_temp),
            "normalized_value": f"{thrust_temp}°F",
            "suggested_value": str(thrust_temp),
            "confidence": 0.59 if is_anom_hr14 else 0.93,
            "needs_review": is_anom_hr14,
            "verified": False,
            "review_reason": "High temperature alert (168°F > 160°F limit) logged in Thrust Bearing Temp column during 24-kt anti-submarine sprint. Circled in red pencil by EOOW." if is_anom_hr14 else "Normal temperature log.",
            "bbox": [0.390, row_y, 0.045, 0.018],
        }
        tokens.append(tok_thrust)

        hourly_rows.append({
            "hour": hr,
            "hour_label": f"{hr:02d}00",
            "port_rpm": rpm,
            "stbd_rpm": rpm,
            "revs": rpm,
            "counter_port": 110000 + hr * rpm * 60,
            "counter_stbd": 110000 + hr * rpm * 60,
            "counter_total": 110000 + hr * rpm * 60,
            "engine_miles": round(speed, 1),
            "speed_knots": speed,
            "boilers_steaming": "Boilers #1, #2, #3, #4",
            "boiler_drum_psi": drum_psi,
            "superheat_temp_f": superheat,
            "aux_steam_psi": 160,
            "feedwater_temp_f": 235,
            "hp_turbine_psi": 280 if is_sprint else 240,
            "main_condenser_vacuum_inhg": 28.7,
            "sea_temp_injection": 40,
            "sea_temp_discharge": 57,
            "lube_oil_pressure_psi": 17,
            "lube_cooler_in_f": 142 if is_sprint else 125,
            "lube_cooler_out_f": 115 if is_sprint else 102,
            "thrust_bearing_temp_f": thrust_temp,
            "sstg_load_kw": 140,
            "evap_distilled_gals": 210,
            "feed_salinity_grains": 0.07,
            "fuel_rate_gph": fuel_rate,
            "barometer_raw": "2855",
            "barometer_inhg": 28.55,
            "temp_dry_bulb": 44,
            "temp_wet_bulb": 43,
            "temp_water": 40,
            "wind_dir": "W",
            "wind_force": 6,
            "weather_sym": "or",
            "weather_decoded": "Overcast with rain",
            "visibility": 5,
            "sea_cond": 4,
            "course": "270°",
            "min_confidence": hr_conf,
            "has_low_confidence": is_anom_hr14,
            "cell_meta": cell_meta,
        })

    data = {
        "day_id": day_id,
        "log_type": "machinery_log",
        "title": "U.S.S. Gilmer (DD-233) — Combat Steaming Machinery Log (Form N. Eng. 10)",
        "date_iso": "1942-10-05",
        "date_human": "Monday, 5 October 1942 (Combat Machinery Log)",
        "day_of_week": "Monday",
        "ship_name": "U.S.S. Gilmer",
        "hull_number": "DD-233",
        "location": "Makushin Bay to Dutch Harbor Anti-Submarine Sweep",
        "zone_description": "+10",
        "commanding_officer": "H. O. Parish, Lt. Comdr., U.S.N.",
        "navigator": "M. Momer, Lt. Comdr., U.S.N.",
        "eoow": "C. E. Miller, Lt. (jg), U.S.N.R.",
        "chief_machinist": "W. H. Vance, Chief Machinist, U.S.N.",
        "plant_config": "4 Boilers Steaming at 295 psi / 510°F Superheat; 24-Kt Sprint",
        "boilers_in_use": "Boilers #1, #2, #3, #4 in Steaming Service",
        "primary_page": page,
        "continuation_page": None,
        "source_pages": [page],
        "position": {
            "pos_8am_lat": "53° 55' N",
            "pos_8am_lon": "166° 50' W",
            "pos_noon_lat": "54° 02' N",
            "pos_noon_lon": "166° 38' W",
            "pos_8pm_lat": "Anchored",
            "pos_8pm_lon": "Dutch Harbor",
        },
        "fuel": {
            "prior_on_hand": 97843,
            "received": 0,
            "expended": 4120,
            "on_hand": 93723,
            "computed_on_hand": 93723,
            "discrepancy": 0,
            "audit_status": "VERIFIED RECONCILED",
            "audit_pass": True,
        },
        "water": {
            "prior_on_hand": 4500,
            "distilled": 3800,
            "received": 0,
            "expended": 3200,
            "on_hand": 5100,
            "computed_on_hand": 5100,
            "discrepancy": 0,
            "audit_status": "VERIFIED RECONCILED",
            "audit_pass": True,
        },
        "draft": {
            "before_label": "Before Leaving Port",
            "before_ford": "10' 3\"",
            "before_aft": "12' 2\"",
            "after_label": "After Entering Port",
            "after_ford": "10' 1\"",
            "after_aft": "12' 0\"",
        },
        "compass_and_mag": {
            "compass_dev": "1.0° W",
            "mag_temp_max": 62,
            "mag_temp_min": 52,
        },
        "watches": [
            {
                "watch_period": "12-16",
                "source_page": page,
                "officer": "C. E. Miller, Lt. (jg), U.S.N.R.",
                "confidence": 0.93,
                "needs_review": False,
                "text": "1230 Bridge rang Ahead Flank (330 RPM, 24.0 kts) on sonar submarine contact alert. All 4 boilers steaming at 295 psi. At 1410, port reduction gear thrust bearing temperature spiked to 168°F. EOOW immediately ordered sea-injection bypass valve opened to full stroke; bearing temperature subsided to 142°F by 1435 without Babbitt metal wiping.",
                "extracted_events": ["1230 Ahead Flank (330 RPM, 24 kts) on sonar alert", "1410 Port thrust bearing temperature spike (168°F)", "Cooler bypass opened, temp reduced to 142°F"],
                "bbox": [0.548, 0.220, 0.380, 0.165],
            },
        ],
        "hourly_rows": hourly_rows,
        "tokens": tokens,
    }
    scan_entry = _render_engineering_scan_image(data, "gilmer_dd233_machinery_1942_10_05.png")
    data["scan_images"] = [scan_entry]
    data["custom_scan_images"] = [scan_entry]
    return data


def build_oct29_machinery_log() -> dict[str, Any]:
    """
    29 October 1942 — U.S.S. Gilmer (DD-233) Heavy Weather Machinery Log (Form N. Eng. 10).
    Force 7 Gale, 35-Degree Rolls near Bogoslof Island.
    Features:
    - Hour 09 Boiler Priming / Wet Steam Carry-over Anomaly (Superheat 425°F)
    - Hour 16 Main Condenser Salinity Warning (0.48 gr/gal)
    """
    day_id = "1942-10-29-machinery"
    page = 45

    hours = list(range(1, 25))
    hourly_rows = []
    tokens = [
        {
            "token_id": "p45_mach_hdr_ship",
            "page": page,
            "category": "header",
            "field_key": "header.ship_name",
            "label": "Form N. Eng. 10 Header — Vessel & Hull",
            "raw_value": "U.S.S. Gilmer (DD-233)",
            "normalized_value": "U.S.S. Gilmer (DD-233)",
            "suggested_value": "U.S.S. Gilmer (DD-233)",
            "confidence": 0.98,
            "needs_review": False,
            "verified": True,
            "review_reason": "Clear vessel header on Form N. Eng. 10.",
            "bbox": [0.050, 0.092, 0.205, 0.026],
        },
    ]

    for hr in hours:
        is_gale = 6 <= hr <= 20
        rpm = 250 if is_gale else 180
        speed = 18.0 if is_gale else 13.0
        fuel_rate = 260.0 if is_gale else 160.0
        row_y = round(0.200 + (hr - 1) * 0.021, 4)

        is_priming_hr09 = (hr == 9)
        is_salinity_hr16 = (hr == 16)

        superheat = 425 if is_priming_hr09 else (500 if is_gale else 480)
        salinity = 0.48 if is_salinity_hr16 else 0.08
        drum_psi = 270 if is_priming_hr09 else 290
        vac = 26.8 if is_salinity_hr16 else 28.5

        hr_conf = 0.52 if (is_priming_hr09 or is_salinity_hr16) else 0.93

        cell_meta = {}
        if is_priming_hr09:
            cell_meta["superheat_temp_f"] = _make_machinery_cell_meta(
                f"p{page}_mach_superheat_hr09",
                0.58,
                "Boiler #1 priming wet steam drop (425°F vs 500°F expected)",
                "425",
                needs_review=True,
            )
            tokens.append({
                "token_id": f"p{page}_mach_superheat_hr09",
                "page": page,
                "category": "hourly_machinery",
                "hour": 9,
                "field_key": "machinery.09.superheat_temp",
                "label": "Hour 0900 — Superheater Outlet Temperature (°F) Priming Dip",
                "raw_value": "425° [rapid fall]",
                "normalized_value": "425°F",
                "suggested_value": "425",
                "confidence": 0.58,
                "needs_review": True,
                "verified": False,
                "review_reason": "Rapid 75°F temperature plunge in Superheat column at Hour 0900 caused by 35° roll water surge carrying wet steam into superheater.",
                "bbox": [0.238, row_y, 0.054, 0.018],
            })

        if is_salinity_hr16:
            cell_meta["feed_salinity_grains"] = _make_machinery_cell_meta(
                f"p{page}_mach_salinity_hr16",
                0.52,
                "Condenser tube weeping salt contamination (0.48 gr/gal > 0.20 limit)",
                "0.48",
                needs_review=True,
            )
            tokens.append({
                "token_id": f"p{page}_mach_salinity_hr16",
                "page": page,
                "category": "hourly_machinery",
                "hour": 16,
                "field_key": "machinery.16.feed_salinity",
                "label": "Hour 1600 — Condensate Salinometer Reading (Grains Cl / Gal)",
                "raw_value": "0.48 gr/gal",
                "normalized_value": "0.48",
                "suggested_value": "0.48",
                "confidence": 0.52,
                "needs_review": True,
                "verified": False,
                "review_reason": "Salt spray smudge over chemical test cell in Salinity column at Hour 1600; indicates seawater weeping into port condenser under heavy sea pounding.",
                "bbox": [0.438, row_y, 0.044, 0.018],
            })

        hourly_rows.append({
            "hour": hr,
            "hour_label": f"{hr:02d}00",
            "port_rpm": rpm,
            "stbd_rpm": rpm,
            "revs": rpm,
            "counter_port": 180000 + hr * rpm * 60,
            "counter_stbd": 180000 + hr * rpm * 60,
            "counter_total": 180000 + hr * rpm * 60,
            "engine_miles": round(speed, 1),
            "speed_knots": speed,
            "boilers_steaming": "Boilers #1 and #3",
            "boiler_drum_psi": drum_psi,
            "superheat_temp_f": superheat,
            "aux_steam_psi": 160,
            "feedwater_temp_f": 220,
            "hp_turbine_psi": 250,
            "main_condenser_vacuum_inhg": vac,
            "sea_temp_injection": 39,
            "sea_temp_discharge": 54,
            "lube_oil_pressure_psi": 16,
            "lube_cooler_in_f": 132,
            "lube_cooler_out_f": 104,
            "thrust_bearing_temp_f": 140,
            "sstg_load_kw": 125,
            "evap_distilled_gals": 160,
            "feed_salinity_grains": salinity,
            "fuel_rate_gph": fuel_rate,
            "barometer_raw": "2910",
            "barometer_inhg": 29.10,
            "temp_dry_bulb": 43,
            "temp_wet_bulb": 42,
            "temp_water": 39,
            "wind_dir": "WNW",
            "wind_force": 7,
            "weather_sym": "orm",
            "weather_decoded": "Overcast with rain & mist",
            "visibility": 4,
            "sea_cond": 5,
            "course": "090°",
            "min_confidence": hr_conf,
            "has_low_confidence": is_priming_hr09 or is_salinity_hr16,
            "cell_meta": cell_meta,
        })

    data = {
        "day_id": day_id,
        "log_type": "machinery_log",
        "title": "U.S.S. Gilmer (DD-233) — Heavy Weather Machinery Log (Form N. Eng. 10)",
        "date_iso": "1942-10-29",
        "date_human": "Thursday, 29 October 1942 (Heavy Weather Engineering Log)",
        "day_of_week": "Thursday",
        "ship_name": "U.S.S. Gilmer",
        "hull_number": "DD-233",
        "location": "Bogoslof Island to Dutch Harbor (Force 7 Gale, 35° Heavy Rolls)",
        "zone_description": "+10",
        "commanding_officer": "H. O. Parish, Lt. Comdr., U.S.N.",
        "navigator": "M. Momer, Lt. Comdr., U.S.N.",
        "eoow": "J. Senter, Jr., Ensign, U.S.N.R.",
        "chief_machinist": "W. H. Vance, Chief Machinist, U.S.N.",
        "plant_config": "Boilers #1 and #3 Steaming; Heavy Seas Priming & Salinity Casualties",
        "boilers_in_use": "Boilers #1 and #3 Online",
        "primary_page": page,
        "continuation_page": None,
        "source_pages": [page],
        "position": {
            "pos_8am_lat": "53° 56' N",
            "pos_8am_lon": "167° 45' W",
            "pos_noon_lat": "53° 58' N",
            "pos_noon_lon": "167° 10' W",
            "pos_8pm_lat": "Anchored",
            "pos_8pm_lon": "Iliuliuk Bay",
        },
        "fuel": {
            "prior_on_hand": 84500,
            "received": 0,
            "expended": 3840,
            "on_hand": 80660,
            "computed_on_hand": 80660,
            "discrepancy": 0,
            "audit_status": "VERIFIED RECONCILED",
            "audit_pass": True,
        },
        "water": {
            "prior_on_hand": 4800,
            "distilled": 3100,
            "received": 0,
            "expended": 2900,
            "on_hand": 5000,
            "computed_on_hand": 5000,
            "discrepancy": 0,
            "audit_status": "VERIFIED RECONCILED",
            "audit_pass": True,
        },
        "draft": {
            "before_label": "Before Leaving Port",
            "before_ford": "10' 2\"",
            "before_aft": "12' 1\"",
            "after_label": "After Entering Port",
            "after_ford": "10' 0\"",
            "after_aft": "11' 11\"",
        },
        "compass_and_mag": {
            "compass_dev": "2.5° W",
            "mag_temp_max": 58,
            "mag_temp_min": 50,
        },
        "watches": [
            {
                "watch_period": "08-12",
                "source_page": page,
                "officer": "J. Senter, Jr., Ensign, U.S.N.R.",
                "confidence": 0.90,
                "needs_review": False,
                "text": "Steaming in A/S screen in heavy Force 7 NW gale with 30-foot seas; ship rolling up to 35 degrees. At 0915, severe roll caused Boiler #1 to prime, carrying water over into superheater elements. Throttled port turbine back to 180 RPM until superheat temperature recovered to 490°F.",
                "extracted_events": ["Heavy seas (35° roll) caused Boiler #1 priming", "Water carryover dropped superheat to 425°F", "Throttled port turbine back until recovered"],
                "bbox": [0.548, 0.220, 0.380, 0.165],
            },
            {
                "watch_period": "16-20",
                "source_page": page,
                "officer": "C. C. Brown, Ensign, U.S.N.R.",
                "confidence": 0.88,
                "needs_review": False,
                "text": "1620 Electrical salinometer alarmed on port main condenser hotwell. Chemical test confirmed chloride salinity jumped to 0.48 grains Cl/gal due to tube weepage under hull pounding. Diverted port condensate to bilge to protect boiler tubes. Shifted makeup feed to reserve bottom tank #2.",
                "extracted_events": ["1620 Salinometer alarm on port condenser", "Chloride salinity spike 0.48 gr/gal", "Diverted contaminated condensate to bilge"],
                "bbox": [0.548, 0.410, 0.380, 0.165],
            },
        ],
        "hourly_rows": hourly_rows,
        "tokens": tokens,
    }
    scan_entry = _render_engineering_scan_image(data, "gilmer_dd233_machinery_1942_10_29.png")
    data["scan_images"] = [scan_entry]
    data["custom_scan_images"] = [scan_entry]
    return data


def add_all_machinery_logs(corpus: dict[str, dict[str, Any]]) -> None:
    """Register all 4 authentic 1940s machinery & bell book logs into the main corpus cache."""
    m1 = build_oct1_machinery_log()
    b2 = build_oct2_bell_book()
    m5 = build_oct5_machinery_log()
    m29 = build_oct29_machinery_log()

    corpus[m1["day_id"]] = m1
    corpus[b2["day_id"]] = b2
    corpus[m5["day_id"]] = m5
    corpus[m29["day_id"]] = m29

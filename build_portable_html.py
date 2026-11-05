"""
Generates a 100% self-contained, zero-server shareable HTML file
(`output/USS_Gilmer_DD233_Portable_Workbench.html`) with all digitized days,
template match scores, <70% confidence tokens, semantic mappings, trend charts,
and base64-encoded compressed scan thumbnails embedded directly inside one HTML file
so it can be emailed or shared on a USB drive without needing Python.
"""

from __future__ import annotations

import base64
import io
import json
from pathlib import Path
from PIL import Image

from app import _build_full_day_bundle, api_get_corpus_trends, api_overview, clear_runtime_store, on_startup, seed_demo_corpus

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Hackathon Store" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INDEX_HTML = BASE_DIR / "static" / "index.html"


def _encode_scan_jpeg_data_uri(img_path: Path, max_width: int = 1250, quality: int = 68) -> str:
    if not img_path.exists():
        return ""
    with Image.open(img_path) as im:
        rgb = im.convert("RGB")
        w, h = rgb.size
        if w > max_width:
            new_h = int(h * (max_width / float(w)))
            rgb = rgb.resize((max_width, new_h), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        rgb.save(buf, format="JPEG", quality=quality, optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        return f"data:image/jpeg;base64,{b64}"


def build_portable_bundle() -> Path:
    on_startup()
    seed_demo_corpus()
    overview = api_overview()
    trends = api_get_corpus_trends()

    day_bundles = {}
    for d in overview["days"]:
        d_id = d["day_id"]
        bundle = _build_full_day_bundle(d_id, regenerate_files=False)
        for s in bundle["extraction"]["scan_images"]:
            local_p = Path(s["local_path"])
            data_uri = _encode_scan_jpeg_data_uri(local_p)
            s["url"] = data_uri
            s["web_url"] = data_uri
        if "days_lookup" in trends and d_id in trends["days_lookup"]:
            trends["days_lookup"][d_id]["scan_images"] = bundle["extraction"]["scan_images"]
        # Point download buttons to relative filenames in the same `output/` folder
        bundle["populated_files"]["xlsx_url"] = bundle["populated_files"]["xlsx_filename"]
        bundle["populated_files"]["docx_url"] = bundle["populated_files"]["docx_filename"]
        day_bundles[d_id] = bundle

    for out_f in overview["populated_outputs"]:
        out_f["url"] = out_f["filename"]

    embedded_payload = {
        "overview": overview,
        "trends": trends,
        "days": day_bundles,
    }

    html_src = INDEX_HTML.read_text(encoding="utf-8")
    shim_script = f"""
  <script>
    window.__PORTABLE_DATA__ = {json.dumps(embedded_payload)};
    const _origFetch = window.fetch.bind(window);
    window.fetch = async function(url, opts) {{
      const u = String(url);
      if (window.__PORTABLE_DATA__) {{
        if (u === '/api/overview') {{
          return new Response(JSON.stringify(window.__PORTABLE_DATA__.overview), {{status: 200}});
        }}
        if (u.startsWith('/api/corpus/trends')) {{
          return new Response(JSON.stringify(window.__PORTABLE_DATA__.trends), {{status: 200}});
        }}
        if (u.startsWith('/api/day/') && (!opts || !opts.method || opts.method === 'GET')) {{
          const dayId = decodeURIComponent(u.replace('/api/day/', ''));
          const b = window.__PORTABLE_DATA__.days[dayId];
          return new Response(JSON.stringify(b), {{status: 200}});
        }}
        if (u.endsWith('/update') && opts && opts.method === 'POST') {{
          const dayId = decodeURIComponent(u.split('/api/day/')[1].split('/update')[0]);
          const body = JSON.parse(opts.body || '{{}}');
          const b = window.__PORTABLE_DATA__.days[dayId];
          if (b && body.updates) {{
            if (body.updates.hourly_rows) b.extraction.hourly_rows = body.updates.hourly_rows;
            if (body.updates.fuel) b.extraction.fuel = body.updates.fuel;
            if (body.updates.water) b.extraction.water = body.updates.water;
          }}
          return new Response(JSON.stringify(b), {{status: 200}});
        }}
        if ((u === '/api/extract' || u === '/api/upload-scan') && opts && opts.method === 'POST') {{
          const reqDate = (opts.body && typeof opts.body.get === 'function' && opts.body.get('date_iso')) || '1942-10-18';
          const targetBundle = window.__PORTABLE_DATA__.days[reqDate] || window.__PORTABLE_DATA__.days['1942-10-18'] || window.__PORTABLE_DATA__.days['1942-10-01'] || window.__PORTABLE_DATA__.days[Object.keys(window.__PORTABLE_DATA__.days)[0]];
          const baseBundle = JSON.parse(JSON.stringify(targetBundle));
          return new Response(JSON.stringify(baseBundle), {{status: 200}});
        }}
        if (u === '/api/intelligent-ocr-extract' && opts && opts.method === 'POST') {{
          let sampleId = 'maintenance';
          let tmplOverride = '';
          if (opts.body && typeof opts.body.get === 'function') {{
            sampleId = opts.body.get('sample_id') || 'maintenance';
            tmplOverride = opts.body.get('template_override') || '';
          }}
          const isDeckLog = (sampleId && sampleId !== 'maintenance' && sampleId !== 'maintenance_checkout') || (tmplOverride && tmplOverride.includes('Deck Log'));
          const dayId = sampleId === 'shore' ? '1942-10-14-shore' : (sampleId === 'air' ? '1942-10-19-air' : '1942-10-01');
          const selTmpl = tmplOverride || (isDeckLog ? 'SAMPLE Deck Log Hourly Record.xlsx' : 'SAMPLE Maintenance Procedure Checkout.xlsx');
          const respPayload = {{
            status: 'success',
            document_name: isDeckLog ? 'gilmer-dd-233-1942-10.pdf' : 'SAMPLE_maintenance_checkout_scan.pdf',
            selected_template: selTmpl,
            template_confidence: 100,
            template_confidence_pct: '100%',
            template_reason: 'Autonomous DECK layout survey & schema classification verified.',
            total_tokens: isDeckLog ? 27 : 38,
            mean_confidence_pct: isDeckLog ? '89.4%' : '90.6%',
            low_confidence_count: isDeckLog ? 3 : 2,
            files: {{
              xlsx_filename: isDeckLog ? 'Populated_1942-10-01_Deck_Log_Hourly.xlsx' : 'Populated_Maintenance_Checkout_MP-42-01A.xlsx',
              xlsx_url: isDeckLog ? 'Populated_1942-10-01_Deck_Log_Hourly.xlsx' : 'Populated_Maintenance_Checkout_MP-42-01A.xlsx',
              docx_filename: isDeckLog ? 'Populated_1942-10-01_Deck_Log_Remarks.docx' : 'Populated_Equipment_Inspection_MP-42-01A.docx',
              docx_url: isDeckLog ? 'Populated_1942-10-01_Deck_Log_Remarks.docx' : 'Populated_Equipment_Inspection_MP-42-01A.docx'
            }},
            day_id: isDeckLog ? dayId : null
          }};
          return new Response(JSON.stringify(respPayload), {{status: 200}});
        }}
        if (u === '/api/upload-manual' && opts && opts.method === 'POST') {{
          const manuals = window.__PORTABLE_DATA__.overview.manuals || [];
          const newMan = {{
            manual_id: 'TM-CUSTOM-' + (manuals.length + 1),
            code: (opts.body && opts.body.get && opts.body.get('code')) || ('TM-' + (manuals.length + 101)),
            title: (opts.body && opts.body.get && opts.body.get('title')) || 'Custom Reference Manual',
            unit_type: (opts.body && opts.body.get && opts.body.get('unit_type')) || 'All Units',
            subsystem: (opts.body && opts.body.get && opts.body.get('subsystem')) || 'General Systems',
            standard_limit: (opts.body && opts.body.get && opts.body.get('standard_limit')) || 'Rated Operating Envelope',
            status: 'INDEXED & ACTIVE'
          }};
          manuals.push(newMan);
          return new Response(JSON.stringify({{status: 'ok', manual: newMan, manuals: manuals}}), {{status: 200}});
        }}
        if (u.endsWith('/verify-token') && opts && opts.method === 'POST') {{
          const dayId = decodeURIComponent(u.split('/api/day/')[1].split('/verify-token')[0]);
          const body = JSON.parse(opts.body);
          const b = window.__PORTABLE_DATA__.days[dayId];
          const tok = b.extraction.tokens.find(t => t.token_id === body.token_id);
          if (tok) {{
            tok.raw_value = body.new_value;
            tok.normalized_value = body.new_value;
            tok.verified = true;
            tok.needs_review = false;
          }}
          const unv = b.extraction.tokens.filter(t => t.confidence < 0.70 && !t.verified).length;
          b.extraction.stats.low_confidence_unverified = unv;
          return new Response(JSON.stringify(b), {{status: 200}});
        }}
        if (u.endsWith('/verify-all') && opts && opts.method === 'POST') {{
          const dayId = decodeURIComponent(u.split('/api/day/')[1].split('/verify-all')[0]);
          const b = window.__PORTABLE_DATA__.days[dayId];
          b.extraction.tokens.forEach(tok => {{
            if (tok.confidence < 0.70 && !tok.verified) {{
              tok.raw_value = tok.suggested_value || tok.raw_value;
              tok.verified = true;
              tok.needs_review = false;
            }}
          }});
          b.extraction.stats.low_confidence_unverified = 0;
          return new Response(JSON.stringify(b), {{status: 200}});
        }}
      }}
      return _origFetch(url, opts);
    }};
  </script>
"""
    portable_html = html_src.replace("<script>", shim_script + "\n  <script>", 1)
    out_file = OUTPUT_DIR / "USS_Gilmer_DD233_Portable_Workbench.html"
    out_file.write_text(portable_html, encoding="utf-8")
    legacy_out_dir = BASE_DIR / "output"
    legacy_out_dir.mkdir(parents=True, exist_ok=True)
    (legacy_out_dir / "USS_Gilmer_DD233_Portable_Workbench.html").write_text(portable_html, encoding="utf-8")
    clear_runtime_store()
    return out_file


if __name__ == "__main__":
    p = build_portable_bundle()
    print(f"Built portable zero-server HTML bundle: {p} ({p.stat().st_size / 1024:.1f} KB)")

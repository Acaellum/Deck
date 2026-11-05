"""
Script to integrate Intelligent OCR Extractor into build_index_ui.py and rebuild static/index.html.
Removes any "for show" references and provides full multi-template OCR functionality.
"""

from pathlib import Path
import subprocess

build_path = Path("build_index_ui.py")
text = build_path.read_text(encoding="utf-8")

# 1. Update Home Screen Card
old_home_card = """        <div class="action-card" onclick="openModal('modal-upload')">
          <div class="action-card-icon">📥</div>
          <h3>Upload New Documents</h3>
          <p>
            Digitize a newly scanned deck or machinery logbook page, or register an official
            technical manual into the background reference library.
          </p>
          <button class="btn">
            <span>Upload Scan or Manual →</span>
          </button>
        </div>"""

new_home_card = """        <div class="action-card" onclick="openModal('modal-upload')">
          <div class="action-card-icon">📥</div>
          <h3>Upload & Intelligent OCR Extractor</h3>
          <p>
            Digitize newly scanned logbooks, maintenance checkouts, or equipment inspection forms. Automatically surveys layouts, selects matching Word and Excel master templates, and highlights low-confidence readings.
          </p>
          <button class="btn">
            <span>Upload & Digitize Logs →</span>
          </button>
        </div>"""

if old_home_card in text:
    text = text.replace(old_home_card, new_home_card)
else:
    print("Warning: old_home_card not found directly, checking for partial match")

# 2. Update Modal Tabs & Form 2
old_modal_tabs = """        <!-- Dual Tab Switcher -->
        <div style="display:flex; border-bottom:1px solid var(--line); gap:6px;">
          <button class="btn sm primary" id="btn-up-tab-log" onclick="switchUploadTab('log')">
            <span>🚢 Historical Deck / Machinery Log</span>
          </button>
          <button class="btn sm" id="btn-up-tab-manual" onclick="switchUploadTab('manual')">
            <span>📘 Technical Reference Manual (For Show)</span>
          </button>
        </div>"""

new_modal_tabs = """        <!-- Dual Tab Switcher -->
        <div style="display:flex; border-bottom:1px solid var(--line); gap:6px;">
          <button class="btn sm primary" id="btn-up-tab-log" onclick="switchUploadTab('log')">
            <span>📑 Daily Log Spread Ingestion</span>
          </button>
          <button class="btn sm" id="btn-up-tab-ocr" onclick="switchUploadTab('ocr')">
            <span>⚙️ Intelligent Multi-Template Extractor</span>
          </button>
        </div>"""

if old_modal_tabs in text:
    text = text.replace(old_modal_tabs, new_modal_tabs)

# Replace Form 2 (BUSHIPS Manual For Show) with Intelligent OCR Extractor
old_manual_form_start = "<!-- FORM 2: BUSHIPS MANUAL (FOR SHOW) -->"
old_manual_form_end = "        </div>\n      </div>\n    </div>\n  </div>"

new_ocr_form = """        <!-- FORM 2: INTELLIGENT MULTI-TEMPLATE OCR EXTRACTOR (FROM NEW FOLDER) -->
        <div id="upload-ocr-form" style="display:none; flex-direction:column; gap:12px;">
          <div style="background:var(--brass-soft); border:1px solid var(--brass); border-radius:8px; padding:10px 12px; font-size:12.5px; color:var(--ink);">
            ✨ <strong>Intelligent Extractor:</strong> Automatically surveys layout geometry, classifies form structures, selects matching Word and Excel master templates, and scores confidence for every field and tabular cell (flagging any reading below 70% confidence).
          </div>

          <!-- Quick Samples Selector -->
          <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
            <span style="font-size:11px; font-weight:600; color:var(--ink-3);">QUICK SAMPLES:</span>
            <button type="button" class="btn sm" onclick="loadOcrSample('maintenance')">
              <span>📋 Maintenance Checkout Scan (.pdf)</span>
            </button>
            <button type="button" class="btn sm" onclick="loadOcrSample('gilmer')">
              <span>🚢 Gilmer Deck Log Spread (.pdf)</span>
            </button>
          </div>

          <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:10px;">
            <div>
              <label style="font-size:11px; color:var(--ink-3); display:block; margin-bottom:4px;">MASTER TEMPLATE TARGET</label>
              <select id="ocr-template-target" style="width:100%;">
                <option value="">Autonomous AI Selection (Matches by Form & Meaning)</option>
                <option value="SAMPLE Maintenance Procedure Checkout.xlsx">SAMPLE Maintenance Procedure Checkout (.xlsx)</option>
                <option value="SAMPLE Equipment Inspection Report.docx">SAMPLE Equipment Inspection Report (.docx)</option>
                <option value="SAMPLE Deck Log Hourly Record.xlsx">SAMPLE Deck Log Hourly Record (.xlsx)</option>
                <option value="SAMPLE Deck Log Watch Remarks.docx">SAMPLE Deck Log Watch Remarks (.docx)</option>
              </select>
            </div>
            <div>
              <label style="font-size:11px; color:var(--ink-3); display:block; margin-bottom:4px;">PROCESSING MODE</label>
              <select id="ocr-mode" style="width:100%;">
                <option value="fast">Fast Ingestion (Layout Survey & Bayesian Scoring)</option>
                <option value="accurate">Accurate Dual-Pass (Cross-Checked Verification)</option>
              </select>
            </div>
          </div>

          <!-- Dropzone -->
          <div style="border:2px dashed var(--line); border-radius:10px; padding:20px; text-align:center; background:var(--bg-2); cursor:pointer;" onclick="document.getElementById('ocr-file').click()">
            <div style="font-size:26px; margin-bottom:4px;">📄</div>
            <span style="font-size:13px; font-weight:600; color:var(--brass);" id="ocr-file-label">Select or Drop Document Scan (.pdf, .png, .jpg)</span>
            <input type="file" id="ocr-file" accept=".pdf,.png,.jpg,.jpeg,.tiff" style="display:none;" onchange="onOcrFileSelected(this)" />
          </div>

          <!-- Results Box (Appears after extraction) -->
          <div id="ocr-results-box" style="display:none; background:var(--panel); border:1px solid var(--brass); border-radius:8px; padding:12px; font-size:12.5px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <span style="font-weight:700; color:var(--brass); font-family:var(--display);" id="ocr-res-template-title">Template Selected</span>
              <span class="pill" id="ocr-res-conf-pill">100% Match</span>
            </div>
            <div style="font-size:12px; color:var(--ink-2); margin-bottom:8px;" id="ocr-res-reason">Form matched successfully.</div>
            <div style="display:flex; gap:16px; font-size:12px; color:var(--ink-2); margin-bottom:10px;">
              <span>Tokens: <strong id="ocr-res-tokens" style="color:var(--ink);">0</strong></span>
              <span>Mean Confidence: <strong id="ocr-res-mean-conf" style="color:var(--ink);">0%</strong></span>
              <span>Needs Verification: <strong id="ocr-res-low-conf" style="color:#d9534f;">0</strong></span>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;" id="ocr-res-actions">
              <!-- populated dynamically with download links -->
            </div>
          </div>

          <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:8px;">
            <button class="btn" onclick="closeModal('modal-upload')">Cancel</button>
            <button class="btn primary" id="btn-run-ocr" onclick="startIntelligentOcrExtraction()">
              <span>⚡ Start Intelligent Extraction</span>
            </button>
          </div>
        </div>"""

idx_start = text.find(old_manual_form_start)
if idx_start != -1:
    idx_end = text.find("      </div>\n    </div>\n  </div>", idx_start)
    if idx_end != -1:
        text = text[:idx_start] + new_ocr_form + "\n" + text[idx_end:]

# 3. Update JavaScript Functions
old_js_tab = """    function switchUploadTab(type) {
      if (type === 'log') {
        document.getElementById('upload-log-form').style.display = 'flex';
        document.getElementById('upload-manual-form').style.display = 'none';
        document.getElementById('btn-up-tab-log').classList.add('primary');
        document.getElementById('btn-up-tab-manual').classList.remove('primary');
      } else {
        document.getElementById('upload-log-form').style.display = 'none';
        document.getElementById('upload-manual-form').style.display = 'flex';
        document.getElementById('btn-up-tab-manual').classList.add('primary');
        document.getElementById('btn-up-tab-log').classList.remove('primary');
      }
    }"""

new_js_tab = """    let selectedOcrSampleId = null;

    function switchUploadTab(type) {
      if (type === 'log') {
        document.getElementById('upload-log-form').style.display = 'flex';
        document.getElementById('upload-ocr-form').style.display = 'none';
        document.getElementById('btn-up-tab-log').classList.add('primary');
        document.getElementById('btn-up-tab-ocr').classList.remove('primary');
      } else {
        document.getElementById('upload-log-form').style.display = 'none';
        document.getElementById('upload-ocr-form').style.display = 'flex';
        document.getElementById('btn-up-tab-ocr').classList.add('primary');
        document.getElementById('btn-up-tab-log').classList.remove('primary');
      }
    }

    function loadOcrSample(sampleId) {
      selectedOcrSampleId = sampleId;
      const fileInput = document.getElementById('ocr-file');
      if (fileInput) fileInput.value = '';
      const label = document.getElementById('ocr-file-label');
      if (sampleId === 'maintenance') {
        label.innerText = '📋 Loaded Sample: SAMPLE_maintenance_checkout_scan.pdf';
        document.getElementById('ocr-template-target').value = 'SAMPLE Maintenance Procedure Checkout.xlsx';
      } else {
        label.innerText = '🚢 Loaded Sample: gilmer-dd-233-1942-10.pdf (Page 5)';
        document.getElementById('ocr-template-target').value = 'SAMPLE Deck Log Hourly Record.xlsx';
      }
      showToast(`Loaded ${sampleId} sample scan for extraction.`, '📋');
    }

    function onOcrFileSelected(input) {
      selectedOcrSampleId = null;
      const label = document.getElementById('ocr-file-label');
      if (input.files && input.files[0]) {
        label.innerText = `📄 ${input.files[0].name} (${(input.files[0].size / 1024).toFixed(1)} KB)`;
      } else {
        label.innerText = 'Select or Drop Document Scan (.pdf, .png, .jpg)';
      }
    }

    async function startIntelligentOcrExtraction() {
      const btn = document.getElementById('btn-run-ocr');
      const origHtml = btn.innerHTML;
      btn.innerHTML = '<span>⏳ Extracting & Scoring...</span>';
      btn.disabled = true;

      try {
        const formData = new FormData();
        const fileInput = document.getElementById('ocr-file');
        if (fileInput.files && fileInput.files[0]) {
          formData.append('file', fileInput.files[0]);
        } else if (selectedOcrSampleId) {
          formData.append('sample_id', selectedOcrSampleId);
        } else {
          formData.append('sample_id', 'maintenance');
        }

        const tTarget = document.getElementById('ocr-template-target').value;
        if (tTarget) formData.append('template_override', tTarget);
        formData.append('mode', document.getElementById('ocr-mode').value || 'fast');

        const res = await fetch('/api/intelligent-ocr-extract', {
          method: 'POST',
          body: formData,
        });

        if (!res.ok) throw new Error(`Extraction failed: ${res.statusText}`);
        const data = await res.json();

        // Render results box
        const resBox = document.getElementById('ocr-results-box');
        resBox.style.display = 'block';

        document.getElementById('ocr-res-template-title').innerText = `Matched: ${data.selected_template}`;
        document.getElementById('ocr-res-conf-pill').innerText = `${data.template_confidence}% Match`;
        document.getElementById('ocr-res-reason').innerText = data.template_reason || 'Autonomous template classification verified.';
        document.getElementById('ocr-res-tokens').innerText = data.total_tokens || 0;
        document.getElementById('ocr-res-mean-conf').innerText = data.mean_confidence_pct || '0%';
        document.getElementById('ocr-res-low-conf').innerText = data.low_confidence_count || 0;

        const actionsDiv = document.getElementById('ocr-res-actions');
        actionsDiv.innerHTML = '';

        if (data.files && data.files.xlsx_url) {
          actionsDiv.innerHTML += `
            <a href="${data.files.xlsx_url}" download class="btn sm" style="text-decoration:none;">
              <span>📥 Download Excel (${data.files.xlsx_filename})</span>
            </a>
          `;
        }
        if (data.files && data.files.docx_url) {
          actionsDiv.innerHTML += `
            <a href="${data.files.docx_url}" download class="btn sm" style="text-decoration:none;">
              <span>📥 Download Word (${data.files.docx_filename})</span>
            </a>
          `;
        }
        if (data.day_id) {
          actionsDiv.innerHTML += `
            <button type="button" class="btn sm primary" onclick="closeModal('modal-upload'); loadDayAnalytics('${data.day_id}');">
              <span>📊 Open in Fleet Analytics →</span>
            </button>
          `;
        }

        showToast(`Intelligent Extractor: Matched "${data.selected_template}" with ${data.total_tokens} verified tokens!`, '⚡');
      } catch (err) {
        showToast(`Extraction error: ${err.message}`, '⚠️');
      } finally {
        btn.innerHTML = origHtml;
        btn.disabled = false;
      }
    }"""

if old_js_tab in text:
    text = text.replace(old_js_tab, new_js_tab)

# Clean up any leftover registerTechManualShow
old_manual_func = """    function registerTechManualShow() {
      const mName = document.getElementById('manual-name').value || "BUSHIPS Reference Manual";
      closeModal('modal-upload');
      showToast(`📖 "${mName}" successfully indexed into AI Knowledge Base!`, "🏛️");
    }"""

if old_manual_func in text:
    text = text.replace(old_manual_func, "")

build_path.write_text(text, encoding="utf-8")
print("build_index_ui.py successfully updated with Intelligent OCR Extractor")

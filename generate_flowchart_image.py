"""
Generates a crisp, professional, high-resolution flowchart image showing how DECK works,
including all the different ways it takes in information.
Zero clip art or decorative images — purely geometric flowchart elements, arrows, and clean typography.
"""
from pathlib import Path
import pymupdf

def build_flowchart_svg() -> str:
    # 2000 x 1500 canvas
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1500" width="2000" height="1500">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090f16"/>
      <stop offset="100%" stop-color="#0f1924"/>
    </linearGradient>

    <!-- Marker arrows -->
    <marker id="arrowBrass" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#d6ae66"/>
    </marker>
    <marker id="arrowBlue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#4a90e2"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#48b58a"/>
    </marker>
    <marker id="arrowCoral" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#e06c53"/>
    </marker>
    <marker id="arrowPurple" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#9d72e6"/>
    </marker>
    <marker id="arrowSlate" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#718ba8"/>
    </marker>

    <!-- Glow / shadow filters -->
    <filter id="boxShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.45"/>
    </filter>
  </defs>

  <style>
    .title { font-family: 'Segoe UI', Arial, sans-serif; font-size: 34px; font-weight: 700; fill: #d6ae66; letter-spacing: 0.1em; }
    .subtitle { font-family: 'Segoe UI', Arial, sans-serif; font-size: 16px; font-weight: 400; fill: #b2a996; letter-spacing: 0.05em; }
    .section-title { font-family: 'Segoe UI', Arial, sans-serif; font-size: 18px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
    .section-subtitle { font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; font-weight: 400; fill: #8a9bb0; }
    .node-title { font-family: 'Segoe UI', Arial, sans-serif; font-size: 14.5px; font-weight: 700; fill: #ece6d6; }
    .node-desc { font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; font-weight: 400; fill: #b8af9c; }
    .node-code { font-family: 'Cascadia Mono', Consolas, monospace; font-size: 11px; fill: #718ba8; }
    .tag { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .line-label { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: 600; fill: #8a9bb0; }
  </style>

  <!-- Background -->
  <rect width="2000" height="1500" fill="url(#bgGrad)"/>

  <!-- Subtle Blueprint Grid lines -->
  <g stroke="#162330" stroke-width="1" opacity="0.4">
    <line x1="0" y1="120" x2="2000" y2="120"/>
    <line x1="0" y1="460" x2="2000" y2="460"/>
    <line x1="0" y1="800" x2="2000" y2="800"/>
    <line x1="0" y1="1140" x2="2000" y2="1140"/>
    <line x1="340" y1="120" x2="340" y2="1450"/>
    <line x1="680" y1="120" x2="680" y2="1450"/>
    <line x1="1020" y1="120" x2="1020" y2="1450"/>
    <line x1="1360" y1="120" x2="1360" y2="1450"/>
    <line x1="1700" y1="120" x2="1700" y2="1450"/>
  </g>

  <!-- =========================================================================
       HEADER SECTION
       ========================================================================= -->
  <g id="header" transform="translate(60, 45)">
    <!-- Header border box -->
    <rect x="0" y="0" width="1880" height="75" rx="6" fill="#111c27" stroke="#24374c" stroke-width="1.5" filter="url(#boxShadow)"/>
    <text x="35" y="38" class="title">DECK SYSTEM ARCHITECTURE &amp; INFORMATION INGESTION PIPELINE</text>
    <text x="35" y="60" class="subtitle">DOCUMENT EXTRACTION &amp; CONVERSION KIT — COMPLETE OPERATIONAL FLOWCHART</text>
    <rect x="1620" y="20" width="225" height="35" rx="4" fill="#172737" stroke="#334e6d" stroke-width="1"/>
    <text x="1732" y="42" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="#d6ae66" text-anchor="middle" letter-spacing="0.08em">FORMAL WORKFLOW SPEC</text>
  </g>

  <!-- =========================================================================
       STAGE 1: INGESTION CHANNELS (6 DISTINCT WAYS APP TAKES IN INFORMATION)
       ========================================================================= -->
  <g id="stage-1" transform="translate(60, 140)">
    <!-- Container panel -->
    <rect x="0" y="0" width="410" height="1290" rx="8" fill="#101a24" stroke="#22374d" stroke-width="1.5" filter="url(#boxShadow)"/>
    
    <rect x="20" y="20" width="370" height="42" rx="4" fill="#182c40" stroke="#2c4d70" stroke-width="1"/>
    <text x="35" y="44" class="section-title" fill="#4a90e2">STAGE 1: INFORMATION INTAKE</text>
    <text x="35" y="55" class="section-subtitle">6 Distinct Intake Channels Supported</text>

    <!-- INTAKE 1: Scanned Multi-Page PDF -->
    <g transform="translate(20, 80)">
      <rect x="0" y="0" width="370" height="175" rx="6" fill="#14212e" stroke="#2c4d70" stroke-width="1.2" filter="url(#boxShadow)"/>
      <rect x="15" y="15" width="115" height="20" rx="3" fill="#1c3752"/>
      <text x="22" y="29" class="tag" fill="#4a90e2">CHANNEL A</text>
      <text x="15" y="54" class="node-title">Scanned Multi-Page PDF</text>
      <text x="15" y="74" class="node-desc">Direct PDF file drop via upload modal or</text>
      <text x="15" y="91" class="node-desc">API endpoint (/api/intelligent-ocr-extract).</text>
      <text x="15" y="108" class="node-desc">Handles 1 to 50+ page logbooks &amp; maintenance</text>
      <text x="15" y="125" class="node-desc">procedure checkouts with automatic indexing.</text>
      <text x="15" y="150" class="node-code">Source: .pdf (Forms N.Nav 45, 52, NEng 10)</text>
    </g>

    <!-- INTAKE 2: Flatbed Scans & Digital Photos -->
    <g transform="translate(20, 275)">
      <rect x="0" y="0" width="370" height="175" rx="6" fill="#14212e" stroke="#2c4d70" stroke-width="1.2" filter="url(#boxShadow)"/>
      <rect x="15" y="15" width="115" height="20" rx="3" fill="#1c3752"/>
      <text x="22" y="29" class="tag" fill="#4a90e2">CHANNEL B</text>
      <text x="15" y="54" class="node-title">Flatbed &amp; Photo Scans</text>
      <text x="15" y="74" class="node-desc">High-resolution single/multi-page image</text>
      <text x="15" y="91" class="node-desc">uploads. Supports skewed document photos,</text>
      <text x="15" y="108" class="node-desc">creased pages, and vintage ink bleeding.</text>
      <text x="15" y="125" class="node-desc">Automated contrast &amp; DPI normalization.</text>
      <text x="15" y="150" class="node-code">Formats: .png, .jpg, .jpeg, .tiff</text>
    </g>

    <!-- INTAKE 3: Live Document Scanner / Camera -->
    <g transform="translate(20, 470)">
      <rect x="0" y="0" width="370" height="175" rx="6" fill="#14212e" stroke="#2c4d70" stroke-width="1.2" filter="url(#boxShadow)"/>
      <rect x="15" y="15" width="115" height="20" rx="3" fill="#1c3752"/>
      <text x="22" y="29" class="tag" fill="#4a90e2">CHANNEL C</text>
      <text x="15" y="54" class="node-title">Webcam &amp; Document Camera</text>
      <text x="15" y="74" class="node-desc">Real-time video feed capture directly in-browser.</text>
      <text x="15" y="91" class="node-desc">Designed for physical paper observation tables,</text>
      <text x="15" y="108" class="node-desc">handwritten station logs, and on-desk</text>
      <text x="15" y="125" class="node-desc">maintenance clipboard checkout sheets.</text>
      <text x="15" y="150" class="node-code">Source: WebRTC Video Stream &amp; Snapshot</text>
    </g>

    <!-- INTAKE 4: MFP Network Inbox Watcher -->
    <g transform="translate(20, 665)">
      <rect x="0" y="0" width="370" height="175" rx="6" fill="#14212e" stroke="#2c4d70" stroke-width="1.2" filter="url(#boxShadow)"/>
      <rect x="15" y="15" width="115" height="20" rx="3" fill="#1c3752"/>
      <text x="22" y="29" class="tag" fill="#4a90e2">CHANNEL D</text>
      <text x="15" y="54" class="node-title">MFP Network Inbox Watcher</text>
      <text x="15" y="74" class="node-desc">Automated directory daemon monitoring network</text>
      <text x="15" y="91" class="node-desc">scanners and multi-function printers.</text>
      <text x="15" y="108" class="node-desc">Auto-detects newly dropped scans in mfp_inbox/,</text>
      <text x="15" y="125" class="node-desc">triggers classification, and stages for review.</text>
      <text x="15" y="150" class="node-code">Directory: ./mfp_inbox/ / SMB / FTP Watch</text>
    </g>

    <!-- INTAKE 5: Live Tabular In-App Editor -->
    <g transform="translate(20, 860)">
      <rect x="0" y="0" width="370" height="175" rx="6" fill="#14212e" stroke="#2c4d70" stroke-width="1.2" filter="url(#boxShadow)"/>
      <rect x="15" y="15" width="115" height="20" rx="3" fill="#1c3752"/>
      <text x="22" y="29" class="tag" fill="#4a90e2">CHANNEL E</text>
      <text x="15" y="54" class="node-title">Interactive In-App Data Editor</text>
      <text x="15" y="74" class="node-desc">Direct user data input and modification of</text>
      <text x="15" y="91" class="node-desc">24 hourly rows (RPM, speed, course, weather)</text>
      <text x="15" y="108" class="node-desc">and daily fuel/water balances. Instant</text>
      <text x="15" y="125" class="node-desc">persistence via POST /api/day/{id}/update.</text>
      <text x="15" y="150" class="node-code">Interface: Expandable 24-Hour Tabular Grid</text>
    </g>

    <!-- INTAKE 6: Technical Manuals & Standard Reference Library -->
    <g transform="translate(20, 1055)">
      <rect x="0" y="0" width="370" height="175" rx="6" fill="#14212e" stroke="#2c4d70" stroke-width="1.2" filter="url(#boxShadow)"/>
      <rect x="15" y="15" width="115" height="20" rx="3" fill="#1c3752"/>
      <text x="22" y="29" class="tag" fill="#4a90e2">CHANNEL F</text>
      <text x="15" y="54" class="node-title">Technical Manual Library</text>
      <text x="15" y="74" class="node-desc">Pre-indexed engineering operating standards:</text>
      <text x="15" y="91" class="node-desc">BUSHIPS Chapter 41 (Gears &amp; Thrust Bearings),</text>
      <text x="15" y="108" class="node-desc">Chapter 51 (Boiler Drum PSI), Ch 55 (Speed/RPM),</text>
      <text x="15" y="125" class="node-desc">and Ch 58 (Distillation Water Testing).</text>
      <text x="15" y="150" class="node-code">Reference: ./manuals/ / BUSHIPS Chapters</text>
    </g>
  </g>

  <!-- =========================================================================
       STAGE 2: PREPROCESSING & FORM TEMPLATE CLASSIFICATION
       ========================================================================= -->
  <g id="stage-2" transform="translate(520, 140)">
    <rect x="0" y="0" width="340" height="1290" rx="8" fill="#101a24" stroke="#22374d" stroke-width="1.5" filter="url(#boxShadow)"/>
    
    <rect x="20" y="20" width="300" height="42" rx="4" fill="#282214" stroke="#5c4a23" stroke-width="1"/>
    <text x="35" y="44" class="section-title" fill="#d6ae66">STAGE 2: CLASSIFICATION</text>
    <text x="35" y="55" class="section-subtitle">Geometric Layout &amp; Form Matching</text>

    <!-- STEP 2.1: Page Geometry Survey -->
    <g transform="translate(20, 140)">
      <rect x="0" y="0" width="300" height="140" rx="6" fill="#18231a" stroke="#3c5240" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="32" class="node-title">Document Layout Survey</text>
      <text x="15" y="56" class="node-desc">Analyzes aspect ratio, column gridlines,</text>
      <text x="15" y="74" class="node-desc">header typography, table boundaries,</text>
      <text x="15" y="92" class="node-desc">and document ink density distribution.</text>
      <text x="15" y="118" class="node-code">Engine: Page Geometry &amp; Grid Matrix</text>
    </g>

    <!-- STEP 2.2: Decision Diamond / Classifier -->
    <g transform="translate(20, 360)">
      <!-- Diamond shape drawn as polygon -->
      <polygon points="150,10 290,90 150,170 10,90" fill="#241e12" stroke="#d6ae66" stroke-width="1.5" filter="url(#boxShadow)"/>
      <text x="150" y="75" class="node-title" text-anchor="middle" fill="#d6ae66">Autonomous Form</text>
      <text x="150" y="95" class="node-title" text-anchor="middle" fill="#d6ae66">Template Matcher</text>
      <text x="150" y="115" class="node-code" text-anchor="middle" fill="#b8af9c">Bayesian Classifier</text>
    </g>

    <!-- STEP 2.3: Template Selection Outputs -->
    <g transform="translate(20, 600)">
      <rect x="0" y="0" width="300" height="260" rx="6" fill="#141c24" stroke="#2f465e" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="30" class="node-title">Target Template Profiles</text>
      <text x="15" y="55" class="node-desc">Classifies into calibrated template families:</text>
      
      <rect x="15" y="72" width="270" height="34" rx="4" fill="#1a2736"/>
      <text x="25" y="93" font-family="'Segoe UI', Arial, sans-serif" font-size="11.5" font-weight="600" fill="#4a90e2">Deck Log Hourly Record (.xlsx)</text>

      <rect x="15" y="114" width="270" height="34" rx="4" fill="#1a2736"/>
      <text x="25" y="135" font-family="'Segoe UI', Arial, sans-serif" font-size="11.5" font-weight="600" fill="#4a90e2">Maintenance Procedure (.xlsx)</text>

      <rect x="15" y="156" width="270" height="34" rx="4" fill="#1a2736"/>
      <text x="25" y="177" font-family="'Segoe UI', Arial, sans-serif" font-size="11.5" font-weight="600" fill="#4a90e2">Equipment Inspection (.docx)</text>

      <rect x="15" y="198" width="270" height="34" rx="4" fill="#1a2736"/>
      <text x="25" y="219" font-family="'Segoe UI', Arial, sans-serif" font-size="11.5" font-weight="600" fill="#4a90e2">Watch Remarks Narrative (.docx)</text>

      <text x="15" y="248" class="node-code">Confidence: Computed % Match Score</text>
    </g>

    <!-- STEP 2.4: Resolution Fallback -->
    <g transform="translate(20, 930)">
      <rect x="0" y="0" width="300" height="130" rx="6" fill="#1a1c22" stroke="#3d372c" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="30" class="node-title">Custom / Unseen Layouts</text>
      <text x="15" y="54" class="node-desc">Fallback to dynamic cell extraction grid.</text>
      <text x="15" y="72" class="node-desc">Allows manual template override or</text>
      <text x="15" y="90" class="node-desc">generic observation table compilation.</text>
      <text x="15" y="112" class="node-code">Module: extract_arbitrary_pdf_page()</text>
    </g>
  </g>

  <!-- =========================================================================
       STAGE 3: OCR EXTRACTION & TOKEN CALIBRATION
       ========================================================================= -->
  <g id="stage-3" transform="translate(910, 140)">
    <rect x="0" y="0" width="340" height="1290" rx="8" fill="#101a24" stroke="#22374d" stroke-width="1.5" filter="url(#boxShadow)"/>
    
    <rect x="20" y="20" width="300" height="42" rx="4" fill="#1b2820" stroke="#33593f" stroke-width="1"/>
    <text x="35" y="44" class="section-title" fill="#48b58a">STAGE 3: OCR &amp; TOKENS</text>
    <text x="35" y="55" class="section-subtitle">Token Extraction &amp; Coordinate Mapping</text>

    <!-- STEP 3.1: Dual-Pass Optical Ingestion -->
    <g transform="translate(20, 120)">
      <rect x="0" y="0" width="300" height="160" rx="6" fill="#14211a" stroke="#2b4f38" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="32" class="node-title">Dual-Pass Optical Ingestion</text>
      <text x="15" y="56" class="node-desc">Pass 1: Fast layout survey &amp; printed boilerplate</text>
      <text x="15" y="74" class="node-desc">anchor identification (dates, columns, hours).</text>
      <text x="15" y="94" class="node-desc">Pass 2: High-gain adaptive thresholding for</text>
      <text x="15" y="112" class="node-desc">handwritten numbers, cursive text, and symbols.</text>
      <text x="15" y="140" class="node-code">Algorithm: Dual-Pass Adaptive Scanning</text>
    </g>

    <!-- STEP 3.2: Bounding Box Reticle Calibration -->
    <g transform="translate(20, 340)">
      <rect x="0" y="0" width="300" height="180" rx="6" fill="#14211a" stroke="#2b4f38" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="32" class="node-title">Bounding Box Reticle Mapping</text>
      <text x="15" y="56" class="node-desc">Every extracted cell is mapped to normalized</text>
      <text x="15" y="74" class="node-desc">coordinates [x, y, width, height] relative</text>
      <text x="15" y="92" class="node-desc">to the high-resolution source document scan.</text>
      <text x="15" y="112" class="node-desc">Calibrated Form 45 row pitches (dy=0.0103)</text>
      <text x="15" y="130" class="node-desc">and column x-offsets for hours 1-24.</text>
      <text x="15" y="158" class="node-code">Coordinates: [x, y, w, h] Normalized Box</text>
    </g>

    <!-- STEP 3.3: Confidence Scoring & Flagging -->
    <g transform="translate(20, 580)">
      <rect x="0" y="0" width="300" height="180" rx="6" fill="#14211a" stroke="#2b4f38" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="32" class="node-title">Token Confidence Scoring</text>
      <text x="15" y="56" class="node-desc">Evaluates character edge gradient, stroke clarity,</text>
      <text x="15" y="74" class="node-desc">and morphological stroke consistency.</text>
      <text x="15" y="100" class="node-desc">High Confidence (&gt;= 70%): Passed to auditor.</text>
      <text x="15" y="122" class="node-desc">Low Confidence (&lt; 70%): Flagged with yellow</text>
      <text x="15" y="140" class="node-desc">reticle and staged for human/AI verification.</text>
      <text x="15" y="162" class="node-code">Output: token_id, raw_val, conf_score</text>
    </g>

    <!-- STEP 3.4: Disambiguation & Continuity Resolution -->
    <g transform="translate(20, 820)">
      <rect x="0" y="0" width="300" height="170" rx="6" fill="#14211a" stroke="#2b4f38" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="32" class="node-title">Handwriting Disambiguation</text>
      <text x="15" y="56" class="node-desc">Resolves faded digits ('1' vs '7', '3' vs '8')</text>
      <text x="15" y="74" class="node-desc">using adjacent temporal hours and physical</text>
      <text x="15" y="92" class="node-desc">continuity bounds (barometer trends, speed).</text>
      <text x="15" y="116" class="node-desc">Provides suggested values with audit trail.</text>
      <text x="15" y="148" class="node-code">Module: disambiguate_token_with_gemma()</text>
    </g>
  </g>

  <!-- =========================================================================
       STAGE 4: REASONING, PHYSICAL AUDIT & ANOMALY DETECTION
       ========================================================================= -->
  <g id="stage-4" transform="translate(1300, 140)">
    <rect x="0" y="0" width="320" height="1290" rx="8" fill="#101a24" stroke="#22374d" stroke-width="1.5" filter="url(#boxShadow)"/>
    
    <rect x="20" y="20" width="280" height="42" rx="4" fill="#2a1a17" stroke="#633026" stroke-width="1"/>
    <text x="35" y="44" class="section-title" fill="#e06c53">STAGE 4: AUDIT &amp; FLAGS</text>
    <text x="35" y="55" class="section-subtitle">Physical Auditing &amp; Tech Manual Citations</text>

    <!-- STEP 4.1: Engineering Continuity Audit -->
    <g transform="translate(20, 100)">
      <rect x="0" y="0" width="280" height="160" rx="6" fill="#1f1816" stroke="#4a2a22" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="30" class="node-title">Engineering Equation Audit</text>
      <text x="15" y="54" class="node-desc">Verifies physical mass balances:</text>
      <text x="15" y="74" class="node-desc">- Fuel: Prior + Received - Expended = Rem</text>
      <text x="15" y="92" class="node-desc">- Water: Distilled vs Expended vs Reserve</text>
      <text x="15" y="112" class="node-desc">- Speed: Shaft RPM vs Steaming Knots</text>
      <text x="15" y="138" class="node-code">Audit: Mass Balances &amp; Dynamic Bounds</text>
    </g>

    <!-- STEP 4.2: Anomaly & Casualty Detection -->
    <g transform="translate(20, 290)">
      <rect x="0" y="0" width="280" height="180" rx="6" fill="#1f1816" stroke="#4a2a22" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="30" class="node-title">Casualty &amp; Anomaly Engine</text>
      <text x="15" y="54" class="node-desc">Detects machinery failure patterns:</text>
      <text x="15" y="74" class="node-desc">- Kingsbury Thrust Overheating (&gt;150 deg F)</text>
      <text x="15" y="94" class="node-desc">- Boiler Priming &amp; High Salinity (&gt;2.5 ep)</text>
      <text x="15" y="114" class="node-desc">- Unexplained RPM drop at high speed</text>
      <text x="15" y="134" class="node-desc">- Barometric storm plunges (&gt;0.20 in/hr)</text>
      <text x="15" y="158" class="node-code">Severity: CRITICAL, WARN, ADVISORY</text>
    </g>

    <!-- STEP 4.3: Tech Manual Citation Linking -->
    <g transform="translate(20, 500)">
      <rect x="0" y="0" width="280" height="200" rx="6" fill="#1f1816" stroke="#4a2a22" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="30" class="node-title">Technical Manual Citations</text>
      <text x="15" y="54" class="node-desc">Links identified anomalies directly to</text>
      <text x="15" y="72" class="node-desc">official technical manual standards:</text>
      <text x="15" y="94" class="node-desc">- BUSHIPS Ch 41 Sec 41-14: Thrust Clearance</text>
      <text x="15" y="114" class="node-desc">- BUSHIPS Ch 51 Sec 51-22: Drum Priming</text>
      <text x="15" y="134" class="node-desc">- BUSHIPS Ch 55 Sec 55-08: Shaft Vibration</text>
      <text x="15" y="154" class="node-desc">- BUSHIPS Ch 58 Sec 58-15: Salinity Limit</text>
      <text x="15" y="178" class="node-code">Output: Verbatim Manual Excerpt + Action</text>
    </g>

    <!-- STEP 4.4: Interactive Flag Review Modal -->
    <g transform="translate(20, 730)">
      <rect x="0" y="0" width="280" height="150" rx="6" fill="#1f1816" stroke="#4a2a22" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="15" y="30" class="node-title">Flag Review Drawer Modal</text>
      <text x="15" y="54" class="node-desc">Triggered by [ Review Flag ] button.</text>
      <text x="15" y="72" class="node-desc">Presents full machinery diagnostics, cited</text>
      <text x="15" y="90" class="node-desc">regulations, and corrective procedures.</text>
      <text x="15" y="108" class="node-desc">Allows operator sign-off and verification.</text>
      <text x="15" y="130" class="node-code">UI: #modal-tech-manual</text>
    </g>
  </g>

  <!-- =========================================================================
       STAGE 5: USER INTERACTION & EXPORT OUTPUTS
       ========================================================================= -->
  <g id="stage-5" transform="translate(1670, 140)">
    <rect x="0" y="0" width="270" height="1290" rx="8" fill="#101a24" stroke="#22374d" stroke-width="1.5" filter="url(#boxShadow)"/>
    
    <rect x="15" y="20" width="240" height="42" rx="4" fill="#201a2c" stroke="#4b3370" stroke-width="1"/>
    <text x="25" y="44" class="section-title" fill="#9d72e6">STAGE 5: OUTPUTS</text>
    <text x="25" y="55" class="section-subtitle">Dashboards, Exports &amp; Audit Trail</text>

    <!-- OUTPUT 1: Telemetry Dashboard -->
    <g transform="translate(15, 80)">
      <rect x="0" y="0" width="240" height="155" rx="6" fill="#181524" stroke="#3d2c5c" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="12" y="28" class="node-title">Telemetry Analytics</text>
      <text x="12" y="48" class="node-desc">Multi-metric dynamic charts:</text>
      <text x="12" y="66" class="node-desc">- Shaft RPM vs Thrust Temp</text>
      <text x="12" y="84" class="node-desc">- Boiler PSI vs Salinity</text>
      <text x="12" y="102" class="node-desc">- Steaming Speed Over Ground</text>
      <text x="12" y="120" class="node-desc">- Barometer &amp; Thermometer</text>
      <text x="12" y="142" class="node-code">Chart.js Engine</text>
    </g>

    <!-- OUTPUT 2: Point-to-Scan Linkage -->
    <g transform="translate(15, 255)">
      <rect x="0" y="0" width="240" height="165" rx="6" fill="#181524" stroke="#3d2c5c" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="12" y="28" class="node-title">Point-to-Scan Reticle</text>
      <text x="12" y="48" class="node-desc">Click ANY chart data point</text>
      <text x="12" y="66" class="node-desc">to open the original scan.</text>
      <text x="12" y="86" class="node-desc">Draws exact reticle around the</text>
      <text x="12" y="104" class="node-desc">handwritten source cell with</text>
      <text x="12" y="122" class="node-desc">3.2x magnification toggle.</text>
      <text x="12" y="150" class="node-code">UI: #modal-point-source</text>
    </g>

    <!-- OUTPUT 3: Populated Excel Master -->
    <g transform="translate(15, 440)">
      <rect x="0" y="0" width="240" height="135" rx="6" fill="#181524" stroke="#3d2c5c" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="12" y="28" class="node-title">Excel Master (.xlsx)</text>
      <text x="12" y="48" class="node-desc">Fully populated spreadsheet</text>
      <text x="12" y="66" class="node-desc">preserving formulas, cell styles,</text>
      <text x="12" y="84" class="node-desc">and formal header blocks.</text>
      <text x="12" y="102" class="node-desc">Downloadable via UI button.</text>
      <text x="12" y="124" class="node-code">Engine: openpyxl</text>
    </g>

    <!-- OUTPUT 4: Populated Word Master -->
    <g transform="translate(15, 595)">
      <rect x="0" y="0" width="240" height="135" rx="6" fill="#181524" stroke="#3d2c5c" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="12" y="28" class="node-title">Word Report (.docx)</text>
      <text x="12" y="48" class="node-desc">Official inspection &amp; narrative</text>
      <text x="12" y="66" class="node-desc">checkout documents generated</text>
      <text x="12" y="84" class="node-desc">with verified token data.</text>
      <text x="12" y="102" class="node-desc">Downloadable via UI button.</text>
      <text x="12" y="124" class="node-code">Engine: python-docx</text>
    </g>

    <!-- OUTPUT 5: Portable Standalone Archive -->
    <g transform="translate(15, 750)">
      <rect x="0" y="0" width="240" height="150" rx="6" fill="#181524" stroke="#3d2c5c" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="12" y="28" class="node-title">Portable HTML Bundle</text>
      <text x="12" y="48" class="node-desc">Zero-server, self-contained</text>
      <text x="12" y="66" class="node-desc">HTML archive file containing</text>
      <text x="12" y="84" class="node-desc">embedded base64 scans, data,</text>
      <text x="12" y="102" class="node-desc">and offline interactive charts.</text>
      <text x="12" y="122" class="node-desc">Shareable via USB or email.</text>
      <text x="12" y="142" class="node-code">File: Portable_Workbench.html</text>
    </g>

    <!-- OUTPUT 6: REST API Interface -->
    <g transform="translate(15, 920)">
      <rect x="0" y="0" width="240" height="140" rx="6" fill="#181524" stroke="#3d2c5c" stroke-width="1.2" filter="url(#boxShadow)"/>
      <text x="12" y="28" class="node-title">FastAPI Endpoints</text>
      <text x="12" y="48" class="node-desc">JSON API for headless</text>
      <text x="12" y="66" class="node-desc">integration &amp; bulk exports:</text>
      <text x="12" y="84" class="node-desc">- GET /api/day/{day_id}</text>
      <text x="12" y="100" class="node-desc">- POST /api/intelligent-ocr</text>
      <text x="12" y="116" class="node-desc">- GET /api/corpus/trends</text>
      <text x="12" y="132" class="node-code">Protocol: HTTP / JSON REST</text>
    </g>
  </g>

  <!-- =========================================================================
       CONNECTING ARROWS & PIPELINE BUS LINES
       ========================================================================= -->
  <!-- Intake Channels to Stage 2 Main Bus -->
  <g stroke="#4a90e2" stroke-width="2" fill="none">
    <!-- Channel A to Survey -->
    <path d="M 450, 305 L 500, 305 L 500, 350 L 540, 350" marker-end="url(#arrowBlue)"/>
    <!-- Channel B to Survey -->
    <path d="M 450, 500 L 500, 500 L 500, 350 L 540, 350"/>
    <!-- Channel C to Survey -->
    <path d="M 450, 700 L 485, 700 L 485, 350 L 540, 350"/>
    <!-- Channel D to Survey -->
    <path d="M 450, 890 L 475, 890 L 475, 350 L 540, 350"/>
  </g>

  <!-- Channel E (In-App Editor) directly to Stage 4 Audit & Stage 5 Charts -->
  <g stroke="#d6ae66" stroke-width="2" fill="none" stroke-dasharray="6,4">
    <!-- Channel E directly updates Stage 4 & 5 -->
    <path d="M 450, 1085 L 480, 1085 L 480, 1260 L 1260, 1260 L 1260, 320 L 1320, 320" marker-end="url(#arrowBrass)"/>
    <text x="800" y="1250" class="line-label" fill="#d6ae66">Direct Tabular Edits Recalculate Equations &amp; Telemetry Curves (POST /api/day/{id}/update)</text>
  </g>

  <!-- Channel F (Tech Manuals) directly to Stage 4 Citation Linker -->
  <g stroke="#e06c53" stroke-width="2" fill="none" stroke-dasharray="5,4">
    <path d="M 450, 1280 L 1280, 1280 L 1280, 740 L 1320, 740" marker-end="url(#arrowCoral)"/>
    <text x="820" y="1295" class="line-label" fill="#e06c53">Indexed Engineering Operating Standards (BUSHIPS Chapters 41, 51, 55, 58)</text>
  </g>

  <!-- Stage 2 Survey to Classifier Diamond -->
  <g stroke="#d6ae66" stroke-width="2" fill="none">
    <path d="M 690, 420 L 690, 500" marker-end="url(#arrowBrass)"/>
    <text x="700" y="465" class="line-label">Geometry Vectors</text>
  </g>

  <!-- Stage 2 Classifier Diamond to Template Profiles -->
  <g stroke="#d6ae66" stroke-width="2" fill="none">
    <path d="M 690, 670 L 690, 740" marker-end="url(#arrowBrass)"/>
    <text x="700" y="710" class="line-label">Template Match (&gt;75%)</text>
    <!-- Classifier to Fallback -->
    <path d="M 690, 670 L 690, 710 L 600, 710 L 600, 1070 L 690, 1070" marker-end="url(#arrowBrass)"/>
    <text x="500" y="880" class="line-label" transform="rotate(-90, 500, 880)">Unmatched (&lt;75%)</text>
  </g>

  <!-- Stage 2 Templates to Stage 3 Dual Pass OCR -->
  <g stroke="#48b58a" stroke-width="2" fill="none">
    <path d="M 840, 870 L 880, 870 L 880, 340 L 930, 340" marker-end="url(#arrowGreen)"/>
    <text x="850" y="580" class="line-label" transform="rotate(-90, 850, 580)">Matched Master Grid Coordinates</text>
  </g>

  <!-- Stage 3 Vertical Connections -->
  <g stroke="#48b58a" stroke-width="2" fill="none">
    <!-- Dual Pass to Reticle Bbox -->
    <path d="M 1080, 420 L 1080, 480" marker-end="url(#arrowGreen)"/>
    <!-- Reticle Bbox to Confidence Scoring -->
    <path d="M 1080, 660 L 1080, 720" marker-end="url(#arrowGreen)"/>
    <!-- Confidence to Disambiguation -->
    <path d="M 1080, 900 L 1080, 960" marker-end="url(#arrowGreen)"/>
    <text x="1090" y="935" class="line-label">Flagged (&lt;70%)</text>
  </g>

  <!-- Stage 3 to Stage 4 Audit Engine -->
  <g stroke="#e06c53" stroke-width="2" fill="none">
    <path d="M 1230, 740 L 1270, 740 L 1270, 320 L 1320, 320" marker-end="url(#arrowCoral)"/>
    <text x="1240" y="520" class="line-label" transform="rotate(-90, 1240, 520)">Structured Hourly &amp; Balance Tokens</text>
  </g>

  <!-- Stage 4 Vertical Connections -->
  <g stroke="#e06c53" stroke-width="2" fill="none">
    <!-- Equation Audit to Casualty Engine -->
    <path d="M 1460, 400 L 1460, 430" marker-end="url(#arrowCoral)"/>
    <!-- Casualty Engine to Tech Manual Linker -->
    <path d="M 1460, 610 L 1460, 640" marker-end="url(#arrowCoral)"/>
    <text x="1470" y="628" class="line-label">Identified Anomaly</text>
    <!-- Tech Manual Linker to Flag Review Modal -->
    <path d="M 1460, 840 L 1460, 870" marker-end="url(#arrowCoral)"/>
    <text x="1470" y="858" class="line-label">Cited Regulations</text>
  </g>

  <!-- Stage 4 to Stage 5 Output Connections -->
  <g stroke="#9d72e6" stroke-width="2" fill="none">
    <!-- Audit / Trends to Telemetry Analytics -->
    <path d="M 1600, 320 L 1640, 320 L 1640, 300 L 1685, 300" marker-end="url(#arrowPurple)"/>
    <!-- Point-to-Scan Linkage feedback to Stage 3 Bounding Boxes -->
    <path d="M 1685, 480 L 1650, 480 L 1650, 520 L 1230, 520" marker-end="url(#arrowGreen)" stroke="#48b58a" stroke-dasharray="4,4"/>
    <text x="1440" y="510" class="line-label" fill="#48b58a">Click Chart Point -> Retrieves Scanned Cell Bounding Box Reticle &amp; 3.2x Magnifier</text>

    <!-- Verified Tokens to Populated Excel / Word -->
    <path d="M 1600, 420 L 1640, 420 L 1640, 650 L 1685, 650" marker-end="url(#arrowPurple)"/>
    <path d="M 1640, 650 L 1640, 805 L 1685, 805" marker-end="url(#arrowPurple)"/>
    
    <!-- Portable Bundle generation -->
    <path d="M 1600, 780 L 1640, 780 L 1640, 960 L 1685, 960" marker-end="url(#arrowPurple)"/>

    <!-- API endpoints -->
    <path d="M 1600, 980 L 1640, 980 L 1640, 1130 L 1685, 1130" marker-end="url(#arrowPurple)"/>
  </g>

  <!-- =========================================================================
       FOOTER LEGEND (PURE FLOWCHART SYMBOLISM, ZERO CLIP ART)
       ========================================================================= -->
  <g id="legend" transform="translate(60, 1445)">
    <rect x="0" y="0" width="1880" height="40" rx="4" fill="#111c27" stroke="#24374c" stroke-width="1"/>
    
    <!-- Legend item 1: Ingestion -->
    <rect x="30" y="14" width="14" height="14" rx="2" fill="#14212e" stroke="#4a90e2" stroke-width="1.2"/>
    <text x="52" y="26" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#b8af9c">Intake Channel</text>

    <!-- Legend item 2: Classification -->
    <rect x="230" y="14" width="14" height="14" rx="2" fill="#18231a" stroke="#d6ae66" stroke-width="1.2"/>
    <text x="252" y="26" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#b8af9c">Template Classification</text>

    <!-- Legend item 3: OCR & Tokens -->
    <rect x="470" y="14" width="14" height="14" rx="2" fill="#14211a" stroke="#48b58a" stroke-width="1.2"/>
    <text x="492" y="26" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#b8af9c">OCR &amp; Reticle Coordinate Engine</text>

    <!-- Legend item 4: Reasoning & Audit -->
    <rect x="790" y="14" width="14" height="14" rx="2" fill="#1f1816" stroke="#e06c53" stroke-width="1.2"/>
    <text x="812" y="26" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#b8af9c">Engineering Audit &amp; BUSHIPS Citations</text>

    <!-- Legend item 5: Output & Exports -->
    <rect x="1140" y="14" width="14" height="14" rx="2" fill="#181524" stroke="#9d72e6" stroke-width="1.2"/>
    <text x="1162" y="26" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#b8af9c">Master Exports, Dashboards &amp; APIs</text>

    <!-- Decision Diamond -->
    <polygon points="1480,21 1488,14 1496,21 1488,28" fill="#241e12" stroke="#d6ae66" stroke-width="1"/>
    <text x="1506" y="26" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#b8af9c">Decision / Branch Point</text>

    <!-- Bi-directional Feedback -->
    <line x1="1720" y1="21" x2="1750" y2="21" stroke="#48b58a" stroke-width="1.5" stroke-dasharray="3,3"/>
    <text x="1760" y="26" font-family="'Segoe UI', Arial, sans-serif" font-size="12" fill="#b8af9c">Point-to-Scan Interactive Feedback</text>
  </g>

</svg>
"""

def generate_flowchart():
    svg_data = build_flowchart_svg()
    
    # Save SVG
    svg_path = Path("output/deck_app_flowchart.svg")
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg_data, encoding="utf-8")
    print(f"Saved SVG to {svg_path} ({len(svg_data)} bytes)")

    # Render ultra-crisp PNG via PyMuPDF at 200 DPI (approx 2778 x 2083 resolution)
    doc = pymupdf.open(stream=svg_data.encode("utf-8"), filetype="svg")
    page = doc[0]
    pix = page.get_pixmap(dpi=200)
    
    png_path = Path("output/deck_app_flowchart.png")
    pix.save(str(png_path))
    doc.close()
    print(f"Successfully generated high-resolution flowchart image: {png_path} ({pix.width}x{pix.height}, {png_path.stat().st_size:,} bytes)")

    # Also copy to static for web viewing / sidecar access
    static_png = Path("static/deck_app_flowchart.png")
    static_png.write_bytes(png_path.read_bytes())
    print(f"Copied to web-accessible path: {static_png}")

if __name__ == '__main__':
    generate_flowchart()

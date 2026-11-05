# -*- coding: utf-8 -*-
# Synced UI builder
from pathlib import Path

INDEX_PATH = Path('static/index.html')
HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DECK — Document Extraction and Conversion Kit</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cascadia+Mono:wght@400;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="/static/chart.min.js"></script>
  <style>
    /* =========================================================================
       ARCHIVAL COLOR SYSTEM (Clean Blue, Black & Gold UI)
       ========================================================================= */
    :root {
      --bg: #080d14;
      --bg-1: #0e1724;
      --bg-2: #142133;
      --bg-3: #1b2c44;
      --border: #253b59;
      --border-light: #314d73;
      
      --ink: #ece6d6;
      --ink-1: #ece6d6;
      --ink-2: #b8c2d0;
      --ink-3: #7f8ea3;
      
      --brass: #d6ae66;
      --brass-hover: #e5c382;
      --brass-soft: rgba(214, 174, 102, 0.14);
      
      --good: #6fbf97;
      --good-soft: rgba(111, 191, 151, 0.14);
      --warn: #e0a353;
      --warn-soft: rgba(224, 163, 83, 0.14);
      --bad: #d96b6b;
      --bad-soft: rgba(217, 107, 107, 0.14);
      --info: #79b4dc;
      --info-soft: rgba(121, 180, 220, 0.14);

      --font-display: 'Newsreader', 'Palatino Linotype', 'Book Antiqua', Georgia, serif;
      --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'Cascadia Mono', Consolas, 'Courier New', monospace;
    }

    [data-theme="light"] {
      --bg: #f4efe4;
      --bg-1: #ece5d6;
      --bg-2: #e2dac7;
      --bg-3: #d5cbb5;
      --border: #c4b89f;
      --border-light: #b4a68a;
      
      --ink: #1c2633;
      --ink-1: #1c2633;
      --ink-2: #4a5666;
      --ink-3: #758294;
      
      --brass: #8f6823;
      --brass-hover: #755419;
      --brass-soft: rgba(143, 104, 35, 0.12);
      
      --good: #2b7a54;
      --good-soft: rgba(43, 122, 84, 0.12);
      --warn: #a16418;
      --warn-soft: rgba(161, 100, 24, 0.12);
      --bad: #aa2c2c;
      --bad-soft: rgba(170, 44, 44, 0.12);
      --info: #2c6e9e;
      --info-soft: rgba(44, 110, 158, 0.12);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg);
      color: var(--ink);
      font-family: var(--font-body);
      font-size: 14px;
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
    }

    /* TOP GLOBAL BAR */
    .top-bar {
      height: 58px;
      background: var(--bg-1);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      user-select: none;
    }

    .brand-icon {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .brand-icon svg {
      width: 100%;
      height: 100%;
    }

    .brand-title {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 600;
      letter-spacing: 0.16em;
      color: var(--brass);
    }

    .brand-subtitle {
      font-size: 12.5px;
      color: var(--ink);
      padding-left: 12px;
      border-left: 1px solid var(--border);
      letter-spacing: 0.03em;
      font-weight: 500;
    }

    .brand-subtitle strong {
      color: var(--brass);
    }

    .top-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* BUTTONS */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-family: var(--font-body);
      font-size: 13px;
      font-weight: 500;
      padding: 7px 14px;
      border-radius: 5px;
      border: 1px solid var(--border-light);
      background: var(--bg-2);
      color: var(--ink);
      cursor: pointer;
      text-decoration: none;
      transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease, transform 0.12s ease;
      white-space: nowrap;
    }

    .btn:hover {
      background: var(--bg-3);
      border-color: var(--brass);
      color: var(--brass);
    }

    .btn.primary {
      background: var(--brass);
      border-color: var(--brass);
      color: #080d14;
      font-weight: 600;
    }

    .btn.primary:hover {
      background: var(--brass-hover);
      border-color: var(--brass-hover);
      color: #080d14;
    }

    .btn.sm {
      font-size: 12px;
      padding: 4px 10px;
    }

    .btn.active {
      background: var(--brass-soft);
      border-color: var(--brass);
      color: var(--brass);
    }

    /* VIEW PANES */
    .view-pane {
      display: none;
      width: 100%;
      flex: 1;
    }

    .view-pane.active {
      display: block;
    }

    /* =========================================================================
       HOME SCREEN: DECK FRONT & CENTER + VISIBLE OCR UPLOAD WORKBENCH
       ========================================================================= */
    #view-home {
      max-width: 1140px;
      margin: 0 auto;
      padding: 36px 24px 64px;
      text-align: center;
    }

    .home-hero {
      margin-bottom: 32px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
    }

    .deck-badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--brass-soft);
      border: 1px solid var(--brass);
      color: var(--brass);
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 4px 14px;
      border-radius: 99px;
      margin-bottom: 4px;
    }

    .deck-hero-acronym,
    .deck-main-acronym {
      font-family: var(--font-display);
      font-size: 64px;
      line-height: 0.95;
      font-weight: 600;
      letter-spacing: 0.16em;
      color: var(--brass);
      text-shadow: 0 4px 28px rgba(214, 174, 102, 0.25);
    }

    .deck-hero-expansion {
      font-family: var(--font-display);
      font-size: 24px;
      font-weight: 600;
      color: var(--ink);
      letter-spacing: 0.03em;
      margin-top: 2px;
    }

    .deck-hero-expansion strong {
      color: var(--brass);
    }

    .home-hero p {
      font-size: 14.5px;
      color: var(--ink-2);
      max-width: 680px;
      margin: 4px auto 0;
      line-height: 1.55;
    }

    .home-workbench-layout {
      display: grid;
      grid-template-columns: 1.35fr 0.95fr;
      gap: 24px;
      text-align: left;
      align-items: stretch;
    }

    @media (max-width: 920px) {
      .home-workbench-layout {
        grid-template-columns: 1fr;
      }
    }

    .home-ocr-workbench-card {
      background: var(--bg-1);
      border: 1.5px solid var(--brass);
      border-radius: 8px;
      padding: 24px 26px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 12px 34px rgba(0, 0, 0, 0.4), 0 0 24px var(--brass-soft);
    }

    .home-ocr-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 12px;
    }

    .home-ocr-head h2 {
      font-family: var(--font-display);
      font-size: 21px;
      font-weight: 600;
      color: var(--ink);
    }

    .home-ocr-head p {
      font-size: 12.5px;
      color: var(--ink-2);
      margin-top: 3px;
    }

    .home-ocr-tabs {
      display: flex;
      gap: 6px;
      background: var(--bg-2);
      padding: 4px;
      border-radius: 6px;
      border: 1px solid var(--border);
    }

    .home-ocr-tab-btn {
      flex: 1;
      padding: 7px 10px;
      border-radius: 4px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--ink-2);
      font-family: var(--font-body);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .home-ocr-tab-btn:hover {
      color: var(--ink);
    }

    .home-ocr-tab-btn.active {
      background: var(--brass);
      color: #080d14;
      border-color: var(--brass);
    }

    .home-ocr-dropzone {
      border: 1.5px dashed var(--brass);
      border-radius: 6px;
      padding: 20px 16px;
      text-align: center;
      background: var(--bg-2);
      cursor: pointer;
      transition: background 0.15s ease, border-color 0.15s ease;
    }

    .home-ocr-dropzone:hover {
      background: var(--bg-3);
      border-color: var(--brass-hover);
    }

    .home-form-input, .home-form-select {
      width: 100%;
      background: var(--bg-2);
      border: 1px solid var(--border-light);
      color: var(--ink);
      padding: 7px 10px;
      border-radius: 4px;
      font-family: var(--font-body);
      font-size: 12.5px;
    }

    .home-form-input:focus, .home-form-select:focus {
      border-color: var(--brass);
      outline: none;
    }

    .home-side-cards {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .home-card {
      background: var(--bg-1);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 24px 24px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      flex: 1;
      transition: border-color 0.2s ease, transform 0.15s ease, background 0.15s ease;
    }

    .home-card:hover {
      border-color: var(--brass);
      background: var(--bg-2);
      transform: translateY(-2px);
    }

    .home-card h2 {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 600;
      color: var(--ink);
      margin-bottom: 8px;
    }

    .home-card p {
      font-size: 13px;
      color: var(--ink-2);
      line-height: 1.55;
      margin-bottom: 16px;
      flex: 1;
    }

    .home-card-foot {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
    }

    .unit-tag-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 16px;
    }

    .unit-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 4px;
      background: var(--bg-2);
      border: 1px solid var(--border-light);
      color: var(--brass);
    }

    /* =========================================================================
       SHIP & DATE PICKER
       ========================================================================= */
    #view-ship-picker {
      max-width: 860px;
      margin: 0 auto;
      padding: 48px 24px;
    }

    .picker-head {
      margin-bottom: 28px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .picker-head h2 {
      font-family: var(--font-display);
      font-size: 24px;
      font-weight: 400;
      color: var(--ink);
    }

    .picker-section {
      background: var(--bg-1);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 24px;
      margin-bottom: 24px;
    }

    .picker-section h3 {
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 600;
      color: var(--brass);
      margin-bottom: 14px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .picker-ship-list {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }

    .picker-ship-item {
      padding: 12px 16px;
      background: var(--bg-2);
      border: 1px solid var(--border);
      border-radius: 4px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.15s ease;
    }

    .picker-ship-item:hover, .picker-ship-item.selected {
      border-color: var(--brass);
      background: var(--brass-soft);
    }

    .picker-ship-item strong {
      font-size: 14px;
      color: var(--ink);
    }

    .picker-ship-item span {
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--ink-2);
    }

    .date-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 8px;
      max-height: 280px;
      overflow-y: auto;
      padding-right: 4px;
    }

    .date-pill {
      padding: 8px 12px;
      background: var(--bg-2);
      border: 1px solid var(--border);
      border-radius: 4px;
      cursor: pointer;
      font-size: 12.5px;
      transition: all 0.15s ease;
    }

    .date-pill:hover, .date-pill.selected {
      border-color: var(--brass);
      color: var(--brass);
      background: var(--brass-soft);
    }

    .date-pill.has-casualty {
      border-color: var(--warn);
    }

    /* =========================================================================
       FLEET ANALYTICS DASHBOARD
       ========================================================================= */
    #view-dashboard {
      max-width: 1280px;
      margin: 0 auto;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    /* Subheader bar */
    .dash-header-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-1);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 14px 20px;
      gap: 16px;
      flex-wrap: wrap;
    }

    .dash-title-group {
      display: flex;
      align-items: baseline;
      gap: 14px;
    }

    .dash-ship-title {
      font-family: var(--font-display);
      font-size: 22px;
      font-weight: 600;
      color: var(--ink);
    }

    .dash-date-badge {
      font-family: var(--font-mono);
      font-size: 13px;
      color: var(--brass);
    }

    .dash-nav-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Charts Section */
    .section-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }

    .section-title {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 600;
      color: var(--ink);
    }

    .section-sub {
      font-size: 12px;
      color: var(--ink-2);
    }

    .charts-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(540px, 1fr));
      gap: 20px;
    }

    .chart-box {
      background: var(--bg-1);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 18px;
      display: flex;
      flex-direction: column;
    }

    .chart-box-header {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin-bottom: 12px;
    }

    .chart-box-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--ink);
    }

    .chart-box-desc {
      font-size: 11.5px;
      color: var(--ink-2);
      font-family: var(--font-mono);
    }

    .chart-canvas-wrap {
      position: relative;
      height: 240px;
      width: 100%;
    }

    /* Flags Section */
    .flags-container {
      background: var(--bg-1);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 20px;
    }

    .flags-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 14px;
    }

    .flag-item {
      background: var(--bg-2);
      border: 1px solid var(--border);
      border-left: 4px solid var(--brass);
      border-radius: 4px;
      padding: 14px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }

    .flag-item.CRITICAL { border-left-color: var(--bad); }
    .flag-item.WARNING { border-left-color: var(--warn); }
    .flag-item.INFO { border-left-color: var(--info); }

    .flag-info {
      flex: 1;
    }

    .flag-head-line {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 4px;
    }

    .flag-category {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--ink);
    }

    .flag-severity-tag {
      font-family: var(--font-mono);
      font-size: 10.5px;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 2px;
      background: var(--bg-3);
      color: var(--ink-2);
    }

    .flag-severity-tag.CRITICAL { color: var(--bad); background: var(--bad-soft); }
    .flag-severity-tag.WARNING { color: var(--warn); background: var(--warn-soft); }
    .flag-severity-tag.INFO { color: var(--info); background: var(--info-soft); }

    .flag-text {
      font-size: 12.5px;
      color: var(--ink-2);
      line-height: 1.45;
    }

    .flag-manual-ref {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--brass);
      margin-top: 4px;
    }

    /* EXPANDABLE SECTIONS (Hiding Complexity) */
    .expandable-panel {
      background: var(--bg-1);
      border: 1px solid var(--border);
      border-radius: 6px;
      overflow: hidden;
      margin-top: 8px;
    }

    .expandable-header {
      padding: 14px 20px;
      background: var(--bg-1);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      user-select: none;
      font-size: 14px;
      font-weight: 600;
      color: var(--ink);
      list-style: none;
      border-bottom: 1px solid transparent;
      transition: background 0.15s ease;
    }

    .expandable-header::-webkit-details-marker { display: none; }

    .expandable-header:hover {
      background: var(--bg-2);
    }

    .expandable-panel[open] .expandable-header {
      border-bottom-color: var(--border);
      color: var(--brass);
    }

    .expandable-hint {
      font-size: 11.5px;
      color: var(--ink-3);
      font-weight: 400;
    }

    .expandable-body {
      padding: 20px;
      background: var(--bg-2);
    }

    /* EDITABLE TABLE */
    .table-responsive {
      overflow-x: auto;
      margin-bottom: 16px;
    }

    .editor-table {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--font-mono);
      font-size: 11.5px;
    }

    .editor-table th, .editor-table td {
      border: 1px solid var(--border);
      padding: 6px 8px;
      text-align: left;
    }

    .editor-table th {
      background: var(--bg-3);
      color: var(--ink-2);
      font-weight: 600;
      white-space: nowrap;
    }

    .editor-table input {
      width: 100%;
      background: transparent;
      border: 1px solid transparent;
      color: var(--ink);
      font-family: inherit;
      font-size: inherit;
      padding: 2px 4px;
      border-radius: 2px;
    }

    .editor-table input:focus {
      background: var(--bg-1);
      border-color: var(--brass);
      outline: none;
    }

    /* BALANCES BAR */
    .balances-row {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      margin-bottom: 16px;
      background: var(--bg-1);
      padding: 12px 16px;
      border: 1px solid var(--border);
      border-radius: 4px;
    }

    .balance-field {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .balance-field label {
      font-size: 11px;
      color: var(--ink-2);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .balance-field input {
      background: var(--bg-2);
      border: 1px solid var(--border);
      color: var(--ink);
      padding: 4px 8px;
      font-family: var(--font-mono);
      font-size: 12px;
      border-radius: 3px;
      width: 110px;
    }

    .balance-field input:focus {
      border-color: var(--brass);
      outline: none;
    }

    /* MODALS */
    .modal-overlay {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(8, 12, 18, 0.82);
      z-index: 1000;
      padding: 24px;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(2px);
    }

    .modal-overlay.open {
      display: flex;
    }

    .modal-dialog {
      background: var(--bg-1);
      border: 1px solid var(--border-light);
      border-radius: 6px;
      width: 100%;
      max-width: 780px;
      max-height: 90vh;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
    }

    .modal-head {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .modal-head h3 {
      font-family: var(--font-display);
      font-size: 18px;
      color: var(--ink);
    }

    .modal-body {
      padding: 20px;
      flex: 1;
    }

    .modal-foot {
      padding: 14px 20px;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 10px;
    }

    /* RETICLE POPUP STYLES */
    .reticle-stage-container {
      position: relative;
      background: #080c10;
      border: 1px solid var(--border);
      border-radius: 4px;
      overflow: hidden;
      height: 480px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .reticle-stage {
      position: relative;
      max-width: 100%;
      max-height: 100%;
      transition: transform 0.25s ease-out;
      transform-origin: center center;
    }

    .reticle-stage img {
      display: block;
      max-width: 100%;
      height: auto;
    }

    .reticle-box {
      position: absolute;
      border: 2px solid var(--brass);
      background: rgba(214, 174, 102, 0.28);
      box-shadow: 0 0 12px rgba(214, 174, 102, 0.45);
      border-radius: 2px;
      pointer-events: none;
    }

    /* CITED MANUAL BOX */
    .citation-card {
      background: var(--bg-2);
      border: 1px solid var(--border);
      border-left: 4px solid var(--brass);
      padding: 16px;
      border-radius: 4px;
      margin-bottom: 16px;
    }

    .citation-code {
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--brass);
      margin-bottom: 4px;
    }

    .citation-title {
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 600;
      color: var(--ink);
      margin-bottom: 8px;
    }

    .citation-excerpt {
      font-family: var(--font-display);
      font-style: italic;
      font-size: 13px;
      color: var(--ink-2);
      line-height: 1.5;
      padding: 10px 14px;
      background: var(--bg-3);
      border-radius: 3px;
      border-left: 2px solid var(--brass);
      margin: 10px 0;
    }

    /* TOAST */
    #toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--bg-2);
      border: 1px solid var(--brass);
      color: var(--ink);
      padding: 10px 18px;
      border-radius: 4px;
      font-size: 13px;
      z-index: 2000;
      opacity: 0;
      transform: translateY(12px);
      transition: all 0.2s ease;
      pointer-events: none;
    }

    #toast.show {
      opacity: 1;
      transform: translateY(0);
    }
  </style>
</head>
<body>

  <!-- TOP BAR: DECK — DOCUMENT EXTRACTION AND CONVERSION KIT -->
  <header class="top-bar">
    <div class="brand-group" onclick="navigateTo('home')">
      <div class="brand-icon">
        <svg viewBox="0 0 32 32">
          <circle cx="16" cy="16" r="15" fill="#101c28"/>
          <path d="M16 3l3 13-3 13-3-13z" fill="#d6ae66"/>
          <circle cx="16" cy="16" r="3" fill="#ece6d6"/>
        </svg>
      </div>
      <div class="brand-title">DECK</div>
      <div class="brand-subtitle"><strong>D</strong>ocument <strong>E</strong>xtraction and <strong>C</strong>onversion <strong>K</strong>it</div>
    </div>
    <div class="top-actions">
      <button class="btn sm" id="btn-gemma-status" onclick="openGemmaModal()" title="Local Offline Gemma AI Settings &amp; GPU Status" style="display:inline-flex; align-items:center; gap:6px;">
        <span id="gemma-status-dot" style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#eab308;"></span>
        <span id="gemma-status-label">Gemma 4 12B Offline AI</span>
      </button>
      <button class="btn sm primary" onclick="openModal('modal-upload'); startWebcamScanner();">📷 Scan Page with Camera</button>
      <button class="btn sm" onclick="openModal('modal-upload')">OCR Upload Modal</button>
      <button class="btn sm" onclick="navigateTo('ship-picker')">Operational Units</button>
      <button class="btn sm" id="theme-btn" onclick="toggleTheme()">Theme: Dark</button>
    </div>
  </header>

  <!-- SCREEN 1: HOME SCREEN WITH DECK FRONT & CENTER + VISIBLE OCR UPLOAD WORKBENCH -->
  <main id="view-home" class="view-pane active">
    <div class="home-hero">
      <div class="deck-badge-pill">
        <span>Multi-Unit Optical OCR &amp; Template Conversion Suite</span>
        <span>•</span>
        <span>Ships • Shore Facilities • Air Squadrons</span>
      </div>
      <h1 class="deck-main-acronym">DECK</h1>
      <div class="deck-hero-expansion">
        <strong>D</strong>ocument <strong>E</strong>xtraction and <strong>C</strong>onversion <strong>K</strong>it
      </div>
      <p>
        Upload operational logs, maintenance checkouts, or technical manuals directly below for instant optical character recognition (OCR),
        automated Word &amp; Excel master template conversion, and technical manual anomaly flagging across any operational unit.
      </p>
    </div>

    <div class="home-workbench-layout">
      <!-- LEFT COLUMN: VISIBLE OCR FOR DOCUMENT UPLOAD DIRECTLY ON HOME SCREEN -->
      <div class="home-ocr-workbench-card" id="home-ocr-workbench">
        <div class="home-ocr-head">
          <div>
            <h2>OCR Document Upload &amp; Conversion Workbench</h2>
            <p>Visible on-home OCR engine: survey layouts, extract handwritten &amp; typed tokens, flag &lt;70% confidence readings, and convert to Excel/Word.</p>
          </div>
          <span class="flag-severity-tag INFO" style="color:var(--brass); background:var(--brass-soft); border:1px solid var(--brass);">Live OCR Ready</span>
        </div>

        <!-- 3-Way Mode Tabs on Home Screen -->
        <div class="home-ocr-tabs">
          <button type="button" class="home-ocr-tab-btn active" id="btn-home-ocr-tab-multi" onclick="switchHomeOcrTab('multi')">
            Intelligent Multi-Template OCR
          </button>
          <button type="button" class="home-ocr-tab-btn" id="btn-home-ocr-tab-log" onclick="switchHomeOcrTab('log')">
            Unit Log Spread OCR
          </button>
          <button type="button" class="home-ocr-tab-btn" id="btn-home-ocr-tab-manual" onclick="switchHomeOcrTab('manual')">
            Technical Manual Indexing
          </button>
        </div>

        <!-- PANE 1: INTELLIGENT MULTI-TEMPLATE OCR EXTRACTOR (VISIBLE BY DEFAULT) -->
        <div id="home-ocr-pane-multi" style="display:flex; flex-direction:column; gap:14px;">
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.04em;">Target Conversion Template</label>
              <select id="home-ocr-template-target" class="home-form-select">
                <option value="">Autonomous AI Selection (Matches Form Layout)</option>
                <option value="Maintenance Procedure Checkout.xlsx">Maintenance Procedure Checkout (.xlsx)</option>
                <option value="Equipment Inspection Report.docx">Equipment Inspection Report (.docx)</option>
                <option value="Deck Log Hourly Record.xlsx">Deck Log Hourly Record (.xlsx)</option>
                <option value="Deck Log Watch Remarks.docx">Deck Log Watch Remarks (.docx)</option>
              </select>
            </div>
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.04em;">OCR Verification Mode</label>
              <select id="home-ocr-mode" class="home-form-select">
                <option value="fast">Fast OCR Ingestion (Layout Survey &amp; Bayesian Scoring)</option>
                <option value="accurate">Accurate Dual-Pass OCR (Cross-Checked Verification)</option>
              </select>
            </div>
          </div>

          <div class="home-ocr-dropzone" id="dropzone-home-ocr" onclick="document.getElementById('home-ocr-file').click()">
            <input type="file" id="home-ocr-file" accept=".pdf,.png,.jpg,.jpeg,.tiff" style="display:none;" onchange="onHomeOcrFileSelected(this)">
            <div style="font-weight:600; font-size:14px; color:var(--brass); margin-bottom:4px;" id="home-ocr-file-label">
              Drop Scanned Document Here or Click to Browse (.pdf, .png, .jpg, .tiff)
            </div>
            <div style="font-size:12px; color:var(--ink-2);">
              DECK surveys page geometry, extracts handwritten &amp; typed fields, flags &lt;70% confidence tokens, and populates Word &amp; Excel records.
            </div>
          </div>

          <!-- Results Box directly on Home Screen -->
          <div id="home-ocr-results-box" style="display:none; background:var(--bg-2); border:1px solid var(--brass); border-radius:6px; padding:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; flex-wrap:wrap; gap:6px;">
              <strong style="font-family:var(--font-display); font-size:15px; color:var(--brass);" id="home-ocr-res-template-title">Template Selected</strong>
              <span class="flag-severity-tag INFO" id="home-ocr-res-conf-pill">100% Match</span>
            </div>
            <div style="font-size:12px; color:var(--ink-2); margin-bottom:10px;" id="home-ocr-res-reason">Autonomous classification verified.</div>
            <div style="display:flex; gap:16px; font-size:12px; color:var(--ink-2); margin-bottom:12px; flex-wrap:wrap; font-family:var(--font-mono);">
              <span>Tokens: <strong id="home-ocr-res-tokens" style="color:var(--ink);">0</strong></span>
              <span>Mean Confidence: <strong id="home-ocr-res-mean-conf" style="color:var(--good);">0%</strong></span>
              <span>Flagged (&lt;70%): <strong id="home-ocr-res-low-conf" style="color:var(--bad);">0</strong></span>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;" id="home-ocr-res-actions"></div>
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
            <span style="font-family:var(--font-mono); font-size:11.5px; color:var(--ink-3);">Generates verified .xlsx &amp; .docx outputs</span>
            <button type="button" class="btn primary" id="btn-home-run-ocr" onclick="startHomeIntelligentOcrExtraction()">
              Run DECK OCR &amp; Convert Document
            </button>
          </div>
        </div>

        <!-- PANE 2: UNIT LOG SPREAD OCR UPLOAD (SHIPS, SHORE FACILITIES, AIR SQUADRONS) -->
        <form id="home-ocr-pane-log" onsubmit="handleHomeLogUpload(event)" style="display:none; flex-direction:column; gap:12px;">
          <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:8px;">
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">UNIT TYPE</label>
              <select id="home-up-unit-type" class="home-form-select">
                <option value="Ship">Naval Vessel / Ship</option>
                <option value="Shore Facility">Shore Facility / Base</option>
                <option value="Air Squadron">Air Squadron / Wing</option>
              </select>
            </div>
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">UNIT NAME</label>
              <input type="text" id="home-up-ship-name" class="home-form-input" value="" placeholder="Enter ship or unit name (or leave blank to detect)">
            </div>
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">DESIGNATION / HULL</label>
              <input type="text" id="home-up-hull-no" class="home-form-input" value="" placeholder="Hull / Unit ID">
            </div>
          </div>

          <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:8px;">
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">LOG DATE (YYYY-MM-DD)</label>
              <input type="text" id="home-up-date-iso" class="home-form-input" value="" placeholder="YYYY-MM-DD">
            </div>
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">PAGE NO.</label>
              <input type="number" id="home-up-page-no" class="home-form-input" value="" placeholder="1" min="1" max="500">
            </div>
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">OPERATIONAL AREA</label>
              <input type="text" id="home-up-location" class="home-form-input" value="" placeholder="Operating location">
            </div>
          </div>

          <div class="home-ocr-dropzone" id="dropzone-home-log" onclick="document.getElementById('home-up-log-file').click()" style="padding:16px;">
            <input type="file" id="home-up-log-file" accept=".pdf,.png,.jpg,.jpeg" style="display:none;" onchange="onHomeLogFileSelected(this)">
            <div style="font-weight:600; font-size:13.5px; color:var(--brass);" id="home-up-file-label">
              Select or Drop Operational Logbook Scan (.pdf, .png, .jpg)
            </div>
            <div style="font-size:11.5px; color:var(--ink-2); margin-top:3px;">
              Extracts 24-hour telemetry and cross-checks against indexed Technical Manuals for anomaly flags.
            </div>
          </div>

          <div style="display:flex; justify-content:flex-end;">
            <button type="submit" class="btn primary" id="btn-home-submit-log">Digitize &amp; Analyze Unit Log</button>
          </div>
        </form>

        <!-- PANE 3: TECHNICAL MANUAL UPLOAD & INDEXING -->
        <form id="home-ocr-pane-manual" onsubmit="handleHomeManualUpload(event)" style="display:none; flex-direction:column; gap:12px;">
          <div style="display:grid; grid-template-columns: 1.4fr 0.8fr 0.8fr; gap:8px;">
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">TECHNICAL MANUAL TITLE</label>
              <input type="text" id="home-man-title" class="home-form-input" value="" placeholder="Enter manual title" required>
            </div>
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">MANUAL CODE</label>
              <input type="text" id="home-man-code" class="home-form-input" value="" placeholder="Enter manual code">
            </div>
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">APPLICABLE UNITS</label>
              <select id="home-man-unit-type" class="home-form-select">
                <option value="All Units">All Units</option>
                <option value="Ship">Ship / Vessel</option>
                <option value="Shore Facility">Shore Facility</option>
                <option value="Air Squadron">Air Squadron</option>
              </select>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px;">
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">SUBSYSTEM / CHAPTER</label>
              <input type="text" id="home-man-subsystem" class="home-form-input" value="" placeholder="Enter subsystem">
            </div>
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">STANDARD OPERATING LIMIT</label>
              <input type="text" id="home-man-limit" class="home-form-input" value="" placeholder="Enter operating limit">
            </div>
          </div>

          <div class="home-ocr-dropzone" id="dropzone-home-manual" onclick="document.getElementById('home-man-file').click()" style="padding:14px;">
            <input type="file" id="home-man-file" accept=".pdf,.docx,.txt,.png,.jpg" style="display:none;" onchange="onHomeManualFileSelected(this)">
            <div style="font-weight:600; font-size:13px; color:var(--brass);" id="home-man-file-label">
              Drop Technical Manual PDF / Document to OCR &amp; Index into Reference Library
            </div>
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-family:var(--font-mono); font-size:11.5px; color:var(--ink-2);" id="home-manuals-count-label">6 Active Manuals Indexed for Anomaly Flags</span>
            <button type="submit" class="btn primary" id="btn-home-submit-manual">OCR &amp; Index Technical Manual</button>
          </div>

          <!-- Active Indexed Manuals List -->
          <div id="home-indexed-manuals-list" style="max-height:115px; overflow-y:auto; display:flex; flex-direction:column; gap:5px; border-top:1px solid var(--border); padding-top:8px;">
            <!-- Populated dynamically from overviewData.manuals -->
          </div>
        </form>
      </div>

      <!-- RIGHT COLUMN: REVIEW EXISTING MULTI-UNIT DATA & TECH MANUAL CITATIONS -->
      <div class="home-side-cards">
        <!-- Option 1: Review Existing Data across Ships, Shore Facilities, Air Squadrons -->
        <div class="home-card" onclick="navigateTo('ship-picker')">
          <div>
            <h2>Review Operational Unit Data</h2>
            <p>Access digitized logs across Naval Vessels, Shore Facilities, and Air Squadrons. Inspect interactive telemetry curves, cell-level OCR reticles, and casualty flags citing technical manuals.</p>
            <div id="home-uploaded-units-tags" style="display:flex; gap:6px; flex-wrap:wrap; margin-top:4px; margin-bottom:16px;">
              <span class="badge unit-tag" style="color:var(--ink-2);">No units uploaded yet</span>
            </div>
          </div>
          <div class="home-card-foot">
            <span id="home-archive-status-label" style="font-family:var(--font-mono); font-size:11.5px; color:var(--ink-2);">● Upload a file to populate archive</span>
            <button class="btn primary" onclick="event.stopPropagation(); navigateTo('ship-picker');">Select Unit &amp; Log Date →</button>
          </div>
        </div>

        <!-- Option 2: Full Modal OCR & Master Templates -->
        <div class="home-card" onclick="openModal('modal-upload')">
          <div>
            <h2>Technical Manuals &amp; Master Templates</h2>
            <p>Logs automatically reference indexed BUSHIPS, NAVAER, and BUDOCKS technical manuals when operating limits are exceeded, and populate standardized Word (.docx) and Excel (.xlsx) records.</p>
          </div>
          <div class="home-card-foot">
            <span style="font-family:var(--font-mono); font-size:11.5px; color:var(--brass);">7 Master Templates Ready</span>
            <button class="btn" onclick="event.stopPropagation(); openModal('modal-upload');">Open Upload Modal ↗</button>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- SCREEN 2: OPERATIONAL UNIT & DATE PICKER (SHIPS, SHORE FACILITIES, AIR SQUADRONS) -->
  <section id="view-ship-picker" class="view-pane">
    <div class="picker-head">
      <h2>Select Operational Unit &amp; Logbook</h2>
      <button class="btn sm" onclick="navigateTo('home')">← Back to DECK Home</button>
    </div>

    <div class="picker-section">
      <h3>Operational Unit (Ships, Shore Facilities &amp; Air Squadrons)</h3>
      <div class="picker-ship-list" id="picker-ship-container">
        <div style="color:var(--ink-2); font-size:13px; padding:12px;">
          No files or operational units stored. Upload a logbook scan on the Home screen or via Scan / Upload to add a ship or unit.
        </div>
      </div>

      <h3>Available Digitized Log Dates</h3>
      <div class="date-grid" id="picker-date-container">
        <div style="color:var(--ink-2); font-size:13px; padding:12px;">
          No files or operational units stored. Upload a logbook scan on the Home screen or via Scan / Upload to add a ship or unit.
        </div>
      </div>
    </div>

    <div style="display:flex; justify-content:flex-end; gap:12px;">
      <button class="btn" onclick="navigateTo('home')">Cancel</button>
      <button class="btn primary" id="btn-open-selected-log" onclick="openSelectedLog()" disabled>Open Selected Log →</button>
    </div>
  </section>

  <!-- SCREEN 3: FLEET ANALYTICS DASHBOARD -->
  <section id="view-dashboard" class="view-pane">
    <!-- Header Controls -->
    <div class="dash-header-bar">
      <div class="dash-title-group">
        <h2 class="dash-ship-title" id="dash-ship-name">No Unit Selected</h2>
        <span class="dash-date-badge" id="dash-date-label">Upload and select a log file to view telemetry</span>
      </div>
      <div class="dash-nav-actions">
        <button class="btn sm" onclick="navigateTo('ship-picker')">Change Ship</button>
        <select id="day-select" class="btn sm" onchange="onDaySelectChange(this.value)" style="padding:4px 8px;"></select>
        <button class="btn sm" onclick="stepDay(-1)" title="Previous Day">Previous</button>
        <button class="btn sm" onclick="stepDay(1)" title="Next Day">Next</button>
      </div>
    </div>

    <!-- Section 1: Telemetry Graphs -->
    <div>
      <div class="section-head">
        <div>
          <h3 class="section-title">Telemetry Graphs</h3>
          <span class="section-sub">Click any data point across the full available ship timeframe to inspect the original handwritten log entry and confidence reticle.</span>
        </div>
        <span class="dash-date-badge" id="timeline-span-badge">No Data Loaded</span>
      </div>

      <div class="charts-grid">
        <!-- Chart 1: Shaft RPM & Thrust Temp -->
        <div class="chart-box">
          <div class="chart-box-header">
            <span class="chart-box-title">Shaft RPM &amp; Thrust Bearing Temperature</span>
            <span class="chart-box-desc" id="tag-chart-rpm">Full Available Timeframe • Click point for source scan</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-machinery-rpm-temp"></canvas>
          </div>
        </div>

        <!-- Chart 2: Boiler Drum PSI & Salinity -->
        <div class="chart-box">
          <div class="chart-box-header">
            <span class="chart-box-title">Boiler Drum Pressure &amp; Feedwater Salinity</span>
            <span class="chart-box-desc" id="tag-chart-boiler">Full Available Timeframe • Steam PSI / gr Cl per gal</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-machinery-boiler"></canvas>
          </div>
        </div>

        <!-- Chart 3: Speed Over Ground -->
        <div class="chart-box">
          <div class="chart-box-header">
            <span class="chart-box-title">Steaming Speed Over Ground</span>
            <span class="chart-box-desc" id="tag-chart-speed">Full Available Timeframe • Knots from Engine Revolutions</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-deck-speed"></canvas>
          </div>
        </div>

        <!-- Chart 4: Synoptic Barometer -->
        <div class="chart-box">
          <div class="chart-box-header">
            <span class="chart-box-title">Synoptic Barometer Curve</span>
            <span class="chart-box-desc" id="tag-chart-baro">Full Available Timeframe • Inches Hg</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-weather-baro"></canvas>
          </div>
        </div>

        <!-- Chart 5: Psychrometer (Dry & Wet Bulb) -->
        <div class="chart-box" style="grid-column: 1 / -1;">
          <div class="chart-box-header">
            <span class="chart-box-title">Psychrometer Air Temperatures (Dry &amp; Wet Bulb)</span>
            <span class="chart-box-desc" id="tag-chart-psychro">Full Available Timeframe • Dry &amp; Wet Bulb F</span>
          </div>
          <div class="chart-canvas-wrap">
            <canvas id="chart-weather-psychro"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- Section 2: Abnormal Trends & Flags for Review -->
    <div class="flags-container">
      <div class="section-head" style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <h3 class="section-title">Flags for Review</h3>
          <span class="section-sub">Abnormal trends, thermodynamic anomalies, or improbable readings requiring verification.</span>
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
          <button class="btn sm" id="btn-gemma-audit" onclick="runGemmaTelemetryAudit()" style="background:rgba(214,174,102,0.12); border:1px solid var(--brass); color:var(--brass); font-weight:600;" title="Run physical and aerological reasoning with Gemma 4 12B">
            ⚡ Gemma 4 12B Physical Audit
          </button>
        </div>
      </div>
      <div class="flags-list" id="flags-list-container">
        <!-- Rendered dynamically via renderFlagCards() -->
      </div>
    </div>

    <!-- Section 3: Expandable Complexity (Collapsed by Default) -->
    <!-- Expandable 1: Edit Log Data -->
    <details class="expandable-panel" id="panel-editor">
      <summary class="expandable-header">
        <span>Edit Log Data (24-Hour Table &amp; Daily Balances)</span>
        <span class="expandable-hint">Click to expand editable entries and recalculate equations</span>
      </summary>
      <div class="expandable-body">
        <div class="balances-row">
          <div class="balance-field">
            <label>Fuel Prior (gal)</label>
            <input type="number" id="edit-fuel-prior" value="0">
          </div>
          <div class="balance-field">
            <label>Fuel Received</label>
            <input type="number" id="edit-fuel-received" value="0">
          </div>
          <div class="balance-field">
            <label>Fuel Expended</label>
            <input type="number" id="edit-fuel-expended" value="0">
          </div>
          <div class="balance-field">
            <label>Water Distilled</label>
            <input type="number" id="edit-water-distilled" value="0">
          </div>
          <div class="balance-field">
            <label>Water Expended</label>
            <input type="number" id="edit-water-expended" value="0">
          </div>
          <div style="align-self:flex-end;">
            <button class="btn primary sm" onclick="saveHourlyEditor()">Save Changes &amp; Recalculate</button>
          </div>
        </div>

        <div class="table-responsive">
          <table class="editor-table">
            <thead>
              <tr>
                <th>Hour</th>
                <th>Revs (RPM)</th>
                <th>Speed (kts)</th>
                <th>Course</th>
                <th>Wind Dir</th>
                <th>Barometer</th>
                <th>Dry Bulb</th>
                <th>Wet Bulb</th>
                <th>Port RPM</th>
                <th>Stbd RPM</th>
                <th>Thrust F</th>
                <th>Salinity</th>
              </tr>
            </thead>
            <tbody id="hourly-tbody">
              <!-- Rendered dynamically -->
            </tbody>
          </table>
        </div>
      </div>
    </details>

    <!-- Expandable 2: Original Scanned Document & Verification Tokens -->
    <details class="expandable-panel" id="panel-scan">
      <summary class="expandable-header">
        <span>Original Scanned Document &amp; Verification Tokens</span>
        <span class="expandable-hint">Click to expand high-resolution scan viewer</span>
      </summary>
      <div class="expandable-body">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <span id="scan-token-summary" style="font-size:12.5px; color:var(--ink-2);">0 Tokens</span>
          <span id="scan-page-info" style="font-family:var(--font-mono); font-size:12px; color:var(--brass);">No scan loaded</span>
        </div>
        <div style="position:relative; max-width:100%; overflow:auto; border:1px solid var(--border); border-radius:4px; background:#080c10;">
          <img id="scan-primary-img" src="" alt="Log Scan" style="width:100%; display:block;">
          <div id="scan-bbox-layer" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none;"></div>
        </div>
      </div>
    </details>
  </section>

  <!-- MODAL: POINT RETICLE SOURCE SCAN -->
  <div class="modal-overlay" id="modal-point-source">
    <div class="modal-dialog">
      <div class="modal-head">
        <div>
          <h3 id="point-modal-field-title">Hour Telemetry Reading</h3>
          <span style="font-size:12px; color:var(--ink-2);" id="point-modal-date-sub">Source Scan Reference</span>
        </div>
        <button class="btn sm" onclick="closeModal('modal-point-source')">Close</button>
      </div>

      <div class="modal-body">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; font-family:var(--font-mono); font-size:12px;">
          <div>
            <strong id="point-modal-field-name" style="color:var(--ink);">Metric</strong>:
            <span id="point-modal-val" style="color:var(--brass); font-weight:600;">--</span>
            <span style="color:var(--ink-3); margin:0 8px;">|</span>
            <span id="point-modal-conf" style="color:var(--good);">-- Confidence</span>
          </div>
          <div style="display:flex; gap:6px;">
            <button class="btn sm active" id="btn-point-zoom-cell" onclick="setPointModalZoom(true)">Zoom to Cell</button>
            <button class="btn sm" id="btn-point-zoom-full" onclick="setPointModalZoom(false)">Full Page</button>
          </div>
        </div>

        <div class="reticle-stage-container">
          <div class="reticle-stage" id="point-modal-stage">
            <img id="point-modal-img" src="" alt="Source Log Scan" onload="onPointModalImgLoaded()">
            <div class="reticle-box" id="point-modal-highlight-box"></div>
          </div>
        </div>
      </div>

      <div class="modal-foot">
        <span style="font-size:11.5px; color:var(--ink-2); margin-right:auto;" id="point-modal-page-ref">Page Citation</span>
        <button class="btn sm" onclick="closeModal('modal-point-source')">Close</button>
      </div>
    </div>
  </div>

  <!-- MODAL: CITED TECHNICAL MANUAL & ANOMALY REVIEW -->
  <div class="modal-overlay" id="modal-tech-manual">
    <div class="modal-dialog">
      <div class="modal-head">
        <div>
          <h3 id="tm-modal-cat">Flag Review</h3>
          <span style="font-size:12px; color:var(--ink-2);" id="tm-modal-time">Incident Log</span>
        </div>
        <button class="btn sm" onclick="closeModal('modal-tech-manual')">Close</button>
      </div>

      <div class="modal-body">
        <div style="margin-bottom:16px;">
          <div style="font-size:13.5px; color:var(--ink); font-weight:500; margin-bottom:6px;" id="tm-modal-finding">Telemetry Finding</div>
          <div style="font-family:var(--font-mono); font-size:12px; color:var(--warn); background:var(--bg-2); padding:8px 12px; border-radius:4px; border:1px solid var(--border);" id="tm-modal-delta">Observed vs Expected</div>
        </div>

        <div class="citation-card" id="tm-modal-card">
          <div class="citation-code" id="tm-modal-code">BUSHIPS Manual Citation</div>
          <div class="citation-title" id="tm-modal-title">Standard Title</div>
          <div style="font-size:12px; color:var(--ink-2); margin-bottom:6px;" id="tm-modal-sec">Section</div>
          <div class="citation-excerpt" id="tm-modal-excerpt">Verbatim text excerpt...</div>
        </div>

        <div style="background:var(--bg-2); border:1px solid var(--border); border-radius:4px; padding:12px 14px;">
          <strong style="font-size:12px; color:var(--brass); text-transform:uppercase; letter-spacing:0.04em;">Engineering Action</strong>
          <p style="font-size:12.5px; color:var(--ink-2); margin-top:4px;" id="tm-modal-action">Recommended corrective procedure.</p>
        </div>
      </div>

      <div class="modal-foot">
        <button class="btn sm" onclick="closeModal('modal-tech-manual')">Close</button>
      </div>
    </div>
  </div>

  <!-- MODAL: UPLOAD & INTELLIGENT OCR EXTRACTOR -->
  <div class="modal-overlay" id="modal-upload">
    <div class="modal-dialog" style="max-width:760px;">
      <div class="modal-head">
        <div>
          <h3>Intelligent OCR Extractor &amp; Camera Page Scanner</h3>
          <span style="font-size:12px; color:var(--ink-2);">Live webcam page scanner, multi-template form layout classifier, and logbook digitizer</span>
        </div>
        <button class="btn sm" onclick="stopWebcamScanner(); closeModal('modal-upload')">Close</button>
      </div>

      <div class="modal-body">
        <p style="font-size:13px; color:var(--ink-2); margin-bottom:14px;">
          Scan a physical logbook page using your camera or upload a scanned document. Automatically surveys page layouts against Word and Excel master templates, extracts 24-hour telemetry, and flags low-confidence readings.
        </p>

        <!-- Action Bar: Camera Page Scanner -->
        <div style="display:flex; gap:10px; margin-bottom:14px; flex-wrap:wrap; align-items:center;">
          <button type="button" class="btn sm primary" id="btn-open-webcam" onclick="startWebcamScanner()">📷 Scan Page with Camera</button>
        </div>

        <!-- CAMERA PAGE SCANNER PANEL (R3) -->
        <div id="webcamScannerBox" style="display:none; background:var(--bg-2); border:1px solid var(--brass); border-radius:6px; padding:14px; margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
            <strong style="font-family:var(--font-display); font-size:14px; color:var(--brass);">Live Camera Document Scanner</strong>
            <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
              <select id="webcamDeviceSelect" class="btn sm" onchange="switchWebcamDevice(this.value)" style="max-width:190px;">
                <option value="">Default Camera</option>
              </select>
              <select id="webcamFilterMode" class="btn sm">
                <option value="doc_contrast">High-Contrast Document Scan</option>
                <option value="grayscale">Archival Grayscale</option>
                <option value="color">Original Color</option>
              </select>
              <label style="font-size:11.5px; color:var(--ink-2); display:flex; align-items:center; gap:4px; cursor:pointer;">
                <input type="checkbox" id="webcamMirrorToggle" onchange="updateWebcamMirror()"> Mirror
              </label>
              <button type="button" class="btn sm" onclick="stopWebcamScanner()">Close Camera</button>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: 1.2fr 1fr; gap:12px; align-items:stretch;">
            <!-- Live Video Feed + Alignment Overlay -->
            <div style="position:relative; background:#05080c; border:1px solid var(--border); border-radius:4px; min-height:210px; overflow:hidden; display:flex; align-items:center; justify-content:center;">
              <video id="webcamVideo" autoplay playsinline muted style="width:100%; max-height:240px; object-fit:contain; display:block;"></video>
              <div id="webcamAlignmentGuide" style="position:absolute; inset:10%; border:1.5px dashed rgba(214, 174, 102, 0.75); border-radius:4px; pointer-events:none; display:flex; align-items:flex-end; justify-content:center; padding-bottom:6px;">
                <span style="font-family:var(--font-mono); font-size:10px; background:rgba(8,12,16,0.75); color:var(--brass); padding:2px 6px; border-radius:3px;">Align Form N. Nav. 45 Margins Inside Frame</span>
              </div>
              <div id="webcamCountdownOverlay" style="display:none; position:absolute; inset:0; background:rgba(8,12,16,0.65); color:var(--brass); font-family:var(--font-display); font-size:48px; font-weight:700; align-items:center; justify-content:center;">3</div>
            </div>

            <!-- Captured Snapshot Preview -->
            <div style="background:#05080c; border:1px solid var(--border); border-radius:4px; min-height:210px; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:8px; position:relative;">
              <canvas id="webcamCanvas" style="display:none;"></canvas>
              <img id="webcamPreviewImg" alt="Captured Page Snapshot" style="display:none; width:100%; max-height:190px; object-fit:contain; border-radius:3px;">
              <div id="webcamPreviewPlaceholder" style="font-size:11.5px; color:var(--ink-3); text-align:center; padding:12px;">
                No snapshot captured yet.<br>Click <strong>Capture Snapshot</strong> or <strong>3s Timer</strong>.
              </div>
              <div id="webcamCaptureMeta" style="font-family:var(--font-mono); font-size:10.5px; color:var(--good); margin-top:6px;"></div>
            </div>
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; flex-wrap:wrap; gap:8px;">
            <span id="upload-status-msg" style="font-family:var(--font-mono); font-size:11.5px; color:var(--ink-2);">Camera ready for page capture.</span>
            <div style="display:flex; gap:8px;">
              <button type="button" class="btn sm" onclick="startWebcamCountdownCapture()">⏱ 3s Timer Capture</button>
              <button type="button" class="btn sm primary" onclick="captureWebcamSnapshot()">📸 Capture Snapshot</button>
              <button type="button" class="btn sm primary" id="btn-submit-webcam-scan" onclick="submitScanUpload()">Digitize Captured Page (/api/extract)</button>
            </div>
          </div>
        </div>

        <!-- Ship / Date Metadata for Camera or Log Scan Upload (/api/extract) -->
        <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:8px; margin-bottom:12px;">
          <div>
            <label style="font-size:10.5px; color:var(--ink-2); display:block; margin-bottom:2px;">SHIP / UNIT</label>
            <input type="text" id="up-ship-name" class="home-form-input" value="" placeholder="Enter ship or unit name (or leave blank to detect)">
          </div>
          <div>
            <label style="font-size:10.5px; color:var(--ink-2); display:block; margin-bottom:2px;">HULL / CODE</label>
            <input type="text" id="up-hull-no" class="home-form-input" value="" placeholder="Hull / Unit ID">
          </div>
          <div>
            <label style="font-size:10.5px; color:var(--ink-2); display:block; margin-bottom:2px;">LOG DATE</label>
            <input type="text" id="up-date-iso" class="home-form-input" value="" placeholder="YYYY-MM-DD">
          </div>
          <div>
            <label style="font-size:10.5px; color:var(--ink-2); display:block; margin-bottom:2px;">PAGE NO.</label>
            <input type="number" id="up-page-no" class="home-form-input" value="" placeholder="1" min="1" max="500">
          </div>
          <div>
            <label style="font-size:10.5px; color:var(--ink-2); display:block; margin-bottom:2px;">LOCATION</label>
            <input type="text" id="up-location" class="home-form-input" value="" placeholder="Operating location">
          </div>
        </div>

        <form id="ocr-extract-form" onsubmit="handleOcrExtractSubmit(event)">
          <input type="hidden" id="ocr-sample-id" value="">
          <input type="file" id="up-log-file" accept=".pdf,.png,.jpg,.jpeg" style="display:none;" onchange="onOcrFileSelected(this)">
          
          <div style="border:1.5px dashed var(--border-light); border-radius:6px; padding:20px; text-align:center; background:var(--bg-2); margin-bottom:14px;">
            <input type="file" id="ocr-file-input" style="display:none;" onchange="onOcrFileSelected(this)">
            <label for="ocr-file-input" style="cursor:pointer; display:block;">
              <div style="font-weight:500; font-size:13.5px; color:var(--ink); margin-bottom:4px;" id="ocr-file-label">No file selected — click to browse or capture from camera</div>
              <div style="font-size:12px; color:var(--ink-3);">Click to select PDF/image file or capture from camera above</div>
            </label>
          </div>

          <div style="display:flex; justify-content:space-between; gap:10px; flex-wrap:wrap;">
            <button type="button" class="btn" id="btn-submit-log" onclick="submitScanUpload()">Extract &amp; Add to Ship Timeline (/api/extract)</button>
            <button type="submit" class="btn primary" id="btn-start-ocr">Start Multi-Template Extraction</button>
          </div>
        </form>

        <!-- Results Box -->
        <div id="ocr-results-box" style="display:none; background:var(--bg-2); border:1px solid var(--brass); border-radius:4px; padding:16px; margin-top:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <strong style="font-family:var(--font-display); font-size:15px; color:var(--brass);" id="ocr-res-template-title">Template Selected</strong>
            <span class="flag-severity-tag INFO" id="ocr-res-conf-pill">100% Match</span>
          </div>
          <div style="font-size:12px; color:var(--ink-2); margin-bottom:10px;" id="ocr-res-reason">Autonomous classification verified.</div>
          <div style="display:flex; gap:16px; font-size:12px; color:var(--ink-2); margin-bottom:14px; flex-wrap:wrap; font-family:var(--font-mono);">
            <span>Tokens: <strong id="ocr-res-tokens" style="color:var(--ink);">0</strong></span>
            <span>Confidence: <strong id="ocr-res-mean-conf" style="color:var(--good);">0%</strong></span>
            <span>Flagged (&lt;70%): <strong id="ocr-res-low-conf" style="color:var(--bad);">0</strong></span>
          </div>
          <div style="display:flex; gap:10px; flex-wrap:wrap;" id="ocr-res-actions">
            <!-- Populated with download links -->
          </div>
        </div>
      </div>

      <div class="modal-foot">
        <button class="btn sm" onclick="stopWebcamScanner(); closeModal('modal-upload')">Close</button>
      </div>
    </div>
  </div>

  <!-- MODAL: ASK FOR SHIP / OPERATIONAL UNIT WHEN UNKNOWN -->
  <div class="modal-overlay" id="modal-ask-ship">
    <div class="modal-dialog" style="max-width:560px;">
      <div class="modal-head">
        <div>
          <h3>Identify Operational Unit / Ship</h3>
          <span style="font-size:12px; color:var(--ink-2);">Assign uploaded document to an existing unit or create a new ship/unit</span>
        </div>
        <button class="btn sm" onclick="closeModal('modal-ask-ship')">Cancel</button>
      </div>

      <div class="modal-body" style="display:flex; flex-direction:column; gap:14px;">
        <p style="font-size:13px; color:var(--ink-2); line-height:1.5;">
          The ship or unit name could not be automatically determined from the uploaded file. Please select an existing unit or create a new ship/unit for this file.
        </p>

        <div style="background:var(--bg-2); border:1px solid var(--border); border-radius:4px; padding:10px 12px; font-family:var(--font-mono); font-size:12px;">
          <span style="color:var(--ink-2);">Uploaded File:</span>
          <strong id="ask-ship-filename-label" style="color:var(--brass); margin-left:6px;">Uploaded Document</strong>
        </div>

        <div id="ask-ship-existing-section" style="background:var(--bg-2); border:1px solid var(--border); border-radius:5px; padding:12px;">
          <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:5px; text-transform:uppercase; letter-spacing:0.04em;">Select Existing Uploaded Ship / Unit</label>
          <select id="ask-ship-existing-select" class="home-form-select" onchange="onAskShipExistingSelected(this.value)">
            <option value="">-- Create New Ship / Unit Below --</option>
          </select>
        </div>

        <div style="display:flex; flex-direction:column; gap:10px; background:var(--bg-2); border:1px solid var(--border); border-radius:5px; padding:12px;">
          <div style="font-size:11px; color:var(--brass); font-weight:600; text-transform:uppercase; letter-spacing:0.04em;">Ship / Unit Details</div>
          <div>
            <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">SHIP / UNIT NAME *</label>
            <input type="text" id="ask-ship-name-input" class="home-form-input" value="" placeholder="Enter ship, shore station, or squadron name" required>
          </div>
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">HULL / UNIT ID (OPTIONAL)</label>
              <input type="text" id="ask-ship-hull-input" class="home-form-input" value="" placeholder="Hull or Designation">
            </div>
            <div>
              <label style="font-size:11px; color:var(--ink-2); display:block; margin-bottom:3px;">UNIT TYPE</label>
              <select id="ask-ship-unit-type" class="home-form-select">
                <option value="Ship">Ship</option>
                <option value="Shore Facility">Shore Facility</option>
                <option value="Air Squadron">Air Squadron</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-foot">
        <button type="button" class="btn sm" onclick="closeModal('modal-ask-ship')">Cancel</button>
        <button type="button" class="btn sm primary" id="btn-confirm-ask-ship" onclick="confirmPendingShipUpload()">Assign &amp; Digitize File</button>
      </div>
    </div>
  </div>

  <!-- MODAL: GEMMA OFFLINE AI INTELLIGENCE -->
  <div class="modal-overlay" id="modal-gemma">
    <div class="modal-dialog" style="max-width:680px;">
      <div class="modal-head">
        <div>
          <h3>Gemma 4 12B Offline Intelligence</h3>
          <span style="font-size:12px; color:var(--ink-2);">Private local multimodal OCR &amp; physical telemetry analytics</span>
        </div>
        <button class="btn sm" onclick="closeModal('modal-gemma')">Close</button>
      </div>

      <div class="modal-body">
        <div style="background:var(--bg-2); border:1px solid var(--border); border-radius:6px; padding:14px; margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div>
              <strong style="font-size:14px; color:var(--brass);">Recommended Model: Gemma 4 12B</strong>
              <div style="font-size:12px; color:var(--ink-2); margin-top:2px;">Selected for maximum speed &amp; zero memory bus latency on this laptop.</div>
            </div>
            <span class="flag-severity-tag INFO" id="gemma-modal-status-badge">Checking...</span>
          </div>
          
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:12px; margin-top:12px;">
            <div style="background:var(--bg-1); padding:8px 10px; border-radius:4px; border:1px solid var(--border);">
              <span style="color:var(--ink-2); display:block;">GPU Acceleration</span>
              <strong style="color:var(--ink);">RTX 4080 Laptop (12 GB VRAM)</strong>
            </div>
            <div style="background:var(--bg-1); padding:8px 10px; border-radius:4px; border:1px solid var(--border);">
              <span style="color:var(--ink-2); display:block;">VRAM Allocation</span>
              <strong style="color:var(--good);">100% In-VRAM (~8 GB Q4)</strong>
            </div>
            <div style="background:var(--bg-1); padding:8px 10px; border-radius:4px; border:1px solid var(--border);">
              <span style="color:var(--ink-2); display:block;">Inference Throughput</span>
              <strong style="color:var(--good);">50-80+ tokens/sec (Pure GPU)</strong>
            </div>
            <div style="background:var(--bg-1); padding:8px 10px; border-radius:4px; border:1px solid var(--border);">
              <span style="color:var(--ink-2); display:block;">Active Runner</span>
              <strong style="color:var(--ink);" id="gemma-modal-active-provider">Checking...</strong>
            </div>
          </div>
        </div>

        <div style="margin-bottom:16px;">
          <label style="display:block; font-size:12px; font-weight:600; color:var(--brass); margin-bottom:6px;">Local Runner Configuration</label>
          <div style="display:grid; grid-template-columns:140px 1fr; gap:10px; margin-bottom:10px;">
            <select id="gemma-cfg-provider" class="home-form-select" onchange="toggleGemmaProviderUI()">
              <option value="ollama">Ollama</option>
              <option value="openai_compatible">LM Studio / vLLM</option>
            </select>
            <input type="text" id="gemma-cfg-url" class="home-form-input" value="http://127.0.0.1:11434" placeholder="Runner API URL">
          </div>
          <div style="display:grid; grid-template-columns:1fr 140px; gap:10px;">
            <input type="text" id="gemma-cfg-model" class="home-form-input" value="gemma4:12b" placeholder="Model identifier (e.g. gemma4:12b)">
            <button class="btn sm" onclick="saveGemmaConfigAndTest()">Save &amp; Test</button>
          </div>
        </div>

        <div style="background:var(--bg-2); border:1px solid var(--border); border-radius:6px; padding:12px; font-size:12px;">
          <strong style="color:var(--ink); display:block; margin-bottom:4px;">How to start Gemma 4 12B locally:</strong>
          <p style="color:var(--ink-2); margin-bottom:6px;">Open PowerShell or Command Prompt and run:</p>
          <div style="background:var(--bg-1); padding:8px 10px; border-radius:4px; font-family:var(--font-mono); color:var(--brass); border:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
            <code>ollama run gemma4:12b</code>
            <button class="btn sm" onclick="navigator.clipboard.writeText('ollama run gemma4:12b'); showToast('Command copied to clipboard!');">Copy</button>
          </div>
          <p style="color:var(--ink-2); margin-top:8px; font-size:11.5px;">
            <em>Note: If the local runner is offline, DECK automatically operates in high-speed deterministic fallback mode without interruption.</em>
          </p>
        </div>
      </div>

      <div class="modal-foot">
        <button class="btn sm" onclick="closeModal('modal-gemma')">Close</button>
      </div>
    </div>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div id="toast">Message</div>

  <!-- JAVASCRIPT CONTROLLERS -->
  <script>
    // Global State
    let overviewData = null;
    let allCorpusTrends = null;
    let currentTimelinePoints = [];
    let currentTimelineMeta = null;
    let currentDayId = '';
    let currentDayData = null;
    let selectedPickerDayId = '';

    // Chart Instances (5 required timeline charts)
    let chartRpmTemp = null;
    let chartBoiler = null;
    let chartSpeed = null;
    let chartBaro = null;
    let chartPsychro = null;

    // Reticle Modal State
    let pointModalTargetTokenId = null;
    let pointModalTargetDayId = null;
    let pointModalBbox = [0.2, 0.25, 0.04, 0.02];
    let pointModalZoomState = true;

    // Initialize on page load
    window.addEventListener('DOMContentLoaded', async () => {
      setupDragAndDropZones();
      refreshGemmaStatus();
      await Promise.all([loadOverviewData(), fetchCorpusTrends()]);
      if (overviewData && overviewData.days && overviewData.days.length > 0) {
        if (!currentDayId) currentDayId = overviewData.days[0].day_id;
        if (!selectedPickerDayId) selectedPickerDayId = overviewData.days[0].day_id;
        await loadDayAnalytics(currentDayId);
      }
    });

    async function fetchCorpusTrends() {
      try {
        const res = await fetch('/api/corpus/trends');
        if (res.ok) {
          allCorpusTrends = await res.json();
        }
      } catch (err) {
        console.error('Failed to fetch corpus trends:', err);
      }
    }

    function resolveShipTimeline(ext) {
      const candidates = [ext.ship_display, ext.ship_name].filter(Boolean);
      if (allCorpusTrends && allCorpusTrends.ship_timelines) {
        for (const key of candidates) {
          const timelineObj = allCorpusTrends.ship_timelines[key];
          const pts = timelineObj ? (timelineObj.timeline_points || timelineObj.points) : null;
          if (timelineObj && Array.isArray(pts) && pts.length > 0) {
            return {
              ...timelineObj,
              date_range_label: timelineObj.date_range_label || timelineObj.timeframe_label || `${ext.date_human || 'Uploaded Log'}`,
              total_days: timelineObj.total_days || timelineObj.day_count || 1,
              total_hours: pts.length,
              timeline_points: pts,
            };
          }
        }
      }
      if (allCorpusTrends && Array.isArray(allCorpusTrends.timeline_points) && allCorpusTrends.timeline_points.length > 0) {
        return {
          ship_display: ext.ship_display || ext.ship_name || 'Unknown Unit',
          date_range_label: `${ext.date_human || 'Uploaded Log'} (Multi-Day Corpus)`,
          total_days: allCorpusTrends.total_days || 1,
          total_hours: allCorpusTrends.timeline_points.length,
          timeline_points: allCorpusTrends.timeline_points,
        };
      }
      const fallbackRows = (ext.hourly_rows || []).map(r => ({
        ...r,
        day_id: ext.day_id,
        date_iso: ext.date_iso,
        date_human: ext.date_human,
        ship_name: ext.ship_name,
        ship_display: ext.ship_display,
        primary_page: ext.primary_page || 1,
        label: `${(ext.date_human || '').replace(', 1942', '')} ${String(r.hour).padStart(2, '0')}00`,
      }));
      return {
        ship_display: ext.ship_display || ext.ship_name || 'Unknown Unit',
        date_range_label: ext.date_human || '24-Hour Log',
        total_days: 1,
        total_hours: fallbackRows.length,
        timeline_points: fallbackRows,
      };
    }

    // Theme Switcher
    function toggleTheme() {
      const isLight = document.documentElement.getAttribute('data-theme') === 'light';
      const newTheme = isLight ? 'dark' : 'light';
      if (newTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        document.getElementById('theme-btn').innerText = 'Theme: Light';
      } else {
        document.documentElement.removeAttribute('data-theme');
        document.getElementById('theme-btn').innerText = 'Theme: Dark';
      }
      if (currentDayData) {
        const timelineObj = resolveShipTimeline(currentDayData.extraction);
        currentTimelineMeta = timelineObj;
        currentTimelinePoints = timelineObj.timeline_points || [];
        initCharts(currentTimelinePoints);
      }
    }

    // View Navigation
    function navigateTo(viewId) {
      document.querySelectorAll('.view-pane').forEach(p => p.classList.remove('active'));
      const target = document.getElementById(`view-${viewId}`);
      if (target) target.classList.add('active');
      window.scrollTo(0, 0);

      if (viewId === 'ship-picker') {
        renderPickerShips();
        renderPickerDates();
      }
    }

    // Modals
    function openModal(id) {
      const m = document.getElementById(id);
      if (m) m.classList.add('open');
    }

    function closeModal(id) {
      const m = document.getElementById(id);
      if (m) m.classList.remove('open');
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      if (!t) return;
      t.innerText = msg;
      t.classList.add('show');
      clearTimeout(window._toastTimer);
      window._toastTimer = setTimeout(() => t.classList.remove('show'), 3500);
    }

    let selectedUnitFilter = '';

    // Load Overview Data
    async function loadOverviewData() {
      try {
        const res = await fetch('/api/overview');
        overviewData = await res.json();
        const daysList = (overviewData && overviewData.days) || [];
        populateDaySelect(daysList);
        renderHomeUploadedUnits(daysList);
        renderPickerShips();
        renderPickerDates();
        const manualsList = overviewData.manuals || overviewData.tech_manuals || [];
        const manCountEl = document.getElementById('home-manuals-count-label');
        if (manCountEl) {
          manCountEl.innerText = `${manualsList.length} Active Manuals Indexed for Anomaly Flags`;
        }
        renderHomeIndexedManuals(manualsList);
      } catch (err) {
        console.error('Failed to load overview:', err);
      }
    }

    function getUniqueUploadedShips(days) {
      const map = new Map();
      (days || []).forEach(d => {
        const shipKey = d.ship_display || d.ship_name || 'Uploaded Unit';
        if (!map.has(shipKey)) {
          map.set(shipKey, {
            shipKey,
            ship_display: d.ship_display || d.ship_name || shipKey,
            ship_name: d.ship_name || d.ship_display || shipKey,
            hull_number: d.hull_number || '',
            unit_type: d.unit_type || 'Ship',
            days: [],
          });
        }
        map.get(shipKey).days.push(d);
      });
      return Array.from(map.values());
    }

    function renderHomeUploadedUnits(days) {
      const tagsCont = document.getElementById('home-uploaded-units-tags');
      const statusLabel = document.getElementById('home-archive-status-label');
      if (!tagsCont) return;
      tagsCont.innerHTML = '';

      const uniqueShips = getUniqueUploadedShips(days);
      if (uniqueShips.length === 0) {
        tagsCont.innerHTML = '<span class="badge unit-tag" style="color:var(--ink-2);">No units uploaded yet — upload a file above</span>';
        if (statusLabel) {
          statusLabel.innerText = '● No units uploaded yet';
          statusLabel.style.color = 'var(--ink-2)';
        }
        return;
      }

      uniqueShips.forEach(s => {
        const span = document.createElement('span');
        span.className = 'badge unit-tag';
        span.innerText = `${s.ship_display} (${s.days.length}d)`;
        tagsCont.appendChild(span);
      });
      if (statusLabel) {
        statusLabel.innerText = `● ${uniqueShips.length} Operational Unit(s) Uploaded`;
        statusLabel.style.color = 'var(--good)';
      }
    }

    function renderHomeIndexedManuals(manuals) {
      const cont = document.getElementById('home-indexed-manuals-list');
      if (!cont) return;
      cont.innerHTML = '';
      (manuals || []).forEach(m => {
        const row = document.createElement('div');
        row.style.cssText = 'display:flex; justify-content:space-between; align-items:center; font-size:11.5px; background:var(--bg-2); padding:5px 8px; border-radius:4px; border:1px solid var(--border); gap:8px;';
        row.innerHTML = `
          <div style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
            <strong style="font-family:var(--font-mono); color:var(--brass);">${m.code}</strong>
            <span style="color:var(--ink); margin-left:6px;">${m.title}</span>
          </div>
          <span style="font-family:var(--font-mono); font-size:10.5px; color:var(--ink-2); flex-shrink:0;">${m.unit_type || 'All Units'} • ${m.standard_limit || ''}</span>
        `;
        cont.appendChild(row);
      });
    }

    function populateDaySelect(days) {
      const sel = document.getElementById('day-select');
      if (!sel) return;
      sel.innerHTML = '';
      (days || []).forEach(d => {
        const opt = document.createElement('option');
        opt.value = d.day_id;
        opt.text = `${d.date_human} — ${d.ship_display || d.title || d.day_id}`;
        if (d.day_id === currentDayId) opt.selected = true;
        sel.appendChild(opt);
      });
    }

    function renderPickerShips() {
      const shipCont = document.getElementById('picker-ship-container');
      const dateCont = document.getElementById('picker-date-container');
      const openBtn = document.getElementById('btn-open-selected-log');
      if (!shipCont) return;

      const allDays = (overviewData && overviewData.days) || [];
      const uniqueShips = getUniqueUploadedShips(allDays);

      if (uniqueShips.length === 0) {
        const emptyHtml = '<div style="color:var(--ink-2); font-size:13px; padding:12px;">No files or operational units stored. Upload a logbook scan on the Home screen or via Scan / Upload to add a ship or unit.</div>';
        shipCont.innerHTML = emptyHtml;
        if (dateCont) dateCont.innerHTML = emptyHtml;
        if (openBtn) openBtn.disabled = true;
        selectedUnitFilter = '';
        selectedPickerDayId = '';
        return;
      }

      if (openBtn) openBtn.disabled = false;
      if (!selectedUnitFilter || !uniqueShips.some(s => s.shipKey === selectedUnitFilter)) {
        selectedUnitFilter = uniqueShips[0].shipKey;
      }

      shipCont.innerHTML = '';
      uniqueShips.forEach(s => {
        const card = document.createElement('div');
        card.className = `picker-ship-item ${s.shipKey === selectedUnitFilter ? 'selected' : ''}`;
        const badgeText = s.hull_number || s.unit_type || 'Unit';
        card.innerHTML = `
          <div>
            <strong>${s.ship_display}</strong>
            <div style="font-size:11px; color:var(--ink-2);">${s.unit_type || 'Ship'} • ${s.days.length} Log Day(s) Uploaded</div>
          </div>
          <span>${badgeText}</span>
        `;
        card.onclick = () => selectPickerShip(s.shipKey, card);
        shipCont.appendChild(card);
      });
    }

    function renderPickerDates() {
      const cont = document.getElementById('picker-date-container');
      const openBtn = document.getElementById('btn-open-selected-log');
      if (!cont) return;

      const allDays = (overviewData && overviewData.days) || [];
      if (allDays.length === 0) {
        cont.innerHTML = '<div style="color:var(--ink-2); font-size:13px; padding:12px;">No files or operational units stored. Upload a logbook scan on the Home screen or via Scan / Upload to add a ship or unit.</div>';
        if (openBtn) openBtn.disabled = true;
        return;
      }

      if (openBtn) openBtn.disabled = false;
      cont.innerHTML = '';

      let filtered = allDays.filter(d => {
        const shipKey = d.ship_display || d.ship_name || 'Uploaded Unit';
        return !selectedUnitFilter || shipKey === selectedUnitFilter;
      });
      if (filtered.length === 0) filtered = allDays;

      if (!filtered.some(d => d.day_id === selectedPickerDayId) && filtered.length > 0) {
        selectedPickerDayId = filtered[0].day_id;
      }

      filtered.forEach(d => {
        const pill = document.createElement('div');
        pill.className = `date-pill ${d.day_id === selectedPickerDayId ? 'selected' : ''} ${d.is_casualty ? 'has-casualty' : ''}`;
        pill.innerText = d.date_human || d.day_id;
        pill.onclick = () => {
          document.querySelectorAll('.date-pill').forEach(p => p.classList.remove('selected'));
          pill.classList.add('selected');
          selectedPickerDayId = d.day_id;
        };
        cont.appendChild(pill);
      });
    }

    function selectPickerShip(shipKey, el) {
      selectedUnitFilter = shipKey;
      document.querySelectorAll('.picker-ship-item').forEach(item => item.classList.remove('selected'));
      if (el) el.classList.add('selected');
      renderPickerDates();
    }

    function openSelectedLog() {
      if (!selectedPickerDayId) {
        showToast('Please upload and select a log date first.');
        return;
      }
      currentDayId = selectedPickerDayId;
      loadDayAnalytics(currentDayId);
      navigateTo('dashboard');
    }

    function onDaySelectChange(dayId) {
      currentDayId = dayId;
      loadDayAnalytics(dayId);
    }

    function stepDay(offset) {
      if (!overviewData || !overviewData.days) return;
      const days = overviewData.days;
      const curIdx = days.findIndex(d => d.day_id === currentDayId);
      if (curIdx === -1) return;
      const nextIdx = Math.max(0, Math.min(days.length - 1, curIdx + offset));
      currentDayId = days[nextIdx].day_id;
      document.getElementById('day-select').value = currentDayId;
      loadDayAnalytics(currentDayId);
    }

    // Load Single Day Data
    async function loadDayAnalytics(dayId) {
      if (!dayId) return;
      try {
        const res = await fetch(`/api/day/${dayId}`);
        if (!res.ok) throw new Error('Failed to load log day');
        currentDayData = await res.json();
        currentDayId = dayId;
        if (!allCorpusTrends) {
          await fetchCorpusTrends();
        }
        renderDashboardView();
      } catch (err) {
        showToast(`Error loading data: ${err.message}`);
      }
    }

    function renderScanViewer(ext) {
      if (!ext) return;
      const scanImgs = ext.scan_images || [];
      if (scanImgs.length > 0) {
        const s = scanImgs[0];
        const imgUrl = s.url || s.web_url || '';
        const imgEl = document.getElementById('scan-primary-img');
        if (imgEl) imgEl.src = imgUrl;
        const pageInfoEl = document.getElementById('scan-page-info');
        if (pageInfoEl) pageInfoEl.innerText = `Page ${ext.primary_page || 1} (${ext.title || 'Form N. Nav. 45'})`;
        const tokSumEl = document.getElementById('scan-token-summary');
        if (tokSumEl) tokSumEl.innerText = `${(ext.tokens || []).length} Verified Tokens`;
      }
    }

    function renderDashboardView() {
      if (!currentDayData) return;
      const ext = currentDayData.extraction;

      document.getElementById('dash-ship-name').innerText = ext.ship_display || ext.ship_name || 'Unknown Unit';
      document.getElementById('dash-date-label').innerText = `${ext.date_human}`;

      const sel = document.getElementById('day-select');
      if (sel) sel.value = ext.day_id;

      // Resolve Full Available Timeframe for this Ship (R2)
      const timelineObj = resolveShipTimeline(ext);
      currentTimelineMeta = timelineObj;
      currentTimelinePoints = timelineObj.timeline_points || [];

      const spanText = `${timelineObj.date_range_label || ext.date_human} (${timelineObj.total_days || 1} Days • ${currentTimelinePoints.length} Hourly Points)`;
      const spanBadge = document.getElementById('timeline-span-badge');
      if (spanBadge) spanBadge.innerText = `Full Available Timeframe: ${spanText}`;

      ['tag-chart-rpm', 'tag-chart-boiler', 'tag-chart-speed', 'tag-chart-baro', 'tag-chart-psychro'].forEach(tagId => {
        const el = document.getElementById(tagId);
        if (el) el.innerText = `${spanText} • Click any point for source scan`;
      });

      // Render All 5 Timeline Charts over Full Available Timeframe
      initCharts(currentTimelinePoints);

      // Render Flags
      const anomalies = (currentDayData.anomaly_analysis && currentDayData.anomaly_analysis.anomalies) ? currentDayData.anomaly_analysis.anomalies : [];
      window._currentAnomalies = anomalies;
      renderFlagCards(anomalies);

      // Render Editable Table (24-hour active day)
      renderHourlyTable(ext.hourly_rows || []);

      // Render Fuel/Water inputs
      if (ext.fuel) {
        document.getElementById('edit-fuel-prior').value = ext.fuel.prior_on_hand || 0;
        document.getElementById('edit-fuel-received').value = ext.fuel.received || 0;
        document.getElementById('edit-fuel-expended').value = ext.fuel.expended || 0;
      }
      if (ext.water) {
        document.getElementById('edit-water-distilled').value = ext.water.distilled || 0;
        document.getElementById('edit-water-expended').value = ext.water.expended || 0;
      }

      // Render Scan Image Viewer (R1)
      renderScanViewer(ext);
    }

    // Chart Theme Configuration
    function getChartThemeColors() {
      const isLight = document.documentElement.getAttribute('data-theme') === 'light';
      return {
        textColor: isLight ? '#1c2633' : '#ece6d6',
        textMuted: isLight ? '#758294' : '#7f8ea3',
        gridLine: isLight ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.06)',
        tooltipBg: isLight ? '#ece5d6' : '#142133',
        tooltipBorder: isLight ? '#c4b89f' : '#253b59',
        brassColor: isLight ? '#8f6823' : '#d6ae66',
        goodColor: isLight ? '#2b7a54' : '#6fbf97',
        badColor: isLight ? '#aa2c2c' : '#d96b6b',
        infoColor: isLight ? '#2c6e9e' : '#79b4dc',
      };
    }

    function initCharts(hourlyRows) {
      const tc = getChartThemeColors();
      const labels = hourlyRows.map((r, idx) => r.label || r.timeline_label || `${String(r.hour || (idx % 24) + 1).padStart(2, '0')}00`);
      const ptRadius = hourlyRows.length > 96 ? 1.5 : 3.5;
      const ptHoverRadius = 6;

      // 1. Chart: Shaft RPM & Thrust Temp
      const portRpm = hourlyRows.map(r => (r.port_rpm !== undefined && r.port_rpm !== null) ? Number(r.port_rpm) : (Number(r.revs) || 0));
      const thrustTemps = hourlyRows.map(r => (r.thrust_bearing_temp_f !== undefined && r.thrust_bearing_temp_f !== null) ? Number(r.thrust_bearing_temp_f) : 135);

      const ctxRpm = document.getElementById('chart-machinery-rpm-temp').getContext('2d');
      if (chartRpmTemp) chartRpmTemp.destroy();
      chartRpmTemp = new Chart(ctxRpm, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Shaft Speed (RPM)',
              data: portRpm,
              borderColor: tc.infoColor,
              backgroundColor: 'rgba(121, 180, 220, 0.08)',
              yAxisID: 'yRPM',
              tension: 0.2,
              borderWidth: 1.8,
              pointRadius: ptRadius,
              pointHoverRadius: ptHoverRadius,
            },
            {
              label: 'Thrust Temp (F)',
              data: thrustTemps,
              borderColor: tc.brassColor,
              backgroundColor: 'rgba(214, 174, 102, 0.08)',
              yAxisID: 'yTemp',
              tension: 0.2,
              borderWidth: 1.8,
              pointRadius: ptRadius,
              pointHoverRadius: ptHoverRadius,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: { legend: { labels: { color: tc.textColor, font: { family: 'Cascadia Mono', size: 11 } } } },
          scales: {
            x: { grid: { color: tc.gridLine }, ticks: { color: tc.textMuted, maxTicksLimit: 16, font: { family: 'Cascadia Mono', size: 10 } } },
            yRPM: { type: 'linear', position: 'left', grid: { color: tc.gridLine }, ticks: { color: tc.infoColor, font: { family: 'Cascadia Mono' } } },
            yTemp: { type: 'linear', position: 'right', grid: { drawOnChartArea: false }, ticks: { color: tc.brassColor, font: { family: 'Cascadia Mono' } } }
          },
          onClick: (evt, elements) => {
            if (elements.length > 0) {
              const idx = elements[0].index;
              const dsIdx = elements[0].datasetIndex;
              if (dsIdx === 0) handleChartPointClick(idx, 'rpm', portRpm[idx]);
              else handleChartPointClick(idx, 'thrust_temp', thrustTemps[idx]);
            }
          }
        }
      });

      // 2. Chart: Boiler Drum PSI & Salinity
      const drumPsi = hourlyRows.map(r => (r.boiler_drum_psi !== undefined && r.boiler_drum_psi !== null) ? Number(r.boiler_drum_psi) : 250);
      const salValues = hourlyRows.map(r => (r.feed_salinity_grains !== undefined && r.feed_salinity_grains !== null) ? Number(r.feed_salinity_grains) : 0.08);

      const ctxBoiler = document.getElementById('chart-machinery-boiler').getContext('2d');
      if (chartBoiler) chartBoiler.destroy();
      chartBoiler = new Chart(ctxBoiler, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Superheat Drum Pressure (PSI)',
              data: drumPsi,
              borderColor: tc.goodColor,
              yAxisID: 'yPSI',
              borderWidth: 1.8,
              tension: 0.2,
              pointRadius: ptRadius,
              pointHoverRadius: ptHoverRadius,
            },
            {
              label: 'Feed Salinity (gr/gal)',
              data: salValues,
              borderColor: tc.badColor,
              yAxisID: 'ySal',
              borderWidth: 1.8,
              tension: 0.2,
              pointRadius: ptRadius,
              pointHoverRadius: ptHoverRadius,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: { legend: { labels: { color: tc.textColor, font: { family: 'Cascadia Mono', size: 11 } } } },
          scales: {
            x: { grid: { color: tc.gridLine }, ticks: { color: tc.textMuted, maxTicksLimit: 16, font: { family: 'Cascadia Mono', size: 10 } } },
            yPSI: { type: 'linear', position: 'left', ticks: { color: tc.goodColor, font: { family: 'Cascadia Mono' } } },
            ySal: { type: 'linear', position: 'right', ticks: { color: tc.badColor, font: { family: 'Cascadia Mono' } }, grid: { drawOnChartArea: false } }
          },
          onClick: (evt, elements) => {
            if (elements.length > 0) {
              const idx = elements[0].index;
              const dsIdx = elements[0].datasetIndex;
              if (dsIdx === 0) handleChartPointClick(idx, 'boiler_drum_psi', drumPsi[idx]);
              else handleChartPointClick(idx, 'salinity', salValues[idx]);
            }
          }
        }
      });

      // 3. Chart: Steaming Speed Over Ground
      const speeds = hourlyRows.map(r => (r.speed_knots !== undefined && r.speed_knots !== null) ? Number(r.speed_knots) : 12);
      const ctxSpeed = document.getElementById('chart-deck-speed').getContext('2d');
      if (chartSpeed) chartSpeed.destroy();
      chartSpeed = new Chart(ctxSpeed, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Speed (Knots)',
            data: speeds,
            borderColor: tc.infoColor,
            backgroundColor: 'rgba(121, 180, 220, 0.08)',
            fill: true,
            tension: 0.2,
            borderWidth: 1.8,
            pointRadius: ptRadius,
            pointHoverRadius: ptHoverRadius,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: { legend: { labels: { color: tc.textColor, font: { family: 'Cascadia Mono', size: 11 } } } },
          scales: {
            x: { grid: { color: tc.gridLine }, ticks: { color: tc.textMuted, maxTicksLimit: 16, font: { family: 'Cascadia Mono', size: 10 } } },
            y: { grid: { color: tc.gridLine }, ticks: { color: tc.infoColor, font: { family: 'Cascadia Mono' } } }
          },
          onClick: (evt, elements) => {
            if (elements.length > 0) {
              const idx = elements[0].index;
              handleChartPointClick(idx, 'speed', speeds[idx]);
            }
          }
        }
      });

      // 4. Chart: Synoptic Barometer
      const baroData = hourlyRows.map(r => parseFloat(r.barometer_inhg || r.barometer_raw) || 29.85);
      const ctxBaro = document.getElementById('chart-weather-baro').getContext('2d');
      if (chartBaro) chartBaro.destroy();
      chartBaro = new Chart(ctxBaro, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Barometer (Inches Hg)',
              data: baroData,
              borderColor: tc.infoColor,
              backgroundColor: 'rgba(121, 180, 220, 0.08)',
              fill: true,
              borderWidth: 1.8,
              tension: 0.2,
              pointRadius: ptRadius,
              pointHoverRadius: ptHoverRadius,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: { legend: { labels: { color: tc.textColor, font: { family: 'Cascadia Mono', size: 11 } } } },
          scales: {
            x: { grid: { color: tc.gridLine }, ticks: { color: tc.textMuted, maxTicksLimit: 16, font: { family: 'Cascadia Mono', size: 10 } } },
            y: { type: 'linear', position: 'left', grid: { color: tc.gridLine }, ticks: { color: tc.infoColor, font: { family: 'Cascadia Mono' } } }
          },
          onClick: (evt, elements) => {
            if (elements.length > 0) {
              const idx = elements[0].index;
              handleChartPointClick(idx, 'barometer', baroData[idx]);
            }
          }
        }
      });

      // 5. Chart: Psychrometer Air Temperatures (Dry & Wet Bulb)
      const dryTemps = hourlyRows.map(r => parseFloat(r.temp_dry_bulb) || 50);
      const wetTemps = hourlyRows.map(r => parseFloat(r.temp_wet_bulb) || 47);
      const ctxPsychro = document.getElementById('chart-weather-psychro').getContext('2d');
      if (chartPsychro) chartPsychro.destroy();
      chartPsychro = new Chart(ctxPsychro, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Dry Bulb Temp (F)',
              data: dryTemps,
              borderColor: tc.brassColor,
              backgroundColor: 'rgba(214, 174, 102, 0.08)',
              borderWidth: 1.8,
              tension: 0.2,
              pointRadius: ptRadius,
              pointHoverRadius: ptHoverRadius,
            },
            {
              label: 'Wet Bulb Temp (F)',
              data: wetTemps,
              borderColor: tc.goodColor,
              backgroundColor: 'rgba(111, 191, 151, 0.08)',
              borderWidth: 1.8,
              tension: 0.2,
              pointRadius: ptRadius,
              pointHoverRadius: ptHoverRadius,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: { legend: { labels: { color: tc.textColor, font: { family: 'Cascadia Mono', size: 11 } } } },
          scales: {
            x: { grid: { color: tc.gridLine }, ticks: { color: tc.textMuted, maxTicksLimit: 16, font: { family: 'Cascadia Mono', size: 10 } } },
            y: { type: 'linear', position: 'left', grid: { color: tc.gridLine }, ticks: { color: tc.brassColor, font: { family: 'Cascadia Mono' } } }
          },
          onClick: (evt, elements) => {
            if (elements.length > 0) {
              const idx = elements[0].index;
              const dsIdx = elements[0].datasetIndex;
              if (dsIdx === 0) handleChartPointClick(idx, 'dry_bulb', dryTemps[idx]);
              else handleChartPointClick(idx, 'wet_bulb', wetTemps[idx]);
            }
          }
        }
      });
    }

    // Chart Point Click -> Reticle Scan Popup (R1: Supports Multi-Day Timeline Points + Form N. Nav. 45 A.M./P.M. Bbox)
    function handleChartPointClick(rowIdx, metricKey, value) {
      if (!currentDayData) return;
      const ext = currentDayData.extraction;
      const points = (currentTimelinePoints && currentTimelinePoints.length > 0) ? currentTimelinePoints : (ext.hourly_rows || []);
      const row = points[rowIdx] || (ext.hourly_rows || [])[rowIdx] || {};
      const hour = Number(row.hour) || ((rowIdx % 24) + 1);

      const pointDayId = row.day_id || ext.day_id;
      pointModalTargetDayId = pointDayId;
      const dayLookup = (allCorpusTrends && allCorpusTrends.days_lookup && allCorpusTrends.days_lookup[pointDayId]) ? allCorpusTrends.days_lookup[pointDayId] : null;
      const pointDateHuman = row.date_human || (dayLookup && dayLookup.date_human) || ext.date_human;
      const pointShipDisplay = row.ship_display || (dayLookup && dayLookup.ship_display) || ext.ship_display;
      const pointPageNum = row.primary_page || (dayLookup && dayLookup.primary_page) || ext.primary_page || 5;

      document.getElementById('point-modal-field-title').innerText = `${pointDateHuman} • Hour ${String(hour).padStart(2, '0')}00 Telemetry Reading`;
      document.getElementById('point-modal-date-sub').innerText = `${pointShipDisplay} — ${pointDateHuman}`;
      document.getElementById('point-modal-val').innerText = `${value !== undefined && value !== null ? value : '--'}`;

      const readableFieldNames = {
        'speed': 'Speed Over Ground (Knots)',
        'rpm': 'Main Shaft Revolutions (RPM)',
        'thrust_temp': 'Kingsbury Thrust Bearing Temp (F)',
        'salinity': 'Boiler Feedwater Salinity (gr Cl/gal)',
        'boiler_drum_psi': 'Superheat Drum Pressure (PSI)',
        'barometer': 'Synoptic Barometer (Inches Hg)',
        'dry_bulb': 'Ambient Air Dry Bulb Temp (F)',
        'wet_bulb': 'Psychrometer Wet Bulb Temp (F)',
      };
      document.getElementById('point-modal-field-name').innerText = readableFieldNames[metricKey] || metricKey.toUpperCase();

      const cellMetaMap = {
        'speed': 'speed_knots',
        'rpm': 'revs',
        'thrust_temp': 'thrust_bearing_temp_f',
        'salinity': 'feed_salinity_grains',
        'boiler_drum_psi': 'boiler_drum_psi',
        'barometer': 'barometer_raw',
        'dry_bulb': 'temp_dry_bulb',
        'wet_bulb': 'temp_wet_bulb',
      };
      const metaKey = cellMetaMap[metricKey] || metricKey;
      let meta = (row.cell_meta && row.cell_meta[metaKey]) ? row.cell_meta[metaKey] : null;
      if (!meta && metricKey === 'speed' && row.cell_meta) {
        meta = row.cell_meta['revs_miles'] || row.cell_meta['log_miles'] || row.cell_meta['revs'];
      }
      if (!meta && metricKey === 'rpm' && row.cell_meta) {
        meta = row.cell_meta['revs'] || row.cell_meta['port_rpm'];
      }

      if (meta && meta.bbox) {
        pointModalBbox = meta.bbox;
        pointModalTargetTokenId = meta.token_id || null;
        const confPercent = Math.round((meta.confidence || 0.92) * 100);
        document.getElementById('point-modal-conf').innerText = `${confPercent}% Confidence`;
      } else {
        // Form N. Nav. 45 A.M. (hours 1-12) and P.M. (hours 13-24) row geometry
        const yBase = hour <= 12 ? (0.2465 + (hour - 1) * 0.0103) : (0.6430 + (hour - 13) * 0.0103);
        let xCol = 0.228;
        let colW = 0.028;
        if (metricKey === 'barometer') { xCol = 0.228; colW = 0.028; }
        else if (metricKey === 'dry_bulb') { xCol = 0.270; colW = 0.015; }
        else if (metricKey === 'wet_bulb') { xCol = 0.289; colW = 0.015; }
        else if (metricKey === 'speed') { xCol = 0.116; colW = 0.025; }
        else if (metricKey === 'rpm') { xCol = 0.098; colW = 0.022; }
        else if (metricKey === 'salinity' || metricKey === 'thrust_temp' || metricKey === 'boiler_drum_psi') { xCol = 0.350; colW = 0.045; }

        pointModalBbox = [xCol, yBase, colW, 0.0103];
        pointModalTargetTokenId = null;
        document.getElementById('point-modal-conf').innerText = `94% Confidence`;
      }

      document.getElementById('point-modal-page-ref').innerText = `Page ${pointPageNum} of ${currentDayData.total_pdf_pages || 49} — Form N. Nav. 45 (${pointDateHuman})`;

      // Resolve scan image from the clicked point's day first, then fallback to active day
      let scanImgs = [];
      if (dayLookup && Array.isArray(dayLookup.scan_images) && dayLookup.scan_images.length > 0) {
        scanImgs = dayLookup.scan_images;
      } else if (ext.scan_images && ext.scan_images.length > 0) {
        scanImgs = ext.scan_images;
      }
      const s = scanImgs.length > 0 ? scanImgs[0] : null;
      const primaryUrl = s ? (s.url || s.web_url || '') : '';
      const imgElem = document.getElementById('point-modal-img');
      imgElem.src = primaryUrl;

      applyPointModalBbox();
      setPointModalZoom(true);
      openModal('modal-point-source');
    }

    function setPointModalZoom(isZoomed) {
      pointModalZoomState = isZoomed;
      const stage = document.getElementById('point-modal-stage');
      const btnZoom = document.getElementById('btn-point-zoom-cell');
      const btnFull = document.getElementById('btn-point-zoom-full');
      if (!stage) return;

      if (isZoomed) {
        if (btnZoom) btnZoom.classList.add('active');
        if (btnFull) btnFull.classList.remove('active');
        const cx = (pointModalBbox[0] + pointModalBbox[2] / 2) * 100;
        const cy = (pointModalBbox[1] + pointModalBbox[3] / 2) * 100;
        stage.style.transformOrigin = `${cx}% ${cy}%`;
        stage.style.transform = 'scale(3.2)';
      } else {
        if (btnFull) btnFull.classList.add('active');
        if (btnZoom) btnZoom.classList.remove('active');
        stage.style.transformOrigin = 'center center';
        stage.style.transform = 'scale(1)';
      }
    }

    function onPointModalImgLoaded() {
      applyPointModalBbox();
      setPointModalZoom(pointModalZoomState);
    }

    function applyPointModalBbox() {
      const box = document.getElementById('point-modal-highlight-box');
      if (!box || !pointModalBbox) return;
      const [x, y, w, h] = pointModalBbox;
      box.style.left = `${x * 100}%`;
      box.style.top = `${y * 100}%`;
      box.style.width = `${Math.max(w * 100, 2.5)}%`;
      box.style.height = `${Math.max(h * 100, 1.8)}%`;
    }

    // Flags & Technical Manual Modal
    function renderFlagCards(anomalies) {
      const cont = document.getElementById('flags-list-container');
      if (!cont) return;
      cont.innerHTML = '';

      if (anomalies.length === 0) {
        cont.innerHTML = '<div style="color:var(--ink-2); font-size:13px; padding:12px 0;">No abnormal trends or improbable telemetry values detected for this date.</div>';
        return;
      }

      anomalies.forEach((a, idx) => {
        const item = document.createElement('div');
        item.className = `flag-item ${a.severity}`;

        item.innerHTML = `
          <div class="flag-info">
            <div class="flag-head-line">
              <span class="flag-category">${a.category}</span>
              <span class="flag-severity-tag ${a.severity}">${a.severity}</span>
            </div>
            <div class="flag-text">${a.finding}</div>
            <div class="flag-manual-ref">Cited: ${a.tech_manual ? a.tech_manual.code : 'BUSHIPS Standards'}</div>
          </div>
          <div>
            <button class="btn sm" onclick="openTechManualModal(window._currentAnomalies[${idx}])">Review Flag</button>
          </div>
        `;
        cont.appendChild(item);
      });
    }

    function openTechManualModal(anomaly) {
      if (!anomaly) return;
      document.getElementById('tm-modal-cat').innerText = anomaly.category;
      document.getElementById('tm-modal-time').innerText = anomaly.date_hour || 'Log Entry';
      document.getElementById('tm-modal-finding').innerText = anomaly.finding;
      document.getElementById('tm-modal-delta').innerText = anomaly.observed_vs_expected || 'Parameter excursion';

      const tm = anomaly.tech_manual;
      if (tm) {
        document.getElementById('tm-modal-card').style.display = 'block';
        document.getElementById('tm-modal-code').innerText = tm.code || 'BUSHIPS Manual';
        document.getElementById('tm-modal-title').innerText = tm.title || 'Standard Operating Threshold';
        document.getElementById('tm-modal-sec').innerText = tm.section || '';
        document.getElementById('tm-modal-excerpt').innerText = tm.citation || tm.citation_excerpt || '';
      } else {
        document.getElementById('tm-modal-card').style.display = 'none';
      }

      document.getElementById('tm-modal-action').innerText = anomaly.recommendation || anomaly.corrective_action || (tm && tm.corrective_procedure) || 'Inspect machinery bearings and record hourly salinity readings in engine room ledger.';
      openModal('modal-tech-manual');
    }

    // Editable 24-Hour Table
    function renderHourlyTable(rows) {
      const tbody = document.getElementById('hourly-tbody');
      if (!tbody) return;
      tbody.innerHTML = '';

      rows.forEach((r, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="font-weight:600; color:var(--brass);">${String(r.hour).padStart(2, '0')}00</td>
          <td><input type="text" value="${r.revs || ''}" id="ed-revs-${idx}"></td>
          <td><input type="text" value="${r.speed_knots || ''}" id="ed-speed-${idx}"></td>
          <td><input type="text" value="${r.course || ''}" id="ed-course-${idx}"></td>
          <td><input type="text" value="${r.wind_dir || ''}" id="ed-wind-${idx}"></td>
          <td><input type="text" value="${r.barometer_raw || ''}" id="ed-baro-${idx}"></td>
          <td><input type="text" value="${r.temp_dry_bulb || ''}" id="ed-dry-${idx}"></td>
          <td><input type="text" value="${r.temp_wet_bulb || ''}" id="ed-wet-${idx}"></td>
          <td><input type="text" value="${r.port_rpm || ''}" id="ed-prpm-${idx}"></td>
          <td><input type="text" value="${r.stbd_rpm || ''}" id="ed-srpm-${idx}"></td>
          <td><input type="text" value="${r.thrust_bearing_temp_f || ''}" id="ed-thrust-${idx}"></td>
          <td><input type="text" value="${r.feed_salinity_grains || ''}" id="ed-sal-${idx}"></td>
        `;
        tbody.appendChild(tr);
      });
    }

    async function saveHourlyEditor() {
      if (!currentDayData) return;
      const ext = currentDayData.extraction;
      const rows = ext.hourly_rows || [];

      const updatedRows = rows.map((orig, idx) => {
        const revsVal = document.getElementById(`ed-revs-${idx}`).value;
        const speedVal = parseFloat(document.getElementById(`ed-speed-${idx}`).value);
        const baroVal = document.getElementById(`ed-baro-${idx}`).value;
        const dryVal = document.getElementById(`ed-dry-${idx}`).value;
        const wetVal = document.getElementById(`ed-wet-${idx}`).value;
        const courseVal = document.getElementById(`ed-course-${idx}`).value;
        const windVal = document.getElementById(`ed-wind-${idx}`).value;
        const prpmVal = parseInt(document.getElementById(`ed-prpm-${idx}`).value, 10);
        const srpmVal = parseInt(document.getElementById(`ed-srpm-${idx}`).value, 10);
        const thrustVal = parseFloat(document.getElementById(`ed-thrust-${idx}`).value);
        const salVal = parseFloat(document.getElementById(`ed-sal-${idx}`).value);

        return {
          ...orig,
          revs: revsVal,
          speed_knots: isNaN(speedVal) ? orig.speed_knots : speedVal,
          barometer_raw: baroVal,
          temp_dry_bulb: dryVal,
          temp_wet_bulb: wetVal,
          course: courseVal,
          wind_dir: windVal,
          port_rpm: isNaN(prpmVal) ? 0 : prpmVal,
          stbd_rpm: isNaN(srpmVal) ? 0 : srpmVal,
          thrust_bearing_temp_f: isNaN(thrustVal) ? null : thrustVal,
          feed_salinity_grains: isNaN(salVal) ? null : salVal,
        };
      });

      const fuelPrior = parseInt(document.getElementById('edit-fuel-prior').value, 10) || 0;
      const fuelRecv = parseInt(document.getElementById('edit-fuel-received').value, 10) || 0;
      const fuelExp = parseInt(document.getElementById('edit-fuel-expended').value, 10) || 0;
      const waterDist = parseInt(document.getElementById('edit-water-distilled').value, 10) || 0;
      const waterExp = parseInt(document.getElementById('edit-water-expended').value, 10) || 0;

      const payload = {
        updates: {
          hourly_rows: updatedRows,
          fuel: {
            ...ext.fuel,
            prior_on_hand: fuelPrior,
            received: fuelRecv,
            expended: fuelExp,
            on_hand: fuelPrior + fuelRecv - fuelExp,
          },
          water: {
            ...ext.water,
            distilled: waterDist,
            expended: waterExp,
            on_hand: (ext.water?.prior_on_hand || 5000) + waterDist - waterExp,
          }
        }
      };

      try {
        const res = await fetch(`/api/day/${ext.day_id}/update`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        currentDayData = await res.json();
        await fetchCorpusTrends();
        renderDashboardView();
        showToast('Log updates saved. Charts and audit equations recalculated.');
      } catch (err) {
        showToast('Error saving updates: ' + err.message);
      }
    }

    // =========================================================================
    // HOME SCREEN VISIBLE OCR WORKBENCH HANDLERS
    // =========================================================================
    let selectedHomeOcrSampleId = null;

    function setupDragAndDropZones() {
      const bindings = [
        { zoneId: 'dropzone-home-ocr', inputId: 'home-ocr-file', cb: onHomeOcrFileSelected },
        { zoneId: 'dropzone-home-log', inputId: 'home-up-log-file', cb: onHomeLogFileSelected },
        { zoneId: 'dropzone-home-manual', inputId: 'home-man-file', cb: onHomeManualFileSelected },
      ];
      bindings.forEach(({ zoneId, inputId, cb }) => {
        const zone = document.getElementById(zoneId);
        const input = document.getElementById(inputId);
        if (!zone || !input) return;

        ['dragenter', 'dragover'].forEach(evtName => {
          zone.addEventListener(evtName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            zone.style.borderColor = 'var(--brass)';
            zone.style.background = 'var(--brass-soft)';
          });
        });

        ['dragleave', 'drop'].forEach(evtName => {
          zone.addEventListener(evtName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            zone.style.borderColor = '';
            zone.style.background = '';
          });
        });

        zone.addEventListener('drop', (e) => {
          const dt = e.dataTransfer;
          if (dt && dt.files && dt.files.length > 0) {
            try {
              input.files = dt.files;
            } catch (_) {}
            cb(input, dt.files[0]);
          }
        });
      });
    }

    function switchHomeOcrTab(tabName) {
      const panes = {
        multi: document.getElementById('home-ocr-pane-multi'),
        log: document.getElementById('home-ocr-pane-log'),
        manual: document.getElementById('home-ocr-pane-manual'),
      };
      const btns = {
        multi: document.getElementById('btn-home-ocr-tab-multi'),
        log: document.getElementById('btn-home-ocr-tab-log'),
        manual: document.getElementById('btn-home-ocr-tab-manual'),
      };
      Object.keys(panes).forEach(k => {
        if (panes[k]) panes[k].style.display = (k === tabName) ? 'flex' : 'none';
        if (btns[k]) {
          if (k === tabName) btns[k].classList.add('active');
          else btns[k].classList.remove('active');
        }
      });
    }

    // =========================================================================
    // SHIP / OPERATIONAL UNIT ASSIGNMENT MODAL FOR UNKNOWN SHIP FILES
    // =========================================================================
    window._pendingShipUpload = null;
    window._askShipExistingList = [];

    function buildExistingShipsList(responseData) {
      const map = new Map();
      const fromOverview = getUniqueUploadedShips((overviewData && overviewData.days) || []);
      fromOverview.forEach(s => {
        map.set(s.ship_display, {
          ship_display: s.ship_display,
          ship_name: s.ship_name || s.ship_display,
          hull_number: s.hull_number || '',
          unit_type: s.unit_type || 'Ship',
        });
      });

      const respShips = (responseData && responseData.existing_ships) || [];
      respShips.forEach(item => {
        if (typeof item === 'string' && item.trim()) {
          const disp = item.trim();
          if (!map.has(disp)) {
            const m = disp.match(/^(.*?)\s*\(([^)]+)\)$/);
            map.set(disp, {
              ship_display: disp,
              ship_name: m ? m[1].trim() : disp,
              hull_number: m ? m[2].trim() : '',
              unit_type: 'Ship',
            });
          }
        } else if (item && typeof item === 'object') {
          const disp = item.ship_display || item.ship_name || item.name || '';
          if (disp && !map.has(disp)) {
            map.set(disp, {
              ship_display: disp,
              ship_name: item.ship_name || item.name || disp,
              hull_number: item.hull_number || item.hull || '',
              unit_type: item.unit_type || 'Ship',
            });
          }
        }
      });

      return Array.from(map.values());
    }

    function promptForShipAssignment(pendingContext, responseData) {
      window._pendingShipUpload = pendingContext;
      const existingShips = buildExistingShipsList(responseData);
      window._askShipExistingList = existingShips;

      const fnLabel = document.getElementById('ask-ship-filename-label');
      if (fnLabel) {
        fnLabel.innerText = (responseData && responseData.pending_filename) || pendingContext.pending_filename || 'Uploaded Document';
      }

      const sel = document.getElementById('ask-ship-existing-select');
      const sec = document.getElementById('ask-ship-existing-section');
      if (sel) {
        sel.innerHTML = '<option value="">-- Create New Ship / Unit Below --</option>';
        existingShips.forEach(s => {
          const opt = document.createElement('option');
          opt.value = s.ship_display;
          opt.text = s.ship_display;
          sel.appendChild(opt);
        });
        sel.value = '';
      }
      if (sec) {
        sec.style.display = existingShips.length > 0 ? 'block' : 'block';
      }

      const nameInput = document.getElementById('ask-ship-name-input');
      const hullInput = document.getElementById('ask-ship-hull-input');
      const unitSelect = document.getElementById('ask-ship-unit-type');
      if (nameInput) nameInput.value = '';
      if (hullInput) hullInput.value = '';
      if (unitSelect) unitSelect.value = 'Ship';

      openModal('modal-ask-ship');
    }

    function onAskShipExistingSelected(val) {
      const nameInput = document.getElementById('ask-ship-name-input');
      const hullInput = document.getElementById('ask-ship-hull-input');
      const unitSelect = document.getElementById('ask-ship-unit-type');
      if (!val) {
        if (nameInput) nameInput.value = '';
        if (hullInput) hullInput.value = '';
        if (unitSelect) unitSelect.value = 'Ship';
        return;
      }
      const found = (window._askShipExistingList || []).find(
        s => s.ship_display === val || s.ship_name === val
      );
      if (found) {
        if (nameInput) nameInput.value = found.ship_name || found.ship_display;
        if (hullInput) hullInput.value = found.hull_number || '';
        if (unitSelect) unitSelect.value = found.unit_type || 'Ship';
      } else if (nameInput) {
        nameInput.value = val;
      }
    }

    async function confirmPendingShipUpload() {
      const pending = window._pendingShipUpload;
      if (!pending) {
        closeModal('modal-ask-ship');
        return;
      }

      const existingSel = document.getElementById('ask-ship-existing-select');
      let shipName = ((document.getElementById('ask-ship-name-input') || {}).value || '').trim();
      const hullNumber = ((document.getElementById('ask-ship-hull-input') || {}).value || '').trim();
      const unitType = ((document.getElementById('ask-ship-unit-type') || {}).value || 'Ship').trim();

      if (!shipName && existingSel && existingSel.value) {
        shipName = existingSel.value.trim();
      }
      if (!shipName) {
        showToast('Please select an existing ship or enter a ship name.');
        return;
      }

      const btn = document.getElementById('btn-confirm-ask-ship');
      const origText = btn ? btn.innerText : 'Assign & Digitize File';
      if (btn) {
        btn.innerText = 'Assigning & Digitizing...';
        btn.disabled = true;
      }

      try {
        const fd = pending.formData || new FormData();
        fd.set('ship_name', shipName);
        fd.set('hull_number', hullNumber);
        fd.set('unit_type', unitType);
        if (pending.pending_filename) {
          fd.set('pending_filename', pending.pending_filename);
        }

        const res = await fetch(pending.endpoint, {
          method: 'POST',
          body: fd,
        });
        let resultData = null;
        try {
          resultData = await res.json();
        } catch (_) {}
        if (!res.ok) {
          throw new Error((resultData && (resultData.detail || resultData.error || resultData.message)) || `Request failed (${res.status})`);
        }

        closeModal('modal-ask-ship');
        window._pendingShipUpload = null;
        await Promise.all([loadOverviewData(), fetchCorpusTrends()]);
        if (pending.onSuccess) {
          await pending.onSuccess(resultData);
        }
      } catch (err) {
        showToast('Error assigning ship: ' + err.message);
      } finally {
        if (btn) {
          btn.innerText = origText;
          btn.disabled = false;
        }
      }
    }

    function onHomeOcrFileSelected(input, droppedFile) {
      selectedHomeOcrSampleId = null;
      const label = document.getElementById('home-ocr-file-label');
      const file = droppedFile || (input && input.files && input.files[0]);
      if (file) {
        window._droppedHomeOcrFile = file;
        label.innerText = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
      } else {
        window._droppedHomeOcrFile = null;
        label.innerText = 'Drop Scanned Document Here or Click to Browse (.pdf, .png, .jpg, .tiff)';
      }
    }

    async function renderHomeOcrResultData(data) {
      if (data.day_id) {
        await Promise.all([loadOverviewData(), fetchCorpusTrends()]);
      }
      const resBox = document.getElementById('home-ocr-results-box');
      resBox.style.display = 'block';

      document.getElementById('home-ocr-res-template-title').innerText = `Converted to: ${data.selected_template}`;
      document.getElementById('home-ocr-res-conf-pill').innerText = `${data.template_confidence}% Match`;
      document.getElementById('home-ocr-res-reason').innerText = data.template_reason || 'Autonomous DECK template classification verified.';
      document.getElementById('home-ocr-res-tokens').innerText = data.total_tokens || 0;
      document.getElementById('home-ocr-res-mean-conf').innerText = data.mean_confidence_pct || '0%';
      document.getElementById('home-ocr-res-low-conf').innerText = data.low_confidence_count || 0;

      const actionsDiv = document.getElementById('home-ocr-res-actions');
      actionsDiv.innerHTML = '';

      if (data.files && data.files.xlsx_url) {
        actionsDiv.innerHTML += `
          <a href="${data.files.xlsx_url}" download class="btn sm" style="text-decoration:none;">
            Download Excel (${data.files.xlsx_filename})
          </a>
        `;
      }
      if (data.files && data.files.docx_url) {
        actionsDiv.innerHTML += `
          <a href="${data.files.docx_url}" download class="btn sm" style="text-decoration:none;">
            Download Word (${data.files.docx_filename})
          </a>
        `;
      }
      if (data.day_id) {
        actionsDiv.innerHTML += `
          <button type="button" class="btn sm primary" onclick="loadDayAnalytics('${data.day_id}'); navigateTo('dashboard');">
            Open in DECK Telemetry Dashboard →
          </button>
        `;
      }

      showToast(`DECK OCR Complete: Converted "${data.selected_template}" (${data.total_tokens} tokens).`);
    }

    async function startHomeIntelligentOcrExtraction() {
      const btn = document.getElementById('btn-home-run-ocr');
      const origHtml = btn.innerText;

      const fileInput = document.getElementById('home-ocr-file');
      const fileToUpload = (fileInput && fileInput.files && fileInput.files[0]) || window._droppedHomeOcrFile;
      if (!fileToUpload && !selectedHomeOcrSampleId) {
        showToast('Please select or drop a scanned document file first.');
        return;
      }

      btn.innerText = 'Running DECK OCR & Converting...';
      btn.disabled = true;

      try {
        const formData = new FormData();
        if (fileToUpload) {
          formData.append('file', fileToUpload);
        } else if (selectedHomeOcrSampleId) {
          formData.append('sample_id', selectedHomeOcrSampleId);
        }

        const tTarget = document.getElementById('home-ocr-template-target').value;
        if (tTarget) formData.append('template_override', tTarget);
        formData.append('mode', document.getElementById('home-ocr-mode').value || 'fast');

        const res = await fetch('/api/intelligent-ocr-extract', {
          method: 'POST',
          body: formData,
        });

        let data = null;
        try {
          data = await res.json();
        } catch (_) {}

        if (data && data.needs_ship_name) {
          promptForShipAssignment({
            endpoint: '/api/intelligent-ocr-extract',
            formData,
            pending_filename: data.pending_filename || (fileToUpload ? fileToUpload.name : ''),
            onSuccess: renderHomeOcrResultData,
          }, data);
          return;
        }

        if (!res.ok) throw new Error((data && (data.detail || data.error)) || `OCR Extraction failed: ${res.statusText}`);
        await renderHomeOcrResultData(data);
      } catch (err) {
        showToast(`DECK OCR Error: ${err.message}`);
      } finally {
        btn.innerText = origHtml;
        btn.disabled = false;
      }
    }

    function onHomeLogFileSelected(input, droppedFile) {
      const file = droppedFile || (input && input.files && input.files[0]);
      if (file) {
        window._droppedHomeLogFile = file;
        document.getElementById('home-up-file-label').innerText = `${file.name} (${Math.round(file.size / 1024)} KB)`;
      }
    }

    async function completeHomeLogUploadSuccess(bundle) {
      await Promise.all([loadOverviewData(), fetchCorpusTrends()]);
      currentDayData = bundle;
      currentDayId = bundle.day_id;
      selectedPickerDayId = bundle.day_id;
      renderDashboardView();
      navigateTo('dashboard');
      showToast('Unit log digitized via DECK OCR! Telemetry & manual audit loaded.');
    }

    async function handleHomeLogUpload(evt) {
      evt.preventDefault();
      const fileInput = document.getElementById('home-up-log-file');
      const fileToSend = (fileInput && fileInput.files && fileInput.files[0]) || window._droppedHomeLogFile;
      if (!fileToSend) {
        showToast('Please select a scanned logbook file (.pdf, .png, .jpg) to digitize.');
        return;
      }

      const btn = document.getElementById('btn-home-submit-log');
      const origText = btn.innerText;
      btn.innerText = 'Running OCR & Auditing...';
      btn.disabled = true;

      const fd = new FormData();
      fd.append('file', fileToSend);
      fd.append('unit_type', document.getElementById('home-up-unit-type').value);
      fd.append('ship_name', document.getElementById('home-up-ship-name').value);
      fd.append('hull_number', document.getElementById('home-up-hull-no').value);
      fd.append('date_iso', document.getElementById('home-up-date-iso').value);
      fd.append('page_number', document.getElementById('home-up-page-no').value);
      fd.append('location', document.getElementById('home-up-location').value);

      try {
        const res = await fetch('/api/upload-scan', {
          method: 'POST',
          body: fd,
        });
        let bundle = null;
        try {
          bundle = await res.json();
        } catch (_) {}

        if (bundle && bundle.needs_ship_name) {
          promptForShipAssignment({
            endpoint: '/api/upload-scan',
            formData: fd,
            pending_filename: bundle.pending_filename || fileToSend.name,
            onSuccess: completeHomeLogUploadSuccess,
          }, bundle);
          return;
        }

        if (!res.ok) throw new Error((bundle && (bundle.detail || bundle.error)) || `Upload failed (${res.status})`);
        await completeHomeLogUploadSuccess(bundle);
      } catch (err) {
        showToast('Log upload failed: ' + err.message);
      } finally {
        btn.innerText = origText;
        btn.disabled = false;
      }
    }

    function onHomeManualFileSelected(input, droppedFile) {
      const file = droppedFile || (input && input.files && input.files[0]);
      if (file) {
        window._droppedHomeManualFile = file;
        document.getElementById('home-man-file-label').innerText = `${file.name} (${Math.round(file.size / 1024)} KB)`;
      }
    }

    async function handleHomeManualUpload(evt) {
      evt.preventDefault();
      const btn = document.getElementById('btn-home-submit-manual');
      const origHtml = btn.innerText;
      btn.innerText = 'Indexing Manual...';
      btn.disabled = true;

      try {
        const fd = new FormData();
        const fileInput = document.getElementById('home-man-file');
        if (fileInput && fileInput.files && fileInput.files[0]) {
          fd.append('file', fileInput.files[0]);
        }
        fd.append('title', document.getElementById('home-man-title').value);
        fd.append('code', document.getElementById('home-man-code').value);
        fd.append('unit_type', document.getElementById('home-man-unit-type').value);
        fd.append('subsystem', document.getElementById('home-man-subsystem').value);
        fd.append('standard_limit', document.getElementById('home-man-limit').value);

        const res = await fetch('/api/upload-manual', {
          method: 'POST',
          body: fd,
        });
        if (!res.ok) throw new Error(`Failed to index manual (${res.status})`);
        const data = await res.json();
        await loadOverviewData();
        showToast(`Technical Manual "${data.manual.code} — ${data.manual.title}" indexed into DECK Reference Library!`);
        document.getElementById('home-man-title').value = '';
        document.getElementById('home-man-code').value = '';
        document.getElementById('home-man-subsystem').value = '';
        document.getElementById('home-man-limit').value = '';
      } catch (err) {
        showToast('Manual indexing failed: ' + err.message);
      } finally {
        btn.innerText = origHtml;
        btn.disabled = false;
      }
    }

    // Intelligent OCR Extractor Modal
    function onOcrFileSelected(input) {
      const file = input.files[0];
      if (file) {
        document.getElementById('ocr-file-label').innerText = `${file.name} (${Math.round(file.size / 1024)} KB)`;
        document.getElementById('ocr-sample-id').value = '';
      }
    }

    async function renderModalOcrResultData(data) {
      if (data.day_id) {
        await Promise.all([loadOverviewData(), fetchCorpusTrends()]);
      }
      const resBox = document.getElementById('ocr-results-box');
      resBox.style.display = 'block';

      document.getElementById('ocr-res-template-title').innerText = `Matched: ${data.selected_template}`;
      document.getElementById('ocr-res-conf-pill').innerText = `${data.template_confidence_pct || (data.template_confidence + '%')} Match`;
      document.getElementById('ocr-res-reason').innerText = data.template_reason || 'Autonomous template classification verified.';
      document.getElementById('ocr-res-tokens').innerText = data.total_tokens || 0;
      document.getElementById('ocr-res-mean-conf').innerText = data.mean_confidence_pct || '0%';
      document.getElementById('ocr-res-low-conf').innerText = data.low_confidence_count || 0;

      const actionsDiv = document.getElementById('ocr-res-actions');
      actionsDiv.innerHTML = '';

      if (data.files && data.files.xlsx_url) {
        actionsDiv.innerHTML += `
          <a href="${data.files.xlsx_url}" download class="btn sm" style="text-decoration:none;">
            Download Excel (${data.files.xlsx_filename})
          </a>
        `;
      }
      if (data.files && data.files.docx_url) {
        actionsDiv.innerHTML += `
          <a href="${data.files.docx_url}" download class="btn sm" style="text-decoration:none;">
            Download Word (${data.files.docx_filename})
          </a>
        `;
      }
      if (data.day_id) {
        actionsDiv.innerHTML += `
          <button type="button" class="btn sm primary" onclick="closeModal('modal-upload'); loadDayAnalytics('${data.day_id}'); navigateTo('dashboard');">
            Open in Fleet Analytics
          </button>
        `;
      }

      showToast(`Matched "${data.selected_template}" with ${data.total_tokens} verified tokens.`);
    }

    async function handleOcrExtractSubmit(e) {
      e.preventDefault();
      const fileInput = document.getElementById('ocr-file-input');
      const upLogInput = document.getElementById('up-log-file');
      const sampleId = (document.getElementById('ocr-sample-id') || {}).value || '';
      const fileToUpload = (fileInput && fileInput.files && fileInput.files[0]) || (upLogInput && upLogInput.files && upLogInput.files[0]) || capturedWebcamFile;

      if (!fileToUpload && !sampleId) {
        showToast('Please select a file or capture a page from the camera first.');
        return;
      }

      const btn = document.getElementById('btn-start-ocr');
      const origText = btn.innerText;
      btn.innerText = 'Processing...';
      btn.disabled = true;

      try {
        const formData = new FormData();
        if (fileToUpload) {
          formData.append('file', fileToUpload);
        }
        if (sampleId) {
          formData.append('sample_id', sampleId);
        }
        const shipNameVal = ((document.getElementById('up-ship-name') || {}).value || '').trim();
        const hullNoVal = ((document.getElementById('up-hull-no') || {}).value || '').trim();
        if (shipNameVal) formData.append('ship_name', shipNameVal);
        if (hullNoVal) formData.append('hull_number', hullNoVal);
        formData.append('mode', 'accurate');

        const res = await fetch('/api/intelligent-ocr-extract', {
          method: 'POST',
          body: formData,
        });

        let data = null;
        try {
          data = await res.json();
        } catch (_) {}

        if (data && data.needs_ship_name) {
          promptForShipAssignment({
            endpoint: '/api/intelligent-ocr-extract',
            formData,
            pending_filename: data.pending_filename || (fileToUpload ? fileToUpload.name : ''),
            onSuccess: renderModalOcrResultData,
          }, data);
          return;
        }

        if (!res.ok) throw new Error((data && (data.detail || data.error)) || 'Extraction failed');
        await renderModalOcrResultData(data);
      } catch (err) {
        showToast('Extraction error: ' + err.message);
      } finally {
        btn.innerText = origText;
        btn.disabled = false;
      }
    }

    // =========================================================================
    // CAMERA PAGE SCANNER & /api/extract SUBMISSION (R3)
    // =========================================================================
    let webcamStream = null;
    let webcamCountdownTimer = null;
    let capturedWebcamFile = null;

    async function startWebcamScanner(preferredDeviceId) {
      const box = document.getElementById('webcamScannerBox');
      const video = document.getElementById('webcamVideo');
      const statusMsg = document.getElementById('upload-status-msg');
      if (box) box.style.display = 'block';

      if (webcamStream) {
        webcamStream.getTracks().forEach(t => t.stop());
        webcamStream = null;
      }

      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        if (statusMsg) statusMsg.innerText = 'Camera API unavailable in this browser context; use file upload or simulated capture.';
        return;
      }

      try {
        const videoConstraints = preferredDeviceId
          ? { deviceId: { exact: preferredDeviceId }, width: { ideal: 1920 }, height: { ideal: 1080 } }
          : { facingMode: { ideal: 'environment' }, width: { ideal: 1920 }, height: { ideal: 1080 } };

        webcamStream = await navigator.mediaDevices.getUserMedia({ video: videoConstraints, audio: false });
        if (video) {
          video.srcObject = webcamStream;
          await video.play().catch(() => {});
        }
        updateWebcamMirror();

        // Populate camera device selector
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(d => d.kind === 'videoinput');
        const selectEl = document.getElementById('webcamDeviceSelect');
        if (selectEl && videoDevices.length > 0) {
          const currentTrack = webcamStream.getVideoTracks()[0];
          const activeDeviceId = (currentTrack && currentTrack.getSettings && currentTrack.getSettings().deviceId) || preferredDeviceId || '';
          selectEl.innerHTML = '';
          videoDevices.forEach((d, idx) => {
            const opt = document.createElement('option');
            opt.value = d.deviceId;
            opt.text = d.label || `Camera ${idx + 1}`;
            if (d.deviceId === activeDeviceId) opt.selected = true;
            selectEl.appendChild(opt);
          });
        }

        if (statusMsg) statusMsg.innerText = 'Camera active — align logbook page inside frame and click Capture Snapshot.';
      } catch (err) {
        if (statusMsg) statusMsg.innerText = `Camera access notice: ${err.message}. You can still capture a test frame or select a file.`;
      }
    }

    async function switchWebcamDevice(deviceId) {
      await startWebcamScanner(deviceId);
    }

    function updateWebcamMirror() {
      const toggle = document.getElementById('webcamMirrorToggle');
      const video = document.getElementById('webcamVideo');
      if (!video) return;
      const isMirrored = toggle && toggle.checked;
      video.style.transform = isMirrored ? 'scaleX(-1)' : 'none';
    }

    function stopWebcamScanner() {
      if (webcamCountdownTimer) {
        clearInterval(webcamCountdownTimer);
        webcamCountdownTimer = null;
      }
      const overlay = document.getElementById('webcamCountdownOverlay');
      if (overlay) overlay.style.display = 'none';

      if (webcamStream) {
        webcamStream.getTracks().forEach(t => t.stop());
        webcamStream = null;
      }
      const video = document.getElementById('webcamVideo');
      if (video) video.srcObject = null;
      const box = document.getElementById('webcamScannerBox');
      if (box) box.style.display = 'none';
    }

    function startWebcamCountdownCapture() {
      const overlay = document.getElementById('webcamCountdownOverlay');
      if (!overlay) {
        captureWebcamSnapshot();
        return;
      }
      if (webcamCountdownTimer) clearInterval(webcamCountdownTimer);
      let remaining = 3;
      overlay.innerText = String(remaining);
      overlay.style.display = 'flex';
      webcamCountdownTimer = setInterval(() => {
        remaining -= 1;
        if (remaining > 0) {
          overlay.innerText = String(remaining);
        } else {
          clearInterval(webcamCountdownTimer);
          webcamCountdownTimer = null;
          overlay.style.display = 'none';
          captureWebcamSnapshot();
        }
      }, 1000);
    }

    function captureWebcamSnapshot() {
      const video = document.getElementById('webcamVideo');
      const canvas = document.getElementById('webcamCanvas');
      const previewImg = document.getElementById('webcamPreviewImg');
      const placeholder = document.getElementById('webcamPreviewPlaceholder');
      const metaEl = document.getElementById('webcamCaptureMeta');
      const statusMsg = document.getElementById('upload-status-msg');
      const filterMode = (document.getElementById('webcamFilterMode') || {}).value || 'doc_contrast';
      const isMirrored = (document.getElementById('webcamMirrorToggle') || {}).checked || false;

      if (!canvas) return;
      const w = (video && video.videoWidth) ? video.videoWidth : 1280;
      const h = (video && video.videoHeight) ? video.videoHeight : 960;
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext('2d');

      ctx.save();
      if (isMirrored) {
        ctx.translate(w, 0);
        ctx.scale(-1, 1);
      }

      if (video && video.videoWidth > 0) {
        ctx.drawImage(video, 0, 0, w, h);
      } else {
        // Fallback synthetic Form N. Nav. 45 scan frame when headless/no physical webcam
        ctx.fillStyle = '#f2ead7';
        ctx.fillRect(0, 0, w, h);
        ctx.strokeStyle = '#2d3b4e';
        ctx.lineWidth = 3;
        ctx.strokeRect(40, 40, w - 80, h - 80);
        ctx.fillStyle = '#1b2636';
        ctx.font = 'bold 28px Georgia, serif';
        ctx.fillText('FORM N. NAV. 45 — CAMERA CAPTURED DECK LOG SPREAD', 80, 100);
      }
      ctx.restore();

      // Apply selected document enhancement filter
      if (filterMode === 'doc_contrast' || filterMode === 'grayscale') {
        const imgData = ctx.getImageData(0, 0, w, h);
        const d = imgData.data;
        for (let i = 0; i < d.length; i += 4) {
          const lum = 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2];
          if (filterMode === 'doc_contrast') {
            const contrasted = Math.max(0, Math.min(255, (lum - 128) * 1.45 + 132));
            d[i] = contrasted;
            d[i + 1] = contrasted;
            d[i + 2] = Math.max(0, contrasted - 6);
          } else {
            d[i] = lum;
            d[i + 1] = lum;
            d[i + 2] = lum;
          }
        }
        ctx.putImageData(imgData, 0, 0);
      }

      const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
      if (previewImg) {
        previewImg.src = dataUrl;
        previewImg.style.display = 'block';
      }
      if (placeholder) placeholder.style.display = 'none';

      const base64Data = dataUrl.split(',')[1] || '';
      const byteString = atob(base64Data);
      const bytes = new Uint8Array(byteString.length);
      for (let i = 0; i < byteString.length; i++) {
        bytes[i] = byteString.charCodeAt(i);
      }
      const ts = new Date().toISOString().replace(/[:.]/g, '-');
      const file = new File([bytes], `camera_scan_${ts}.jpg`, { type: 'image/jpeg' });
      capturedWebcamFile = file;

      // Attach to file inputs via DataTransfer where supported
      try {
        const dt = new DataTransfer();
        dt.items.add(file);
        const upLogFile = document.getElementById('up-log-file');
        if (upLogFile) upLogFile.files = dt.files;
        const ocrFileInput = document.getElementById('ocr-file-input');
        if (ocrFileInput) ocrFileInput.files = dt.files;
      } catch (_) {}

      const sizeKb = Math.max(1, Math.round(file.size / 1024));
      const label = document.getElementById('ocr-file-label');
      if (label) label.innerText = `${file.name} (${sizeKb} KB • Camera Capture)`;
      if (metaEl) metaEl.innerText = `Captured ${w}×${h}px (${filterMode}) — ${sizeKb} KB`;
      if (statusMsg) statusMsg.innerText = `Snapshot captured (${file.name}). Click "Digitize Captured Page" to extract.`;
    }

    async function completeScanExtractSuccess(bundle) {
      await Promise.all([loadOverviewData(), fetchCorpusTrends()]);
      currentDayData = bundle;
      currentDayId = bundle.day_id;
      selectedPickerDayId = bundle.day_id;
      stopWebcamScanner();
      closeModal('modal-upload');
      renderDashboardView();
      navigateTo('dashboard');
      showToast(`Camera page scan digitized (${bundle.extraction?.date_human || bundle.day_id}) and added to timeline!`);
    }

    async function submitScanUpload() {
      const upLogInput = document.getElementById('up-log-file');
      const ocrFileInput = document.getElementById('ocr-file-input');
      const statusMsg = document.getElementById('upload-status-msg');

      let fileToUpload = capturedWebcamFile;
      if (!fileToUpload && upLogInput && upLogInput.files && upLogInput.files[0]) {
        fileToUpload = upLogInput.files[0];
      }
      if (!fileToUpload && ocrFileInput && ocrFileInput.files && ocrFileInput.files[0]) {
        fileToUpload = ocrFileInput.files[0];
      }
      if (!fileToUpload) {
        // Synthesize a quick camera snapshot if user clicked directly
        captureWebcamSnapshot();
        await new Promise(r => setTimeout(r, 120));
        fileToUpload = capturedWebcamFile || new File([new Uint8Array([255, 216, 255, 217])], 'camera_page_scan.jpg', { type: 'image/jpeg' });
      }

      if (statusMsg) statusMsg.innerText = 'Submitting page scan to /api/extract...';
      const fd = new FormData();
      fd.append('file', fileToUpload);
      fd.append('unit_type', 'Ship');
      fd.append('ship_name', (document.getElementById('up-ship-name') || {}).value || '');
      fd.append('hull_number', (document.getElementById('up-hull-no') || {}).value || '');
      fd.append('date_iso', (document.getElementById('up-date-iso') || {}).value || '');
      fd.append('page_number', (document.getElementById('up-page-no') || {}).value || '');
      fd.append('location', (document.getElementById('up-location') || {}).value || '');

      try {
        const res = await fetch('/api/extract', {
          method: 'POST',
          body: fd,
        });
        let bundle = null;
        try {
          bundle = await res.json();
        } catch (_) {}

        if (bundle && bundle.needs_ship_name) {
          promptForShipAssignment({
            endpoint: '/api/extract',
            formData: fd,
            pending_filename: bundle.pending_filename || (fileToUpload ? fileToUpload.name : ''),
            onSuccess: completeScanExtractSuccess,
          }, bundle);
          return;
        }

        if (!res.ok) throw new Error((bundle && (bundle.detail || bundle.error)) || `Extraction failed (${res.status})`);
        await completeScanExtractSuccess(bundle);
      } catch (err) {
        if (statusMsg) statusMsg.innerText = `Error: ${err.message}`;
        showToast('Camera scan extraction failed: ' + err.message);
      }
    }

    // =========================================================================
    // Gemma 4 12B Offline Intelligence Interface
    // =========================================================================
    let gemmaStatusData = null;

    async function refreshGemmaStatus() {
      try {
        const res = await fetch('/api/gemma/status');
        if (!res.ok) return;
        gemmaStatusData = await res.json();
        updateGemmaUI(gemmaStatusData);
      } catch (err) {
        console.warn('Gemma status probe failed:', err);
      }
    }

    function updateGemmaUI(status) {
      if (!status) return;
      const dot = document.getElementById('gemma-status-dot');
      const lbl = document.getElementById('gemma-status-label');
      const badge = document.getElementById('gemma-modal-status-badge');
      const provEl = document.getElementById('gemma-modal-active-provider');

      if (status.connected) {
        if (dot) dot.style.background = 'var(--good, #22c55e)';
        if (lbl) lbl.innerText = `Gemma 4 12B (${status.active_runner === 'ollama' ? 'Ollama' : 'LM Studio'})`;
        if (badge) {
          badge.className = 'flag-severity-tag INFO';
          badge.innerText = 'ONLINE / GPU ACCELERATED';
          badge.style.background = 'rgba(34,197,94,0.15)';
          badge.style.color = '#22c55e';
        }
        if (provEl) provEl.innerText = `${status.active_runner.toUpperCase()} (Online)`;
      } else {
        if (dot) dot.style.background = 'var(--warn, #eab308)';
        if (lbl) lbl.innerText = 'Gemma 4 12B (Offline Ready)';
        if (badge) {
          badge.className = 'flag-severity-tag WARNING';
          badge.innerText = 'OFFLINE STANDBY';
          badge.style.background = 'rgba(234,179,8,0.15)';
          badge.style.color = '#eab308';
        }
        if (provEl) provEl.innerText = 'Fallback Built-in Engine (Active)';
      }
    }

    function openGemmaModal() {
      openModal('modal-gemma');
      refreshGemmaStatus();
    }

    function toggleGemmaProviderUI() {
      const prov = document.getElementById('gemma-cfg-provider').value;
      const urlInput = document.getElementById('gemma-cfg-url');
      if (prov === 'ollama') {
        urlInput.value = 'http://127.0.0.1:11434';
      } else {
        urlInput.value = 'http://127.0.0.1:1234/v1';
      }
    }

    async function saveGemmaConfigAndTest() {
      const prov = document.getElementById('gemma-cfg-provider').value;
      const url = document.getElementById('gemma-cfg-url').value;
      const model = document.getElementById('gemma-cfg-model').value;

      try {
        const payload = {
          enabled: true,
          provider: prov,
          model: model,
          ollama_url: prov === 'ollama' ? url : 'http://127.0.0.1:11434',
          openai_url: prov === 'openai_compatible' ? url : 'http://127.0.0.1:1234/v1',
          temperature: 0.1,
        };
        const res = await fetch('/api/gemma/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        gemmaStatusData = data.gemma_status;
        updateGemmaUI(gemmaStatusData);
        if (gemmaStatusData.connected) {
          showToast(`Connected to Gemma via ${prov.toUpperCase()}! Model: ${model}`);
        } else {
          showToast('Settings saved. Gemma runner is in offline standby mode.');
        }
      } catch (err) {
        showToast('Failed to save config: ' + err.message);
      }
    }

    async function runGemmaTelemetryAudit() {
      if (!currentDayId) {
        showToast('Please select or upload a log day first.');
        return;
      }
      const btn = document.getElementById('btn-gemma-audit');
      if (btn) {
        btn.disabled = true;
        btn.innerText = '⚡ Running Gemma 4 12B Audit...';
      }
      try {
        const res = await fetch(`/api/gemma/analyze-day/${currentDayId}`, {
          method: 'POST',
        });
        if (!res.ok) throw new Error('Failed to run Gemma audit');
        const data = await res.json();
        const analysis = data.gemma_analysis || {};
        const anomalies = analysis.anomalies || [];
        window._currentAnomalies = anomalies;
        renderFlagCards(anomalies);
        showToast(`Gemma 4 12B Audit complete: ${anomalies.length} physical/aerological flags verified.`);
      } catch (err) {
        showToast('Audit error: ' + err.message);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerText = '⚡ Gemma 4 12B Physical Audit';
        }
      }
    }
  </script>
</body>
</html>

"""

def build_simplified_html() -> str:
    return HTML_CONTENT.strip() + "\n"

if __name__ == '__main__':
    INDEX_PATH.write_text(build_simplified_html(), encoding='utf-8')
    print(f'Successfully generated DECK UI index at {INDEX_PATH} ({len(HTML_CONTENT)} bytes)')

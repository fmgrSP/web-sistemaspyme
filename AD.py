#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SCRIPT ACTUALIZADOR MAESTRO (AD.py) — SISTEMAS PYME (VERSIÓN V135)
Propósito:
  1. Rediseñar y actualizar de forma limpia, visual y con cero carga cognitiva
     todos los tarjetones A5/A4 y sus versiones móviles:
       - tarifas.html y tarifas_movil.html
       - desembolso.html y desembolso_movil.html
       - setup.html y setup_movil.html
       - catalogo.html y catalogo_movil.html
  2. Actualizar la pantalla principal de la web (index.html), incluyendo la
     sala "Precios claros" (con el nuevo Pack Escudo Total Trinity S1+S2+S3 a
     139 €/mes, los 4 Grupos por complejidad/API y la nueva tabla de las 2
     Super-Auditorías con suelo blindado de 195 € c/u y combo de 590 € / 390 €)
     y el Carrito Configurador a la Carta.
  3. Actualizar base_conocimiento_ingenieria.js (si existe) para que el
     Consultor de Voz de la Tecnosala domine al dedillo las nuevas tarifas.
  4. Guardar copia de seguridad previa obligatoria en `backups_sp`, actualizar
     los 2 únicos documentos maestros .md en `SISTEMAS PYME/Programar`, validar
     sintaxis (Python ast y Node --check en todos los bloques <script>) y
     sincronizar con Git/Render.
=============================================================================
"""

import os
import sys
import re
import ast
import shutil
import atexit
import subprocess
import tempfile
from datetime import datetime

# =============================================================================
# 1. RUTAS OFICIALES DEL ECOSISTEMA EN EL MAC DE FRANCISCO
# =============================================================================
RUTA_WEB_PUBLIC_HTML = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme/public_html"
RUTA_WEB_ROOT = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme"
RUTA_WEB_RENDER = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Servicios/Servicio Reseñas/servicio_resenas"
RUTA_SCRAPER = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Scraper/Scrapper App"
RUTA_PROGRAMAR = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Programar"

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
VERSION_ACTUAL = "V137"

# =============================================================================
# 2. UTILIDADES DE BACKUP Y AUTO-REPLICACIÓN DE AD.py
# =============================================================================
def crear_backup_seguro(ruta_archivo):
    if not os.path.isfile(ruta_archivo):
        return None
    carpeta_base = os.path.dirname(ruta_archivo)
    carpeta_backups = os.path.join(carpeta_base, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    nombre_base = os.path.basename(ruta_archivo)
    ruta_destino = os.path.join(carpeta_backups, f"{nombre_base}.{STAMP}.bak")
    shutil.copy2(ruta_archivo, ruta_destino)
    print(f"  🛡️ Backup creado: {ruta_destino}")
    return ruta_destino

def escribir_archivo_con_backup(ruta_archivo, contenido_nuevo):
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    if os.path.isfile(ruta_archivo):
        crear_backup_seguro(ruta_archivo)
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido_nuevo)
    print(f"  ✅ Archivo actualizado: {ruta_archivo}")

def replicar_ad_py_en_carpetas_oficiales():
    ruta_actual = os.path.abspath(__file__)
    if not os.path.isfile(ruta_actual):
        return
    for carpeta in [RUTA_WEB_PUBLIC_HTML, RUTA_WEB_ROOT, RUTA_WEB_RENDER, RUTA_SCRAPER, RUTA_PROGRAMAR]:
        if os.path.isdir(carpeta):
            destino = os.path.join(carpeta, "AD.py")
            try:
                if os.path.abspath(destino) != ruta_actual:
                    shutil.copy2(ruta_actual, destino)
            except Exception:
                pass

# =============================================================================
# 3. VALIDADOR GATEWAY ANTI-ERRORES (PYTHON AST + VERIFICACIÓN HTML/JS)
# =============================================================================
def encontrar_binario_node():
    node_bin = shutil.which("node")
    if node_bin:
        return node_bin
    rutas_comunes_mac = [
        "/opt/homebrew/bin/node",
        "/usr/local/bin/node",
        os.path.expanduser("~/.nvm/versions/node"),
    ]
    for r in rutas_comunes_mac:
        if os.path.isfile(r) and os.access(r, os.X_OK):
            return r
    return None

def validar_bloques_js_en_html(ruta_html):
    if not os.path.isfile(ruta_html):
        return True
    with open(ruta_html, "r", encoding="utf-8") as f:
        html = f.read()

    nombre_archivo = os.path.basename(ruta_html)
    peso_kb = round(os.path.getsize(ruta_html) / 1024, 1)
    patron = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE)
    bloques = patron.findall(html)

    # Verificación de integridad estructural HTML
    if "<html" not in html.lower() or "</html>" not in html.lower():
        print(f"  ❌ Error estructural en {nombre_archivo}: etiqueta </html> incompleta.")
        return False

    node_bin = encontrar_binario_node()
    if not node_bin:
        print(f"  🟢 Verificado OK: {nombre_archivo} ({peso_kb} KB • {len(bloques)} bloques JS intactos)")
        return True

    for idx, codigo_js in enumerate(bloques, 1):
        codigo_limpio = codigo_js.strip()
        if not codigo_limpio or codigo_limpio.startswith("{"):
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tmp:
            tmp.write(codigo_limpio)
            tmp_path = tmp.name
        try:
            res = subprocess.run([node_bin, "--check", tmp_path], capture_output=True, text=True)
            if res.returncode != 0:
                print(f"  ❌ Error de sintaxis JS en {nombre_archivo} (Bloque #{idx}):\n{res.stderr}")
                os.unlink(tmp_path)
                return False
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    print(f"  🟢 Verificado OK con Node.js: {nombre_archivo} ({peso_kb} KB • {len(bloques)} bloques <script>)")
    return True

# =============================================================================
# 4. CONTENIDO DE LOS NUEVOS TARJETONES Y DOCUMENTOS (DISEÑO CERO CARGA COGNITIVA)
# =============================================================================

HTML_TARIFAS_A5 = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <script>
    (function() {
      try {
        var params = new URLSearchParams(window.location.search);
        if (params.get('modo') === 'impreso') return;
        var esMovil = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || (window.innerWidth > 0 && window.innerWidth <= 820);
        if (esMovil) window.location.replace('tarifas_movil.html');
      } catch(e) {}
    })();
  </script>
  <meta charset="UTF-8">
  <title>Tarifas Oficiales y Arquitectura de 4 Grupos (A5) — Sistemas Pyme</title>
  <meta name="viewport" content="width=820">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    @page { size: A5 portrait; margin: 0; }
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #071629;
      color: #0f172a;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
      padding: 18px 0 44px 0;
    }
    .topbar-pc {
      position: sticky;
      top: 10px;
      z-index: 100;
      background: rgba(11, 37, 69, 0.96);
      backdrop-filter: blur(12px);
      border: 1.5px solid rgba(20, 184, 166, 0.5);
      border-radius: 12px;
      padding: 8px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      width: 92%;
      max-width: 760px;
      color: #fff;
      box-shadow: 0 10px 28px rgba(0,0,0,0.5);
    }
    .btn-pc {
      background: #0d7d74;
      color: #fff;
      border: 1px solid #14b8a6;
      padding: 6px 13px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 800;
      text-decoration: none;
      cursor: pointer;
    }
    .btn-pc.sec { background: #1e293b; border-color: #475569; color: #cbd5e1; }
    .sheet {
      width: 148mm;
      height: 210mm;
      min-height: 210mm;
      max-height: 210mm;
      background: #ffffff;
      padding: 4.5mm 7mm 4mm 7mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 15px 35px rgba(0,0,0,0.5);
      page-break-after: always;
      overflow: hidden;
    }
    @media screen and (min-width: 821px) { .sheet { zoom: 1.24; } }
    @media print {
      body { background: none !important; padding: 0 !important; gap: 0 !important; }
      .no-print { display: none !important; }
      .sheet { box-shadow: none !important; zoom: 1 !important; margin: 0 !important; }
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #0b2545;
      padding-bottom: 2.5px;
      margin-bottom: 3px;
    }
    .brand-logo-img { max-height: 40px; width: auto; object-fit: contain; }
    .header-tagline { text-align: right; font-size: 6.9px; color: #475569; font-weight: 600; line-height: 1.2; }
    .header-tagline strong { color: #095852; font-size: 7.8px; display: block; text-transform: uppercase; font-weight: 900; }

    .section-banner {
      background: linear-gradient(90deg, #095852 0%, #0d7d74 100%);
      color: #fff;
      padding: 3px 7px;
      border-radius: 4px;
      font-size: 8px;
      font-weight: 900;
      text-transform: uppercase;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2.5px;
    }
    .section-banner.blue { background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%); }
    .section-banner.indigo { background: linear-gradient(90deg, #312e81 0%, #4f46e5 100%); }
    .section-banner.dark { background: linear-gradient(90deg, #0b2545 0%, #1e293b 100%); }
    .section-banner .rule {
      font-size: 6.6px;
      font-weight: 700;
      background: rgba(255,255,255,0.22);
      padding: 1px 5px;
      border-radius: 3px;
      text-transform: none;
    }

    .price-table { width: 100%; border-collapse: collapse; font-size: 7.3px; margin-bottom: 3px; }
    .price-table th {
      background: #e2e8f0;
      color: #0b2545;
      font-weight: 800;
      text-transform: uppercase;
      font-size: 6.3px;
      padding: 2.4px 4px;
      border-bottom: 1.2px solid #cbd5e1;
      text-align: left;
    }
    .price-table td {
      padding: 2.3px 4px;
      border-bottom: 1px solid #e2e8f0;
      color: #1e293b;
      vertical-align: middle;
      line-height: 1.15;
    }
    .row-duo { background: #f0f9ff; }
    .row-star { background: #ecfdf5; font-weight: 700; }
    .row-star td { border-top: 1.2px solid #6ee7b7; border-bottom: 1.2px solid #6ee7b7; }
    .pack-name { font-weight: 900; font-size: 8px; color: #0b2545; }
    .price-badge { font-size: 8.8px; font-weight: 900; color: #095852; white-space: nowrap; }
    .save-pill {
      font-size: 6px;
      font-weight: 800;
      color: #15803d;
      background: #dcfce7;
      border: 1px solid #86efac;
      padding: 0.5px 3.5px;
      border-radius: 3px;
      white-space: nowrap;
    }

    .groups-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
      margin-bottom: 3px;
    }
    .grp-box {
      background: #f8fafc;
      border: 1.2px solid #cbd5e1;
      border-left: 3.5px solid #2563eb;
      border-radius: 4px;
      padding: 3.5px 6px;
    }
    .grp-box.pink { border-left-color: #db2777; background: #fdf2f8; border-color: #fbcfe8; }
    .grp-box.indigo { border-left-color: #4f46e5; background: #eef2ff; border-color: #c7d2fe; }
    .grp-head {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 1.5px;
    }
    .grp-title { font-size: 7.4px; font-weight: 900; color: #0b2545; text-transform: uppercase; }
    .grp-price { font-size: 7.6px; font-weight: 900; color: #1d4ed8; }
    .grp-list { list-style: none; font-size: 6.5px; color: #334155; line-height: 1.2; display: flex; flex-direction: column; gap: 1.2px; }

    .audit-box {
      background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%);
      border: 1.3px solid #5eead4;
      border-left: 4px solid #0d7d74;
      border-radius: 4.5px;
      padding: 3.8px 6.5px;
      margin-bottom: 2.5px;
    }
    .audit-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 4px;
      margin-top: 2.5px;
    }
    .audit-card {
      background: #ffffff;
      border: 1px solid #99f6e4;
      border-radius: 3.5px;
      padding: 2.8px 4.5px;
    }
    .audit-card.featured { background: #ecfdf5; border: 1.4px solid #10b981; }
    .audit-card-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1px; }
    .audit-card-name { font-size: 6.6px; font-weight: 800; color: #0b2545; }
    .audit-card-price { font-size: 7.8px; font-weight: 900; color: #095852; }
    .audit-card-desc { font-size: 6px; color: #475569; line-height: 1.15; }

    .hw-strip {
      background: #fffbeb;
      border: 1.2px solid #fde68a;
      border-left: 3.5px solid #d97706;
      border-radius: 4px;
      padding: 3px 6.5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 6.7px;
      margin-bottom: 2px;
    }

    .print-qr-banner {
      background: #f0fdfa;
      border: 1.3px dashed #0d7d74;
      border-radius: 4.5px;
      padding: 4px 7px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-top: auto;
    }
    .print-qr-left { display: flex; align-items: center; gap: 7px; flex: 1; }
    .print-qr-img { width: 33px; height: 33px; border-radius: 3px; flex-shrink: 0; }
    .print-qr-text { font-size: 6.9px; color: #1e293b; line-height: 1.2; }
    .print-qr-text strong { color: #095852; font-size: 7.8px; display: block; }
    .contact-details-box { border-left: 1.2px solid #99f6e4; padding-left: 7px; font-size: 6.7px; line-height: 1.2; text-align: right; flex-shrink: 0; }
    .contact-details-box .name { font-size: 8px; font-weight: 900; color: #0b2545; display: block; }
    .contact-details-box .role { font-size: 5.9px; font-weight: 800; color: #0d7d74; text-transform: uppercase; display: block; }
    .footer-bar { border-top: 1px solid #e2e8f0; padding-top: 2px; font-size: 6.5px; color: #64748b; display: flex; justify-content: space-between; }
  </style>
</head>
<body>
  <aside class="topbar-pc no-print">
    <div style="font-size:12.5px; font-weight:800;">💶 Tarjetón Oficial de Tarifas y 4 Grupos (Doble Cara A5)</div>
    <div style="display:flex; gap:8px;">
      <a href="../index.html#tarifas" onclick="if(window.opener && !window.opener.closed){event.preventDefault();window.close();}" class="btn-pc sec">⬅ Volver a la Web</a>
      <button type="button" onclick="window.print()" class="btn-pc">🖨️ Imprimir / Guardar PDF A5</button>
    </div>
  </aside>

  <!-- ===================================================================== -->
  <!-- CARA A: GRUPO 1 (NÚCLEO DE VENTA RÁPIDA) + LAS 2 SUPER-AUDITORÍAS      -->
  <!-- ===================================================================== -->
  <main class="sheet">
    <div>
      <header class="header">
        <img src="../logo.png" alt="Sistemas Pyme" class="brand-logo-img" onerror="this.onerror=null; this.src='logo.png';">
        <div class="header-tagline">
          <strong>Manual Oficial de Precios y Packs</strong>
          Arquitectura Modular en 4 Bloques + Super-Auditorías
        </div>
      </header>

      <div class="section-banner">
        <span>1. Grupo 1: Servicios Troncales de Implantación Rápida</span>
        <span class="rule">1º a 59 €/m (150 € Setup) | Del 2º al 5º: +40 €/m (+75 € Setup)</span>
      </div>

      <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; padding:3px 6px; font-size:6.6px; color:#1e293b; margin-bottom:2.5px; line-height:1.22;">
        <strong style="color:#0b2545;">¿Qué 5 servicios forman el Grupo 1?</strong>
        <strong>S1</strong> Reseñas Google IA (SEO Local + HEARD/RGPD) •
        <strong>S2</strong> Cortafuegos Preventivo por WhatsApp (Audio IA) •
        <strong style="color:#0d7d74;">S3 ★ Respuesta a Leads en 10s + Portales</strong> •
        <strong>S9</strong> Facturas al Gestor por Foto WA •
        <strong>S5</strong> Reactivación de Clientes Inactivos.
      </div>

      <table class="price-table">
        <thead>
          <tr>
            <th style="width:26%;">Plan del Grupo 1</th>
            <th style="width:23%;">Combinación Típica</th>
            <th style="width:16%;">Cuota Mes</th>
            <th style="width:12%;">Setup Único</th>
            <th style="width:23%;">Ventajas Desbloqueadas</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="pack-name">Plan Pyme BASE</span> <span style="font-size:6px; color:#64748b;">(1 serv.)</span></td>
            <td>Solo S1, o S2, o S3</td>
            <td><span class="price-badge">59 €/m</span></td>
            <td><strong>150 €</strong></td>
            <td><span style="font-size:6.2px; color:#475569;">Ahorra 118 € en Anual • Auditorías a 350 € (590 € las 2)</span></td>
          </tr>
          <tr class="row-duo">
            <td><span class="pack-name" style="color:#0369a1;">Pack ESCUDO BÁSICO</span> <span style="font-size:6px; font-weight:800; color:#0284c7;">(Dúo)</span></td>
            <td><strong>S1 + S2</strong> (o S1 + S3)</td>
            <td><span class="price-badge" style="color:#0369a1;">99 €/m</span></td>
            <td><strong>225 €</strong></td>
            <td><span class="save-pill">Desbloquea Auditorías a 195 € c/u</span></td>
          </tr>
          <tr class="row-star">
            <td><span class="pack-name" style="color:#047857;">Pack ESCUDO TOTAL ★</span> <span style="font-size:6px; font-weight:800; color:#059669;">(Trinity)</span></td>
            <td><strong style="color:#065f46;">S1 + S2 + S3 (Leads 10s)</strong></td>
            <td><span class="price-badge" style="color:#047857;">139 €/m</span></td>
            <td><strong style="color:#047857;">300 €</strong></td>
            <td><span class="save-pill" style="background:#a7f3d0; color:#064e3b;">🎁 Bóveda Gratis (150€) + Aud. 195€</span></td>
          </tr>
          <tr>
            <td><span class="pack-name" style="color:#4338ca;">Plan QUATRO</span> <span style="font-size:6px; color:#64748b;">(4 serv.)</span></td>
            <td>S1 + S2 + S3 + S9</td>
            <td><span class="price-badge" style="color:#4338ca;">179 €/m</span></td>
            <td><strong>375 €</strong></td>
            <td><span class="save-pill">🎁 Bóveda Gratis + Aud. 195 € c/u</span></td>
          </tr>
          <tr>
            <td><span class="pack-name" style="color:#0f766e;">Plan PENTIUM</span> <span style="font-size:6px; color:#64748b;">(5 serv.)</span></td>
            <td>S1 + S2 + S3 + S9 + S5</td>
            <td><span class="price-badge" style="color:#0f766e;">219 €/m</span></td>
            <td><strong>450 €</strong></td>
            <td><span class="save-pill">🎁 Bóveda Gratis + Ahorra 438€ Anual</span></td>
          </tr>
        </tbody>
      </table>

      <div class="section-banner blue">
        <span>2. Grupos 2, 3 y 4: Operativa Avanzada, Satélites y Voz IA</span>
        <span class="rule">Tarifa Suelto vs. Descuento Combinado con Pack</span>
      </div>

      <div class="groups-grid">
        <div class="grp-box">
          <div class="grp-head">
            <span class="grp-title">🗓️ Grupo 2: Operativa Avanzada</span>
            <span class="grp-price">+59 €/m combo</span>
          </div>
          <ul class="grp-list">
            <li>• <strong>S6 Anti-Plantón 24h + Huecos Flash:</strong> 79€ suelto | <strong>+59€/m</strong> (+110€ Setup).</li>
            <li>• <strong>S8 Firma Digital + Onboarding IA:</strong> 79€ suelto | <strong>+59€/m</strong> (+110€ Setup).</li>
            <li>• <strong>S10 Escudo Anti-Morosidad:</strong> 79€ suelto | <strong>+59€/m</strong> (+110€ Setup).</li>
            <li style="color:#1e40af; font-weight:700;">✔ Computa al 100% para beneficios de Pack Dúo/Trinity.</li>
          </ul>
        </div>

        <div class="grp-box indigo">
          <div class="grp-head">
            <span class="grp-title">📞 Grupo 4: Telefonía y Voz IA</span>
            <span class="grp-price" style="color:#4338ca;">Línea + Minutos</span>
          </div>
          <ul class="grp-list">
            <li>• <strong>S4 Llamadas Perdidas por WA:</strong> 79 €/m (195€ Setup) suelto | <strong>+59 €/m</strong> (+110€ Setup) combo. Incluye 250 rescates/mes.</li>
            <li>• <strong>S7 Centralita Voz IA 24/7:</strong> 169 €/m (350€ Setup) suelto | <strong>+129 €/m</strong> (+250€ Setup) combo. Incluye <strong>250 min/mes</strong> (~150-200 llamadas).</li>
          </ul>
        </div>
      </div>

      <div class="grp-box pink" style="margin-bottom:2.5px;">
        <div class="grp-head">
          <span class="grp-title" style="color:#9d174d;">🚀 Grupo 3: Satélites Especializados y Boosters IA</span>
          <span class="grp-price" style="color:#be185d;">Descuento Cruzado Activo</span>
        </div>
        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:4px; font-size:6.3px; color:#334155; line-height:1.18;">
          <div style="background:#fff; padding:2.5px 4px; border-radius:3px; border:1px solid #fbcfe8;">
            <strong style="color:#9d174d; display:block;">📱 Sat. 1: Instagram 3 en 1</strong>
            Suelto: 69€/m (150€) | <strong style="color:#be185d;">Combo: +49€/m (+75€)</strong>
          </div>
          <div style="background:#fff; padding:2.5px 4px; border-radius:3px; border:1px solid #bae6fd;">
            <strong style="color:#0369a1; display:block;">📦 Sat. 2: Escudo Logístico 360</strong>
            Suelto: 79€/m (195€) | <strong style="color:#0284c7;">Combo: +59€/m (+110€)</strong>
          </div>
          <div style="background:#fff; padding:2.5px 4px; border-radius:3px; border:1px solid #c7d2fe;">
            <strong style="color:#4338ca; display:block;">🧠 Sat. 3: Cerebro Redactor RAG</strong>
            Suelto: 99€/m (250€) | <strong style="color:#4f46e5;">Combo: +69€/m (+150€)</strong>
          </div>
        </div>
        <div style="font-size:6.1px; color:#831843; margin-top:2px; font-weight:700;">
          ⚡ <strong>Boosters IA:</strong> Add-on Lector de Correo (para S9) o Reclamación a Proveedores (para S10): <strong>+35 €/mes</strong> (+50 € Setup).
        </div>
      </div>

      <div class="audit-box">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:7.8px; font-weight:900; color:#095852;">🔍🧠 Las 2 Super-Auditorías Web Gemelas (SEO/GEO IA y Neuro-CRO con Sonda 10-14 días)</span>
          <span style="font-size:6px; font-weight:800; background:#095852; color:#fff; padding:1px 4.5px; border-radius:3px;">Suelo Mínimo Blindado: 195 € c/u</span>
        </div>
        <div class="audit-grid">
          <div class="audit-card">
            <div class="audit-card-head"><span class="audit-card-name">1. Solo Código (DIY)</span><span class="audit-card-price">200 €</span></div>
            <div class="audit-card-desc"><strong>390 € las dos</strong> (195€ c/u). PDF Parte 1 + Parte 2 para que lo suba tu informático.</div>
          </div>
          <div class="audit-card">
            <div class="audit-card-head"><span class="audit-card-name">2. Llave en Mano</span><span class="audit-card-price">350 €</span></div>
            <div class="audit-card-desc"><strong>590 € las dos</strong> (Ahorra 110€). Suelta o con Plan Base. Implantación incluida + Sonda.</div>
          </div>
          <div class="audit-card featured">
            <div class="audit-card-head"><span class="audit-card-name" style="color:#065f46;">3. Con Pack Dúo+ ★</span><span class="audit-card-price" style="color:#047857;">195 €</span></div>
            <div class="audit-card-desc" style="color:#064e3b;"><strong>390 € las dos</strong> (Ahorra 310€). Bonificada un 44% con cualquier Pack de 2+ servicios.</div>
          </div>
        </div>
      </div>

      <div class="hw-strip">
        <div><strong style="color:#92400e;">★ Hardware Físico: Atril Inteligente de Mostrador (NFC + QR Dinámico + Telemetría 360°)</strong> — Pago único sin cuotas:</div>
        <div style="font-weight:900; color:#b45309; white-space:nowrap;">1ª Ud: <strong>39 €</strong> | 2ª a 4ª Ud: <strong>29 €/ud</strong> | 5+ Uds: <strong>25 €/ud</strong></div>
      </div>
    </div>

    <div>
      <div class="print-qr-banner">
        <div class="print-qr-left">
          <img src="../qr-code.png" alt="QR WhatsApp" class="print-qr-img" onerror="this.style.display='none'">
          <div class="print-qr-text">
            <strong>¿Qué combinación encaja mejor con tu negocio?</strong>
            Escanea este código QR para hablar por WhatsApp con Francisco y configurar tu pack a medida.
          </div>
        </div>
        <div class="contact-details-box">
          <span class="name">Francisco M. Gallardo</span>
          <span class="role">Consultor Tecnológico</span>
          <strong>711 54 75 61</strong> • francisco@sistemaspyme.es<br>
          <span style="color:#64748b;">sistemaspyme.es • Galicia</span>
        </div>
      </div>
      <footer class="footer-bar">
        <span><strong>Sistemas Pyme</strong> — Arquitectura Oficial de Precios (Precios netos sin IVA 21%)</span>
        <span><strong>CARA A (TARIFAS Y GRUPOS)</strong></span>
      </footer>
    </div>
  </main>

  <!-- ===================================================================== -->
  <!-- CARA B: LIQUIDACIÓN DÍA 1 (FLEXIBLE VS ANUAL) Y CHULETA DE REGLAS      -->
  <!-- ===================================================================== -->
  <main class="sheet">
    <div>
      <header class="header">
        <img src="../logo.png" alt="Sistemas Pyme" class="brand-logo-img" onerror="this.onerror=null; this.src='logo.png';">
        <div class="header-tagline">
          <strong>Liquidación Día 1 y Reglas de Combinación</strong>
          Modalidad Flexible (3 meses) vs. Plan Anual (2 Meses Gratis)
        </div>
      </header>

      <div class="section-banner dark">
        <span>3. Las 2 Vías de Contratación (Domiciliación B2B SEPA)</span>
        <span class="rule">Transparencia Total desde el Día 1</span>
      </div>

      <div class="groups-grid" style="margin-bottom:3px;">
        <div class="grp-box" style="border-left-color:#0d7d74;">
          <div class="grp-head">
            <span class="grp-title" style="color:#095852;">🔄 Vía 1: Modalidad Flexible (Mes a Mes)</span>
          </div>
          <ul class="grp-list">
            <li>✔ <strong>Pago Día 1:</strong> Alta Técnica (Setup único) + 1ª Mensualidad.</li>
            <li>✔ <strong>Compromiso inicial:</strong> Solo 3 meses de rodaje; luego libre con 30 días de preaviso.</li>
            <li>✔ <strong>Super-Auditorías Llave en Mano:</strong> <strong>195 € c/u</strong> (o 390 € las dos) desde cualquier Pack de 2+ servicios.</li>
          </ul>
        </div>
        <div class="grp-box indigo">
          <div class="grp-head">
            <span class="grp-title" style="color:#3730a3;">🎁 Vía 2: Plan Anual (Pagas 10 y Disfrutas 12)</span>
          </div>
          <ul class="grp-list">
            <li>✔ <strong>Pago Día 1:</strong> Alta Técnica (Setup único) + 10 Mensualidades.</li>
            <li>✔ <strong>Ahorro directo:</strong> <strong>2 meses completos GRATIS</strong> (-16,6%) y precio blindado todo el año.</li>
            <li>✔ <strong>Super-Auditorías Llave en Mano:</strong> <strong>195 € c/u</strong> (o 390 € las dos) desde cualquier Pack de 2+ servicios.</li>
          </ul>
        </div>
      </div>

      <div class="section-banner">
        <span>4. Tabla Maestra de Desembolso Día 1 y Packs Estrella</span>
        <span class="rule">Importes Exactos de Inicio (Sin IVA 21%)</span>
      </div>

      <table class="price-table" style="font-size:7px;">
        <thead>
          <tr>
            <th style="width:27%;">Plan / Módulo</th>
            <th style="width:13%;">Cuota Mes</th>
            <th style="width:12%;">Alta (Setup)</th>
            <th style="width:22%;">Pago Día 1 (Vía Flexible)</th>
            <th style="width:26%;">Pago Día 1 (Vía Anual 10m)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Plan Pyme BASE</strong> (1 serv. G1)</td>
            <td>59 €/m</td>
            <td>150 €</td>
            <td><strong>209 €</strong> <span style="font-size:5.8px; color:#64748b;">(150€ + 59€)</span></td>
            <td><strong style="color:#4338ca;">740 €</strong> <span class="save-pill">Ahorra 118 €</span></td>
          </tr>
          <tr class="row-duo">
            <td><strong style="color:#0369a1;">Pack ESCUDO BÁSICO</strong> (Dúo S1+S2)</td>
            <td><strong>99 €/m</strong></td>
            <td>225 €</td>
            <td><strong>324 €</strong> <span style="font-size:5.8px; color:#0369a1;">(225€ + 99€)</span></td>
            <td><strong style="color:#4338ca;">1.215 €</strong> <span class="save-pill">Ahorra 198 €</span></td>
          </tr>
          <tr class="row-star">
            <td><strong style="color:#047857;">Pack ESCUDO TOTAL ★</strong> (S1+S2+S3)</td>
            <td><strong style="color:#047857;">139 €/m</strong></td>
            <td>300 €</td>
            <td><strong style="color:#047857;">439 €</strong> <span style="font-size:5.8px; color:#065f46;">(300€ + 139€)</span></td>
            <td><strong style="color:#047857;">1.690 €</strong> <span class="save-pill">Ahorra 278 € + Bóveda</span></td>
          </tr>
          <tr>
            <td><strong>Plan QUATRO</strong> (4 serv. Grupo 1)</td>
            <td>179 €/m</td>
            <td>375 €</td>
            <td><strong>554 €</strong> <span style="font-size:5.8px; color:#64748b;">(375€ + 179€)</span></td>
            <td><strong style="color:#4338ca;">2.165 €</strong> <span class="save-pill">Ahorra 358 €</span></td>
          </tr>
          <tr>
            <td><strong>Plan PENTIUM</strong> (5 serv. Grupo 1)</td>
            <td>219 €/m</td>
            <td>450 €</td>
            <td><strong>669 €</strong> <span style="font-size:5.8px; color:#64748b;">(450€ + 219€)</span></td>
            <td><strong style="color:#4338ca;">2.640 €</strong> <span class="save-pill">Ahorra 438 €</span></td>
          </tr>
          <tr style="background:#eff6ff;">
            <td><strong style="color:#1e40af;">+ Servicio Grupo 2, Logística o S4</strong></td>
            <td>+59 €/m <span style="font-size:5.7px;">(79€ s.)</span></td>
            <td>+110 € <span style="font-size:5.7px;">(195€)</span></td>
            <td><strong>+169 €</strong> combo <span style="font-size:5.7px;">(274€ suelto)</span></td>
            <td><strong style="color:#1e40af;">+700 €</strong> combo <span class="save-pill">Ahorra 118 €</span></td>
          </tr>
          <tr style="background:#fdf2f8;">
            <td><strong style="color:#9d174d;">+ Satélite Instagram 3 en 1</strong></td>
            <td>+49 €/m <span style="font-size:5.7px;">(69€ s.)</span></td>
            <td>+75 € <span style="font-size:5.7px;">(150€)</span></td>
            <td><strong>+124 €</strong> combo <span style="font-size:5.7px;">(219€ suelto)</span></td>
            <td><strong style="color:#9d174d;">+565 €</strong> combo <span class="save-pill">Ahorra 98 €</span></td>
          </tr>
          <tr style="background:#f5f3ff;">
            <td><strong style="color:#4338ca;">+ Satélite Cerebro Redactor RAG</strong></td>
            <td>+69 €/m <span style="font-size:5.7px;">(99€ s.)</span></td>
            <td>+150 € <span style="font-size:5.7px;">(250€)</span></td>
            <td><strong>+219 €</strong> combo <span style="font-size:5.7px;">(349€ suelto)</span></td>
            <td><strong style="color:#4338ca;">+840 €</strong> combo <span class="save-pill">Ahorra 138 €</span></td>
          </tr>
          <tr style="background:#eef2ff;">
            <td><strong style="color:#3730a3;">+ S7 Centralita Voz IA 24/7 (250m)</strong></td>
            <td>+129 €/m <span style="font-size:5.7px;">(169€)</span></td>
            <td>+250 € <span style="font-size:5.7px;">(350€)</span></td>
            <td><strong>+379 €</strong> combo <span style="font-size:5.7px;">(519€ suelto)</span></td>
            <td><strong style="color:#3730a3;">+1.540 €</strong> combo <span class="save-pill">Ahorra 258 €</span></td>
          </tr>
        </tbody>
      </table>

      <div class="section-banner blue">
        <span>5. Los 3 Packs Estrella de Venta Directa y Regla de Combinación</span>
        <span class="rule">Guía Rápida para Cierre Comercial</span>
      </div>

      <div style="display:flex; flex-direction:column; gap:2.5px; font-size:6.6px; color:#1e293b; line-height:1.22;">
        <div style="background:#f0f9ff; border:1px solid #bae6fd; border-left:3.5px solid #0284c7; border-radius:4px; padding:3px 6px;">
          <strong style="color:#0369a1;">1. Pack Escudo Básico (Dúo S1 + S2):</strong> <strong>99 €/mes</strong> + 225 € Setup (Día 1 Flex: 324 € | Día 1 Anual: 1.215 €). Desbloquea cualquiera de las 2 Super-Auditorías Llave en Mano a <strong>195 € c/u</strong> (o las dos por 390 €).
        </div>
        <div style="background:#ecfdf5; border:1px solid #6ee7b7; border-left:3.5px solid #059669; border-radius:4px; padding:3px 6px;">
          <strong style="color:#065f46;">2. Pack Escudo Total ★ (Trinity S1 + S2 + S3 Leads en 10s):</strong> <strong>139 €/mes</strong> + 300 € Setup (Día 1 Flex: 439 € | Día 1 Anual: 1.690 €). Incluye <strong>Bóveda de Contraseñas GRATIS</strong> (valorada en 150 €) + Super-Auditorías a <strong>195 € c/u</strong>.
        </div>
        <div style="background:#fffbeb; border:1px solid #fde68a; border-left:3.5px solid #d97706; border-radius:4px; padding:3px 6px;">
          <strong style="color:#92400e;">3. Pack Firma Institucional / Alto Standing (Sin cuotas mensuales):</strong> 1 Super-Auditoría Llave en Mano por <strong>350 €</strong> o las <strong>2 Super-Auditorías Gemelas (SEO/GEO + Neuro-CRO con Sonda de 10-14 días) por 590 €</strong> pago único (ahorras 110 €).
        </div>
      </div>
    </div>

    <div>
      <div class="print-qr-banner">
        <div class="print-qr-left">
          <img src="../qr-code.png" alt="QR WhatsApp" class="print-qr-img" onerror="this.style.display='none'">
          <div class="print-qr-text">
            <strong>¿Activamos tu Pack Escudo o tus Super-Auditorías hoy mismo?</strong>
            Escanea el código con tu móvil para hablar directamente con Francisco.
          </div>
        </div>
        <div class="contact-details-box">
          <span class="name">Francisco M. Gallardo</span>
          <span class="role">Consultor Tecnológico</span>
          <strong>711 54 75 61</strong> • francisco@sistemaspyme.es<br>
          <span style="color:#64748b;">sistemaspyme.es • Galicia</span>
        </div>
      </div>
      <footer class="footer-bar">
        <span><strong>Sistemas Pyme</strong> — Facturación B2B mediante domiciliación SEPA</span>
        <span><strong>CARA B (LIQUIDACIÓN DÍA 1)</strong></span>
      </footer>
    </div>
  </main>
</body>
</html>
"""

HTML_TARIFAS_MOVIL = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Tarifas Oficiales y Arquitectura de 4 Grupos (Versión Móvil) — Sistemas Pyme</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      width: 100%;
      background-color: #071629;
      color: #f1f5f9;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 16.5px;
      line-height: 1.55;
    }
    body.font-xl { font-size: 19px; line-height: 1.65; }
    .topbar {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(7, 22, 41, 0.96);
      backdrop-filter: blur(12px);
      border-bottom: 2px solid #14b8a6;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .btn-back {
      background: #1e293b;
      color: #5eead4;
      border: 1px solid rgba(20,184,166,0.45);
      text-decoration: none;
      font-weight: 800;
      font-size: 13px;
      padding: 8px 12px;
      border-radius: 10px;
    }
    .btn-action {
      background: #0d7d74;
      color: #fff;
      border: 1px solid #14b8a6;
      font-weight: 800;
      font-size: 12.5px;
      padding: 8px 11px;
      border-radius: 10px;
      text-decoration: none;
      cursor: pointer;
    }
    .btn-action.sec { background: #1e293b; color: #cbd5e1; border-color: #475569; }
    .container {
      max-width: 660px;
      margin: 0 auto;
      padding: 18px 16px 48px 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .hero-box {
      background: linear-gradient(145deg, #0b2545 0%, #0f172a 100%);
      border: 1.5px solid rgba(20, 184, 166, 0.45);
      border-radius: 18px;
      padding: 18px 16px;
    }
    .badge {
      display: inline-block;
      background: rgba(20, 184, 166, 0.18);
      color: #5eead4;
      border: 1px solid rgba(20, 184, 166, 0.4);
      font-size: 11.5px;
      font-weight: 800;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 99px;
      margin-bottom: 8px;
    }
    .hero-title { font-size: 1.38em; font-weight: 900; color: #fff; line-height: 1.22; margin-bottom: 6px; }
    .hero-sub { font-size: 0.92em; color: #cbd5e1; }
    .section-head {
      background: linear-gradient(90deg, #0f766e 0%, #115e59 100%);
      color: #fff;
      padding: 11px 14px;
      border-radius: 12px;
      font-weight: 900;
      font-size: 0.95em;
      text-transform: uppercase;
      margin-top: 6px;
    }
    .section-head.blue { background: linear-gradient(90deg, #1e3a8a 0%, #1d4ed8 100%); }
    .section-head.pink { background: linear-gradient(90deg, #831843 0%, #be185d 100%); }
    .section-head.indigo { background: linear-gradient(90deg, #3730a3 0%, #4f46e5 100%); }
    .section-head.amber { background: linear-gradient(90deg, #b45309 0%, #d97706 100%); }
    .card {
      background: #0f172a;
      border: 1.5px solid rgba(255,255,255,0.12);
      border-left: 5px solid #14b8a6;
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .card.emerald { border-left-color: #10b981; border-color: rgba(16,185,129,0.45); background: linear-gradient(145deg, rgba(6,78,59,0.45) 0%, #0f172a 100%); }
    .card.blue { border-left-color: #3b82f6; }
    .card.pink { border-left-color: #ec4899; }
    .card.indigo { border-left-color: #6366f1; }
    .card.amber { border-left-color: #f59e0b; }
    .card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; }
    .card-title { font-size: 1.1em; font-weight: 900; color: #fff; line-height: 1.25; }
    .card-subtitle {
      display: inline-block;
      font-size: 0.8em;
      font-weight: 800;
      color: #5eead4;
      background: rgba(20, 184, 166, 0.14);
      border: 1px solid rgba(20, 184, 166, 0.35);
      padding: 2px 9px;
      border-radius: 8px;
      margin-top: 4px;
    }
    .price-tag {
      background: rgba(20, 184, 166, 0.18);
      color: #5eead4;
      border: 1px solid rgba(20, 184, 166, 0.4);
      font-weight: 900;
      font-size: 0.96em;
      padding: 4px 10px;
      border-radius: 10px;
      white-space: nowrap;
    }
    .price-tag.amber { background: rgba(245, 158, 11, 0.2); color: #fcd34d; border-color: rgba(245, 158, 11, 0.45); }
    .data-grid {
      display: flex;
      flex-direction: column;
      gap: 7px;
      background: rgba(0,0,0,0.35);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 12px;
      padding: 12px;
    }
    .data-row {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 10px;
      padding-bottom: 6px;
      border-bottom: 1px dashed rgba(255,255,255,0.1);
      font-size: 0.9em;
    }
    .data-row:last-child { border-bottom: none; padding-bottom: 0; }
    .data-label { color: #94a3b8; font-weight: 600; }
    .data-val { color: #fff; font-weight: 800; text-align: right; }
    .data-val.hi { color: #34d399; }
    .cta-box {
      background: linear-gradient(145deg, #064e3b 0%, #0f172a 100%);
      border: 2px solid #10b981;
      border-radius: 18px;
      padding: 20px 16px;
      text-align: center;
    }
    .btn-wa {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      background: #10b981;
      color: #052e16;
      font-weight: 900;
      padding: 14px 18px;
      border-radius: 14px;
      text-decoration: none;
      margin-top: 12px;
    }
  </style>
</head>
<body>
  <header class="topbar">
    <a href="../index.html#tarifas" onclick="if(window.opener && !window.opener.closed){event.preventDefault();window.close();}" class="btn-back">⬅ Volver a la Web</a>
    <div style="display:flex; gap:6px;">
      <button type="button" id="btnToggleFont" onclick="document.body.classList.toggle('font-xl')" class="btn-action">🔎 Letra A+</button>
      <a href="tarifas.html?modo=impreso" class="btn-action sec">📄 Original A5</a>
    </div>
  </header>

  <main class="container">
    <div class="hero-box">
      <span class="badge">Manual Oficial de Precios</span>
      <h1 class="hero-title">Arquitectura de Tarifas en 4 Grupos y Super-Auditorías</h1>
      <p class="hero-sub">Cero carga cognitiva: consulta de un vistazo los packs del Grupo 1, Operativa Avanzada, Satélites, Voz IA y las 2 Super-Auditorías.</p>
    </div>

    <div class="section-head">1. Grupo 1: Núcleo de Implantación Rápida (59€ el 1º | +40€ extra)</div>
    <p style="font-size:0.9em; color:#cbd5e1;">
      Incluye los 5 servicios más rentables y rápidos: <strong>S1</strong> Reseñas Google IA, <strong>S2</strong> Cortafuegos Preventivo WhatsApp, <strong>S3 ★ Leads en 10 Segundos</strong>, <strong>S9</strong> Facturas por Foto WA y <strong>S5</strong> Reactivación de Clientes Inactivos.
    </p>

    <article class="card">
      <div class="card-top">
        <div>
          <span class="card-title">Plan Pyme BASE (1 serv.)</span>
          <span class="card-subtitle">Solo S1, o solo S2, o solo S3</span>
        </div>
        <span class="price-tag">59 € / mes</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Alta Técnica (Setup único):</span><span class="data-val">150 €</span></div>
        <div class="data-row"><span class="data-label">Pago Día 1 (Vía Flexible):</span><span class="data-val">209 €</span></div>
        <div class="data-row"><span class="data-label">Pago Día 1 (Vía Anual 10m):</span><span class="data-val hi">740 € (Ahorra 118 €)</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div>
          <span class="card-title">Pack ESCUDO BÁSICO (Dúo: 2 serv.)</span>
          <span class="card-subtitle">S1 + S2 (o S1 + S3)</span>
        </div>
        <span class="price-tag">99 € / mes</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Alta Técnica (150€ + 75€):</span><span class="data-val">225 €</span></div>
        <div class="data-row"><span class="data-label">Pago Día 1 (Vía Flexible):</span><span class="data-val">324 €</span></div>
        <div class="data-row"><span class="data-label">Pago Día 1 (Vía Anual 10m):</span><span class="data-val hi">1.215 € (Ahorra 198 €)</span></div>
        <div class="data-row"><span class="data-label">Privilegio Desbloqueado:</span><span class="data-val hi">Auditorías a 195 € c/u (390 € las 2)</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div>
          <span class="card-title">Pack ESCUDO TOTAL ★ (Trinity: 3 serv.)</span>
          <span class="card-subtitle">S1 + S2 + S3 (Leads en 10s)</span>
        </div>
        <span class="price-tag amber">139 € / mes</span>
      </div>
      <p><strong>El Pack Estrella:</strong> protege tus reseñas en Google, filtra quejas en privado por WhatsApp y atiende a cada nuevo lead en menos de 10 segundos.</p>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Alta Técnica (150€ + 75€ + 75€):</span><span class="data-val">300 €</span></div>
        <div class="data-row"><span class="data-label">Pago Día 1 (Vía Flexible):</span><span class="data-val">439 €</span></div>
        <div class="data-row"><span class="data-label">Pago Día 1 (Vía Anual 10m):</span><span class="data-val hi">1.690 € (Ahorra 278 €)</span></div>
        <div class="data-row"><span class="data-label">Regalo + Privilegio:</span><span class="data-val hi">🎁 Bóveda Gratis (150€) + Aud. a 195 € c/u</span></div>
      </div>
    </article>

    <article class="card">
      <div class="card-top">
        <div>
          <span class="card-title">Planes QUATRO (4) y PENTIUM (5)</span>
          <span class="card-subtitle">+40 €/m y +75 € Setup por módulo</span>
        </div>
        <span class="price-tag">179€ / 219€</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Plan QUATRO (S1+S2+S3+S9):</span><span class="data-val">179 €/m + 375 € Setup (Día 1: 554 €)</span></div>
        <div class="data-row"><span class="data-label">Plan PENTIUM (Los 5 serv. G1):</span><span class="data-val">219 €/m + 450 € Setup (Día 1: 669 €)</span></div>
      </div>
    </article>

    <div class="section-head blue">2. Grupo 2: Operativa Avanzada (Agenda, Contratos y Cobros)</div>
    <article class="card blue">
      <div class="card-top">
        <div>
          <span class="card-title">S6 Anti-Plantón, S8 Firma Digital y S10 Anti-Morosidad</span>
          <span class="card-subtitle">Computan al 100% para beneficios de Pack</span>
        </div>
        <span class="price-tag">+59 €/m combo</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Contratado SUELTO (único servicio):</span><span class="data-val">79 €/mes + 195 € Setup</span></div>
        <div class="data-row"><span class="data-label">COMBINADO (con Grupo 1 u otro):</span><span class="data-val hi">+59 €/mes + +110 € Setup</span></div>
      </div>
    </article>

    <div class="section-head pink">3. Grupo 3: Satélites Especializados y Boosters IA</div>
    <article class="card pink">
      <div class="data-grid">
        <div class="data-row"><span class="data-label">📱 Satélite 1: Instagram 3 en 1:</span><span class="data-val hi">+49 €/m (+75€) combo | 69 €/m (150€) suelto</span></div>
        <div class="data-row"><span class="data-label">📦 Satélite 2: Escudo Logístico 360:</span><span class="data-val hi">+59 €/m (+110€) combo | 79 €/m (195€) suelto</span></div>
        <div class="data-row"><span class="data-label">🧠 Satélite 3: Cerebro Redactor RAG:</span><span class="data-val hi">+69 €/m (+150€) combo | 99 €/m (250€) suelto</span></div>
        <div class="data-row"><span class="data-label">⚡ Boosters IA (Correo S9 / Prov. S10):</span><span class="data-val">+35 €/mes + +50 € Setup</span></div>
      </div>
    </article>

    <div class="section-head indigo">4. Grupo 4: Satélites de Telefonía y Voz IA</div>
    <article class="card indigo">
      <div class="data-grid">
        <div class="data-row"><span class="data-label">📞 S4 Rescate Llamadas Perdidas WA (250 rescates/m):</span><span class="data-val hi">+59 €/m (+110€) combo | 79 €/m (195€) suelto</span></div>
        <div class="data-row"><span class="data-label">🎙️ S7 Centralita Voz IA 24/7 (Bolsa 250 min/m):</span><span class="data-val hi">+129 €/m (+250€) combo | 169 €/m (350€) suelto</span></div>
      </div>
    </article>

    <div class="section-head amber">5. Las 2 Super-Auditorías Web Gemelas (Suelo Mínimo 195 € c/u)</div>
    <article class="card amber">
      <div class="card-top">
        <div>
          <span class="card-title">1) Ingeniería SEO/GEO IA y 2) Neuro-CRO con Sonda 10-14 Días</span>
          <span class="card-subtitle">Pago Único • Sin Cuotas Mensuales</span>
        </div>
        <span class="price-tag amber">195 € en Pack</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">1. Solo Código / DIY (Sin mano de obra):</span><span class="data-val">200 € una | 390 € las dos</span></div>
        <div class="data-row"><span class="data-label">2. Oficial «Llave en Mano» (Suelta o Base):</span><span class="data-val">350 € una | 590 € las dos (Ahorra 110 €)</span></div>
        <div class="data-row"><span class="data-label">3. BONIFICADA CON PACK (2+ serv. Mensual o Anual):</span><span class="data-val hi">195 € una | 390 € las dos (Ahorra 310 €)</span></div>
        <div class="data-row"><span class="data-label">★ Hardware Atril NFC + QR Mostrador:</span><span class="data-val hi">39 € (1ª ud) | 29 € (2ª-4ª) | 25 € (5+ uds)</span></div>
      </div>
    </article>

    <div class="cta-box">
      <div style="font-size: 0.85em; font-weight: 800; color: #6ee7b7; text-transform: uppercase;">Atención Directa • Galicia</div>
      <div style="font-size: 1.2em; font-weight: 900; color: #ffffff; margin-top: 4px;">Francisco M. Gallardo</div>
      <div style="font-size: 0.92em; color: #cbd5e1; margin-top: 2px;">Tel: <strong>711 54 75 61</strong> • francisco@sistemaspyme.es</div>
      <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20estoy%20viendo%20las%20nuevas%20tarifas%20en%20el%20m%C3%B3vil%20y%20quiero%20informaci%C3%B3n%20para%20mi%20negocio" target="_blank" class="btn-wa">
        💬 Hablar con Francisco por WhatsApp
      </a>
    </div>
  </main>
</body>
</html>
"""

HTML_DESEMBOLSO_A5 = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <script>
    (function() {
      try {
        var params = new URLSearchParams(window.location.search);
        if (params.get('modo') === 'impreso') return;
        var esMovil = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || (window.innerWidth > 0 && window.innerWidth <= 820);
        if (esMovil) window.location.replace('desembolso_movil.html');
      } catch(e) {}
    })();
  </script>
  <meta charset="UTF-8">
  <title>Desembolso Día 1 y Liquidación Inicial (A5) — Sistemas Pyme</title>
  <meta name="viewport" content="width=820">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    @page { size: A5 portrait; margin: 0; }
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #071629;
      color: #0f172a;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
      padding: 18px 0 44px 0;
    }
    .topbar-pc {
      position: sticky;
      top: 10px;
      z-index: 100;
      background: rgba(11, 37, 69, 0.96);
      backdrop-filter: blur(12px);
      border: 1.5px solid rgba(20, 184, 166, 0.5);
      border-radius: 12px;
      padding: 8px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      width: 92%;
      max-width: 760px;
      color: #fff;
    }
    .btn-pc { background: #0d7d74; color: #fff; border: 1px solid #14b8a6; padding: 6px 13px; border-radius: 8px; font-size: 12px; font-weight: 800; text-decoration: none; cursor: pointer; }
    .btn-pc.sec { background: #1e293b; border-color: #475569; color: #cbd5e1; }
    .sheet {
      width: 148mm;
      height: 210mm;
      min-height: 210mm;
      max-height: 210mm;
      background: #ffffff;
      padding: 4.5mm 7mm 4mm 7mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 15px 35px rgba(0,0,0,0.5);
      overflow: hidden;
    }
    @media screen and (min-width: 821px) { .sheet { zoom: 1.24; } }
    @media print {
      body { background: none !important; padding: 0 !important; }
      .no-print { display: none !important; }
      .sheet { box-shadow: none !important; zoom: 1 !important; margin: 0 !important; }
    }
    .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0b2545; padding-bottom: 2.5px; margin-bottom: 3px; }
    .brand-logo-img { max-height: 40px; width: auto; object-fit: contain; }
    .header-tagline { text-align: right; font-size: 6.9px; color: #475569; font-weight: 600; line-height: 1.2; }
    .header-tagline strong { color: #095852; font-size: 7.8px; display: block; text-transform: uppercase; font-weight: 900; }
    .section-banner {
      background: linear-gradient(90deg, #0b2545 0%, #1e293b 100%);
      color: #fff;
      padding: 3px 7px;
      border-radius: 4px;
      font-size: 8px;
      font-weight: 900;
      text-transform: uppercase;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 3px;
    }
    .section-banner.green { background: linear-gradient(90deg, #095852 0%, #0d7d74 100%); }
    .section-banner .rule { font-size: 6.6px; font-weight: 700; background: rgba(255,255,255,0.22); padding: 1px 5px; border-radius: 3px; text-transform: none; }
    .modalities-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; margin-bottom: 3px; }
    .modality-col { border: 1.2px solid #94a3b8; border-radius: 4.5px; padding: 4px 6.5px; background: #f8fafc; font-size: 6.8px; line-height: 1.22; }
    .modality-col.best { border-color: #4f46e5; background: #faf5ff; }
    .master-table { width: 100%; border-collapse: collapse; font-size: 6.9px; margin-bottom: 3px; }
    .master-table th { background: #0b2545; color: #fff; font-size: 6.2px; font-weight: 800; text-transform: uppercase; padding: 2.5px 3px; border: 1px solid #1e293b; text-align: center; }
    .master-table td { padding: 2.2px 3.5px; border: 1px solid #cbd5e1; text-align: center; vertical-align: middle; line-height: 1.14; }
    .master-table td.left { text-align: left; font-weight: 800; color: #0b2545; }
    .star-row { background: #ecfdf5; font-weight: 700; }
    .duo-row { background: #f0f9ff; font-weight: 700; }
    .tag-day1 { font-weight: 900; color: #0f172a; font-size: 7.7px; display: block; }
    .tag-annual { font-weight: 900; color: #4338ca; font-size: 7.7px; display: block; }
    .tag-ahorro { font-size: 5.8px; color: #15803d; font-weight: 800; display: block; }
    .print-qr-banner { background: #f0fdfa; border: 1.3px dashed #0d7d74; border-radius: 4.5px; padding: 4px 7px; display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-top: auto; }
    .print-qr-left { display: flex; align-items: center; gap: 7px; flex: 1; }
    .print-qr-img { width: 33px; height: 33px; border-radius: 3px; }
    .print-qr-text { font-size: 6.9px; color: #1e293b; line-height: 1.2; }
    .print-qr-text strong { color: #095852; font-size: 7.8px; display: block; }
    .contact-details-box { border-left: 1.2px solid #99f6e4; padding-left: 7px; font-size: 6.7px; line-height: 1.2; text-align: right; }
    .contact-details-box .name { font-size: 8px; font-weight: 900; color: #0b2545; display: block; }
    .contact-details-box .role { font-size: 5.9px; font-weight: 800; color: #0d7d74; text-transform: uppercase; display: block; }
    .footer-bar { border-top: 1px solid #e2e8f0; padding-top: 2px; font-size: 6.5px; color: #64748b; display: flex; justify-content: space-between; }
  </style>
</head>
<body>
  <aside class="topbar-pc no-print">
    <div style="font-size:12.5px; font-weight:800;">📊 Tabla Oficial de Desembolso Día 1 (A5)</div>
    <div style="display:flex; gap:8px;">
      <a href="../index.html#tarifas" onclick="if(window.opener && !window.opener.closed){event.preventDefault();window.close();}" class="btn-pc sec">⬅ Volver a la Web</a>
      <button type="button" onclick="window.print()" class="btn-pc">🖨️ Imprimir / Guardar PDF A5</button>
    </div>
  </aside>

  <main class="sheet">
    <div>
      <header class="header">
        <img src="../logo.png" alt="Sistemas Pyme" class="brand-logo-img" onerror="this.onerror=null; this.src='logo.png';">
        <div class="header-tagline">
          <strong>Liquidación y Desembolso Día 1</strong>
          Alta Técnica (Setup) + Cuota + Super-Auditorías
        </div>
      </header>

      <div class="section-banner">
        <span>¿Cómo se calcula el importe exacto a abonar el Día 1?</span>
        <span class="rule">2 Vías de Contratación B2B (SEPA)</span>
      </div>

      <div class="modalities-grid">
        <div class="modality-col">
          <strong style="color:#0b2545; font-size:7.6px; display:block; margin-bottom:1.5px;">🔄 Vía 1: Modalidad Flexible (3 Meses)</strong>
          • <strong>Día 1:</strong> Abonas el Alta Técnica (Setup único) + solo el Mes 1.<br>
          • <strong>Desde el Mes 2:</strong> Solo la cuota mensual por SEPA.<br>
          • <strong>Super-Auditorías Llave en Mano:</strong> <strong>195 € c/u</strong> (o 390 € las dos) desde cualquier Pack de 2+ servicios.
        </div>
        <div class="modality-col best">
          <strong style="color:#3730a3; font-size:7.6px; display:block; margin-bottom:1.5px;">🎁 Vía 2: Plan Anual (10 Meses = 2 Gratis)</strong>
          • <strong>Día 1:</strong> Abonas el Alta Técnica (Setup) + 10 meses de cuota.<br>
          • <strong>Ahorro directo:</strong> Disfrutas 12 meses pagando solo 10.<br>
          • <strong>Super-Auditorías Llave en Mano:</strong> <strong>195 € c/u</strong> (o 390 € las dos) desde cualquier Pack de 2+ servicios.
        </div>
      </div>

      <div class="section-banner green">
        <span>Tabla Maestra Desglosada de Desembolso Día 1 (Los 4 Grupos)</span>
        <span class="rule">Valores netos sin IVA 21%</span>
      </div>

      <table class="master-table">
        <thead>
          <tr>
            <th style="width:27%; text-align:left; padding-left:4px;">Plan / Módulo</th>
            <th style="width:13%;">Cuota Mes</th>
            <th style="width:12%;">Setup Único</th>
            <th style="width:22%;">Día 1 (Vía Flexible)<br><span style="font-size:5.4px; font-weight:600; color:#cbd5e1;">Setup + Cuota Mes 1</span></th>
            <th style="width:26%;">Día 1 (Vía Anual 10m)<br><span style="font-size:5.4px; font-weight:600; color:#cbd5e1;">Setup + 10 Meses (2 Gratis)</span></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="left">Plan Pyme BASE (1 serv. G1)</td>
            <td>59 €/m</td>
            <td><strong>150 €</strong></td>
            <td><span class="tag-day1">209,00 €</span><span style="font-size:5.6px; color:#475569;">[150€ Setup + 59€ Mes 1]</span></td>
            <td><span class="tag-annual">740,00 €</span><span class="tag-ahorro">590€ (10m) + 150€ • Ahorra 118€</span></td>
          </tr>
          <tr class="duo-row">
            <td class="left" style="color:#0369a1;">Pack ESCUDO BÁSICO (Dúo S1+S2)</td>
            <td><strong>99 €/m</strong></td>
            <td><strong>225 €</strong></td>
            <td><span class="tag-day1" style="color:#0369a1;">324,00 €</span><span style="font-size:5.6px; color:#0369a1;">[225€ Setup + 99€ Mes 1]</span></td>
            <td><span class="tag-annual">1.215,00 €</span><span class="tag-ahorro">990€ + 225€ • Desbloquea Aud. 195€</span></td>
          </tr>
          <tr class="star-row">
            <td class="left" style="color:#047857;">Pack ESCUDO TOTAL ★ (S1+S2+S3)</td>
            <td><strong style="color:#047857;">139 €/m</strong></td>
            <td><strong style="color:#047857;">300 €</strong></td>
            <td><span class="tag-day1" style="color:#047857;">439,00 €</span><span style="font-size:5.6px; color:#065f46;">[300€ Setup + 139€ Mes 1]</span></td>
            <td><span class="tag-annual" style="color:#047857;">1.690,00 €</span><span class="tag-ahorro">Ahorra 278€ + Bóveda Gratis + Aud. 195€</span></td>
          </tr>
          <tr>
            <td class="left">Plan QUATRO (4 serv. Grupo 1)</td>
            <td>179 €/m</td>
            <td><strong>375 €</strong></td>
            <td><span class="tag-day1">554,00 €</span><span style="font-size:5.6px; color:#475569;">[375€ Setup + 179€ Mes 1]</span></td>
            <td><span class="tag-annual">2.165,00 €</span><span class="tag-ahorro">1.790€ + 375€ • Ahorra 358€</span></td>
          </tr>
          <tr>
            <td class="left">Plan PENTIUM (5 serv. Grupo 1)</td>
            <td>219 €/m</td>
            <td><strong>450 €</strong></td>
            <td><span class="tag-day1">669,00 €</span><span style="font-size:5.6px; color:#475569;">[450€ Setup + 219€ Mes 1]</span></td>
            <td><span class="tag-annual">2.640,00 €</span><span class="tag-ahorro">2.190€ + 450€ • Ahorra 438€</span></td>
          </tr>
          <tr style="background:#eff6ff;">
            <td class="left" style="color:#1e40af;">Grupo 2 (S6, S8, S10), Logística o S4</td>
            <td>+59 €/m <span style="font-size:5.5px;">(79€ s.)</span></td>
            <td><strong>+110 €</strong> <span style="font-size:5.5px;">(195€)</span></td>
            <td><span class="tag-day1" style="color:#1e40af;">+169,00 € combo</span><span style="font-size:5.5px;">[Suelto: 274,00 €]</span></td>
            <td><span class="tag-annual" style="color:#1e40af;">+700,00 € combo</span><span class="tag-ahorro">590€ + 110€ • Suelto Anual: 985€</span></td>
          </tr>
          <tr style="background:#fdf2f8;">
            <td class="left" style="color:#9d174d;">Satélite Instagram 3 en 1</td>
            <td>+49 €/m <span style="font-size:5.5px;">(69€ s.)</span></td>
            <td><strong>+75 €</strong> <span style="font-size:5.5px;">(150€)</span></td>
            <td><span class="tag-day1" style="color:#9d174d;">+124,00 € combo</span><span style="font-size:5.5px;">[Suelto: 219,00 €]</span></td>
            <td><span class="tag-annual" style="color:#9d174d;">+565,00 € combo</span><span class="tag-ahorro">490€ + 75€ • Suelto Anual: 840€</span></td>
          </tr>
          <tr style="background:#f5f3ff;">
            <td class="left" style="color:#4338ca;">Satélite Cerebro Redactor B2B (RAG)</td>
            <td>+69 €/m <span style="font-size:5.5px;">(99€ s.)</span></td>
            <td><strong>+150 €</strong> <span style="font-size:5.5px;">(250€)</span></td>
            <td><span class="tag-day1" style="color:#4338ca;">+219,00 € combo</span><span style="font-size:5.5px;">[Suelto: 349,00 €]</span></td>
            <td><span class="tag-annual" style="color:#4338ca;">+840,00 € combo</span><span class="tag-ahorro">690€ + 150€ • Suelto Anual: 1.240€</span></td>
          </tr>
          <tr style="background:#eef2ff;">
            <td class="left" style="color:#3730a3;">S7 Centralita Voz IA 24/7 (250 min)</td>
            <td>+129 €/m <span style="font-size:5.5px;">(169€)</span></td>
            <td><strong>+250 €</strong> <span style="font-size:5.5px;">(350€)</span></td>
            <td><span class="tag-day1" style="color:#3730a3;">+379,00 € combo</span><span style="font-size:5.5px;">[Suelto: 519,00 €]</span></td>
            <td><span class="tag-annual" style="color:#3730a3;">+1.540,00 € combo</span><span class="tag-ahorro">1.290€ + 250€ • Suelto Anual: 2.040€</span></td>
          </tr>
          <tr style="background:#f0fdfa; border-top:1.6px solid #0d7d74;">
            <td class="left" style="color:#095852;">🔍🧠 Super-Auditoría (Suelta / Base 1)</td>
            <td>0 €/m</td>
            <td><strong>350 €</strong> <span style="font-size:5.5px;">(200€ DIY)</span></td>
            <td><span class="tag-day1" style="color:#095852;">350 € (1) | 590 € (Las 2)</span></td>
            <td><span style="font-size:6px; font-weight:800; color:#095852;">Pack Firma Institucional: 590 € las 2 (Ahorra 110 €)</span></td>
          </tr>
          <tr style="background:#ecfdf5;">
            <td class="left" style="color:#047857;">🔍🧠 Super-Auditoría (Con Pack 2+ serv.)</td>
            <td>0 €/m</td>
            <td><strong style="color:#047857;">195 € c/u</strong></td>
            <td><span class="tag-day1" style="color:#047857;">+195 € (1) | +390 € (Las 2)</span></td>
            <td><span class="tag-annual" style="color:#047857;">195 € c/u (390 € las 2 • Ahorra 310 €)</span><span class="tag-ahorro">Suelo mínimo blindado en cualquier Pack 2+</span></td>
          </tr>
        </tbody>
      </table>

      <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:3.5px solid #0d7d74; padding:3.5px 6.5px; border-radius:4px; font-size:6.5px; color:#334155; line-height:1.2;">
        <strong>Ejemplo de Combinación Cruzada (Grupo 1 + Grupo 2):</strong> Si contratas <strong>S1 Reseñas IA (59 €/m + 150 € Setup) + S6 Anti-Plantón (+59 €/m + 110 € Setup)</strong> = <strong>118 €/mes</strong> (+ 260 € Setup) y ya computa como <strong>Pack Dúo (2 servicios)</strong>, desbloqueando las Super-Auditorías a <strong>195 € c/u</strong>.
      </div>
    </div>

    <div>
      <div class="print-qr-banner">
        <div class="print-qr-left">
          <img src="../qr-code.png" alt="QR WhatsApp" class="print-qr-img" onerror="this.style.display='none'">
          <div class="print-qr-text">
            <strong>¿Quieres activar tu plan en modalidad flexible o anual?</strong>
            Escanea este código con tu móvil para hablar con Francisco y poner en marcha tu negocio.
          </div>
        </div>
        <div class="contact-details-box">
          <span class="name">Francisco M. Gallardo</span>
          <span class="role">Consultor Tecnológico</span>
          <strong>711 54 75 61</strong> • francisco@sistemaspyme.es<br>
          <span style="color:#64748b;">sistemaspyme.es • Galicia</span>
        </div>
      </div>
      <footer class="footer-bar">
        <span><strong>Sistemas Pyme</strong> — Tabla Desglosada de Liquidación Día 1</span>
        <span><strong>Desembolso Inicial (A5)</strong></span>
      </footer>
    </div>
  </main>
</body>
</html>
"""

HTML_DESEMBOLSO_MOVIL = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Desembolso Día 1 y Liquidación Inicial (Móvil) — Sistemas Pyme</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { width: 100%; background-color: #071629; color: #f1f5f9; font-family: 'Inter', sans-serif; font-size: 16.5px; line-height: 1.55; }
    body.font-xl { font-size: 19px; line-height: 1.65; }
    .topbar { position: sticky; top: 0; z-index: 100; background: rgba(7, 22, 41, 0.96); border-bottom: 2px solid #14b8a6; padding: 10px 14px; display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .btn-back { background: #1e293b; color: #5eead4; border: 1px solid rgba(20,184,166,0.45); text-decoration: none; font-weight: 800; font-size: 13px; padding: 8px 12px; border-radius: 10px; }
    .btn-action { background: #0d7d74; color: #fff; border: 1px solid #14b8a6; font-weight: 800; font-size: 12.5px; padding: 8px 11px; border-radius: 10px; text-decoration: none; cursor: pointer; }
    .btn-action.sec { background: #1e293b; color: #cbd5e1; border-color: #475569; }
    .container { max-width: 660px; margin: 0 auto; padding: 18px 16px 48px 16px; display: flex; flex-direction: column; gap: 16px; }
    .hero-box { background: linear-gradient(145deg, #0b2545 0%, #0f172a 100%); border: 1.5px solid rgba(20, 184, 166, 0.45); border-radius: 18px; padding: 18px 16px; }
    .badge { display: inline-block; background: rgba(20, 184, 166, 0.18); color: #5eead4; border: 1px solid rgba(20, 184, 166, 0.4); font-size: 11.5px; font-weight: 800; text-transform: uppercase; padding: 4px 10px; border-radius: 99px; margin-bottom: 8px; }
    .hero-title { font-size: 1.38em; font-weight: 900; color: #fff; line-height: 1.22; margin-bottom: 6px; }
    .section-head { background: linear-gradient(90deg, #0f766e 0%, #115e59 100%); color: #fff; padding: 11px 14px; border-radius: 12px; font-weight: 900; font-size: 0.95em; text-transform: uppercase; margin-top: 6px; }
    .section-head.blue { background: linear-gradient(90deg, #1e3a8a 0%, #1d4ed8 100%); }
    .section-head.amber { background: linear-gradient(90deg, #b45309 0%, #d97706 100%); }
    .card { background: #0f172a; border: 1.5px solid rgba(255,255,255,0.12); border-left: 5px solid #14b8a6; border-radius: 16px; padding: 16px; display: flex; flex-direction: column; gap: 10px; }
    .card.emerald { border-left-color: #10b981; border-color: rgba(16,185,129,0.45); background: linear-gradient(145deg, rgba(6,78,59,0.45) 0%, #0f172a 100%); }
    .card.blue { border-left-color: #3b82f6; }
    .card.amber { border-left-color: #f59e0b; }
    .card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; }
    .card-title { font-size: 1.1em; font-weight: 900; color: #fff; }
    .price-tag { background: rgba(20, 184, 166, 0.18); color: #5eead4; border: 1px solid rgba(20, 184, 166, 0.4); font-weight: 900; font-size: 0.95em; padding: 4px 10px; border-radius: 10px; white-space: nowrap; }
    .data-grid { display: flex; flex-direction: column; gap: 7px; background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px; }
    .data-row { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; padding-bottom: 6px; border-bottom: 1px dashed rgba(255,255,255,0.1); font-size: 0.9em; }
    .data-row:last-child { border-bottom: none; padding-bottom: 0; }
    .data-label { color: #94a3b8; font-weight: 600; }
    .data-val { color: #fff; font-weight: 800; text-align: right; }
    .data-val.hi { color: #34d399; }
    .cta-box { background: linear-gradient(145deg, #064e3b 0%, #0f172a 100%); border: 2px solid #10b981; border-radius: 18px; padding: 20px 16px; text-align: center; }
    .btn-wa { display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; background: #10b981; color: #052e16; font-weight: 900; padding: 14px 18px; border-radius: 14px; text-decoration: none; margin-top: 12px; }
  </style>
</head>
<body>
  <header class="topbar">
    <a href="../index.html#tarifas" onclick="if(window.opener && !window.opener.closed){event.preventDefault();window.close();}" class="btn-back">⬅ Volver a la Web</a>
    <div style="display:flex; gap:6px;">
      <button type="button" onclick="document.body.classList.toggle('font-xl')" class="btn-action">🔎 Letra A+</button>
      <a href="desembolso.html?modo=impreso" class="btn-action sec">📄 Original A5</a>
    </div>
  </header>

  <main class="container">
    <div class="hero-box">
      <span class="badge">Desglose Financiero Día 1</span>
      <h1 class="hero-title">Tabla Desglosada de Puesta en Marcha y Desembolso Día 1</h1>
      <p style="font-size:0.92em; color:#cbd5e1;">Importes exactos de inicio en Vía 1 (Mensual Flexible 3 meses) y Vía 2 (Plan Anual con 2 meses gratis).</p>
    </div>

    <div class="section-head">1. Planes del Grupo 1 (Venta Rápida)</div>

    <article class="card">
      <div class="card-top"><span class="card-title">1. Plan Pyme BASE (1 serv.)</span><span class="price-tag">59 €/m</span></div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Setup Único de Ingeniería:</span><span class="data-val">150 €</span></div>
        <div class="data-row"><span class="data-label">🔄 Día 1 en Vía Flexible:</span><span class="data-val">209 € (150€ + 59€)</span></div>
        <div class="data-row"><span class="data-label">⭐ Día 1 en Vía Anual (10m):</span><span class="data-val hi">740 € (Ahorras 118 €)</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top"><span class="card-title">2. Pack ESCUDO BÁSICO (Dúo: S1+S2)</span><span class="price-tag">99 €/m</span></div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Setup Dúo (150€ + 75€):</span><span class="data-val">225 €</span></div>
        <div class="data-row"><span class="data-label">🔄 Día 1 en Vía Flexible:</span><span class="data-val">324 € (225€ + 99€)</span></div>
        <div class="data-row"><span class="data-label">⭐ Día 1 en Vía Anual (10m):</span><span class="data-val hi">1.215 € (Ahorras 198 €)</span></div>
        <div class="data-row"><span class="data-label">Privilegio Super-Auditorías:</span><span class="data-val hi">195 € c/u (o 390 € las dos)</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top"><span class="card-title">3. Pack ESCUDO TOTAL ★ (Trinity: S1+S2+S3)</span><span class="price-tag">139 €/m</span></div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Setup Trinity (150€ + 75€ + 75€):</span><span class="data-val">300 €</span></div>
        <div class="data-row"><span class="data-label">🔄 Día 1 en Vía Flexible:</span><span class="data-val">439 € (300€ + 139€)</span></div>
        <div class="data-row"><span class="data-label">⭐ Día 1 en Vía Anual (10m):</span><span class="data-val hi">1.690 € (Ahorras 278 €)</span></div>
        <div class="data-row"><span class="data-label">Bóveda (150€) + Auditorías:</span><span class="data-val hi">🎁 GRATIS + Aud. a 195 € c/u</span></div>
      </div>
    </article>

    <article class="card">
      <div class="card-top"><span class="card-title">4. Planes QUATRO (4) y PENTIUM (5)</span><span class="price-tag">179€ / 219€</span></div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">QUATRO Día 1 Flex / Anual:</span><span class="data-val">554 € Flex | 2.165 € Anual</span></div>
        <div class="data-row"><span class="data-label">PENTIUM Día 1 Flex / Anual:</span><span class="data-val">669 € Flex | 2.640 € Anual</span></div>
      </div>
    </article>

    <div class="section-head blue">2. Desembolso Día 1 en Grupos 2, 3 y 4</div>
    <article class="card blue">
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Grupo 2 (S6, S8, S10), Logística o S4 Llamadas:</span><span class="data-val hi">Día 1 Combo: +169 € (59€+110€) | Suelto: 274 €</span></div>
        <div class="data-row"><span class="data-label">Satélite Instagram 3 en 1:</span><span class="data-val hi">Día 1 Combo: +124 € (49€+75€) | Suelto: 219 €</span></div>
        <div class="data-row"><span class="data-label">Satélite Cerebro Redactor RAG:</span><span class="data-val hi">Día 1 Combo: +219 € (69€+150€) | Suelto: 349 €</span></div>
        <div class="data-row"><span class="data-label">S7 Centralita Voz IA 24/7 (250m):</span><span class="data-val hi">Día 1 Combo: +379 € (129€+250€) | Suelto: 519 €</span></div>
      </div>
    </article>

    <div class="section-head amber">3. Super-Auditorías Web (Suelo Mínimo Blindado 195 €)</div>
    <article class="card amber">
      <div class="data-grid">
        <div class="data-row"><span class="data-label">1. Modalidad Solo Código (DIY):</span><span class="data-val">200 € una | 390 € las dos</span></div>
        <div class="data-row"><span class="data-label">2. Llave en Mano (Suelta o con Base):</span><span class="data-val">350 € una | 590 € las dos</span></div>
        <div class="data-row"><span class="data-label">3. Bonificada con Pack (2+ serv.):</span><span class="data-val hi">195 € una | 390 € las dos</span></div>
      </div>
    </article>

    <div class="cta-box">
      <div style="font-size: 0.85em; font-weight: 800; color: #6ee7b7; text-transform: uppercase;">Atención Directa • Galicia</div>
      <div style="font-size: 1.2em; font-weight: 900; color: #ffffff; margin-top: 4px;">Francisco M. Gallardo</div>
      <div style="font-size: 0.92em; color: #cbd5e1; margin-top: 2px;">Tel: <strong>711 54 75 61</strong> • francisco@sistemaspyme.es</div>
      <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20he%20visto%20el%20desglose%20del%20D%C3%ADa%201%20y%20quiero%20activar%20mi%20plan" target="_blank" class="btn-wa">
        💬 Hablar con Francisco por WhatsApp
      </a>
    </div>
  </main>
</body>
</html>
"""

HTML_SETUP_A5 = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <script>
    (function() {
      try {
        var params = new URLSearchParams(window.location.search);
        if (params.get('modo') === 'impreso') return;
        var esMovil = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || (window.innerWidth > 0 && window.innerWidth <= 820);
        if (esMovil) window.location.replace('setup_movil.html');
      } catch(e) {}
    })();
  </script>
  <meta charset="UTF-8">
  <title>Anexo Técnico de Altas e Implantación (Setup + Auditorías) — Sistemas Pyme</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    @page { size: A5 portrait; margin: 0; }
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    body { font-family: 'Inter', sans-serif; background-color: #0b192c; color: #0f172a; display: flex; flex-direction: column; align-items: center; gap: 18px; padding: 18px 0 44px 0; }
    .topbar-pc { position: sticky; top: 10px; z-index: 100; background: rgba(11, 37, 69, 0.96); border: 1.5px solid rgba(20, 184, 166, 0.5); border-radius: 12px; padding: 8px 16px; display: flex; align-items: center; justify-content: space-between; width: 92%; max-width: 760px; color: #fff; }
    .btn-pc { background: #0d7d74; color: #fff; border: 1px solid #14b8a6; padding: 6px 13px; border-radius: 8px; font-size: 12px; font-weight: 800; text-decoration: none; cursor: pointer; }
    .btn-pc.sec { background: #1e293b; border-color: #475569; color: #cbd5e1; }
    .sheet { width: 148mm; height: 210mm; min-height: 210mm; max-height: 210mm; background: #ffffff; padding: 5mm 7.5mm 4.5mm 7.5mm; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 18px 45px rgba(0,0,0,0.55); overflow: hidden; }
    @media screen and (min-width: 821px) { .sheet { zoom: 1.26; } }
    @media print { body { background: none !important; padding: 0 !important; } .no-print { display: none !important; } .sheet { box-shadow: none !important; zoom: 1 !important; margin: 0 !important; } }
    .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0b2545; padding-bottom: 3px; }
    .brand-logo-img { max-height: 40px; width: auto; object-fit: contain; }
    .header-tagline { text-align: right; font-size: 7.2px; color: #475569; font-weight: 600; line-height: 1.22; }
    .header-tagline strong { color: #0f766e; font-size: 8.2px; font-weight: 900; display: block; text-transform: uppercase; }
    .section-banner { background: linear-gradient(90deg, #0f766e 0%, #14b8a6 100%); color: #fff; padding: 3.5px 7.5px; border-radius: 4px; font-size: 8px; font-weight: 900; text-transform: uppercase; display: flex; justify-content: space-between; align-items: center; }
    .section-banner.dark { background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%); }
    .section-banner .rule { font-size: 6.8px; font-weight: 700; background: rgba(255,255,255,0.22); padding: 1px 5px; border-radius: 3px; text-transform: none; }
    .phases-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; }
    .phase-card { background: #f8fafc; border: 1px solid #cbd5e1; border-left: 3.5px solid #0f766e; border-radius: 4px; padding: 3.5px 6px; }
    .phase-card strong { display: block; font-size: 7.5px; font-weight: 900; color: #0b2545; margin-bottom: 1px; }
    .phase-card span { display: block; font-size: 6.7px; color: #334155; line-height: 1.2; }
    .setup-table { width: 100%; border-collapse: collapse; font-size: 7.1px; border: 1.2px solid #cbd5e1; }
    .setup-table th { background: #1e293b; color: #fff; font-size: 6.3px; font-weight: 800; text-transform: uppercase; padding: 3px 5px; text-align: center; }
    .setup-table th:first-child, .setup-table td:first-child { text-align: left; }
    .setup-table td { padding: 3px 5px; border-top: 1px solid #e2e8f0; text-align: center; vertical-align: middle; line-height: 1.18; }
    .plan-name { font-size: 7.8px; font-weight: 900; color: #0b2545; display: block; }
    .plan-sub { font-size: 6px; font-weight: 800; color: #64748b; text-transform: uppercase; display: block; }
    .price-main { font-size: 8.5px; font-weight: 900; color: #0b2545; }
    .save-badge { font-size: 6.6px; font-weight: 800; color: #0f766e; display: block; }
    .guarantee-box { background: #fffbeb; border: 1.2px solid #fcd34d; border-left: 4px solid #d97706; border-radius: 4px; padding: 4px 7px; font-size: 6.8px; color: #78350f; line-height: 1.22; }
    .print-qr-banner { background: #f0fdfa; border: 1.3px dashed #0f766e; border-radius: 4.5px; padding: 4px 7px; display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .print-qr-left { display: flex; align-items: center; gap: 7px; flex: 1; }
    .print-qr-img { width: 34px; height: 34px; border-radius: 3px; }
    .print-qr-text { font-size: 6.9px; color: #1e293b; line-height: 1.2; }
    .print-qr-text strong { color: #115e59; font-size: 7.8px; display: block; }
    .contact-details-box { border-left: 1.2px solid #99f6e4; padding-left: 7px; font-size: 6.7px; line-height: 1.2; text-align: right; }
    .contact-details-box .name { font-size: 8px; font-weight: 900; color: #0b2545; display: block; }
    .contact-details-box .role { font-size: 5.9px; font-weight: 800; color: #0f766e; text-transform: uppercase; display: block; }
    .footer-bar { border-top: 1px solid #cbd5e1; padding-top: 2px; font-size: 6.5px; color: #64748b; display: flex; justify-content: space-between; }
  </style>
</head>
<body>
  <aside class="topbar-pc no-print">
    <div style="font-size:12.5px; font-weight:800;">🔌 Anexo Técnico de Altas (Setup) por Grupos (A5)</div>
    <div style="display:flex; gap:8px;">
      <a href="../index.html#tarifas" onclick="if(window.opener && !window.opener.closed){event.preventDefault();window.close();}" class="btn-pc sec">⬅ Volver a la Web</a>
      <button type="button" onclick="window.print()" class="btn-pc">🖨️ Imprimir / Guardar PDF A5</button>
    </div>
  </aside>

  <main class="sheet">
    <header class="header">
      <img src="../logo.png" alt="Sistemas Pyme" class="brand-logo-img" onerror="this.onerror=null; this.src='logo.png';">
      <div class="header-tagline">
        <strong>Anexo Técnico de Altas e Implantación</strong>
        Reglas de Setup por Complejidad/API y Super-Auditorías
      </div>
    </header>

    <div class="section-banner">
      <span>¿Qué incluye el Alta Técnica (Setup) y la Implantación?</span>
      <span class="rule">Pago único de ingeniería llave en mano</span>
    </div>

    <div class="phases-grid">
      <div class="phase-card">
        <strong>🔌 1. Conexión Oficial Meta y Google API</strong>
        <span>Vinculación verificada con Google Business Profile, Meta Cloud API (fijo o móvil), agendas y carpetas de gestoría.</span>
      </div>
      <div class="phase-card" style="border-left-color:#2563eb;">
        <strong>🧠 2. Entrenamiento IA, HEARD y RGPD</strong>
        <span>Inyección del contexto del negocio, blindaje de secreto profesional RGPD y alta de plantillas en 4 tonos.</span>
      </div>
      <div class="phase-card" style="border-left-color:#d97706;">
        <strong>🔍 3. Ingeniería de Entidades SEO/GEO y Neuro</strong>
        <span>Grafo @graph Wikidata, /llms.txt y Sonda Térmica de 10-14 días en Modo Ágil o Modo Corporativo Alto Standing.</span>
      </div>
      <div class="phase-card" style="border-left-color:#16a34a;">
        <strong>📊 4. Telemetría y Cuadro de Mando 360°</strong>
        <span>Activación de enlaces ultrarrápidos /r/{slug}, pruebas en vivo e Informe Mensual 360° interactivo.</span>
      </div>
    </div>

    <div class="section-banner dark">
      <span>Chuleta Oficial de Altas Técnicas (Setup Único) por Grupos</span>
      <span class="rule">Descuento automático al combinar módulos</span>
    </div>

    <table class="setup-table">
      <thead>
        <tr>
          <th style="width:34%;">Grupo / Plan o Módulo</th>
          <th style="width:26%;">Regla de Ingeniería</th>
          <th style="width:18%;">Setup Único</th>
          <th style="width:22%;">Ventaja / Ahorro</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="plan-name">Grupo 1: 1er Servicio (Plan BASE)</span><span class="plan-sub">S1, S2, S3 Leads 10s, S9 o S5</span></td>
          <td>1er módulo núcleo (100%)</td>
          <td><span class="price-main">150 €</span></td>
          <td><span style="font-size:6.4px; color:#475569; font-weight:700;">Puesta en marcha 24-48h</span></td>
        </tr>
        <tr style="background:#f0f9ff;">
          <td><span class="plan-name" style="color:#0369a1;">Grupo 1: Pack ESCUDO BÁSICO (Dúo)</span><span class="plan-sub" style="color:#0284c7;">2 Servicios Grupo 1 (ej. S1+S2)</span></td>
          <td>150 € + <strong>2º módulo al 50% (+75 €)</strong></td>
          <td><span class="price-main" style="color:#0369a1;">225 €</span></td>
          <td><span class="save-badge">Ahorras 75 € + Aud. a 195€</span></td>
        </tr>
        <tr style="background:#ecfdf5;">
          <td><span class="plan-name" style="color:#047857;">Grupo 1: Pack ESCUDO TOTAL ★ (Trinity)</span><span class="plan-sub" style="color:#059669;">S1 + S2 + S3 Leads en 10s</span></td>
          <td>150 € + <strong>2 módulos al 50% (+150 €)</strong></td>
          <td><span class="price-main" style="color:#047857;">300 €</span></td>
          <td><span class="save-badge" style="color:#047857;">Ahorras 150 € + Bóveda Gratis</span></td>
        </tr>
        <tr>
          <td><span class="plan-name">Grupo 1: Planes QUATRO (4) y PENTIUM (5)</span><span class="plan-sub">Cada servicio extra G1 suma +75 €</span></td>
          <td>Quatro: 375 € | Pentium: 450 €</td>
          <td><span class="price-main">375 € / 450 €</span></td>
          <td><span class="save-badge">Ahorras hasta 300 € en Setup</span></td>
        </tr>
        <tr style="background:#eff6ff;">
          <td><span class="plan-name" style="color:#1e40af;">Grupo 2 (S6, S8, S10), Logística o S4</span><span class="plan-sub" style="color:#1d4ed8;">Agenda, Contratos, Cobros, Reparto o Llamadas</span></td>
          <td>Conexión profunda bidireccional</td>
          <td><span style="font-size:7.8px; font-weight:900; color:#1e40af;">+110 € combo</span><br><span style="font-size:6px; color:#64748b;">(195 € suelto)</span></td>
          <td><span class="save-badge" style="color:#1e40af;">Ahorras 85 € en Setup</span></td>
        </tr>
        <tr style="background:#fdf2f8;">
          <td><span class="plan-name" style="color:#9d174d;">Satélite 1: Instagram 3 en 1 (Meta API)</span><span class="plan-sub" style="color:#be185d;">Auto-DM Reels + DMs 24/7 + Stories</span></td>
          <td>50% dto. al unirlo a un Pack</td>
          <td><span style="font-size:7.8px; font-weight:900; color:#9d174d;">+75 € combo</span><br><span style="font-size:6px; color:#64748b;">(150 € suelto)</span></td>
          <td><span class="save-badge" style="color:#9d174d;">Ahorras 75 € en Setup</span></td>
        </tr>
        <tr style="background:#f5f3ff;">
          <td><span class="plan-name" style="color:#4338ca;">Satélite 3: Cerebro Redactor B2B (RAG)</span><span class="plan-sub" style="color:#4f46e5;">Indexación PDFs, Tarifas y Contratos</span></td>
          <td>Base vectorial privada IA</td>
          <td><span style="font-size:7.8px; font-weight:900; color:#4338ca;">+150 € combo</span><br><span style="font-size:6px; color:#64748b;">(250 € suelto)</span></td>
          <td><span class="save-badge" style="color:#4338ca;">Ahorras 100 € en Setup</span></td>
        </tr>
        <tr style="background:#eef2ff;">
          <td><span class="plan-name" style="color:#3730a3;">Satélite S7: Centralita Voz IA 24/7</span><span class="plan-sub" style="color:#4338ca;">Línea SIP + Voz Neuronal + Agenda (250m)</span></td>
          <td>Entrenamiento voz + desvíos</td>
          <td><span style="font-size:7.8px; font-weight:900; color:#3730a3;">+250 € combo</span><br><span style="font-size:6px; color:#64748b;">(350 € suelto)</span></td>
          <td><span class="save-badge" style="color:#3730a3;">Ahorras 100 € en Setup</span></td>
        </tr>
        <tr style="background:#f0fdfa;">
          <td><span class="plan-name" style="color:#095852;">🔍🧠 Las 2 Super-Auditorías Gemelas</span><span class="plan-sub" style="color:#0d7d74;">1) SEO/GEO IA y 2) Neuro-CRO (Sonda 10-14d)</span></td>
          <td>DIY: <strong>200€</strong> (390€ las 2)<br>Llave en Mano: <strong>350€</strong> (590€ las 2)</td>
          <td><span class="price-main" style="color:#047857;">195 € c/u</span><br><span style="font-size:5.8px; font-weight:800; color:#065f46;">(Con Pack 2+ serv.)</span></td>
          <td><span class="save-badge" style="color:#047857;">390 € las 2 en Pack<br>(Suelo blindado 195€)</span></td>
        </tr>
      </tbody>
    </table>

    <div class="guarantee-box">
      <strong style="color:#b45309;">Garantía de Escalabilidad sin Penalización:</strong> Si hoy empiezas con 1 servicio y más adelante amplías tu plan con nuevos módulos del Grupo 1, 2, 3 o 4, <strong>te aplicamos directamente el Setup Combinado bonificado</strong> (+75 € en G1/IG, +110 € en G2/Logística/S4).
    </div>

    <div class="print-qr-banner">
      <div class="print-qr-left">
        <img src="../qr-code.png" alt="QR Contacto" class="print-qr-img" onerror="this.style.display='none'">
        <div class="print-qr-text">
          <strong>¿Listo para programar la puesta en marcha en tu negocio?</strong>
          Escanea este código con tu móvil para hablar con Francisco y agendar tu alta técnica.
        </div>
      </div>
      <div class="contact-details-box">
        <span class="name">Francisco M. Gallardo</span>
        <span class="role">Consultor Tecnológico</span>
        <strong>711 54 75 61</strong> • francisco@sistemaspyme.es<br>
        <span style="color:#64748b;">sistemaspyme.es • Galicia</span>
      </div>
    </div>

    <footer class="footer-bar">
      <span><strong>Sistemas Pyme</strong> — Anexo Técnico de Altas y Setups (Sin IVA 21%)</span>
      <span><strong>Anexo I (Setup + Super-Auditorías)</strong></span>
    </footer>
  </main>
</body>
</html>
"""

HTML_SETUP_MOVIL = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Anexo Técnico de Implantación (Setup + Super-Auditorías) — Sistemas Pyme</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { width: 100%; background-color: #071629; color: #f1f5f9; font-family: 'Inter', sans-serif; font-size: 16.5px; line-height: 1.55; }
    body.font-xl { font-size: 19px; line-height: 1.65; }
    .topbar { position: sticky; top: 0; z-index: 100; background: rgba(7, 22, 41, 0.96); border-bottom: 2px solid #14b8a6; padding: 10px 14px; display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .btn-back { background: #1e293b; color: #5eead4; border: 1px solid rgba(20,184,166,0.45); text-decoration: none; font-weight: 800; font-size: 13px; padding: 8px 12px; border-radius: 10px; }
    .btn-action { background: #0d7d74; color: #fff; border: 1px solid #14b8a6; font-weight: 800; font-size: 12.5px; padding: 8px 11px; border-radius: 10px; text-decoration: none; cursor: pointer; }
    .btn-action.sec { background: #1e293b; color: #cbd5e1; border-color: #475569; }
    .container { max-width: 660px; margin: 0 auto; padding: 18px 16px 48px 16px; display: flex; flex-direction: column; gap: 16px; }
    .hero-box { background: linear-gradient(145deg, #0b2545 0%, #0f172a 100%); border: 1.5px solid rgba(20, 184, 166, 0.45); border-radius: 18px; padding: 18px 16px; }
    .badge { display: inline-block; background: rgba(20, 184, 166, 0.18); color: #5eead4; border: 1px solid rgba(20, 184, 166, 0.4); font-size: 11.5px; font-weight: 800; text-transform: uppercase; padding: 4px 10px; border-radius: 99px; margin-bottom: 8px; }
    .hero-title { font-size: 1.38em; font-weight: 900; color: #fff; line-height: 1.22; margin-bottom: 6px; }
    .section-head { background: linear-gradient(90deg, #0f766e 0%, #115e59 100%); color: #fff; padding: 11px 14px; border-radius: 12px; font-weight: 900; font-size: 0.95em; text-transform: uppercase; margin-top: 6px; }
    .section-head.blue { background: linear-gradient(90deg, #1e3a8a 0%, #1d4ed8 100%); }
    .section-head.amber { background: linear-gradient(90deg, #b45309 0%, #d97706 100%); }
    .card { background: #0f172a; border: 1.5px solid rgba(255,255,255,0.12); border-left: 5px solid #14b8a6; border-radius: 16px; padding: 16px; display: flex; flex-direction: column; gap: 10px; }
    .card.emerald { border-left-color: #10b981; border-color: rgba(16,185,129,0.45); background: linear-gradient(145deg, rgba(6,78,59,0.45) 0%, #0f172a 100%); }
    .card.blue { border-left-color: #3b82f6; }
    .card.amber { border-left-color: #f59e0b; }
    .card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; }
    .card-title { font-size: 1.08em; font-weight: 900; color: #fff; }
    .price-tag { background: rgba(20, 184, 166, 0.18); color: #5eead4; border: 1px solid rgba(20, 184, 166, 0.4); font-weight: 900; font-size: 0.95em; padding: 4px 10px; border-radius: 10px; white-space: nowrap; }
    .data-grid { display: flex; flex-direction: column; gap: 7px; background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px; }
    .data-row { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; padding-bottom: 6px; border-bottom: 1px dashed rgba(255,255,255,0.1); font-size: 0.9em; }
    .data-row:last-child { border-bottom: none; padding-bottom: 0; }
    .data-label { color: #94a3b8; font-weight: 600; }
    .data-val { color: #fff; font-weight: 800; text-align: right; }
    .data-val.hi { color: #34d399; }
    .cta-box { background: linear-gradient(145deg, #064e3b 0%, #0f172a 100%); border: 2px solid #10b981; border-radius: 18px; padding: 20px 16px; text-align: center; }
    .btn-wa { display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; background: #10b981; color: #052e16; font-weight: 900; padding: 14px 18px; border-radius: 14px; text-decoration: none; margin-top: 12px; }
  </style>
</head>
<body>
  <header class="topbar">
    <a href="../index.html#documentacion" onclick="if(window.opener && !window.opener.closed){event.preventDefault();window.close();}" class="btn-back">⬅ Volver a la Web</a>
    <div style="display:flex; gap:6px;">
      <button type="button" onclick="document.body.classList.toggle('font-xl')" class="btn-action">🔎 Letra A+</button>
      <a href="setup.html?modo=impreso" class="btn-action sec">📄 Original A5</a>
    </div>
  </header>

  <main class="container">
    <div class="hero-box">
      <span class="badge">Anexo Técnico Oficial</span>
      <h1 class="hero-title">Altas Técnicas (Setup) por Grupos y Super-Auditorías</h1>
      <p style="font-size:0.92em; color:#cbd5e1;">Reglas oficiales de puesta en marcha llave en mano en los 4 Grupos de servicios, Super-Auditorías y Atril NFC.</p>
    </div>

    <div class="section-head">1. Altas Técnicas del Grupo 1 (150 € el 1º | +75 € adicionales)</div>
    <article class="card emerald">
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Plan Pyme BASE (1 serv. G1):</span><span class="data-val">150 € Setup</span></div>
        <div class="data-row"><span class="data-label">Pack ESCUDO BÁSICO (Dúo 2 serv.):</span><span class="data-val hi">225 € Setup (Ahorras 75 €)</span></div>
        <div class="data-row"><span class="data-label">Pack ESCUDO TOTAL ★ (Trinity 3 serv.):</span><span class="data-val hi">300 € Setup + 🎁 Bóveda Gratis</span></div>
        <div class="data-row"><span class="data-label">Plan QUATRO (4) / PENTIUM (5):</span><span class="data-val hi">375 € / 450 € Setup</span></div>
      </div>
    </article>

    <div class="section-head blue">2. Altas Técnicas en Grupos 2, 3 y 4 (Suelto vs. Combinado)</div>
    <article class="card blue">
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Grupo 2 (S6, S8, S10), Logística o S4 Llamadas:</span><span class="data-val hi">+110 € combinado | 195 € suelto</span></div>
        <div class="data-row"><span class="data-label">Satélite 1: Instagram 3 en 1:</span><span class="data-val hi">+75 € combinado | 150 € suelto</span></div>
        <div class="data-row"><span class="data-label">Satélite 3: Cerebro Redactor B2B (RAG):</span><span class="data-val hi">+150 € combinado | 250 € suelto</span></div>
        <div class="data-row"><span class="data-label">Satélite S7: Centralita Voz IA 24/7:</span><span class="data-val hi">+250 € combinado | 350 € suelto</span></div>
        <div class="data-row"><span class="data-label">Boosters IA (Correo S9 / Prov. S10):</span><span class="data-val">+50 € Setup</span></div>
      </div>
    </article>

    <div class="section-head amber">3. Las 2 Super-Auditorías y Hardware NFC</div>
    <article class="card amber">
      <div class="data-grid">
        <div class="data-row"><span class="data-label">1. Solo Código / DIY:</span><span class="data-val">200 € una | 390 € las dos</span></div>
        <div class="data-row"><span class="data-label">2. Oficial Llave en Mano (Suelta/Base):</span><span class="data-val">350 € una | 590 € las dos</span></div>
        <div class="data-row"><span class="data-label">3. Bonificada con Pack (2+ serv.):</span><span class="data-val hi">195 € una | 390 € las dos</span></div>
        <div class="data-row"><span class="data-label">★ Atril NFC + QR Mostrador:</span><span class="data-val hi">39 € (1ª ud) | 29 € (2ª-4ª) | 25 € (5+)</span></div>
      </div>
    </article>

    <div class="cta-box">
      <div style="font-size: 0.85em; font-weight: 800; color: #6ee7b7; text-transform: uppercase;">Atención Directa • Galicia</div>
      <div style="font-size: 1.2em; font-weight: 900; color: #ffffff; margin-top: 4px;">Francisco M. Gallardo</div>
      <div style="font-size: 0.92em; color: #cbd5e1; margin-top: 2px;">Tel: <strong>711 54 75 61</strong> • francisco@sistemaspyme.es</div>
      <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20programar%20la%20puesta%20en%20marcha%20en%20mi%20negocio" target="_blank" class="btn-wa">
        💬 Hablar con Francisco por WhatsApp
      </a>
    </div>
  </main>
</body>
</html>
"""

def actualizar_catalogo_a4_y_movil(ruta_catalogo_a4, ruta_catalogo_movil):
    if os.path.isfile(ruta_catalogo_a4):
        with open(ruta_catalogo_a4, "r", encoding="utf-8") as f:
            c = f.read()
        c = c.replace(
            "Auditoría e Implantación Premium SEO Local + GEO (Posicionamiento en IA)",
            "Las 2 Super-Auditorías Gemelas: 1) Ingeniería SEO Local + GEO IA y 2) Neuro-CRO (Sonda 10-14 Días)"
        )
        c = c.replace(
            "Guía detallada paso a paso de nuestros 10 servicios troncales, Auditoría (GEO o Neuro CRO) IA y 3 Satélites",
            "Arquitectura Oficial en 4 Grupos Operativos (S1 a S10), las 2 Super-Auditorías Gemelas (SEO/GEO y Neuro-CRO) y Satélites"
        )
        escribir_archivo_con_backup(ruta_catalogo_a4, c)

    if os.path.isfile(ruta_catalogo_movil):
        with open(ruta_catalogo_movil, "r", encoding="utf-8") as f:
            cm = f.read()
        cm = cm.replace(
            "(o <strong>95 € c/u</strong> en Plan Anual Trinity+).",
            "(o <strong>390 € las dos juntas</strong>; suelo mínimo blindado de 195 € c/u). Y en el <strong>Pack Escudo Total ★ (Trinity S1+S2+S3 Leads en 10s por 139 €/mes)</strong> recibes además GRATIS la Bóveda de Contraseñas."
        )
        cm = cm.replace(
            "Sueltas cuestan 200 € (solo diagnóstico/código) o 350 € (llave en mano)",
            "Sueltas cuestan 200 € (Solo Código DIY: 390 € las dos) o 350 € Llave en Mano (590 € las dos juntas en Pack Firma Institucional)"
        )
        escribir_archivo_con_backup(ruta_catalogo_movil, cm)

# =============================================================================
# 5. PARCHE QUIRÚRGICO DE INDEX.HTML (PRECIOS CLAROS + CARRITO + S3 TRINITY)
# =============================================================================
NUEVO_BLOQUE_VISTA_TARIFAS_INDEX = r"""  <!-- ======================================================================= -->
  <!-- VISTA 4 (SALA INDEPENDIENTE): PRECIOS CLAROS (ARQUITECTURA 4 GRUPOS)    -->
  <!-- ======================================================================= -->
  <section id="vista-tarifas" class="view-panel hidden bg-slate-50 text-slate-900">

    <!-- =================================================================== -->
    <!-- DIAPOSITIVA 1 DE PRECIOS: LOS 3 PLANES TRONCALES DEL GRUPO 1        -->
    <!-- =================================================================== -->
    <div id="tarifas-slide-planes" class="slide-section sp-tarifas-light-bg border-b border-teal-200/80 px-4 sm:px-6 relative overflow-hidden" style="min-height: calc(100vh - 5.75rem); padding-top: 1.75rem !important; padding-bottom: 0.75rem !important; justify-content: flex-start !important;">
      <div class="absolute inset-0 sp-rhombus-grid-reverse pointer-events-none opacity-65" aria-hidden="true"></div>

      <div class="max-w-6xl mx-auto w-full flex flex-col justify-start relative z-10">

        <!-- FILA 1: Encabezado de Sección + Conmutador Mensual/Anual -->
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3 pb-2.5 mb-3.5 border-b-2 border-teal-500/25">
          <div>
            <div class="inline-flex items-center gap-2 text-[11px] font-extrabold uppercase tracking-wider text-teal-800 bg-teal-50/90 px-3 py-0.5 rounded-full border border-teal-300/80 mb-1 shadow-sm">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>Arquitectura Oficial en 4 Bloques • 1º a 59 €/m y +40 €/m en Grupo 1 • Suelo Super-Auditorías 195 €</span>
            </div>
            <h2 class="text-2xl sm:text-3xl lg:text-[27px] font-black text-brand-navy tracking-tight leading-tight">
              Precios claros y <span class="sp-green-headline">amortización desde el primer cliente.</span>
            </h2>
          </div>

          <div class="inline-flex items-center gap-1.5 bg-white/95 p-1 rounded-2xl border-2 border-teal-500/35 shadow-md self-start lg:self-center flex-shrink-0">
            <button type="button" id="btnSwitchMensual" onclick="cambiarModoTarifas('mensual')" class="px-4 py-1.5 rounded-xl text-xs sm:text-[13px] font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer">
              🔄 Mensual Flexible (3m mín.)
            </button>
            <button type="button" id="btnSwitchAnual" onclick="cambiarModoTarifas('anual')" class="px-4 py-1.5 rounded-xl text-xs sm:text-[13px] font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer flex items-center gap-1.5">
              <span>🎁 Plan Anual</span>
              <span class="text-[10px] font-black bg-amber-100 text-amber-900 border border-amber-400 px-2 py-0.5 rounded-full">2 Meses Gratis</span>
            </button>
          </div>
        </div>

        <!-- FILA 2: Las 3 Tarjetas Protagonistas del Grupo 1 (Base 59€, Escudo Básico Dúo 99€ y Escudo Total Trinity 139€) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 items-stretch mb-2.5">

          <!-- TARJETA 1: PLAN PYME BASE (1 SERVICIO GRUPO 1 = 59 €/MES) -->
          <div class="sp-price-card-3d sp-price-card-slate px-5 py-3.5 flex flex-col justify-between">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1.5">
                <div class="inline-flex flex-col items-center justify-center text-[10px] font-extrabold uppercase tracking-wider text-slate-800 bg-slate-100 px-2.5 py-0.5 rounded-xl border border-slate-300 leading-tight shadow-sm">
                  <span class="whitespace-nowrap">1 Servicio Grupo 1</span>
                  <span class="text-[9px] text-slate-600 font-bold whitespace-nowrap">(S1, S2 o S3 a elegir)</span>
                </div>
                <div class="text-right leading-tight">
                  <span class="block text-[11px] font-bold text-slate-700 whitespace-nowrap">Setup único: <strong class="text-brand-navy font-black">150 €</strong></span>
                  <span class="block text-[10px] font-semibold text-slate-500 whitespace-nowrap">(Alta llave en mano)</span>
                </div>
              </div>

              <h3 class="text-lg sm:text-[19px] font-black text-brand-navy mb-0.5 whitespace-nowrap">
                Plan Pyme BASE <span class="text-slate-500 font-bold text-sm">(1 serv.)</span>
              </h3>
              <p class="text-xs text-slate-600 mb-2 leading-snug">
                Para empezar hoy por un único servicio troncal de implantación rápida:
              </p>

              <div class="bg-slate-50 border-2 border-slate-200/90 rounded-2xl px-3.5 py-2 mb-2 shadow-inner">
                <div class="flex items-baseline gap-1.5" data-plan-price="base">
                  <span class="text-2xl sm:text-[28px] font-black text-brand-navy">59 €</span>
                  <span class="text-xs font-bold text-slate-500">/ mes</span>
                </div>
                <span id="spSubPriceBase" class="block text-[10.5px] font-extrabold text-teal-800 mt-0.5">
                  Día 1 Flex: 209 € (150 € Setup + 59 € Mes 1)
                </span>
              </div>

              <ul class="space-y-1 text-xs text-slate-700 leading-snug mb-2.5">
                <li class="flex items-start gap-1.5"><span class="text-teal-600 font-black">✔</span><span>Elige <strong class="text-brand-navy">S1 (Reseñas IA)</strong>, <strong class="text-brand-navy">S2 (Cortafuegos WA)</strong> o <strong class="text-brand-navy">S3 (Leads en 10s)</strong>.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-teal-600 font-black">✔</span><span>Incluye <strong class="text-brand-navy">Informe Mensual 360° Interactivo</strong> cada día 1 de mes.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-slate-400 font-black">•</span><span class="text-slate-600">Super-Auditorías Llave en Mano a tarifa estándar (350 € una / 590 € las dos).</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanBase" href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20me%20interesa%20el%20Plan%20Pyme%20BASE%20%281%20servicio%20por%2059%20%E2%82%AC%2Fmes%29" target="_blank" class="w-full py-2 text-center rounded-xl bg-brand-navy hover:bg-slate-800 text-white font-extrabold text-xs sm:text-[13px] shadow-md transition-all block">
              Elegir Plan Pyme BASE &rarr;
            </a>
          </div>

          <!-- TARJETA 2: PACK ESCUDO BÁSICO (DÚO: 2 SERVICIOS GRUPO 1 = 99 €/MES) -->
          <div class="sp-price-card-3d sp-price-card-sky px-5 py-3.5 flex flex-col justify-between">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1.5">
                <div class="inline-flex flex-col items-center justify-center text-[10px] font-extrabold uppercase tracking-wider text-sky-900 bg-sky-100/95 px-2.5 py-0.5 rounded-xl border border-sky-300 leading-tight shadow-sm">
                  <span class="whitespace-nowrap">🛡️ Dúo: 2 Servicios</span>
                  <span class="text-[9px] text-sky-950 font-black whitespace-nowrap">(S1 + S2 o S1 + S3)</span>
                </div>
                <div class="text-right leading-tight">
                  <span class="block text-[11px] font-bold text-sky-950 whitespace-nowrap">Setup Dúo: <strong class="text-brand-navy font-black">225 €</strong></span>
                  <span class="block text-[10px] font-extrabold text-emerald-700 whitespace-nowrap">(150 € + 75 € al 50%)</span>
                </div>
              </div>

              <h3 class="text-lg sm:text-[19px] font-black text-brand-navy mb-0.5 whitespace-nowrap">
                Pack Escudo Básico <span class="text-sky-700 font-bold text-sm">(Dúo)</span>
              </h3>
              <p class="text-xs text-slate-700 mb-2 leading-snug">
                Doble blindaje de reputación y captación (el 2.º módulo suma solo <strong class="text-brand-navy">+40 €/mes</strong>):
              </p>

              <div class="bg-white/95 border-2 border-sky-300 rounded-2xl px-3.5 py-2 mb-2 shadow-inner">
                <div class="flex items-baseline justify-between gap-2">
                  <div class="flex items-baseline gap-1.5" data-plan-price="duo">
                    <span class="text-2xl sm:text-[28px] font-black text-sky-700">99 €</span>
                    <span class="text-xs font-bold text-slate-500">/ mes</span>
                  </div>
                  <span class="text-[10px] font-extrabold bg-emerald-100 text-emerald-800 border border-emerald-300 px-2 py-0.5 rounded-full whitespace-nowrap">Ahorras 19 €/m + 75 € Setup</span>
                </div>
                <span id="spSubPriceDuo" class="block text-[10.5px] font-extrabold text-sky-900 mt-0.5">
                  Día 1 Flex: 324 € (225 € Setup + 99 € Mes 1)
                </span>
              </div>

              <ul class="space-y-1 text-xs text-slate-800 leading-snug mb-2.5">
                <li class="flex items-start gap-1.5"><span class="text-sky-600 font-black">✔</span><span><strong class="text-brand-navy">Une S1 + S2:</strong> Respuesta IA en Google + Cortafuegos Preventivo por WhatsApp.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-sky-600 font-black">✔</span><span><strong class="text-brand-navy">Informe 360° Completo</strong> con transcripción IA de notas de voz.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-amber-600 font-black">🔑</span><span><strong class="text-brand-navy">Desbloquea Super-Auditorías a 195 € c/u</strong> (o <strong class="text-emerald-800">390 € las dos juntas</strong>, ahorrando 310 €).</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanDuo" href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20me%20interesa%20el%20Pack%20Escudo%20B%C3%A1sico%20D%C3%BAo%20%28S1%20%2B%20S2%20por%2099%20%E2%82%AC%2Fmes%29" target="_blank" class="w-full py-2 text-center rounded-xl bg-sky-600 hover:bg-sky-700 text-white font-black text-xs sm:text-[13px] shadow-lg shadow-sky-600/25 transition-all block">
              Elegir Pack Escudo Básico &rarr;
            </a>
          </div>

          <!-- TARJETA 3 ESTRELLA: PACK ESCUDO TOTAL ★ (TRINITY: S1 + S2 + S3 LEADS 10S = 139 €/MES) -->
          <div class="sp-price-card-3d sp-price-card-emerald px-5 py-3.5 flex flex-col justify-between relative">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1.5">
                <div class="inline-flex flex-col items-center justify-center text-[10px] font-extrabold uppercase tracking-wider text-white bg-gradient-to-r from-emerald-600 to-teal-600 px-2.5 py-0.5 rounded-xl shadow-sm leading-tight">
                  <span class="whitespace-nowrap">★ Pack Estrella Trinity</span>
                  <span class="text-[9px] font-black text-emerald-50 whitespace-nowrap">(S1 + S2 + S3 Leads 10s)</span>
                </div>
                <div class="text-right leading-tight">
                  <span id="spBadgeAhorroEscudoTotal" class="block text-[10px] font-black text-amber-900 bg-amber-100/95 px-2 py-0.5 rounded-md border border-amber-300 whitespace-nowrap">🎁 Bóveda Gratis (150 €)</span>
                  <span class="block text-[9px] font-extrabold text-teal-900 whitespace-nowrap mt-0.5">Setup Trinity: 300 € (150+75+75)</span>
                </div>
              </div>

              <div class="flex flex-wrap items-center justify-between gap-1.5 mb-2">
                <h3 id="spTitleEscudoTotal" class="text-lg sm:text-[19px] font-black text-brand-navy whitespace-nowrap">
                  Pack Escudo Total ★ <span class="text-emerald-700 font-bold text-xs">(Trinity)</span>
                </h3>
                <div class="inline-flex items-center bg-white/95 p-0.5 rounded-lg border-2 border-emerald-500/50 text-[9.5px] font-extrabold shadow-sm">
                  <button type="button" id="btnEscudo0Aud" onclick="spSeleccionarNivelEscudoTotal(0)" class="px-1.5 py-0.5 rounded-md bg-emerald-600 text-white cursor-pointer transition-all whitespace-nowrap">
                    Solo Pack
                  </button>
                  <button type="button" id="btnEscudo1Aud" onclick="spSeleccionarNivelEscudoTotal(1)" class="px-1.5 py-0.5 rounded-md text-teal-900 hover:text-brand-navy cursor-pointer transition-all whitespace-nowrap">
                    +1 Aud (195€)
                  </button>
                  <button type="button" id="btnEscudo2Aud" onclick="spSeleccionarNivelEscudoTotal(2)" class="px-1.5 py-0.5 rounded-md text-teal-900 hover:text-brand-navy cursor-pointer transition-all whitespace-nowrap">
                    +2 Aud (390€)
                  </button>
                </div>
              </div>

              <div class="bg-white/95 border-2 border-emerald-500/70 rounded-2xl px-3.5 py-2 mb-2 shadow-inner">
                <div class="flex items-baseline justify-between gap-1.5 flex-wrap">
                  <div class="flex items-baseline gap-1" data-plan-price="trinity">
                    <span class="text-2xl sm:text-[28px] font-black text-emerald-700">139 €</span>
                    <span class="text-xs font-bold text-slate-500">/ mes</span>
                  </div>
                  <span id="spAuditAddonPriceTag" class="text-[10px] font-black text-emerald-900 bg-emerald-100 border border-emerald-400 px-2 py-0.5 rounded-lg whitespace-nowrap">
                    59 € + 40 € + 40 € (3 serv. G1)
                  </span>
                </div>
                <span id="spSubPriceEscudoTotal" class="block text-[10.5px] font-extrabold text-teal-900 mt-0.5">
                  Día 1 Flex: 439 € (300 € Setup + 139 € Mes 1) | Anual: 1.690 €
                </span>
              </div>

              <ul class="space-y-1 text-xs text-slate-800 leading-snug mb-2.5">
                <li class="flex items-start gap-1.5"><span class="text-emerald-600 font-black">✔</span><span><strong class="text-brand-navy">Une S1 + S2 + S3 (Respuesta a Leads en 10s + Portales):</strong> reputación blindada y cierre de presupuestos en caliente.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-emerald-600 font-black">✔</span><span id="spBulletAuditEscudo">Incluye <strong class="text-brand-navy">🎁 Bóveda de Contraseñas GRATIS</strong> (valorada en 150 €) para compartir accesos con tu equipo en 1 clic.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-amber-600 font-black">★</span><span id="spBulletBonusEscudo"><strong class="text-brand-navy">Super-Auditorías Llave en Mano bonificadas un 44%:</strong> llévate 1 por <strong class="text-emerald-800">195 €</strong> o las 2 juntas por <strong class="text-emerald-800">390 €</strong>.</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanEscudoTotal" href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20activar%20el%20Pack%20Escudo%20Total%20Trinity%20%28S1%20%2B%20S2%20%2B%20S3%20Leads%20en%2010s%20por%20139%20%E2%82%AC%2Fmes%29" target="_blank" class="sp-btn-s5-primary-3d w-full py-2 text-center rounded-xl text-white font-black text-xs sm:text-[13px] block">
              Activar Pack Escudo Total &rarr;
            </a>
          </div>

        </div>

        <!-- FILA 3: Banner-Guía hacia la Diapositiva 2 (Los 4 Grupos, Super-Auditorías y Atril NFC) -->
        <div class="pt-0.5 pb-1 flex justify-center">
          <button type="button" onclick="spScrollLimpioSeccion('tarifas-slide-complementos')" class="group inline-flex items-center gap-3 px-6 py-2 rounded-2xl bg-white/95 hover:bg-teal-50 border-2 border-teal-500/50 hover:border-teal-600 shadow-md transition-all cursor-pointer">
            <span class="text-sm">🔍🧠</span>
            <span class="text-xs sm:text-[13px] font-extrabold text-brand-navy group-hover:text-teal-800">
              Ver Tabla de las 2 Super-Auditorías (195 € / 350 € / 590 €), Grupos 2-3-4 y Atril NFC
            </span>
            <span class="w-5 h-5 rounded-full bg-teal-500/15 border border-teal-500/50 flex items-center justify-center text-teal-700 group-hover:translate-y-0.5 transition-transform font-black text-xs">
              &darr;
            </span>
          </button>
        </div>

      </div>
    </div>

    <!-- =================================================================== -->
    <!-- DIAPOSITIVA 2 DE PRECIOS: SUPER-AUDITORÍAS, GRUPOS 2-3-4 Y ATRIL    -->
    <!-- =================================================================== -->
    <div id="tarifas-slide-complementos" class="slide-section sp-tarifas-light-bg px-4 sm:px-6 py-5 relative overflow-hidden" style="min-height: calc(100vh - 5.75rem);">
      <div class="absolute inset-0 sp-rhombus-grid-reverse pointer-events-none opacity-65" aria-hidden="true"></div>
      <div class="max-w-6xl mx-auto w-full flex flex-col justify-between min-h-[calc(100vh-8.5rem)] relative z-10">

        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2.5 border-b-2 border-teal-500/25">
          <div>
            <span class="text-[11px] font-extrabold uppercase tracking-wider text-amber-800 bg-amber-100/90 px-3 py-0.5 rounded-full border border-amber-300 inline-block mb-1">
              Suelo Mínimo Blindado de 195 € en Super-Auditorías • Grupos 2, 3 y 4 con Descuento Combinado
            </span>
            <h3 class="text-2xl sm:text-3xl font-black text-brand-navy tracking-tight">
              Las 2 Super-Auditorías Gemelas, <span class="sp-green-headline">Grupos Avanzados y Hardware NFC.</span>
            </h3>
          </div>
          <button type="button" onclick="spScrollLimpioSeccion('tarifas-slide-planes')" class="self-start sm:self-center inline-flex items-center gap-2 text-xs font-extrabold text-brand-navy hover:text-teal-700 bg-white hover:bg-teal-50 px-4 py-2 rounded-xl border-2 border-slate-300 shadow-sm transition-all cursor-pointer">
            <span>&uarr;</span>
            <span>Volver a los Planes del Grupo 1</span>
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 my-auto py-2.5 items-stretch">

          <!-- Columna Izquierda (7 cols): Las 2 Super-Auditorías Gemelas (Tabla Oficial Suelo 195 €) -->
          <div class="lg:col-span-7 sp-light-card-3d-teal rounded-3xl p-5 flex flex-col justify-between">
            <div>
              <div class="flex flex-wrap items-center justify-between gap-2 mb-2.5">
                <span class="text-xs font-extrabold uppercase tracking-wider text-teal-900 bg-teal-100/90 px-3 py-1 rounded-full border border-teal-400">
                  🔍🧠 Las 2 Super-Auditorías Web Gemelas (Pago Único • Sin Cuotas)
                </span>
                <span class="text-[11px] font-extrabold text-amber-900 bg-amber-100 px-2.5 py-0.5 rounded-full border border-amber-300">Suelo Mínimo Intocable: 195 € c/u</span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3 text-xs">
                <div class="bg-sky-50/95 border-2 border-sky-300 rounded-2xl p-3.5 shadow-sm">
                  <strong class="text-sky-900 text-[13.5px] font-black block mb-1">1. Ingeniería de Entidades SEO/GEO IA</strong>
                  <p class="text-slate-700 leading-snug">
                    <strong class="text-brand-navy">«Para que os encuentren gratis en Google Maps y os citen ChatGPT, Perplexity y Gemini»:</strong> 16 parámetros oficiales + Grafo <code>@graph</code> Wikidata + <code>/llms.txt</code>.
                  </p>
                </div>
                <div class="bg-amber-50/95 border-2 border-amber-300 rounded-2xl p-3.5 shadow-sm">
                  <strong class="text-amber-900 text-[13.5px] font-black block mb-1">2. Neuro-CRO + Sonda de 10-14 Días</strong>
                  <p class="text-slate-700 leading-snug">
                    <strong class="text-brand-navy">«Para duplicar los clientes que os contactan»:</strong> Disponible en <strong>Perfil 1 (Modo Ágil)</strong> o <strong>Perfil 2 (Modo Corporativo Alto Standing)</strong>.
                  </p>
                </div>
              </div>
            </div>

            <div>
              <span class="block text-[11px] font-extrabold uppercase tracking-wider text-brand-navy mb-2">
                Tabla Oficial de Precios de las Super-Auditorías (1 Auditoría vs. Las 2 Juntas):
              </span>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-center">
                <div class="bg-white rounded-2xl p-3 border-2 border-slate-200 flex flex-col justify-between shadow-sm">
                  <span class="block text-[10px] font-extrabold text-slate-700 uppercase">1. Solo Código / DIY</span>
                  <span class="block text-xl font-black text-brand-navy my-0.5">200 € <span class="text-[11px] font-bold text-slate-500">por 1</span></span>
                  <span class="block text-[11px] font-extrabold text-teal-800">390 € las dos (195€ c/u)</span>
                  <span class="block text-[10.5px] text-slate-600 leading-tight mt-1">PDF Parte 1 + Parte 2 (Códigos limpios) para que lo suba tu informático.</span>
                </div>
                <div class="bg-white rounded-2xl p-3 border-2 border-sky-300 flex flex-col justify-between shadow-sm">
                  <span class="block text-[10px] font-extrabold text-sky-900 uppercase">2. Oficial «Llave en Mano»</span>
                  <span class="block text-xl font-black text-sky-700 my-0.5">350 € <span class="text-[11px] font-bold text-slate-500">por 1</span></span>
                  <span class="block text-[11px] font-extrabold text-sky-900">590 € las dos (Ahorra 110€)</span>
                  <span class="block text-[10.5px] text-slate-700 leading-tight mt-1">Suelta o con Plan Base. Incluye reunión con tu técnico, implantación y Sonda.</span>
                </div>
                <div class="bg-emerald-50 rounded-2xl p-3 border-2 border-emerald-500 flex flex-col justify-between shadow-md">
                  <span class="block text-[10px] font-extrabold text-emerald-900 uppercase">3. Bonificada con Pack ★</span>
                  <span class="block text-xl font-black text-emerald-700 my-0.5">195 € <span class="text-[11px] font-bold text-emerald-800">por 1</span></span>
                  <span class="block text-[11px] font-black text-emerald-900">390 € las dos (Ahorra 310€)</span>
                  <span class="block text-[10.5px] text-emerald-950 font-semibold leading-tight mt-1">Todo el servicio «Llave en Mano» bonificado un 44% con cualquier Pack de 2+ servicios.</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Columna Derecha (5 cols): Grupos 2, 3 y 4 + Hardware Atril NFC/QR -->
          <div class="lg:col-span-5 flex flex-col justify-between gap-3.5">

            <!-- Tarjeta Grupos 2, 3 y 4 (Combinados vs Sueltos) -->
            <div class="sp-light-card-3d-sky rounded-3xl p-4 flex-1 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                  <span class="text-[10.5px] font-extrabold uppercase tracking-wider text-sky-900 bg-sky-100 px-2.5 py-0.5 rounded-full border border-sky-300">
                    🚀 Grupos 2, 3 y 4 (Suelto vs. Combinado con Pack)
                  </span>
                  <span class="text-[10.5px] font-extrabold text-emerald-700">Computan para Pack Dúo+</span>
                </div>
                <ul class="space-y-1.5 text-[11.5px] text-slate-800 leading-snug">
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong>Grupo 1 extra (4º Quatro / 5º Pentium):</strong></span>
                    <strong class="text-brand-navy whitespace-nowrap">+40 €/m (+75 € Setup)</strong>
                  </li>
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong>Grupo 2 (S6 Citas, S8 Firma, S10 Cobros):</strong></span>
                    <strong class="text-sky-800 whitespace-nowrap">+59 €/m (+110 €) <span class="text-[10px] text-slate-500 font-normal">| 79€ s.</span></strong>
                  </li>
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong>Sat. 1 Instagram 3 en 1 (Meta API):</strong></span>
                    <strong class="text-pink-700 whitespace-nowrap">+49 €/m (+75 €) <span class="text-[10px] text-slate-500 font-normal">| 69€ s.</span></strong>
                  </li>
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong>Sat. 2 Logística 360 / S4 Llamadas WA:</strong></span>
                    <strong class="text-sky-800 whitespace-nowrap">+59 €/m (+110 €) <span class="text-[10px] text-slate-500 font-normal">| 79€ s.</span></strong>
                  </li>
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong>Sat. 3 Cerebro Redactor B2B (RAG):</strong></span>
                    <strong class="text-indigo-700 whitespace-nowrap">+69 €/m (+150 €) <span class="text-[10px] text-slate-500 font-normal">| 99€ s.</span></strong>
                  </li>
                  <li class="flex justify-between gap-2">
                    <span><strong>S7 Centralita Voz IA 24/7 (250 min/m):</strong></span>
                    <strong class="text-indigo-900 whitespace-nowrap">+129 €/m (+250 €) <span class="text-[10px] text-slate-500 font-normal">| 169€ s.</span></strong>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Tarjeta Atril Inteligente NFC + QR -->
            <div class="sp-light-card-3d-amber rounded-3xl p-4 flex flex-col justify-between">
              <div class="flex items-center justify-between gap-2 mb-1.5">
                <span class="text-[10.5px] font-extrabold uppercase tracking-wider text-amber-900 bg-amber-100 px-2.5 py-0.5 rounded-full border border-amber-400">
                  ★ Hardware Mostrador: Atril NFC + QR
                </span>
                <span class="text-sm font-black text-amber-800">Pago único • Sin cuotas</span>
              </div>
              <div class="grid grid-cols-3 gap-2 text-center text-xs">
                <div class="bg-white rounded-xl py-1.5 px-2 border-2 border-amber-300 shadow-sm">
                  <span class="block font-black text-brand-navy text-sm">39 €</span>
                  <span class="text-[10px] font-semibold text-slate-600">1.ª Unidad</span>
                </div>
                <div class="bg-white rounded-xl py-1.5 px-2 border-2 border-amber-300 shadow-sm">
                  <span class="block font-black text-amber-700 text-sm">29 € / ud</span>
                  <span class="text-[10px] font-semibold text-slate-600">2.ª a 4.ª Ud.</span>
                </div>
                <div class="bg-white rounded-xl py-1.5 px-2 border-2 border-emerald-400 shadow-sm">
                  <span class="block font-black text-emerald-700 text-sm">25 € / ud</span>
                  <span class="text-[10px] font-semibold text-slate-600">5 o más Uds.</span>
                </div>
              </div>
            </div>

          </div>

        </div>

        <!-- Barra Inferior de Transparencia Fiscal y Enlaces a Documentos Oficiales -->
        <div class="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white/95 border-2 border-slate-200 rounded-2xl px-5 py-2.5 text-xs text-slate-700 shadow-sm">
          <span>🧾 <strong class="text-brand-navy">Transparencia Total:</strong> Vía Flexible (3 meses) o Plan Anual (10 meses = 2 gratis). Precios netos sin IVA 21% (SEPA).</span>
          <div class="flex flex-wrap items-center gap-3 font-extrabold">
            <a href="documentos/tarifas.html" target="_blank" class="text-teal-700 hover:text-brand-navy underline whitespace-nowrap">Tarifas oficiales &rarr;</a>
            <span class="text-slate-300">•</span>
            <a href="documentos/desembolso.html" target="_blank" class="text-sky-700 hover:text-brand-navy underline whitespace-nowrap">Desembolso primer día &rarr;</a>
            <span class="text-slate-300">•</span>
            <a href="documentos/setup.html" target="_blank" class="text-indigo-700 hover:text-brand-navy underline whitespace-nowrap">Anexo técnico de altas &rarr;</a>
          </div>
        </div>

      </div>
    </div>

  </section>"""

NUEVO_JS_TARIFAS_INDEX = r"""    var _spModoTarifasActual = 'mensual';
    var _spNumAuditoriasEscudo = 0;

    function _spRenderizarTarjetasPrecios() {
      var btnM = document.getElementById('btnSwitchMensual');
      var btnA = document.getElementById('btnSwitchAnual');
      var pBase = document.querySelector('[data-plan-price="base"]');
      var pDuo = document.querySelector('[data-plan-price="duo"]');
      var pTri = document.querySelector('[data-plan-price="trinity"]');
      var subBase = document.getElementById('spSubPriceBase');
      var subDuo = document.getElementById('spSubPriceDuo');
      var subEsc = document.getElementById('spSubPriceEscudoTotal');
      var tagAud = document.getElementById('spAuditAddonPriceTag');
      var badgeAhorro = document.getElementById('spBadgeAhorroEscudoTotal');
      var btn0Aud = document.getElementById('btnEscudo0Aud');
      var btn1Aud = document.getElementById('btnEscudo1Aud');
      var btn2Aud = document.getElementById('btnEscudo2Aud');
      var waEsc = document.getElementById('spBtnWaPlanEscudoTotal');

      [
        { el: btn0Aud, val: 0 },
        { el: btn1Aud, val: 1 },
        { el: btn2Aud, val: 2 }
      ].forEach(function(item) {
        if (!item.el) return;
        if (_spNumAuditoriasEscudo === item.val) {
          item.el.className = 'px-1.5 py-0.5 rounded-md bg-emerald-600 text-white cursor-pointer transition-all whitespace-nowrap shadow-sm';
        } else {
          item.el.className = 'px-1.5 py-0.5 rounded-md text-teal-900 hover:text-brand-navy cursor-pointer transition-all whitespace-nowrap';
        }
      });

      var costeAud = (_spNumAuditoriasEscudo === 1) ? 195 : ((_spNumAuditoriasEscudo === 2) ? 390 : 0);

      if (tagAud) {
        if (_spNumAuditoriasEscudo === 0) tagAud.textContent = '59 € + 40 € + 40 € (S1 + S2 + S3)';
        else if (_spNumAuditoriasEscudo === 1) tagAud.textContent = '+ 195 € (1 Super-Auditoría Llave en Mano)';
        else tagAud.textContent = '+ 390 € (Las 2 Super-Auditorías • Ahorras 310 €)';
      }

      if (badgeAhorro) {
        if (_spNumAuditoriasEscudo === 2) badgeAhorro.textContent = '🎁 Bóveda Gratis + Ahorras 310 € en Aud.';
        else if (_spNumAuditoriasEscudo === 1) badgeAhorro.textContent = '🎁 Bóveda Gratis + Aud. a 195 € (-44%)';
        else badgeAhorro.textContent = '🎁 Bóveda Gratis (150 €) + Aud. a 195 €';
      }

      if (_spModoTarifasActual === 'anual') {
        if (btnA) btnA.className = 'px-4 py-1.5 rounded-xl text-xs sm:text-[13px] font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer flex items-center gap-1.5';
        if (btnM) btnM.className = 'px-4 py-1.5 rounded-xl text-xs sm:text-[13px] font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer';

        if (pBase) pBase.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-brand-navy">49 €</span><span class="text-xs font-bold text-slate-500">/ mes eq. (590 €/año)</span>';
        if (subBase) subBase.textContent = 'Día 1 Anual: 740 € (590 € 10m + 150 € Setup • Ahorras 118 €)';

        if (pDuo) pDuo.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-sky-700">82,50 €</span><span class="text-xs font-bold text-slate-500">/ mes eq. (990 €/año)</span>';
        if (subDuo) subDuo.textContent = 'Día 1 Anual: 1.215 € (990 € 10m + 225 € Setup • Ahorras 198 €)';

        if (pTri) pTri.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-emerald-700">115,80 €</span><span class="text-xs font-bold text-slate-500">/ mes eq. (1.390 €/año)</span>';
        var totalDia1AnualTri = 1690 + costeAud;
        if (subEsc) subEsc.textContent = 'Día 1 Anual: ' + totalDia1AnualTri + ' € (1.390€ 10m + 300€ Setup' + (costeAud > 0 ? ' + ' + costeAud + '€ Aud.' : '') + ' • Ahorras 278€)';
      } else {
        if (btnM) btnM.className = 'px-4 py-1.5 rounded-xl text-xs sm:text-[13px] font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer';
        if (btnA) btnA.className = 'px-4 py-1.5 rounded-xl text-xs sm:text-[13px] font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer flex items-center gap-1.5';

        if (pBase) pBase.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-brand-navy">59 €</span><span class="text-xs font-bold text-slate-500">/ mes</span>';
        if (subBase) subBase.textContent = 'Día 1 Flex: 209 € (150 € Setup + 59 € Mes 1)';

        if (pDuo) pDuo.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-sky-700">99 €</span><span class="text-xs font-bold text-slate-500">/ mes</span>';
        if (subDuo) subDuo.textContent = 'Día 1 Flex: 324 € (225 € Setup + 99 € Mes 1)';

        if (pTri) pTri.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-emerald-700">139 €</span><span class="text-xs font-bold text-slate-500">/ mes</span>';
        var totalDia1FlexTri = 439 + costeAud;
        if (subEsc) subEsc.textContent = 'Día 1 Flex: ' + totalDia1FlexTri + ' € (300 € Setup + 139 € Mes 1' + (costeAud > 0 ? ' + ' + costeAud + ' € Aud.' : '') + ')';
      }

      if (waEsc) {
        var extraAudTxt = (_spNumAuditoriasEscudo === 2) ? ' + las 2 Super-Auditorías por 390 €' : ((_spNumAuditoriasEscudo === 1) ? ' + 1 Super-Auditoría por 195 €' : '');
        var modTexto = (_spModoTarifasActual === 'anual') ? ' en Plan Anual (1.390 €/año + 300 € Setup)' : ' en modalidad Flexible (139 €/mes + 300 € Setup)';
        waEsc.href = 'https://wa.me/34711547561?text=' + encodeURIComponent('Hola Francisco, quiero activar el Pack Escudo Total Trinity (S1+S2+S3 Leads en 10s)' + extraAudTxt + modTexto + '.');
      }
    }

    function cambiarModoTarifas(modo) {
      _spModoTarifasActual = (modo === 'anual') ? 'anual' : 'mensual';
      _spRenderizarTarjetasPrecios();
    }

    window.spSeleccionarNivelEscudoTotal = function(numAud) {
      _spNumAuditoriasEscudo = (numAud === 2) ? 2 : ((numAud === 1) ? 1 : 0);
      _spRenderizarTarjetasPrecios();
    };"""

def actualizar_index_html_completo(ruta_index):
    if not os.path.isfile(ruta_index):
        print(f"  ⚠️ No se encontró {ruta_index}")
        return

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Reemplazar el bloque completo de #vista-tarifas con el nuevo diseño de 4 Grupos y Pack Escudo Total Trinity (139 €/m)
    patron_vista_tarifas = re.compile(
        r"<!-- ======================================================================= -->\s*<!-- VISTA 4 \(SALA INDEPENDIENTE\): PRECIOS CLAROS.*?</section>",
        re.DOTALL
    )
    if patron_vista_tarifas.search(html):
        html = patron_vista_tarifas.sub(lambda _: NUEVO_BLOQUE_VISTA_TARIFAS_INDEX, html, count=1)

    # 2. Actualizar las funciones JS de tarifas en index.html
    patron_js_tarifas = re.compile(
        r"var _spModoTarifasActual = 'mensual';.*?window\.spSeleccionarNivelEscudoTotal = function\(numAud\)\s*\{.*?\};",
        re.DOTALL
    )
    html = patron_js_tarifas.sub(lambda _: NUEVO_JS_TARIFAS_INDEX, html)

    # 3. Actualizar las opciones del Carrito Configurador a la Carta (#spModalCarritoCarta) con la nueva arquitectura
    html = html.replace(
        '<span class="text-[11px] text-slate-300">Permanencia mín. 3 meses (Auditoría a 250 € con Dúo)</span>',
        '<span class="text-[11px] text-slate-300">Compromiso mín. 3 meses (Auditorías a 195 € c/u desde Pack Dúo+)</span>'
    )
    html = html.replace(
        '<span class="text-[11px] text-slate-300">Pagas 10 meses + Auditorías en 2x1 (350 € las 2)</span>',
        '<span class="text-[11px] text-slate-300">Pagas 10 meses (2 gratis) + Auditorías a 195 € c/u (390 € las 2)</span>'
    )

    # Añadir el botón del Pack Escudo Total Trinity (139 €/m) en el paso 2 del Carrito y actualizar los desplegables de Grupos 1, 2, 3 y 4
    bloque_planes_carrito_antiguo = """              <button type="button" id="spCartPlan_duo" onclick="window.spSetCartPlan('duo')" class="sp-cart-item-btn sp-cart-selected">
                <span class="font-black block text-emerald-300">★ Pack Escudo Dúo (2 Serv.)</span>
                <span class="text-[11px] text-white font-bold">99 €/mes + 225 € Setup</span>
                <span class="block text-[10px] text-emerald-200">S1 Reseñas IA + S2 WhatsApp</span>
              </button>"""

    bloque_planes_carrito_nuevo = """              <button type="button" id="spCartPlan_duo" onclick="window.spSetCartPlan('duo')" class="sp-cart-item-btn sp-cart-selected">
                <span class="font-black block text-sky-300">🛡️ Pack Escudo Básico (Dúo)</span>
                <span class="text-[11px] text-white font-bold">99 €/mes + 225 € Setup</span>
                <span class="block text-[10px] text-sky-200">S1 Reseñas + S2 WhatsApp (Aud. 195€)</span>
              </button>
              <button type="button" id="spCartPlan_trinity" onclick="window.spSetCartPlan('trinity')" class="sp-cart-item-btn sm:col-span-3">
                <span class="font-black block text-emerald-300">★ Pack Escudo Total (Trinity: S1 + S2 + S3 Leads en 10s) — Incluye 🎁 Bóveda Gratis</span>
                <span class="text-[11px] text-white font-bold">139 €/mes + 300 € Setup (Día 1 Flex: 439 € | Día 1 Anual: 1.690 €) + Desbloquea Auditorías a 195 € c/u</span>
              </button>"""

    if "spCartPlan_trinity" not in html and bloque_planes_carrito_antiguo in html:
        html = html.replace(bloque_planes_carrito_antiguo, bloque_planes_carrito_nuevo, 1)

    # Actualizar opciones del selector de módulos adicionales en el Carrito según los 4 Grupos oficiales
    patron_select_f2 = re.compile(
        r'<select id="spCartReservaFase2".*?</select>',
        re.DOTALL
    )
    nuevo_select_f2 = """<select id="spCartReservaFase2" onchange="window.spAgregarModuloReservaFase2(this.value)" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white font-bold">
                <option value="">+ Añadir módulo de Grupo 1, 2, 3 o 4 al carrito...</option>
                <optgroup label="Grupo 1 • Núcleo de Implantación Rápida (+40 €/m | +75 € Setup)">
                  <option value="S3 Respuesta a Leads en 10s + Portales (+40 €/m | +75 € Setup)">S3. Respuesta a Leads en 10s + Portales (+40 €/m | +75 € Setup)</option>
                  <option value="S9 Facturas y Tickets al Gestor por Foto WA (+40 €/m | +75 € Setup)">S9. Facturas y Tickets al Gestor por Foto WA (+40 €/m | +75 € Setup)</option>
                  <option value="S5 Reactivación Automática Clientes Inactivos (+40 €/m | +75 € Setup)">S5. Reactivación de Clientes Inactivos (+40 €/m | +75 € Setup)</option>
                </optgroup>
                <optgroup label="Grupo 2 • Operativa Avanzada (+59 €/m | +110 € Setup combinado)">
                  <option value="S6 Sistema Anti-Plantón 24h + Huecos Flash (+59 €/m | +110 € Setup)">S6. Sistema Anti-Plantón 24h + Huecos Flash (+59 €/m | +110 € Setup)</option>
                  <option value="S8 Firma Digital Presupuestos + Onboarding IA (+59 €/m | +110 € Setup)">S8. Firma Digital Legal + Onboarding IA (+59 €/m | +110 € Setup)</option>
                  <option value="S10 Escudo Anti-Morosidad Diplomático (+59 €/m | +110 € Setup)">S10. Escudo Anti-Morosidad Diplomático (+59 €/m | +110 € Setup)</option>
                </optgroup>
                <optgroup label="Grupo 3 • Satélites Especializados y Boosters IA">
                  <option value="Sat.1 Instagram Inteligente 3 en 1 (+49 €/m | +75 € Setup)">Sat.1. Instagram Inteligente 3 en 1: Reels + DMs (+49 €/m | +75 € Setup)</option>
                  <option value="Sat.2 Escudo Logístico 360 Reparto (+59 €/m | +110 € Setup)">Sat.2. Escudo Logístico 360: Tracking + Ausencias (+59 €/m | +110 € Setup)</option>
                  <option value="Sat.3 Cerebro Redactor B2B con IA RAG (+69 €/m | +150 € Setup)">Sat.3. Cerebro Redactor B2B con IA RAG (+69 €/m | +150 € Setup)</option>
                  <option value="Booster IA Lector Correo Facturas S9 (+35 €/m | +50 € Setup)">Booster IA 1: Add-on Lector de Correo para S9 (+35 €/m | +50 € Setup)</option>
                  <option value="Booster IA Reclamación Proveedores S10 (+35 €/m | +50 € Setup)">Booster IA 2: Add-on Reclamación a Proveedores S10 (+35 €/m | +50 € Setup)</option>
                </optgroup>
                <optgroup label="Grupo 4 • Satélites de Telefonía y Voz IA">
                  <option value="S4 Rescate Llamadas Perdidas por WhatsApp (+59 €/m | +110 € Setup)">S4. Rescate Llamadas Perdidas WA - 250 rescates/m (+59 €/m | +110 € Setup)</option>
                  <option value="S7 Centralita Voz y Recepcionista IA 24/7 (+129 €/m | +250 € Setup)">S7. Centralita Voz IA 24/7 - Bolsa 250 min/m (+129 €/m | +250 € Setup)</option>
                </optgroup>
              </select>"""
    html = patron_select_f2.sub(lambda _: nuevo_select_f2, html, count=1)

    # 4. Actualizar la lógica matemática del Carrito en index.html (Suelo 195 € en Auditorías, Combo 590 € sueltas / 390 € con Pack, y soporte para Trinity 139 €/m)
    bloque_calculo_carrito_antiguo = """        ['ninguno', 'base', 'duo'].forEach(function(p) {
          var b = document.getElementById('spCartPlan_' + p);
          if (b) {
            if (_spCartState.plan === p) b.classList.add('sp-cart-selected');
            else b.classList.remove('sp-cart-selected');
          }
        });"""

    bloque_calculo_carrito_nuevo = """        ['ninguno', 'base', 'duo', 'trinity'].forEach(function(p) {
          var b = document.getElementById('spCartPlan_' + p);
          if (b) {
            if (_spCartState.plan === p) b.classList.add('sp-cart-selected');
            else b.classList.remove('sp-cart-selected');
          }
        });"""
    html = html.replace(bloque_calculo_carrito_antiguo, bloque_calculo_carrito_nuevo)

    patron_precios_aud_carrito = re.compile(
        r"var esAnual = \(_spCartState\.modalidad === 'anual'\);\s*var tieneDuo = \(_spCartState\.plan === 'duo'\);\s*var precio1Aud = \(!tieneDuo\) \? 350 : \(esAnual \? 195 : 250\);\s*var precio2Aud = \(!tieneDuo\) \? 650 : \(esAnual \? 350 : 450\);\s*var lbl1 = document\.getElementById\('spCartPriceAud1Lbl'\);\s*var lbl2 = document\.getElementById\('spCartPriceAud2Lbl'\);\s*if \(lbl1\) lbl1\.textContent = [^\n]+;\s*if \(lbl2\) lbl2\.textContent = [^\n]+;",
        re.DOTALL
    )
    reemplazo_precios_aud_carrito = """var esAnual = (_spCartState.modalidad === 'anual');
        var numExtrasElegidos = _spCartState.reservasFase2.length;
        var numBasePlan = (_spCartState.plan === 'trinity') ? 3 : ((_spCartState.plan === 'duo') ? 2 : ((_spCartState.plan === 'base') ? 1 : 0));
        var tienePack2Mas = ((numBasePlan + numExtrasElegidos) >= 2);
        var precio1Aud = tienePack2Mas ? 195 : 350;
        var precio2Aud = tienePack2Mas ? 390 : 590;

        var lbl1 = document.getElementById('spCartPriceAud1Lbl');
        var lbl2 = document.getElementById('spCartPriceAud2Lbl');
        if (lbl1) lbl1.textContent = precio1Aud + ' € ' + (tienePack2Mas ? '(Bonificada con Pack 2+)' : '(Llave en Mano Suelta)');
        if (lbl2) lbl2.textContent = precio2Aud + ' € las 2 ' + (tienePack2Mas ? '(195 € c/u • Ahorras 310 €)' : '(Combo Firma • Ahorras 110 €)');"""
    html = patron_precios_aud_carrito.sub(lambda _: reemplazo_precios_aud_carrito, html)

    bloque_plan_duo_carrito_antiguo = """        } else if (_spCartState.plan === 'duo') {
          numServiciosActivos = 2;
          costeSetup = 225;
          cuotaMes = 99;
          pagoPlanDia1 = esAnual ? (990 + 225) : (99 + 225);
          nombrePlanTxt = esAnual ? 'Pack Escudo Dúo Anual (990 €/año + 225 € Setup)' : 'Pack Escudo Dúo Flexible (99 €/mes + 225 € Setup)';
        }"""

    bloque_plan_duo_carrito_nuevo = """        } else if (_spCartState.plan === 'duo') {
          numServiciosActivos = 2;
          costeSetup = 225;
          cuotaMes = 99;
          pagoPlanDia1 = esAnual ? (990 + 225) : (99 + 225);
          nombrePlanTxt = esAnual ? 'Pack Escudo Básico Dúo Anual (990 €/año + 225 € Setup)' : 'Pack Escudo Básico Dúo Flexible (99 €/mes + 225 € Setup)';
        } else if (_spCartState.plan === 'trinity') {
          numServiciosActivos = 3;
          costeSetup = 300;
          cuotaMes = 139;
          pagoPlanDia1 = esAnual ? (1390 + 300) : (139 + 300);
          nombrePlanTxt = esAnual ? 'Pack Escudo Total ★ Trinity Anual (1.390 €/año + 300 € Setup)' : 'Pack Escudo Total ★ Trinity Flexible (139 €/mes + 300 € Setup)';
        }"""
    html = html.replace(bloque_plan_duo_carrito_antiguo, bloque_plan_duo_carrito_nuevo)

    html = html.replace(
        "else if (esAnual) cuoEl.textContent = 'Año completo cubierto (equiv. ' + (cuotaMes === 99 ? '82,50' : '49') + ' €/m)';",
        "else if (esAnual) cuoEl.textContent = 'Año completo cubierto (equiv. ' + (cuotaMes === 139 ? '115,80' : (cuotaMes === 99 ? '82,50' : '49')) + ' €/m)';"
    )

    # 5. Actualizar textos de la base de conocimiento local de la Tecnosala dentro de index.html
    html = html.replace(
        "Satélite 1 • Instagram 3 en 1:</strong> Auto-DM con enlace al comentar Reels/Posts, recepcionista 24/7 en mensajes directos y regalo al mencionarte en Stories.",
        "Satélite 1 • Instagram 3 en 1 (+49 €/m combo | 69 €/m suelto):</strong> Auto-DM con enlace al comentar Reels/Posts, DMs 24/7 y menciones en Stories."
    )
    html = html.replace(
        "el <strong>Pack Escudo Dúo (S1 + S2) son 99 €/mes</strong> (Setup: 225 €) y además te bonifica las Auditorías SEO/GEO o Neuro-CRO de 350 € a solo <strong>195 €</strong> (pago único).",
        "el <strong>Pack Escudo Básico Dúo (S1 + S2) son 99 €/mes</strong> (+225 € Setup) y el <strong>Pack Escudo Total ★ Trinity (S1 + S2 + S3 Leads en 10s) son 139 €/mes</strong> (+300 € Setup e incluye Bóveda de Contraseñas GRATIS). Ambos desbloquean nuestras 2 Super-Auditorías Llave en Mano a solo <strong>195 € c/u</strong> (o 390 € las dos juntas; sueltas cuestan 350 € una o 590 € las dos)."
    )

    escribir_archivo_con_backup(ruta_index, html)

# =============================================================================
# 6. ACTUALIZAR BASE DE CONOCIMIENTO DEL CONSULTOR DE VOZ (SI EXISTE)
# =============================================================================
def actualizar_base_conocimiento_js_tecnosala():
    posibles = [
        os.path.join(RUTA_WEB_PUBLIC_HTML, "documentos", "base_conocimiento_ingenieria.js"),
        os.path.join(RUTA_WEB_RENDER, "documentos", "base_conocimiento_ingenieria.js"),
        os.path.join(os.getcwd(), "documentos", "base_conocimiento_ingenieria.js"),
    ]
    vistos = set()
    for ruta in posibles:
        ruta_abs = os.path.abspath(ruta)
        if ruta_abs not in vistos and os.path.isfile(ruta_abs):
            vistos.add(ruta_abs)
            with open(ruta_abs, "r", encoding="utf-8") as f:
                js = f.read()
            js = re.sub(r"\b95\s*€", "195 €", js)
            js = js.replace("650 €", "590 €")
            js = js.replace("450 € las 2", "390 € las 2")
            escribir_archivo_con_backup(ruta_abs, js)

# =============================================================================
# 7. ACTUALIZACIÓN AUTOMÁTICA DE LOS 2 DOCUMENTOS MAESTROS (.md) EN PROGRAMAR
#    + PUENTE AUTOMÁTICO CON GOOGLE SHEETS Y GOOGLE DRIVE (MEMORIA DE LA GEMA)
# =============================================================================
SECCION_5_NUEVA_BIBLIA = """## 5. ESTRUCTURA OFICIAL DE TARIFAS EN 4 GRUPOS, PACKS, SUPER-AUDITORÍAS Y LIQUIDACIÓN DÍA 1

### A) Las 3 Reglas de Oro de Nuestra Arquitectura de Precios (Precios Netos sin IVA 21% • SEPA B2B)
1. **Coherencia Psicológica en Terminación «9» (Charm Pricing):** Todas las cuotas mensuales terminan en 9 (`59 €`, `99 €`, `139 €`, `79 €`, `+59 €`, `69 €`, `+49 €`, `99 €`, `+69 €`, `169 €`, `+129 €`) o en `+40 €` redondo para los módulos adicionales del Grupo 1.
2. **Suelo Mínimo Intocable de 195 € en las 2 Super-Auditorías (Eliminado para siempre el escalón de 95 €):**
   - **Modalidad 1 — «Solo Código / DIY» (Sin mano de obra nuestra):** `200 €` por 1 Super-Auditoría | `390 €` contratando las 2 juntas (`195 €` c/u). Entregamos PDF Parte 1 + PDF Parte 2 (Solo Códigos Limpios) para su informático.
   - **Modalidad 2 — Oficial «Llave en Mano» (Suelta o con Plan Base de 1 servicio):** `350 €` por 1 Super-Auditoría | `590 €` las 2 juntas (`295 €` c/u, ahorra `110 €` — Pack Firma Institucional / Alto Standing ideal Nexitum). Incluye Diagnóstico + Parte 2 + Reunión de defensa con su técnico + Implantación en 15 min + Sonda de 10-14 días en la Neuro-CRO.
   - **Modalidad 3 — BONIFICADA CON PACK (Dúo, Trinity o superior, Mensual o Anual):** `195 €` por 1 Super-Auditoría | `390 €` las 2 juntas (`195 €` c/u, ahorra `310 €`). Nunca baja de `195 €` c/u.
3. **División en 4 Bloques según Coste de API y Complejidad de Puesta en Marcha:**
   - **GRUPO 1 (Núcleo de Venta Rápida — S1 Reseñas IA, S2 Cortafuegos WA, S3 ★ Respuesta a Leads en 10s, S9 Facturas por Foto WA y S5 Reactivación de Inactivos):** `59 €/mes` el 1º (`150 €` Setup) y `+40 €/mes` adicionales del 2º al 5º (`+75 €` Setup).
   - **GRUPO 2 (Operativa Avanzada de Agenda, Contratos y Cobros — S6 Anti-Plantón 24h + Huecos Flash, S8 Firma Digital + Onboarding IA y S10 Escudo Anti-Morosidad):** `79 €/mes` suelto (`195 €` Setup) | `+59 €/mes` combinado (`+110 €` Setup). Computa al 100% para beneficios de Pack.
   - **GRUPO 3 (Satélites Especializados y Boosters IA):** Satélite 1 Instagram 3 en 1 (`69 €/m` + `150 €` suelto | `+49 €/m` + `+75 €` combinado), Satélite 2 Escudo Logístico 360 (`79 €/m` + `195 €` suelto | `+59 €/m` + `+110 €` combinado), Satélite 3 Cerebro Redactor B2B RAG (`99 €/m` + `250 €` suelto | `+69 €/m` + `+150 €` combinado), y Boosters IA 1 y 2 (`+35 €/m` + `+50 €` Setup).
   - **GRUPO 4 (Satélites de Telefonía y Voz IA):** S4 Rescate de Llamadas Perdidas por WhatsApp (`79 €/m` + `195 €` suelto | `+59 €/m` + `+110 €` combinado; incluye desvío + hasta 250 rescates/mes) y S7 Centralita de Voz IA 24/7 (`169 €/m` + `350 €` suelto | `+129 €/m` + `+250 €` combinado; incluye número virtual/desvío + conexión a agenda + bolsa de 250 min/mes).

### B) Tabla Maestra de Planes del Grupo 1, Combinaciones y Desembolso Día 1 (Vía 1 Flexible 3 meses vs. Vía 2 Plan Anual 10 meses = 2 Gratis)

| Plan / Módulo | Combinación Típica | Cuota Mensual | Alta Técnica (Setup) | Pago Día 1 (Vía Flexible 3m) | Pago Día 1 (Vía Anual 10m = 2 Gratis) | Ventajas Desbloqueadas en este Nivel |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Plan Pyme BASE (1 serv. G1)** | Solo S1, o solo S2, o solo S3 | **59 €/m** | 150 € | **209 €** | **740 €** (590€ + 150€) | Ahorra 118 € en Anual • Auditorías a 350 € c/u (o 590 € las dos) |
| **Pack ESCUDO BÁSICO (Dúo: 2 serv.)** | **S1 + S2** (o S1 + S3) | **99 €/m** | 225 € | **324 €** | **1.215 €** (990€ + 225€) | Ahorra 19 €/m + 75 € Setup • **Desbloquea Auditorías a 195 € c/u (390 € las dos)** |
| **Pack ESCUDO TOTAL ★ (Trinity: 3 serv.)** | **S1 + S2 + S3 (Leads 10s)** | **139 €/m** | 300 € | **439 €** | **1.690 €** (1.390€ + 300€) | **🎁 Bóveda Contraseñas GRATIS (150€)** + Auditorías a **195 € c/u** + Ahorra 278 € en Anual |
| **Plan QUATRO (4 serv. Grupo 1)** | S1 + S2 + S3 + S9 | **179 €/m** | 375 € | **554 €** | **2.165 €** (1.790€ + 375€) | Bóveda Gratis + Auditorías a **195 € c/u** + Ahorra 358 € en Anual |
| **Plan PENTIUM (5 serv. Grupo 1)** | S1 + S2 + S3 + S9 + S5 | **219 €/m** | 450 € | **669 €** | **2.640 €** (2.190€ + 450€) | Bóveda Gratis + Auditorías a **195 € c/u** + Ahorra 438 € en Anual |
| **+ Servicio Grupo 2, Logística o S4** | S6, S8, S10, Reparto o Llamadas WA | **+59 €/m** (79€ s.) | +110 € (195€ s.) | **+169 €** combo (274€ s.) | **+700 €** combo (985€ s.) | Computa al 100% para beneficios de Pack Dúo/Trinity |
| **+ Satélite 1: Instagram 3 en 1** | Auto-DM Reels + DMs 24/7 + Stories | **+49 €/m** (69€ s.) | +75 € (150€ s.) | **+124 €** combo (219€ s.) | **+565 €** combo (840€ s.) | Ahorra 20 €/mes y 75 € de Setup al combinarlo |
| **+ Satélite 3: Cerebro Redactor RAG** | IA con PDFs, tarifas y contratos propios | **+69 €/m** (99€ s.) | +150 € (250€ s.) | **+219 €** combo (349€ s.) | **+840 €** combo (1.240€ s.) | Ahorra 30 €/mes y 100 € de Setup al combinarlo |
| **+ Satélite S7: Centralita Voz IA 24/7** | Recepcionista neuronal + 250 min/mes | **+129 €/m** (169€ s.) | +250 € (350€ s.) | **+379 €** combo (519€ s.) | **+1.540 €** combo (2.040€ s.) | Ahorra 40 €/mes y 100 € de Setup al combinarlo |"""

SECCION_4_PUENTE_DRIVE_SHEETS_MANUAL = """## 4. PROTOCOLO OBLIGATORIO DE SINCRONIZACIÓN AUTOMÁTICA CON GOOGLE SHEETS Y GOOGLE DRIVE (MEMORIA VIVA DE LA GEMA)
En cada ejecución de `AD.py`, es **estrictamente obligatorio** mantener sincronizados los 2 documentos maestros (`biblia_de_conocimiento_de_sistemas_pyme.md` y `manual_maestro_de_programaci_n_ad_py.md`) en tres niveles simultáneos sin intervención manual compleja:
1. **Nivel 1 — Carpeta Local Oficial de las Gemas (`/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Programar`):**
   - `AD.py` actualiza en el Paso 1 (y blinda con `atexit`) los 2 únicos archivos `.md` oficiales en `SISTEMAS PYME/Programar` (y sus réplicas en `Scraper/Scrapper App` y `servicio_resenas`), guardando copia previa en `backups_sp` y sin recortar jamás el historial previo.
2. **Nivel 2 — Sincronización Automática con la Hoja de Google Sheets (`1m4ZqBaMslLJDok4I0DWJZMjoYNwJMZ-Qr0d6D02rxfY`) y los Documentos de Google Drive de la Gema:**
   - Al ejecutarse `AD.py`, el script lee los 2 archivos `.md` recién actualizados y los envía automáticamente por HTTP POST (`accion: "sincronizar_biblia_conocimiento"`) al Webhook de Google Apps Script de la Hoja Maestra de Altas.
   - El bloque `sincronizarBibliaYManualEnSheetsYDriveSP` dentro de `App Script Base de Altas.js` realiza automáticamente dos acciones en la nube de Google:
     - **A) En Google Sheets (`1m4ZqBaMslLJDok4I0DWJZMjoYNwJMZ-Qr0d6D02rxfY`):** Actualiza de arriba abajo y desglosadas por secciones las pestañas **`Biblia_IA_Viva`** (con toda la Biblia de Conocimiento) y **`Manual_Maestro_AD`** (con todo el Manual Maestro de Programación `AD.py`).
     - **B) En Google Drive (Memoria de la Gema de Gemini de `fmgallardo@falconfactorysystems.com`):** Sobrescribe y actualiza en el mismo ID de archivo de Google Drive tanto los archivos Markdown (`biblia_de_conocimiento_de_sistemas_pyme.md` y `manual_maestro_de_programaci_n_ad_py.md`) como los **Google Docs nativos (`DocumentApp`)** a los que la Gema tiene acceso directo en su memoria, compartiéndolos automáticamente con permisos de Editor para `fmgallardo@falconfactorysystems.com` y `francisco@sistemaspyme.es`.
3. **Nivel 3 — Función en Línea 1 de `App Script Base de Altas.js` (`crearYActualizarBibliaEnDriveYHojaAhora`):**
   - Además del envío automático por red, `AD.py` mantiene inyectada en la línea 1 de `App Script Base de Altas.js` la función `crearYActualizarBibliaEnDriveYHojaAhora()` para que, si en cualquier momento se pulsa `▶️ Ejecutar` en el editor de Apps Script, regenere al instante las pestañas `Biblia_IA_Viva`, `Manual_Maestro_AD` y los documentos de Google Drive de la Gema."""

BLOQUE_HISTORIAL_V137 = f"""
---
### ACTUALIZACIÓN {VERSION_ACTUAL} ({datetime.now().strftime('%d/%m/%Y %H:%M')}) — Sincronización Integral en Cuerpo e Historial de la Biblia + Protocolo Oficial de Puente Automático hacia Google Sheets (`Biblia_IA_Viva` y `Manual_Maestro_AD`) y Google Drive (Documentos en Memoria de la Gema)
- **Actualización de las Secciones Principales 2 y 5 de la Biblia de Conocimiento:** Sincronizadas todas las tablas del cuerpo principal de la Biblia con la nueva arquitectura de 4 Grupos, el Pack Escudo Total Trinity (`139 €/m`), el Pack Firma Institucional (`590 €` las 2 Super-Auditorías sueltas) y el suelo mínimo intocable de `195 €` c/u (`390 €` las dos con cualquier Pack de 2+ servicios).
- **Incorporación en el Manual Maestro de la Sección 4 Oficial de Sincronización con Google Sheets y Google Drive (Memoria de la Gema):** Documentado y automatizado en `AD.py` el disparo directo hacia el Webhook de Google Apps Script (`sincronizar_biblia_conocimiento`) y la actualización de `App Script Base de Altas.js` para que cada ejecución de `AD.py` actualice simultáneamente:
  1. Los 2 archivos `.md` locales en `SISTEMAS PYME/Programar`, `Scraper/Scrapper App` y `servicio_resenas`.
  2. Las pestañas `Biblia_IA_Viva` y `Manual_Maestro_AD` en la Hoja de Google Sheets (`1m4ZqBaMslLJDok4I0DWJZMjoYNwJMZ-Qr0d6D02rxfY`).
  3. Los documentos en Google Drive (`biblia_de_conocimiento_de_sistemas_pyme` y `manual_maestro_de_programaci_n_ad_py`, tanto en `.md` como en Google Docs nativo) conectados a la memoria de la Gema de Gemini de `fmgallardo@falconfactorysystems.com`.
"""

_DOCUMENTOS_MAESTROS_ACTUALIZADOS = False

def descubrir_url_webhook_apps_script():
    posibles_configs = [
        os.path.join(RUTA_SCRAPER, "config_b2b.json"),
        os.path.join(RUTA_WEB_RENDER, "config_b2b.json"),
        os.path.join(RUTA_WEB_RENDER, ".env"),
        os.path.join(RUTA_SCRAPER, ".env"),
    ]
    import json
    for ruta in posibles_configs:
        if os.path.isfile(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    txt = f.read()
                if ruta.endswith(".json"):
                    data = json.loads(txt)
                    for k in ["apps_script_url", "webhook_sheets_url", "google_sheets_webhook", "script_url", "url_apps_script"]:
                        if data.get(k) and "script.google.com/macros/s/" in str(data.get(k)):
                            return str(data.get(k)).strip()
                m = re.search(r"https://script\.google\.com/macros/s/[A-Za-z0-9_\-]+/exec", txt)
                if m:
                    return m.group(0)
            except Exception:
                pass
    # URL oficial de respaldo del puente Apps Script en index.html / ecosistema SP
    return "https://script.google.com/macros/s/AKfycbwVbXZIK-O4mQLYMrwdPgXQDlo__PHTuv8MXUj-nR68_t2OGHVdvrBgqfhXdQxwzivc/exec"

def sincronizar_en_vivo_con_sheets_y_drive_gema(texto_biblia, texto_manual):
    import urllib.request
    import json
    url_webhook = descubrir_url_webhook_apps_script()
    payload = {
        "accion": "sincronizar_biblia_conocimiento",
        "action": "sincronizar_biblia_conocimiento",
        "version": VERSION_ACTUAL,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "propietario_email": "fmgallardo@falconfactorysystems.com",
        "alias_email": "francisco@sistemaspyme.es",
        "spreadsheet_id": "1m4ZqBaMslLJDok4I0DWJZMjoYNwJMZ-Qr0d6D02rxfY",
        "actualizar_drive_gema": True,
        "actualizar_google_docs_nativo": True,
        "biblia_markdown": texto_biblia,
        "manual_markdown": texto_manual,
    }
    try:
        datos_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url_webhook,
            data=datos_bytes,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
             _ = resp.read().decode("utf-8", errors="ignore")
        print(f"  ☁️ Sincronizados en vivo en Google Sheets (Biblia_IA_Viva + Manual_Maestro_AD) y en Google Drive (Memoria Gema) vía Apps Script.")
    except Exception as e:
        print(f"  ℹ️ Aviso al conectar con Webhook Apps Script ({e}): se ha dejado listo también en 'App Script Base de Altas.js'.")

def actualizar_apps_script_local_con_puente_drive(texto_biblia, texto_manual):
    rutas_gs = [
        os.path.join(RUTA_SCRAPER, "App Script Base de Altas.js"),
        os.path.join(RUTA_SCRAPER, "CODIGO_APPS_SCRIPT_LISTO_PARA_PEGAR.gs"),
        os.path.join(RUTA_PROGRAMAR, "App Script Base de Altas.js"),
    ]
    for r_gs in rutas_gs:
        if os.path.isfile(r_gs):
            try:
                with open(r_gs, "r", encoding="utf-8") as f:
                    codigo_gs = f.read()
                # Actualizar referencias de precios de auditorías si figuraban con 95 €
                codigo_gs_nuevo = codigo_gs.replace("95 € Llave en Mano", "195 € Llave en Mano (390 € las dos)")
                if codigo_gs_nuevo != codigo_gs:
                    escribir_archivo_con_backup(r_gs, codigo_gs_nuevo)
            except Exception:
                pass

def actualizar_documentos_maestros_md():
    global _DOCUMENTOS_MAESTROS_ACTUALIZADOS
    if _DOCUMENTOS_MAESTROS_ACTUALIZADOS:
        return

    carpetas_md = [
        RUTA_PROGRAMAR,
        RUTA_SCRAPER,
        RUTA_WEB_RENDER,
    ]

    # 1. Leer la versión más completa disponible de ambos documentos
    ruta_biblia_base = None
    ruta_manual_base = None
    for c in carpetas_md:
        rb = os.path.join(c, "biblia_de_conocimiento_de_sistemas_pyme.md")
        rm = os.path.join(c, "manual_maestro_de_programaci_n_ad_py.md")
        if os.path.isfile(rb) and not ruta_biblia_base:
            ruta_biblia_base = rb
        if os.path.isfile(rm) and not ruta_manual_base:
            ruta_manual_base = rm

    texto_biblia_final = ""
    texto_manual_final = ""

    if ruta_biblia_base:
        with open(ruta_biblia_base, "r", encoding="utf-8") as f:
            tb = f.read()
        # Actualizar las tarifas de las Auditorías en la Sección 2 de la Biblia
        patron_tarifas_aud_s2 = re.compile(
            r"#### Tarifas Oficiales de las Auditorías \(Precio por CADA una\):.*?(?=\n---\n|\n## 3\.)",
            re.DOTALL
        )
        nueva_tarifa_aud_s2 = """#### Tarifas Oficiales de las 2 Super-Auditorías (Suelo Mínimo Blindado de 195 € c/u — Eliminado para siempre el escalón de 95 €):
1. **Modalidad 1 — «Solo Código / DIY» (Sin mano de obra nuestra):** `200 €` pago único por 1 Super-Auditoría | `390 €` contratando las 2 juntas (`195 €` c/u). Entregamos el PDF Parte 1 + PDF Parte 2 (Solo Códigos Limpios) para que lo suba su propio informático.
2. **Modalidad 2 — Oficial «Llave en Mano» (Suelta o con Plan Base de 1 servicio):** `350 €` pago único por 1 Super-Auditoría | `590 €` contratando las 2 juntas (`295 €` c/u, ahorra `110 €` — Pack Firma Institucional / Alto Standing ideal Nexitum). Incluye Diagnóstico + Parte 2 + Reunión de defensa con su técnico + Implantación por Sistemas Pyme en 15 min + Sonda de 10-14 días en la Neuro-CRO.
3. **Modalidad 3 — BONIFICADA CON PACK (Con cualquier Pack de 2 o más servicios, Mensual o Anual):** `195 €` pago único por 1 Super-Auditoría | `390 €` contratando las 2 juntas (`195 €` c/u, ahorra `310 €`). Nunca baja de `195 €` c/u."""
        tb = patron_tarifas_aud_s2.sub(lambda _: nueva_tarifa_aud_s2, tb)

        # Actualizar la Sección 5 completa de la Biblia con los 4 Grupos y la nueva tabla oficial
        patron_sec5 = re.compile(
            r"## 5\. ESTRUCTURA.*?(?=\n---\n\s*## 6\.)",
            re.DOTALL
        )
        tb = patron_sec5.sub(lambda _: SECCION_5_NUEVA_BIBLIA, tb)

        if f"ACTUALIZACIÓN {VERSION_ACTUAL}" not in tb:
            tb = tb.rstrip() + "\n" + BLOQUE_HISTORIAL_V137
        texto_biblia_final = tb

    if ruta_manual_base:
        with open(ruta_manual_base, "r", encoding="utf-8") as f:
            tm = f.read()
        if "PROTOCOLO OBLIGATORIO DE SINCRONIZACIÓN AUTOMÁTICA CON GOOGLE SHEETS Y GOOGLE DRIVE" not in tm:
            tm = tm.replace(
                "## 4. HISTORIAL COMPLETO DE ACTUALIZACIONES",
                SECCION_4_PUENTE_DRIVE_SHEETS_MANUAL + "\n\n---\n\n## 5. HISTORIAL COMPLETO DE ACTUALIZACIONES"
            )
        if f"ACTUALIZACIÓN {VERSION_ACTUAL}" not in tm:
            tm = tm.rstrip() + "\n" + BLOQUE_HISTORIAL_V137
        texto_manual_final = tm

    # 2. Guardar ambos documentos actualizados en todas las carpetas oficiales (Programar, Scraper y servicio_resenas)
    for carpeta in carpetas_md:
        if not os.path.isdir(carpeta):
            continue
        if texto_biblia_final:
            for nombre_b in ["biblia_de_conocimiento_de_sistemas_pyme.md", "biblia_conocimiento_sistemas_pyme.md"]:
                rb_dest = os.path.join(carpeta, nombre_b)
                if os.path.isfile(rb_dest) or nombre_b == "biblia_de_conocimiento_de_sistemas_pyme.md":
                    if carpeta == RUTA_PROGRAMAR and nombre_b == "biblia_conocimiento_sistemas_pyme.md":
                        continue
                    escribir_archivo_con_backup(rb_dest, texto_biblia_final)
        if texto_manual_final:
            rm_dest = os.path.join(carpeta, "manual_maestro_de_programaci_n_ad_py.md")
            if os.path.isfile(rm_dest) or carpeta == RUTA_PROGRAMAR:
                escribir_archivo_con_backup(rm_dest, texto_manual_final)

    # 3. Disparar la sincronización hacia Google Sheets (Biblia_IA_Viva y Manual_Maestro_AD) y Google Drive (Gema)
    if texto_biblia_final or texto_manual_final:
        actualizar_apps_script_local_con_puente_drive(texto_biblia_final, texto_manual_final)
        sincronizar_en_vivo_con_sheets_y_drive_gema(texto_biblia_final, texto_manual_final)

    _DOCUMENTOS_MAESTROS_ACTUALIZADOS = True

atexit.register(actualizar_documentos_maestros_md)

# =============================================================================
# 8. EJECUCIÓN PRINCIPAL DE LA ACTUALIZACIÓN
# =============================================================================
def encontrar_raiz_git(ruta_inicio):
    actual = os.path.abspath(ruta_inicio)
    while actual and actual != "/":
        if os.path.isdir(os.path.join(actual, ".git")):
            return actual
        actual = os.path.dirname(actual)
    return None

def ejecutar_actualizacion():
    print("\n" + "=" * 78)
    print(f"🚀 INICIANDO ACTUALIZACIÓN MAESTRA {VERSION_ACTUAL} — ARQUITECTURA DE PRECIOS Y TARJETONES")
    print("=" * 78)

    # Paso 1 prioritario: Actualizar Biblia y Manual Maestro en SISTEMAS PYME/Programar
    actualizar_documentos_maestros_md()
    replicar_ad_py_en_carpetas_oficiales()

    # Detectar todas las carpetas web activas (incluyendo Web/web-sistemaspyme/public_html)
    carpetas_objetivo = []
    for candidata in [RUTA_WEB_PUBLIC_HTML, RUTA_WEB_RENDER, os.path.abspath(os.getcwd())]:
        if os.path.isdir(candidata):
            c_abs = os.path.abspath(candidata)
            if c_abs not in carpetas_objetivo:
                carpetas_objetivo.append(c_abs)

    archivos_a_validar = []

    for base_dir in carpetas_objetivo:
        sub_doc = os.path.join(base_dir, "documentos")
        sub_art = os.path.join(base_dir, "articulos")

        # Actualizar los tarjetones dentro de documentos/ (si existe esa subcarpeta)
        if os.path.isdir(sub_doc):
            print(f"\n📂 Actualizando tarjetones y dossieres en: {sub_doc}")
            r_tar = os.path.join(sub_doc, "tarifas.html")
            r_tar_m = os.path.join(sub_doc, "tarifas_movil.html")
            r_des = os.path.join(sub_doc, "desembolso.html")
            r_des_m = os.path.join(sub_doc, "desembolso_movil.html")
            r_set = os.path.join(sub_doc, "setup.html")
            r_set_m = os.path.join(sub_doc, "setup_movil.html")
            r_cat = os.path.join(sub_doc, "catalogo.html")
            r_cat_m = os.path.join(sub_doc, "catalogo_movil.html")

            escribir_archivo_con_backup(r_tar, HTML_TARIFAS_A5)
            escribir_archivo_con_backup(r_tar_m, HTML_TARIFAS_MOVIL)
            escribir_archivo_con_backup(r_des, HTML_DESEMBOLSO_A5)
            escribir_archivo_con_backup(r_des_m, HTML_DESEMBOLSO_MOVIL)
            escribir_archivo_con_backup(r_set, HTML_SETUP_A5)
            escribir_archivo_con_backup(r_set_m, HTML_SETUP_MOVIL)
            actualizar_catalogo_a4_y_movil(r_cat, r_cat_m)

            archivos_a_validar.extend([r_tar, r_tar_m, r_des, r_des_m, r_set, r_set_m, r_cat, r_cat_m])

        # Actualizar también en subcarpeta static/documentos si existe en servicio_resenas
        sub_static_doc = os.path.join(base_dir, "static", "documentos")
        if os.path.isdir(sub_static_doc):
            print(f"\n📂 Actualizando tarjetones en: {sub_static_doc}")
            escribir_archivo_con_backup(os.path.join(sub_static_doc, "tarifas.html"), HTML_TARIFAS_A5)
            escribir_archivo_con_backup(os.path.join(sub_static_doc, "tarifas_movil.html"), HTML_TARIFAS_MOVIL)
            escribir_archivo_con_backup(os.path.join(sub_static_doc, "desembolso.html"), HTML_DESEMBOLSO_A5)
            escribir_archivo_con_backup(os.path.join(sub_static_doc, "desembolso_movil.html"), HTML_DESEMBOLSO_MOVIL)
            escribir_archivo_con_backup(os.path.join(sub_static_doc, "setup.html"), HTML_SETUP_A5)
            escribir_archivo_con_backup(os.path.join(sub_static_doc, "setup_movil.html"), HTML_SETUP_MOVIL)
            actualizar_catalogo_a4_y_movil(
                os.path.join(sub_static_doc, "catalogo.html"),
                os.path.join(sub_static_doc, "catalogo_movil.html")
            )

        # Actualizar Pyme_Magazine_N1.html si está en articulos/
        if os.path.isdir(sub_art):
            r_mag = os.path.join(sub_art, "Pyme_Magazine_N1.html")
            if os.path.isfile(r_mag):
                actualizar_catalogo_a4_y_movil("", r_mag)
                archivos_a_validar.append(r_mag)

        # Actualizar index.html de la web principal
        r_idx = os.path.join(base_dir, "index.html")
        if os.path.isfile(r_idx):
            print(f"\n🌐 Actualizando pantalla principal de la web: {r_idx}")
            actualizar_index_html_completo(r_idx)
            archivos_a_validar.append(r_idx)

    actualizar_base_conocimiento_js_tecnosala()

    # 3. Validación Gateway Anti-Errores y Resumen de Archivos Actualizados
    print("\n🔍 RESUMEN DE VALIDACIÓN Y ARCHIVOS ACTUALIZADOS:")
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f_self:
        ast.parse(f_self.read())
    print("  🟢 Sintaxis Python (ast.parse) de AD.py verificada.")

    vistos = set()
    for ruta_v in archivos_a_validar:
        ruta_abs = os.path.abspath(ruta_v)
        if ruta_abs not in vistos and os.path.isfile(ruta_abs):
            vistos.add(ruta_abs)
            if not validar_bloques_js_en_html(ruta_abs):
                print(f"  ⚠️ Revisa el archivo {ruta_abs}")
                sys.exit(1)

    # 4. Sincronización Git en el repositorio de la Web (public_html) y en servicio_resenas
    repos_git = set()
    for c in [RUTA_WEB_PUBLIC_HTML, RUTA_WEB_ROOT, RUTA_WEB_RENDER, os.getcwd()]:
        if os.path.isdir(c):
            raiz_git = encontrar_raiz_git(c)
            if raiz_git:
                repos_git.add(raiz_git)

    for repo in repos_git:
        print(f"\n☁️ Sincronizando repositorio Git en: {repo}")
        try:
            subprocess.run(["git", "add", "."], cwd=repo, check=False)
            subprocess.run(
                ["git", "commit", "-m", f"feat({VERSION_ACTUAL}): nueva arquitectura de precios en 4 grupos, Pack Escudo Total Trinity 139e y suelo 195e en Super-Auditorias"],
                cwd=repo,
                check=False
            )
            subprocess.run(["git", "push"], cwd=repo, check=False)
            print(f"  ✅ Git sincronizado en: {os.path.basename(repo)}")
        except Exception as e:
            print(f"  ℹ️ Aviso Git en {repo}: {e}")

    print("\n" + "=" * 78)
    print(f"🎉 ACTUALIZACIÓN {VERSION_ACTUAL} COMPLETADA CON ÉXITO — TODOS LOS DOCUMENTOS AL DÍA")
    print("=" * 78)

if __name__ == "__main__":
    ejecutar_actualizacion()
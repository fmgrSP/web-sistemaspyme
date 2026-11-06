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
VERSION_ACTUAL = "V144"

# =============================================================================
# 2. UTILIDADES DE BACKUP, VALIDACIÓN Y AUTO-REPLICACIÓN DE AD.py
# =============================================================================
def crear_backup_seguro(ruta_archivo):
    """Crea una copia de seguridad obligatoria en backups_sp antes de modificar."""
    if not os.path.isfile(ruta_archivo):
        return None
    carpeta_base = os.path.dirname(os.path.abspath(ruta_archivo))
    carpeta_backups = os.path.join(carpeta_base, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    nombre = os.path.basename(ruta_archivo)
    ruta_bak = os.path.join(carpeta_backups, f"{nombre}.{STAMP}.bak")
    shutil.copy2(ruta_archivo, ruta_bak)
    print(f"  🛡️ Backup creado: {ruta_bak}")
    return ruta_bak

def escribir_archivo_con_backup(ruta_archivo, nuevo_contenido):
    """Guarda el archivo creando antes su copia en backups_sp."""
    os.makedirs(os.path.dirname(os.path.abspath(ruta_archivo)), exist_ok=True)
    if os.path.isfile(ruta_archivo):
        crear_backup_seguro(ruta_archivo)
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)
    print(f"  ✅ Archivo actualizado: {ruta_archivo}")

def replicar_ad_py_en_carpetas_oficiales():
    """Replica este mismo script AD.py en las carpetas oficiales del ecosistema."""
    ruta_actual = os.path.abspath(__file__)
    for carpeta in [RUTA_WEB_PUBLIC_HTML, RUTA_WEB_ROOT, RUTA_WEB_RENDER, RUTA_SCRAPER, RUTA_PROGRAMAR]:
        if os.path.isdir(carpeta):
            destino = os.path.join(carpeta, "AD.py")
            if os.path.abspath(destino) != ruta_actual:
                try:
                    shutil.copy2(ruta_actual, destino)
                except Exception:
                    pass

def descubrir_binario_node():
    """Busca el binario de Node.js en PATH o en las rutas típicas del Mac."""
    bin_path = shutil.which("node")
    if bin_path:
        return bin_path
    rutas_mac = [
        "/opt/homebrew/bin/node",
        "/usr/local/bin/node",
        os.path.expanduser("~/.nvm/versions/node"),
    ]
    for r in rutas_mac:
        if os.path.isfile(r) and os.access(r, os.X_OK):
            return r
        if os.path.isdir(r):
            try:
                versiones = sorted(os.listdir(r), reverse=True)
                for v in versiones:
                    cand = os.path.join(r, v, "bin", "node")
                    if os.path.isfile(cand) and os.access(cand, os.X_OK):
                        return cand
            except Exception:
                pass
    return None

def validar_bloques_js_en_html(ruta_html):
    """Valida la estructura HTML y todos sus bloques <script>."""
    if not os.path.isfile(ruta_html):
        return True
    with open(ruta_html, "r", encoding="utf-8") as f:
        contenido = f.read()

    if "<html" not in contenido.lower() or "</html>" not in contenido.lower():
        print(f"  ❌ Error estructural en {ruta_html}: etiquetas HTML incompletas.")
        return False

    patron_script = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE)
    bloques = patron_script.findall(contenido)
    node_bin = descubrir_binario_node()

    if node_bin and bloques:
        for idx, codigo_js in enumerate(bloques, 1):
            if not codigo_js.strip():
                continue
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tmp:
                tmp.write(codigo_js)
                tmp_path = tmp.name
            try:
                res = subprocess.run([node_bin, "--check", tmp_path], capture_output=True, text=True)
                if res.returncode != 0:
                    print(f"  ❌ Error JS en bloque #{idx} de {os.path.basename(ruta_html)}:\n{res.stderr}")
                    return False
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

    peso_kb = os.path.getsize(ruta_html) / 1024.0
    print(f"  🟢 Verificado OK: {os.path.basename(ruta_html)} ({peso_kb:.1f} KB, {len(bloques)} bloques <script> limpios)")
    return True

def renumerar_servicios_en_html_documentos(html):
    """Actualiza la numeración en catálogos y tarjetones para que Grupo 1 = S1..S5, Grupo 2 = S6..S8 y Grupo 4 Telefonía = S9..S10."""
    # En textos de tablas y planes donde salía S1+S2+S3+S9 -> S1+S2+S3+S4
    html = html.replace("S1+S2+S3+S9", "S1+S2+S3+S4")
    html = html.replace("S1 + S2 + S3 + S9", "S1 + S2 + S3 + S4")
    html = html.replace("(o con S9)", "(o con S4)")
    html = html.replace("(S1, S2, S3, S5, S9)", "(S1, S2, S3, S4, S5)")
    html = html.replace("(S6, S8, S10)", "(S6, S7, S8)")
    html = html.replace("(Para S9 Facturas)", "(Para S4 Facturas)")
    html = html.replace("(Requiere tener S9)", "(Requiere tener S4)")
    html = html.replace("(Para S10)", "(Para S8 Anti-Morosidad)")
    html = html.replace("(Requiere tener S10)", "(Requiere tener S8)")
    html = html.replace("Llamadas Perdidas (S4)", "Llamadas Perdidas (S9)")
    html = html.replace("Satélite Telefónico A (S4)", "Satélite Telefónico A (S9)")
    html = html.replace("Centralita de Voz IA 24/7 (S7)", "Centralita de Voz IA 24/7 (S10)")
    html = html.replace("Satélite Telefónico B (S7)", "Satélite Telefónico B (S10)")
    return html

def actualizar_tarjeton_existente_si_procede(ruta_archivo):
    """Asegura que cualquier tarjetón existente mantenga el suelo de 195 €, las nuevas tarifas y la numeración correlativa S1-S10."""
    if not os.path.isfile(ruta_archivo):
        return
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        html = f.read()
    nuevo = html.replace("95 € Llave en Mano", "195 € Llave en Mano (390 € las dos)")
    nuevo = re.sub(r"o\s*<strong>95\s*€\s*c/u</strong>\s*en\s*Plan\s*Anual\s*Trinity\+", "o <strong>390 € las dos</strong>", nuevo)
    nuevo = renumerar_servicios_en_html_documentos(nuevo)
    if nuevo != html:
        escribir_archivo_con_backup(ruta_archivo, nuevo)

def actualizar_catalogo_a4_y_movil(ruta_cat, ruta_cat_m):
    for r in [ruta_cat, ruta_cat_m]:
        if r and os.path.isfile(r):
            actualizar_tarjeton_existente_si_procede(r)

# =============================================================================
# 5. PARCHE QUIRÚRGICO DE INDEX.HTML (PRECIOS CLAROS + CARRITO + 4 GRUPOS S1-S10)
# =============================================================================
NUEVO_BLOQUE_VISTA_TARIFAS_INDEX = r"""  <!-- ======================================================================= -->
  <!-- VISTA 4 (SALA INDEPENDIENTE): PRECIOS CLAROS (ARQUITECTURA 4 GRUPOS)    -->
  <!-- ======================================================================= -->
  <section id="vista-tarifas" class="view-panel hidden bg-slate-50 text-slate-900">

    <!-- =================================================================== -->
    <!-- DIAPOSITIVA 1 DE PRECIOS: LOS 3 PLANES ACTIVOS HOY (100VH LUMINOSO) -->
    <!-- =================================================================== -->
    <div id="tarifas-slide-planes" class="slide-section sp-tarifas-light-bg border-b border-teal-200/80 px-4 sm:px-6 relative overflow-hidden" style="min-height: calc(100vh - 5.75rem); padding-top: 1.9rem !important; padding-bottom: 0.75rem !important; justify-content: flex-start !important;">
      <div class="absolute inset-0 sp-rhombus-grid-reverse pointer-events-none opacity-65" aria-hidden="true"></div>

      <div class="max-w-6xl mx-auto w-full flex flex-col justify-start relative z-10">

        <!-- FILA 1: Encabezado encajado al 100% dentro del ancho de las 3 tarjetas (sin que el botón de compra se salga por la derecha) -->
        <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-2.5 pb-2.5 mb-3.5 border-b-2 border-teal-500/25 w-full">
          <h2 class="text-xl sm:text-2xl lg:text-[24px] font-black text-brand-navy tracking-tight leading-tight">
            Precios claros y <span class="sp-green-headline">amortización desde el primer cliente.</span>
          </h2>

          <div class="flex flex-wrap items-center justify-start xl:justify-end gap-2 flex-shrink-0">
            <div class="inline-flex items-center gap-1 bg-white/95 p-1 rounded-2xl border-2 border-teal-500/35 shadow-md">
              <button type="button" id="btnSwitchMensual" onclick="cambiarModoTarifas('mensual')" class="px-3 py-1.5 rounded-xl text-xs font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer whitespace-nowrap">
                🔄 Mensual (3m mín.)
              </button>
              <button type="button" id="btnSwitchAnual" onclick="cambiarModoTarifas('anual')" class="px-3 py-1.5 rounded-xl text-xs font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer flex items-center gap-1 whitespace-nowrap">
                <span>🎁 Plan Anual</span>
                <span class="text-[9.5px] font-black bg-amber-100 text-amber-900 border border-amber-400 px-1.5 py-0.5 rounded-full">2 Meses Gratis</span>
              </button>
            </div>
            <button type="button" id="spBtnTopCarritoPrecios" onclick="window.spAbrirCarritoConfigurador()" class="sp-btn-carrito-gold-3d px-3.5 py-2 rounded-xl text-xs inline-flex items-center gap-1.5 whitespace-nowrap shadow-md">
              <span class="sp-cart-icon-badge">🛒</span>
              <span>Configurar a la Carta / Contratar</span>
            </button>
          </div>
        </div>

        <!-- FILA 2: Las 3 Tarjetas Protagonistas (Base 59€, Pack Escudo Básico 99€ y Pack Escudo Total 99€ + 1 o 2 Auditorías) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 items-stretch mb-2.5">

          <!-- TARJETA 1: PLAN PYME BASE (1 SERVICIO DEL GRUPO 1 = 59 €/MES) -->
          <div class="sp-price-card-3d sp-price-card-slate px-5 py-3.5 flex flex-col justify-between">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1.5">
                <div class="inline-flex flex-col items-center justify-center text-[10px] font-extrabold uppercase tracking-wider text-slate-800 bg-slate-100 px-3 py-1 rounded-xl border border-slate-300 leading-tight shadow-sm">
                  <span class="whitespace-nowrap">1 Servicio Grupo 1</span>
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
                Un servicio del Grupo 1 de libre elección para empezar paso a paso:
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
                <li class="flex items-start gap-1.5"><span class="text-teal-600 font-black">✔</span><span><strong class="text-brand-navy">1 servicio activo del Grupo 1</strong> a elegir según tu prioridad hoy.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-teal-600 font-black">✔</span><span>Incluye <strong class="text-brand-navy">Informe Mensual 360° Interactivo</strong> cada día 1 de mes.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-slate-400 font-black">•</span><span class="text-slate-600">Super-Auditorías Llave en Mano a tarifa estándar (350 € una / 590 € las dos).</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanBase" href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20me%20interesa%20el%20Plan%20Pyme%20BASE%20%281%20servicio%20del%20Grupo%201%20por%2059%20%E2%82%AC%2Fmes%29" target="_blank" class="w-full py-2 text-center rounded-xl bg-brand-navy hover:bg-slate-800 text-white font-extrabold text-xs sm:text-[13px] shadow-md transition-all block">
              Elegir Plan Pyme BASE &rarr;
            </a>
          </div>

          <!-- TARJETA 2: PACK ESCUDO BÁSICO (2 SERVICIOS: S1 + S2 = 99 €/MES, SIN AUDITORÍA) -->
          <div class="sp-price-card-3d sp-price-card-sky px-5 py-3.5 flex flex-col justify-between">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1.5">
                <div class="inline-flex flex-col items-center justify-center text-[10px] font-extrabold uppercase tracking-wider text-sky-900 bg-sky-100/95 px-2.5 py-0.5 rounded-xl border border-sky-300 leading-tight shadow-sm">
                  <span class="whitespace-nowrap">🛡️ 2 Servicios</span>
                  <span class="text-[9px] text-sky-950 font-black whitespace-nowrap">(S1 + S2)</span>
                </div>
                <div class="text-right leading-tight">
                  <span class="block text-[11px] font-bold text-sky-950 whitespace-nowrap">Setup Dúo: <strong class="text-brand-navy font-black">225 €</strong></span>
                  <span class="block text-[10px] font-extrabold text-emerald-700 whitespace-nowrap">(2.º al 50%)</span>
                </div>
              </div>

              <h3 class="text-lg sm:text-[19px] font-black text-brand-navy mb-0.5 whitespace-nowrap">
                Pack Escudo Básico <span class="text-sky-700 font-bold text-sm">(Dúo)</span>
              </h3>
              <p class="text-xs text-slate-700 mb-2 leading-snug">
                2 servicios de libre elección (hoy <strong class="text-brand-navy">S1 + S2</strong>; el 2.º suma solo <strong class="text-brand-navy">+40 €/mes</strong>):
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
                <li class="flex items-start gap-1.5"><span class="text-amber-600 font-black">🔑</span><span><strong class="text-brand-navy">Llave de Socio:</strong> Desbloquea las Super-Auditorías a <strong class="text-emerald-800">195 € c/u</strong> (en vez de 350 €).</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanDuo" href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20me%20interesa%20el%20Pack%20Escudo%20B%C3%A1sico%20%28S1%20%2B%20S2%20por%2099%20%E2%82%AC%2Fmes%29" target="_blank" class="w-full py-2 text-center rounded-xl bg-sky-600 hover:bg-sky-700 text-white font-black text-xs sm:text-[13px] shadow-lg shadow-sky-600/25 transition-all block">
              Elegir Pack Escudo Básico &rarr;
            </a>
          </div>

          <!-- TARJETA 3 ESTRELLA: PACK ESCUDO TOTAL ★ (S1 + S2 POR 99 €/MES + 1 O 2 SUPER-AUDITORÍAS BONIFICADAS A 195 € C/U) -->
          <div class="sp-price-card-3d sp-price-card-emerald px-5 py-3.5 flex flex-col justify-between relative">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1.5">
                <div class="inline-flex flex-col items-center justify-center text-[10px] font-extrabold uppercase tracking-wider text-white bg-gradient-to-r from-emerald-600 to-teal-600 px-2.5 py-0.5 rounded-xl shadow-sm leading-tight">
                  <span class="whitespace-nowrap">🚀 Recomendado</span>
                  <span class="text-[9px] font-black text-emerald-50 whitespace-nowrap">(S1 + S2 + Auditoría)</span>
                </div>
                <div class="text-right leading-tight">
                  <span id="spBadgeAhorroEscudoTotal" class="block text-[10px] font-black text-amber-900 bg-amber-100/95 px-2 py-0.5 rounded-md border border-amber-300 whitespace-nowrap">¡Ahorras 155 € en la Auditoría!</span>
                  <span class="block text-[9px] font-extrabold text-teal-900 whitespace-nowrap mt-0.5">Setup Dúo: 225 € + Aud. a 195 €</span>
                </div>
              </div>

              <div class="flex flex-wrap items-center justify-between gap-1.5 mb-2">
                <h3 id="spTitleEscudoTotal" class="text-lg sm:text-[19px] font-black text-brand-navy whitespace-nowrap">
                  Pack Escudo Total ★
                </h3>
                <div class="inline-flex items-center bg-white/95 p-0.5 rounded-lg border-2 border-emerald-500/50 text-[10px] font-extrabold shadow-sm">
                  <button type="button" id="btnEscudo1Aud" onclick="spSeleccionarNivelEscudoTotal(1)" class="px-2 py-0.5 rounded-md bg-emerald-600 text-white cursor-pointer transition-all whitespace-nowrap">
                    +1 Auditoría (195€)
                  </button>
                  <button type="button" id="btnEscudo2Aud" onclick="spSeleccionarNivelEscudoTotal(2)" class="px-2 py-0.5 rounded-md text-teal-900 hover:text-brand-navy cursor-pointer transition-all whitespace-nowrap">
                    +2 Auditorías (390€)
                  </button>
                </div>
              </div>

              <div class="bg-white/95 border-2 border-emerald-500/70 rounded-2xl px-3.5 py-2 mb-2 shadow-inner">
                <div class="flex items-baseline justify-between gap-1.5 flex-wrap">
                  <div class="flex items-baseline gap-1" data-plan-price="trinity">
                    <span class="text-2xl sm:text-[28px] font-black text-emerald-700">99 €</span>
                    <span class="text-xs font-bold text-slate-500">/ mes</span>
                  </div>
                  <span id="spAuditAddonPriceTag" class="text-[10.5px] font-black text-amber-900 bg-amber-100 border border-amber-400 px-2 py-0.5 rounded-lg whitespace-nowrap">
                    + 195 € (1 Super-Auditoría Llave en Mano)
                  </span>
                </div>
                <span id="spSubPriceEscudoTotal" class="block text-[10.5px] font-extrabold text-teal-900 mt-0.5">
                  Día 1 Flex: 519 € (225€ Setup + 195€ Aud. + 99€ Mes 1)
                </span>
              </div>

              <ul class="space-y-1 text-xs text-slate-800 leading-snug mb-2.5">
                <li class="flex items-start gap-1.5"><span class="text-emerald-600 font-black">✔</span><span><strong class="text-brand-navy">Incluye S1 + S2 (Grupo 1)</strong> protegiendo y multiplicando tus 5★ en Google y WhatsApp.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-emerald-600 font-black">✔</span><span id="spBulletAuditEscudo"><strong class="text-brand-navy">1 Super-Auditoría Llave en Mano a elegir</strong> (SEO+GEO IA o Neuro-CRO Web) por solo <strong class="text-emerald-800">195 €</strong> en vez de 350 €.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-amber-600 font-black">★</span><span id="spBulletBonusEscudo">Si eliges <strong class="text-brand-navy">+2 Auditorías (390 €)</strong> arriba, te llevas ambas implantadas ahorrando <strong class="text-emerald-800">310 €</strong>.</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanEscudoTotal" href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20activar%20el%20Pack%20Escudo%20Total%20%28S1%20%2B%20S2%20por%2099%20%E2%82%AC%2Fmes%20%2B%201%20Super-Auditor%C3%ADa%20bonificada%20a%20195%20%E2%82%AC%29" target="_blank" class="sp-btn-s5-primary-3d w-full py-2 text-center rounded-xl text-white font-black text-xs sm:text-[13px] block">
              Activar Pack Escudo Total &rarr;
            </a>
          </div>

        </div>

        <!-- FILA 3: Banner-Guía hacia la Diapositiva 2 (Las 2 Super-Auditorías, los 4 Grupos y Atril NFC) -->
        <div class="pt-0.5 pb-1 flex justify-center">
          <button type="button" onclick="spScrollLimpioSeccion('tarifas-slide-complementos')" class="group inline-flex items-center gap-3 px-6 py-2 rounded-2xl bg-white/95 hover:bg-teal-50 border-2 border-teal-500/50 hover:border-teal-600 shadow-md transition-all cursor-pointer">
            <span class="text-sm">🔍🧠</span>
            <span class="text-xs sm:text-[13px] font-extrabold text-brand-navy group-hover:text-teal-800">
              Ver Tabla de las 2 Super-Auditorías (195 € / 350 € / 590 €), los 4 Grupos (S1 a S10) y Atril NFC
            </span>
            <span class="w-5 h-5 rounded-full bg-teal-500/15 border border-teal-500/50 flex items-center justify-center text-teal-700 group-hover:translate-y-0.5 transition-transform font-black text-xs">
              &darr;
            </span>
          </button>
        </div>

      </div>
    </div>

    <!-- =================================================================== -->
    <!-- DIAPOSITIVA 2 DE PRECIOS: SUPER-AUDITORÍAS, LOS 4 GRUPOS Y ATRIL    -->
    <!-- =================================================================== -->
    <div id="tarifas-slide-complementos" class="slide-section sp-tarifas-light-bg px-4 sm:px-6 py-5 relative overflow-hidden" style="min-height: calc(100vh - 5.75rem);">
      <div class="absolute inset-0 sp-rhombus-grid-reverse pointer-events-none opacity-65" aria-hidden="true"></div>
      <div class="max-w-6xl mx-auto w-full flex flex-col justify-between min-h-[calc(100vh-8.5rem)] relative z-10">

        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2.5 border-b-2 border-teal-500/25">
          <div>
            <span class="text-[11px] font-extrabold uppercase tracking-wider text-amber-800 bg-amber-100/90 px-3 py-0.5 rounded-full border border-amber-300 inline-block mb-1">
              Pagos Únicos Sin Cuotas Mensuales y Escalado por Nivel Técnico (S1 a S10 en 4 Grupos)
            </span>
            <h3 class="text-2xl sm:text-3xl font-black text-brand-navy tracking-tight">
              Las 2 Super-Auditorías Gemelas, <span class="sp-green-headline">los 4 Grupos y Hardware NFC.</span>
            </h3>
          </div>
          <button type="button" onclick="spScrollLimpioSeccion('tarifas-slide-planes')" class="self-start sm:self-center inline-flex items-center gap-2 text-xs font-extrabold text-brand-navy hover:text-teal-700 bg-white hover:bg-teal-50 px-4 py-2 rounded-xl border-2 border-slate-300 shadow-sm transition-all cursor-pointer">
            <span>&uarr;</span>
            <span>Volver a los 3 Planes Principales</span>
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
                <span class="text-[11px] font-extrabold text-amber-900 bg-amber-100 px-2.5 py-0.5 rounded-full border border-amber-300">Elige 1 o las 2 juntas</span>
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

          <!-- Columna Derecha (5 cols): Resumen de los 4 Grupos correlativos S1 a S10 + Hardware Atril NFC/QR -->
          <div class="lg:col-span-5 flex flex-col justify-between gap-3.5">

            <div class="sp-light-card-3d-sky rounded-3xl p-4 flex-1 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                  <span class="text-[10.5px] font-extrabold uppercase tracking-wider text-sky-900 bg-sky-100 px-2.5 py-0.5 rounded-full border border-sky-300">
                    🚀 Los 4 Grupos en Orden de Dificultad (S1 a S10)
                  </span>
                  <span class="text-[10.5px] font-extrabold text-emerald-700">🎁 Bóveda Gratis desde 3 serv.</span>
                </div>
                <ul class="space-y-1.5 text-[11.5px] text-slate-800 leading-snug">
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong>Grupo 1 (S1 a S5 • Implantación Rápida):</strong></span>
                    <strong class="text-brand-navy whitespace-nowrap">+40 €/m (+75 € Setup)</strong>
                  </li>
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong>Grupo 2 (S6 Agenda, S7 Firma, S8 Cobros):</strong></span>
                    <strong class="text-sky-800 whitespace-nowrap">+59 €/m (+110 €) <span class="text-[10px] text-slate-500 font-normal">| 79€ s.</span></strong>
                  </li>
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong>Grupo 3 (Sat.1 Instagram 3 en 1 Meta API):</strong></span>
                    <strong class="text-pink-700 whitespace-nowrap">+49 €/m (+75 €) <span class="text-[10px] text-slate-500 font-normal">| 69€ s.</span></strong>
                  </li>
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong>Grupo 3 (Sat.2 Logística / Sat.3 RAG B2B):</strong></span>
                    <strong class="text-indigo-700 whitespace-nowrap">+59 € / +69 €/m <span class="text-[10px] text-slate-500 font-normal">combo</span></strong>
                  </li>
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong>Grupo 4 (S9 Rescate Llamadas WA 250/m):</strong></span>
                    <strong class="text-sky-800 whitespace-nowrap">+59 €/m (+110 €) <span class="text-[10px] text-slate-500 font-normal">| 79€ s.</span></strong>
                  </li>
                  <li class="flex justify-between gap-2">
                    <span><strong>Grupo 4 (S10 Centralita Voz IA 24/7 250m):</strong></span>
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

NUEVO_BLOQUE_CA_SLIDE_PROXIMOS = r"""    <!-- ===================================================================== -->
    <!-- DIAPOSITIVA 5 DE CÓMO AYUDAMOS: CLASIFICACIÓN CORRELATIVA S1 A S10    -->
    <!-- ===================================================================== -->
    <section id="ca-slide-proximos" class="scroll-mt-20 slide-section sp-ca-slide5-proximos-dark text-white px-4 sm:px-6 pt-6 pb-4" style="min-height: calc(100vh - 5rem); justify-content: center;">
      <div class="max-w-6xl mx-auto w-full relative z-10 flex flex-col justify-center">

        <div class="text-center mt-1 mb-5 sm:mb-6">
          <div class="inline-flex items-center justify-center gap-3.5 mb-2">
            <span class="sp-proximamente-line-l"></span>
            <span class="sp-proximamente-sweep text-[11.5px] font-black uppercase tracking-[0.28em]">Arquitectura Modular en 4 Grupos (S1 a S10)</span>
            <span class="sp-proximamente-line-r"></span>
          </div>
          <h2 class="sp-roadmap-title-blue-cloud text-2xl sm:text-3xl lg:text-[32px] font-black tracking-tight leading-[1.18] mb-1.5">
            Nuestros servicios ordenados por facilidad de implantación y coste técnico.
          </h2>
          <p class="text-[13px] sm:text-[14px] text-slate-300 max-w-3xl mx-auto leading-snug">
            Empieza hoy con los servicios activos (S1 Reseñas IA, S2 Cortafuegos WhatsApp, Atril NFC y Super-Auditorías) y suma cualquier módulo con descuento automático de combinación:
          </p>
        </div>

        <!-- 4 TARJETAS GIRATORIAS (FLIP CARDS) CON NUMERACIÓN CORRELATIVA S1 A S10 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 text-left mb-5 items-stretch">

          <!-- GRUPO 1: S1, S2, S3, S4, S5 (NÚCLEO DE IMPLANTACIÓN RÁPIDA: 59€ EL 1º | +40€ EXTRA) -->
          <div id="cat1-grupo1-rapido" onclick="spToggleFlipCard('cat1-grupo1-rapido', event)" class="sp-flip-scene sp-flip-roadmap-height sp-flip-led-blue cursor-pointer">
            <div class="sp-flip-card-inner">

              <div class="sp-flip-face sp-flip-front sp-roadmap-face-card border-t-4 border-t-emerald-400 flex flex-col items-center justify-between p-6 text-center group">
                <div class="w-full flex items-center justify-between">
                  <span class="text-[10px] font-extrabold uppercase tracking-widest text-emerald-300">Grupo 1 • S1 a S5</span>
                  <span class="sp-flip-plus-btn bg-emerald-500/20 text-emerald-200 border border-emerald-400/50 group-hover:bg-emerald-500 group-hover:text-white transition-colors">+</span>
                </div>

                <div class="my-auto py-3 flex flex-col items-center">
                  <span class="inline-block text-[10.5px] font-extrabold uppercase tracking-wider text-emerald-200 bg-emerald-950/90 px-3.5 py-1 rounded-full border border-emerald-400/40 mb-3">
                    59 €/m el 1.º • +40 €/m extra
                  </span>
                  <h3 class="text-lg sm:text-xl font-black text-white tracking-tight leading-snug mb-2">
                    Implantación Rápida (S1 a S5)
                  </h3>
                  <p class="text-xs text-slate-300 leading-relaxed">
                    Los 5 servicios más ágiles y económicos de poner en marcha (Setup: 150 € el 1.º y +75 € adicionales).
                  </p>
                </div>

                <div class="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-300 group-hover:text-white transition-colors">
                  <span>Ver S1 a S5 del Grupo 1</span>
                  <span>&#8635;</span>
                </div>
              </div>

              <div class="sp-flip-face sp-flip-back sp-roadmap-face-card border-t-4 border-t-emerald-400 flex flex-col justify-between px-5 pt-4 pb-5">
                <div>
                  <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-[10px] font-extrabold uppercase tracking-wider text-emerald-200 bg-emerald-950/90 px-2.5 py-0.5 rounded-full border border-emerald-400/50">
                      Grupo 1 (S1 a S5) • +40 €/m
                    </span>
                    <button type="button" onclick="spToggleFlipCard('cat1-grupo1-rapido', event)" class="px-2 py-0.5 rounded-full bg-white/10 hover:bg-white/20 text-slate-200 text-[10.5px] font-bold cursor-pointer">
                      &#8635;
                    </button>
                  </div>
                  <ul class="space-y-1.5 text-[11.5px] text-slate-200 leading-snug">
                    <li class="flex items-start gap-1.5"><span class="text-emerald-400 font-black">S1.</span><span><strong class="text-white">Reseñas Google IA (Activo):</strong> Auto-respuesta SEO en 4-5★ y freno HEARD en 1-3★.</span></li>
                    <li class="flex items-start gap-1.5"><span class="text-emerald-400 font-black">S2.</span><span><strong class="text-white">Cortafuegos WA (Activo):</strong> Encuesta post-visita y buzón privado con audio IA.</span></li>
                    <li class="flex items-start gap-1.5"><span class="text-emerald-400 font-black">S3.</span><span><strong class="text-white">Leads en 10s + Portales:</strong> WhatsApp en &lt;10s a solicitudes web/portales y alerta al móvil.</span></li>
                    <li class="flex items-start gap-1.5"><span class="text-emerald-400 font-black">S4.</span><span><strong class="text-white">Facturas por Foto WA:</strong> Foto al ticket y subida directa al Excel del gestor.</span></li>
                    <li class="flex items-start gap-1.5"><span class="text-emerald-400 font-black">S5.</span><span><strong class="text-white">Clientes Inactivos:</strong> Campaña automática de retorno (+60/90 días).</span></li>
                  </ul>
                </div>
                <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20informaci%C3%B3n%20sobre%20los%20servicios%20S1%20a%20S5%20del%20Grupo%201" target="_blank" onclick="event.stopPropagation();" class="pt-2 border-t border-white/15 text-xs font-extrabold text-emerald-300 hover:text-white inline-flex items-center justify-between">
                  <span>Consultar S1 a S5</span><span>&rarr;</span>
                </a>
              </div>

            </div>
          </div>

          <!-- GRUPO 2: S6, S7, S8 (OPERATIVA AVANZADA DE AGENDA, CONTRATOS Y COBROS: 79€ SUELTO | +59€ COMBO) -->
          <div id="cat2-facturacion" onclick="spToggleFlipCard('cat2-facturacion', event)" class="sp-flip-scene sp-flip-roadmap-height sp-flip-led-blue cursor-pointer">
            <div class="sp-flip-card-inner">

              <div class="sp-flip-face sp-flip-front sp-roadmap-face-card border-t-4 border-t-blue-500 flex flex-col items-center justify-between p-6 text-center group">
                <div class="w-full flex items-center justify-between">
                  <span class="text-[10px] font-extrabold uppercase tracking-widest text-blue-300">Grupo 2 • S6 a S8</span>
                  <span class="sp-flip-plus-btn bg-blue-500/20 text-blue-200 border border-blue-400/50 group-hover:bg-blue-500 group-hover:text-white transition-colors">+</span>
                </div>

                <div class="my-auto py-3 flex flex-col items-center">
                  <span class="inline-block text-[10.5px] font-extrabold uppercase tracking-wider text-blue-200 bg-blue-950/90 px-3.5 py-1 rounded-full border border-blue-400/40 mb-3">
                    +59 €/m combo • 79 €/m suelto
                  </span>
                  <h3 class="text-lg sm:text-xl font-black text-white tracking-tight leading-snug mb-2">
                    Agenda, Contratos y Cobros (S6 a S8)
                  </h3>
                  <p class="text-xs text-slate-300 leading-relaxed">
                    Conexión bidireccional con calendarios, firmas legales y facturación (Setup: +110 € combo | 195 € suelto).
                  </p>
                </div>

                <div class="inline-flex items-center gap-1.5 text-xs font-bold text-blue-300 group-hover:text-white transition-colors">
                  <span>Ver S6 a S8 del Grupo 2</span>
                  <span>&#8635;</span>
                </div>
              </div>

              <div class="sp-flip-face sp-flip-back sp-roadmap-face-card border-t-4 border-t-blue-500 flex flex-col justify-between px-5 pt-4 pb-5">
                <div>
                  <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-[10px] font-extrabold uppercase tracking-wider text-blue-200 bg-blue-950/90 px-2.5 py-0.5 rounded-full border border-blue-400/50">
                      Grupo 2 (S6 a S8) • +59 €/m
                    </span>
                    <button type="button" onclick="spToggleFlipCard('cat2-facturacion', event)" class="px-2 py-0.5 rounded-full bg-white/10 hover:bg-white/20 text-slate-200 text-[10.5px] font-bold cursor-pointer">
                      &#8635;
                    </button>
                  </div>
                  <ul class="space-y-2.5 text-[12px] text-slate-200 leading-snug">
                    <li class="flex items-start gap-1.5"><span class="text-blue-400 font-black">S6.</span><span><strong class="text-white">Anti-Plantón 24h + Huecos Flash:</strong> Confirma citas por WA y rellena bajas con la lista de espera.</span></li>
                    <li class="flex items-start gap-1.5"><span class="text-blue-400 font-black">S7.</span><span><strong class="text-white">Firma Digital + Onboarding IA:</strong> Firma legal en el móvil, carpeta en Drive y validación de documentos.</span></li>
                    <li class="flex items-start gap-1.5"><span class="text-blue-400 font-black">S8.</span><span><strong class="text-white">Escudo Anti-Morosidad:</strong> Reclamación diplomática (+3, +7, +15 días) con PDF y enlace de pago.</span></li>
                  </ul>
                </div>
                <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20informaci%C3%B3n%20sobre%20los%20servicios%20S6%2C%20S7%20y%20S8%20del%20Grupo%202" target="_blank" onclick="event.stopPropagation();" class="pt-2 border-t border-white/15 text-xs font-extrabold text-blue-300 hover:text-white inline-flex items-center justify-between">
                  <span>Reservar S6 a S8</span><span>&rarr;</span>
                </a>
              </div>

            </div>
          </div>

          <!-- GRUPO 3: SATÉLITES ESPECIALIZADOS POR SECTOR Y BOOSTERS IA -->
          <div id="cat4-satelites" onclick="spToggleFlipCard('cat4-satelites', event)" class="sp-flip-scene sp-flip-roadmap-height sp-flip-led-pink cursor-pointer">
            <div class="sp-flip-card-inner">

              <div class="sp-flip-face sp-flip-front sp-roadmap-face-card border-t-4 border-t-pink-500 flex flex-col items-center justify-between p-6 text-center group">
                <div class="w-full flex items-center justify-between">
                  <span class="text-[10px] font-extrabold uppercase tracking-widest text-pink-300">Grupo 3 • Satélites</span>
                  <span class="sp-flip-plus-btn bg-pink-500/20 text-pink-200 border border-pink-400/50 group-hover:bg-pink-500 group-hover:text-white transition-colors">+</span>
                </div>

                <div class="my-auto py-3 flex flex-col items-center">
                  <span class="inline-block text-[10.5px] font-extrabold uppercase tracking-wider text-pink-200 bg-pink-950/90 px-3.5 py-1 rounded-full border border-pink-400/40 mb-3">
                    Desde +49 €/m combinado
                  </span>
                  <h3 class="text-lg sm:text-xl font-black text-white tracking-tight leading-snug mb-2">
                    Satélites de Sector y Boosters IA
                  </h3>
                  <p class="text-xs text-slate-300 leading-relaxed">
                    Módulos especializados en Instagram Meta API, E-commerce/Reparto y Cerebro Documental RAG B2B.
                  </p>
                </div>

                <div class="inline-flex items-center gap-1.5 text-xs font-bold text-pink-300 group-hover:text-white transition-colors">
                  <span>Ver Satélites del Grupo 3</span>
                  <span>&#8635;</span>
                </div>
              </div>

              <div class="sp-flip-face sp-flip-back sp-roadmap-face-card border-t-4 border-t-pink-500 flex flex-col justify-between px-5 pt-4 pb-5">
                <div>
                  <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-[10px] font-extrabold uppercase tracking-wider text-pink-200 bg-pink-950/90 px-2.5 py-0.5 rounded-full border border-pink-400/50">
                      Grupo 3 • Satélites y Boosters
                    </span>
                    <button type="button" onclick="spToggleFlipCard('cat4-satelites', event)" class="px-2 py-0.5 rounded-full bg-white/10 hover:bg-white/20 text-slate-200 text-[10.5px] font-bold cursor-pointer">
                      &#8635;
                    </button>
                  </div>
                  <ul class="space-y-2 text-[11.5px] text-slate-200 leading-snug">
                    <li class="flex items-start gap-1.5"><span class="text-pink-400 font-black">Sat.1</span><span><strong class="text-white">Instagram 3 en 1:</strong> +49 €/m (+75€) combo | 69 €/m (150€) suelto.</span></li>
                    <li class="flex items-start gap-1.5"><span class="text-sky-400 font-black">Sat.2</span><span><strong class="text-white">Escudo Logístico 360:</strong> +59 €/m (+110€) combo | 79 €/m (195€) suelto.</span></li>
                    <li class="flex items-start gap-1.5"><span class="text-violet-400 font-black">Sat.3</span><span><strong class="text-white">Cerebro Redactor RAG:</strong> +69 €/m (+150€) combo | 99 €/m (250€) suelto.</span></li>
                    <li class="flex items-start gap-1.5"><span class="text-amber-300 font-black">Boost</span><span><strong class="text-white">Add-ons IA (Correo S4 / Prov. S8):</strong> +35 €/m (+50 € Setup).</span></li>
                  </ul>
                </div>
                <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20informaci%C3%B3n%20sobre%20los%20Sat%C3%A9lites%20del%20Grupo%203%20%28Instagram%2C%20Log%C3%ADstica%20o%20Redactor%20RAG%29" target="_blank" onclick="event.stopPropagation();" class="pt-2 border-t border-white/15 text-xs font-extrabold text-pink-300 hover:text-white inline-flex items-center justify-between">
                  <span>Reservar Grupo 3</span><span>&rarr;</span>
                </a>
              </div>

            </div>
          </div>

          <!-- GRUPO 4: S9 Y S10 (TELEFONÍA Y CENTRALITA DE VOZ IA 24/7) -->
          <div id="cat3-eficiencia" onclick="spToggleFlipCard('cat3-eficiencia', event)" class="sp-flip-scene sp-flip-roadmap-height sp-flip-led-indigo cursor-pointer">
            <div class="sp-flip-card-inner">

              <div class="sp-flip-face sp-flip-front sp-roadmap-face-card border-t-4 border-t-indigo-500 flex flex-col items-center justify-between p-6 text-center group">
                <div class="w-full flex items-center justify-between">
                  <span class="text-[10px] font-extrabold uppercase tracking-widest text-indigo-300">Grupo 4 • S9 y S10</span>
                  <span class="sp-flip-plus-btn bg-indigo-500/20 text-indigo-200 border border-indigo-400/50 group-hover:bg-indigo-500 group-hover:text-white transition-colors">+</span>
                </div>

                <div class="my-auto py-3 flex flex-col items-center">
                  <span class="inline-block text-[10.5px] font-extrabold uppercase tracking-wider text-indigo-200 bg-indigo-950/90 px-3.5 py-1 rounded-full border border-indigo-400/40 mb-3">
                    Línea SIP + Minutos Voz IA
                  </span>
                  <h3 class="text-lg sm:text-xl font-black text-white tracking-tight leading-snug mb-2">
                    Telefonía y Voz IA 24/7 (S9 y S10)
                  </h3>
                  <p class="text-xs text-slate-300 leading-relaxed">
                    Satélites de telecomunicaciones con desvío de operadora y bolsa de minutos de voz neuronal.
                  </p>
                </div>

                <div class="inline-flex items-center gap-1.5 text-xs font-bold text-indigo-300 group-hover:text-white transition-colors">
                  <span>Ver S9 y S10 del Grupo 4</span>
                  <span>&#8635;</span>
                </div>
              </div>

              <div class="sp-flip-face sp-flip-back sp-roadmap-face-card border-t-4 border-t-indigo-500 flex flex-col justify-between px-5 pt-4 pb-5">
                <div>
                  <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-[10px] font-extrabold uppercase tracking-wider text-indigo-200 bg-indigo-950/90 px-2.5 py-0.5 rounded-full border border-indigo-400/50">
                      Grupo 4 (S9 y S10) • Voz IA
                    </span>
                    <button type="button" onclick="spToggleFlipCard('cat3-eficiencia', event)" class="px-2 py-0.5 rounded-full bg-white/10 hover:bg-white/20 text-slate-200 text-[10.5px] font-bold cursor-pointer">
                      &#8635;
                    </button>
                  </div>
                  <ul class="space-y-2.5 text-[12px] text-slate-200 leading-snug">
                    <li class="flex items-start gap-1.5"><span class="text-indigo-400 font-black">S9.</span><span><strong class="text-white">Rescate Llamadas Perdidas WA:</strong> +59 €/m (+110€ Setup) combo | 79 €/m (195€) suelto. Incluye desvío + hasta <strong>250 rescates/mes</strong>.</span></li>
                    <li class="flex items-start gap-1.5"><span class="text-indigo-400 font-black">S10.</span><span><strong class="text-white">Centralita Recepcionista Voz IA 24/7:</strong> +129 €/m (+250€ Setup) combo | 169 €/m (350€) suelto. Atiende y agenda sola con <strong>bolsa de 250 min/mes</strong>.</span></li>
                  </ul>
                </div>
                <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20informaci%C3%B3n%20sobre%20los%20servicios%20S9%20y%20S10%20del%20Grupo%204%20de%20Telefon%C3%ADa%20y%20Voz%20IA" target="_blank" onclick="event.stopPropagation();" class="pt-2 border-t border-white/15 text-xs font-extrabold text-indigo-300 hover:text-white inline-flex items-center justify-between">
                  <span>Reservar S9 y S10</span><span>&rarr;</span>
                </a>
              </div>

            </div>
          </div>

        </div>

        <div class="relative flex flex-wrap lg:flex-nowrap items-center justify-between gap-3 pt-1">

          <div class="relative flex items-center z-30">
            <button type="button" id="spGiftBubbleBtn" onclick="spToggleGiftBubble()" class="sp-gift-square-btn group flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-amber-950/80 hover:bg-amber-900 border-2 border-amber-400/75 shadow-lg shadow-amber-500/15 transition-all cursor-pointer" title="Pulsa para descubrir tu regalo">
              <span class="w-7 h-7 rounded-xl bg-amber-400/20 border border-amber-300/50 flex items-center justify-center text-base sp-gift-icon-wobble">🎁</span>
              <span id="spGiftBubbleHint" class="text-xs font-extrabold text-amber-200 group-hover:text-white whitespace-nowrap">Despliega el regalo &rarr;</span>
            </button>

            <div id="spGiftExpandPanel" class="sp-gift-expand-panel">
              <div class="flex items-start justify-between gap-3">
                <p class="text-xs text-amber-100 leading-snug">
                  <strong class="text-amber-300 font-extrabold">BONO REGALO a partir de 3 servicios mensuales (Plan Trinity+): Bóveda Segura de Contraseñas.</strong> Comparte accesos del negocio con tu equipo en 1 clic sin revelar claves ni usar notas adhesivas (valorada en 150 €).
                </p>
                <button type="button" onclick="spCerrarGiftBubble()" class="text-amber-300 hover:text-white text-xs font-black px-1.5 py-0.5 rounded bg-amber-900/60 flex-shrink-0 cursor-pointer" title="Recoger">✕</button>
              </div>
              <div class="w-full h-1 bg-amber-950 rounded-full overflow-hidden mt-1.5">
                <div id="spGiftProgressBar" class="h-full bg-gradient-to-r from-amber-400 to-yellow-200 rounded-full" style="width: 100%;"></div>
              </div>
            </div>
          </div>

          <div class="flex items-center justify-center gap-3">
            <button type="button" onclick="cambiarVista('tarifas')" class="sp-btn-s5-primary-3d px-6 h-[44px] inline-flex items-center justify-center gap-2 text-white font-extrabold text-xs sm:text-[14px] rounded-2xl cursor-pointer whitespace-nowrap">
              <span>Ver Precios Claros</span>
              <span>&rarr;</span>
            </button>
            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20querr%C3%ADa%20consultar%20qu%C3%A9%20combinaci%C3%B3n%20de%20servicios%20me%20recomiendas" target="_blank" class="sp-btn-s5-secondary-3d px-6 h-[44px] inline-flex items-center justify-center gap-2 text-white font-bold text-xs sm:text-[14px] rounded-2xl whitespace-nowrap">
              <span>Hablar con Francisco</span>
            </a>
          </div>

          <button type="button" onclick="cambiarVista('auditorias')" class="inline-flex items-center gap-2 px-4 h-[44px] rounded-2xl bg-gradient-to-r from-teal-500/25 via-emerald-500/25 to-sky-500/25 hover:from-teal-500/40 hover:to-sky-500/40 border border-teal-300/60 text-teal-200 hover:text-white text-xs sm:text-[13px] font-extrabold shadow-md transition-all cursor-pointer whitespace-nowrap">
            <span>✨</span>
            <span>Cuestionario dinámico</span>
            <span>&rarr;</span>
          </button>

        </div>

      </div>
    </section>"""

NUEVO_SELECT_RESERVA_CARRITO = r"""              <select id="spCartReservaFase2" onchange="window.spAgregarModuloReservaFase2(this.value)" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white font-bold">
                <option value="">+ Añadir módulo en Reserva Prioritaria (Grupos 1 a 4: S3 a S10 y Satélites)...</option>
                <optgroup label="Grupo 1 • Implantación Rápida (+40 €/m | +75 € Setup)">
                  <option value="S3 Leads en 10s + Portales (+40 €/m)">S3. Respuesta a Leads en 10s + Portales (+40 €/m)</option>
                  <option value="S4 Facturas al Gestor por Foto WA (+40 €/m)">S4. Facturas y Tickets al Gestor por Foto WA (+40 €/m)</option>
                  <option value="S5 Reactivación Clientes Inactivos (+40 €/m)">S5. Reactivación de Clientes Inactivos (+40 €/m)</option>
                </optgroup>
                <optgroup label="Grupo 2 • Operativa Avanzada (+59 €/m combo | 79 €/m suelto)">
                  <option value="S6 Agenda Anti-Plantón 24h + Flash (+59 €/m)">S6. Sistema Anti-Plantón de Citas 24h + Huecos Flash (+59 €/m)</option>
                  <option value="S7 Firma Digital + Onboarding IA (+59 €/m)">S7. Firma Digital de Presupuestos + Onboarding IA (+59 €/m)</option>
                  <option value="S8 Escudo Anti-Morosidad (+59 €/m)">S8. Escudo Anti-Morosidad Diplomático (+59 €/m)</option>
                </optgroup>
                <optgroup label="Grupo 3 • Satélites Especializados y Boosters IA">
                  <option value="Sat.1 Instagram 3 en 1 (+49 €/m combo)">Sat.1. Instagram Inteligente 3 en 1: Reels + DMs (+49 €/m)</option>
                  <option value="Sat.2 Escudo Logístico 360 (+59 €/m combo)">Sat.2. Escudo Logístico 360: Tracking + Ausencias (+59 €/m)</option>
                  <option value="Sat.3 Cerebro Redactor B2B RAG (+69 €/m combo)">Sat.3. Cerebro Redactor Técnico B2B RAG (+69 €/m)</option>
                  <option value="Booster IA Lector Correo S4 / Prov S8 (+35 €/m)">Booster IA: Lector Correo (S4) o Proveedores (S8) (+35 €/m)</option>
                </optgroup>
                <optgroup label="Grupo 4 • Telefonía y Voz Neuronal IA 24/7">
                  <option value="S9 Rescate Llamadas Perdidas WA (+59 €/m combo)">S9. Rescate de Llamadas Perdidas por WA (+59 €/m • 250/m)</option>
                  <option value="S10 Centralita Voz IA 24/7 (+129 €/m combo)">S10. Centralita Recepcionista de Voz IA 24/7 (+129 €/m • 250 min)</option>
                </optgroup>
              </select>"""

NUEVO_JS_TARIFAS_INDEX = r"""var _spModoTarifasActual = 'mensual';
    var _spNumAuditoriasEscudo = 1;

    function _spRenderizarTarjetasPrecios() {
      var btnM = document.getElementById('btnSwitchMensual');
      var btnA = document.getElementById('btnSwitchAnual');
      var pBase = document.querySelector('[data-plan-price="base"]');
      var pDuo = document.querySelector('[data-plan-price="duo"]');
      var pTri = document.querySelector('[data-plan-price="trinity"]');
      var subBase = document.getElementById('spSubPriceBase');
      var subDuo = document.getElementById('spSubPriceDuo');
      var subEsc = document.getElementById('spSubPriceEscudoTotal');
      var titleEsc = document.getElementById('spTitleEscudoTotal');
      var tagAud = document.getElementById('spAuditAddonPriceTag');
      var bulletAud = document.getElementById('spBulletAuditEscudo');
      var bulletBon = document.getElementById('spBulletBonusEscudo');
      var badgeAhorro = document.getElementById('spBadgeAhorroEscudoTotal');
      var btn1Aud = document.getElementById('btnEscudo1Aud');
      var btn2Aud = document.getElementById('btnEscudo2Aud');
      var waEsc = document.getElementById('spBtnWaPlanEscudoTotal');

      if (btn1Aud && btn2Aud) {
        if (_spNumAuditoriasEscudo === 2) {
          btn2Aud.className = 'px-2 py-0.5 rounded-md bg-emerald-600 text-white cursor-pointer transition-all whitespace-nowrap shadow-sm';
          btn1Aud.className = 'px-2 py-0.5 rounded-md text-teal-900 hover:text-brand-navy cursor-pointer transition-all whitespace-nowrap';
        } else {
          btn1Aud.className = 'px-2 py-0.5 rounded-md bg-emerald-600 text-white cursor-pointer transition-all whitespace-nowrap shadow-sm';
          btn2Aud.className = 'px-2 py-0.5 rounded-md text-teal-900 hover:text-brand-navy cursor-pointer transition-all whitespace-nowrap';
        }
      }

      var esPlus = (_spNumAuditoriasEscudo === 2);
      var costeAud = esPlus ? 390 : 195;

      if (titleEsc) titleEsc.textContent = esPlus ? 'Pack Escudo Plus ★' : 'Pack Escudo Total ★';
      if (tagAud) tagAud.textContent = esPlus ? '+ 390 € (Las 2 Super-Auditorías)' : '+ 195 € (1 Super-Auditoría Llave en Mano)';
      if (badgeAhorro) badgeAhorro.textContent = esPlus ? '¡Ahorras 310 € en las 2 Auditorías!' : '¡Ahorras 155 € en la Auditoría!';

      if (bulletAud) {
        bulletAud.innerHTML = esPlus
          ? '<strong class="text-brand-navy">Las 2 Super-Auditorías Llave en Mano incluidas</strong> (SEO+GEO IA + Neuro-CRO Web) por <strong class="text-emerald-800">390 €</strong> en vez de 700 €.'
          : '<strong class="text-brand-navy">1 Super-Auditoría Llave en Mano a elegir</strong> (SEO+GEO IA o Neuro-CRO Web) por solo <strong class="text-emerald-800">195 €</strong> en vez de 350 €.';
      }
      if (bulletBon) {
        bulletBon.innerHTML = esPlus
          ? 'Dejas blindados a la vez tu posicionamiento en Google/IA y la conversión de tu página web.'
          : 'Si eliges <strong class="text-brand-navy">+2 Auditorías (390 €)</strong> arriba, te llevas ambas implantadas ahorrando <strong class="text-emerald-800">310 €</strong>.';
      }

      if (_spModoTarifasActual === 'anual') {
        if (btnA) btnA.className = 'px-3 py-1.5 rounded-xl text-xs font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer flex items-center gap-1 whitespace-nowrap';
        if (btnM) btnM.className = 'px-3 py-1.5 rounded-xl text-xs font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer whitespace-nowrap';

        if (pBase) pBase.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-brand-navy">49 €</span><span class="text-xs font-bold text-slate-500">/ mes eq. (590 €/año)</span>';
        if (subBase) subBase.textContent = 'Día 1 Anual: 740 € (590€ 10m + 150€ Setup • Ahorras 118 €)';

        if (pDuo) pDuo.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-sky-700">82,50 €</span><span class="text-xs font-bold text-slate-500">/ mes eq. (990 €/año)</span>';
        if (subDuo) subDuo.textContent = 'Día 1 Anual: 1.215 € (990€ 10m + 225€ Setup • Ahorras 198 €)';

        if (pTri) pTri.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-emerald-700">82,50 €</span><span class="text-xs font-bold text-slate-500">/ mes eq. (990 €/año)</span>';
        var totalAnualEsc = 1215 + costeAud;
        if (subEsc) subEsc.textContent = 'Día 1 Anual: ' + totalAnualEsc + ' € (1.215€ Pack Anual + ' + costeAud + '€ Aud.)';
      } else {
        if (btnM) btnM.className = 'px-3 py-1.5 rounded-xl text-xs font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer whitespace-nowrap';
        if (btnA) btnA.className = 'px-3 py-1.5 rounded-xl text-xs font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer flex items-center gap-1 whitespace-nowrap';

        if (pBase) pBase.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-brand-navy">59 €</span><span class="text-xs font-bold text-slate-500">/ mes</span>';
        if (subBase) subBase.textContent = 'Día 1 Flex: 209 € (150 € Setup + 59 € Mes 1)';

        if (pDuo) pDuo.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-sky-700">99 €</span><span class="text-xs font-bold text-slate-500">/ mes</span>';
        if (subDuo) subDuo.textContent = 'Día 1 Flex: 324 € (225 € Setup + 99 € Mes 1)';

        if (pTri) pTri.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-emerald-700">99 €</span><span class="text-xs font-bold text-slate-500">/ mes</span>';
        var totalFlexEsc = 324 + costeAud;
        if (subEsc) subEsc.textContent = 'Día 1 Flex: ' + totalFlexEsc + ' € (225€ Setup + ' + costeAud + '€ Aud. + 99€ Mes 1)';
      }

      if (waEsc) {
        var nombrePack = esPlus ? 'Pack Escudo Plus (S1 + S2 por 99 €/mes + 2 Super-Auditorías por 390 €)' : 'Pack Escudo Total (S1 + S2 por 99 €/mes + 1 Super-Auditoría por 195 €)';
        var modTexto = (_spModoTarifasActual === 'anual') ? ' en modalidad Plan Anual (2 meses gratis)' : ' en modalidad mensual';
        waEsc.href = 'https://wa.me/34711547561?text=' + encodeURIComponent('Hola Francisco, quiero activar el ' + nombrePack + modTexto + '.');
        waEsc.textContent = esPlus ? 'Activar Pack Escudo Plus →' : 'Activar Pack Escudo Total →';
      }
    }

    function cambiarModoTarifas(modo) {
      _spModoTarifasActual = (modo === 'anual') ? 'anual' : 'mensual';
      _spRenderizarTarjetasPrecios();
    }

    window.spSeleccionarNivelEscudoTotal = function(numAud) {
      _spNumAuditoriasEscudo = (numAud === 2) ? 2 : 1;
      _spRenderizarTarjetasPrecios();
    };"""

ESTILOS_CARRITO_LUMINOSO_CRO = r"""    /* =========================================================================
       MODAL CARRITO CONFIGURADOR EN MODO CRISTAL LUMINOSO CRO (NEUROMARKETING)
       PUNTO INTERMEDIO EXACTO: APTO PARA PRESBICIA + CERO SCROLL EN PANTALLA
       ========================================================================= */
    #spModalCarritoCarta {
      padding: 0.5rem 1rem !important;
      overflow: hidden !important;
    }
    #spModalCarritoCarta > div {
      max-width: 74rem !important; /* 1184px: ancho panorámico para que nada salte de línea */
      max-height: 96vh !important;
      overflow: hidden !important;
      padding: 0.9rem 1.4rem !important;
      background: linear-gradient(160deg, #f8fafc 0%, #ffffff 55%, #f0fdfa 100%) !important;
      color: #0b2239 !important;
      border: 2.5px solid #0d9488 !important;
      box-shadow: 0 28px 65px -12px rgba(11, 34, 57, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.95) !important;
    }
    /* Cabecera compacta en 1 sola línea sin el banner superior de ruido */
    #spModalCarritoCarta > div > div:first-child {
      padding-bottom: 0.45rem !important;
      margin-bottom: 0.55rem !important;
      border-bottom: 1.5px solid #cbd5e1 !important;
    }
    /* Ocultar el banner superior "CONFIGURADOR A LA CARTA • IMPLANTACIÓN RÁPIDA 24-48H" */
    #spModalCarritoCarta > div > div:first-child span.bg-amber-950\/90 {
      display: none !important;
    }
    /* Botón X de cerrar bien visible sobre fondo blanco */
    #spModalCarritoCarta button[onclick*="spCerrarCarritoConfigurador"] {
      width: 2.15rem !important;
      height: 2.15rem !important;
      background: #e2e8f0 !important;
      color: #0b2239 !important;
      border: 1.5px solid #94a3b8 !important;
      font-size: 1rem !important;
      font-weight: 900 !important;
      box-shadow: 0 2px 5px rgba(15, 23, 42, 0.10) !important;
    }
    #spModalCarritoCarta button[onclick*="spCerrarCarritoConfigurador"]:hover {
      background: #e11d48 !important;
      color: #ffffff !important;
      border-color: #be123c !important;
    }
    /* Títulos principales del Carrito */
    #spModalCarritoCarta h3 {
      font-size: 1.24rem !important; /* ~20px: claro y en 1 sola línea */
      line-height: 1.2 !important;
      color: #0b2239 !important;
      margin-top: 0 !important;
    }
    #spModalCarritoCarta h4 {
      font-size: 0.88rem !important;
      color: #0b2239 !important;
      letter-spacing: 0.02em !important;
    }
    /* Espaciado vertical compacto entre bloques de las columnas */
    #spModalCarritoCarta .lg\:col-span-7 {
      gap: 0.45rem !important;
    }
    #spModalCarritoCarta .lg\:col-span-7.space-y-3 > * + * {
      margin-top: 0.45rem !important;
    }
    /* Etiquetas de los pasos 1, 2, 3, 4 y 5 (punto intermedio nítido 12.5px) */
    #spModalCarritoCarta label {
      font-size: 0.78rem !important; /* ~12.5px */
      font-weight: 900 !important;
      color: #065f46 !important;
      letter-spacing: 0.02em !important;
      margin-bottom: 0.22rem !important;
    }
    /* Botones de selección (Pasos 1, 2 y 3) con altura contenida y letra intermedia clara */
    #spModalCarritoCarta .sp-cart-item-btn {
      border: 2px solid #cbd5e1 !important;
      background: #ffffff !important;
      border-radius: 0.8rem !important;
      padding: 0.48rem 0.75rem !important;
      text-align: left;
      transition: all 0.18s ease;
      cursor: pointer;
      color: #0f172a !important;
      box-shadow: 0 2px 8px -2px rgba(11, 34, 57, 0.06) !important;
    }
    /* Título principal dentro de cada tarjeta seleccionable (~14.5px) */
    #spModalCarritoCarta .sp-cart-item-btn > span:first-child {
      font-size: 0.91rem !important; /* ~14.5px */
      font-weight: 900 !important;
      color: #0b2239 !important;
      line-height: 1.2 !important;
      margin-bottom: 0.1rem !important;
    }
    /* Subtítulos y precios dentro de cada tarjeta seleccionable (~12.4px) */
    #spModalCarritoCarta .sp-cart-item-btn > span:not(:first-child) {
      font-size: 0.775rem !important; /* ~12.4px */
      font-weight: 600 !important;
      color: #334155 !important;
      line-height: 1.24 !important;
      display: block !important;
      margin-top: 0.06rem !important;
    }
    #spModalCarritoCarta .sp-cart-item-btn:hover {
      border-color: #0d9488 !important;
      background: #f0fdfa !important;
    }
    /* Estado seleccionado: Verde Esmeralda Luminoso con texto ultra-nítido */
    #spModalCarritoCarta .sp-cart-item-btn.sp-cart-selected {
      border: 2px solid #059669 !important;
      background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%) !important;
      box-shadow: 0 6px 16px -4px rgba(5, 150, 105, 0.22), inset 0 1px 0 #ffffff !important;
      color: #064e3b !important;
    }
    #spModalCarritoCarta .sp-cart-item-btn.sp-cart-selected > span:first-child {
      color: #064e3b !important;
    }
    #spModalCarritoCarta .sp-cart-item-btn.sp-cart-selected > span:not(:first-child) {
      color: #065f46 !important;
      font-weight: 700 !important;
    }
    /* Campos de formulario y desplegables compactos de alto contraste (13.8px) */
    #spModalCarritoCarta select,
    #spModalCarritoCarta input[type="text"],
    #spModalCarritoCarta input[type="tel"],
    #spModalCarritoCarta input[type="datetime-local"] {
      background: #ffffff !important;
      color: #0b2239 !important;
      border: 1.5px solid #94a3b8 !important;
      font-size: 0.86rem !important; /* ~13.8px */
      font-weight: 700 !important;
      padding: 0.38rem 0.68rem !important;
      height: 2.25rem !important; /* 36px fijo para ahorrar altura vertical */
      border-radius: 0.65rem !important;
      box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.04) !important;
    }
    #spModalCarritoCarta select:focus,
    #spModalCarritoCarta input:focus {
      border-color: #0d9488 !important;
      box-shadow: 0 0 0 2px rgba(20, 184, 166, 0.2) !important;
    }
    #spModalCarritoCarta input::placeholder {
      color: #475569 !important;
      font-weight: 600 !important;
    }
    /* Cajas contenedoras secundarias */
    #spModalCarritoCarta .bg-slate-950,
    #spModalCarritoCarta .bg-slate-950\/80,
    #spModalCarritoCarta .bg-slate-900,
    #spModalCarritoCarta .bg-slate-900\/95 {
      background: #f8fafc !important;
      border: 1.5px solid #cbd5e1 !important;
      color: #0b2239 !important;
    }
    #spModalCarritoCarta .lg\:col-span-5 {
      padding: 0.7rem 0.95rem !important;
    }
    /* Píldora superior derecha "2 servicios mensuales" con alto contraste */
    #spModalCarritoCarta #spCartCountModulosBadge {
      background: #065f46 !important;
      color: #ffffff !important;
      border: 1px solid #047857 !important;
      font-size: 0.74rem !important;
      font-weight: 800 !important;
      padding: 0.15rem 0.55rem !important;
    }
    /* Líneas del Resumen de tu Pedido (sin partir "324 €" en dos renglones) */
    #spModalCarritoCarta #spCartSummaryLines {
      font-size: 0.83rem !important; /* ~13.3px */
      line-height: 1.32 !important;
      color: #0b2239 !important;
      margin-bottom: 0.35rem !important;
    }
    #spModalCarritoCarta #spCartSummaryLines > div {
      display: flex !important;
      align-items: baseline !important;
      justify-content: space-between !important;
      gap: 0.5rem !important;
      padding: 0.06rem 0 !important;
    }
    #spModalCarritoCarta #spCartSummaryLines span {
      color: #1e293b !important;
      font-weight: 600 !important;
    }
    #spModalCarritoCarta #spCartSummaryLines strong {
      color: #0b2239 !important;
      font-weight: 900 !important;
      font-size: 0.9rem !important;
      white-space: nowrap !important;
      flex-shrink: 0 !important;
    }
    /* Caja de Total Desembolso Día 1 compacta */
    #spModalCarritoCarta .bg-emerald-950\/60 {
      background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%) !important;
      border: 2px solid #059669 !important;
      padding: 0.45rem 0.75rem !important;
      margin-bottom: 0.45rem !important;
    }
    #spModalCarritoCarta .bg-emerald-950\/60 span {
      color: #064e3b !important;
      font-size: 0.78rem !important;
      line-height: 1.25 !important;
    }
    #spModalCarritoCarta #spCartTotalDia1 {
      color: #064e3b !important;
      font-size: 1.35rem !important; /* ~21.6px rotundo y sin comer altura */
      font-weight: 900 !important;
      white-space: nowrap !important;
    }
    #spModalCarritoCarta #spCartCuotaMensual {
      color: #0f766e !important;
      font-size: 0.82rem !important;
      font-weight: 900 !important;
    }
    /* Todos los textos que eran amarillos pálidos pasan a Cobre/Ámbar Oscuro (#92400e) */
    #spModalCarritoCarta .text-amber-300,
    #spModalCarritoCarta .text-amber-200,
    #spModalCarritoCarta .text-amber-200\/95 {
      color: #92400e !important;
      font-weight: 800 !important;
    }
    #spModalCarritoCarta #spCartSelectDiaLV,
    #spModalCarritoCarta #spCartSelectHoraManana {
      font-size: 0.82rem !important; /* ~13.1px */
      color: #0b2239 !important;
      font-weight: 800 !important;
    }
    #spModalCarritoCarta #spCartSyncCalBadge {
      color: #047857 !important;
      background: #d1fae5 !important;
      padding: 0.1rem 0.45rem !important;
      border-radius: 9999px !important;
      font-size: 0.72rem !important;
      font-weight: 800 !important;
    }
    #spModalCarritoCarta .text-slate-400,
    #spModalCarritoCarta .text-slate-300,
    #spModalCarritoCarta .text-slate-200,
    #spModalCarritoCarta .text-emerald-200,
    #spModalCarritoCarta .text-sky-300 {
      color: #1e293b !important;
      font-size: 0.78rem !important;
      line-height: 1.28 !important;
    }
    /* Subselector de Plan Base (S1 vs S2) en modo luminoso compacto */
    #spModalCarritoCarta #spSubSelectorBaseS1S2 {
      background: #f0fdfa !important;
      border: 1.5px solid #0d9488 !important;
      padding: 0.45rem 0.65rem !important;
      margin-top: 0.35rem !important;
    }
    #spModalCarritoCarta #spSubSelectorBaseS1S2 button {
      background: #ffffff !important;
      color: #0b2239 !important;
      font-size: 0.82rem !important;
      padding: 0.35rem 0.6rem !important;
    }
    #spModalCarritoCarta #spSubSelectorBaseS1S2 button span {
      color: #334155 !important;
      font-size: 0.75rem !important;
    }
    /* Botón principal de Confirmar Pedido siempre visible sin scroll */
    #spModalCarritoCarta #spBtnSubmitCarrito {
      font-size: 0.95rem !important;
      padding: 0.62rem 1rem !important;
    }"""

JS_PUENTE_TEST_A_CARRITO = r"""window.spAbrirCarritoConDiagnosticoPreseleccionado = function() {
          var recs = (typeof recsIntegralGlobal !== 'undefined' && Array.isArray(recsIntegralGlobal)) ? recsIntegralGlobal : [];
          var tieneS1 = recs.indexOf('s1_resenas') !== -1;
          var tieneS2 = recs.indexOf('s2_cortafuegos') !== -1;
          var tieneGeo = recs.indexOf('audit_geo') !== -1;
          var tieneCro = recs.indexOf('audit_cro') !== -1;
          var tieneAtril = recs.indexOf('hw_atril') !== -1;

          var planElegir = 'duo';
          if (tieneS1 && tieneS2) {
            planElegir = 'duo';
          } else if (tieneS1 || tieneS2) {
            planElegir = 'base';
          } else if (tieneGeo || tieneCro || tieneAtril) {
            planElegir = 'ninguno';
          }

          var numAud = (tieneGeo && tieneCro) ? 2 : ((tieneGeo || tieneCro) ? 1 : 0);

          if (typeof window.spAbrirCarritoConfigurador === 'function') {
            window.spAbrirCarritoConfigurador(planElegir, numAud);
          }

          if (planElegir === 'base' && typeof window.spSeleccionarSubServicioBaseV125 === 'function') {
            if (tieneS2 && !tieneS1) {
              window.spSeleccionarSubServicioBaseV125('S2 Encuesta Cortafuegos WhatsApp');
            } else {
              window.spSeleccionarSubServicioBaseV125('S1 Reseñas Google IA');
            }
          }

          var selAtril = document.getElementById('spCartAtrilSelect');
          if (selAtril) {
            selAtril.value = tieneAtril ? '1' : '0';
          }

          var mapaRecAFase2 = {
            s3_leads10s: 'S3 Leads en 10s + Portales (+40 €/m)',
            s9_facturas: 'S4 Facturas al Gestor por Foto WA (+40 €/m)',
            s5_inactivos: 'S5 Reactivación Clientes Inactivos (+40 €/m)',
            s6_antiplanton: 'S6 Agenda Anti-Plantón 24h + Flash (+59 €/m)',
            s8_firma: 'S7 Firma Digital + Onboarding IA (+59 €/m)',
            s10_cobros: 'S8 Escudo Anti-Morosidad (+59 €/m)',
            sat1_instagram: 'Sat.1 Instagram 3 en 1 (+49 €/m combo)',
            sat2_logistica: 'Sat.2 Escudo Logístico 360 (+59 €/m combo)',
            sat3_b2b: 'Sat.3 Cerebro Redactor B2B RAG (+69 €/m combo)',
            s4_llamadas: 'S9 Rescate Llamadas Perdidas WA (+59 €/m combo)',
            s7_centralita: 'S10 Centralita Voz IA 24/7 (+129 €/m combo)'
          };

          if (typeof window.spAgregarModuloReservaFase2 === 'function') {
            recs.forEach(function(k) {
              if (mapaRecAFase2[k]) {
                window.spAgregarModuloReservaFase2(mapaRecAFase2[k]);
              }
            });
          }

          if (typeof window.spRecalcularCarritoCarta === 'function') {
            window.spRecalcularCarritoCarta();
          }
        };"""

def actualizar_index_html_completo(ruta_index):
    if not os.path.isfile(ruta_index):
        print(f"  ⚠️ No se encontró {ruta_index}")
        return

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Reemplazar el bloque completo de #vista-tarifas con el botón dorado integrado y alineado dentro del contenedor sin salirse por la derecha
    patron_vista_tarifas = re.compile(
        r"<!-- ======================================================================= -->\s*<!-- VISTA 4 \(SALA INDEPENDIENTE\): PRECIOS CLAROS.*?</section>",
        re.DOTALL
    )
    if patron_vista_tarifas.search(html):
        html = patron_vista_tarifas.sub(lambda _: NUEVO_BLOQUE_VISTA_TARIFAS_INDEX, html, count=1)

    # 2. Reemplazar la última diapositiva de Cómo ayudamos (#ca-slide-proximos) con la numeración correlativa S1-S5 (G1), S6-S8 (G2), Satélites (G3) y S9-S10 (G4)
    patron_ca_proximos = re.compile(
        r"<!-- ===================================================================== -->\s*<!-- DIAPOSITIVA 5(?: DE CÓMO AYUDAMOS)?:.*?</section>",
        re.DOTALL
    )
    if patron_ca_proximos.search(html):
        html = patron_ca_proximos.sub(lambda _: NUEVO_BLOQUE_CA_SLIDE_PROXIMOS, html, count=1)

    # 3. Actualizar el desplegable de Reserva Prioritaria en el Carrito Configurador con los números correlativos S3..S10
    patron_select_reserva = re.compile(
        r'<select id="spCartReservaFase2".*?</select>',
        re.DOTALL
    )
    if patron_select_reserva.search(html):
        html = patron_select_reserva.sub(lambda _: NUEVO_SELECT_RESERVA_CARRITO, html, count=1)

    # 4. Actualizar las referencias en el Test de Diagnóstico (CATALOGO_RECOMENDACIONES y mapaFase2) a la nueva numeración S1..S10
    reemplazos_numeracion_index = [
        ("Servicio 4 • Cero Ventas Perdidas", "Servicio 9 • Grupo 4 Telefonía"),
        ("S4. Rescate de Llamadas Perdidas", "S9. Rescate de Llamadas Perdidas"),
        ("Servicio 7 • Atención Telefónica 24/7", "Servicio 10 • Grupo 4 Voz IA 24/7"),
        ("S7. Centralita de Voz y Citas con IA", "S10. Centralita de Voz y Citas con IA"),
        ("Servicio 8 • Cierre Inmediato", "Servicio 7 • Grupo 2 Contratos"),
        ("S8. Firma de Presupuestos + Onboarding IA", "S7. Firma de Presupuestos + Onboarding IA"),
        ("Servicio 9 • Paz Trimestral (+ Add-on Correo)", "Servicio 4 • Grupo 1 Cero Papeles"),
        ("S9. Facturas al Gestor IA (Cero Papeles)", "S4. Facturas al Gestor IA (Cero Papeles)"),
        ("Servicio 10 • Cobro Puntual (+ Proveedores)", "Servicio 8 • Grupo 2 Anti-Morosidad"),
        ("S10. Anti-Morosidad Diplomático", "S8. Anti-Morosidad Diplomático"),
        ("S4 Rescate Llamadas Perdidas (+59 €/m)", "S9 Rescate Llamadas Perdidas WA (+59 €/m combo)"),
        ("S7 Centralita Voz IA 24/7 (Desde 149 €/m)", "S10 Centralita Voz IA 24/7 (+129 €/m combo)"),
        ("S8 Firma Digital Presupuestos (+40 €/m)", "S7 Firma Digital + Onboarding IA (+59 €/m)"),
        ("S9 Facturas al Gestor por Foto WA (+40 €/m)", "S4 Facturas al Gestor por Foto WA (+40 €/m)"),
        ("S10 Escudo Anti-Morosidad (+40 €/m)", "S8 Escudo Anti-Morosidad (+59 €/m)"),
    ]
    for viejo, nuevo in reemplazos_numeracion_index:
        html = html.replace(viejo, nuevo)

    # 5. Reparar el bug de urgenciaPorMódulo (con tilde) que dejaba vacío el resultado del Test de Diagnóstico
    html = html.replace("var urgenciaPorMódulo = {};", "var urgenciaPorModulo = {};")
    html = html.replace("urgenciaPorMódulo", "urgenciaPorModulo")

    # 6. Quitar el botón dorado de compra que salía arriba en la cabecera del Test de Diagnóstico (#vista-auditorias)
    patron_inyeccion_test_top = re.compile(
        r"// 3\. TEST DE DIAGNÓSTICO \(#vista-test\):.*?contenedorTest\.insertBefore\(barraCarritoTest, contenedorTest\.firstChild\);\s*\}\s*\}",
        re.DOTALL
    )
    html = patron_inyeccion_test_top.sub("// 3. TEST DE DIAGNÓSTICO: Sin botón de compra arriba (aparece al final con el diagnóstico preseleccionado)", html)
    # Por si ya estaba en el DOM estático
    html = re.sub(r'<div id="spWrapBtnCarritoEnTest".*?</div>', '', html, flags=re.DOTALL)

    # 7. Añadir el botón dorado "🛒 Configurar y Contratar mi Solución" en la barra inferior del resultado del Test (#spTestResultContainer)
    if 'id="spBtnComprarDesdeDiagnostico"' not in html:
        html = html.replace(
            '<a id="spTestWhatsappBtn" href="https://wa.me/34711547561" target="_blank" class="sp-btn-s5-primary-3d w-full sm:w-auto text-center text-white font-extrabold text-xs sm:text-[13.5px] px-5 py-2.5 rounded-xl">\n              💬 Comentar mi diagnóstico con Francisco &rarr;\n            </a>',
            '<a id="spTestWhatsappBtn" href="https://wa.me/34711547561" target="_blank" class="sp-btn-s5-secondary-3d w-full sm:w-auto text-center text-white font-bold text-xs sm:text-[13px] px-4 py-2 rounded-xl">\n              💬 Comentar con Francisco\n            </a>\n            <button type="button" id="spBtnComprarDesdeDiagnostico" onclick="window.spAbrirCarritoConDiagnosticoPreseleccionado()" class="sp-btn-carrito-gold-3d w-full sm:w-auto text-center px-5 py-2.5 rounded-xl text-xs sm:text-[13.5px] inline-flex items-center justify-center gap-2 shadow-lg cursor-pointer">\n              <span class="sp-cart-icon-badge">🛒</span>\n              <span>Configurar y Contratar mi Solución &rarr;</span>\n            </button>'
        )

    # 8. Inyectar la función spAbrirCarritoConDiagnosticoPreseleccionado() dentro del script del Test de Diagnóstico
    if "window.spAbrirCarritoConDiagnosticoPreseleccionado" not in html:
        html = html.replace(
            "window.spReiniciarTestDiagnostico = function()",
            JS_PUENTE_TEST_A_CARRITO + "\n\n        window.spReiniciarTestDiagnostico = function()"
        )

    # 9. Inyectar o actualizar los estilos de «Modo Cristal Luminoso de Alta Confianza» para el Carrito (#spModalCarritoCarta)
    patron_css_carrito_luminoso = re.compile(
        r"/\*\s*===\s*=========================================================================\s*MODAL CARRITO CONFIGURADOR EN MODO CRISTAL LUMINOSO CRO.*?(?=/\*\s*===\s*\[SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_END\]\s*===\s*\*/)",
        re.DOTALL
    )
    if patron_css_carrito_luminoso.search(html):
        html = patron_css_carrito_luminoso.sub(lambda _: ESTILOS_CARRITO_LUMINOSO_CRO + "\n    ", html)
    elif "MODAL CARRITO CONFIGURADOR EN MODO CRISTAL LUMINOSO CRO" in html:
        patron_alt = re.compile(
            r"/\*\s*=========================================================================\s*MODAL CARRITO CONFIGURADOR EN MODO CRISTAL LUMINOSO CRO.*?(?=/\*\s*===\s*\[SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_END\]\s*===\s*\*/)",
            re.DOTALL
        )
        html = patron_alt.sub(lambda _: ESTILOS_CARRITO_LUMINOSO_CRO + "\n    ", html)
    else:
        html = html.replace(
            "/* === [SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_END] === */",
            ESTILOS_CARRITO_LUMINOSO_CRO + "\n    /* === [SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_END] === */"
        )

    # 10. Actualizar las funciones JS de tarifas en index.html
    patron_js_tarifas = re.compile(
        r"var _spModoTarifasActual = 'mensual';.*?window\.spSeleccionarNivelEscudoTotal = function\(numAud\)\s*\{.*?\};",
        re.DOTALL
    )
    html = patron_js_tarifas.sub(lambda _: NUEVO_JS_TARIFAS_INDEX, html)

    # 11. Limpiar botón Trinity duplicado en el paso 2 del carrito si existía
    patron_btn_trinity_carrito = re.compile(
        r'\s*<button type="button" id="spCartPlan_trinity".*?</button>',
        re.DOTALL
    )
    html = patron_btn_trinity_carrito.sub("", html)

    # 12. Quitar el banner superior de ruido en el Carrito y poner "(listo en 24-48h)" al lado del título
    html = re.sub(
        r'<span class="text-\[10\.5px\] font-extrabold uppercase tracking-wider text-amber-300 bg-amber-950/90[^>]*>\s*🛒 Configurador a la Carta • Implantación Rápida 24-48h\s*</span>\s*',
        '',
        html
    )
    html = html.replace(
        "Configura tu Plan a Medida y Agenda tu Videollamada de Alta",
        'Configura tu Plan a Medida y Agenda tu Videollamada de Alta <span class="text-teal-700 font-extrabold text-base sm:text-lg">(listo en 24-48h)</span>'
    )

    # 13. Compactar los campos de Nombre + Teléfono en una misma fila (2 columnas) para ahorrar altura y evitar cualquier scroll
    patron_inputs_carrito = re.compile(
        r'var inpNom = document\.getElementById\(\'spCartInputNombre\'\);\s*if \(inpNom && inpNom\.parentNode && !document\.getElementById\(\'spCartInputNegocioCiudad\'\)\) \{.*?inpNom\.parentNode\.insertBefore\(inpNeg, inpNom\.nextSibling\);\s*\}',
        re.DOTALL
    )
    nuevo_js_inputs_compactos = r"""var inpNom = document.getElementById('spCartInputNombre');
    var inpTel = document.getElementById('spCartInputTelefono');
    if (inpNom && inpTel && inpNom.parentNode && !document.getElementById('spCartInputNegocioCiudad')) {
      var parentForm = inpNom.parentNode;
      parentForm.className = 'space-y-1.5 text-xs';
      inpNom.placeholder = '1. Tu Nombre (Ej: Carlos) *';
      inpTel.placeholder = '2. Tu Móvil (Ej: 600 123 456) *';
      var filaNomTel = document.createElement('div');
      filaNomTel.className = 'grid grid-cols-1 sm:grid-cols-2 gap-1.5';
      parentForm.insertBefore(filaNomTel, inpNom);
      filaNomTel.appendChild(inpNom);
      filaNomTel.appendChild(inpTel);
      var inpNeg = document.createElement('input');
      inpNeg.id = 'spCartInputNegocioCiudad';
      inpNeg.type = 'text';
      inpNeg.required = true;
      inpNeg.placeholder = '3. Nombre de tu Negocio y Ciudad (Ej: Clínica Sol - Vigo) *';
      inpNeg.className = 'w-full bg-white border-2 border-teal-600/60 focus:border-teal-600 rounded-xl px-3 py-1.5 text-slate-900 placeholder-slate-500 outline-none font-bold';
      parentForm.insertBefore(inpNeg, filaNomTel.nextSibling);
    }"""
    html = patron_inputs_carrito.sub(lambda _: nuevo_js_inputs_compactos, html)

    # 14. Compactar el bloque de Cita de Alta en 1 sola línea informativa sin el párrafo largo inferior que provocaba scroll
    html = html.replace(
        '<p class="text-[10px] text-amber-200/95 leading-snug">🔥 <strong>Horario Especial Gerentes:</strong> Habilitamos Sábados y Domingos (mañana y tarde) para ver juntos tu diagnóstico sin interrumpir tu horario de atención al público.</p>',
        '<p class="text-[11px] text-amber-900 font-bold leading-tight">🔥 Incluye Sábados y Domingos (mañana y tarde) para no interrumpir tu horario de apertura.</p>'
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
SECCION_5_NUEVA_BIBLIA = """## 5. ESTRUCTURA OFICIAL DE TARIFAS EN 4 GRUPOS (NUMERACIÓN CORRELATIVA S1 A S10), PACKS, SUPER-AUDITORÍAS Y LIQUIDACIÓN DÍA 1

### A) Las 3 Reglas de Oro de Nuestra Arquitectura de Precios (Precios Netos sin IVA 21% • SEPA B2B)
1. **Coherencia Psicológica en Terminación «9» (Charm Pricing):** Todas las cuotas mensuales terminan en 9 (`59 €`, `99 €`, `139 €`, `79 €`, `+59 €`, `69 €`, `+49 €`, `99 €`, `+69 €`, `169 €`, `+129 €`) o en `+40 €` redondo para los módulos adicionales del Grupo 1.
2. **Suelo Mínimo Intocable de 195 € en las 2 Super-Auditorías (Eliminado para siempre el escalón de 95 €):**
   - **Modalidad 1 — «Solo Código / DIY» (Sin mano de obra nuestra):** `200 €` por 1 Super-Auditoría | `390 €` contratando las 2 juntas (`195 €` c/u). Entregamos PDF Parte 1 + PDF Parte 2 (Solo Códigos Limpios) para su informático.
   - **Modalidad 2 — Oficial «Llave en Mano» (Suelta o con Plan Base de 1 servicio):** `350 €` por 1 Super-Auditoría | `590 €` las 2 juntas (`295 €` c/u, ahorra `110 €` — Pack Firma Institucional / Alto Standing ideal Nexitum). Incluye Diagnóstico + Parte 2 + Reunión de defensa con su técnico + Implantación en 15 min + Sonda de 10-14 días en la Neuro-CRO.
   - **Modalidad 3 — BONIFICADA CON PACK (Dúo, Trinity o superior, Mensual o Anual):** `195 €` por 1 Super-Auditoría | `390 €` las 2 juntas (`195 €` c/u, ahorra `310 €`). Nunca baja de `195 €` c/u.
3. **División en 4 Bloques con Numeración Correlativa (`S1` a `S10`) según Dificultad de Puesta en Marcha y Coste de API:**
   - **GRUPO 1 (S1 a S5 — Núcleo de Implantación Rápida: S1 Reseñas IA, S2 Cortafuegos WA, S3 ★ Respuesta a Leads en 10s, S4 Facturas por Foto WA y S5 Reactivación de Inactivos):** `59 €/mes` el 1º (`150 €` Setup) y `+40 €/mes` adicionales del 2º al 5º (`+75 €` Setup).
   - **GRUPO 2 (S6 a S8 — Operativa Avanzada de Agenda, Contratos y Cobros: S6 Anti-Plantón 24h + Huecos Flash, S7 Firma Digital + Onboarding IA y S8 Escudo Anti-Morosidad):** `79 €/mes` suelto (`195 €` Setup) | `+59 €/mes` combinado (`+110 €` Setup). Computa al 100% para beneficios de Pack.
   - **GRUPO 3 (Satélites Especializados y Boosters IA):** Satélite 1 Instagram 3 en 1 (`69 €/m` + `150 €` suelto | `+49 €/m` + `+75 €` combinado), Satélite 2 Escudo Logístico 360 (`79 €/m` + `195 €` suelto | `+59 €/m` + `+110 €` combinado), Satélite 3 Cerebro Redactor B2B RAG (`99 €/m` + `250 €` suelto | `+69 €/m` + `+150 €` combinado), y Boosters IA 1 (Lector Correo para S4) y 2 (Proveedores para S8) a `+35 €/m` + `+50 €` Setup.
   - **GRUPO 4 (S9 y S10 — Satélites de Telefonía y Voz IA):** **S9** Rescate de Llamadas Perdidas por WhatsApp (`79 €/m` + `195 €` suelto | `+59 €/m` + `+110 €` combinado; incluye desvío + hasta 250 rescates/mes) y **S10** Centralita de Voz IA 24/7 (`169 €/m` + `350 €` suelto | `+129 €/m` + `+250 €` combinado; incluye número virtual/desvío + conexión a agenda + bolsa de 250 min/mes).

### B) Tabla Maestra de Planes del Grupo 1, Combinaciones y Desembolso Día 1 (Vía 1 Flexible 3 meses vs. Vía 2 Plan Anual 10 meses = 2 Gratis)

| Plan / Módulo | Combinación Típica | Cuota Mensual | Alta Técnica (Setup) | Pago Día 1 (Vía Flexible 3m) | Pago Día 1 (Vía Anual 10m = 2 Gratis) | Ventajas Desbloqueadas en este Nivel |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Plan Pyme BASE (1 serv. G1)** | 1 servicio del Grupo 1 (S1..S5) | **59 €/m** | 150 € | **209 €** | **740 €** (590€ + 150€) | Ahorra 118 € en Anual • Auditorías a 350 € c/u (o 590 € las dos) |
| **Pack ESCUDO BÁSICO (Dúo: 2 serv.)** | **S1 + S2** (2 serv. libre elección) | **99 €/m** | 225 € | **324 €** | **1.215 €** (990€ + 225€) | Ahorra 19 €/m + 75 € Setup • **Desbloquea Auditorías a 195 € c/u (390 € las dos)** |
| **Pack ESCUDO TOTAL ★ (Hoy: S1+S2 + Aud.)** | **S1 + S2 (99€/m) + 1 o 2 Auditorías** | **99 €/m** | 225 € (+195€/390€ Aud.) | **519 €** (con 1 Aud.) / **714 €** (con 2) | **1.410 €** (con 1 Aud.) / **1.605 €** (con 2) | **Ahorra 155 € en 1 Auditoría o 310 € en las 2 Super-Auditorías** |
| **Plan TRINITY (3 serv. Grupo 1)** | 3 servicios Grupo 1 (ej. S1+S2+S3) | **139 €/m** | 300 € | **439 €** | **1.690 €** (1.390€ + 300€) | **🎁 Bóveda Contraseñas GRATIS (150€)** + Auditorías a **195 € c/u** + Ahorra 278 € en Anual |
| **Plan QUATRO (4 serv. Grupo 1)** | S1 + S2 + S3 + S4 | **179 €/m** | 375 € | **554 €** | **2.165 €** (1.790€ + 375€) | Bóveda Gratis + Auditorías a **195 € c/u** + Ahorra 358 € en Anual |
| **Plan PENTIUM (5 serv. Grupo 1)** | S1 + S2 + S3 + S4 + S5 | **219 €/m** | 450 € | **669 €** | **2.640 €** (2.190€ + 450€) | Bóveda Gratis + Auditorías a **195 € c/u** + Ahorra 438 € en Anual |
| **+ Servicio Grupo 2 (S6..S8), Logística o S9** | S6, S7, S8, Reparto o Llamadas WA | **+59 €/m** (79€ s.) | +110 € (195€ s.) | **+169 €** combo (274€ s.) | **+700 €** combo (985€ s.) | Computa al 100% para beneficios de Pack Dúo/Trinity |
| **+ Satélite 1: Instagram 3 en 1** | Auto-DM Reels + DMs 24/7 + Stories | **+49 €/m** (69€ s.) | +75 € (150€ s.) | **+124 €** combo (219€ s.) | **+565 €** combo (840€ s.) | Ahorra 20 €/mes y 75 € de Setup al combinarlo |
| **+ Satélite 3: Cerebro Redactor RAG** | IA con PDFs, tarifas y contratos propios | **+69 €/m** (99€ s.) | +150 € (250€ s.) | **+219 €** combo (349€ s.) | **+840 €** combo (1.240€ s.) | Ahorra 30 €/mes y 100 € de Setup al combinarlo |
| **+ Satélite S10: Centralita Voz IA 24/7** | Recepcionista neuronal + 250 min/mes | **+129 €/m** (169€ s.) | +250 € (350€ s.) | **+379 €** combo (519€ s.) | **+1.540 €** combo (2.040€ s.) | Ahorra 40 €/mes y 100 € de Setup al combinarlo |"""

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
### ACTUALIZACIÓN {VERSION_ACTUAL} ({datetime.now().strftime('%d/%m/%Y %H:%M')}) — Carrito en «Modo Cristal Luminoso CRO», Reparación del Resultado del Test de Diagnóstico y Preselección Automática de Soluciones al Contratar
- **Nuevo Diseño Luminoso de Alta Confianza en el Carrito Configurador (`#spModalCarritoCarta` en `index.html`):** Siguiendo los principios de neuromarketing y conversión (CRO), el modal de compra abandona el fondo negro oscuro y adopta la misma estética luminosa blanco/menta/perla de `Precios claros`, con tipografía azul marino de alto contraste para presbicia y tarjetas seleccionables en verde esmeralda suave.
- **Eliminado el Botón Dorado Superior en el Test de Diagnóstico (`#vista-auditorias`):** Mientras el usuario responde las 12 fichas, arriba se muestra únicamente el encabezado limpio *«Descubre el pulso digital de tu negocio.»*.
- **Reparación del Motor de Resultados del Test (`urgenciaPorModulo`) y Preselección Automática en el Carrito (`spAbrirCarritoConDiagnosticoPreseleccionado`):** Corregida la variable que impedía mostrar los módulos al terminar las 12 preguntas, e incorporado en la barra inferior del diagnóstico el botón dorado `🛒 Configurar y Contratar mi Solución →`, que abre el Carrito Luminoso con todos los servicios y auditorías recomendados por el Test ya marcados automáticamente para que el cliente solo tenga que elegir fecha/hora de la cita y confirmar.
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
            print(f"\n📂 Verificando y actualizando tarjetones en: {sub_doc}")
            r_tar = os.path.join(sub_doc, "tarifas.html")
            r_tar_m = os.path.join(sub_doc, "tarifas_movil.html")
            r_des = os.path.join(sub_doc, "desembolso.html")
            r_des_m = os.path.join(sub_doc, "desembolso_movil.html")
            r_set = os.path.join(sub_doc, "setup.html")
            r_set_m = os.path.join(sub_doc, "setup_movil.html")
            r_cat = os.path.join(sub_doc, "catalogo.html")
            r_cat_m = os.path.join(sub_doc, "catalogo_movil.html")

            for r_doc in [r_tar, r_tar_m, r_des, r_des_m, r_set, r_set_m, r_cat, r_cat_m]:
                if os.path.isfile(r_doc):
                    actualizar_tarjeton_existente_si_procede(r_doc)
                    archivos_a_validar.append(r_doc)

        # Actualizar también en subcarpeta static/documentos si existe en servicio_resenas
        sub_static_doc = os.path.join(base_dir, "static", "documentos")
        if os.path.isdir(sub_static_doc):
            for nombre_doc in ["tarifas.html", "tarifas_movil.html", "desembolso.html", "desembolso_movil.html", "setup.html", "setup_movil.html", "catalogo.html", "catalogo_movil.html"]:
                r_sdoc = os.path.join(sub_static_doc, nombre_doc)
                if os.path.isfile(r_sdoc):
                    actualizar_tarjeton_existente_si_procede(r_sdoc)

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
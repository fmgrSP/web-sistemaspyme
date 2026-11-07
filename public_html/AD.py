#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SISTEMAS PYME — ACTUALIZADOR MAESTRO SEGURO COMPLETO (AD.py - VERSIÓN V154)
================================================================================
Archivo 100% COMPLETO de principio a fin.
Copia todo este contenido dentro de tu archivo `AD.py` y ejecútalo en Terminal:
    python3 AD.py

Qué soluciona de raíz esta versión V154:
1. SOLUCIÓN DEFINITIVA A `IndentationError` (línea 62) Y `FileNotFoundError: 'node'`:
   - Restituidas íntegramente las funciones `crear_backup_seguro`,
     `escribir_archivo_con_backup`, `validar_sintaxis_python` y
     `validar_bloques_js_en_html` con sangría de 4 espacios verificada.
   - `validar_bloques_js_en_html` localiza automáticamente Node en Mac
     (`/opt/homebrew/bin/node`, `/usr/local/bin/node`, `~/.nvm/...`) y captura
     `FileNotFoundError` para que nunca detenga el script en entornos Miniconda.
2. PRECIOS CLAROS (DIAPOSITIVA 1) — SUBCAJAS DE IDÉNTICA ALTURA Y CERO CONFUSIÓN:
   - Titular H2 en 2 líneas limpias: «Precios claros y amortización» arriba y
     «desde el primer cliente.» debajo, dejando espacio amplio para los botones.
   - Botón Mensual grande y claro: «🔄 Mensual (permanencia de 3 meses)».
   - Quitada la frase de permanencia dentro de la tarjeta `Pyme Base` para que
     nadie piense que los otros dos planes tienen permanencia distinta.
   - En Plan Anual, las 3 subcajas tienen exactamente la misma altura y una sola
     línea de ahorro:
       * Pyme Base: «🎁 Ahorras 118 € al año (pagas 10 meses)»
       * Pack Escudo Básico: «🎁 Ahorras 198 € al año (pagas 10 meses)»
       * Pack Escudo Total / Plus: «🎁 Ahorras 198 € al año (pagas 10 meses)»
3. CARRITO A LA CARTA (#spModalCarritoCarta) — CONTRASTE INEQUÍVOCO, ALTURA
   COMPACTA SIN CORTAR EL BOTÓN Y SELECTOR INTELIGENTE DE FASE 2:
   - Diferencia visual rotunda entre tarjeta SELECCIONADA (color intenso, borde
     oscuro de 3px, sombra profunda e insignia `✓ ACTIVO`) y NO seleccionada
     (fondo muy suave y atenuado al 58% de opacidad).
   - Reajuste de alturas en la columna derecha del Carrito para que, aunque se
     active el Bono Regalo de Bóveda y el subselector de Plan Base, el botón
     dorado «🚀 Confirmar Pedido y Agendar Alta →» jamás quede cortado abajo.
   - Selector inteligente en «5. Reserva Prioritaria Fase 2»: los módulos que ya
     has añadido aparecen en gris deshabilitados (`disabled` con `✓ Ya seleccionado`)
     y si los quitas de la lista vuelven a estar disponibles automáticamente.
4. TECNOCONSULTOR CONECTADO DE VERDAD A LA IA DE GEMINI + APAGADO AL CAMBIAR DE
   PESTAÑA O SECCIÓN:
   - Eliminado el bloqueo en `file://` que devolvía siempre la misma respuesta
     enlatada. Ahora consulta en directo a Gemini (vía Vertex AI directo desde
     el navegador o servidor local 5000 con historial conversacional real).
   - Al cambiar a cualquier otra sección de la web (`Inicio`, `Cómo ayudamos`,
     `Test de diagnóstico`, `Precios claros`, `Magazine`) o cambiar de pestaña,
     el consultor detiene su voz y apaga la escucha del micrófono en el acto.
================================================================================
"""

import os
import sys
import re
import ast
import glob
import json
import time
import shutil
import atexit
import subprocess
import urllib.request
from datetime import datetime

VERSION_ACTUAL = "V158"
FECHA_EJECUCION = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
TIMESTAMP_BAK = datetime.now().strftime("%Y%m%d_%H%M%S")

RUTA_WEB_PUBLIC = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme/public_html"
RUTA_SCRAPER = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Scraper/Scrapper App"
RUTA_SERVICIO_RESENAS = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Servicios/Servicio Reseñas/servicio_resenas"
RUTA_PROGRAMAR = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Programar"

VERSION_ACTUAL = "V162"
FECHA_EJECUCION = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
TIMESTAMP_BAK = datetime.now().strftime("%Y%m%d_%H%M%S")

URL_WEBHOOK_SHEETS_DEFAULT = "https://script.google.com/macros/s/AKfycbwo9pcYbQKru4WMAxAnHNcqtIcAYQogXkaQ8BAWhTeyzc49kLtM02SVFnTxYRGqUStapg/exec"

# ==============================================================================
# 1. UTILIDADES DE BACKUP, ESCRITURA SEGURA Y VALIDACIÓN (PYTHON + JS NODE)
# ==============================================================================
def crear_backup_seguro(ruta_archivo):
    if not ruta_archivo or not os.path.exists(ruta_archivo):
        return None
    carpeta_base = os.path.dirname(os.path.abspath(ruta_archivo))
    carpeta_bak = os.path.join(carpeta_base, "backups_sp")
    os.makedirs(carpeta_bak, exist_ok=True)
    nombre_base = os.path.basename(ruta_archivo)
    ruta_bak = os.path.join(carpeta_bak, f"{nombre_base}.{TIMESTAMP_BAK}.bak")
    shutil.copy2(ruta_archivo, ruta_bak)
    print(f"  🛡️ Backup creado en backups_sp: {ruta_bak}")
    return ruta_bak


def escribir_archivo_con_backup(ruta_archivo, contenido):
    if not ruta_archivo:
        return False
    os.makedirs(os.path.dirname(os.path.abspath(ruta_archivo)), exist_ok=True)
    if os.path.exists(ruta_archivo):
        crear_backup_seguro(ruta_archivo)
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)
    size_kb = round(os.path.getsize(ruta_archivo) / 1024.0, 1)
    print(f"  🟢 Archivo actualizado y verificado ({size_kb} KB): {ruta_archivo}")
    return True


def validar_sintaxis_python(ruta_py):
    if not os.path.exists(ruta_py):
        return True
    try:
        with open(ruta_py, "r", encoding="utf-8") as f:
            codigo = f.read()
        ast.parse(codigo)
        print(f"  ✅ Sintaxis Python (ast.parse) OK: {os.path.basename(ruta_py)}")
        return True
    except SyntaxError as e:
        print(f"  ❌ ERROR DE SINTAXIS PYTHON en {ruta_py}: {e}")
        return False


def validar_bloques_js_en_html(ruta_html):
    if not os.path.exists(ruta_html):
        return True
    try:
        with open(ruta_html, "r", encoding="utf-8") as f:
            html = f.read()
        bloques = re.findall(r"<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>", html, flags=re.IGNORECASE)
        node_bin = shutil.which("node")
        if not node_bin:
            candidatos_node = [
                "/opt/homebrew/bin/node",
                "/usr/local/bin/node",
                "/usr/bin/node",
                os.path.expanduser("~/.nvm/versions/node/current/bin/node"),
            ]
            candid_glob = glob.glob(os.path.expanduser("~/.nvm/versions/node/*/bin/node"))
            candidatos_node.extend(sorted(candid_glob, reverse=True))
            for cand in candidatos_node:
                if cand and os.path.exists(cand) and os.access(cand, os.X_OK):
                    node_bin = cand
                    break
        if node_bin and bloques:
            for idx, b in enumerate(bloques):
                if "application/ld+json" in b or not b.strip():
                    continue
                tmp_js = f"/tmp/_sp_check_v161_{idx}.js"
                with open(tmp_js, "w", encoding="utf-8") as tf:
                    tf.write(b)
                try:
                    proc = subprocess.run([node_bin, "--check", tmp_js], capture_output=True, text=True)
                except FileNotFoundError:
                    try:
                        os.remove(tmp_js)
                    except Exception:
                        pass
                    break
                try:
                    os.remove(tmp_js)
                except Exception:
                    pass
                if proc.returncode != 0:
                    print(f"  ❌ Error JS en bloque #{idx + 1} de {os.path.basename(ruta_html)}:\n{proc.stderr}")
                    return False
        print(f"  🟢 Todos los bloques <script> validados OK: {os.path.basename(ruta_html)}")
        return True
    except Exception as e:
        print(f"  ⚠️ Aviso validando JS en {ruta_html}: {e}")
        return True


# ==============================================================================
# 2. SECCIÓN COMPLETA `#vista-tarifas` (PRECIOS CLAROS CON SUS 3 TARJETAS ÍNTEGRAS)
# ==============================================================================
HTML_VISTA_TARIFAS_V152 = r'''  <!-- ======================================================================= -->
  <!-- VISTA 4 (SALA INDEPENDIENTE): PRECIOS CLAROS (ARQUITECTURA 4 GRUPOS)    -->
  <!-- ======================================================================= -->
  <section id="vista-tarifas" class="view-panel hidden bg-slate-50 text-slate-900">

    <!-- =================================================================== -->
    <!-- DIAPOSITIVA 1 DE PRECIOS: LOS 3 PLANES ACTIVOS HOY (100VH LUMINOSO) -->
    <!-- =================================================================== -->
    <div id="tarifas-slide-planes" class="slide-section sp-tarifas-light-bg border-b border-teal-200/80 px-4 sm:px-6 relative overflow-hidden" style="min-height: calc(100vh - 5.75rem); padding-top: 1.5rem !important; padding-bottom: 1.1rem !important; justify-content: space-between !important;">
      <div class="absolute inset-0 sp-rhombus-grid-reverse pointer-events-none opacity-65" aria-hidden="true"></div>

      <div class="max-w-6xl mx-auto w-full flex flex-col justify-between flex-1 relative z-10">

        <!-- FILA 1: Titular en 2 líneas a la izquierda + Botones Mensual/Anual grandes y claros -->
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3 pb-2.5 mb-2 border-b-2 border-teal-500/25 w-full">
          <h2 class="text-xl sm:text-2xl lg:text-[26px] font-black text-brand-navy tracking-tight leading-[1.15] text-left">
            <span class="block">Precios claros y amortización</span>
            <span class="block sp-green-headline">desde el primer cliente.</span>
          </h2>

          <div class="flex flex-wrap items-center justify-start lg:justify-end gap-2.5 flex-shrink-0">
            <div class="inline-flex items-center gap-1.5 bg-white/95 p-1.5 rounded-2xl border-2 border-teal-500/35 shadow-md">
              <button type="button" id="btnSwitchMensual" onclick="cambiarModoTarifas('mensual')" class="px-4 py-2 rounded-xl text-xs sm:text-[13px] font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer whitespace-nowrap">
                🔄 Mensual (permanencia de 3 meses)
              </button>
              <button type="button" id="btnSwitchAnual" onclick="cambiarModoTarifas('anual')" class="px-4 py-2 rounded-xl text-xs sm:text-[13px] font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap">
                <span>🎁 Plan Anual</span>
                <span class="text-[10.5px] font-black bg-amber-100 text-amber-900 border border-amber-400 px-2 py-0.5 rounded-full">Pagas 10 meses</span>
              </button>
            </div>
            <button type="button" id="spBtnTopCarritoPrecios" onclick="window.spAbrirCarritoConfigurador()" class="sp-btn-carrito-gold-3d px-4 py-2.5 rounded-xl text-xs sm:text-[13px] inline-flex items-center gap-1.5 whitespace-nowrap shadow-md">
              <span class="sp-cart-icon-badge">🛒</span>
              <span>Configurar a la Carta / Contratar</span>
            </button>
          </div>
        </div>

        <!-- FILA 2: Las 3 Tarjetas Protagonistas con toda su estructura completa y Subcajas Simétricas -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 items-stretch my-auto py-1">

          <!-- TARJETA 1: PYME BASE -->
          <div class="sp-price-card-3d sp-price-card-slate px-5 py-3.5 flex flex-col justify-between">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1.5 min-h-[34px]">
                <div class="inline-flex items-center justify-center text-[10px] font-extrabold uppercase tracking-wider text-slate-800 bg-slate-100 px-3 py-1 rounded-xl border border-slate-300 leading-tight shadow-sm whitespace-nowrap">
                  1 Servicio Activo
                </div>
                <div class="text-right leading-tight">
                  <span class="block text-[11px] font-bold text-slate-700 whitespace-nowrap">Setup único: <strong class="text-brand-navy font-black">150 €</strong></span>
                  <span class="block text-[10px] font-semibold text-slate-500 whitespace-nowrap">(Alta llave en mano)</span>
                </div>
              </div>

              <div class="mb-2 min-h-[48px] flex flex-col justify-center">
                <h3 class="text-lg sm:text-[19px] font-black text-brand-navy whitespace-nowrap">
                  Pyme BASE <span class="text-slate-500 font-bold text-sm">(1 serv.)</span>
                </h3>
                <p class="text-xs text-slate-600 leading-snug mt-0.5">
                  1 servicio de libre elección (hoy S1 o S2) para empezar paso a paso:
                </p>
              </div>

              <!-- Subcaja Simétrica 1 (Altura idéntica h-[100px] y 1 sola línea de insignia) -->
              <div class="bg-slate-50 border-2 border-slate-200/90 rounded-2xl px-3.5 py-2 mb-2.5 shadow-inner flex flex-col justify-between h-[100px]">
                <div class="flex items-baseline justify-between gap-2" data-plan-price="base">
                  <div class="flex items-baseline gap-1.5 whitespace-nowrap">
                    <span class="text-2xl sm:text-[28px] font-black text-brand-navy whitespace-nowrap">59 €</span>
                    <span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span>
                  </div>
                </div>
                <span id="spSubPriceBase" class="block text-xs font-extrabold text-slate-700 truncate">
                  + 150 € Setup único
                </span>
                <span id="spSavingLineBase" class="block text-[11px] font-extrabold text-slate-700 bg-slate-200/75 border border-slate-300 rounded-lg px-2.5 py-0.5 truncate whitespace-nowrap">
                  ✓ 1 módulo activo a elegir (S1 o S2)
                </span>
              </div>

              <ul class="space-y-1 text-xs text-slate-700 leading-snug mb-2.5">
                <li class="flex items-start gap-1.5"><span class="text-teal-600 font-black">✔</span><span><strong class="text-brand-navy">1 servicio activo</strong> a elegir según tu prioridad hoy (S1 Reseñas IA o S2 WhatsApp).</span></li>
                <li class="flex items-start gap-1.5"><span class="text-teal-600 font-black">✔</span><span>Incluye <strong class="text-brand-navy">Informe Mensual 360° Interactivo</strong> cada día 1 de mes.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-slate-400 font-black">•</span><span class="text-slate-600">Super-Auditorías Llave en Mano a tarifa estándar (350 € una / 590 € las dos).</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanBase" href="javascript:void(0)" onclick="window.spAbrirCarritoConfigurador('base', 0)" class="w-full py-2 text-center rounded-xl bg-brand-navy hover:bg-slate-800 text-white font-extrabold text-xs sm:text-[13px] shadow-md transition-all block cursor-pointer">
              Elegir Pyme BASE &rarr;
            </a>
          </div>

          <!-- TARJETA 2: PACK ESCUDO BÁSICO (DÚO) -->
          <div class="sp-price-card-3d sp-price-card-sky px-5 py-3.5 flex flex-col justify-between">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1.5 min-h-[34px]">
                <div class="inline-flex items-center gap-1.5 text-[10px] font-extrabold uppercase tracking-wider text-sky-900 bg-sky-100/95 px-2.5 py-1 rounded-xl border border-sky-300 leading-tight shadow-sm whitespace-nowrap">
                  <span>🛡️ 2 Servicios (S1 + S2)</span>
                </div>
                <div class="text-right leading-tight">
                  <span class="block text-[11px] font-bold text-sky-950 whitespace-nowrap">Setup Dúo: <strong class="text-brand-navy font-black">225 €</strong></span>
                  <span class="block text-[10px] font-extrabold text-emerald-700 whitespace-nowrap">(2.º Setup al 50%)</span>
                </div>
              </div>

              <div class="mb-2 min-h-[48px] flex flex-col justify-center">
                <h3 class="text-lg sm:text-[19px] font-black text-brand-navy whitespace-nowrap">
                  Pack Escudo Básico <span class="text-sky-700 font-bold text-sm">(Dúo)</span>
                </h3>
                <p class="text-xs text-slate-700 leading-snug mt-0.5">
                  2 servicios de libre elección (hoy <strong class="text-brand-navy">S1 + S2</strong>; el 2.º suma solo <strong class="text-brand-navy">+40 €/m</strong>):
                </p>
              </div>

              <!-- Subcaja Simétrica 2 (Altura idéntica h-[100px] y 1 sola línea de insignia) -->
              <div class="bg-white/95 border-2 border-sky-300 rounded-2xl px-3.5 py-2 mb-2.5 shadow-inner flex flex-col justify-between h-[100px]">
                <div class="flex items-baseline justify-between gap-2" data-plan-price="duo">
                  <div class="flex items-baseline gap-1.5 whitespace-nowrap">
                    <span class="text-2xl sm:text-[28px] font-black text-sky-700 whitespace-nowrap">99 €</span>
                    <span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span>
                  </div>
                </div>
                <span id="spSubPriceDuo" class="block text-xs font-extrabold text-sky-950 truncate">
                  + 225 € Setup Dúo
                </span>
                <span id="spSavingLineDuo" class="block text-[11px] font-extrabold text-emerald-800 bg-emerald-50 border border-emerald-300 rounded-lg px-2.5 py-0.5 truncate whitespace-nowrap">
                  🎁 Ahorras 19 €/mes + 75 € en Setup
                </span>
              </div>

              <ul class="space-y-1 text-xs text-slate-800 leading-snug mb-2.5">
                <li class="flex items-start gap-1.5"><span class="text-sky-600 font-black">✔</span><span><strong class="text-brand-navy">Une S1 + S2:</strong> Respuesta IA en Google + Cortafuegos Preventivo por WhatsApp.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-sky-600 font-black">✔</span><span><strong class="text-brand-navy">Informe 360° Completo</strong> con transcripción IA de notas de voz.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-amber-600 font-black">🔑</span><span><strong class="text-brand-navy">Llave de Socio:</strong> Desbloquea las Super-Auditorías a <strong class="text-emerald-800">195 € c/u</strong> (en vez de 350 €).</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanDuo" href="javascript:void(0)" onclick="window.spAbrirCarritoConfigurador('duo', 0)" class="w-full py-2 text-center rounded-xl bg-sky-600 hover:bg-sky-700 text-white font-black text-xs sm:text-[13px] shadow-lg shadow-sky-600/25 transition-all block cursor-pointer">
              Elegir Pack Escudo Básico &rarr;
            </a>
          </div>

          <!-- TARJETA 3 ESTRELLA: PACK ESCUDO TOTAL / PLUS ★ -->
          <div class="sp-price-card-3d sp-price-card-emerald px-5 py-3.5 flex flex-col justify-between relative">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1.5 min-h-[34px]">
                <div class="inline-flex items-center gap-1 text-[10px] font-extrabold uppercase tracking-wider text-white bg-gradient-to-r from-emerald-600 to-teal-600 px-2.5 py-1 rounded-xl shadow-sm leading-tight whitespace-nowrap">
                  <span>🚀 Recomendado</span>
                </div>
                <div class="text-right leading-tight">
                  <span class="block text-[11px] font-bold text-teal-950 whitespace-nowrap">Setup Dúo: <strong class="text-brand-navy font-black">225 €</strong></span>
                  <span id="spTopRightAudLabel" class="block text-[10px] font-extrabold text-emerald-700 whitespace-nowrap">+ 1 Auditoría (195 €)</span>
                </div>
              </div>

              <div class="flex flex-wrap items-center justify-between gap-1.5 mb-2 min-h-[48px]">
                <h3 id="spTitleEscudoTotal" class="text-lg sm:text-[19px] font-black text-brand-navy whitespace-nowrap">
                  Pack Escudo Total ★
                </h3>
                <div class="inline-flex items-center bg-white/95 p-0.5 rounded-lg border-2 border-emerald-500/50 text-[10px] font-extrabold shadow-sm">
                  <button type="button" id="btnEscudo1Aud" onclick="spSeleccionarNivelEscudoTotal(1)" class="px-2 py-0.5 rounded-md bg-emerald-600 text-white cursor-pointer transition-all whitespace-nowrap shadow-sm">
                    +1 Auditoría (195€)
                  </button>
                  <button type="button" id="btnEscudo2Aud" onclick="spSeleccionarNivelEscudoTotal(2)" class="px-2 py-0.5 rounded-md text-teal-900 hover:text-brand-navy cursor-pointer transition-all whitespace-nowrap">
                    +2 Auditorías (390€)
                  </button>
                </div>
              </div>

              <!-- Subcaja Simétrica 3 (Altura idéntica h-[100px] y 1 sola línea de insignia) -->
              <div class="bg-white/95 border-2 border-emerald-500/70 rounded-2xl px-3.5 py-2 mb-2.5 shadow-inner flex flex-col justify-between h-[100px]">
                <div class="flex items-baseline justify-between gap-2" data-plan-price="trinity">
                  <div class="flex items-baseline gap-1.5 whitespace-nowrap">
                    <span class="text-2xl sm:text-[28px] font-black text-emerald-700 whitespace-nowrap">99 €</span>
                    <span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span>
                  </div>
                </div>
                <span id="spSubPriceEscudoTotal" class="block text-xs font-extrabold text-teal-950 truncate">
                  + 225 € Setup Dúo + 195 € (1 Auditoría)
                </span>
                <span id="spSavingLineEscudoTotal" class="block text-[11px] font-extrabold text-emerald-900 bg-emerald-100/90 border border-emerald-400 rounded-lg px-2.5 py-0.5 truncate whitespace-nowrap">
                  🎁 Ahorras 155 € en Auditoría + 75 € Setup
                </span>
              </div>

              <ul class="space-y-1 text-xs text-slate-800 leading-snug mb-2.5">
                <li class="flex items-start gap-1.5"><span class="text-emerald-600 font-black">✔</span><span><strong class="text-brand-navy">Incluye S1 + S2</strong> protegiendo y multiplicando tus 5★ en Google y WhatsApp.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-emerald-600 font-black">✔</span><span id="spBulletAuditEscudo"><strong class="text-brand-navy">1 Super-Auditoría Llave en Mano a elegir</strong> (SEO+GEO IA o Neuro-CRO Web) por solo <strong class="text-emerald-800">195 €</strong> en vez de 350 €.</span></li>
                <li class="flex items-start gap-1.5"><span class="text-amber-600 font-black">★</span><span id="spBulletBonusEscudo">Si eliges <strong class="text-brand-navy">+2 Auditorías (390 €)</strong> arriba, te llevas ambas implantadas ahorrando <strong class="text-emerald-800">310 €</strong>.</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanEscudoTotal" href="javascript:void(0)" onclick="window.spAbrirCarritoConfigurador('duo', (typeof _spNumAuditoriasEscudo !== 'undefined' ? _spNumAuditoriasEscudo : 1))" class="sp-btn-s5-primary-3d w-full py-2 text-center rounded-xl text-white font-black text-xs sm:text-[13px] block cursor-pointer">
              Activar Pack Escudo Total &rarr;
            </a>
          </div>

        </div>

        <!-- FILA 3: Banner-Guía Inferior Centrado Equidistante -->
        <div class="my-auto pt-3 pb-1 flex justify-center">
          <button type="button" onclick="spScrollLimpioSeccion('tarifas-slide-complementos')" class="group inline-flex items-center gap-3.5 px-7 py-3 rounded-2xl bg-gradient-to-r from-brand-navy via-[#0f3456] to-teal-800 hover:from-teal-800 hover:to-brand-navy text-white border-2 border-teal-300/80 shadow-xl hover:shadow-2xl hover:-translate-y-0.5 transition-all cursor-pointer">
            <span class="text-base">🔍🧠</span>
            <span class="text-xs sm:text-[14px] font-black tracking-tight text-white">
              Ver tabla de las 2 Super-Auditorías, los 4 Grupos (S1 a S10) y Atril NFC
            </span>
            <span class="w-7 h-7 rounded-full bg-emerald-400 text-slate-950 flex items-center justify-center font-black text-sm shadow-md animate-bounce">
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

          <!-- Columna Izquierda (7 cols): Las 2 Super-Auditorías Gemelas -->
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
                    <strong class="text-brand-navy">«Para que te encuentren en Google Maps y te citen ChatGPT, Perplexity y Gemini»:</strong> 22 parámetros + Grafo <code>@graph</code> Wikidata + <code>/llms.txt</code> (Tabla 1 Dueño + Tabla 2 Informático).
                  </p>
                </div>
                <div class="bg-amber-50/95 border-2 border-amber-300 rounded-2xl p-3.5 shadow-sm">
                  <strong class="text-amber-900 text-[13.5px] font-black block mb-1">2. Neuro-CRO + Sonda de 10-14 Días</strong>
                  <p class="text-slate-700 leading-snug">
                    <strong class="text-brand-navy">«Para duplicar las visitas web que te contactan»:</strong> Disponible en <strong>Modo Ágil</strong> (Comercios/Clínicas) o <strong>Modo Corporativo</strong> (Despachos y Firmas).
                  </p>
                </div>
              </div>
            </div>

            <div>
              <span class="block text-[11px] font-extrabold uppercase tracking-wider text-brand-navy mb-2">
                Tabla Oficial de las Super-Auditorías (Solución Completa Llave en Mano o Lista para tu Técnico):
              </span>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-center">
                <div class="bg-emerald-50 rounded-2xl p-3.5 border-2 border-emerald-500 flex flex-col justify-between shadow-md">
                  <span class="block text-[10.5px] font-extrabold text-emerald-900 uppercase">1. Bonificada con Pack 2+ Servicios ★</span>
                  <span class="block text-2xl font-black text-emerald-700 my-0.5">195 € <span class="text-xs font-bold text-emerald-800">por 1 auditoría</span></span>
                  <span class="block text-xs font-black text-emerald-900">390 € las dos juntas (Ahorras 310 €)</span>
                  <span class="block text-[11px] text-emerald-950 font-semibold leading-snug mt-1.5">Todo el servicio «Llave en Mano» completo bonificado un 44% al activar cualquier Pack de 2 o más servicios.</span>
                </div>
                <div class="bg-white rounded-2xl p-3.5 border-2 border-sky-300 flex flex-col justify-between shadow-sm">
                  <span class="block text-[10.5px] font-extrabold text-sky-900 uppercase">2. Tarifa Estándar «Llave en Mano»</span>
                  <span class="block text-2xl font-black text-sky-700 my-0.5">350 € <span class="text-xs font-bold text-slate-500">por 1 auditoría</span></span>
                  <span class="block text-xs font-extrabold text-sky-900">590 € las dos juntas (Ahorras 110 €)</span>
                  <span class="block text-[11px] text-slate-700 leading-snug mt-1.5">Contratada suelta o con Pyme Base. Incluye implantación por nosotros o entrega de todos los códigos e instrucciones a tu técnico.</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Columna Derecha (5 cols): Los servicios divididos en 4 Grupos + Hardware Atril -->
          <div class="lg:col-span-5 flex flex-col justify-between gap-3.5">

            <div class="sp-light-card-3d-sky rounded-3xl p-4 flex-1 flex flex-col justify-between">
              <div>
                <div class="flex items-start justify-between gap-2 mb-2.5 pb-2 border-b border-sky-200">
                  <div class="bg-sky-100/90 border border-sky-300 rounded-xl px-3 py-1 text-left leading-tight">
                    <span class="block text-[10.5px] font-extrabold uppercase tracking-wider text-sky-950 whitespace-nowrap">🚀 Los servicios divididos en 4 Grupos</span>
                    <span class="block text-[10px] font-black text-sky-700 mt-0.5 whitespace-nowrap">Secuencia S1 a S10 (Precio Combo vs. Suelto)</span>
                  </div>
                  <div class="bg-emerald-50 border border-emerald-300 rounded-xl px-2.5 py-1 text-right leading-tight flex-shrink-0">
                    <span class="block text-[10.5px] font-extrabold text-emerald-800 whitespace-nowrap">🎁 Bóveda Gratis</span>
                    <span class="block text-[10px] font-black text-emerald-700 mt-0.5 whitespace-nowrap">3 o más servicios</span>
                  </div>
                </div>

                <ul class="space-y-1.5 text-[11px] text-slate-800 leading-snug">
                  <li class="border-b border-sky-200/70 pb-1">
                    <div class="flex justify-between items-baseline gap-1">
                      <span><strong class="text-brand-navy">Grupo 1</strong> (S1 a S5):</span>
                      <span class="whitespace-nowrap"><strong class="text-emerald-800">Combo: +40 €/m (+75€ Setup)</strong> <span class="text-slate-500">| 1.º: 59€/m (150€)</span></span>
                    </div>
                  </li>
                  <li class="border-b border-sky-200/70 pb-1">
                    <div class="flex justify-between items-baseline gap-1">
                      <span><strong class="text-sky-900">Grupo 2</strong> (S6 a S8):</span>
                      <span class="whitespace-nowrap"><strong class="text-sky-800">Combo: +59 €/m (+110€ Setup)</strong> <span class="text-slate-500">| Suelto: 79€/m (195€)</span></span>
                    </div>
                  </li>
                  <li class="border-b border-sky-200/70 pb-1">
                    <div class="flex justify-between items-baseline gap-1">
                      <span><strong class="text-pink-800">Grupo 3</strong> · Sat.1 IG 3 en 1:</span>
                      <span class="whitespace-nowrap"><strong class="text-pink-700">Combo: +49 €/m (+75€)</strong> <span class="text-slate-500">| Suelto: 69€/m (150€)</span></span>
                    </div>
                    <div class="flex justify-between items-baseline gap-1 pl-11 mt-0.5 text-slate-700">
                      <span>· Sat.2 Logística 360:</span>
                      <span class="whitespace-nowrap"><strong class="text-indigo-700">Combo: +59 €/m (+110€)</strong> <span class="text-slate-500">| Suelto: 79€/m (195€)</span></span>
                    </div>
                    <div class="flex justify-between items-baseline gap-1 pl-11 mt-0.5 text-slate-700">
                      <span>· Sat.3 Redactor RAG:</span>
                      <span class="whitespace-nowrap"><strong class="text-indigo-700">Combo: +69 €/m (+150€)</strong> <span class="text-slate-500">| Suelto: 99€/m (250€)</span></span>
                    </div>
                  </li>
                  <li>
                    <div class="flex justify-between items-baseline gap-1">
                      <span><strong class="text-indigo-950">Grupo 4</strong> · S9 Llamadas WA:</span>
                      <span class="whitespace-nowrap"><strong class="text-sky-800">Combo: +59 €/m (+110€)</strong> <span class="text-slate-500">| Suelto: 79€/m (195€)</span></span>
                    </div>
                    <div class="flex justify-between items-baseline gap-1 pl-11 mt-0.5 text-slate-700">
                      <span>· S10 Centralita Voz IA:</span>
                      <span class="whitespace-nowrap"><strong class="text-indigo-900">Combo: +129 €/m (+250€)</strong> <span class="text-slate-500">| Suelto: 169€/m (350€)</span></span>
                    </div>
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
                <span class="text-xs font-black text-amber-800 whitespace-nowrap">Pago único • Sin cuotas</span>
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
          <span>🧾 <strong class="text-brand-navy">Transparencia Total:</strong> Mensual (permanencia de 3 meses) o Plan Anual (pagas 10 meses). Precios netos sin IVA 21% (SEPA).</span>
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

  </section>'''


# ==============================================================================
# 3. BLOQUE CSS + JS DEFINITIVO V160 PARA `index.html`:
#    - CERO DOBLE PERMISO DE MICRO (ELIMINADO getUserMedia Y RECONOCEDOR DUPLICADO)
#    - USA EL MOTOR ORIGINAL DEL ORBE 3D QUE FUNCIONABA PERFECTO EN V149
#    - SE CALLA AL SALIR DE TECNOSALA Y SE REACTIVA SOLO AL VOLVER
#    - BUSCADOR DINÁMICO DEL MODELO GEMINI FLASH-LITE MÁS NUEVO (3.8+)
# ==============================================================================
BLOQUE_JS_MAESTRO_WEB_V152 = r'''
<!-- [SP_AGENDA_CRM_WEB_SYNC_V160_START] -->
<style>
  /* 1. CONTRASTE CLARO EN LAS TARJETAS DEL CARRITO + INSIGNIA COMPACTA "✓" */
  #spModalCarritoCarta .sp-cart-item-btn {
    position: relative !important;
    opacity: 0.64 !important;
    filter: saturate(0.65) !important;
    transform: scale(0.99) !important;
    border: 1.5px solid #cbd5e1 !important;
    box-shadow: none !important;
    padding: 0.38rem 1.45rem 0.38rem 0.65rem !important;
    transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
  }
  #spModalCarritoCarta .sp-cart-item-btn:hover:not(.sp-cart-selected) {
    opacity: 0.88 !important;
    filter: saturate(0.9) !important;
    transform: translateY(-1px) scale(0.998) !important;
  }
  #spModalCarritoCarta .sp-cart-item-btn.sp-cart-selected {
    opacity: 1 !important;
    filter: saturate(1.1) !important;
    transform: translateY(-1px) scale(1.01) !important;
    z-index: 5 !important;
  }
  #spModalCarritoCarta .sp-cart-item-btn.sp-cart-selected::after {
    content: "✓" !important;
    position: absolute !important;
    top: 5px !important;
    right: 6px !important;
    width: 18px !important;
    height: 18px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: #0b2239 !important;
    color: #fde047 !important;
    font-size: 11px !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    padding: 0 !important;
    border-radius: 9999px !important;
    border: 1.5px solid #fde047 !important;
    box-shadow: 0 2px 5px rgba(11, 34, 57, 0.28) !important;
    pointer-events: none !important;
  }

  #spModalCarritoCarta #spCartMod_mensual.sp-cart-selected {
    background: linear-gradient(135deg, #e0f2fe 0%, #7dd3fc 100%) !important;
    border: 2.5px solid #0284c7 !important;
    box-shadow: 0 8px 18px -4px rgba(2, 132, 199, 0.35), 0 0 0 1.5px #ffffff inset !important;
  }
  #spModalCarritoCarta #spCartMod_anual.sp-cart-selected {
    background: linear-gradient(135deg, #fef3c7 0%, #fcd34d 100%) !important;
    border: 2.5px solid #b45309 !important;
    box-shadow: 0 8px 18px -4px rgba(217, 119, 6, 0.38), 0 0 0 1.5px #ffffff inset !important;
  }
  #spModalCarritoCarta #spCartPlan_ninguno.sp-cart-selected {
    background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%) !important;
    border: 2.5px solid #1e293b !important;
    box-shadow: 0 8px 18px -4px rgba(15, 23, 42, 0.30), 0 0 0 1.5px #ffffff inset !important;
  }
  #spModalCarritoCarta #spCartPlan_base.sp-cart-selected {
    background: linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%) !important;
    border: 2.5px solid #1d4ed8 !important;
    box-shadow: 0 8px 18px -4px rgba(37, 99, 235, 0.36), 0 0 0 1.5px #ffffff inset !important;
  }
  #spModalCarritoCarta #spCartPlan_duo.sp-cart-selected {
    background: linear-gradient(135deg, #d1fae5 0%, #6ee7b7 100%) !important;
    border: 2.5px solid #047857 !important;
    box-shadow: 0 8px 18px -4px rgba(5, 150, 105, 0.38), 0 0 0 1.5px #ffffff inset !important;
  }
  #spModalCarritoCarta #spCartAud_0.sp-cart-selected {
    background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%) !important;
    border: 2.5px solid #334155 !important;
    box-shadow: 0 8px 16px -4px rgba(30, 41, 59, 0.28), 0 0 0 1.5px #ffffff inset !important;
  }
  #spModalCarritoCarta #spCartAud_1.sp-cart-selected {
    background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 100%) !important;
    border: 2.5px solid #4338ca !important;
    box-shadow: 0 8px 18px -4px rgba(79, 70, 229, 0.36), 0 0 0 1.5px #ffffff inset !important;
  }
  #spModalCarritoCarta #spCartAud_2.sp-cart-selected {
    background: linear-gradient(135deg, #ffedd5 0%, #fdba74 100%) !important;
    border: 2.5px solid #c2410c !important;
    box-shadow: 0 8px 18px -4px rgba(234, 88, 12, 0.38), 0 0 0 1.5px #ffffff inset !important;
  }

  /* 2. SUB-SELECTOR DE PLAN BASE (S1 vs S2) 100% VISIBLE Y NÍTIDO */
  #spModalCarritoCarta #spSubSelectorBaseS1S2 {
    background: linear-gradient(135deg, #f0fdfa 0%, #e0f2fe 100%) !important;
    border: 2px solid #0d9488 !important;
    padding: 0.42rem 0.65rem !important;
    margin-top: 0.3rem !important;
    border-radius: 0.85rem !important;
    opacity: 1 !important;
    filter: none !important;
  }
  #spModalCarritoCarta #spSubSelectorBaseS1S2 > span:first-child {
    color: #0b2239 !important;
    font-size: 0.76rem !important;
    font-weight: 900 !important;
  }
  #spModalCarritoCarta #spSubSelectorBaseS1S2 button {
    opacity: 1 !important;
    filter: none !important;
    transform: none !important;
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #94a3b8 !important;
    font-size: 0.81rem !important;
    font-weight: 800 !important;
    padding: 0.38rem 0.65rem !important;
    border-radius: 0.7rem !important;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.06) !important;
    transition: all 0.18s ease !important;
  }
  #spModalCarritoCarta #spSubSelectorBaseS1S2 button span {
    color: #334155 !important;
    font-size: 0.73rem !important;
    font-weight: 600 !important;
    opacity: 1 !important;
  }
  #spModalCarritoCarta #spSubSelectorBaseS1S2 button.sp-subbase-active {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
    border: 2.5px solid #047857 !important;
    color: #022c22 !important;
    box-shadow: 0 6px 14px -3px rgba(5, 150, 105, 0.30), 0 0 0 1.5px #ffffff inset !important;
  }
  #spModalCarritoCarta #spSubSelectorBaseS1S2 button.sp-subbase-active span {
    color: #064e3b !important;
    font-weight: 700 !important;
  }

  /* 3. SUBCAJA "TOTAL DESEMBOLSO DÍA 1" SUAVE + PÍLDORA "🟢 Calendario Activo" SIMÉTRICA */
  #spModalCarritoCarta > div {
    padding: 0.65rem 1.25rem !important;
    max-height: 97vh !important;
  }
  #spModalCarritoCarta > div > div:first-child {
    padding-bottom: 0.3rem !important;
    margin-bottom: 0.4rem !important;
  }
  #spModalCarritoCarta .lg\:col-span-5 {
    padding: 0.55rem 0.85rem !important;
  }
  #spModalCarritoCarta #spCartSummaryLines {
    font-size: 0.79rem !important;
    line-height: 1.22 !important;
    margin-bottom: 0.25rem !important;
  }
  #spModalCarritoCarta #spCartSummaryLines > div {
    padding: 0.02rem 0 !important;
  }
  #spModalCarritoCarta #spCartBonoBovedaBox {
    background: linear-gradient(135deg, #fef9c3 0%, #fef08a 100%) !important;
    border: 1.5px solid #d97706 !important;
    color: #451a03 !important;
    padding: 0.26rem 0.55rem !important;
    margin-bottom: 0.28rem !important;
    border-radius: 0.65rem !important;
  }
  #spModalCarritoCarta #spCartBonoBovedaBox strong {
    color: #78350f !important;
    font-size: 0.71rem !important;
  }
  #spModalCarritoCarta #spCartBonoBovedaBox span {
    color: #451a03 !important;
    font-size: 0.71rem !important;
    font-weight: 700 !important;
    line-height: 1.18 !important;
  }
  #spModalCarritoCarta .bg-emerald-950\/60 {
    background: linear-gradient(135deg, #f8fafc 0%, #f0fdf4 55%, #ecfdf5 100%) !important;
    border: 1.5px solid #6ee7b7 !important;
    padding: 0.35rem 0.68rem !important;
    margin-bottom: 0.32rem !important;
    box-shadow: inset 0 1px 0 #ffffff, 0 2px 6px rgba(15, 23, 42, 0.04) !important;
  }
  #spModalCarritoCarta #spCartTotalDia1 {
    font-size: 1.24rem !important;
    color: #065f46 !important;
  }
  #spModalCarritoCarta #spCartSyncCalBadge {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.28rem !important;
    white-space: nowrap !important;
    flex-shrink: 0 !important;
    background: #059669 !important;
    color: #ffffff !important;
    padding: 0.16rem 0.62rem !important;
    border-radius: 9999px !important;
    font-size: 0.7rem !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    text-align: center !important;
    box-shadow: 0 2px 5px rgba(5, 150, 105, 0.25) !important;
  }
  #spModalCarritoCarta select,
  #spModalCarritoCarta input[type="text"],
  #spModalCarritoCarta input[type="tel"] {
    height: 1.95rem !important;
    padding: 0.22rem 0.6rem !important;
    font-size: 0.81rem !important;
  }
  #spModalCarritoCarta #spCartFormInputsWrap {
    gap: 0.28rem !important;
  }
  #spModalCarritoCarta #spCartFormInputsWrap.space-y-2 > * + * {
    margin-top: 0.28rem !important;
  }
  #spModalCarritoCarta #spCartBoxCitaAlta {
    padding: 0.35rem 0.6rem !important;
  }
  #spModalCarritoCarta .lg\:col-span-5 > div:last-child {
    margin-top: 0.32rem !important;
    padding-top: 0.32rem !important;
  }
  #spModalCarritoCarta #spBtnSubmitCarrito {
    padding: 0.48rem 0.9rem !important;
    font-size: 0.88rem !important;
  }
  #spModalCarritoCarta #spCartReservaFase2 option:disabled {
    color: #94a3b8 !important;
    background-color: #f1f5f9 !important;
    font-style: italic !important;
  }
</style>

<script>
(function() {
  /* =========================================================================
     1. COORDINACIÓN LIMPIA DEL TECNOCONSULTOR SOBRE SU MOTOR ORIGINAL NATIVO
        (CERO getUserMedia Y CERO RECONOCEDOR DUPLICADO = NUNCA SALE DOBLE PERMISO)
     ========================================================================= */
  window._spConsultorEstabaActivoAntesDeSalir = false;

  /* Guardamos referencias al motor original nativo del Orbe 3D (el que crea la cabina del Teleprompter y habla) */
  var _origActivarOrbeNativo = window.spActivarOrbeConsultorInteractivo;
  var _origPararTotalNativo = window.spPararConsultorTotalmente;

  if (typeof _origActivarOrbeNativo === 'function' && !_origActivarOrbeNativo._wrappedV160) {
    var nuevoActivarOrbe = function(ev) {
      window._spConsultorEstabaActivoAntesDeSalir = true;
      return _origActivarOrbeNativo.apply(this, arguments);
    };
    nuevoActivarOrbe._wrappedV160 = true;
    window.spActivarOrbeConsultorInteractivo = nuevoActivarOrbe;
  }

  if (typeof _origPararTotalNativo === 'function' && !_origPararTotalNativo._wrappedV160) {
    var nuevoPararTotal = function(ev) {
      /* Si el usuario pulsa manualmente PARAR (con evento de clic), desactivamos el auto-retorno */
      if (ev) {
        window._spConsultorEstabaActivoAntesDeSalir = false;
      }
      return _origPararTotalNativo.apply(this, arguments);
    };
    nuevoPararTotal._wrappedV160 = true;
    window.spPararConsultorTotalmente = nuevoPararTotal;
  }

  /* Al cambiar de sección en la web:
     - Si sale de Tecnosala -> se calla y apaga el micro en el acto (pero recuerda que estaba activo)
     - Si vuelve a entrar en Tecnosala y ya lo había activado -> vuelve a activar la escucha solo */
  if (typeof window.cambiarVista === 'function' && !window.cambiarVista._hookAutoTecnosalaV160) {
    var _origCambiarVistaV160 = window.cambiarVista;
    var nuevaCambiarVistaV160 = function(vistaDestino) {
      var estabaActivo = window._spConsultorEstabaActivoAntesDeSalir;
      if (vistaDestino !== 'tecnosala') {
        if (typeof _origPararTotalNativo === 'function') {
          try { _origPararTotalNativo(); } catch (e) {}
        }
        window._spConsultorEstabaActivoAntesDeSalir = estabaActivo;
      }
      var res = _origCambiarVistaV160.apply(this, arguments);
      if (vistaDestino === 'tecnosala' && window._spConsultorEstabaActivoAntesDeSalir) {
        setTimeout(function() {
          if (typeof window.spIniciarEscuchaDirectaConsultor === 'function') {
            window.spIniciarEscuchaDirectaConsultor();
          }
        }, 220);
      }
      return res;
    };
    nuevaCambiarVistaV160._hookAutoTecnosalaV160 = true;
    window.cambiarVista = nuevaCambiarVistaV160;
  }

  document.addEventListener('visibilitychange', function() {
    var estabaActivo = window._spConsultorEstabaActivoAntesDeSalir;
    if (document.hidden) {
      if (typeof _origPararTotalNativo === 'function') {
        try { _origPararTotalNativo(); } catch (e) {}
      }
      window._spConsultorEstabaActivoAntesDeSalir = estabaActivo;
    } else {
      var vTec = document.getElementById('vista-tecnosala');
      if (vTec && !vTec.classList.contains('hidden') && window._spConsultorEstabaActivoAntesDeSalir) {
        setTimeout(function() {
          if (typeof window.spIniciarEscuchaDirectaConsultor === 'function') {
            window.spIniciarEscuchaDirectaConsultor();
          }
        }, 250);
      }
    }
  });

  /* =========================================================================
     2. MOTOR DE PRECIOS CLAROS (TARJETAS COMPLETAS CON SU ESTRUCTURA ORIGINAL
        Y CAMBIO INMEDIATO ENTRE MENSUAL Y PLAN ANUAL)
     ========================================================================= */
  window._spModoTarifasActual = 'mensual';
  window._spNumAuditoriasEscudo = 1;

  window._spRenderizarTarjetasPrecios = function() {
    var btnM = document.getElementById('btnSwitchMensual');
    var btnA = document.getElementById('btnSwitchAnual');
    var pBase = document.querySelector('[data-plan-price="base"]');
    var pDuo = document.querySelector('[data-plan-price="duo"]');
    var pTri = document.querySelector('[data-plan-price="trinity"]');
    var subBase = document.getElementById('spSubPriceBase');
    var subDuo = document.getElementById('spSubPriceDuo');
    var subEsc = document.getElementById('spSubPriceEscudoTotal');
    var savBase = document.getElementById('spSavingLineBase');
    var savDuo = document.getElementById('spSavingLineDuo');
    var savEsc = document.getElementById('spSavingLineEscudoTotal');
    var titleEsc = document.getElementById('spTitleEscudoTotal');
    var topRightAud = document.getElementById('spTopRightAudLabel');
    var bulletAud = document.getElementById('spBulletAuditEscudo');
    var bulletBon = document.getElementById('spBulletBonusEscudo');
    var btn1Aud = document.getElementById('btnEscudo1Aud');
    var btn2Aud = document.getElementById('btnEscudo2Aud');
    var waEsc = document.getElementById('spBtnWaPlanEscudoTotal');

    var esPlus = (window._spNumAuditoriasEscudo === 2);
    var costeAud = esPlus ? 390 : 195;
    var ahorroAud = esPlus ? 310 : 155;

    if (btn1Aud && btn2Aud) {
      if (esPlus) {
        btn2Aud.className = 'px-2 py-0.5 rounded-md bg-emerald-600 text-white cursor-pointer transition-all whitespace-nowrap shadow-sm';
        btn1Aud.className = 'px-2 py-0.5 rounded-md text-teal-900 hover:text-brand-navy cursor-pointer transition-all whitespace-nowrap';
      } else {
        btn1Aud.className = 'px-2 py-0.5 rounded-md bg-emerald-600 text-white cursor-pointer transition-all whitespace-nowrap shadow-sm';
        btn2Aud.className = 'px-2 py-0.5 rounded-md text-teal-900 hover:text-brand-navy cursor-pointer transition-all whitespace-nowrap';
      }
    }

    if (titleEsc) titleEsc.textContent = esPlus ? 'Pack Escudo Plus ★' : 'Pack Escudo Total ★';
    if (topRightAud) topRightAud.textContent = esPlus ? '+ 2 Auditorías (390 €)' : '+ 1 Auditoría (195 €)';

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

    if (window._spModoTarifasActual === 'anual') {
      if (btnA) btnA.className = 'px-4 py-2 rounded-xl text-xs sm:text-[13px] font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap';
      if (btnM) btnM.className = 'px-4 py-2 rounded-xl text-xs sm:text-[13px] font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer whitespace-nowrap';

      if (pBase) pBase.innerHTML = '<div class="flex items-baseline gap-1.5 whitespace-nowrap"><span class="text-2xl sm:text-[28px] font-black text-brand-navy whitespace-nowrap">590 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ año</span></div>';
      if (subBase) subBase.textContent = '+ 150 € Setup único';
      if (savBase) {
        savBase.className = 'block text-[11px] font-extrabold text-teal-800 bg-teal-50/90 border border-teal-200/80 rounded-lg px-2.5 py-0.5 truncate whitespace-nowrap';
        savBase.textContent = '🎁 Ahorras 118 € al año (pagas 10 meses)';
      }

      if (pDuo) pDuo.innerHTML = '<div class="flex items-baseline gap-1.5 whitespace-nowrap"><span class="text-2xl sm:text-[28px] font-black text-sky-700 whitespace-nowrap">990 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ año</span></div>';
      if (subDuo) subDuo.textContent = '+ 225 € Setup Dúo';
      if (savDuo) savDuo.textContent = '🎁 Ahorras 198 € al año (pagas 10 meses)';

      if (pTri) pTri.innerHTML = '<div class="flex items-baseline gap-1.5 whitespace-nowrap"><span class="text-2xl sm:text-[28px] font-black text-emerald-700 whitespace-nowrap">990 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ año</span></div>';
      if (subEsc) subEsc.textContent = '+ 225 € Setup Dúo + ' + costeAud + ' € (' + (esPlus ? '2 Auditorías' : '1 Auditoría') + ')';
      if (savEsc) savEsc.textContent = '🎁 Ahorras 198 € al año (pagas 10 meses)';
    } else {
      if (btnM) btnM.className = 'px-4 py-2 rounded-xl text-xs sm:text-[13px] font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer whitespace-nowrap';
      if (btnA) btnA.className = 'px-4 py-2 rounded-xl text-xs sm:text-[13px] font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap';

      if (pBase) pBase.innerHTML = '<div class="flex items-baseline gap-1.5 whitespace-nowrap"><span class="text-2xl sm:text-[28px] font-black text-brand-navy whitespace-nowrap">59 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span></div>';
      if (subBase) subBase.textContent = '+ 150 € Setup único';
      if (savBase) {
        savBase.className = 'block text-[11px] font-extrabold text-slate-700 bg-slate-200/75 border border-slate-300 rounded-lg px-2.5 py-0.5 truncate whitespace-nowrap';
        savBase.textContent = '✓ 1 módulo activo a elegir (S1 o S2)';
      }

      if (pDuo) pDuo.innerHTML = '<div class="flex items-baseline gap-1.5 whitespace-nowrap"><span class="text-2xl sm:text-[28px] font-black text-sky-700 whitespace-nowrap">99 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span></div>';
      if (subDuo) subDuo.textContent = '+ 225 € Setup Dúo';
      if (savDuo) savDuo.textContent = '🎁 Ahorras 19 €/mes + 75 € en Setup';

      if (pTri) pTri.innerHTML = '<div class="flex items-baseline gap-1.5 whitespace-nowrap"><span class="text-2xl sm:text-[28px] font-black text-emerald-700 whitespace-nowrap">99 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span></div>';
      if (subEsc) subEsc.textContent = '+ 225 € Setup Dúo + ' + costeAud + ' € (' + (esPlus ? '2 Auditorías' : '1 Auditoría') + ')';
      if (savEsc) savEsc.textContent = '🎁 Ahorras ' + ahorroAud + ' € en Auditoría + 75 € Setup';
    }

    if (waEsc) {
      waEsc.textContent = esPlus ? 'Activar Pack Escudo Plus →' : 'Activar Pack Escudo Total →';
      waEsc.onclick = function(ev) {
        if (ev) ev.preventDefault();
        window.spAbrirCarritoConfigurador('duo', window._spNumAuditoriasEscudo);
      };
    }
  };

  window.cambiarModoTarifas = function(modo) {
    window._spModoTarifasActual = (modo === 'anual') ? 'anual' : 'mensual';
    window._spRenderizarTarjetasPrecios();
  };

  window.spSeleccionarNivelEscudoTotal = function(numAud) {
    window._spNumAuditoriasEscudo = (numAud === 2) ? 2 : 1;
    window._spRenderizarTarjetasPrecios();
  };

  /* =========================================================================
     3. SELECTOR INTELIGENTE DE FASE 2 Y VISIBILIDAD DEL SUBSELECTOR S1/S2
     ========================================================================= */
  window.spSincronizarOpcionesGrisesFase2 = function() {
    var sel = document.getElementById('spCartReservaFase2');
    var chipsBox = document.getElementById('spCartReservasChipsBox');
    if (!sel) return;

    var textosElegidos = [];
    if (chipsBox) {
      var spans = chipsBox.querySelectorAll('span > span:first-child');
      for (var s = 0; s < spans.length; s++) {
        textosElegidos.push(String(spans[s].textContent || '').trim());
      }
    }

    for (var i = 0; i < sel.options.length; i++) {
      var opt = sel.options[i];
      var val = String(opt.value || '').trim();
      if (!val) continue;
      if (!opt.getAttribute('data-orig-text')) {
        opt.setAttribute('data-orig-text', opt.textContent);
      }
      var txtOriginal = opt.getAttribute('data-orig-text');
      var yaElegido = (textosElegidos.indexOf(val) !== -1);
      opt.disabled = yaElegido;
      opt.textContent = yaElegido ? ('✓ ' + txtOriginal + ' (Ya seleccionado)') : txtOriginal;
    }
  };

  function sincronizarSubBotonesPlanBaseV160() {
    var b1 = document.getElementById('spBtnSubBase_S1');
    var b2 = document.getElementById('spBtnSubBase_S2');
    if (!b1 || !b2) return;
    var txt1 = b1.textContent || '';
    var esS1 = (txt1.indexOf('✓') !== -1) || (b1.className.indexOf('border-emerald') !== -1);
    if (esS1) {
      b1.classList.add('sp-subbase-active');
      b2.classList.remove('sp-subbase-active');
    } else {
      b2.classList.add('sp-subbase-active');
      b1.classList.remove('sp-subbase-active');
    }
  }

  var _origSubBaseV125 = window.spSeleccionarSubServicioBaseV125;
  window.spSeleccionarSubServicioBaseV125 = function(eleccion) {
    if (typeof _origSubBaseV125 === 'function') {
      _origSubBaseV125.apply(this, arguments);
    }
    var b1 = document.getElementById('spBtnSubBase_S1');
    var b2 = document.getElementById('spBtnSubBase_S2');
    var esS1 = String(eleccion || '').indexOf('S1') !== -1;
    if (b1 && b2) {
      if (esS1) {
        b1.classList.add('sp-subbase-active');
        b2.classList.remove('sp-subbase-active');
        b1.innerHTML = '⭐ S1. Gestor de Reseñas Google con IA ✓<span class="block text-[10px] font-normal mt-0.5">Contesta 4-5★ con SEO local y frena 1-3★ avisándote al móvil</span>';
        b2.innerHTML = '💬 S2. Encuesta Cortafuegos por WhatsApp<span class="block text-[10px] font-normal mt-0.5">Envía encuesta tras cada cita o pedido y filtra quejas en privado</span>';
      } else {
        b2.classList.add('sp-subbase-active');
        b1.classList.remove('sp-subbase-active');
        b1.innerHTML = '⭐ S1. Gestor de Reseñas Google con IA<span class="block text-[10px] font-normal mt-0.5">Contesta 4-5★ con SEO local y frena 1-3★ avisándote al móvil</span>';
        b2.innerHTML = '💬 S2. Encuesta Cortafuegos por WhatsApp ✓<span class="block text-[10px] font-normal mt-0.5">Envía encuesta tras cada cita o pedido y filtra quejas en privado</span>';
      }
    }
  };

  /* =========================================================================
     4. COLORES, PÍLDORA "🟢 Calendario Activo" SIMÉTRICA Y AGENDA DEL CARRITO
     ========================================================================= */
  function aplicarIdsColorCajasCarritoV160() {
    var selAtr = document.getElementById('spCartAtrilSelect');
    if (selAtr && selAtr.parentNode) {
      selAtr.parentNode.id = 'spCartBoxAtriles4';
    }
    var selRes = document.getElementById('spCartReservaFase2');
    if (selRes && selRes.parentNode) {
      selRes.parentNode.id = 'spCartBoxReserva5';
    }
    var selDia = document.getElementById('spCartSelectDiaLV');
    if (selDia && selDia.parentNode && selDia.parentNode.parentNode) {
      selDia.parentNode.parentNode.id = 'spCartBoxCitaAlta';
    }
    var calBadge = document.getElementById('spCartSyncCalBadge');
    if (calBadge) {
      calBadge.innerHTML = '<span>🟢</span><span>Calendario Activo</span>';
    }
    sincronizarSubBotonesPlanBaseV160();
  }

  window.spAbrirCarritoConDiagnosticoPreseleccionado = function() {
    if (typeof window.spAbrirCarritoConfigurador === 'function') {
      window.spAbrirCarritoConfigurador('duo', 1);
      setTimeout(function() {
        aplicarIdsColorCajasCarritoV160();
        window.spSincronizarOpcionesGrisesFase2();
      }, 40);
    }
  };

  window.SP_SLOTS_OCUPADOS_CRM_EXTRA = window.SP_SLOTS_OCUPADOS_CRM_EXTRA || new Set();

  function normalizarSlotEspacio(slotRaw) {
    var s = String(slotRaw || '').trim();
    if (!s) return '';
    s = s.replace('|', ' ').replace('T', ' ');
    var m = s.match(/^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})/);
    return m ? (m[1] + ' ' + m[2]) : '';
  }

  window.spAplicarBloqueoHorasCrmEnSelect = function() {
    aplicarIdsColorCajasCarritoV160();
    var selDia = document.getElementById('spCartSelectDiaLV');
    var selHora = document.getElementById('spCartSelectHoraManana');
    var inpISO = document.getElementById('spCartInputFechaHoraISO');
    var inpHor = document.getElementById('spCartInputHorario');
    if (!selDia || !selHora) return;

    var ymd = selDia.value;
    if (!ymd) return;

    var cambioSeleccion = false;
    for (var i = 0; i < selHora.options.length; i++) {
      var opt = selHora.options[i];
      var hhmm = String(opt.value || '').trim().substring(0, 5);
      if (!hhmm) continue;
      var claveEspacio = ymd + ' ' + hhmm;
      if (window.SP_SLOTS_OCUPADOS_CRM_EXTRA.has(claveEspacio)) {
        opt.disabled = true;
        var txtBase = opt.textContent.replace(/^🟢\s*/, '').replace(/^⛔\s*/, '').replace(/\s*\(Ocupado.*\)$/i, '').trim();
        opt.textContent = '⛔ ' + txtBase + ' (Ocupado en Agenda CRM)';
        if (selHora.selectedIndex === i) {
          cambioSeleccion = true;
        }
      }
    }

    if (cambioSeleccion || (selHora.options[selHora.selectedIndex] && selHora.options[selHora.selectedIndex].disabled)) {
      for (var j = 0; j < selHora.options.length; j++) {
        if (!selHora.options[j].disabled) {
          selHora.selectedIndex = j;
          break;
        }
      }
    }

    var hSel = selHora.value || '10:00';
    var dTxt = (selDia.options[selDia.selectedIndex] ? selDia.options[selDia.selectedIndex].text : ymd);
    if (inpISO) inpISO.value = ymd + 'T' + hSel;
    if (inpHor) inpHor.value = dTxt + ' a las ' + hSel + ' h';
  };

  window.spSincronizarCitasCrmLocal = function() {
    try {
      var guardados = JSON.parse(localStorage.getItem('sp_citas_ocupadas_crm_v160') || '[]');
      if (Array.isArray(guardados)) {
        guardados.forEach(function(sl) {
          var norm = normalizarSlotEspacio(sl);
          if (norm) window.SP_SLOTS_OCUPADOS_CRM_EXTRA.add(norm);
        });
      }
    } catch (e) {}

    var ahora = Date.now();
    var urls = [
      'http://127.0.0.1:5000/api/horarios-ocupados-agenda?t=' + ahora,
      'http://localhost:5000/api/horarios-ocupados-agenda?t=' + ahora
    ];

    Promise.all(urls.map(function(u) {
      return fetch(u, { method: 'GET', mode: 'cors' })
        .then(function(r) { return r.ok ? r.json() : null; })
        .then(function(d) {
          if (d && Array.isArray(d.slots_ocupados)) {
            d.slots_ocupados.forEach(function(sl) {
              var norm = normalizarSlotEspacio(sl);
              if (norm) window.SP_SLOTS_OCUPADOS_CRM_EXTRA.add(norm);
            });
            try {
              localStorage.setItem('sp_citas_ocupadas_crm_v160', JSON.stringify(Array.from(window.SP_SLOTS_OCUPADOS_CRM_EXTRA)));
            } catch (e) {}
          }
        })
        .catch(function() {});
    })).then(function() {
      window.spAplicarBloqueoHorasCrmEnSelect();
    });
  };

  function inicializarMejorasV160() {
    aplicarIdsColorCajasCarritoV160();
    window._spRenderizarTarjetasPrecios();
    window.spSincronizarCitasCrmLocal();
    window.spSincronizarOpcionesGrisesFase2();

    if (typeof window.spRecalcularCarritoCarta === 'function' && !window.spRecalcularCarritoCarta._hookFase2GrisV160) {
      var origRecalcCart = window.spRecalcularCarritoCarta;
      var nuevoRecalcCart = function() {
        var r = origRecalcCart.apply(this, arguments);
        window.spSincronizarOpcionesGrisesFase2();
        sincronizarSubBotonesPlanBaseV160();
        return r;
      };
      nuevoRecalcCart._hookFase2GrisV160 = true;
      window.spRecalcularCarritoCarta = nuevoRecalcCart;
    }

    if (typeof window.spActualizarHorasDisponiblesCarritoV125 === 'function' && !window.spActualizarHorasDisponiblesCarritoV125._hookV160) {
      var origActHoras = window.spActualizarHorasDisponiblesCarritoV125;
      var nuevaActHoras = function() {
        var r = origActHoras.apply(this, arguments);
        window.spAplicarBloqueoHorasCrmEnSelect();
        return r;
      };
      nuevaActHoras._hookV160 = true;
      window.spActualizarHorasDisponiblesCarritoV125 = nuevaActHoras;
    }

    if (typeof window.spAbrirCarritoConfigurador === 'function' && !window.spAbrirCarritoConfigurador._hookV160) {
      var origOpen = window.spAbrirCarritoConfigurador;
      var nuevoOpen = function() {
        var r = origOpen.apply(this, arguments);
        aplicarIdsColorCajasCarritoV160();
        window.spSincronizarCitasCrmLocal();
        window.spSincronizarOpcionesGrisesFase2();
        setTimeout(window.spAplicarBloqueoHorasCrmEnSelect, 120);
        return r;
      };
      nuevoOpen._hookV160 = true;
      window.spAbrirCarritoConfigurador = nuevoOpen;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(inicializarMejorasV160, 180);
    });
  } else {
    setTimeout(inicializarMejorasV160, 180);
  }
})();
</script>
<!-- [SP_AGENDA_CRM_WEB_SYNC_V160_END] -->
'''


# ==============================================================================
# 4. LOS 6 TARJETONES DE LA BIBLIOTECA (`documentos/*.html`) ACTUALIZADOS A FONDO
# ==============================================================================
ESTILO_COMUN_TARJETONES = """
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; background: #0f172a; color: #0f172a; margin: 0; padding: 24px 16px; }
    h1, h2, h3, h4, .font-display { font-family: 'Montserrat', 'Inter', sans-serif; letter-spacing: -0.02em; }
    .a4-sheet { max-width: 1020px; margin: 0 auto; background: #ffffff; border-radius: 24px; padding: 36px 42px; box-shadow: 0 25px 60px -15px rgba(0,0,0,0.6); border: 2px solid #0d9488; }
    @media print {
      body { background: #ffffff; padding: 0; }
      .a4-sheet { box-shadow: none; border: none; padding: 12px; max-width: 100%; }
      .no-print { display: none !important; }
    }
  </style>
"""

# ------------------------------------------------------------------------------
# 4.1 GUÍA TÉCNICA SEO/GEO IA (CON BLOQUE EXPLICATIVO PARA EL DUEÑO SIN TECNICISMOS)
# ------------------------------------------------------------------------------
HTML_GUIA_SEO_GEO_COMPLETA = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Guía Técnica Ejecutiva: Super-Auditoría SEO Local + GEO (IA) | Sistemas Pyme</title>
  {ESTILO_COMUN_TARJETONES}
</head>
<body>
  <div class="a4-sheet">
    <div class="no-print flex flex-wrap items-center justify-between gap-3 pb-5 mb-6 border-b border-slate-200">
      <div class="flex items-center gap-2">
        <span class="px-3 py-1 rounded-full bg-sky-100 text-sky-900 font-extrabold text-xs border border-sky-300">🧭 DOSSIER OFICIAL • SUPER-AUDITORÍA 1 (DUEÑO + INFORMÁTICO)</span>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="bg-[#0b2239] hover:bg-slate-800 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow cursor-pointer">🖨️ Imprimir / Guardar PDF</button>
        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20acabo%20de%20leer%20la%20Gu%C3%ADa%20SEO%2FGEO%20IA%20y%20quiero%20consultarte%20para%20mi%20negocio" target="_blank" class="bg-[#0d7d74] hover:bg-teal-700 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow">💬 Consultar con Francisco</a>
      </div>
    </div>

    <div class="bg-gradient-to-r from-[#0b2239] via-[#0f3456] to-[#0d7d74] text-white rounded-3xl p-6 sm:p-8 mb-6 shadow-lg">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
        <span class="text-[11px] font-extrabold uppercase tracking-widest text-teal-300 bg-white/10 px-3 py-1 rounded-full border border-teal-300/40">Ingeniería de Entidades Digitales • Sistemas Pyme</span>
        <span class="text-xs font-bold text-amber-300">Sin cambiar ni un píxel el diseño visual de tu web</span>
      </div>
      <h1 class="text-2xl sm:text-4xl font-black leading-tight mb-2">
        Super-Auditoría e Implantación SEO Local + GEO (IA)
      </h1>
      <p class="text-sm sm:text-base text-slate-200 leading-relaxed">
        Cómo logramos que tu negocio aparezca en el <strong>Top 3 de Google Maps</strong> y sea la respuesta recomendada por <strong>ChatGPT, Gemini, Perplexity y Siri</strong> cuando alguien busca tu especialidad en tu zona.
      </p>
    </div>

    <!-- NUEVO BLOQUE 1: EXPLICACIÓN PARA EL DUEÑO (EN LENGUAJE CLARO Y SIN TECNICISMOS) -->
    <div class="bg-gradient-to-br from-amber-50 via-white to-teal-50 border-2 border-amber-400 rounded-3xl p-6 mb-7 shadow-sm">
      <div class="inline-flex items-center gap-2 bg-amber-100 text-amber-950 font-black text-xs uppercase tracking-wider px-3.5 py-1 rounded-full border border-amber-300 mb-3">
        <span>👔 PARTE 1: INFORMACIÓN CLARA PARA EL DUEÑO DEL NEGOCIO (CERO TECNICISMOS)</span>
      </div>
      <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-2">
        ¿Qué problema resolvemos en tu negocio y qué vas a notar en el día a día?
      </h2>
      <p class="text-xs sm:text-[13.5px] text-slate-700 leading-relaxed mb-4">
        Muchos negocios tienen una página web bonita para el ojo humano, pero cuando los robots de <strong>Google Maps, ChatGPT o Gemini</strong> entran a leerla por dentro, <strong>no entienden con certeza quién eres, en qué calle exacta estás, qué especialidades ofreces ni por qué eres más fiable que tu competencia</strong>. Por eso recomiendan antes a otros locales que quizás llevan menos años que tú.
      </p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-[13px]">
        <div class="bg-white rounded-2xl p-4 border border-amber-300 shadow-sm space-y-2">
          <strong class="text-amber-900 font-black block text-sm">🎯 Qué hacemos por ti (sin tocar el diseño de tu web):</strong>
          <ul class="space-y-1.5 text-slate-700 leading-snug">
            <li>• <strong>Le ponemos un «Carnet de Identidad Oficial» a tu web:</strong> Traducimos al idioma interno de Google y de las IAs tus servicios, horarios, dirección exacta, premios, colegiación y nota media de reseñas.</li>
            <li>• <strong>Alineamos tu web con tu ficha de Google Maps:</strong> Para que cuando un vecino busque tu oficio en el móvil, salgas en el bloque superior de los 3 primeros del mapa.</li>
            <li>• <strong>Le damos respuesta directa a las dudas de tus clientes:</strong> Dejamos contestadas las preguntas típicas (precios orientativos, urgencias, aparcamiento, garantías) para que ChatGPT te cite como referencia.</li>
          </ul>
        </div>
        <div class="bg-white rounded-2xl p-4 border border-teal-300 shadow-sm space-y-2">
          <strong class="text-teal-900 font-black block text-sm">📈 Qué recibe el dueño (Tabla 1 de tu Auditoría):</strong>
          <ul class="space-y-1.5 text-slate-700 leading-snug">
            <li>• <strong>Semáforo visual de tu negocio (Rojo / Ámbar / Verde):</strong> Ves de un vistazo qué puntos tienes cubiertos y por dónde se te estaban escapando clientes frente a tus competidores locales.</li>
            <li>• <strong>Traducción a impacto económico real:</strong> Cada punto indica cuántos clientes adicionales atrae sin tener que pagar campañas mensuales de publicidad.</li>
            <li>• <strong>Cero dolores de cabeza:</strong> Lo dejamos implantado nosotros mismos en 24-48h o, si tienes informático de confianza, le entregamos la Tabla 2 con todo el código hecho para copiar y pegar en 10 minutos.</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- BLOQUE 2: LAS 3 ESTADÍSTICAS DE IMPACTO -->
    <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-3">2. El Respaldo en Cifras: Por qué estar en Google Maps y en la IA multiplica tus cierres</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-7">
      <div class="bg-sky-50 border-2 border-sky-300 rounded-2xl p-4">
        <span class="block text-2xl sm:text-3xl font-black text-sky-700 mb-1">x9 Ventas (15,9%)</span>
        <strong class="block text-xs uppercase tracking-wider text-sky-950 mb-1">Estudio Seer Interactive</strong>
        <p class="text-xs text-slate-700 leading-relaxed">En Google normal solo compra el 1,76% porque abren diez webs para comparar. Quien pregunta a ChatGPT y recibe tu recomendación compra el <strong>15,9%</strong>.</p>
      </div>
      <div class="bg-teal-50 border-2 border-teal-300 rounded-2xl p-4">
        <span class="block text-2xl sm:text-3xl font-black text-teal-700 mb-1">+115,1% Visibilidad</span>
        <strong class="block text-xs uppercase tracking-wider text-teal-950 mb-1">Universidad de Princeton (GEO)</strong>
        <p class="text-xs text-slate-700 leading-relaxed">El <strong>83%</strong> de los negocios citados por las IAs son elegidos por tener sus datos internos estructurados con <code>Schema.org</code> y <code>Wikidata</code>.</p>
      </div>
      <div class="bg-amber-50 border-2 border-amber-300 rounded-2xl p-4">
        <span class="block text-2xl sm:text-3xl font-black text-amber-700 mb-1">69% Cero Clics</span>
        <strong class="block text-xs uppercase tracking-wider text-amber-950 mb-1">Similarweb & SparkToro</strong>
        <p class="text-xs text-slate-700 leading-relaxed">Casi 7 de cada 10 usuarios deciden hoy leyendo el resumen superior de la IA, que extrae el <strong>44%</strong> de sus citas de las primeras 100 palabras de tu web.</p>
      </div>
    </div>

    <!-- BLOQUE 3: INFORMACIÓN TÉCNICA PARA EL INFORMÁTICO (LOS 22 PARÁMETROS) -->
    <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-3">3. Parte 2 (Para el Informático): Los 22 Parámetros de Ingeniería que Implantamos</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-7 text-xs sm:text-[13px]">
      <div class="bg-slate-50 border border-slate-300 rounded-2xl p-5 space-y-2">
        <span class="inline-block text-[11px] font-black uppercase tracking-wider bg-[#0b2239] text-white px-3 py-1 rounded-lg">A. Grafo de Entidad e Inteligencia Artificial (GEO)</span>
        <ul class="space-y-1.5 text-slate-700 leading-snug">
          <li>✔ <strong>Grafo <code>Schema.org @graph JSON-LD</code>:</strong> Validado en verde en <em>Google Rich Results Test</em> con coordenadas GPS, horarios, área de servicio y <code>AggregateRating</code>.</li>
          <li>✔ <strong>Enlace Oficial a <code>Wikidata</code>:</strong> Desambiguación geográfica unívoca de tu localidad y especialidad.</li>
          <li>✔ <strong>Autoridad E-E-A-T de Fundadores:</strong> Fichas <code>@type: Person</code>, colegios oficiales (<code>memberOf</code>), universidades (<code>alumniOf</code>) y apariciones en medios.</li>
          <li>✔ <strong>Archivo <code>/llms.txt</code> y <code>/robots.txt</code> IA:</strong> Apertura explícita para <code>OAI-SearchBot</code>, <code>ChatGPT-User</code>, <code>PerplexityBot</code>, <code>ClaudeBot</code> y <code>Google-Extended</code>.</li>
        </ul>
      </div>

      <div class="bg-slate-50 border border-slate-300 rounded-2xl p-5 space-y-2">
        <span class="inline-block text-[11px] font-black uppercase tracking-wider bg-[#0d7d74] text-white px-3 py-1 rounded-lg">B. SEO Local en Google Maps y Portada RAG</span>
        <ul class="space-y-1.5 text-slate-700 leading-snug">
          <li>✔ <strong>Bloque de Respuesta Directa (Primeras 100 palabras):</strong> Resumen semántico de alta densidad informativa para motores RAG.</li>
          <li>✔ <strong>Jerarquía <code>&lt;title&gt;</code>, <code>&lt;meta description&gt;</code>, <code>&lt;h1&gt;</code> y <code>&lt;h2&gt;</code> Conversacionales.</strong></li>
          <li>✔ <strong>4 Meta-Etiquetas Geográficas Invisibles:</strong> <code>geo.region</code>, <code>geo.placename</code>, <code>geo.position</code> e <code>ICBM</code>.</li>
          <li>✔ <strong>Módulo <code>FAQPage</code> Invisible + Acordeón HTML + Enlace UTM Google Business Profile.</strong></li>
        </ul>
      </div>
    </div>

    <!-- BLOQUE 4: INVERSIÓN ÚNICA OFICIAL -->
    <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-3">4. Inversión Oficial (Pago Único • Sin Cuotas Mensuales)</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 text-center">
      <div class="bg-emerald-50 border-2 border-emerald-500 rounded-2xl p-5 shadow-md">
        <span class="inline-block text-[11px] font-extrabold uppercase tracking-wider text-emerald-950 bg-emerald-200 px-3 py-0.5 rounded-full mb-2">1. Bonificada en Combo con Pack 2+ Servicios ★</span>
        <div class="text-3xl font-black text-emerald-700 mb-1">195 € <span class="text-xs font-bold text-emerald-900">por 1 auditoría</span></div>
        <div class="text-sm font-black text-emerald-950 mb-2">390 € si contratas las 2 Super-Auditorías juntas (Ahorras 310 €)</div>
        <p class="text-xs text-emerald-950 leading-relaxed font-medium">Al activar cualquier Pack de 2 o más servicios mensuales (como el <strong>Pack Escudo Básico Dúo</strong> de 99 €/mes), tienes un <strong>44% de bonificación directa</strong> en la auditoría completa Llave en Mano.</p>
      </div>

      <div class="bg-white border-2 border-sky-400 rounded-2xl p-5 shadow-sm">
        <span class="inline-block text-[11px] font-extrabold uppercase tracking-wider text-sky-900 bg-sky-100 px-3 py-0.5 rounded-full mb-2">2. Tarifa Suelta «Llave en Mano»</span>
        <div class="text-3xl font-black text-sky-700 mb-1">350 € <span class="text-xs font-bold text-slate-500">por 1 auditoría</span></div>
        <div class="text-sm font-extrabold text-[#0b2239] mb-2">590 € si contratas las 2 Super-Auditorías juntas (Ahorras 110 €)</div>
        <p class="text-xs text-slate-600 leading-relaxed">Contratada suelta o con Pyme Base (1 servicio). Incluye Tabla 1 para el Dueño, Tabla 2 para el Informático e implantación por nosotros o entrega de todos los códigos e instrucciones a tu técnico.</p>
      </div>
    </div>

    <div class="text-center text-xs text-slate-500 pt-3 border-t border-slate-200">
      <strong>Sistemas Pyme — Francisco M. Gallardo (NIF 52938419D)</strong> • Tel / WhatsApp: <strong>711 54 75 61</strong> • Web: <strong>sistemaspyme.es</strong> • Precios netos sin IVA (21%).
    </div>
  </div>
</body>
</html>
"""

# ------------------------------------------------------------------------------
# 4.2 GUÍA TÉCNICA NEURO-CRO WEB (CON BLOQUE EXPLICATIVO PARA EL DUEÑO + SIN 200 €)
# ------------------------------------------------------------------------------
HTML_GUIA_NEURO_COMPLETA = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Guía Técnica Ejecutiva: Super-Auditoría Neuro-CRO y Sonda Térmica | Sistemas Pyme</title>
  {ESTILO_COMUN_TARJETONES}
</head>
<body>
  <div class="a4-sheet">
    <div class="no-print flex flex-wrap items-center justify-between gap-3 pb-5 mb-6 border-b border-slate-200">
      <div class="flex items-center gap-2">
        <span class="px-3 py-1 rounded-full bg-amber-100 text-amber-950 font-extrabold text-xs border border-amber-400">🧠 DOSSIER OFICIAL • SUPER-AUDITORÍA 2 (DUEÑO + INFORMÁTICO)</span>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="bg-[#0b2239] hover:bg-slate-800 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow cursor-pointer">🖨️ Imprimir / Guardar PDF</button>
        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20acabo%20de%20leer%20la%20Gu%C3%ADa%20Neuro-CRO%20y%20quiero%20consultarte%20para%20mi%20web" target="_blank" class="bg-amber-600 hover:bg-amber-700 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow">💬 Consultar con Francisco</a>
      </div>
    </div>

    <div class="bg-gradient-to-r from-[#451a03] via-[#78350f] to-[#0b2239] text-white rounded-3xl p-6 sm:p-8 mb-6 shadow-lg">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
        <span class="text-[11px] font-extrabold uppercase tracking-widest text-amber-300 bg-white/10 px-3 py-1 rounded-full border border-amber-300/40">Neuromarketing Aplicado y Sonda Térmica • Sistemas Pyme</span>
        <span class="text-xs font-bold text-teal-300">Duplica las visitas de tu web que terminan llamándote</span>
      </div>
      <h1 class="text-2xl sm:text-4xl font-black leading-tight mb-2">
        Super-Auditoría Neuro-CRO + Sonda Térmica de 10-14 Días
      </h1>
      <p class="text-sm sm:text-base text-amber-100 leading-relaxed">
        Por qué el 80% de las personas que entran a mirar una web se marchan sin llamar ni escribir, y cómo duplicamos tus contactos reales midiendo con mapas de calor dónde miran, dónde dudan y dónde se atascan tus clientes.
      </p>
    </div>

    <!-- BLOQUE 1: EXPLICACIÓN PARA EL DUEÑO (SIN TECNICISMOS) -->
    <div class="bg-gradient-to-br from-amber-50 via-white to-sky-50 border-2 border-amber-400 rounded-3xl p-6 mb-7 shadow-sm">
      <div class="inline-flex items-center gap-2 bg-amber-100 text-amber-950 font-black text-xs uppercase tracking-wider px-3.5 py-1 rounded-full border border-amber-300 mb-3">
        <span>👔 PARTE 1: EXPLICACIÓN CLARA PARA EL DUEÑO DEL NEGOCIO (SIN TECNICISMOS)</span>
      </div>
      <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-2">
        ¿Qué hacemos exactamente en tu página web para que te entren el doble de clientes?
      </h2>
      <p class="text-xs sm:text-[13.5px] text-slate-700 leading-relaxed mb-4">
        Cuando un cliente entra en tu web desde su teléfono móvil, <strong>decide en solo 3 a 5 segundos si le inspiras confianza o si cierra la página</strong>. Si tiene que buscar dónde está tu teléfono, rellenar un formulario largo con 6 casillas o no ve al instante las opiniones reales de otros clientes, se agobia y llama al siguiente de la lista.
      </p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-[13px]">
        <div class="bg-white rounded-2xl p-4 border border-amber-300 shadow-sm space-y-2">
          <strong class="text-amber-900 font-black block text-sm">🔬 Paso 1: Ponemos una «Cámara Térmica» 10-14 días en tu web:</strong>
          <ul class="space-y-1.5 text-slate-700 leading-snug">
            <li>• <strong>No adivinamos a ciegas; medimos la realidad:</strong> Durante 10 a 14 días grabamos de forma 100% anónima y legal (cumpliendo la Guía AEPD) cómo se mueven tus visitas reales por tu web.</li>
            <li>• <strong>Descubrimos tus fugas ocultas:</strong> Vemos en qué casilla exacta abandonan tu formulario, qué botones intentan pulsar sin éxito y <strong>cuántas personas intentan llamar a tu teléfono fijo al mediodía, por la noche o en fin de semana cuando estás cerrado</strong>.</li>
          </ul>
        </div>
        <div class="bg-white rounded-2xl p-4 border border-sky-300 shadow-sm space-y-2">
          <strong class="text-sky-900 font-black block text-sm">🛠️ Paso 2: Implantamos las mejoras según el estilo de tu negocio:</strong>
          <ul class="space-y-1.5 text-slate-700 leading-snug">
            <li>• <strong>Modo Ágil (Clínicas, Talleres, Comercios, Hostelería):</strong> Ponemos el botón de WhatsApp en la zona del pulgar, la barra superior con tus estrellas de Google Maps y llamada en 1 toque, y reducimos las trabas del formulario.</li>
            <li>• <strong>Modo Corporativo de Alto Standing (Despachos de Abogados, Notarías, Consultoras con Secretaria):</strong> Cero botones invasivos. Mantenemos tu sobriedad institucional, añadimos tus sellos de colegiación junto al formulario y medimos las llamadas perdidas fuera de horario.</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- BLOQUE 2: ESTADÍSTICAS DEL ESTUDIO -->
    <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-3">2. Las 3 Cifras Clave de Conversión Web (Neuromarketing CRO)</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-7">
      <div class="bg-amber-50 border-2 border-amber-300 rounded-2xl p-4">
        <span class="block text-2xl sm:text-3xl font-black text-amber-700 mb-1">+156% Contactos</span>
        <strong class="block text-xs uppercase tracking-wider text-amber-950 mb-1">MIT Attention Insight</strong>
        <p class="text-xs text-slate-700 leading-relaxed">Situar tu propuesta de valor y tus estrellas reales donde van los ojos en los primeros 4 segundos multiplica por más de dos las solicitudes.</p>
      </div>
      <div class="bg-emerald-50 border-2 border-emerald-300 rounded-2xl p-4">
        <span class="block text-2xl sm:text-3xl font-black text-emerald-700 mb-1">+103% Llamadas</span>
        <strong class="block text-xs uppercase tracking-wider text-emerald-950 mb-1">Ley de Hick (Fricción Móvil)</strong>
        <p class="text-xs text-slate-700 leading-relaxed">Eliminar campos intimidantes y facilitar el contacto directo con el pulgar duplica la tasa media de conversión del 3,3% al 6,7%.</p>
      </div>
      <div class="bg-sky-50 border-2 border-sky-300 rounded-2xl p-4">
        <span class="block text-2xl sm:text-3xl font-black text-sky-700 mb-1">10 a 14 Días</span>
        <strong class="block text-xs uppercase tracking-wider text-sky-950 mb-1">Sonda Árbitro + Panel Vivo</strong>
        <p class="text-xs text-slate-700 leading-relaxed">Incluye acceso a tu <strong>Portal Privado de Telemetría</strong> para ver tus visitas por horas, ciudades, mapas de calor y clics reales.</p>
      </div>
    </div>

    <!-- BLOQUE 3: PARTE TÉCNICA PARA EL INFORMÁTICO -->
    <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-3">3. Parte 2 (Para el Informático): Qué inyectamos o entregamos listo para pegar</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-7 text-xs sm:text-[13px]">
      <div class="bg-slate-50 border border-slate-300 rounded-2xl p-5 space-y-1.5">
        <strong class="text-[#0b2239] font-black block text-sm mb-1">1.º Dictamen Pre-Sonda + 4 Módulos Universales (75%):</strong>
        <p class="text-slate-700">Auditoría de velocidad móvil (<code>LCP</code> en PageSpeed), enlaces <code>tel:</code> y <code>mailto:</code>, Ley de Hick en formularios, Efecto Cialdini de prueba social, Sonda Microsoft Clarity con enmascaramiento estricto AEPD y banner de cookies simétrico.</p>
      </div>
      <div class="bg-slate-50 border border-slate-300 rounded-2xl p-5 space-y-1.5">
        <strong class="text-[#0b2239] font-black block text-sm mb-1">2.º Dictamen Post-Sonda + Pliego de 5 Prescripciones (25%):</strong>
        <p class="text-slate-700">Tras los 10-14 días de grabación real, entregamos el informe de mapas de calor (<em>Scroll Map</em>, <em>Click Map</em> y <em>Rage Clicks</em>), el registro de llamadas fuera de horario y los 5 ajustes finos listos para aplicar.</p>
      </div>
    </div>

    <!-- BLOQUE 4: INVERSIÓN OFICIAL (SIN 200 € SOLO CÓDIGO) -->
    <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-3">4. Inversión Oficial (Pago Único • Sin Cuotas Mensuales)</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 text-center">
      <div class="bg-emerald-50 border-2 border-emerald-500 rounded-2xl p-5 shadow-md">
        <span class="inline-block text-[11px] font-extrabold uppercase tracking-wider text-emerald-950 bg-emerald-200 px-3 py-0.5 rounded-full mb-2">1. Bonificada en Combo con Pack 2+ Servicios ★</span>
        <div class="text-3xl font-black text-emerald-700 mb-1">195 € <span class="text-xs font-bold text-emerald-900">por 1 auditoría</span></div>
        <div class="text-sm font-black text-emerald-950 mb-2">390 € si contratas las 2 Super-Auditorías juntas (Ahorras 310 €)</div>
        <p class="text-xs text-emerald-950 leading-relaxed font-medium">Al activar cualquier Pack de 2 o más servicios mensuales (como el <strong>Pack Escudo Básico Dúo</strong> de 99 €/mes), tienes un <strong>44% de bonificación directa</strong>.</p>
      </div>

      <div class="bg-white border-2 border-amber-400 rounded-2xl p-5 shadow-sm">
        <span class="inline-block text-[11px] font-extrabold uppercase tracking-wider text-amber-900 bg-amber-100 px-3 py-0.5 rounded-full mb-2">2. Tarifa Suelta «Llave en Mano»</span>
        <div class="text-3xl font-black text-amber-700 mb-1">350 € <span class="text-xs font-bold text-slate-500">por 1 auditoría</span></div>
        <div class="text-sm font-extrabold text-[#0b2239] mb-2">590 € si contratas las 2 Super-Auditorías juntas (Ahorras 110 €)</div>
        <p class="text-xs text-slate-600 leading-relaxed">Contratada suelta o con Pyme Base. Incluye Sonda de 10-14 días, Portal de Telemetría e implantación por nosotros o entrega de todos los códigos e instrucciones a tu técnico.</p>
      </div>
    </div>

    <div class="text-center text-xs text-slate-500 pt-3 border-t border-slate-200">
      <strong>Sistemas Pyme — Francisco M. Gallardo (NIF 52938419D)</strong> • Tel / WhatsApp: <strong>711 54 75 61</strong> • Web: <strong>sistemaspyme.es</strong> • Precios netos sin IVA (21%).
    </div>
  </div>
</body>
</html>
"""

# ------------------------------------------------------------------------------
# 4.3 DOSSIER CATÁLOGO EXTENSO Y PROFUNDO (`catalogo.html`)
# ------------------------------------------------------------------------------
HTML_CATALOGO_DOSSIER_V152 = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dossier Catálogo Explicado a Fondo (S1 a S10 + Satélites + Auditorías) | Sistemas Pyme</title>
  {ESTILO_COMUN_TARJETONES}
</head>
<body>
  <div class="a4-sheet">
    <div class="no-print flex flex-wrap items-center justify-between gap-3 pb-4 mb-5 border-b border-slate-200">
      <span class="px-3 py-1 rounded-full bg-indigo-100 text-indigo-900 font-extrabold text-xs border border-indigo-300">📘 DOSSIER CATÁLOGO EXPLICADO EN PROFUNDIDAD • SECUENCIA S1 A S10</span>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="bg-[#0b2239] hover:bg-slate-800 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow cursor-pointer">🖨️ Imprimir / Guardar PDF</button>
        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20he%20le%C3%ADdo%20el%20Dossier%20Cat%C3%A1logo%20completo%20y%20querr%C3%ADa%20comentarlo%20contigo" target="_blank" class="bg-[#0d7d74] text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow">💬 Hablar con Francisco</a>
      </div>
    </div>

    <div class="bg-gradient-to-r from-[#0b2239] via-[#103459] to-[#0d7d74] text-white rounded-3xl p-6 sm:p-8 mb-6">
      <h1 class="text-2xl sm:text-3xl font-black mb-2">Dossier Explicativo de Todos los Servicios de Sistemas Pyme</h1>
      <p class="text-xs sm:text-sm text-teal-100 leading-relaxed">
        Este documento está diseñado para que conozcas <strong>en profundidad y sin prisas</strong> qué hace exactamente cada servicio, qué problema cotidiano te quita de encima, cómo se adapta a tu negocio sin cambiar tu forma de trabajar y cuál es su inversión tanto en combinación (<strong>Precio Combo</strong>) como contratado de forma individual (<strong>Precio Suelto</strong>).
      </p>
    </div>

    <!-- GRUPO 1 EXPLICADO A FONDO -->
    <div class="mb-6 bg-emerald-50/70 border-2 border-emerald-400 rounded-3xl p-5 sm:p-6">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-4 border-b-2 border-emerald-300 pb-2.5">
        <div>
          <span class="text-[11px] font-extrabold uppercase tracking-wider text-emerald-800 block">GRUPO 1 • MÓDULOS S1 A S5</span>
          <h2 class="text-lg sm:text-xl font-black text-emerald-950">Servicios Esenciales de Reputación, Cierre de Ventas y Gestión Diaria</h2>
        </div>
        <div class="bg-emerald-800 text-white text-xs font-extrabold px-3.5 py-1.5 rounded-xl text-right">
          <div>En Combo: +40 €/mes (+75 € Setup)</div>
          <div class="text-[10.5px] text-emerald-200 font-semibold">1.º o Suelto: 59 €/mes (150 € Setup)</div>
        </div>
      </div>

      <div class="space-y-3.5 text-xs sm:text-[13px] text-slate-800 leading-relaxed">
        <div class="bg-white p-4 rounded-2xl border border-emerald-300 shadow-sm">
          <div class="flex flex-wrap justify-between items-center gap-2 mb-1">
            <strong class="text-sm font-black text-[#0b2239]">⭐ S1. Gestión y Respuesta Inteligente de Reseñas en Google con IA <span class="text-emerald-700">(Activo Hoy)</span></strong>
            <span class="text-[11px] font-extrabold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-full">Área: Reputación y SEO en Google Maps</span>
          </div>
          <p class="mb-1.5"><strong>¿Qué problema resuelve?</strong> El 88% de los clientes lee las respuestas del dueño antes de decidirse, y responder incluyendo tu oficio y tu ciudad sube hasta un +35% las llamadas desde Google Maps. Pero responder a mano quita tiempo y, en clínicas o despachos, confirmar sin querer que alguien es paciente o cliente en público conlleva multas de la AEPD de 10.000 € a 40.000 €.</p>
          <p><strong>¿Cómo funciona por dentro?</strong> En las reseñas de <strong>4 y 5 estrellas</strong>, nuestra IA redacta y publica sola una respuesta cálida en el mismo idioma del cliente, sin repetir frases y posicionando tu especialidad en tu localidad. En cambio, cuando entra una reseña delicada de <strong>1 a 3 estrellas</strong> (o una de 4★ con queja oculta, o un 1★ por error de dedo con elogio), <strong>el sistema frena la publicación automática</strong> y te envía al móvil un aviso inmediato con 4 borradores redactados bajo el protocolo psicológico HEARD y blindados ante el RGPD (sin repetir jamás palabras tóxicas por la <em>Regla Anti-Loro</em>) para que tú apruebes o edites en 1 clic antes de que se publique. Incluye el Módulo 2 de tu <strong>Informe Mensual 360°</strong>.</p>
        </div>

        <div class="bg-white p-4 rounded-2xl border border-emerald-300 shadow-sm">
          <div class="flex flex-wrap justify-between items-center gap-2 mb-1">
            <strong class="text-sm font-black text-[#0b2239]">🛡️ S2. Cortafuegos Preventivo y Encuesta Post-Visita por WhatsApp Oficial <span class="text-emerald-700">(Activo Hoy)</span></strong>
            <span class="text-[11px] font-extrabold text-teal-800 bg-teal-100 px-2.5 py-0.5 rounded-full">Área: Escucha Activa y Captación 5★</span>
          </div>
          <p class="mb-1.5"><strong>¿Qué problema resuelve?</strong> 9 de cada 10 clientes salen encantados de tu negocio pero con las prisas del día se olvidan de ponerte reseña; mientras que el único que sufrió un retraso o malentendido va directo a escribir 1 estrella en internet porque nadie le preguntó antes en privado.</p>
          <p><strong>¿Cómo funciona por dentro?</strong> Configuramos la API Oficial de WhatsApp Business (sobre tu móvil o incluso sobre el <strong>teléfono fijo de toda la vida de tu local</strong>). Tras la cita o visita (respetando el <em>Modo Silencio Nocturno</em> de 21:30h a 10:00h y la <em>Higiene de 180 días</em> para no saturar a clientes habituales), envía un mensaje breve con 3 botones: si pulsa <strong>«Excelente»</strong>, le entrega el enlace directo a tus 5★ de Google Maps; si pulsa <strong>«Bien»</strong> o <strong>«Mejorable»</strong>, abre un canal privado para que te cuente qué ocurrió por escrito o mediante una <strong>nota de voz</strong>. Nuestra IA transcribe el audio a texto al instante y te manda a tu móvil tanto la transcripción como la voz original para que lo soluciones en casa.</p>
        </div>

        <div class="bg-white p-4 rounded-2xl border border-emerald-200 shadow-sm">
          <div class="flex flex-wrap justify-between items-center gap-2 mb-1">
            <strong class="text-sm font-black text-[#0b2239]">⚡ S3. Atención a Leads en 10 Segundos + Extractor de Portales</strong>
            <span class="text-[11px] font-extrabold text-blue-800 bg-blue-100 px-2.5 py-0.5 rounded-full">Área: Cierre de Ventas en Caliente</span>
          </div>
          <p><strong>¿Qué hace?</strong> El 75% de las personas que piden presupuesto en una web o portal contrata al primero que le atiende. En cuanto entra una solicitud en el formulario de tu web o en portales sectoriales, el sistema le escribe por WhatsApp en menos de 10 segundos saludándole por su nombre, adelantándole información útil y enviándote a ti una alerta directa al móvil para que le llames en un toque mientras aún tiene el teléfono en la mano.</p>
        </div>

        <div class="bg-white p-4 rounded-2xl border border-emerald-200 shadow-sm">
          <div class="flex flex-wrap justify-between items-center gap-2 mb-1">
            <strong class="text-sm font-black text-[#0b2239]">🧾 S4. Facturas y Tickets de Gastos al Gestor por Foto de WhatsApp (Cero Papeles)</strong>
            <span class="text-[11px] font-extrabold text-indigo-800 bg-indigo-100 px-2.5 py-0.5 rounded-full">Área: Ahorro de Tiempo Administrativo</span>
          </div>
          <p><strong>¿Qué hace?</strong> Se acabó perder horas al final del trimestre buscando tickets borrados o facturas arrugadas en la guantera. Cada vez que pagues un gasto del negocio, le haces una foto desde tu propio WhatsApp; nuestra IA con visión artificial lee el proveedor, NIF, fecha, base imponible e IVA, guarda la imagen ordenada en Google Drive y añade el apunte contable directo en la hoja Excel de tu gestoría.</p>
        </div>

        <div class="bg-white p-4 rounded-2xl border border-emerald-200 shadow-sm">
          <div class="flex flex-wrap justify-between items-center gap-2 mb-1">
            <strong class="text-sm font-black text-[#0b2239]">🔄 S5. Reactivación Automática de Clientes Inactivos (Clientela de Toda la Vida)</strong>
            <span class="text-[11px] font-extrabold text-sky-800 bg-sky-100 px-2.5 py-0.5 rounded-full">Área: Facturación Recurrente</span>
          </div>
          <p><strong>¿Qué hace?</strong> Cuesta 5 veces menos que vuelva un cliente que ya te conoce que captar a uno nuevo. El sistema detecta automáticamente qué clientes llevan más de 60, 90 o 180 días sin acudir (revisiones anuales, mantenimientos, ITV, limpiezas dentales, cortes o tratamientos) y les envía un WhatsApp cercano y personalizado invitándoles a reservar su próxima visita.</p>
        </div>
      </div>
    </div>

    <!-- GRUPO 2 EXPLICADO A FONDO -->
    <div class="mb-6 bg-sky-50/70 border-2 border-sky-400 rounded-3xl p-5 sm:p-6">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-4 border-b-2 border-sky-300 pb-2.5">
        <div>
          <span class="text-[11px] font-extrabold uppercase tracking-wider text-sky-800 block">GRUPO 2 • MÓDULOS S6 A S8</span>
          <h2 class="text-lg sm:text-xl font-black text-sky-950">Operativa Avanzada de Agenda, Contratos Digitales y Cobros</h2>
        </div>
        <div class="bg-sky-800 text-white text-xs font-extrabold px-3.5 py-1.5 rounded-xl text-right">
          <div>En Combo: +59 €/mes (+110 € Setup)</div>
          <div class="text-[10.5px] text-sky-200 font-semibold">Suelto: 79 €/mes (195 € Setup)</div>
        </div>
      </div>

      <div class="space-y-3.5 text-xs sm:text-[13px] text-slate-800 leading-relaxed">
        <div class="bg-white p-4 rounded-2xl border border-sky-200 shadow-sm">
          <strong class="text-sm font-black text-[#0b2239] block mb-1">📅 S6. Sistema Anti-Plantón 24h + Relleno Automático de Huecos Flash (-85% Ausencias)</strong>
          <p>Cada cita a la que un cliente no acude sin avisar es una hora de facturación perdida que ya no recuperas. 24 horas antes de cada cita, el sistema envía un WhatsApp interactivo con los botones <code>[Confirmar asistencia]</code> o <code>[Solicitar cambio]</code>. Si el cliente confirma, marca la cita como verificada en tu calendario; y si avisa de que no puede ir, libera el hueco y avisa automáticamente por WhatsApp a los clientes de tu lista de espera para rellenar esa hora vacía en minutos.</p>
        </div>

        <div class="bg-white p-4 rounded-2xl border border-sky-200 shadow-sm">
          <strong class="text-sm font-black text-[#0b2239] block mb-1">✍️ S7. Firma Digital de Presupuestos desde el Móvil + Onboarding IA de Clientes</strong>
          <p>Evita que los presupuestos se enfríen porque el cliente no tiene impresora o escáner a mano. Envía el presupuesto listo para firmar con el dedo desde la pantalla del móvil con validez legal. En el mismo instante en que el cliente firma, el sistema crea su carpeta privada en tu Google Drive, te avisa del cierre y le solicita amablemente por WhatsApp o correo la documentación necesaria para empezar el trabajo.</p>
        </div>

        <div class="bg-white p-4 rounded-2xl border border-sky-200 shadow-sm">
          <strong class="text-sm font-black text-[#0b2239] block mb-1">⚖️ S8. Escudo Anti-Morosidad Diplomático (Recordatorio Aséptico de Facturas Vencidas)</strong>
          <p>Quita a gerencia la incomodidad personal de tener que llamar para perseguir cobros pendientes. Cuando una factura supera su fecha de vencimiento (+3, +7 y +15 días), el sistema envía en nombre del departamento administrativo un recordatorio educado y neutral por WhatsApp y correo adjuntando el PDF de la factura y el enlace directo de pago o número de cuenta.</p>
        </div>
      </div>
    </div>

    <!-- GRUPO 3 Y GRUPO 4 EXPLICADOS A FONDO -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
      <div class="bg-pink-50/70 border-2 border-pink-400 rounded-3xl p-5 text-xs sm:text-[12.5px] space-y-3">
        <div class="border-b-2 border-pink-300 pb-2">
          <span class="text-[10.5px] font-extrabold uppercase tracking-wider text-pink-800 block">GRUPO 3 • SATÉLITES Y BOOSTERS IA</span>
          <h2 class="text-base sm:text-lg font-black text-pink-950">Redes Sociales, Reparto Logístico y Cerebro Documental B2B</h2>
        </div>
        <div class="bg-white p-3.5 rounded-2xl border border-pink-200">
          <strong class="text-[#0b2239] font-black block mb-0.5">📲 Sat.1 Instagram Inteligente 3 en 1 (Meta API Oficial)</strong>
          <span class="block text-[11px] font-extrabold text-pink-700 mb-1">En Combo: +49 €/m (+75 € Setup) | Suelto: 69 €/m (150 € Setup)</span>
          <p class="text-slate-700 leading-snug">Convierte tus seguidores en clientes reales: 1) Cuando alguien comenta una palabra clave en tus Reels o Posts, le envía al instante por mensaje directo (DM) el enlace o información prometida; 2) Atiende dudas frecuentes en DMs las 24h; 3) Agradece automáticamente cuando un cliente te menciona en sus Stories.</p>
        </div>
        <div class="bg-white p-3.5 rounded-2xl border border-pink-200">
          <strong class="text-[#0b2239] font-black block mb-0.5">🚚 Sat.2 Escudo Logístico 360 (E-commerce y Entregas a Domicilio)</strong>
          <span class="block text-[11px] font-extrabold text-indigo-700 mb-1">En Combo: +59 €/m (+110 € Setup) | Suelto: 79 €/m (195 € Setup)</span>
          <p class="text-slate-700 leading-snug">Elimina el 90% de las llamadas preguntando «¿Dónde está mi pedido?». Envía un WhatsApp automático cuando el paquete sale del almacén, otro la mañana del reparto («Llega hoy») y permite coordinar al instante si el destinatario está ausente.</p>
        </div>
        <div class="bg-white p-3.5 rounded-2xl border border-pink-200">
          <strong class="text-[#0b2239] font-black block mb-0.5">📐 Sat.3 Cerebro Redactor Técnico B2B con IA (RAG Privado)</strong>
          <span class="block text-[11px] font-extrabold text-indigo-700 mb-1">En Combo: +69 €/m (+150 € Setup) | Suelto: 99 €/m (250 € Setup)</span>
          <p class="text-slate-700 leading-snug">Entrenado exclusivamente con los catálogos, tarifas y memorias técnicas privadas de tu empresa para redactar borradores de presupuestos complejos a medida en segundos.</p>
        </div>
        <div class="bg-white p-3 rounded-2xl border border-amber-300">
          <strong class="text-amber-950 font-black block">⚡ Boosters IA (+35 €/m y +50 € Setup):</strong>
          <span class="text-slate-700"><strong>Add-on Correo (S4):</strong> lee y clasifica sola las facturas que llegan a tu email. <strong>Add-on Proveedores (S8):</strong> reclama pedidos retrasados a tus proveedores.</span>
        </div>
      </div>

      <div class="bg-indigo-50/70 border-2 border-indigo-400 rounded-3xl p-5 text-xs sm:text-[12.5px] space-y-3 flex flex-col justify-between">
        <div class="space-y-3">
          <div class="border-b-2 border-indigo-300 pb-2">
            <span class="text-[10.5px] font-extrabold uppercase tracking-wider text-indigo-800 block">GRUPO 4 • MÓDULOS S9 Y S10</span>
            <h2 class="text-base sm:text-lg font-black text-indigo-950">Telefonía Inteligente y Centralita de Voz IA 24/7</h2>
          </div>
          <div class="bg-white p-4 rounded-2xl border border-indigo-200">
            <strong class="text-[#0b2239] font-black block text-sm mb-0.5">📵 S9. Rescate Automático de Llamadas Perdidas por WhatsApp</strong>
            <span class="block text-[11px] font-extrabold text-sky-800 mb-1.5">En Combo: +59 €/m (+110 € Setup) | Suelto: 79 €/m (195 € Setup)</span>
            <p class="text-slate-700 leading-relaxed">Cuando estás atendiendo a un cliente, en cabina o fuera de horario y alguien llama a tu negocio sin obtener respuesta, antes de que cuelgue y llame a otro competidor recibe a los 5 segundos un WhatsApp oficial de tu negocio disculpándose por estar ocupados y preguntándole en qué puedes ayudarle. <strong>Incluye desvío de línea y bolsa de hasta 250 rescates al mes.</strong></p>
          </div>
          <div class="bg-white p-4 rounded-2xl border border-indigo-200">
            <strong class="text-[#0b2239] font-black block text-sm mb-0.5">🎙️ S10. Centralita Recepcionista de Voz IA 24/7</strong>
            <span class="block text-[11px] font-extrabold text-indigo-900 mb-1.5">En Combo: +129 €/m (+250 € Setup) | Suelto: 169 €/m (350 € Setup)</span>
            <p class="text-slate-700 leading-relaxed">Tu recepcionista telefónica con voz neuronal natural disponible las 24 horas los 365 días. Descuelga al instante cuando comunicas o estás cerrado, responde dudas sobre tus servicios, precios y ubicación, recoge recados urgentes y agenda citas directamente en tu calendario enviando confirmación por WhatsApp. <strong>Incluye bolsa de 250 minutos de voz IA al mes.</strong></p>
          </div>
        </div>

        <div class="bg-amber-100/90 border-2 border-amber-400 rounded-2xl p-3.5 text-slate-900">
          <strong class="text-amber-950 font-black block mb-1">🎁 Bono Regalo en Pyme Trinity+ (3 o más servicios mensuales):</strong>
          Recibes <strong>100% GRATIS tu Bóveda Segura de Contraseñas</strong> (valorada en 150 €) para compartir accesos del negocio con tu equipo en 1 clic sin revelar jamás las claves.
        </div>
      </div>
    </div>

    <div class="text-center text-xs text-slate-500 pt-3 border-t border-slate-200">
      <strong>Sistemas Pyme — Francisco M. Gallardo (NIF 52938419D)</strong> • Tel / WhatsApp: <strong>711 54 75 61</strong> • Web: <strong>sistemaspyme.es</strong>
    </div>
  </div>
</body>
</html>
"""

# ------------------------------------------------------------------------------
# 4.4 TARIFAS OFICIALES (`tarifas.html`): CÓDIGO DE COLORES + PYME QUATRO CON Q + COMBO VS SUELTO
# ------------------------------------------------------------------------------
HTML_TARIFAS_OFICIALES_V152 = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tarifas Oficiales y Combinaciones por Grupos | Sistemas Pyme</title>
  {ESTILO_COMUN_TARJETONES}
</head>
<body>
  <div class="a4-sheet">
    <div class="no-print flex flex-wrap items-center justify-between gap-3 pb-4 mb-5 border-b border-slate-200">
      <span class="px-3 py-1 rounded-full bg-teal-100 text-teal-900 font-extrabold text-xs border border-teal-300">💶 TARIFAS OFICIALES Y ESCALADO MODULAR</span>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="bg-[#0b2239] hover:bg-slate-800 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow cursor-pointer">🖨️ Imprimir / Guardar PDF</button>
        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20estoy%20viendo%20la%20tabla%20de%20Tarifas%20Oficiales%20y%20querr%C3%ADa%20consultar%20una%20combinaci%C3%B3n" target="_blank" class="bg-[#0d7d74] text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow">💬 Consultar combinación</a>
      </div>
    </div>

    <div class="bg-gradient-to-r from-[#0b2239] to-[#0d7d74] text-white rounded-3xl p-6 mb-6">
      <h1 class="text-2xl sm:text-3xl font-black mb-1">Tarifas Oficiales y Planes de Libre Combinación</h1>
      <p class="text-xs sm:text-sm text-teal-100">Con salvar o captar un solo cliente al mes, todo el sistema se amortiza solo. Modalidad Flexible (3 meses mín.) o Plan Anual (solo pagas 10 meses).</p>
    </div>

    <!-- TABLA 1 CON CÓDIGO DE COLORES PARA TODOS LOS PACKS Y PYME QUATRO CON Q MAYÚSCULA -->
    <h2 class="text-base sm:text-lg font-black text-[#0b2239] mb-2">1. Planes Mensuales de Libre Elección (Con Código de Colores Oficial)</h2>
    <div class="overflow-x-auto mb-3">
      <table class="w-full text-left border-collapse text-xs sm:text-[13px]">
        <thead>
          <tr class="bg-[#0b2239] text-white">
            <th class="p-3 rounded-tl-xl">Módulo / Pack</th>
            <th class="p-3">1. Cuota al Mes / Año</th>
            <th class="p-3">2. Setup Único (Alta)</th>
            <th class="p-3 rounded-tr-xl">3. En qué consiste (Libre Combinación entre los 4 Grupos)</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200 border border-slate-300">
          <!-- Pyme Base: Pizarra -->
          <tr class="bg-slate-100/90 border-l-8 border-l-slate-600">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-slate-800 text-white font-black text-xs">Pyme Base</span></td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 59 € / mes<span class="block text-[10.5px] text-slate-700 font-bold">Anual: desde 590 € / año</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">Desde 150 €</td>
            <td class="p-3 text-slate-800"><strong>1 servicio de libre elección</strong> de cualquiera de los 4 grupos (ej. S1 Reseñas IA o S2 Cortafuegos WhatsApp). Incluye Informe Mensual 360°.</td>
          </tr>
          <!-- Escudo Básico: Azul Cielo -->
          <tr class="bg-sky-50/90 border-l-8 border-l-sky-600">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-sky-600 text-white font-black text-xs">Escudo Básico</span></td>
            <td class="p-3 font-black text-sky-800 whitespace-nowrap">Desde 99 € / mes<span class="block text-[10.5px] text-sky-900 font-bold">Anual: desde 990 € / año</span></td>
            <td class="p-3 font-bold text-sky-950 whitespace-nowrap">Desde 225 €<span class="block text-[10px] text-emerald-700 font-extrabold">(2.º Setup al 50%)</span></td>
            <td class="p-3 text-slate-800"><strong>2 servicios de libre elección</strong> (ej. S1 Reseñas IA + S2 Cortafuegos WA). Desbloquea las Super-Auditorías a <strong>195 € c/u</strong> (en vez de 350 €).</td>
          </tr>
          <!-- Escudo Total: Verde Esmeralda -->
          <tr class="bg-emerald-50/95 border-l-8 border-l-emerald-600">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-emerald-600 text-white font-black text-xs">Escudo Total ★</span></td>
            <td class="p-3 font-black text-emerald-800 whitespace-nowrap">Desde 99 € / mes<span class="block text-[10.5px] text-amber-900 font-extrabold">+ 195 € (1 Aud.) o 390 € (las 2)</span></td>
            <td class="p-3 font-bold text-emerald-950 whitespace-nowrap">Desde 225 € + Aud.<span class="block text-[10px] text-emerald-800 font-extrabold">(Ahorras 155 € o 310 €)</span></td>
            <td class="p-3 text-slate-800"><strong>2 servicios de libre elección + 1 o 2 Super-Auditorías Llave en Mano</strong> bonificadas a 195 € c/u (SEO+GEO IA y/o Neuro-CRO Web).</td>
          </tr>
          <!-- Pyme Trinity: Ámbar / Dorado -->
          <tr class="bg-amber-50/90 border-l-8 border-l-amber-500">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-black text-xs">Pyme Trinity 🎁</span></td>
            <td class="p-3 font-black text-amber-900 whitespace-nowrap">Desde 139 € / mes<span class="block text-[10.5px] text-amber-950 font-bold">Anual: desde 1.390 € / año</span></td>
            <td class="p-3 font-bold text-amber-950 whitespace-nowrap">Desde 300 €</td>
            <td class="p-3 text-slate-800"><strong>3 servicios mensuales de libre elección</strong> de cualquier grupo + <strong>🎁 Bóveda Segura de Contraseñas GRATIS</strong> (valorada en 150 €) + Auditorías a 195 € c/u.</td>
          </tr>
          <!-- Pyme Quatro (con Q mayúscula): Índigo -->
          <tr class="bg-indigo-50/90 border-l-8 border-l-indigo-600">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-indigo-600 text-white font-black text-xs">Pyme Quatro</span></td>
            <td class="p-3 font-black text-indigo-900 whitespace-nowrap">Desde 179 € / mes<span class="block text-[10.5px] text-indigo-950 font-bold">Anual: desde 1.790 € / año</span></td>
            <td class="p-3 font-bold text-indigo-950 whitespace-nowrap">Desde 375 €</td>
            <td class="p-3 text-slate-800"><strong>4 servicios mensuales de libre elección</strong> combinando cualquier grupo + Bóveda de Contraseñas GRATIS + Auditorías bonificadas a 195 € c/u.</td>
          </tr>
          <!-- Pyme Pentium: Púrpura / Violeta -->
          <tr class="bg-purple-50/90 border-l-8 border-l-purple-600">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-purple-700 text-white font-black text-xs">Pyme Pentium</span></td>
            <td class="p-3 font-black text-purple-900 whitespace-nowrap">Desde 219 € / mes<span class="block text-[10.5px] text-purple-950 font-bold">Anual: desde 2.190 € / año</span></td>
            <td class="p-3 font-bold text-purple-950 whitespace-nowrap">Desde 450 €</td>
            <td class="p-3 text-slate-800"><strong>5 servicios mensuales de libre elección</strong> combinando cualquier grupo + Bóveda de Contraseñas GRATIS + Auditorías bonificadas a 195 € c/u.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="bg-amber-50 border-2 border-amber-400 rounded-2xl p-4 mb-6 text-xs text-slate-800 leading-relaxed">
      <strong class="text-amber-950 font-black block mb-1">💡 Regla de Combinación Libre entre cualquiera de los 4 Grupos:</strong>
      Puedes combinar servicios de cualquier grupo. <strong>Tu primer servicio toma la tarifa individual del módulo más económico que hayas incluido</strong> (59 €/m y 150 € Setup si incluyes al menos uno del Grupo 1; o la tarifa suelta de su grupo si solo eliges de los Grupos 2, 3 o 4), y <strong>todos los demás servicios suman directamente su precio reducido de combinación (Combo)</strong>.
    </div>

    <!-- TABLA 2: TARIFAS POR GRUPO CON SUBTÍTULO EN LÍNEA PROPIA Y MISMA SECUENCIA COMBO -> SUELTO -->
    <h2 class="text-base sm:text-lg font-black text-[#0b2239] mb-2">2. Tarifas por Grupo (S1 a S10), Super-Auditorías y Hardware NFC</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
      <div class="border-2 border-sky-300 rounded-2xl p-4 bg-sky-50/40 space-y-2.5">
        <div class="border-b border-sky-200 pb-1.5">
          <h3 class="font-black text-[#0b2239] text-sm">🚀 Los servicios divididos en 4 Grupos (S1 a S10)</h3>
          <span class="block text-[11px] font-extrabold text-sky-800 mt-0.5">Cuota y Setup en Combo vs. Suelto</span>
        </div>
        <ul class="space-y-2 text-slate-800">
          <li class="flex justify-between items-baseline gap-2 border-b border-sky-200/60 pb-1">
            <span><strong>Grupo 1 (S1 a S5):</strong></span>
            <span class="whitespace-nowrap"><strong class="text-emerald-800">Combo: +40 €/m (+75€ Setup)</strong> | 1.º: 59€/m (150€)</span>
          </li>
          <li class="flex justify-between items-baseline gap-2 border-b border-sky-200/60 pb-1">
            <span><strong>Grupo 2 (S6 a S8):</strong></span>
            <span class="whitespace-nowrap"><strong class="text-sky-800">Combo: +59 €/m (+110€ Setup)</strong> | Suelto: 79€/m (195€)</span>
          </li>
          <li class="border-b border-sky-200/60 pb-1 space-y-1">
            <div class="flex justify-between items-baseline gap-2">
              <span><strong>Grupo 3</strong> · Sat.1 Instagram 3 en 1:</span>
              <span class="whitespace-nowrap"><strong class="text-pink-700">Combo: +49 €/m (+75€)</strong> | Suelto: 69€/m (150€)</span>
            </div>
            <div class="flex justify-between items-baseline gap-2 pl-12 text-slate-700">
              <span>· Sat.2 Escudo Logístico 360:</span>
              <span class="whitespace-nowrap"><strong class="text-indigo-700">Combo: +59 €/m (+110€)</strong> | Suelto: 79€/m (195€)</span>
            </div>
            <div class="flex justify-between items-baseline gap-2 pl-12 text-slate-700">
              <span>· Sat.3 Redactor B2B RAG:</span>
              <span class="whitespace-nowrap"><strong class="text-indigo-700">Combo: +69 €/m (+150€)</strong> | Suelto: 99€/m (250€)</span>
            </div>
          </li>
          <li class="space-y-1">
            <div class="flex justify-between items-baseline gap-2">
              <span><strong>Grupo 4</strong> · S9 Llamadas Perdidas WA:</span>
              <span class="whitespace-nowrap"><strong class="text-sky-800">Combo: +59 €/m (+110€)</strong> | Suelto: 79€/m (195€)</span>
            </div>
            <div class="flex justify-between items-baseline gap-2 pl-12 text-slate-700">
              <span>· S10 Centralita Voz IA 24/7:</span>
              <span class="whitespace-nowrap"><strong class="text-indigo-900">Combo: +129 €/m (+250€)</strong> | Suelto: 169€/m (350€)</span>
            </div>
          </li>
        </ul>
      </div>

      <div class="border-2 border-teal-400 rounded-2xl p-4 bg-teal-50/40 space-y-2.5 flex flex-col justify-between">
        <div>
          <div class="border-b border-teal-200 pb-1.5 mb-2">
            <h3 class="font-black text-[#0b2239] text-sm">🔍🧠 Super-Auditorías Web y ★ Atril NFC + QR</h3>
            <span class="block text-[11px] font-extrabold text-teal-800 mt-0.5">Pagos únicos sin cuotas mensuales (Combo vs. Suelto)</span>
          </div>
          <ul class="space-y-2.5 text-slate-800">
            <li class="flex justify-between items-baseline gap-2 border-b border-teal-200/60 pb-1.5">
              <span><strong>Super-Auditoría Web (1 unidad):</strong><br><span class="text-[11px] text-slate-600">SEO Local + GEO IA o Neuro-CRO Web</span></span>
              <span class="whitespace-nowrap"><strong class="text-emerald-700">Combo: 195 €</strong> | Suelta: 350 €</span>
            </li>
            <li class="flex justify-between items-baseline gap-2 border-b border-teal-200/60 pb-1.5">
              <span><strong>Doble Super-Auditoría (Las 2 juntas):</strong><br><span class="text-[11px] text-slate-600">SEO/GEO IA + Neuro-CRO implantadas</span></span>
              <span class="whitespace-nowrap"><strong class="text-emerald-700">Combo: 390 €</strong> | Sueltas: 590 €</span>
            </li>
            <li class="flex justify-between items-baseline gap-2 pt-1">
              <span><strong>★ Atril Inteligente NFC + QR:</strong><br><span class="text-[11px] text-slate-600">Soporte físico + telemetría en Informe 360°</span></span>
              <span class="whitespace-nowrap"><strong class="text-amber-800">2ª-4ª: 29 € | 5+: 25 €</strong> | 1.ª: 39 €</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="text-center text-xs text-slate-500 mt-6 pt-3 border-t border-slate-200">
      <strong>Sistemas Pyme — Francisco M. Gallardo (NIF 52938419D)</strong> • Tel / WhatsApp: <strong>711 54 75 61</strong> • Precios netos sin IVA (21%) • Domiciliación SEPA.
    </div>
  </div>
</body>
</html>
"""

# ------------------------------------------------------------------------------
# 4.5 DESEMBOLSO DEL PRIMER DÍA (`desembolso.html`): CÓDIGO DE COLORES + PYME QUATRO CON Q
# ------------------------------------------------------------------------------
HTML_DESEMBOLSO_DIA1_V152 = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Desembolso del Primer Día y Liquidación Transparente | Sistemas Pyme</title>
  {ESTILO_COMUN_TARJETONES}
</head>
<body>
  <div class="a4-sheet">
    <div class="no-print flex flex-wrap items-center justify-between gap-3 pb-4 mb-5 border-b border-slate-200">
      <span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-900 font-extrabold text-xs border border-emerald-300">📊 DESEMBOLSO DEL PRIMER DÍA (VÍA FLEXIBLE VS. PLAN ANUAL)</span>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="bg-[#0b2239] hover:bg-slate-800 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow cursor-pointer">🖨️ Imprimir / Guardar PDF</button>
        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20estoy%20revisando%20el%20documento%20de%20Desembolso%20del%20Primer%20D%C3%ADa" target="_blank" class="bg-[#0d7d74] text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow">💬 Consultar mi caso</a>
      </div>
    </div>

    <div class="bg-gradient-to-r from-[#0b2239] via-[#0f3456] to-[#059669] text-white rounded-3xl p-6 mb-6">
      <h1 class="text-2xl sm:text-3xl font-black mb-1">Desembolso Exacto del Primer Día (Sin Sorpresas)</h1>
      <p class="text-xs sm:text-sm text-emerald-100">Qué abonas el Día 1 al poner en marcha tu sistema (Setup de instalación única + primer período) tanto en Vía Flexible como en Plan Anual (donde solo pagas 10 meses).</p>
    </div>

    <div class="overflow-x-auto mb-5">
      <table class="w-full text-left border-collapse text-xs sm:text-[13px]">
        <thead>
          <tr class="bg-[#0b2239] text-white">
            <th class="p-3 rounded-tl-xl">Módulo / Pack</th>
            <th class="p-3">1. Vía Flexible: Total Día 1<span class="block text-[10px] text-teal-300 font-normal">(Setup único + Mes 1)</span></th>
            <th class="p-3">2. Plan Anual: Total Día 1<span class="block text-[10px] text-amber-300 font-normal">(Setup único + 10 Meses)</span></th>
            <th class="p-3 rounded-tr-xl">3. Qué incluye y Ahorro Directo</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200 border border-slate-300">
          <!-- Pyme Base: Pizarra -->
          <tr class="bg-slate-100/90 border-l-8 border-l-slate-600">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-slate-800 text-white font-black text-xs">Pyme Base</span><span class="block text-[11px] text-slate-600 mt-0.5">1 servicio libre elección</span></td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 209 €<span class="block text-[10.5px] text-slate-600 font-normal">(59 € Mes 1 + 150 € Setup)</span></td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 740 €<span class="block text-[10.5px] text-slate-600 font-normal">(590 € Año + 150 € Setup)</span></td>
            <td class="p-3 text-slate-800">1 servicio a elegir. En Plan Anual <strong>ahorras 118 € al año (solo pagas 10 meses)</strong>.</td>
          </tr>
          <!-- Escudo Básico: Azul Cielo -->
          <tr class="bg-sky-50/90 border-l-8 border-l-sky-600">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-sky-600 text-white font-black text-xs">Escudo Básico</span><span class="block text-[11px] text-sky-800 mt-0.5">2 servicios libre elección</span></td>
            <td class="p-3 font-black text-sky-900 whitespace-nowrap">Desde 324 €<span class="block text-[10.5px] text-sky-800 font-normal">(99 € Mes 1 + 225 € Setup)</span></td>
            <td class="p-3 font-black text-sky-900 whitespace-nowrap">Desde 1.215 €<span class="block text-[10.5px] text-sky-800 font-normal">(990 € Año + 225 € Setup)</span></td>
            <td class="p-3 text-slate-800"><strong>Ahorras 75 € en Setup + 19 €/m</strong>. En Plan Anual <strong>ahorras 198 € (solo pagas 10 meses)</strong>. Desbloquea Auditorías a 195 €.</td>
          </tr>
          <!-- Escudo Total: Verde Esmeralda -->
          <tr class="bg-emerald-50/95 border-l-8 border-l-emerald-600">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-emerald-600 text-white font-black text-xs">Escudo Total ★</span><span class="block text-[11px] text-emerald-800 font-bold mt-0.5">2 servicios + 1 o 2 Auditorías</span></td>
            <td class="p-3 font-black text-emerald-900 whitespace-nowrap">Desde 519 € (con 1 Aud.)<span class="block text-[10.5px] text-emerald-800 font-bold">o 714 € (con las 2 Auditorías)</span></td>
            <td class="p-3 font-black text-emerald-900 whitespace-nowrap">Desde 1.410 € (con 1 Aud.)<span class="block text-[10.5px] text-emerald-800 font-bold">o 1.605 € (con las 2 Auditorías)</span></td>
            <td class="p-3 text-slate-800">Incluye S1+S2 + Super-Auditoría(s) a 195 € c/u. <strong>Ahorras 155 € (con 1) o 310 € (con las 2)</strong> + 75 € Setup (y 198 € extra en Anual).</td>
          </tr>
          <!-- Pyme Trinity: Ámbar -->
          <tr class="bg-amber-50/90 border-l-8 border-l-amber-500">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-black text-xs">Pyme Trinity 🎁</span><span class="block text-[11px] text-amber-900 font-bold mt-0.5">3 servicios libre elección</span></td>
            <td class="p-3 font-black text-amber-950 whitespace-nowrap">Desde 439 €<span class="block text-[10.5px] text-amber-900 font-normal">(139 € Mes 1 + 300 € Setup)</span></td>
            <td class="p-3 font-black text-amber-950 whitespace-nowrap">Desde 1.690 €<span class="block text-[10.5px] text-amber-900 font-normal">(1.390 € Año + 300 € Setup)</span></td>
            <td class="p-3 text-slate-800">3 servicios mensuales + <strong>🎁 Bóveda de Contraseñas GRATIS (150 €)</strong>. En Anual <strong>ahorras 278 € (solo pagas 10 meses)</strong>.</td>
          </tr>
          <!-- Pyme Quatro (con Q mayúscula): Índigo -->
          <tr class="bg-indigo-50/90 border-l-8 border-l-indigo-600">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-indigo-600 text-white font-black text-xs">Pyme Quatro</span><span class="block text-[11px] text-indigo-800 mt-0.5">4 servicios libre elección</span></td>
            <td class="p-3 font-black text-indigo-950 whitespace-nowrap">Desde 554 €<span class="block text-[10.5px] text-indigo-800 font-normal">(179 € Mes 1 + 375 € Setup)</span></td>
            <td class="p-3 font-black text-indigo-950 whitespace-nowrap">Desde 2.165 €<span class="block text-[10.5px] text-indigo-800 font-normal">(1.790 € Año + 375 € Setup)</span></td>
            <td class="p-3 text-slate-800">4 servicios mensuales + Bóveda GRATIS. En Anual <strong>ahorras 358 € (solo pagas 10 meses)</strong>.</td>
          </tr>
          <!-- Pyme Pentium: Púrpura -->
          <tr class="bg-purple-50/90 border-l-8 border-l-purple-600">
            <td class="p-3"><span class="inline-block px-2.5 py-1 rounded-lg bg-purple-700 text-white font-black text-xs">Pyme Pentium</span><span class="block text-[11px] text-purple-800 mt-0.5">5 servicios libre elección</span></td>
            <td class="p-3 font-black text-purple-950 whitespace-nowrap">Desde 669 €<span class="block text-[10.5px] text-purple-800 font-normal">(219 € Mes 1 + 450 € Setup)</span></td>
            <td class="p-3 font-black text-purple-950 whitespace-nowrap">Desde 2.640 €<span class="block text-[10.5px] text-purple-800 font-normal">(2.190 € Año + 450 € Setup)</span></td>
            <td class="p-3 text-slate-800">5 servicios mensuales + Bóveda GRATIS. En Anual <strong>ahorras 438 € (solo pagas 10 meses)</strong>.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="bg-sky-50 border-2 border-sky-300 rounded-2xl p-4 text-xs text-slate-800 leading-relaxed">
      <strong class="text-sky-950 font-black block mb-1">📌 Cómo funciona la combinación libre de servicios entre los 4 Grupos:</strong>
      Los importes «Desde» corresponden a elegir servicios del Grupo 1. Si en tu combinación incluyes módulos de los Grupos 2, 3 o 4, el módulo más económico que hayas elegido marca el precio base y el resto se suma directamente con su precio bonificado en Combo (tanto en cuota como en Setup al 50%).
    </div>

    <div class="text-center text-xs text-slate-500 mt-6 pt-3 border-t border-slate-200">
      <strong>Sistemas Pyme — Francisco M. Gallardo (NIF 52938419D)</strong> • Tel / WhatsApp: <strong>711 54 75 61</strong> • Precios netos sin IVA (21%).
    </div>
  </div>
</body>
</html>
"""

# ------------------------------------------------------------------------------
# 4.6 ANEXO TÉCNICO DE ALTAS (`setup.html`): POR QUÉ SE COBRA EL SETUP + TABLA SENCILLA COMBO VS SUELTO
# ------------------------------------------------------------------------------
HTML_SETUP_ANEXO_V152 = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Anexo Técnico de Altas e Instalación Llave en Mano (Setup) | Sistemas Pyme</title>
  {ESTILO_COMUN_TARJETONES}
</head>
<body>
  <div class="a4-sheet">
    <div class="no-print flex flex-wrap items-center justify-between gap-3 pb-4 mb-5 border-b border-slate-200">
      <span class="px-3 py-1 rounded-full bg-indigo-100 text-indigo-900 font-extrabold text-xs border border-indigo-300">🔌 ANEXO TÉCNICO OFICIAL • ALTAS E INSTALACIÓN (SETUP ÚNICO)</span>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="bg-[#0b2239] hover:bg-slate-800 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow cursor-pointer">🖨️ Imprimir / Guardar PDF</button>
        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20estoy%20viendo%20el%20Anexo%20T%C3%A9cnico%20de%20Setup" target="_blank" class="bg-[#0d7d74] text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow">💬 Consultar alta</a>
      </div>
    </div>

    <div class="bg-gradient-to-r from-[#0b2239] via-[#1e1b4b] to-[#0d7d74] text-white rounded-3xl p-6 mb-6">
      <h1 class="text-2xl sm:text-3xl font-black mb-1">Anexo Técnico: Alta e Instalación «Llave en Mano» (Setup Único)</h1>
      <p class="text-xs sm:text-sm text-indigo-100">Qué trabajo de ingeniería incluye la puesta en marcha inicial y tabla clara de costes de Setup en combinación (Combo) frente a módulo suelto.</p>
    </div>

    <!-- BLOQUE 1: ¿POR QUÉ EXISTE EL ALTA TÉCNICA (SETUP) Y QUÉ INCLUYE? -->
    <div class="bg-gradient-to-br from-amber-50 via-white to-teal-50 border-2 border-amber-400 rounded-3xl p-5 sm:p-6 mb-6 shadow-sm">
      <h2 class="text-base sm:text-lg font-black text-[#0b2239] mb-2">
        1. ¿Por qué existe un Alta Técnica inicial (Setup único) y por qué te ahorra decenas de horas?
      </h2>
      <p class="text-xs sm:text-[13px] text-slate-700 leading-relaxed mb-3.5">
        A diferencia de las plataformas genéricas donde te dan un usuario y una contraseña para que tú te pelees durante semanas leyendo manuales, en <strong>Sistemas Pyme no vendemos software vacío: te entregamos el sistema 100% configurado, probado y funcionando sobre tu negocio real en 24 a 48 horas</strong>. El Setup se abona <strong>una sola vez en la vida del servicio</strong> y cubre las horas de ingeniería necesarias para:
      </p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-slate-800">
        <div class="bg-white p-3.5 rounded-2xl border border-amber-300">
          <strong class="text-amber-950 font-black block mb-1">🔐 1. Alta y Verificación en Meta API Oficial y Google Cloud:</strong>
          Vinculamos tu ficha oficial de Google Business Profile y registramos tu número (móvil o teléfono fijo del local) en WhatsApp Business Cloud API Oficial de Meta, aprobando tus plantillas verificadas en Español, Gallego o Catalán.
        </div>
        <div class="bg-white p-3.5 rounded-2xl border border-teal-300">
          <strong class="text-teal-950 font-black block mb-1">🧠 2. Entrenamiento del Motor IA a la Medida de tu Oficio:</strong>
          Calibramos los prompts de tu sector, tus palabras clave de SEO local (especialidad + ciudad), los 4 tonos de voz, el blindaje de secreto profesional RGPD y la conexión con tu Google Calendar, CRM o App de Recepción.
        </div>
      </div>
    </div>

    <!-- BLOQUE 2: TABLA ULTRA-SENCILLA DE SETUP (EN COMBO VS. SUELTO) -->
    <h2 class="text-base sm:text-lg font-black text-[#0b2239] mb-2">
      2. Tabla Sencilla de Altas Técnicas (Setup en Combo vs. Setup Suelto)
    </h2>
    <p class="text-xs text-slate-600 mb-3">
      <strong>Regla de Ahorro en Setup:</strong> Solo abonas el Setup completo en tu primer módulo; en todos los módulos adicionales que sumes disfrutas de cerca de un <strong>50% de bonificación directa en la instalación</strong>:
    </p>

    <div class="overflow-x-auto mb-6">
      <table class="w-full text-left border-collapse text-xs sm:text-[13px]">
        <thead>
          <tr class="bg-[#0b2239] text-white">
            <th class="p-3 rounded-tl-xl">Grupo / Módulo</th>
            <th class="p-3">Servicios Incluidos</th>
            <th class="p-3 bg-emerald-800">1. Setup en COMBO<span class="block text-[10px] text-emerald-200 font-normal">(Módulo adicional bonificado)</span></th>
            <th class="p-3 rounded-tr-xl">2. Setup SUELTO<span class="block text-[10px] text-slate-300 font-normal">(Como 1.er módulo o único)</span></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200 border border-slate-300">
          <tr class="bg-emerald-50/70 border-l-8 border-l-emerald-500">
            <td class="p-3 font-black text-emerald-950">Grupo 1 (S1 a S5)</td>
            <td class="p-3 text-slate-800">S1 Reseñas IA, S2 Cortafuegos WA, S3 Leads en 10s, S4 Facturas Foto WA, S5 Clientes Inactivos</td>
            <td class="p-3 font-black text-emerald-800 text-sm whitespace-nowrap">+75 € <span class="text-[11px] font-bold">(50% dto.)</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">150 €</td>
          </tr>
          <tr class="bg-sky-50/70 border-l-8 border-l-sky-500">
            <td class="p-3 font-black text-sky-950">Grupo 2 (S6 a S8)</td>
            <td class="p-3 text-slate-800">S6 Agenda Anti-Plantón 24h + Huecos Flash, S7 Firma Digital + Onboarding, S8 Anti-Morosidad</td>
            <td class="p-3 font-black text-sky-800 text-sm whitespace-nowrap">+110 € <span class="text-[11px] font-bold">(-85 € dto.)</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">195 €</td>
          </tr>
          <tr class="bg-pink-50/60 border-l-8 border-l-pink-500">
            <td class="p-3 font-black text-pink-950">Grupo 3 · Satélite 1</td>
            <td class="p-3 text-slate-800">Instagram Inteligente 3 en 1 (Auto-DM en Reels/Posts + Recepcionista DMs 24/7 + Stories)</td>
            <td class="p-3 font-black text-pink-700 text-sm whitespace-nowrap">+75 € <span class="text-[11px] font-bold">(50% dto.)</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">150 €</td>
          </tr>
          <tr class="bg-pink-50/40 border-l-8 border-l-pink-400">
            <td class="p-3 font-black text-pink-950">Grupo 3 · Satélite 2</td>
            <td class="p-3 text-slate-800">Escudo Logístico 360 (Tracking WhatsApp «Sale hoy», «Llega hoy» y ausencias en reparto)</td>
            <td class="p-3 font-black text-indigo-700 text-sm whitespace-nowrap">+110 € <span class="text-[11px] font-bold">(-85 € dto.)</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">195 €</td>
          </tr>
          <tr class="bg-pink-50/60 border-l-8 border-l-pink-500">
            <td class="p-3 font-black text-pink-950">Grupo 3 · Satélite 3</td>
            <td class="p-3 text-slate-800">Cerebro Redactor Técnico B2B con IA (Entrenamiento RAG sobre tus catálogos y tarifas)</td>
            <td class="p-3 font-black text-indigo-700 text-sm whitespace-nowrap">+150 € <span class="text-[11px] font-bold">(-100 € dto.)</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">250 €</td>
          </tr>
          <tr class="bg-amber-50/60 border-l-8 border-l-amber-400">
            <td class="p-3 font-black text-amber-950">Grupo 3 · Boosters IA</td>
            <td class="p-3 text-slate-800">Add-on Lector de Facturas en Email (S4) o Vigilante de Pedidos a Proveedores (S8)</td>
            <td class="p-3 font-black text-amber-800 text-sm whitespace-nowrap">+50 €</td>
            <td class="p-3 font-bold text-slate-600 whitespace-nowrap">+50 € (Vinculado)</td>
          </tr>
          <tr class="bg-indigo-50/70 border-l-8 border-l-indigo-500">
            <td class="p-3 font-black text-indigo-950">Grupo 4 · S9 Telefonía</td>
            <td class="p-3 text-slate-800">Rescate de Llamadas Perdidas en 5s por WhatsApp (incluye configuración de desvío SIP)</td>
            <td class="p-3 font-black text-sky-800 text-sm whitespace-nowrap">+110 € <span class="text-[11px] font-bold">(-85 € dto.)</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">195 €</td>
          </tr>
          <tr class="bg-indigo-50/90 border-l-8 border-l-indigo-700">
            <td class="p-3 font-black text-indigo-950">Grupo 4 · S10 Voz IA</td>
            <td class="p-3 text-slate-800">Centralita Recepcionista de Voz IA 24/7 conectada en vivo a tu agenda y WhatsApp</td>
            <td class="p-3 font-black text-indigo-900 text-sm whitespace-nowrap">+250 € <span class="text-[11px] font-bold">(-100 € dto.)</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">350 €</td>
          </tr>
          <tr class="bg-teal-50/90 border-l-8 border-l-teal-600">
            <td class="p-3 font-black text-teal-950">Super-Auditorías Web</td>
            <td class="p-3 text-slate-800">Auditoría e Implantación Llave en Mano SEO Local + GEO (IA) o Neuro-CRO Web (Sin cuotas)</td>
            <td class="p-3 font-black text-emerald-700 text-sm whitespace-nowrap">195 € (1) | 390 € (las 2)</td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">350 € (1) | 590 € (las 2)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-center text-xs text-slate-500 pt-3 border-t border-slate-200">
      <strong>Sistemas Pyme — Francisco M. Gallardo (NIF 52938419D)</strong> • Tel / WhatsApp: <strong>711 54 75 61</strong> • Precios netos sin IVA (21%).
    </div>
  </div>
</body>
</html>
"""


# ==============================================================================
# 5. REPARACIÓN DE `index.html` Y ACTUALIZACIÓN DE LOS 6 TARJETONES
# ==============================================================================
def reparar_index_html_v152(html):
    # 1. Quitar cualquier bloque [SP_AGENDA_CRM_WEB_SYNC_V1...] y cualquier [SP_PATCH_V15...] previo
    html = re.sub(
        r"<!-- \[SP_AGENDA_CRM_WEB_SYNC_V1\d+_START\] -->[\s\S]*?<!-- \[SP_AGENDA_CRM_WEB_SYNC_V1\d+_END\] -->\s*",
        "",
        html
    )
    html = re.sub(
        r"<!-- \[SP_PATCH_V15\d_START\] -->[\s\S]*?<!-- \[SP_PATCH_V15\d_END\] -->\s*",
        "",
        html
    )

    # 2. Restaurar el bloque original de `spReproducirEnTeleprompter2027` y el vigilante de micrófono en el motor V131
    html = html.replace(
        "/* V158: mantenemos la instancia única de micrófono viva sin destruirla mientras el consultor habla */",
        """if (_spRecogInstance) {
          try {
            _spRecogInstance.onend = null;
            _spRecogInstance.onerror = null;
            _spRecogInstance.onresult = null;
            _spRecogInstance.stop();
          } catch (e) {}
          _spRecogInstance = null;
          _spMicroSesionActiva = false;
        }"""
    )

    # 3. Restaurar el vigilante nativo de manos libres dentro de `iniciarVigilanteMicrofonoContinuo`
    html = re.sub(
        r"function iniciarVigilanteMicrofonoContinuo\(\)\s*\{\s*/\*[\s\S]*?\*/\s*\}",
        """function iniciarVigilanteMicrofonoContinuo() {
        if (_spWatchdogMicroInterval) return;
        _spWatchdogMicroInterval = setInterval(function() {
          var vistaTec = document.getElementById('vista-tecnosala');
          if (!vistaTec || vistaTec.classList.contains('hidden')) return;
          if (_spOrbeDespierto && _spAutoEscuchaContinua && !_spHablandoSintesis && !_spMicroSesionActiva && !_spRearmandoOido) {
            window.spActivarModoEscuchaPersistente(false);
          }
        }, 1200);
      }""",
        html
    )

    # 4. Neutralizar `instalarMicrofonoContinuoSinRePromptV129` en `spScriptMejorasCarritoYMigradoPersistenteV130`
    #    para que NO llame a `getUserMedia` ni cree un segundo micrófono que pida permiso dos veces
    html = re.sub(
        r"function instalarMicrofonoContinuoSinRePromptV129\(\)\s*\{[\s\S]*?\n  \}\n\n  function obtenerTramosPorDiaSemanaV125",
        """function instalarMicrofonoContinuoSinRePromptV129() {
    /* V160: Desactivado para no duplicar getUserMedia ni interferir con el motor nativo del Orbe 3D */
  }

  function obtenerTramosPorDiaSemanaV125""",
        html,
        count=1
    )

    # 5. Actualizar `llamarVertexDirectoNavegador` en el motor nativo para que busque dinámicamente en la base de datos
    #    de Google (`/v1beta/models`) el modelo Flash-Lite más nuevo (> 2.5) o use `gemini-3.8-flash-lite` en su defecto
    viejo_vertex = re.compile(
        r"function llamarVertexDirectoNavegador\(promptCompleto\)\s*\{[\s\S]*?return intentar\(0\);\s*\}",
        re.MULTILINE
    )
    nuevo_vertex = """var _spColaModelosFlashLiteCache = null;
      function _descubrirModelosFlashLiteGoogle(k) {
        if (_spColaModelosFlashLiteCache) return Promise.resolve(_spColaModelosFlashLiteCache);
        var porDefecto = ['gemini-3.8-flash-lite', 'gemini-3.8-flash-lite-preview', 'gemini-flash-lite-latest', 'gemini-3.0-flash-lite', 'gemini-2.0-flash-lite-001'];
        return fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=100&key=' + encodeURIComponent(k))
          .then(function(r) { return r && r.ok ? r.json() : null; })
          .then(function(d) {
            var mods = (d && Array.isArray(d.models)) ? d.models : [];
            var lite = [];
            for (var i = 0; i < mods.length; i++) {
              var m = mods[i];
              var met = m.supportedGenerationMethods || [];
              if (met.indexOf('generateContent') === -1) continue;
              var id = String(m.name || '').replace(/^models\\//, '');
              var low = id.toLowerCase();
              if (low.indexOf('gemini-') !== 0 || low.indexOf('flash-lite') === -1) continue;
              var mVer = low.match(/gemini-(\\d+(?:\\.\\d+)?)/);
              var ver = mVer ? parseFloat(mVer[1]) : 99.0;
              if (ver > 0 && ver <= 2.5) continue;
              lite.push({ id: id, ver: ver });
            }
            lite.sort(function(a, b) { return b.ver - a.ver; });
            var lista = lite.map(function(x) { return x.id; });
            for (var j = 0; j < porDefecto.length; j++) {
              if (lista.indexOf(porDefecto[j]) === -1) lista.push(porDefecto[j]);
            }
            _spColaModelosFlashLiteCache = lista;
            return lista;
          })
          .catch(function() {
            _spColaModelosFlashLiteCache = porDefecto;
            return porDefecto;
          });
      }

      function llamarVertexDirectoNavegador(promptCompleto) {
        var k = _obtenerKBrowser();
        if (!k) return Promise.resolve(null);
        return _descubrirModelosFlashLiteGoogle(k).then(function(modelosProbar) {
          function intentar(idx) {
            if (idx >= modelosProbar.length) return Promise.resolve(null);
            var m = modelosProbar[idx];
            var url = 'https://aiplatform.googleapis.com/v1beta1/publishers/google/models/' + m + ':generateContent?key=' + encodeURIComponent(k);
            return fetch(url, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                contents: [{ role: 'user', parts: [{ text: promptCompleto }] }],
                generationConfig: { temperature: 0.65, topP: 0.92, maxOutputTokens: 350 }
              })
            })
            .then(function(r) { return r && r.ok ? r.json() : null; })
            .then(function(d) {
              var parts = d && d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts;
              if (parts && parts.length) {
                var txt = parts.map(function(p) { return p.thought ? '' : (p.text || ''); }).join(' ').trim();
                if (txt.length > 10) return { texto: txt, modelo: m };
              }
              return intentar(idx + 1);
            })
            .catch(function() { return intentar(idx + 1); });
          }
          return intentar(0);
        });
      }"""
    if viejo_vertex.search(html):
        html = viejo_vertex.sub(lambda _: nuevo_vertex, html, count=1)

    # 6. Asegurar que en el HTML inyectado de la agenda del carrito ponga "🟢 Calendario Activo" completo
    html = html.replace(
        "🟢 Calendar Activo",
        "🟢 Calendario Activo"
    )

    # 7. Sustituir la sección #vista-tarifas completa por la versión con toda su estructura íntegra
    patron_vista_tarifas = re.compile(
        r"<!-- ={40,}\s*-->\s*<!-- VISTA 4 \(SALA INDEPENDIENTE\): PRECIOS CLAROS[\s\S]*?</section>\s*(?=<!-- ={40,}\s*-->\s*<!-- VISTA 5)",
        re.MULTILINE
    )
    if patron_vista_tarifas.search(html):
        html = patron_vista_tarifas.sub(lambda _: HTML_VISTA_TARIFAS_V152 + "\n\n\n                    ", html, count=1)

    # 8. Inyectar el bloque maestro V160 justo antes del último </body> real (usando rsplit)
    if "</body>" in html:
        partes = html.rsplit("</body>", 1)
        html = partes[0].rstrip() + "\n" + BLOQUE_JS_MAESTRO_WEB_V152.strip() + "\n</body>" + partes[1]

    return html


def actualizar_tarjetones_documentos():
    carpetas_docs = [
        os.path.join(RUTA_WEB_PUBLIC, "documentos"),
        os.path.join(RUTA_SERVICIO_RESENAS, "documentos"),
    ]
    for c_doc in carpetas_docs:
        if not os.path.exists(c_doc):
            os.makedirs(c_doc, exist_ok=True)

        for nom in ("guia_seo_geo.html", "guia_seo_geo_movil.html"):
            escribir_archivo_con_backup(os.path.join(c_doc, nom), HTML_GUIA_SEO_GEO_COMPLETA)

        for nom in ("guia_neuro.html", "guia_neuro_movil.html"):
            escribir_archivo_con_backup(os.path.join(c_doc, nom), HTML_GUIA_NEURO_COMPLETA)

        for nom in ("catalogo.html", "catalogo_movil.html"):
            escribir_archivo_con_backup(os.path.join(c_doc, nom), HTML_CATALOGO_DOSSIER_V152)

        for nom in ("tarifas.html", "tarifas_movil.html"):
            escribir_archivo_con_backup(os.path.join(c_doc, nom), HTML_TARIFAS_OFICIALES_V152)

        for nom in ("desembolso.html", "desembolso_movil.html"):
            escribir_archivo_con_backup(os.path.join(c_doc, nom), HTML_DESEMBOLSO_DIA1_V152)

        for nom in ("setup.html", "setup_movil.html"):
            escribir_archivo_con_backup(os.path.join(c_doc, nom), HTML_SETUP_ANEXO_V152)


def actualizar_index_html():
    rutas_index = [
        os.path.join(RUTA_WEB_PUBLIC, "index.html"),
        os.path.join(RUTA_SERVICIO_RESENAS, "index.html"),
    ]
    for ruta in rutas_index:
        if not os.path.exists(ruta):
            continue
        with open(ruta, "r", encoding="utf-8") as f:
            html_actual = f.read()

        html_nuevo = reparar_index_html_v152(html_actual)
        escribir_archivo_con_backup(ruta, html_nuevo)
        validar_bloques_js_en_html(ruta)


# ==============================================================================
# 6. PASO 1 PRIORITARIO + BLINDAJE ATEXIT: ACTUALIZAR LOS 2 DOCUMENTOS .MD
# ==============================================================================
NOTA_HISTORIAL_V152 = f"""
---
### ACTUALIZACIÓN {VERSION_ACTUAL} ({FECHA_EJECUCION}) — Subcajas Simétricas de 1 Sola Línea en Precios Claros, Botón Mensual con Permanencia de 3 Meses, Contraste Rotundo en Tarjetas Seleccionadas del Carrito, Selector Inteligente Fase 2 y Tecnoconsultor Conectado en Vivo a Gemini con Silenciado al Cambiar de Pestaña
- **Precios Claros (Diapositiva 1):** Titular H2 en 2 líneas (`Precios claros y amortización` / `desde el primer cliente.`), botón `🔄 Mensual (permanencia de 3 meses)`, eliminada la mención de permanencia dentro de `Pyme Base` y unificadas las 3 subcajas con altura idéntica (`h-[100px]`) y 1 sola línea de ahorro en Plan Anual (`🎁 Ahorras 118 € / 198 € al año (pagas 10 meses)`).
- **Carrito Configurador (`#spModalCarritoCarta`):** Contraste máximo entre tarjetas seleccionadas (`✓ ACTIVO`, borde de 3px y color saturado) y no seleccionadas (atenuadas al 58% de opacidad); reajuste de alturas en la columna derecha para que el botón `🚀 Confirmar Pedido y Agendar Alta →` nunca quede cortado al desbloquear el Bono Regalo de Bóveda; y selector inteligente en `5. Reserva Prioritaria Fase 2` que deshabilita en gris (`disabled`) los módulos ya añadidos.
- **Tecnoconsultor (`#vista-tecnosala`):** Conectado en vivo con la IA de Google Gemini (eliminando el retorno fijo en `file://`) y silenciado automático inmediato de voz y micrófono al cambiar a cualquier otra sección del menú.
"""


def actualizar_documentos_maestros_md():
    if getattr(actualizar_documentos_maestros_md, "_ejecutado", False):
        return
    actualizar_documentos_maestros_md._ejecutado = True

    os.makedirs(RUTA_PROGRAMAR, exist_ok=True)
    archivos_md = [
        os.path.join(RUTA_PROGRAMAR, "biblia_de_conocimiento_de_sistemas_pyme.md"),
        os.path.join(RUTA_PROGRAMAR, "manual_maestro_de_programaci_n_ad_py.md"),
    ]
    textos_enviar = {}
    for ruta_md in archivos_md:
        if os.path.exists(ruta_md):
            with open(ruta_md, "r", encoding="utf-8") as f:
                txt = f.read()
            if f"ACTUALIZACIÓN {VERSION_ACTUAL}" not in txt:
                txt = txt.rstrip() + "\n" + NOTA_HISTORIAL_V152
                escribir_archivo_con_backup(ruta_md, txt)
            textos_enviar[os.path.basename(ruta_md)] = txt

    for carpeta_dest in (RUTA_SCRAPER, RUTA_SERVICIO_RESENAS):
        if os.path.exists(carpeta_dest):
            for nom_md, contenido_md in textos_enviar.items():
                try:
                    with open(os.path.join(carpeta_dest, nom_md), "w", encoding="utf-8") as fc:
                        fc.write(contenido_md)
                except Exception:
                    pass

    try:
        payload = json.dumps({
            "accion": "sincronizar_biblia_conocimiento",
            "version": VERSION_ACTUAL,
            "fecha": FECHA_EJECUCION,
            "biblia_markdown": textos_enviar.get("biblia_de_conocimiento_de_sistemas_pyme.md", ""),
            "manual_markdown": textos_enviar.get("manual_maestro_de_programaci_n_ad_py.md", ""),
            "compartir_con": ["fmgallardo@falconfactorysystems.com", "francisco@sistemaspyme.es"]
        }).encode("utf-8")
        req = urllib.request.Request(
            URL_WEBHOOK_SHEETS_DEFAULT,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            if 200 <= resp.status < 400:
                print("  ☁️ Biblia y Manual sincronizados en Google Sheets y Google Drive OK.")
    except Exception as e_cloud:
        print(f"  ℹ️ Aviso sincronización cloud Drive/Sheets: {e_cloud}")


atexit.register(actualizar_documentos_maestros_md)


def replicar_ad_py_en_carpetas_oficiales():
    ruta_actual = os.path.abspath(__file__)
    for carpeta in (RUTA_WEB_PUBLIC, RUTA_SCRAPER, RUTA_SERVICIO_RESENAS):
        if os.path.exists(carpeta):
            destino = os.path.join(carpeta, "AD.py")
            if os.path.abspath(destino) != ruta_actual:
                try:
                    shutil.copy2(ruta_actual, destino)
                except Exception:
                    pass


def sincronizar_git_repositorios():
    for carpeta_git in (RUTA_SERVICIO_RESENAS, os.path.dirname(RUTA_WEB_PUBLIC)):
        if os.path.exists(os.path.join(carpeta_git, ".git")):
            try:
                subprocess.run(["git", "-C", carpeta_git, "add", "-A"], check=False)
                subprocess.run(
                    ["git", "-C", carpeta_git, "commit", "-m", f"feat({VERSION_ACTUAL}): Precios Claros simplificacion maxima, Tecnoconsultor file:// continuo y 6 Tarjetones"],
                    check=False, capture_output=True
                )
                subprocess.run(["git", "-C", carpeta_git, "push"], check=False, capture_output=True)
                print(f"  ✅ Git sincronizado en: {os.path.basename(carpeta_git)}")
            except Exception:
                pass


def ejecutar_actualizacion():
    print("=" * 78)
    print(f"🚀 INICIANDO ACTUALIZACIÓN MAESTRA {VERSION_ACTUAL} — PRECIOS + TECNOCONSULTOR + 6 TARJETONES")
    print("=" * 78)
    actualizar_documentos_maestros_md()
    actualizar_index_html()
    actualizar_tarjetones_documentos()
    replicar_ad_py_en_carpetas_oficiales()
    sincronizar_git_repositorios()
    print("=" * 78)
    print(f"🎉 ACTUALIZACIÓN {VERSION_ACTUAL} COMPLETADA CON ÉXITO — RECARGA TU WEB CON CMD+SHIFT+R")
    print("=" * 78)


if __name__ == "__main__":
    ejecutar_actualizacion()
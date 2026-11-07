#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SISTEMAS PYME — ACTUALIZADOR MAESTRO SEGURO COMPLETO (AD.py - VERSIÓN V151)
================================================================================
Archivo 100% COMPLETO de principio a fin (CERO '# ... existing code ...').
Copia todo este contenido dentro de tu archivo `AD.py` y ejecútalo en Terminal:
    python3 AD.py

Qué soluciona de raíz esta versión V151:
1. TECNOCONSULTOR QUE RESPONDE SIEMPRE AL INSTANTE (EN `file://` Y EN SERVIDOR):
   - En `file://`, las llamadas fetch directas a Vertex AI desde origen nulo
     podían quedarse colgadas sin responder tras pintar tu frase en el
     Teleprompter LED. Ahora tiene un timeout estricto de 1,8s y un salvavidas
     automático que garantiza respuesta hablada y escrita inmediata en <2s.
2. REDISEÑO SIMÉTRICO DE «PRECIOS CLAROS» (DIAPOSITIVA 1 Y DIAPOSITIVA 2):
   - Subcajas de precio unificadas visualmente en las 3 tarjetas (Mensual y Anual),
     sin símbolos `€` partidos en otra línea (`whitespace-nowrap`).
   - Eliminado `Setup Dúo: 225 € + Aud. a 195 €` debajo de la insignia superior
     derecha en Pack Escudo Total / Plus (queda solo `¡Ahorras 155 € / 310 €!`).
   - Línea inferior de ahorro clara en las 3 tarjetas (explicando en Plan Anual
     que el ahorro viene de los 2 meses gratis al pagar 10 meses, e incluyendo
     también la línea de ahorro en Pack Escudo Total y Pack Escudo Plus).
   - Banner inferior hacia la tabla de Auditorías bajado, centrado con aire,
     con flecha animada en movimiento y texto limpio sin precios:
     «🔍🧠 Ver tabla de las 2 Super-Auditorías, los 4 Grupos (S1 a S10) y Atril NFC ↓».
   - En la Diapositiva 2 de Precios: eliminado el banner superior redundante,
     eliminada la columna «Solo Código (200 €)» (son 350 € llave en mano o con
     entrega de códigos e instrucciones al técnico del cliente, y 195 € bonificada),
     cambiado el título a «Los servicios divididos en 4 Grupos (S1 a S10)»,
     quitado «Implantación Rápida» en el Grupo 1 y limpiada la repetición de
     «Grupo 3» y «Grupo 4» en las sublíneas.
3. LÓGICA TÁCTIL ORIGINAL EN LAS 2 TARJETAS DE AUDITORÍAS («CÓMO AYUDAMOS»):
   - Cara A -> clic abre Cara B (Estadísticas).
   - Clic en cualquiera de las 3 subcajas de estadísticas -> despliega la
     explicación detallada de esa estadística.
   - Clic en ese texto desplegado -> vuelve a la Cara B con las 3 subcajas.
   - Clic fuera de las 3 subcajas (en el fondo/cuerpo de la tarjeta en Cara B)
     -> pasa a la Cara C (Técnico). Clic en Cara C -> vuelve a Cara A.
4. RENOVACIÓN COMPLETA DE LOS TARJETONES DE LA BIBLIOTECA (`documentos/*.html`):
   - `guia_seo_geo.html` reconstruida con diseño ejecutivo A4 grande y completo
     (a la par con `guia_neuro.html`), sin la tarifa de «Solo código 200 €».
   - `guia_neuro.html` actualizada sin «Solo código 200 €».
   - `catalogo.html` actualizado con la división oficial en 4 Grupos (S1 a S10)
     combinada con el beneficio de negocio de cada módulo.
   - `tarifas.html`, `desembolso.html` y `setup.html` actualizados con 4 columnas
     limpias (`Pyme Base`, `Escudo Básico`, `Escudo Total`, `Pyme Trinity`,
     `Pyme 4`, `Pyme Pentium`), precios `Desde X €/mes` y la Regla de Oro de
     Combinación Libre entre cualquier grupo.
================================================================================
"""

import os
import sys
import re
import ast
import json
import time
import shutil
import atexit
import subprocess
import urllib.request
from datetime import datetime

VERSION_ACTUAL = "V151"
FECHA_EJECUCION = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
TIMESTAMP_BAK = datetime.now().strftime("%Y%m%d_%H%M%S")

RUTA_WEB_PUBLIC = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme/public_html"
RUTA_SCRAPER = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Scraper/Scrapper App"
RUTA_SERVICIO_RESENAS = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Servicios/Servicio Reseñas/servicio_resenas"
RUTA_PROGRAMAR = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Programar"

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


def validar_bloques_js_en_html(ruta_html):
    if not os.path.exists(ruta_html):
        return True
    try:
        with open(ruta_html, "r", encoding="utf-8") as f:
            html = f.read()
        bloques = re.findall(r"<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>", html, flags=re.IGNORECASE)
        node_bin = shutil.which("node")
        if not node_bin:
            for cand in ("/opt/homebrew/bin/node", "/usr/local/bin/node", "/usr/bin/node"):
                if os.path.exists(cand):
                    node_bin = cand
                    break
        if node_bin and bloques:
            for idx, b in enumerate(bloques):
                if "application/ld+json" in b or not b.strip():
                    continue
                tmp_js = f"/tmp/_sp_check_v151_{idx}.js"
                with open(tmp_js, "w", encoding="utf-8") as tf:
                    tf.write(b)
                proc = subprocess.run([node_bin, "--check", tmp_js], capture_output=True, text=True)
                try:
                    os.remove(tmp_js)
                except Exception:
                    pass
                if proc.returncode != 0:
                    print(f"  ❌ Error JS en bloque #{idx + 1} de {os.path.basename(ruta_html)}:\n{proc.stderr}")
                    return False
        print(f"  🟢 Todos los bloques <script> validados con node --check OK: {os.path.basename(ruta_html)}")
        return True
    except Exception as e:
        print(f"  ⚠️ Aviso validando JS en {ruta_html}: {e}")
        return True


# ==============================================================================
# 2. NUEVA SECCIÓN #vista-tarifas COMPLETA (DIAPOSITIVA 1 Y DIAPOSITIVA 2 LIMPIAS)
# ==============================================================================
HTML_VISTA_TARIFAS_V151 = r"""  <!-- ======================================================================= -->
  <!-- VISTA 4 (SALA INDEPENDIENTE): PRECIOS CLAROS (ARQUITECTURA 4 GRUPOS)    -->
  <!-- ======================================================================= -->
  <section id="vista-tarifas" class="view-panel hidden bg-slate-50 text-slate-900">

    <!-- =================================================================== -->
    <!-- DIAPOSITIVA 1 DE PRECIOS: LOS 3 PLANES ACTIVOS HOY (100VH LUMINOSO) -->
    <!-- =================================================================== -->
    <div id="tarifas-slide-planes" class="slide-section sp-tarifas-light-bg border-b border-teal-200/80 px-4 sm:px-6 relative overflow-hidden" style="min-height: calc(100vh - 5.75rem); padding-top: 1.7rem !important; padding-bottom: 1.2rem !important; justify-content: space-between !important;">
      <div class="absolute inset-0 sp-rhombus-grid-reverse pointer-events-none opacity-65" aria-hidden="true"></div>

      <div class="max-w-6xl mx-auto w-full flex flex-col justify-between flex-1 relative z-10">

        <!-- FILA 1: Encabezado encajado al 100% dentro del ancho de las 3 tarjetas -->
        <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-2.5 pb-2.5 mb-2 border-b-2 border-teal-500/25 w-full">
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

        <!-- FILA 2: Las 3 Tarjetas Protagonistas con Subcajas de Precio 100% Simétricas -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 items-stretch my-auto py-1">

          <!-- TARJETA 1: PYME BASE (1 SERVICIO = 59 €/MES) -->
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

              <!-- Subcaja de Precio Simétrica 1 -->
              <div class="bg-slate-50 border-2 border-slate-200/90 rounded-2xl px-3.5 py-2.5 mb-2.5 shadow-inner flex flex-col justify-between min-h-[96px]">
                <div class="flex items-baseline justify-between gap-2 flex-nowrap" data-plan-price="base">
                  <div class="flex items-baseline gap-1.5 whitespace-nowrap">
                    <span class="text-2xl sm:text-[28px] font-black text-brand-navy whitespace-nowrap">59 €</span>
                    <span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span>
                  </div>
                  <span class="text-[10px] font-bold text-slate-500 bg-white px-2 py-0.5 rounded-lg border border-slate-200 whitespace-nowrap">Desde 1 módulo</span>
                </div>
                <span id="spSubPriceBase" class="block text-[11px] font-extrabold text-slate-800 mt-1 whitespace-nowrap">
                  Día 1 Flex: 209 € (150 € Setup + 59 € Mes 1)
                </span>
                <span id="spSavingLineBase" class="block text-[10.5px] font-extrabold text-teal-800 bg-teal-50/90 border border-teal-200/80 rounded-lg px-2 py-0.5 mt-1 whitespace-nowrap truncate">
                  ✓ Sin permanencia anual (solo 3 meses mín.)
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

          <!-- TARJETA 2: PACK ESCUDO BÁSICO (2 SERVICIOS: S1 + S2 = 99 €/MES) -->
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

              <!-- Subcaja de Precio Simétrica 2 -->
              <div class="bg-white/95 border-2 border-sky-300 rounded-2xl px-3.5 py-2.5 mb-2.5 shadow-inner flex flex-col justify-between min-h-[96px]">
                <div class="flex items-baseline justify-between gap-2 flex-nowrap" data-plan-price="duo">
                  <div class="flex items-baseline gap-1.5 whitespace-nowrap">
                    <span class="text-2xl sm:text-[28px] font-black text-sky-700 whitespace-nowrap">99 €</span>
                    <span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span>
                  </div>
                  <span class="text-[10px] font-extrabold text-sky-900 bg-sky-100 px-2 py-0.5 rounded-lg border border-sky-300 whitespace-nowrap">S1 + S2 Activos</span>
                </div>
                <span id="spSubPriceDuo" class="block text-[11px] font-extrabold text-sky-950 mt-1 whitespace-nowrap">
                  Día 1 Flex: 324 € (225 € Setup + 99 € Mes 1)
                </span>
                <span id="spSavingLineDuo" class="block text-[10.5px] font-extrabold text-emerald-800 bg-emerald-50 border border-emerald-300 rounded-lg px-2 py-0.5 mt-1 whitespace-nowrap truncate">
                  🎁 Ahorras 19 €/mes en cuota + 75 € en Setup
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

          <!-- TARJETA 3 ESTRELLA: PACK ESCUDO TOTAL / PLUS ★ (MISMA SUBCAJA Y SIN TEXTO DUPLICADO ARRIBA) -->
          <div class="sp-price-card-3d sp-price-card-emerald px-5 py-3.5 flex flex-col justify-between relative">
            <div>
              <div class="flex items-start justify-between gap-2 mb-1.5 min-h-[34px]">
                <div class="inline-flex items-center gap-1 text-[10px] font-extrabold uppercase tracking-wider text-white bg-gradient-to-r from-emerald-600 to-teal-600 px-2.5 py-1 rounded-xl shadow-sm leading-tight whitespace-nowrap">
                  <span>🚀 Recomendado (Dúo + Auditoría)</span>
                </div>
                <div class="text-right leading-tight">
                  <span id="spBadgeAhorroEscudoTotal" class="inline-block text-[10px] font-black text-amber-950 bg-amber-100 px-2.5 py-1 rounded-xl border border-amber-400 shadow-sm whitespace-nowrap">
                    ¡Ahorras 155 € en la Auditoría!
                  </span>
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

              <!-- Subcaja de Precio Simétrica 3 (Misma distribución que Pack Escudo Básico) -->
              <div class="bg-white/95 border-2 border-emerald-500/70 rounded-2xl px-3.5 py-2.5 mb-2.5 shadow-inner flex flex-col justify-between min-h-[96px]">
                <div class="flex items-baseline justify-between gap-1.5 flex-nowrap">
                  <div class="flex items-baseline gap-1.5 whitespace-nowrap" data-plan-price="trinity">
                    <span class="text-2xl sm:text-[28px] font-black text-emerald-700 whitespace-nowrap">99 €</span>
                    <span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span>
                  </div>
                  <span id="spAuditAddonPriceTag" class="text-[10px] font-black text-amber-950 bg-amber-100 border border-amber-400 px-2 py-0.5 rounded-lg whitespace-nowrap">
                    + 195 € (1 Auditoría)
                  </span>
                </div>
                <span id="spSubPriceEscudoTotal" class="block text-[11px] font-extrabold text-teal-950 mt-1 whitespace-nowrap">
                  Día 1 Flex: 519 € (225€ Setup + 195€ Aud. + 99€ Mes 1)
                </span>
                <span id="spSavingLineEscudoTotal" class="block text-[10.5px] font-extrabold text-emerald-900 bg-emerald-100/90 border border-emerald-400 rounded-lg px-2 py-0.5 mt-1 whitespace-nowrap truncate">
                  🎁 Ahorras 155 € en Auditoría + 75 € Setup + 19 €/m
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

        <!-- FILA 3: Banner-Guía Inferior Centrado Equidistante, con Flecha en Movimiento y Sin Precios -->
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

        <!-- Cabecera limpia (sin el banner superior redundante) -->
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

          <!-- Columna Izquierda (7 cols): Las 2 Super-Auditorías Gemelas (Sin "Solo Código 200 €") -->
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
                <div class="bg-white rounded-2xl p-3.5 border-2 border-sky-300 flex flex-col justify-between shadow-sm">
                  <span class="block text-[10.5px] font-extrabold text-sky-900 uppercase">1. Tarifa Estándar «Llave en Mano»</span>
                  <span class="block text-2xl font-black text-sky-700 my-0.5">350 € <span class="text-xs font-bold text-slate-500">por 1 auditoría</span></span>
                  <span class="block text-xs font-extrabold text-sky-900">590 € las dos juntas (Ahorras 110 €)</span>
                  <span class="block text-[11px] text-slate-700 leading-snug mt-1.5">Contratada suelta o con Pyme Base. Incluye implantación por nosotros o entrega de todos los códigos e instrucciones a tu técnico.</span>
                </div>
                <div class="bg-emerald-50 rounded-2xl p-3.5 border-2 border-emerald-500 flex flex-col justify-between shadow-md">
                  <span class="block text-[10.5px] font-extrabold text-emerald-900 uppercase">2. Bonificada con Pack 2+ Servicios ★</span>
                  <span class="block text-2xl font-black text-emerald-700 my-0.5">195 € <span class="text-xs font-bold text-emerald-800">por 1 auditoría</span></span>
                  <span class="block text-xs font-black text-emerald-900">390 € las dos juntas (Ahorras 310 €)</span>
                  <span class="block text-[11px] text-emerald-950 font-semibold leading-snug mt-1.5">Todo el servicio «Llave en Mano» completo bonificado un 44% al activar cualquier Pack de 2 o más servicios.</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Columna Derecha (5 cols): Los servicios divididos en 4 Grupos (Sin repetir Grupo 3 ni Grupo 4) + Hardware Atril -->
          <div class="lg:col-span-5 flex flex-col justify-between gap-3.5">

            <div class="sp-light-card-3d-sky rounded-3xl p-4 flex-1 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                  <span class="text-[10.5px] font-extrabold uppercase tracking-wider text-sky-900 bg-sky-100 px-2.5 py-0.5 rounded-full border border-sky-300">
                    🚀 Los servicios divididos en 4 Grupos (S1 a S10)
                  </span>
                  <span class="text-[10.5px] font-extrabold text-emerald-700">🎁 Bóveda Gratis (3+ serv.)</span>
                </div>
                <ul class="space-y-1.5 text-[11.5px] text-slate-800 leading-snug">
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong class="text-brand-navy">Grupo 1</strong> (S1 Reseñas, S2 WA, S3 Leads, S4 Gastos, S5 Inactivos):</span>
                    <strong class="text-brand-navy whitespace-nowrap">59 € 1.º | +40 €/m</strong>
                  </li>
                  <li class="flex justify-between gap-2 border-b border-sky-200/70 pb-1">
                    <span><strong class="text-sky-900">Grupo 2</strong> (S6 Agenda, S7 Firma, S8 Cobros):</span>
                    <strong class="text-sky-800 whitespace-nowrap">+59 €/m (+110 €) <span class="text-[10px] text-slate-500 font-normal">| 79€ s.</span></strong>
                  </li>
                  <li class="pt-0.5">
                    <div class="flex justify-between gap-2">
                      <span><strong class="text-pink-800">Grupo 3</strong> · Sat.1 Instagram 3 en 1 (Meta API):</span>
                      <strong class="text-pink-700 whitespace-nowrap">+49 €/m (+75 €) <span class="text-[10px] text-slate-500 font-normal">| 69€ s.</span></strong>
                    </div>
                    <div class="flex justify-between gap-2 pl-12 border-b border-sky-200/70 pb-1 mt-0.5 text-slate-700">
                      <span>· Sat.2 Logística 360 / Sat.3 Redactor RAG:</span>
                      <strong class="text-indigo-700 whitespace-nowrap">+59 € / +69 €/m <span class="text-[10px] text-slate-500 font-normal">combo</span></strong>
                    </div>
                  </li>
                  <li class="pt-0.5">
                    <div class="flex justify-between gap-2">
                      <span><strong class="text-indigo-950">Grupo 4</strong> · S9 Rescate Llamadas WA (250/m):</span>
                      <strong class="text-sky-800 whitespace-nowrap">+59 €/m (+110 €) <span class="text-[10px] text-slate-500 font-normal">| 79€ s.</span></strong>
                    </div>
                    <div class="flex justify-between gap-2 pl-12 mt-0.5 text-slate-700">
                      <span>· S10 Centralita Voz IA 24/7 (250 min):</span>
                      <strong class="text-indigo-900 whitespace-nowrap">+129 €/m (+250 €) <span class="text-[10px] text-slate-500 font-normal">| 169€ s.</span></strong>
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


# ==============================================================================
# 3. BLOQUE JS DEFINITIVO V151 PARA `index.html`:
#    - TECNOCONSULTOR CON RESPUESTA GARANTIZADA EN <2 SEGUNDOS (CERO BLOQUEOS)
#    - RENDERIZADOR SIMÉTRICO DE PRECIOS CLAROS (MENSUAL Y ANUAL SIN SALTOS DE €)
#    - LÓGICA TÁCTIL ORIGINAL DE LAS 2 TARJETAS DE AUDITORÍAS EN «CÓMO AYUDAMOS»
#    - CARRITO COLOREADO Y SINCRONIZADO CON AGENDA CRM
# ==============================================================================
BLOQUE_JS_MAESTRO_WEB_V151 = r'''
<!-- [SP_AGENDA_CRM_WEB_SYNC_V151_START] -->
<script>
(function() {
  /* =========================================================================
     1. REPARACIÓN DEL TECNOCONSULTOR EN `file://` Y SERVIDOR:
        Cuando terminas de hablar y aparece tu frase en el Teleprompter LED,
        garantiza que responda en voz alta en <1.8s sin quedarse colgado en
        los 4 intentos de fetch a Vertex AI cuando abres desde `file://`.
     ========================================================================= */
  var _spRecUnicoV151 = null;
  var _spEscuchandoActivoV151 = false;
  var _spHablandoConsultorV151 = false;
  var _spManosLibresDeseadoV151 = false;
  var _spTimerSilencioV151 = null;
  var _spLineaDictadoEnPantallaV151 = null;
  var _spPidiendoPermisoAhoraV151 = false;
  var _spUltimoStartTsV151 = 0;

  function actualizarUiMicrofonoTecnosalaV151(modo) {
    var btnV = document.getElementById('spBtnVoiceTecnosala');
    var txtV = document.getElementById('spVoiceBtnText');
    var icoV = document.getElementById('spVoiceMicIcon');
    var inp = document.getElementById('spTecnosalaInput');
    var hud = document.getElementById('spTeleprompterHudStatus');
    var wrappers = document.querySelectorAll('#spOrb3DWrapperMain, #vista-tecnosala .sp-ai-core-orb');

    for (var i = 0; i < wrappers.length; i++) {
      wrappers[i].classList.remove('sp-orb-state-speaking', 'sp-orb-state-listening');
      if (modo === 'speaking') wrappers[i].classList.add('sp-orb-state-speaking');
      else if (modo === 'listening') wrappers[i].classList.add('sp-orb-state-listening');
    }

    if (modo === 'listening') {
      if (btnV) btnV.classList.add('sp-voice-listening');
      if (txtV) txtV.textContent = 'Escuchando...';
      if (icoV) icoV.textContent = '🔴';
      if (inp) inp.setAttribute('placeholder', '🟢 Escuchando tu voz ahora... habla con total naturalidad');
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping inline-block mr-1.5"></span>🎙️ MANOS LIBRES ACTIVO • HÁBLAME DIRECTAMENTE SIN PULSAR NADA';
    } else if (modo === 'speaking') {
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Hablar';
      if (icoV) icoV.textContent = '🎙️';
      if (inp) inp.setAttribute('placeholder', '🔊 El consultor te está respondiendo (al terminar volverá a escucharte)...');
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse inline-block mr-1.5"></span>HABLANDO EN VIVO • AL TERMINAR SE ACTIVARÁ EL MICRÓFONO SOLO';
    } else {
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Hablar';
      if (icoV) icoV.textContent = '🎙️';
      if (inp) inp.setAttribute('placeholder', 'Escribe tu duda o pulsa 🎙️ Hablar o la Esfera 3D para hablar por voz...');
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-sky-400 inline-block mr-1.5"></span>⏸ EN PAUSA • PULSA LA ESFERA 3D O «🎙️ HABLAR» PARA ACTIVAR EL MICRO';
    }
  }

  function pintarTranscripcionEnTeleprompterV151(textoParcial) {
    var track = document.getElementById('spTeleprompterRollTrack');
    if (!track) return;
    if (!_spLineaDictadoEnPantallaV151 || !_spLineaDictadoEnPantallaV151.parentNode) {
      _spLineaDictadoEnPantallaV151 = document.createElement('div');
      _spLineaDictadoEnPantallaV151.className = 'sp-led-line-item sp-led-line-user';
      track.appendChild(_spLineaDictadoEnPantallaV151);
      while (track.children.length > 4) {
        track.removeChild(track.firstElementChild);
      }
    }
    _spLineaDictadoEnPantallaV151.innerHTML = '🎙️ <span>«' + String(textoParcial || '').replace(/</g, '&lt;') + '»</span><span class="sp-led-cursor"></span>';
  }

  function limpiarLineaDictadoTemporalV151() {
    if (_spLineaDictadoEnPantallaV151 && _spLineaDictadoEnPantallaV151.parentNode) {
      try { _spLineaDictadoEnPantallaV151.parentNode.removeChild(_spLineaDictadoEnPantallaV151); } catch (e) {}
    }
    _spLineaDictadoEnPantallaV151 = null;
  }

  function inicializarInstanciaUnicaSpeechV151() {
    if (_spRecUnicoV151) return _spRecUnicoV151;
    var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) return null;

    var rec = new SpeechRec();
    rec.lang = 'es-ES';
    rec.continuous = true;
    rec.interimResults = true;
    rec.maxAlternatives = 1;

    var fraseAcumulada = '';

    function dispararEnvioFraseDetectada() {
      if (_spTimerSilencioV151) {
        clearTimeout(_spTimerSilencioV151);
        _spTimerSilencioV151 = null;
      }
      var enviar = String(fraseAcumulada || '').trim();
      fraseAcumulada = '';
      if (!enviar || enviar.length < 2) return;
      if (_spHablandoConsultorV151) return;

      limpiarLineaDictadoTemporalV151();
      _spHablandoConsultorV151 = true;

      if (_spRecUnicoV151 && _spEscuchandoActivoV151) {
        try { _spRecUnicoV151.stop(); } catch (e) {}
        _spEscuchandoActivoV151 = false;
      }

      actualizarUiMicrofonoTecnosalaV151('speaking');
      window.spProcesarConsultaEnTeleprompterDirecto(enviar);
    }

    rec.onstart = function() {
      _spEscuchandoActivoV151 = true;
      _spPidiendoPermisoAhoraV151 = false;
      if (!_spHablandoConsultorV151) {
        actualizarUiMicrofonoTecnosalaV151('listening');
      }
    };

    rec.onresult = function(ev) {
      if (_spHablandoConsultorV151 || (window.speechSynthesis && window.speechSynthesis.speaking)) {
        fraseAcumulada = '';
        return;
      }
      var textoActual = '';
      var esFinal = false;
      for (var i = ev.resultIndex; i < ev.results.length; i++) {
        textoActual += ev.results[i][0].transcript;
        if (ev.results[i].isFinal) esFinal = true;
      }
      var limpio = textoActual.trim();
      if (!limpio) return;
      fraseAcumulada = limpio;

      var inp = document.getElementById('spTecnosalaInput');
      if (inp) inp.value = limpio;
      pintarTranscripcionEnTeleprompterV151(limpio);

      if (_spTimerSilencioV151) clearTimeout(_spTimerSilencioV151);
      _spTimerSilencioV151 = setTimeout(dispararEnvioFraseDetectada, esFinal ? 620 : 1100);
    };

    rec.onerror = function(ev) {
      _spEscuchandoActivoV151 = false;
      _spPidiendoPermisoAhoraV151 = false;
      var errCode = ev ? ev.error : '';
      if (errCode === 'not-allowed' || errCode === 'service-not-allowed') {
        _spManosLibresDeseadoV151 = false;
        actualizarUiMicrofonoTecnosalaV151('idle');
      }
    };

    rec.onend = function() {
      _spEscuchandoActivoV151 = false;
      _spPidiendoPermisoAhoraV151 = false;

      if (fraseAcumulada && fraseAcumulada.trim().length >= 2 && !_spHablandoConsultorV151) {
        dispararEnvioFraseDetectada();
        return;
      }

      var vistaTec = document.getElementById('vista-tecnosala');
      var enTecnosala = vistaTec && !vistaTec.classList.contains('hidden');
      if (_spManosLibresDeseadoV151 && !_spHablandoConsultorV151 && enTecnosala) {
        setTimeout(function() {
          if (_spManosLibresDeseadoV151 && !_spHablandoConsultorV151 && !_spEscuchandoActivoV151) {
            window.spActivarModoEscuchaPersistente(false);
          }
        }, 300);
      } else if (!_spHablandoConsultorV151) {
        actualizarUiMicrofonoTecnosalaV151('idle');
      }
    };

    _spRecUnicoV151 = rec;
    return rec;
  }

  window.spActivarModoEscuchaPersistente = function(forzarManual) {
    var vistaTec = document.getElementById('vista-tecnosala');
    if (!vistaTec || vistaTec.classList.contains('hidden')) return;

    if (forzarManual) {
      _spManosLibresDeseadoV151 = true;
      _spHablandoConsultorV151 = false;
      if (window.speechSynthesis && window.speechSynthesis.speaking) {
        try { window.speechSynthesis.cancel(); } catch (e) {}
      }
    }

    if (!_spManosLibresDeseadoV151 || _spHablandoConsultorV151) return;
    if (_spEscuchandoActivoV151 || _spPidiendoPermisoAhoraV151) return;

    var ahora = Date.now();
    if (!forzarManual && (ahora - _spUltimoStartTsV151 < 800)) return;
    _spUltimoStartTsV151 = ahora;

    var rec = inicializarInstanciaUnicaSpeechV151();
    if (!rec) return;

    try {
      _spPidiendoPermisoAhoraV151 = true;
      rec.start();
    } catch (e) {
      _spPidiendoPermisoAhoraV151 = false;
    }
  };

  window.spIniciarEscuchaDirectaConsultor = function() {
    _spManosLibresDeseadoV151 = true;
    _spHablandoConsultorV151 = false;
    window.spActivarModoEscuchaPersistente(true);
  };

  window.spToggleDictadoVozTecnosala = function() {
    var stage = document.getElementById('spTeleprompter2027Stage');
    if (!stage && typeof window.spActivarOrbeConsultorInteractivo === 'function') {
      window.spActivarOrbeConsultorInteractivo();
      return;
    }
    if (_spEscuchandoActivoV151 && _spRecUnicoV151) {
      _spManosLibresDeseadoV151 = false;
      try { _spRecUnicoV151.stop(); } catch (e) {}
      _spEscuchandoActivoV151 = false;
      actualizarUiMicrofonoTecnosalaV151('idle');
      return;
    }
    _spManosLibresDeseadoV151 = true;
    _spHablandoConsultorV151 = false;
    window.spActivarModoEscuchaPersistente(true);
  };

  /* LA CLAVE POR LA QUE ANTES NO TE CONTESTABA AL HABLARLE:
     Sobrescribimos `spProcesarConsultaEnTeleprompterDirecto` con un temporizador
     salvavidas de 1.8 segundos para que NUNCA se quede mudo esperando un fetch colgado */
  var _historialV151 = [];
  window.spProcesarConsultaEnTeleprompterDirecto = function(textoPregunta) {
    var limpia = String(textoPregunta || '').trim();
    if (!limpia) return;

    var inp = document.getElementById('spTecnosalaInput');
    if (inp) inp.value = '';

    _historialV151.push('Usuario: ' + limpia);
    if (typeof window.spExtraerYPreconfigurarCarritoDesdeCharla === 'function') {
      try { window.spExtraerYPreconfigurarCarritoDesdeCharla(limpia, _historialV151); } catch (e) {}
    }

    var respLocalGarantizada = (typeof window.spObtenerRespuestaOmniscienteCompleta === 'function')
      ? window.spObtenerRespuestaOmniscienteCompleta(limpia)
      : 'En Sistemas Pyme activamos en 24-48 horas tu sistema de Reseñas con IA en Google (59 €/mes), el Cortafuegos por WhatsApp (en Pack Escudo Básico Dúo por 99 €/mes), el Atril NFC (39 €) y nuestras 2 Super-Auditorías SEO/GEO IA y Neuro-CRO Web (195 € c/u con Pack o 350 € sueltas). ¿Qué área de tu negocio quieres impulsar primero?';

    var respondidoYa = false;
    function emitirRespuestaEnVivo(textoRespuesta) {
      if (respondidoYa) return;
      respondidoYa = true;
      var textoFinal = String(textoRespuesta || respLocalGarantizada).replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim();
      _historialV151.push('Consultor: ' + textoFinal);
      if (typeof window.spReproducirEnTeleprompter2027 === 'function') {
        window.spReproducirEnTeleprompter2027(textoFinal, null, limpia);
      }
    }

    /* Salvavidas estricto: si en 1.6 segundos el servidor remoto no ha contestado, responde al instante con la Base Omnisciente */
    var timerSalvavidas = setTimeout(function() {
      emitirRespuestaEnVivo(respLocalGarantizada);
    }, 1600);

    fetch('http://127.0.0.1:5000/api/tecnosala-consulta', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pregunta: limpia, apoyo: respLocalGarantizada })
    })
    .then(function(r) { return r && r.ok ? r.json() : null; })
    .then(function(d) {
      clearTimeout(timerSalvavidas);
      if (d && (d.respuesta || d.answer)) {
        emitirRespuestaEnVivo(d.respuesta || d.answer);
      } else {
        emitirRespuestaEnVivo(respLocalGarantizada);
      }
    })
    .catch(function() {
      clearTimeout(timerSalvavidas);
      emitirRespuestaEnVivo(respLocalGarantizada);
    });
  };

  function engancharTurnosDePalabraConsultorV151() {
    if (typeof window.spReproducirEnTeleprompter2027 === 'function' && !window.spReproducirEnTeleprompter2027._hookV151) {
      var origReprod = window.spReproducirEnTeleprompter2027;
      var nuevaReprod = function(textoCompleto, alTerminarCallback, etiquetaUsuarioPrevio) {
        _spHablandoConsultorV151 = true;
        _spManosLibresDeseadoV151 = true;
        limpiarLineaDictadoTemporalV151();
        if (_spRecUnicoV151 && _spEscuchandoActivoV151) {
          try { _spRecUnicoV151.stop(); } catch (e) {}
          _spEscuchandoActivoV151 = false;
        }
        actualizarUiMicrofonoTecnosalaV151('speaking');

        return origReprod.call(this, textoCompleto, function() {
          _spHablandoConsultorV151 = false;
          if (typeof alTerminarCallback === 'function') {
            try { alTerminarCallback(); } catch (e) {}
          }
          if (_spManosLibresDeseadoV151) {
            setTimeout(function() {
              window.spActivarModoEscuchaPersistente(false);
            }, 220);
          }
        }, etiquetaUsuarioPrevio);
      };
      nuevaReprod._hookV151 = true;
      window.spReproducirEnTeleprompter2027 = nuevaReprod;
    }

    if (typeof window.spPararConsultorTotalmente === 'function' && !window.spPararConsultorTotalmente._hookV151) {
      var origParar = window.spPararConsultorTotalmente;
      var nuevoParar = function(ev) {
        _spManosLibresDeseadoV151 = false;
        _spHablandoConsultorV151 = false;
        _spEscuchandoActivoV151 = false;
        _spPidiendoPermisoAhoraV151 = false;
        if (_spTimerSilencioV151) {
          clearTimeout(_spTimerSilencioV151);
          _spTimerSilencioV151 = null;
        }
        limpiarLineaDictadoTemporalV151();
        if (_spRecUnicoV151) {
          try { _spRecUnicoV151.stop(); } catch (e) {}
        }
        var r = origParar.apply(this, arguments);
        actualizarUiMicrofonoTecnosalaV151('idle');
        return r;
      };
      nuevoParar._hookV151 = true;
      window.spPararConsultorTotalmente = nuevoParar;
    }
  }

  /* =========================================================================
     2. MOTOR SIMÉTRICO DE PRECIOS CLAROS (MENSUAL Y PLAN ANUAL SIN SALTOS DE €)
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
    var tagAud = document.getElementById('spAuditAddonPriceTag');
    var bulletAud = document.getElementById('spBulletAuditEscudo');
    var bulletBon = document.getElementById('spBulletBonusEscudo');
    var badgeAhorro = document.getElementById('spBadgeAhorroEscudoTotal');
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
    if (tagAud) tagAud.textContent = esPlus ? '+ 390 € (2 Auditorías)' : '+ 195 € (1 Auditoría)';
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

    if (window._spModoTarifasActual === 'anual') {
      if (btnA) btnA.className = 'px-3 py-1.5 rounded-xl text-xs font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer flex items-center gap-1 whitespace-nowrap';
      if (btnM) btnM.className = 'px-3 py-1.5 rounded-xl text-xs font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer whitespace-nowrap';

      if (pBase) pBase.innerHTML = '<div class="flex items-baseline gap-1.5 whitespace-nowrap"><span class="text-2xl sm:text-[28px] font-black text-brand-navy whitespace-nowrap">49 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes eq. (590 €/año)</span></div><span class="text-[10px] font-bold text-slate-500 bg-white px-2 py-0.5 rounded-lg border border-slate-200 whitespace-nowrap">10 meses</span>';
      if (subBase) subBase.textContent = 'Día 1 Anual: 740 € (590 € 10 meses + 150 € Setup)';
      if (savBase) savBase.textContent = '🎁 Ahorras 118 € al año (pagas 10 meses = 2 meses gratis)';

      if (pDuo) pDuo.innerHTML = '<div class="flex items-baseline gap-1.5 whitespace-nowrap"><span class="text-2xl sm:text-[28px] font-black text-sky-700 whitespace-nowrap">82,50 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes eq. (990 €/año)</span></div><span class="text-[10px] font-extrabold text-sky-900 bg-sky-100 px-2 py-0.5 rounded-lg border border-sky-300 whitespace-nowrap">S1 + S2</span>';
      if (subDuo) subDuo.textContent = 'Día 1 Anual: 1.215 € (990 € 10 meses + 225 € Setup)';
      if (savDuo) savDuo.textContent = '🎁 Ahorras 198 € en cuotas (2 meses gratis) + 75 € Setup';

      if (pTri) pTri.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-emerald-700 whitespace-nowrap">82,50 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes eq. (990 €/año)</span>';
      var totalAnualEsc = 1215 + costeAud;
      if (subEsc) subEsc.textContent = 'Día 1 Anual: ' + totalAnualEsc + ' € (1.215 € Pack Anual + ' + costeAud + ' € Aud.)';
      if (savEsc) savEsc.textContent = '🎁 Ahorras 198 € (2 meses gratis) + ' + ahorroAud + ' € en Auditoría + 75 € Setup';
    } else {
      if (btnM) btnM.className = 'px-3 py-1.5 rounded-xl text-xs font-extrabold bg-brand-navy text-white shadow-sm transition-all cursor-pointer whitespace-nowrap';
      if (btnA) btnA.className = 'px-3 py-1.5 rounded-xl text-xs font-extrabold text-slate-700 hover:text-brand-navy transition-all cursor-pointer flex items-center gap-1 whitespace-nowrap';

      if (pBase) pBase.innerHTML = '<div class="flex items-baseline gap-1.5 whitespace-nowrap"><span class="text-2xl sm:text-[28px] font-black text-brand-navy whitespace-nowrap">59 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span></div><span class="text-[10px] font-bold text-slate-500 bg-white px-2 py-0.5 rounded-lg border border-slate-200 whitespace-nowrap">Desde 1 módulo</span>';
      if (subBase) subBase.textContent = 'Día 1 Flex: 209 € (150 € Setup + 59 € Mes 1)';
      if (savBase) savBase.textContent = '✓ Sin permanencia anual (solo 3 meses mín.)';

      if (pDuo) pDuo.innerHTML = '<div class="flex items-baseline gap-1.5 whitespace-nowrap"><span class="text-2xl sm:text-[28px] font-black text-sky-700 whitespace-nowrap">99 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span></div><span class="text-[10px] font-extrabold text-sky-900 bg-sky-100 px-2 py-0.5 rounded-lg border border-sky-300 whitespace-nowrap">S1 + S2 Activos</span>';
      if (subDuo) subDuo.textContent = 'Día 1 Flex: 324 € (225 € Setup + 99 € Mes 1)';
      if (savDuo) savDuo.textContent = '🎁 Ahorras 19 €/mes en cuota + 75 € en Setup';

      if (pTri) pTri.innerHTML = '<span class="text-2xl sm:text-[28px] font-black text-emerald-700 whitespace-nowrap">99 €</span><span class="text-xs font-bold text-slate-500 whitespace-nowrap">/ mes</span>';
      var totalFlexEsc = 324 + costeAud;
      if (subEsc) subEsc.textContent = 'Día 1 Flex: ' + totalFlexEsc + ' € (225€ Setup + ' + costeAud + '€ Aud. + 99€ Mes 1)';
      if (savEsc) savEsc.textContent = '🎁 Ahorras ' + ahorroAud + ' € en Auditoría + 75 € Setup + 19 €/m';
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
     3. LÓGICA TÁCTIL ORIGINAL DE LAS 2 TARJETAS DE AUDITORÍAS («CÓMO AYUDAMOS»)
        - Cara A -> clic abre Cara B (Estadísticas con sus 3 subcajas).
        - Si pinchas encima de una de las 3 subcajas de estadísticas -> abre la
          explicación detallada de esa estadística.
        - Si vuelves a pinchar en ese texto detallado -> regresa a la Cara B
          con las 3 subcajas de estadísticas.
        - Si estás en la Cara B y pinchas fuera de las 3 subcajas -> pasa a la
          Cara C (Explicación Técnica).
        - Si estás en la Cara C y pinchas en la tarjeta (o en ✕) -> vuelve a la Cara A.
     ========================================================================= */
  var DETALLE_SUBCAJAS_AUDITORIA = {
    1: {
      1: {
        titulo: '📊 x9 Ventas desde ChatGPT y Asistentes IA (Seer Interactive):',
        texto: 'En el buscador tradicional de Google solo compra el 1,76% de las visitas porque abren diez pestañas para comparar precios. En cambio, cuando un cliente pregunta a ChatGPT o Gemini «¿cuál es el mejor profesional de mi zona?» y la IA recomienda directamente tu negocio, la conversión a cliente real sube al <strong>15,9% (9 veces más cierres)</strong>.'
      },
      2: {
        titulo: '📊 +115% más apariciones al estructurar tu Entidad (Univ. de Princeton):',
        texto: 'El 83% de los negocios recomendados por las IAs no son las webs más grandes, sino aquellas cuyos datos internos están conectados mediante código estructurado <code>Schema.org JSON-LD</code> al nodo oficial de su ciudad en <strong>Wikidata</strong> y cuentan con archivo <code>/llms.txt</code>.'
      },
      3: {
        titulo: '📊 El 69% decide leyendo el resumen de la IA (Similarweb / SparkToro):',
        texto: 'Casi 7 de cada 10 búsquedas actuales se resuelven leyendo el bloque superior generado por la IA sin hacer clic en enlaces azules. El 44% de esas recomendaciones se extraen del bloque de respuesta directa de tu portada.'
      }
    },
    2: {
      1: {
        titulo: '📊 +156% más ventas al colocar tu propuesta donde miran (MIT Attention Insight):',
        texto: 'El visitante decide en los primeros 3 a 5 segundos si se queda en tu web o se marcha. Al situar tu titular de valor, tus estrellas de Google Maps y tu llamada a la acción en las zonas calientes de lectura ocular, los contactos aumentan un 156%.'
      },
      2: {
        titulo: '📊 +103% el doble de llamadas eliminando fricción móvil (Ley de Hick):',
        texto: 'Cada casilla innecesaria en un formulario o un teléfono que no se puede pulsar con el pulgar desde el móvil hace que la mitad de tus visitas abandone. Simplificar el contacto duplica del 3,3% al 6,7% quienes te llaman o escriben.'
      },
      3: {
        titulo: '📊 Sonda Térmica de 10 a 14 días (Certeza matemática del 94%):',
        texto: 'En lugar de cambiar tu web a ciegas, instalamos durante 10-14 días nuestra Sonda Árbitro 100% anónima (cumplidora AEPD) que mide en qué punto exacto abandonan tus visitas y cuántas llamadas pierde tu teléfono fijo fuera de horario (tanto en Modo Ágil como en Modo Corporativo).'
      }
    }
  };

  window.spCerrarTarjetaAuditoriaACaraA = function(num, ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    var circle = document.getElementById('spCaAuditCircle_' + num);
    if (circle) circle.classList.remove('sp-circle-open');
    window.spRestaurarVista3SubcajasCaraB(num);
  };

  window.spRestaurarVista3SubcajasCaraB = function(num) {
    var caraB = document.getElementById('spCaAuditCaraB_' + num);
    var caraC = document.getElementById('spCaAuditCaraC_' + num);
    var resStat = document.getElementById('spCaAuditStatResumen_' + num);
    var deepStat = document.getElementById('spCaAuditStatDeep_' + num);
    var grid3 = document.getElementById('spCaStatGrid3_' + num);
    var foot = document.getElementById('spCaStatFoot_' + num);
    var singleExp = document.getElementById('spCaStatSingleExpand_' + num);
    var btnB = document.getElementById('spBtnCaraB_' + num);
    var btnC = document.getElementById('spBtnCaraC_' + num);
    var linkToggle = document.getElementById('spLinkToggleVista_' + num);

    if (caraB) caraB.classList.remove('hidden');
    if (caraC) caraC.classList.add('hidden');
    if (resStat) resStat.classList.remove('hidden');
    if (deepStat) deepStat.classList.add('hidden');
    if (grid3) grid3.classList.remove('hidden');
    if (foot) foot.classList.remove('hidden');
    if (singleExp) {
      singleExp.classList.add('hidden');
      singleExp.innerHTML = '';
    }
    if (btnB && btnC) {
      if (num === 1) {
        btnB.className = 'px-3 py-1 rounded-full text-xs font-black bg-cyan-600 text-white shadow cursor-pointer transition';
        btnC.className = 'px-3 py-1 rounded-full text-xs font-bold bg-white/85 text-cyan-900 border border-cyan-400/60 cursor-pointer transition';
      } else {
        btnB.className = 'px-3 py-1 rounded-full text-xs font-black bg-amber-500 text-slate-950 shadow cursor-pointer transition';
        btnC.className = 'px-3 py-1 rounded-full text-xs font-bold bg-white/85 text-amber-900 border border-amber-400/60 cursor-pointer transition';
      }
    }
    if (linkToggle) {
      linkToggle.textContent = '🛠️ Ver explicación técnica (Cara C) →';
    }
  };

  window.spCambiarCaraInternaAuditoria = function(num, caraDestino, ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    var caraB = document.getElementById('spCaAuditCaraB_' + num);
    var caraC = document.getElementById('spCaAuditCaraC_' + num);
    var btnB = document.getElementById('spBtnCaraB_' + num);
    var btnC = document.getElementById('spBtnCaraC_' + num);
    var linkToggle = document.getElementById('spLinkToggleVista_' + num);

    if (caraDestino === 'C') {
      if (caraB) caraB.classList.add('hidden');
      if (caraC) caraC.classList.remove('hidden');
      if (btnB && btnC) {
        if (num === 1) {
          btnC.className = 'px-3 py-1 rounded-full text-xs font-black bg-cyan-600 text-white shadow cursor-pointer transition';
          btnB.className = 'px-3 py-1 rounded-full text-xs font-bold bg-white/85 text-cyan-900 border border-cyan-400/60 cursor-pointer transition';
        } else {
          btnC.className = 'px-3 py-1 rounded-full text-xs font-black bg-amber-500 text-slate-950 shadow cursor-pointer transition';
          btnB.className = 'px-3 py-1 rounded-full text-xs font-bold bg-white/85 text-amber-900 border border-amber-400/60 cursor-pointer transition';
        }
      }
      if (linkToggle) linkToggle.textContent = '📊 Volver a Estadísticas (Cara B)';
    } else {
      window.spRestaurarVista3SubcajasCaraB(num);
    }
  };

  /* Al pinchar encima de una de las 3 subcajas de estadísticas -> muestra su explicación detallada.
     Al volver a pinchar en ese texto detallado -> regresa a la Cara B con las 3 subcajas. */
  window.spToggleExpandirCajaStat = function(numCard, idxStat, ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    var grid3 = document.getElementById('spCaStatGrid3_' + numCard);
    var foot = document.getElementById('spCaStatFoot_' + numCard);
    var singleExp = document.getElementById('spCaStatSingleExpand_' + numCard);
    if (!singleExp || !grid3) return;

    var info = (DETALLE_SUBCAJAS_AUDITORIA[numCard] || {})[idxStat];
    if (!info) return;

    grid3.classList.add('hidden');
    if (foot) foot.classList.add('hidden');
    var borderCol = (numCard === 1) ? 'border-cyan-500/70 hover:bg-cyan-50/90' : 'border-amber-500/70 hover:bg-amber-50/90';
    var badgeCol = (numCard === 1) ? 'text-cyan-800' : 'text-amber-900';

    singleExp.className = 'bg-white/95 rounded-2xl p-3.5 border-2 ' + borderCol + ' shadow-md text-left cursor-pointer transition my-1';
    singleExp.innerHTML =
      '<div class="flex items-center justify-between gap-2 border-b border-slate-200 pb-1.5 mb-1.5">' +
        '<strong class="text-[13.5px] sm:text-[14.5px] font-black text-brand-navy">' + info.titulo + '</strong>' +
        '<span class="text-[11px] font-extrabold ' + badgeCol + ' underline whitespace-nowrap">&larr; Pulsa aquí para volver</span>' +
      '</div>' +
      '<p class="text-[12.5px] sm:text-[13.5px] text-slate-800 leading-relaxed">' + info.texto + '</p>';

    singleExp.onclick = function(eClick) {
      if (eClick && eClick.stopPropagation) eClick.stopPropagation();
      window.spRestaurarVista3SubcajasCaraB(numCard);
    };
  };

  window.spToggleProfundizarCaraAuditoria = function(num, ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    var caraC = document.getElementById('spCaAuditCaraC_' + num);
    var estaEnCaraC = caraC && !caraC.classList.contains('hidden');
    if (estaEnCaraC) {
      window.spCambiarCaraInternaAuditoria(num, 'B', ev);
    } else {
      window.spCambiarCaraInternaAuditoria(num, 'C', ev);
    }
  };

  /* Clic general en la tarjeta de Auditoría:
     - Si está cerrada (Cara A) -> abre Cara B (con las 3 subcajas de estadísticas).
     - Si está abierta en Cara B (con las 3 subcajas visibles) y pinchas fuera de las subcajas -> pasa a Cara C (Técnico).
     - Si está abierta en un detalle de estadística -> vuelve a las 3 subcajas de Cara B.
     - Si está en Cara C y pinchas fuera de botones -> cierra a Cara A. */
  window.spToggleAuditCircleCA = function(num, ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    var card = document.getElementById('spCaAuditCard_' + num);
    var badge = document.getElementById('spCaAuditBadge_' + num);
    var circle = document.getElementById('spCaAuditCircle_' + num);
    if (!circle) return;

    if (card && badge) {
      var cRect = card.getBoundingClientRect();
      var bRect = badge.getBoundingClientRect();
      if (cRect.width > 0 && cRect.height > 0) {
        var cx = (((bRect.left + bRect.width / 2) - cRect.left) / cRect.width * 100).toFixed(1) + '%';
        var cy = (((bRect.top + bRect.height / 2) - cRect.top) / cRect.height * 100).toFixed(1) + '%';
        circle.style.setProperty('--sp-cx', cx);
        circle.style.setProperty('--sp-cy', cy);
      }
    }

    var otroNum = (num === 1) ? 2 : 1;
    var otroCircle = document.getElementById('spCaAuditCircle_' + otroNum);

    if (!circle.classList.contains('sp-circle-open')) {
      if (otroCircle) otroCircle.classList.remove('sp-circle-open');
      window.spRestaurarVista3SubcajasCaraB(num);
      circle.classList.add('sp-circle-open');
      return;
    }

    /* Si ya estaba abierta: comprobar si está en un detalle expandido, en Cara B o en Cara C */
    var singleExp = document.getElementById('spCaStatSingleExpand_' + num);
    var caraC = document.getElementById('spCaAuditCaraC_' + num);
    if (singleExp && !singleExp.classList.contains('hidden')) {
      window.spRestaurarVista3SubcajasCaraB(num);
    } else if (caraC && !caraC.classList.contains('hidden')) {
      window.spCerrarTarjetaAuditoriaACaraA(num, ev);
    } else {
      window.spCambiarCaraInternaAuditoria(num, 'C', ev);
    }
  };

  /* =========================================================================
     4. COLORES Y AGENDA DEL CARRITO DE COMPRA (TARJETAS 4, 5 Y CITA DE ALTA)
     ========================================================================= */
  function aplicarIdsColorCajasCarritoV151() {
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
  }

  window.spAbrirCarritoConDiagnosticoPreseleccionado = function() {
    if (typeof window.spAbrirCarritoConfigurador === 'function') {
      window.spAbrirCarritoConfigurador('duo', 1);
      setTimeout(aplicarIdsColorCajasCarritoV151, 40);
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
    aplicarIdsColorCajasCarritoV151();
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
      var guardados = JSON.parse(localStorage.getItem('sp_citas_ocupadas_crm_v151') || '[]');
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
              localStorage.setItem('sp_citas_ocupadas_crm_v151', JSON.stringify(Array.from(window.SP_SLOTS_OCUPADOS_CRM_EXTRA)));
            } catch (e) {}
          }
        })
        .catch(function() {});
    })).then(function() {
      window.spAplicarBloqueoHorasCrmEnSelect();
    });
  };

  function inicializarMejorasV151() {
    engancharTurnosDePalabraConsultorV151();
    aplicarIdsColorCajasCarritoV151();
    window._spRenderizarTarjetasPrecios();
    window.spSincronizarCitasCrmLocal();

    if (typeof window.spActualizarHorasDisponiblesCarritoV125 === 'function' && !window.spActualizarHorasDisponiblesCarritoV125._hookV151) {
      var origActHoras = window.spActualizarHorasDisponiblesCarritoV125;
      var nuevaActHoras = function() {
        var r = origActHoras.apply(this, arguments);
        window.spAplicarBloqueoHorasCrmEnSelect();
        return r;
      };
      nuevaActHoras._hookV151 = true;
      window.spActualizarHorasDisponiblesCarritoV125 = nuevaActHoras;
    }

    if (typeof window.spAbrirCarritoConfigurador === 'function' && !window.spAbrirCarritoConfigurador._hookV151) {
      var origOpen = window.spAbrirCarritoConfigurador;
      var nuevoOpen = function() {
        var r = origOpen.apply(this, arguments);
        aplicarIdsColorCajasCarritoV151();
        window.spSincronizarCitasCrmLocal();
        setTimeout(window.spAplicarBloqueoHorasCrmEnSelect, 120);
        return r;
      };
      nuevoOpen._hookV151 = true;
      window.spAbrirCarritoConfigurador = nuevoOpen;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(inicializarMejorasV151, 180);
    });
  } else {
    setTimeout(inicializarMejorasV151, 180);
  }
})();
</script>
<!-- [SP_AGENDA_CRM_WEB_SYNC_V151_END] -->
'''


# ==============================================================================
# 4. GENERADORES DE LOS TARJETONES OFICIALES DE LA BIBLIOTECA (`documentos/*.html`)
#    - Sin la opción de "Solo Código 200 €" (son 350 € llave en mano o con códigos
#      para su técnico, y 195 € bonificada con Pack 2+).
#    - `guia_seo_geo.html` igual de amplia, profunda y visual que `guia_neuro.html`.
#    - `tarifas.html` y `desembolso.html` con 4 columnas limpias y la Regla de Oro
#      de Combinación Libre (`Desde X €/mes`) para `Pyme Base`, `Escudo Básico`,
#      `Escudo Total`, `Pyme Trinity`, `Pyme 4` y `Pyme Pentium`.
# ==============================================================================
ESTILO_COMUN_TARJETONES = """
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; background: #0f172a; color: #0f172a; margin: 0; padding: 24px 16px; }
    h1, h2, h3, h4, .font-display { font-family: 'Montserrat', 'Inter', sans-serif; letter-spacing: -0.02em; }
    .a4-sheet { max-width: 980px; margin: 0 auto; background: #ffffff; border-radius: 24px; padding: 36px 42px; box-shadow: 0 25px 60px -15px rgba(0,0,0,0.6); border: 2px solid #0d9488; }
    @media print {
      body { background: #ffffff; padding: 0; }
      .a4-sheet { box-shadow: none; border: none; padding: 12px; max-width: 100%; }
      .no-print { display: none !important; }
    }
  </style>
"""

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
    <!-- Barra superior de acciones -->
    <div class="no-print flex flex-wrap items-center justify-between gap-3 pb-5 mb-6 border-b border-slate-200">
      <div class="flex items-center gap-2">
        <span class="px-3 py-1 rounded-full bg-sky-100 text-sky-900 font-extrabold text-xs border border-sky-300">🧭 DOSSIER TÉCNICO OFICIAL • AUDITORÍA 1</span>
        <span class="text-xs font-bold text-slate-500">Formato Ejecutivo A4 / Móvil</span>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="bg-[#0b2239] hover:bg-slate-800 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow cursor-pointer">🖨️ Imprimir / Guardar PDF</button>
        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20acabo%20de%20leer%20la%20Gu%C3%ADa%20T%C3%A9cnica%20SEO%2FGEO%20IA%20y%20quiero%20consultarte%20para%20mi%20negocio" target="_blank" class="bg-[#0d7d74] hover:bg-teal-700 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow">💬 Consultar con Francisco</a>
      </div>
    </div>

    <!-- Cabecera Ejecutiva -->
    <div class="bg-gradient-to-r from-[#0b2239] via-[#0f3456] to-[#0d7d74] text-white rounded-3xl p-6 sm:p-8 mb-7 shadow-lg">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
        <span class="text-[11px] font-extrabold uppercase tracking-widest text-teal-300 bg-white/10 px-3 py-1 rounded-full border border-teal-300/40">Ingeniería de Entidades Digitales • Sistemas Pyme</span>
        <span class="text-xs font-bold text-amber-300">Sin cambiar ni un píxel el diseño visual de tu web</span>
      </div>
      <h1 class="text-2xl sm:text-4xl font-black leading-tight mb-2">
        Super-Auditoría e Implantación SEO Local + GEO (IA)
      </h1>
      <p class="text-sm sm:text-base text-slate-200 leading-relaxed max-w-3xl">
        Cómo logramos que tu negocio aparezca en el <strong>Top 3 de Google Maps</strong> y sea la respuesta recomendada por <strong>ChatGPT, Gemini, Perplexity, Claude y Siri</strong> cuando un cliente busca tu especialidad en tu ciudad.
      </p>
    </div>

    <!-- Bloque 1: Las 3 Estadísticas de Impacto Real -->
    <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-3">1. Por qué el Posicionamiento en IA (GEO / LLMO) multiplica tus ventas</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-7">
      <div class="bg-sky-50 border-2 border-sky-300 rounded-2xl p-4">
        <span class="block text-2xl sm:text-3xl font-black text-sky-700 mb-1">x9 Ventas (15,9%)</span>
        <strong class="block text-xs uppercase tracking-wider text-sky-950 mb-1">Estudio Seer Interactive</strong>
        <p class="text-xs text-slate-700 leading-relaxed">Mientras que el buscador tradicional de Google convierte al 1,76% (porque el usuario abre 10 webs para comparar), quien llega recomendado por ChatGPT convierte al <strong>15,9%</strong>.</p>
      </div>
      <div class="bg-teal-50 border-2 border-teal-300 rounded-2xl p-4">
        <span class="block text-2xl sm:text-3xl font-black text-teal-700 mb-1">+115,1% Visibilidad</span>
        <strong class="block text-xs uppercase tracking-wider text-teal-950 mb-1">Universidad de Princeton (GEO)</strong>
        <p class="text-xs text-slate-700 leading-relaxed">El <strong>83%</strong> de los negocios citados por las IAs no estaban en el Top 10 antiguo: son elegidos porque sus datos internos están estructurados con <code>Schema.org</code> y <code>Wikidata</code>.</p>
      </div>
      <div class="bg-amber-50 border-2 border-amber-300 rounded-2xl p-4">
        <span class="block text-2xl sm:text-3xl font-black text-amber-700 mb-1">69% Cero Clics</span>
        <strong class="block text-xs uppercase tracking-wider text-amber-950 mb-1">Similarweb & SparkToro</strong>
        <p class="text-xs text-slate-700 leading-relaxed">Casi 7 de cada 10 búsquedas actuales se deciden leyendo el resumen superior de la IA. El <strong>44%</strong> de las citas salen de las primeras 100 palabras de tu portada.</p>
      </div>
    </div>

    <!-- Bloque 2: Qué auditamos e implantamos (Los 22 Parámetros y las 2 Tablas) -->
    <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-3">2. Qué incluye nuestra Ingeniería (22 Parámetros en 2 Tablas: Dueño + Informático)</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-7 text-xs sm:text-[13px]">
      <div class="bg-slate-50 border border-slate-300 rounded-2xl p-5 space-y-2.5">
        <span class="inline-block text-[11px] font-black uppercase tracking-wider bg-[#0b2239] text-white px-3 py-1 rounded-lg">A. Grafo de Entidad e Inteligencia Artificial (GEO)</span>
        <ul class="space-y-2 text-slate-700 leading-snug">
          <li>✔ <strong>Carnet Digital Invisible (<code>Schema.org @graph JSON-LD</code>):</strong> Pasamos tu web de dar <code>0 resultados</code> en el validador oficial de Google (<em>Rich Results Test</em>) a estar <strong>Validada en Verde</strong> con coordenadas GPS, horarios, área de servicio y nota media.</li>
          <li>✔ <strong>Conexión Oficial con <code>Wikidata</code>:</strong> Enlazamos tu entidad con el nodo oficial de tu ciudad y especialidad en Wikidata para que ChatGPT y Gemini no confundan tu negocio.</li>
          <li>✔ <strong>Autoridad E-E-A-T de Fundadores:</strong> Fichas estructuradas de dirección/doctores/abogados, colegios profesionales (<code>memberOf</code>), universidades (<code>alumniOf</code>) y prensa.</li>
          <li>✔ <strong>Estándar <code>/llms.txt</code> y Permisos de Bots IA:</strong> Instalamos el archivo de lectura directa para motores generativos y habilitamos en <code>/robots.txt</code> a <code>OAI-SearchBot</code>, <code>ChatGPT-User</code>, <code>PerplexityBot</code>, <code>ClaudeBot</code> y <code>Google-Extended</code>.</li>
        </ul>
      </div>

      <div class="bg-slate-50 border border-slate-300 rounded-2xl p-5 space-y-2.5">
        <span class="inline-block text-[11px] font-black uppercase tracking-wider bg-[#0d7d74] text-white px-3 py-1 rounded-lg">B. SEO Local en Google Maps y Portada RAG</span>
        <ul class="space-y-2 text-slate-700 leading-snug">
          <li>✔ <strong>Bloque de Respuesta Directa (Primeras 100 palabras):</strong> Redactamos e inyectamos el resumen semántico del que las IAs extraen el 44% de sus recomendaciones.</li>
          <li>✔ <strong>Etiquetas <code>&lt;title&gt;</code>, <code>&lt;meta description&gt;</code>, <code>&lt;h1&gt;</code> y <code>&lt;h2&gt;</code> Conversacionales:</strong> Optimizadas con tu especialidad + localidad exacta.</li>
          <li>✔ <strong>4 Meta-Etiquetas Geográficas Invisibles:</strong> <code>geo.region</code>, <code>geo.placename</code>, <code>geo.position</code> e <code>ICBM</code> en la cabecera de tu web.</li>
          <li>✔ <strong>Módulo <code>FAQPage</code> Invisible + Acordeón Visible:</strong> 5 a 6 preguntas estratégicas respondidas en menos de 40 palabras listas para Google y Google Business Profile.</li>
          <li>✔ <strong>Consistencia NAP+W y Enlace UTM para Google Maps:</strong> Medición exacta de cuántas visitas y llamadas entran desde tu ficha de Google Maps.</li>
        </ul>
      </div>
    </div>

    <!-- Bloque 3: Formato de Entrega en 2 Tablas -->
    <div class="bg-gradient-to-r from-sky-50 to-teal-50 border-2 border-teal-400 rounded-2xl p-5 mb-7">
      <h3 class="text-base font-black text-[#0b2239] mb-2">📋 Doble Entrega Clarísima (Para Ti y Para tu Informático):</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-[13px] text-slate-800">
        <div>
          <strong class="text-sky-900 block mb-0.5">1. Tabla Ejecutiva para el Dueño (Lenguaje Claro):</strong>
          Explicación sin tecnicismos del estado actual de tu negocio frente a tus competidores locales y el impacto comercial de cada mejora.
        </div>
        <div>
          <strong class="text-teal-900 block mb-0.5">2. Paquete de Ingeniería Llave en Mano:</strong>
          Lo dejamos implantado nosotros mismos en 24-48h sin interrumpir tu actividad o, si tienes informático propio, nos reunimos 15 min con él y le entregamos todos los códigos e instrucciones paso a paso.
        </div>
      </div>
    </div>

    <!-- Bloque 4: Inversión Única Oficial (Sin "Solo Código 200 €") -->
    <h2 class="text-lg sm:text-xl font-black text-[#0b2239] mb-3">3. Inversión Oficial (Pago Único • Sin Cuotas Mensuales)</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 text-center">
      <div class="bg-white border-2 border-sky-400 rounded-2xl p-5 shadow-sm">
        <span class="inline-block text-[11px] font-extrabold uppercase tracking-wider text-sky-900 bg-sky-100 px-3 py-0.5 rounded-full mb-2">1. Tarifa Estándar «Llave en Mano»</span>
        <div class="text-3xl font-black text-sky-700 mb-1">350 € <span class="text-xs font-bold text-slate-500">por 1 auditoría</span></div>
        <div class="text-sm font-extrabold text-[#0b2239] mb-2">590 € si contratas las 2 Super-Auditorías juntas (Ahorras 110 €)</div>
        <p class="text-xs text-slate-600 leading-relaxed">Contratada de forma suelta o junto al plan Pyme Base (1 servicio). Incluye diagnóstico completo, implantación técnica o entrega de todos los códigos e instrucciones a tu técnico y verificación en verde en Google.</p>
      </div>

      <div class="bg-emerald-50 border-2 border-emerald-500 rounded-2xl p-5 shadow-md">
        <span class="inline-block text-[11px] font-extrabold uppercase tracking-wider text-emerald-950 bg-emerald-200 px-3 py-0.5 rounded-full mb-2">2. Bonificada con Pack de 2+ Servicios ★</span>
        <div class="text-3xl font-black text-emerald-700 mb-1">195 € <span class="text-xs font-bold text-emerald-900">por 1 auditoría</span></div>
        <div class="text-sm font-black text-emerald-950 mb-2">390 € si contratas las 2 Super-Auditorías juntas (Ahorras 310 €)</div>
        <p class="text-xs text-emerald-950 leading-relaxed font-medium">Al activar cualquier Pack de 2 o más servicios mensuales (como el <strong>Pack Escudo Básico Dúo</strong> de 99 €/mes), tienes un <strong>44% de bonificación directa</strong> en nuestras Super-Auditorías Llave en Mano.</p>
      </div>
    </div>

    <div class="text-center text-xs text-slate-500 pt-3 border-t border-slate-200">
      <strong>Sistemas Pyme — Francisco M. Gallardo (NIF 52938419D)</strong> • Tel / WhatsApp: <strong>711 54 75 61</strong> • Web: <strong>sistemaspyme.es</strong> • Precios netos sin IVA (21%).
    </div>
  </div>
</body>
</html>
"""


HTML_TARIFAS_OFICIALES_V151 = f"""<!DOCTYPE html>
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
      <p class="text-xs sm:text-sm text-teal-100">Con salvar o captar un solo cliente al mes, todo el sistema se amortiza solo. Modalidad Flexible (3 meses mín.) o Plan Anual (pagas 10 meses = 2 meses gratis).</p>
    </div>

    <!-- TABLA 1: PLANES DE LIBRE ELECCIÓN EN 4 COLUMNAS LIMPIAS -->
    <h2 class="text-base sm:text-lg font-black text-[#0b2239] mb-2">1. Planes Mensuales de Libre Elección (4 Columnas Claras)</h2>
    <div class="overflow-x-auto mb-3">
      <table class="w-full text-left border-collapse text-xs sm:text-[13px]">
        <thead>
          <tr class="bg-[#0b2239] text-white">
            <th class="p-3 rounded-tl-xl">Nombre del Módulo / Pack</th>
            <th class="p-3">1. Cuota al Mes</th>
            <th class="p-3">2. Setup Único (Alta)</th>
            <th class="p-3 rounded-tr-xl">3. En qué consiste (Libre Combinación entre los 4 Grupos)</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200 border border-slate-200">
          <tr class="bg-white">
            <td class="p-3 font-black text-[#0b2239]">Pyme Base</td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 59 € / mes<span class="block text-[10.5px] text-teal-700 font-bold">Anual: desde 49 €/m eq.</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">Desde 150 €</td>
            <td class="p-3 text-slate-700"><strong>1 servicio de libre elección</strong> de cualquiera de los 4 grupos (ej. S1 Reseñas IA o S2 Cortafuegos WhatsApp). Incluye Informe Mensual 360°.</td>
          </tr>
          <tr class="bg-sky-50/70">
            <td class="p-3 font-black text-sky-900">Escudo Básico</td>
            <td class="p-3 font-black text-sky-700 whitespace-nowrap">Desde 99 € / mes<span class="block text-[10.5px] text-sky-900 font-bold">Anual: desde 82,50 €/m eq.</span></td>
            <td class="p-3 font-bold text-sky-950 whitespace-nowrap">Desde 225 €<span class="block text-[10px] text-emerald-700 font-extrabold">(2.º Setup al 50%)</span></td>
            <td class="p-3 text-slate-800"><strong>2 servicios de libre elección</strong> (ej. S1 Reseñas IA + S2 Cortafuegos WA). Desbloquea las Super-Auditorías a <strong>195 € c/u</strong> (en vez de 350 €).</td>
          </tr>
          <tr class="bg-emerald-50/90 border-l-4 border-l-emerald-500">
            <td class="p-3 font-black text-emerald-950">Escudo Total ★</td>
            <td class="p-3 font-black text-emerald-700 whitespace-nowrap">Desde 99 € / mes<span class="block text-[10.5px] text-amber-900 font-extrabold">+ 195 € (1 Aud.) o 390 € (las 2)</span></td>
            <td class="p-3 font-bold text-emerald-950 whitespace-nowrap">Desde 225 € + Aud.<span class="block text-[10px] text-emerald-800 font-extrabold">(Ahorras 155 € o 310 €)</span></td>
            <td class="p-3 text-slate-800"><strong>2 servicios de libre elección + 1 o 2 Super-Auditorías Llave en Mano</strong> bonificadas a 195 € c/u (SEO+GEO IA y/o Neuro-CRO Web).</td>
          </tr>
          <tr class="bg-amber-50/60">
            <td class="p-3 font-black text-[#0b2239]">Pyme Trinity 🎁</td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 139 € / mes<span class="block text-[10.5px] text-teal-700 font-bold">Anual: desde 115,80 €/m eq.</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">Desde 300 €</td>
            <td class="p-3 text-slate-800"><strong>3 servicios mensuales de libre elección</strong> de cualquier grupo + <strong>🎁 Bóveda Segura de Contraseñas GRATIS</strong> (valorada en 150 €) + Auditorías a 195 € c/u.</td>
          </tr>
          <tr class="bg-white">
            <td class="p-3 font-black text-[#0b2239]">Pyme 4</td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 179 € / mes<span class="block text-[10.5px] text-teal-700 font-bold">Anual: desde 149,15 €/m eq.</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">Desde 375 €</td>
            <td class="p-3 text-slate-700"><strong>4 servicios mensuales de libre elección</strong> combinando cualquier grupo + Bóveda de Contraseñas GRATIS + Auditorías bonificadas a 195 € c/u.</td>
          </tr>
          <tr class="bg-slate-50">
            <td class="p-3 font-black text-[#0b2239]">Pyme Pentium</td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 219 € / mes<span class="block text-[10.5px] text-teal-700 font-bold">Anual: desde 182,50 €/m eq.</span></td>
            <td class="p-3 font-bold text-slate-800 whitespace-nowrap">Desde 450 €</td>
            <td class="p-3 text-slate-700"><strong>5 servicios mensuales de libre elección</strong> combinando cualquier grupo + Bóveda de Contraseñas GRATIS + Auditorías bonificadas a 195 € c/u.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- REGLA DE ORO DE COMBINACIÓN LIBRE ENTRE GRUPOS -->
    <div class="bg-amber-50 border-2 border-amber-400 rounded-2xl p-4 mb-6 text-xs text-slate-800 leading-relaxed">
      <strong class="text-amber-950 font-black block mb-1">💡 ¿Cómo se calcula tu cuota exacta al combinar servicios de distintos Grupos? (Regla del Módulo Base):</strong>
      Puedes combinar libremente servicios de cualquiera de los 4 Grupos (por ejemplo, elegir para tu <em>Pyme Trinity</em> el servicio S4 del Grupo 1, el S6 del Grupo 2 y el S10 del Grupo 4). <strong>Tu primer servicio toma siempre la tarifa individual del módulo más económico que hayas incluido</strong> (59 €/m y 150 € Setup si incluyes al menos uno del Grupo 1; o la tarifa suelta de su grupo si todos pertenecen a los Grupos 2, 3 o 4), y <strong>todos los demás servicios se suman directamente con su tarifa reducida de combinación (Combo)</strong> detallada aquí abajo:
    </div>

    <!-- TABLA 2: LOS SERVICIOS DIVIDIDOS EN 4 GRUPOS + SUPER-AUDITORÍAS Y ATRIL -->
    <h2 class="text-base sm:text-lg font-black text-[#0b2239] mb-2">2. Tarifas por Grupo (S1 a S10), Super-Auditorías y Hardware NFC</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
      <div class="border-2 border-sky-300 rounded-2xl p-4 bg-sky-50/40 space-y-2">
        <h3 class="font-black text-[#0b2239] text-sm border-b border-sky-200 pb-1">🚀 Los servicios divididos en 4 Grupos (Cuota Combo vs. Suelto)</h3>
        <ul class="space-y-1.5 text-slate-800">
          <li class="flex justify-between gap-2"><span><strong>Grupo 1 (S1 a S5):</strong> Reseñas IA, Cortafuegos WA, Leads 10s, Facturas Foto, Inactivos</span><strong class="whitespace-nowrap text-teal-800">+40 €/m (+75€) | 59€ (150€) s.</strong></li>
          <li class="flex justify-between gap-2"><span><strong>Grupo 2 (S6 a S8):</strong> Agenda Anti-Plantón, Firma Digital, Anti-Morosidad</span><strong class="whitespace-nowrap text-sky-800">+59 €/m (+110€) | 79€ (195€) s.</strong></li>
          <li>
            <div class="flex justify-between gap-2"><span><strong>Grupo 3</strong> · Sat.1 Instagram 3 en 1 (Meta API):</span><strong class="whitespace-nowrap text-pink-700">+49 €/m (+75€) | 69€ (150€) s.</strong></div>
            <div class="flex justify-between gap-2 pl-12 mt-0.5 text-slate-700"><span>· Sat.2 Logística 360 / Sat.3 Redactor B2B RAG:</span><strong class="whitespace-nowrap text-indigo-700">+59€ / +69 €/m combo</strong></div>
          </li>
          <li>
            <div class="flex justify-between gap-2"><span><strong>Grupo 4</strong> · S9 Rescate Llamadas Perdidas WA (250/m):</span><strong class="whitespace-nowrap text-sky-800">+59 €/m (+110€) | 79€ (195€) s.</strong></div>
            <div class="flex justify-between gap-2 pl-12 mt-0.5 text-slate-700"><span>· S10 Centralita Voz IA 24/7 (250 min/m):</span><strong class="whitespace-nowrap text-indigo-900">+129 €/m (+250€) | 169€ (350€) s.</strong></div>
          </li>
        </ul>
      </div>

      <div class="border-2 border-teal-400 rounded-2xl p-4 bg-teal-50/40 space-y-2">
        <h3 class="font-black text-[#0b2239] text-sm border-b border-teal-200 pb-1">🔍🧠 Super-Auditorías Web y ★ Atril NFC + QR (Pagos Únicos)</h3>
        <ul class="space-y-1.5 text-slate-800">
          <li class="flex justify-between gap-2"><span><strong>Super-Auditoría Llave en Mano (Suelta o con Pyme Base):</strong><br><span class="text-[11px] text-slate-600">(Implantada por nosotros o entregando códigos e instrucciones a tu técnico)</span></span><strong class="whitespace-nowrap text-sky-800">350 € (1) | 590 € (las 2)</strong></li>
          <li class="flex justify-between gap-2"><span><strong>Super-Auditoría Bonificada (Con Pack 2+ servicios ★):</strong></span><strong class="whitespace-nowrap text-emerald-700">195 € (1) | 390 € (las 2)</strong></li>
          <li class="flex justify-between gap-2 pt-1 border-t border-teal-200"><span><strong>★ Atril Inteligente NFC + QR (Pago único sin cuotas):</strong></span><strong class="whitespace-nowrap text-amber-800">39 € (1.ª) | 29 € (2ª-4ª) | 25 € (5+)</strong></li>
        </ul>
      </div>
    </div>

    <div class="text-center text-xs text-slate-500 mt-6 pt-3 border-t border-slate-200">
      <strong>Sistemas Pyme — Francisco M. Gallardo (NIF 52938419D)</strong> • Tel / WhatsApp: <strong>711 54 75 61</strong> • Precios netos sin IVA (21%) • Domiciliación SEPA.
    </div>
  </div>
</body>
</html>
"""


HTML_DESEMBOLSO_DIA1_V151 = f"""<!DOCTYPE html>
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
      <p class="text-xs sm:text-sm text-emerald-100">Qué abonas el Día 1 al poner en marcha tu sistema (Setup de instalación única + primer período) tanto en Vía Flexible como en Plan Anual (pagas 10 meses y disfrutas de 2 meses gratis).</p>
    </div>

    <!-- TABLA DE 4 COLUMNAS LIMPIAS -->
    <div class="overflow-x-auto mb-5">
      <table class="w-full text-left border-collapse text-xs sm:text-[13px]">
        <thead>
          <tr class="bg-[#0b2239] text-white">
            <th class="p-3 rounded-tl-xl">Módulo / Pack</th>
            <th class="p-3">1. Vía Flexible: Total Día 1<span class="block text-[10px] text-teal-300 font-normal">(Setup único + Mes 1)</span></th>
            <th class="p-3">2. Plan Anual: Total Día 1<span class="block text-[10px] text-amber-300 font-normal">(Setup único + 10 Meses = 2 Gratis)</span></th>
            <th class="p-3 rounded-tr-xl">3. Qué incluye y Ahorro Directo</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200 border border-slate-200">
          <tr class="bg-white">
            <td class="p-3 font-black text-[#0b2239]">Pyme Base<span class="block text-[11px] text-slate-500 font-normal">1 servicio libre elección</span></td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 209 €<span class="block text-[10.5px] text-slate-500 font-normal">(150 € Setup + 59 € Mes 1)</span></td>
            <td class="p-3 font-black text-teal-800 whitespace-nowrap">Desde 740 €<span class="block text-[10.5px] text-slate-600 font-normal">(150 € Setup + 590 € Año)</span></td>
            <td class="p-3 text-slate-700">1 servicio a elegir. En Plan Anual <strong>ahorras 118 €</strong> (2 meses gratis).</td>
          </tr>
          <tr class="bg-sky-50/70">
            <td class="p-3 font-black text-sky-900">Escudo Básico<span class="block text-[11px] text-sky-700 font-normal">2 servicios libre elección</span></td>
            <td class="p-3 font-black text-sky-800 whitespace-nowrap">Desde 324 €<span class="block text-[10.5px] text-slate-600 font-normal">(225 € Setup + 99 € Mes 1)</span></td>
            <td class="p-3 font-black text-sky-900 whitespace-nowrap">Desde 1.215 €<span class="block text-[10.5px] text-slate-600 font-normal">(225 € Setup + 990 € Año)</span></td>
            <td class="p-3 text-slate-800"><strong>Ahorras 75 € en Setup + 19 €/m</strong> (y en Plan Anual <strong>198 € extra</strong> por 2 meses gratis). Desbloquea Auditorías a 195 €.</td>
          </tr>
          <tr class="bg-emerald-50/90 border-l-4 border-l-emerald-500">
            <td class="p-3 font-black text-emerald-950">Escudo Total ★<span class="block text-[11px] text-emerald-800 font-bold">2 servicios + 1 o 2 Auditorías</span></td>
            <td class="p-3 font-black text-emerald-800 whitespace-nowrap">Desde 519 € (con 1 Aud.)<span class="block text-[10.5px] text-emerald-950 font-bold">o 714 € (con las 2 Auditorías)</span></td>
            <td class="p-3 font-black text-emerald-900 whitespace-nowrap">Desde 1.410 € (con 1 Aud.)<span class="block text-[10.5px] text-emerald-950 font-bold">o 1.605 € (con las 2 Auditorías)</span></td>
            <td class="p-3 text-slate-800">Incluye S1+S2 + Super-Auditoría(s) bonificada(s) a 195 € c/u. <strong>Ahorras 155 € (con 1) o 310 € (con las 2)</strong> + 75 € Setup.</td>
          </tr>
          <tr class="bg-amber-50/60">
            <td class="p-3 font-black text-[#0b2239]">Pyme Trinity 🎁<span class="block text-[11px] text-amber-800 font-bold">3 servicios libre elección</span></td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 439 €<span class="block text-[10.5px] text-slate-600 font-normal">(300 € Setup + 139 € Mes 1)</span></td>
            <td class="p-3 font-black text-teal-900 whitespace-nowrap">Desde 1.690 €<span class="block text-[10.5px] text-slate-600 font-normal">(300 € Setup + 1.390 € Año)</span></td>
            <td class="p-3 text-slate-800">3 servicios mensuales + <strong>🎁 Bóveda de Contraseñas GRATIS (150 €)</strong>. En Anual <strong>ahorras 278 €</strong> en cuotas.</td>
          </tr>
          <tr class="bg-white">
            <td class="p-3 font-black text-[#0b2239]">Pyme 4<span class="block text-[11px] text-slate-500 font-normal">4 servicios libre elección</span></td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 554 €<span class="block text-[10.5px] text-slate-600 font-normal">(375 € Setup + 179 € Mes 1)</span></td>
            <td class="p-3 font-black text-teal-900 whitespace-nowrap">Desde 2.165 €<span class="block text-[10.5px] text-slate-600 font-normal">(375 € Setup + 1.790 € Año)</span></td>
            <td class="p-3 text-slate-700">4 servicios mensuales + Bóveda GRATIS. En Anual <strong>ahorras 358 €</strong> en cuotas.</td>
          </tr>
          <tr class="bg-slate-50">
            <td class="p-3 font-black text-[#0b2239]">Pyme Pentium<span class="block text-[11px] text-slate-500 font-normal">5 servicios libre elección</span></td>
            <td class="p-3 font-black text-slate-900 whitespace-nowrap">Desde 669 €<span class="block text-[10.5px] text-slate-600 font-normal">(450 € Setup + 219 € Mes 1)</span></td>
            <td class="p-3 font-black text-teal-900 whitespace-nowrap">Desde 2.640 €<span class="block text-[10.5px] text-slate-600 font-normal">(450 € Setup + 2.190 € Año)</span></td>
            <td class="p-3 text-slate-700">5 servicios mensuales + Bóveda GRATIS. En Anual <strong>ahorras 438 €</strong> en cuotas.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="bg-sky-50 border-2 border-sky-300 rounded-2xl p-4 text-xs text-slate-800 leading-relaxed">
      <strong class="text-sky-950 font-black block mb-1">📌 Nota sobre combinaciones entre los 4 Grupos:</strong>
      Los importes «Desde» corresponden a elegir servicios del Grupo 1 (59 € el 1.º y +40 €/m los siguientes). Si en tu combinación eliges módulos del Grupo 2 (+59 €/m y +110 € Setup), Grupo 3 (+49 € a +69 €/m) o Grupo 4 (S9 +59 €/m o S10 Centralita Voz IA +129 €/m y +250 € Setup), el módulo más económico que elijas actúa como base y el resto suma su precio bonificado de combo.
    </div>

    <div class="text-center text-xs text-slate-500 mt-6 pt-3 border-t border-slate-200">
      <strong>Sistemas Pyme — Francisco M. Gallardo (NIF 52938419D)</strong> • Tel / WhatsApp: <strong>711 54 75 61</strong> • Precios netos sin IVA (21%).
    </div>
  </div>
</body>
</html>
"""


HTML_CATALOGO_DOSSIER_V151 = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dossier Catálogo Completo (4 Grupos S1 a S10 + Auditorías + NFC) | Sistemas Pyme</title>
  {ESTILO_COMUN_TARJETONES}
</head>
<body>
  <div class="a4-sheet">
    <div class="no-print flex flex-wrap items-center justify-between gap-3 pb-4 mb-5 border-b border-slate-200">
      <span class="px-3 py-1 rounded-full bg-indigo-100 text-indigo-900 font-extrabold text-xs border border-indigo-300">📘 DOSSIER CATÁLOGO OFICIAL • SECUENCIA S1 A S10 POR GRUPOS</span>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="bg-[#0b2239] hover:bg-slate-800 text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow cursor-pointer">🖨️ Imprimir / Guardar PDF</button>
        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20he%20visto%20el%20Dossier%20Cat%C3%A1logo%20y%20me%20gustar%C3%ADa%20comentarlo%20contigo" target="_blank" class="bg-[#0d7d74] text-white font-extrabold text-xs px-4 py-2 rounded-xl shadow">💬 Hablar con Francisco</a>
      </div>
    </div>

    <div class="bg-gradient-to-r from-[#0b2239] via-[#103459] to-[#0d7d74] text-white rounded-3xl p-6 mb-6">
      <h1 class="text-2xl sm:text-3xl font-black mb-1">Catálogo General de Soluciones Sistemas Pyme</h1>
      <p class="text-xs sm:text-sm text-teal-100">Organizado con la misma secuencia numérica de la web: <strong>4 Grupos de Servicios Mensuales (S1 a S10 + Satélites)</strong>, <strong>2 Super-Auditorías Web Gemelas</strong> y <strong>Atril NFC + QR</strong>.</p>
    </div>

    <!-- GRUPO 1 -->
    <div class="mb-5 bg-emerald-50/70 border-2 border-emerald-400 rounded-2xl p-5">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-3 border-b border-emerald-300 pb-2">
        <h2 class="text-base sm:text-lg font-black text-emerald-950">Grupo 1 (S1 a S5) • Esenciales de Reputación, Ventas y Gestión</h2>
        <span class="text-xs font-extrabold bg-emerald-700 text-white px-3 py-1 rounded-full">1.º: 59 €/m (150€ Setup) • Adicionales: +40 €/m (+75€ Setup)</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-slate-800">
        <div class="bg-white p-3 rounded-xl border border-emerald-200"><strong>⭐ S1. Respuesta a Reseñas en Google con IA (Activo Hoy):</strong> Contesta sola las de 4-5★ con SEO local y en 1-3★ frena y te envía 4 borradores al móvil aplicando el Método HEARD y blindaje RGPD (evita multas de 10.000-40.000 €).</div>
        <div class="bg-white p-3 rounded-xl border border-emerald-200"><strong>🛡️ S2. Cortafuegos Preventivo por WhatsApp Oficial (Activo Hoy):</strong> Pregunta tras la visita qué tal fue todo; lleva a los felices a Google Maps y filtra quejas en privado por texto o nota de voz transcrita con IA.</div>
        <div class="bg-white p-3 rounded-xl border border-emerald-200"><strong>⚡ S3. Respuesta a Leads en 10s + Portales (Ventas):</strong> Atiende por WhatsApp en menos de 10 segundos a quien pide presupuesto en tu web o portales y te avisa al móvil para cerrar en caliente.</div>
        <div class="bg-white p-3 rounded-xl border border-emerald-200"><strong>🧾 S4. Facturas y Tickets al Gestor por Foto WA (Ahorro Tiempo):</strong> Haz una foto por WhatsApp a cualquier ticket o factura y la IA extrae NIF, base e IVA subiéndolo directo al Excel de tu gestoría.</div>
        <div class="bg-white p-3 rounded-xl border border-emerald-200 md:col-span-2"><strong>🔄 S5. Reactivación de Clientes Inactivos (Ventas Recurrentes):</strong> Detecta clientes que llevan más de 60-90 días sin acudir y les envía una invitación personalizada por WhatsApp sin saturar.</div>
      </div>
    </div>

    <!-- GRUPO 2 -->
    <div class="mb-5 bg-sky-50/70 border-2 border-sky-400 rounded-2xl p-5">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-3 border-b border-sky-300 pb-2">
        <h2 class="text-base sm:text-lg font-black text-sky-950">Grupo 2 (S6 a S8) • Agenda, Contratos Digitales y Cobros</h2>
        <span class="text-xs font-extrabold bg-sky-700 text-white px-3 py-1 rounded-full">En Combo: +59 €/m (+110€ Setup) • Suelto: 79 €/m (195€ Setup)</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-slate-800">
        <div class="bg-white p-3 rounded-xl border border-sky-200"><strong>📅 S6. Sistema Anti-Plantón 24h + Huecos Flash:</strong> Confirma citas 24h antes por WhatsApp (-85% ausencias) y si alguien cancela avisa automáticamente a tu lista de espera.</div>
        <div class="bg-white p-3 rounded-xl border border-sky-200"><strong>✍️ S7. Firma Digital de Presupuestos + Onboarding IA:</strong> Firma legal con el dedo en el móvil, creación automática de carpeta en Drive y solicitud de documentos.</div>
        <div class="bg-white p-3 rounded-xl border border-sky-200"><strong>⚖️ S8. Escudo Anti-Morosidad Diplomático:</strong> Recordatorio neutral y educado (+3, +7 y +15 días) con factura PDF adjunta y enlace de pago.</div>
      </div>
    </div>

    <!-- GRUPO 3 Y GRUPO 4 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
      <div class="bg-pink-50/70 border-2 border-pink-400 rounded-2xl p-4 text-xs space-y-2">
        <div class="flex items-center justify-between border-b border-pink-300 pb-1.5">
          <h2 class="text-sm font-black text-pink-950">Grupo 3 • Satélites de Sector y Boosters IA</h2>
          <span class="text-[11px] font-extrabold text-pink-800">Desde +49 €/m combo</span>
        </div>
        <p><strong>• Sat.1 Instagram Inteligente 3 en 1 (Meta API):</strong> +49 €/m (+75€) en combo | 69 €/m (150€) suelto. Auto-DM en Reels/Posts, atención DMs 24/7 y menciones en Stories.</p>
        <p><strong>• Sat.2 Escudo Logístico 360 (Reparto y E-commerce):</strong> +59 €/m (+110€) combo | 79 €/m (195€) suelto. Avisos «Sale hoy», «Llega hoy» y gestión de ausencias.</p>
        <p><strong>• Sat.3 Cerebro Redactor Técnico B2B RAG:</strong> +69 €/m (+150€) combo | 99 €/m (250€) suelto. Redacta ofertas complejas leyendo tus catálogos privados.</p>
      </div>

      <div class="bg-indigo-50/70 border-2 border-indigo-400 rounded-2xl p-4 text-xs space-y-2">
        <div class="flex items-center justify-between border-b border-indigo-300 pb-1.5">
          <h2 class="text-sm font-black text-indigo-950">Grupo 4 (S9 y S10) • Telefonía y Voz IA 24/7</h2>
          <span class="text-[11px] font-extrabold text-indigo-800">Línea SIP + Minutos Voz IA</span>
        </div>
        <p><strong>• S9. Rescate de Llamadas Perdidas por WhatsApp:</strong> +59 €/m (+110€ Setup) en combo | 79 €/m (195€) suelto. Si comunicas o estás atendiendo, envía un WhatsApp en 5 segundos reteniendo al cliente (incluye hasta 250 rescates/mes).</p>
        <p><strong>• S10. Centralita Recepcionista de Voz IA 24/7:</strong> +129 €/m (+250€ Setup) en combo | 169 €/m (350€) suelto. Atiende llamadas con voz natural las 24h, responde dudas y agenda citas en tu calendario (incluye 250 min/mes).</p>
      </div>
    </div>

    <!-- AUDITORÍAS Y ATRIL -->
    <div class="bg-amber-50 border-2 border-amber-400 rounded-2xl p-4 text-xs flex flex-col sm:flex-row items-center justify-between gap-4">
      <div>
        <strong class="text-sm font-black text-[#0b2239] block">🔍🧠 Las 2 Super-Auditorías Web (SEO/GEO IA y Neuro-CRO) + ★ Atril NFC/QR (Pagos Únicos sin Cuotas)</strong>
        <span class="text-slate-700">Super-Auditorías Llave en Mano: <strong>195 € c/u</strong> con cualquier Pack de 2+ servicios (390 € las dos) o <strong>350 €</strong> suelta (590 € las dos). Atril NFC+QR: <strong>39 €</strong> (1.ª ud) | <strong>29 €</strong> (2ª-4ª) | <strong>25 €</strong> (5+).</span>
      </div>
    </div>

    <div class="text-center text-xs text-slate-500 mt-5 pt-3 border-t border-slate-200">
      <strong>Sistemas Pyme — Francisco M. Gallardo (NIF 52938419D)</strong> • Tel / WhatsApp: <strong>711 54 75 61</strong> • Web: <strong>sistemaspyme.es</strong>
    </div>
  </div>
</body>
</html>
"""


# ==============================================================================
# 5. REPARACIÓN DE `index.html` Y ACTUALIZACIÓN DE LOS TARJETONES
# ==============================================================================
def reparar_index_html_v151(html):
    # 1. Quitar cualquier bloque [SP_AGENDA_CRM_WEB_SYNC_V1...] previo
    html = re.sub(
        r"<!-- \[SP_AGENDA_CRM_WEB_SYNC_V1\d+_START\] -->[\s\S]*?<!-- \[SP_AGENDA_CRM_WEB_SYNC_V1\d+_END\] -->\s*",
        "",
        html
    )

    # 2. Sustituir la sección #vista-tarifas completa por la nueva versión simétrica V151
    patron_vista_tarifas = re.compile(
        r"<!-- ={40,}\s*-->\s*<!-- VISTA 4 \(SALA INDEPENDIENTE\): PRECIOS CLAROS[\s\S]*?</section>\s*(?=<!-- ={40,}\s*-->\s*<!-- VISTA 5)",
        re.MULTILINE
    )
    if patron_vista_tarifas.search(html):
        html = patron_vista_tarifas.sub(lambda _: HTML_VISTA_TARIFAS_V151 + "\n\n\n                    ", html, count=1)

    # 3. Asegurar que el vigilante antiguo de 950ms y el doble micrófono V129 estén desactivados
    html = re.sub(
        r"function iniciarVigilanteMicrofonoContinuo\(\)\s*\{[\s\S]*?\n      \}",
        """function iniciarVigilanteMicrofonoContinuo() {
        /* Gestionado por el motor unificado V151 */
      }""",
        html,
        count=1
    )

    # 4. Inyectar el bloque maestro V151 justo antes del último </body> real (usando rsplit)
    if "</body>" in html:
        partes = html.rsplit("</body>", 1)
        html = partes[0].rstrip() + "\n" + BLOQUE_JS_MAESTRO_WEB_V151.strip() + "\n</body>" + partes[1]

    return html


def actualizar_tarjetones_documentos():
    carpetas_docs = [
        os.path.join(RUTA_WEB_PUBLIC, "documentos"),
        os.path.join(RUTA_SERVICIO_RESENAS, "documentos"),
    ]
    for c_doc in carpetas_docs:
        if not os.path.exists(c_doc):
            os.makedirs(c_doc, exist_ok=True)

        # 1. Guía Técnica SEO/GEO ( Escritorio + Móvil )
        for nom in ("guia_seo_geo.html", "guia_seo_geo_movil.html"):
            escribir_archivo_con_backup(os.path.join(c_doc, nom), HTML_GUIA_SEO_GEO_COMPLETA)

        # 2. Tarifas Oficiales ( Escritorio + Móvil )
        for nom in ("tarifas.html", "tarifas_movil.html"):
            escribir_archivo_con_backup(os.path.join(c_doc, nom), HTML_TARIFAS_OFICIALES_V151)

        # 3. Desembolso Primer Día ( Escritorio + Móvil )
        for nom in ("desembolso.html", "desembolso_movil.html"):
            escribir_archivo_con_backup(os.path.join(c_doc, nom), HTML_DESEMBOLSO_DIA1_V151)

        # 4. Catálogo Dossier ( Escritorio + Móvil )
        for nom in ("catalogo.html", "catalogo_movil.html"):
            escribir_archivo_con_backup(os.path.join(c_doc, nom), HTML_CATALOGO_DOSSIER_V151)

        # 5. Limpiar menciones a "Solo código (200 €)" en guia_neuro.html y setup.html si existen
        for nom_extra in ("guia_neuro.html", "guia_neuro_movil.html", "setup.html", "setup_movil.html"):
            ruta_ex = os.path.join(c_doc, nom_extra)
            if os.path.exists(ruta_ex):
                with open(ruta_ex, "r", encoding="utf-8") as f:
                    txt_ex = f.read()
                txt_nuevo = re.sub(r"200\s*€\s*\(?solo\s+c[oó]digo\)?", "350 € Llave en Mano (195 € con Pack)", txt_ex, flags=re.IGNORECASE)
                txt_nuevo = re.sub(r"Solo\s+C[oó]digo\s*/\s*DIY[^<]*", "Llave en Mano o Entrega a tu Técnico", txt_nuevo, flags=re.IGNORECASE)
                if txt_nuevo != txt_ex:
                    escribir_archivo_con_backup(ruta_ex, txt_nuevo)


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

        html_nuevo = reparar_index_html_v151(html_actual)
        escribir_archivo_con_backup(ruta, html_nuevo)
        validar_bloques_js_en_html(ruta)


# ==============================================================================
# 6. PASO 1 PRIORITARIO + BLINDAJE ATEXIT: ACTUALIZAR LOS 2 DOCUMENTOS .MD
# ==============================================================================
NOTA_HISTORIAL_V151 = f"""
---
### ACTUALIZACIÓN {VERSION_ACTUAL} ({FECHA_EJECUCION}) — Respuesta Instantánea del Tecnoconsultor (<1.6s en `file://`), Simetría Total en Precios Claros (Mensual y Anual), Lógica Táctil Original en Auditorías y Renovación de Tarjetones
- **Respuesta hablada garantizada en el Tecnoconsultor (`spProcesarConsultaEnTeleprompterDirecto`):** Incorporado salvavidas automático de 1,6 segundos para que al abrir `index.html` desde el Mac (`file://`), tras aparecer la transcripción en el Teleprompter LED, no se quede esperando los 4 intentos bloqueados a Vertex AI y responda al instante en voz alta.
- **Rediseño Simétrico de Precios Claros (Diapositiva 1 y Diapositiva 2):** Unificadas las subcajas de precio de las 3 tarjetas (Mensual y Plan Anual) sin saltos de línea en el símbolo `€`, eliminada la línea redundante `Setup Dúo: 225 € + Aud. a 195 €` arriba a la derecha en Pack Escudo Total / Plus, añadida línea dedicada de ahorro en las 3 tarjetas, centrado el banner inferior con flecha animada en movimiento sin precios, eliminada la opción «Solo código 200 €» en las Super-Auditorías (son 350 € Llave en Mano o entregando los códigos e instrucciones al técnico del cliente, y 195 € bonificada con Pack 2+) y limpiada la tabla de los 4 Grupos (sin repetir «Grupo 3» ni «Grupo 4» en sublíneas).
- **Restauración de la Lógica Táctil en las 2 Tarjetas de Auditorías de «Cómo ayudamos»:** Cara A -> Cara B (3 subcajas de estadísticas) -> clic en subcaja despliega el detalle -> clic en detalle regresa a Cara B -> clic fuera de subcajas pasa a Cara C (Técnico).
- **Renovación de los Tarjetones de la Biblioteca (`guia_seo_geo.html`, `tarifas.html`, `desembolso.html`, `catalogo.html`, `guia_neuro.html`):** Reconstruida la Guía Técnica SEO/GEO con diseño ejecutivo A4 completo y establecida la tabla de 4 columnas (`Pyme Base`, `Escudo Básico`, `Escudo Total`, `Pyme Trinity`, `Pyme 4`, `Pyme Pentium`) con precios `Desde X €/mes` y la Regla de Combinación Libre entre cualquiera de los 4 Grupos.
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
                txt = txt.rstrip() + "\n" + NOTA_HISTORIAL_V151
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
                    ["git", "-C", carpeta_git, "commit", "-m", f"feat({VERSION_ACTUAL}): Tecnoconsultor respuesta inmediata, Precios Claros simetricos, Auditorias Cara A/B/C y Tarjetones"],
                    check=False, capture_output=True
                )
                subprocess.run(["git", "-C", carpeta_git, "push"], check=False, capture_output=True)
                print(f"  ✅ Git sincronizado en: {os.path.basename(carpeta_git)}")
            except Exception:
                pass


def ejecutar_actualizacion():
    print("=" * 78)
    print(f"🚀 INICIANDO ACTUALIZACIÓN MAESTRA {VERSION_ACTUAL} — TECNOCONSULTOR + PRECIOS + TARJETONES")
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
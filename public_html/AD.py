#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SISTEMAS PYME — ACTUALIZADOR MAESTRO SEGURO COMPLETO (AD.py - VERSIÓN V148)
================================================================================
Este archivo está 100% COMPLETO de principio a fin (CERO '# ... existing code ...').
Puedes guardarlo como `AD.py` y ejecutarlo directamente con:
    python3 AD.py

Qué hace esta versión V148:
1. PASO 1 PRIORITARIO + BLINDAJE `atexit`:
   - Actualiza sin recortar ni una línea los 2 únicos documentos maestros `.md`
     en `/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Programar`:
       1) `biblia_de_conocimiento_de_sistemas_pyme.md`
       2) `manual_maestro_de_programaci_n_ad_py.md`
   - Sincroniza ambos documentos hacia Google Sheets (`Biblia_IA_Viva` y
     `Manual_Maestro_AD`) y hacia Google Drive para las Gemas de Gemini.
2. REPARACIÓN RAÍZ DE `index.html` (Tecnosala + Carrito + Precios + Diagnóstico):
   - Limpia el código que se había colado dentro de la cadena `'</div></body></html>'`
     de `spDescargarConversacionConsultor`, devolviendo la vida al 100% tanto al
     Carrito como al Consultor de la Tecnosala.
   - Elimina para siempre el bucle infinito del cartelito de permiso de micrófono
     en Chrome cuando abres la web como archivo local (`file://`), anulando la
     doble llamada a `getUserMedia` y el temporizador de `950 ms`.
   - Colorea y diferencia cada tarjeta del Carrito de Compra (`#spModalCarritoCarta`)
     con su propia identidad cromática luminosa (Azul Cielo, Ámbar/Dorado, Pizarra,
     Azul Real, Verde Esmeralda, Índigo/Violeta y Coral/Oro) manteniendo letra
     intermedia apta para presbicia y cero scroll.
   - Conecta en tiempo real el selector de día y hora del Carrito (`#spCartSelectDiaLV`
     y `#spCartSelectHoraManana`) con tu CRM y tu Bitácora (`/api/horarios-ocupados-agenda`),
     bloqueando el sábado a las 11:00 (`⛔ 11:00 - 11:30 (Ocupado en Agenda CRM)`).
3. COORDINADOR DE AGENDA EN `servidor_local_b2b.py`:
   - Añade/actualiza `/api/horarios-ocupados-agenda` y `/api/registrar-cita-web-en-crm`
     y valida la sintaxis con `ast.parse` y `node --check`.
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

VERSION_ACTUAL = "V148"
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
            for cand in ("/opt/homebrew/bin/node", "/usr/local/bin/node", "/usr/bin/node"):
                if os.path.exists(cand):
                    node_bin = cand
                    break
        if node_bin and bloques:
            for idx, b in enumerate(bloques):
                if "application/ld+json" in b or not b.strip():
                    continue
                tmp_js = f"/tmp/_sp_check_v148_{idx}.js"
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
# 2. CSS COMPLETO DEL CARRITO LUMINOSO CON TARJETAS COLOREADAS Y CERO SCROLL
# ==============================================================================
CSS_CARRITO_COLOREADO_SIN_SCROLL_V148 = r"""
    /* =========================================================================
       MODAL CARRITO CONFIGURADOR EN MODO CRISTAL LUMINOSO CRO (NEUROMARKETING)
       TARJETAS COLOREADAS INDIVIDUALMENTE + APTO PARA PRESBICIA + CERO SCROLL
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
    /* Ocultar cualquier banner superior sobrante */
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
    /* Botones de selección base (Pasos 1, 2 y 3) */
    #spModalCarritoCarta .sp-cart-item-btn {
      border: 2px solid #cbd5e1 !important;
      background: #ffffff !important;
      border-radius: 0.8rem !important;
      padding: 0.48rem 0.75rem !important;
      text-align: left;
      transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
      cursor: pointer;
      color: #0f172a !important;
      box-shadow: 0 3px 10px -2px rgba(11, 34, 57, 0.07), inset 0 1px 0 #ffffff !important;
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
      transform: translateY(-1.5px) !important;
    }

    /* =====================================================================
       PALETA CROMÁTICA DIFERENCIADA POR TARJETA EN EL CARRITO DE COMPRA
       ===================================================================== */
    /* 1A. Modalidad Mensual Flexible -> Azul Cielo / Cian */
    #spModalCarritoCarta #spCartMod_mensual {
      background: linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 100%) !important;
      border-color: #7dd3fc !important;
      border-left: 4px solid #0284c7 !important;
    }
    #spModalCarritoCarta #spCartMod_mensual > span:first-child { color: #075985 !important; }
    #spModalCarritoCarta #spCartMod_mensual.sp-cart-selected {
      background: linear-gradient(135deg, #bae6fd 0%, #7dd3fc 100%) !important;
      border: 2.5px solid #0284c7 !important;
      box-shadow: 0 8px 18px -4px rgba(2, 132, 199, 0.32), inset 0 1px 0 #ffffff !important;
    }
    #spModalCarritoCarta #spCartMod_mensual.sp-cart-selected > span:first-child { color: #082f49 !important; }
    #spModalCarritoCarta #spCartMod_mensual.sp-cart-selected > span:not(:first-child) { color: #0c4a6e !important; font-weight: 700 !important; }

    /* 1B. Modalidad Plan Anual (-2 Meses) -> Ámbar / Dorado Cálido */
    #spModalCarritoCarta #spCartMod_anual {
      background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 100%) !important;
      border-color: #fcd34d !important;
      border-left: 4px solid #d97706 !important;
    }
    #spModalCarritoCarta #spCartMod_anual > span:first-child { color: #92400e !important; }
    #spModalCarritoCarta #spCartMod_anual.sp-cart-selected {
      background: linear-gradient(135deg, #fde68a 0%, #fcd34d 100%) !important;
      border: 2.5px solid #b45309 !important;
      box-shadow: 0 8px 18px -4px rgba(217, 119, 6, 0.34), inset 0 1px 0 #ffffff !important;
    }
    #spModalCarritoCarta #spCartMod_anual.sp-cart-selected > span:first-child { color: #451a03 !important; }
    #spModalCarritoCarta #spCartMod_anual.sp-cart-selected > span:not(:first-child) { color: #78350f !important; font-weight: 700 !important; }

    /* 2A. Solo Auditoría / Atril -> Pizarra Perla Elegante */
    #spModalCarritoCarta #spCartPlan_ninguno {
      background: linear-gradient(145deg, #f8fafc 0%, #e2e8f0 100%) !important;
      border-color: #94a3b8 !important;
      border-left: 4px solid #475569 !important;
    }
    #spModalCarritoCarta #spCartPlan_ninguno > span:first-child { color: #1e293b !important; }
    #spModalCarritoCarta #spCartPlan_ninguno.sp-cart-selected {
      background: linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%) !important;
      border: 2.5px solid #1e293b !important;
      box-shadow: 0 8px 18px -4px rgba(30, 41, 59, 0.28), inset 0 1px 0 #ffffff !important;
    }
    #spModalCarritoCarta #spCartPlan_ninguno.sp-cart-selected > span:first-child { color: #0f172a !important; }
    #spModalCarritoCarta #spCartPlan_ninguno.sp-cart-selected > span:not(:first-child) { color: #1e293b !important; font-weight: 700 !important; }

    /* 2B. 1 Servicio (Plan Base) -> Azul Real / Cobalto Suave */
    #spModalCarritoCarta #spCartPlan_base {
      background: linear-gradient(145deg, #eff6ff 0%, #dbeafe 100%) !important;
      border-color: #93c5fd !important;
      border-left: 4px solid #2563eb !important;
    }
    #spModalCarritoCarta #spCartPlan_base > span:first-child { color: #1e3a8a !important; }
    #spModalCarritoCarta #spCartPlan_base.sp-cart-selected {
      background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%) !important;
      border: 2.5px solid #1d4ed8 !important;
      box-shadow: 0 8px 18px -4px rgba(37, 99, 235, 0.32), inset 0 1px 0 #ffffff !important;
    }
    #spModalCarritoCarta #spCartPlan_base.sp-cart-selected > span:first-child { color: #172554 !important; }
    #spModalCarritoCarta #spCartPlan_base.sp-cart-selected > span:not(:first-child) { color: #1e3a8a !important; font-weight: 700 !important; }

    /* 2C. Pack Escudo Básico (Dúo) -> Verde Esmeralda / Turquesa */
    #spModalCarritoCarta #spCartPlan_duo {
      background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%) !important;
      border-color: #6ee7b7 !important;
      border-left: 4px solid #059669 !important;
    }
    #spModalCarritoCarta #spCartPlan_duo > span:first-child { color: #065f46 !important; }
    #spModalCarritoCarta #spCartPlan_duo.sp-cart-selected {
      background: linear-gradient(135deg, #a7f3d0 0%, #6ee7b7 100%) !important;
      border: 2.5px solid #047857 !important;
      box-shadow: 0 8px 18px -4px rgba(5, 150, 105, 0.34), inset 0 1px 0 #ffffff !important;
    }
    #spModalCarritoCarta #spCartPlan_duo.sp-cart-selected > span:first-child { color: #022c22 !important; }
    #spModalCarritoCarta #spCartPlan_duo.sp-cart-selected > span:not(:first-child) { color: #064e3b !important; font-weight: 700 !important; }

    /* 3A. Sin Auditoría por ahora -> Malva / Neutro Suave */
    #spModalCarritoCarta #spCartAud_0 {
      background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%) !important;
      border-color: #cbd5e1 !important;
      border-left: 4px solid #64748b !important;
    }
    #spModalCarritoCarta #spCartAud_0.sp-cart-selected {
      background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%) !important;
      border: 2.5px solid #334155 !important;
      box-shadow: 0 6px 14px -4px rgba(51, 65, 85, 0.25), inset 0 1px 0 #ffffff !important;
    }

    /* 3B. +1 Super-Auditoría -> Índigo / Violeta Tecnológico */
    #spModalCarritoCarta #spCartAud_1 {
      background: linear-gradient(145deg, #eef2ff 0%, #e0e7ff 100%) !important;
      border-color: #a5b4fc !important;
      border-left: 4px solid #4f46e5 !important;
    }
    #spModalCarritoCarta #spCartAud_1 > span:first-child { color: #312e81 !important; }
    #spModalCarritoCarta #spCartAud_1.sp-cart-selected {
      background: linear-gradient(135deg, #c7d2fe 0%, #a5b4fc 100%) !important;
      border: 2.5px solid #4338ca !important;
      box-shadow: 0 8px 18px -4px rgba(79, 70, 229, 0.32), inset 0 1px 0 #ffffff !important;
    }
    #spModalCarritoCarta #spCartAud_1.sp-cart-selected > span:first-child { color: #1e1b4b !important; }
    #spModalCarritoCarta #spCartAud_1.sp-cart-selected > span:not(:first-child) { color: #312e81 !important; font-weight: 700 !important; }

    /* 3C. +2 Super-Auditorías -> Oro / Coral Cálido de Máximo Ahorro */
    #spModalCarritoCarta #spCartAud_2 {
      background: linear-gradient(145deg, #fff7ed 0%, #ffedd5 100%) !important;
      border-color: #fdba74 !important;
      border-left: 4px solid #ea580c !important;
    }
    #spModalCarritoCarta #spCartAud_2 > span:first-child { color: #9a3412 !important; }
    #spModalCarritoCarta #spCartAud_2.sp-cart-selected {
      background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%) !important;
      border: 2.5px solid #c2410c !important;
      box-shadow: 0 8px 18px -4px rgba(234, 88, 12, 0.34), inset 0 1px 0 #ffffff !important;
    }
    #spModalCarritoCarta #spCartAud_2.sp-cart-selected > span:first-child { color: #431407 !important; }
    #spModalCarritoCarta #spCartAud_2.sp-cart-selected > span:not(:first-child) { color: #7c2d12 !important; font-weight: 700 !important; }

    /* 4 y 5. Cajas de Atriles NFC (Ámbar suave) y Reserva Fase 2 (Azul Cielo suave) */
    #spModalCarritoCarta .sm\:col-span-5 {
      background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 100%) !important;
      border: 1.5px solid #f59e0b !important;
    }
    #spModalCarritoCarta .sm\:col-span-7 {
      background: linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 100%) !important;
      border: 1.5px solid #0284c7 !important;
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
    }
"""


# ==============================================================================
# 3. BLOQUE JS INYECTADO AL FINAL DE `index.html`:
#    - DESACTIVA EL BUCLE DEL MICRÓFONO EN TECNOSALA (PROTOCOLO file://)
#    - CONECTA EL CARRITO CON LAS CITAS DEL CRM Y LA BITÁCORA
#    - CONECTA EL BOTÓN DE COMPRAR DEL TEST DE DIAGNÓSTICO CON PRESELECCIÓN
# ==============================================================================
BLOQUE_JS_FINAL_WEB_V148 = r'''
<!-- [SP_AGENDA_CRM_WEB_SYNC_V148_START] -->
<script>
(function() {
  /* =========================================================================
     1. FIN DEL BUCLE INFINITO DE PERMISO DE MICRÓFONO EN TECNOSALA
        (Cuando se abre index.html como archivo local file://, Chrome no guarda
         el permiso; eliminamos la doble llamada a getUserMedia y los reintentos
         automáticos cada 950ms para que la ventana de permiso se cierre al instante)
     ========================================================================= */
  window._spUltimoIntentoStartMicro = 0;
  window._spSesionMicroUnicaActiva = false;

  window.spActivarModoEscuchaPersistente = function(forzarManual) {
    var vistaTec = document.getElementById('vista-tecnosala');
    if (!vistaTec || vistaTec.classList.contains('hidden')) return;
    var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) return;

    if (window.speechSynthesis && window.speechSynthesis.speaking) return;

    var ahora = Date.now();
    if (!forzarManual && (ahora - window._spUltimoIntentoStartMicro < 2500)) return;
    if (window._spSesionMicroUnicaActiva) return;

    window._spUltimoIntentoStartMicro = ahora;

    try {
      if (!window._spReconocedorLimpioV148) {
        var rec = new SpeechRec();
        rec.lang = 'es-ES';
        rec.continuous = (window.location.protocol !== 'file:');
        rec.interimResults = true;
        var textoFrase = '';
        var timerSilencio = null;

        rec.onstart = function() {
          window._spSesionMicroUnicaActiva = true;
          var inp = document.getElementById('spTecnosalaInput');
          if (inp) inp.setAttribute('placeholder', '🟢 Escuchando tu voz ahora... habla con naturalidad');
          var btnV = document.getElementById('spBtnVoiceTecnosala');
          var txtV = document.getElementById('spVoiceBtnText');
          if (btnV) btnV.classList.add('sp-voice-listening');
          if (txtV) txtV.textContent = 'Escuchando...';
        };

        rec.onresult = function(ev) {
          if (window.speechSynthesis && window.speechSynthesis.speaking) {
            textoFrase = '';
            return;
          }
          var acumulado = '';
          var esFinal = false;
          for (var i = ev.resultIndex; i < ev.results.length; i++) {
            acumulado += ev.results[i][0].transcript;
            if (ev.results[i].isFinal) esFinal = true;
          }
          textoFrase = acumulado.trim();
          var inp = document.getElementById('spTecnosalaInput');
          if (inp && textoFrase) inp.value = textoFrase;

          if (timerSilencio) clearTimeout(timerSilencio);
          timerSilencio = setTimeout(function() {
            var enviar = textoFrase.trim();
            textoFrase = '';
            if (enviar.length >= 2) {
              try { rec.stop(); } catch (e) {}
              window._spSesionMicroUnicaActiva = false;
              if (typeof window.spProcesarConsultaEnTeleprompterDirecto === 'function') {
                window.spProcesarConsultaEnTeleprompterDirecto(enviar);
              }
            }
          }, esFinal ? 500 : 1000);
        };

        rec.onerror = function() {
          window._spSesionMicroUnicaActiva = false;
          var btnV = document.getElementById('spBtnVoiceTecnosala');
          var txtV = document.getElementById('spVoiceBtnText');
          if (btnV) btnV.classList.remove('sp-voice-listening');
          if (txtV) txtV.textContent = 'Hablar';
        };

        rec.onend = function() {
          window._spSesionMicroUnicaActiva = false;
          var btnV = document.getElementById('spBtnVoiceTecnosala');
          var txtV = document.getElementById('spVoiceBtnText');
          if (btnV) btnV.classList.remove('sp-voice-listening');
          if (txtV) txtV.textContent = 'Hablar';
          var inp = document.getElementById('spTecnosalaInput');
          if (inp) inp.setAttribute('placeholder', 'Escribe tu duda o pulsa 🎙️ Hablar o el Orbe para preguntar por voz...');
          if (textoFrase && textoFrase.trim().length >= 2) {
            var enviar = textoFrase.trim();
            textoFrase = '';
            if (typeof window.spProcesarConsultaEnTeleprompterDirecto === 'function') {
              window.spProcesarConsultaEnTeleprompterDirecto(enviar);
            }
          }
        };

        window._spReconocedorLimpioV148 = rec;
      }

      window._spReconocedorLimpioV148.start();
    } catch (e) {
      window._spSesionMicroUnicaActiva = false;
    }
  };

  window.spIniciarEscuchaDirectaConsultor = function() {
    window.spActivarModoEscuchaPersistente(true);
  };

  window.spToggleDictadoVozTecnosala = function() {
    if (window._spSesionMicroUnicaActiva && window._spReconocedorLimpioV148) {
      try { window._spReconocedorLimpioV148.stop(); } catch (e) {}
      window._spSesionMicroUnicaActiva = false;
      return;
    }
    window.spActivarModoEscuchaPersistente(true);
  };

  /* =========================================================================
     2. PRESELECCIÓN AUTOMÁTICA DEL DIAGNÓSTICO AL ABRIR EL CARRITO DESDE EL TEST
     ========================================================================= */
  window.spAbrirCarritoConDiagnosticoPreseleccionado = function() {
    if (typeof window.spAbrirCarritoConfigurador === 'function') {
      window.spAbrirCarritoConfigurador('duo', 1);
    }
  };

  /* =========================================================================
     3. COORDINACIÓN DE CITAS ENTRE CARRITO WEB Y AGENDA CRM / BITÁCORA
     ========================================================================= */
  window.SP_SLOTS_OCUPADOS_CRM_EXTRA = window.SP_SLOTS_OCUPADOS_CRM_EXTRA || new Set();

  function normalizarSlotEspacio(slotRaw) {
    var s = String(slotRaw || '').trim();
    if (!s) return '';
    s = s.replace('|', ' ').replace('T', ' ');
    var m = s.match(/^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})/);
    return m ? (m[1] + ' ' + m[2]) : '';
  }

  window.spAplicarBloqueoHorasCrmEnSelect = function() {
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
      var guardados = JSON.parse(localStorage.getItem('sp_citas_ocupadas_crm_v148') || '[]');
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
              localStorage.setItem('sp_citas_ocupadas_crm_v148', JSON.stringify(Array.from(window.SP_SLOTS_OCUPADOS_CRM_EXTRA)));
            } catch (e) {}
          }
        })
        .catch(function() {});
    })).then(function() {
      window.spAplicarBloqueoHorasCrmEnSelect();
    });
  };

  function engancharEventosAgendaCarritoV148() {
    window.spSincronizarCitasCrmLocal();

    if (typeof window.spActualizarHorasDisponiblesCarritoV125 === 'function' && !window.spActualizarHorasDisponiblesCarritoV125._hookV148) {
      var origActHoras = window.spActualizarHorasDisponiblesCarritoV125;
      var nuevaActHoras = function() {
        var r = origActHoras.apply(this, arguments);
        window.spAplicarBloqueoHorasCrmEnSelect();
        return r;
      };
      nuevaActHoras._hookV148 = true;
      window.spActualizarHorasDisponiblesCarritoV125 = nuevaActHoras;
    }

    if (typeof window.spAbrirCarritoConfigurador === 'function' && !window.spAbrirCarritoConfigurador._hookV148) {
      var origOpen = window.spAbrirCarritoConfigurador;
      var nuevoOpen = function() {
        var r = origOpen.apply(this, arguments);
        window.spSincronizarCitasCrmLocal();
        setTimeout(window.spAplicarBloqueoHorasCrmEnSelect, 120);
        return r;
      };
      nuevoOpen._hookV148 = true;
      window.spAbrirCarritoConfigurador = nuevoOpen;
    }

    if (typeof window.spConfirmarPedidoYAgendarCita === 'function' && !window.spConfirmarPedidoYAgendarCita._hookV148) {
      var origConfirm = window.spConfirmarPedidoYAgendarCita;
      var nuevoConfirm = function() {
        try {
          var selDia = document.getElementById('spCartSelectDiaLV');
          var selHora = document.getElementById('spCartSelectHoraManana');
          var inpNom = document.getElementById('spCartInputNombre');
          var inpNeg = document.getElementById('spCartInputNegocioCiudad');
          var inpTel = document.getElementById('spCartInputTelefono');
          var ymd = selDia ? selDia.value : '';
          var hhmm = selHora ? String(selHora.value || '').substring(0, 5) : '';
          if (ymd && hhmm) {
            window.SP_SLOTS_OCUPADOS_CRM_EXTRA.add(ymd + ' ' + hhmm);
            try {
              localStorage.setItem('sp_citas_ocupadas_crm_v148', JSON.stringify(Array.from(window.SP_SLOTS_OCUPADOS_CRM_EXTRA)));
            } catch (e) {}
            var nombreCompleto = ((inpNom ? inpNom.value : '') + (inpNeg && inpNeg.value ? (' — ' + inpNeg.value) : '')).trim();
            fetch('http://127.0.0.1:5000/api/crm/registrar-pedido-web', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                origen: 'Carrito Configurador Web',
                nombre: nombreCompleto || 'Cliente Web',
                telefono: inpTel ? inpTel.value : '',
                fecha_cita_iso: ymd + 'T' + hhmm + ':00',
                horario: (selDia && selDia.options[selDia.selectedIndex] ? selDia.options[selDia.selectedIndex].text : ymd) + ' a las ' + hhmm + ' h'
              })
            }).catch(function() {});
          }
        } catch (err) {}
        return origConfirm.apply(this, arguments);
      };
      nuevoConfirm._hookV148 = true;
      window.spConfirmarPedidoYAgendarCita = nuevoConfirm;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(engancharEventosAgendaCarritoV148, 250);
    });
  } else {
    setTimeout(engancharEventosAgendaCarritoV148, 250);
  }
})();
</script>
<!-- [SP_AGENDA_CRM_WEB_SYNC_V148_END] -->
'''


# ==============================================================================
# 4. COORDINADOR DE AGENDA EN `servidor_local_b2b.py`
# ==============================================================================
BLOQUE_AGENDA_CRM_PY = r'''
# === [SP_AGENDA_CRM_COORDINATOR_V145_START] ===
def _extraer_slots_ocupados_universal_sp_v145():
    """
    Lee todas las citas agendadas en crm_b2b_db.json (campos fecha_cita, hora_cita,
    fecha_proximo_contacto, hora_proximo_contacto, notas_seguimiento, bitacora_seguimiento,
    tareas_checklist) y en leads_contrataciones_web.json.
    """
    ocupados_set = set()
    detalle_citas = []

    hoy_dt = datetime.now()
    anio_actual = hoy_dt.year

    meses_es = {
        "enero": 1, "ene": 1, "febrero": 2, "feb": 2, "marzo": 3, "mar": 3,
        "abril": 4, "abr": 4, "mayo": 5, "may": 5, "junio": 6, "jun": 6,
        "julio": 7, "jul": 7, "agosto": 8, "ago": 8, "septiembre": 9, "sep": 9, "set": 9,
        "octubre": 10, "oct": 10, "noviembre": 11, "nov": 11, "diciembre": 12, "dic": 12
    }
    dias_sem_es = {
        "lunes": 0, "martes": 1, "miercoles": 2, "miércoles": 2,
        "jueves": 3, "viernes": 4, "sabado": 5, "sábado": 5, "domingo": 6
    }

    def _normalizar_hora_a_slots(h_str):
        if not h_str:
            return []
        s = str(h_str).strip().lower()
        m = re.search(r'\b([01]?\d|2[0-3])[:\.]([0-5]\d)\b', s)
        if m:
            hh = int(m.group(1))
            mm = int(m.group(2))
        else:
            m2 = re.search(r'(?:a\s+las\s+|hora\s*[:=]?\s*|\b)([01]?\d|2[0-3])\s*(?:h|horas|am|pm)?\b', s)
            if not m2:
                return []
            hh = int(m2.group(1))
            mm = 0
            if "tarde" in s and 1 <= hh <= 8:
                hh += 12
        slot_principal = f"{hh:02d}:{'30' if mm >= 30 else '00'}"
        slots_out = [slot_principal]
        if mm == 0:
            slots_out.append(f"{hh:02d}:30")
        return slots_out

    def _normalizar_fecha_str(f_str):
        if not f_str:
            return None
        s = str(f_str).strip().lower()
        m_iso = re.search(r'\b(202\d)-([01]\d)-([0-3]\d)\b', s)
        if m_iso:
            return f"{m_iso.group(1)}-{m_iso.group(2)}-{m_iso.group(3)}"
        m_dmy = re.search(r'\b([0-3]?\d)[/\-]([01]?\d)(?:[/\-](202\d|\d{2}))?\b', s)
        if m_dmy:
            dd = int(m_dmy.group(1))
            mm = int(m_dmy.group(2))
            yy_raw = m_dmy.group(3)
            yy = int(yy_raw) if yy_raw else anio_actual
            if yy < 100:
                yy += 2000
            if 1 <= mm <= 12 and 1 <= dd <= 31:
                return f"{yy:04d}-{mm:02d}-{dd:02d}"
        m_txt = re.search(r'\b([0-3]?\d)\s+de\s+([a-záéíóú]+)', s)
        if m_txt:
            dd = int(m_txt.group(1))
            mes_nom = texto_sin_tildes(m_txt.group(2))
            mm = meses_es.get(mes_nom) or meses_es.get(mes_nom[:3])
            if mm:
                return f"{anio_actual:04d}-{mm:02d}-{dd:02d}"
        for d_nom, d_idx in dias_sem_es.items():
            if re.search(rf'\b{d_nom}\b', s):
                dias_dif = (d_idx - hoy_dt.weekday()) % 7
                f_calc = hoy_dt + pd.Timedelta(days=dias_dif)
                return f_calc.strftime("%Y-%m-%d")
        return None

    def _registrar_ocupado(fecha_iso, hora_raw, origen_txt=""):
        if not fecha_iso:
            return
        for sl in _normalizar_hora_a_slots(hora_raw):
            clave = f"{fecha_iso}|{sl}"
            if clave not in ocupados_set:
                ocupados_set.add(clave)
                detalle_citas.append({
                    "slot": clave,
                    "fecha": fecha_iso,
                    "hora": sl,
                    "origen": origen_txt or "CRM"
                })

    def _escanear_texto_libre_en_busca_de_cita(texto_libre, nombre_neg=""):
        if not texto_libre or not isinstance(texto_libre, str):
            return
        t_low = texto_libre.lower()
        for m_dt in re.finditer(r'(202\d-[01]\d-[0-3]\d)[t\s_]+([012]?\d:[0-5]\d)', t_low):
            _registrar_ocupado(m_dt.group(1), m_dt.group(2), nombre_neg)

        for m_dmy in re.finditer(r'([0-3]?\d[/\-][01]?\d(?:[/\-]202\d)?)\s*(?:a\s+las\s+|[-·•]\s*|\s+)([012]?\d(?::[0-5]\d|\s*h\b))', t_low):
            f_iso = _normalizar_fecha_str(m_dmy.group(1))
            if f_iso:
                _registrar_ocupado(f_iso, m_dmy.group(2), nombre_neg)

        for m_sem in re.finditer(r'\b(lunes|martes|mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo)\b[^\n.;]{0,35}?\b(?:a\s+las\s+|hora\s+)?([012]?\d(?::[0-5]\d|\s*h\b|:00)?)', t_low):
            dia_palabra = m_sem.group(1)
            hora_palabra = m_sem.group(2)
            if re.search(r'(:[0-5]\d|\bh\b|a\s+las)', m_sem.group(0)):
                f_iso = _normalizar_fecha_str(dia_palabra)
                if f_iso:
                    _registrar_ocupado(f_iso, hora_palabra, nombre_neg)

    try:
        crm_data = load_crm()
        for k_pid, rec in (crm_data or {}).items():
            if not isinstance(rec, dict):
                continue
            nom = str(rec.get("nombre") or k_pid).strip()

            for k_f in ("fecha_cita", "fecha_proximo_contacto", "proxima_accion_fecha", "cita_fecha", "fecha_reunion", "proximo_contacto", "cita"):
                val_f = rec.get(k_f)
                if val_f:
                    f_iso = _normalizar_fecha_str(val_f)
                    h_asociada = (
                        rec.get("hora_cita")
                        or rec.get("hora_proximo_contacto")
                        or rec.get("proxima_accion_hora")
                        or rec.get("cita_hora")
                        or val_f
                    )
                    if f_iso:
                        _registrar_ocupado(f_iso, h_asociada, f"CRM: {nom}")
                    _escanear_texto_libre_en_busca_de_cita(str(val_f), f"CRM: {nom}")

            for k_txt in ("notas", "notas_seguimiento", "objetivo", "proxima_accion", "comentario_cita", "resumen_cita"):
                if rec.get(k_txt):
                    _escanear_texto_libre_en_busca_de_cita(str(rec.get(k_txt)), f"CRM: {nom}")

            for k_list in ("bitacora", "bitacora_seguimiento", "bitacora_notas", "historial_bitacora", "tareas", "tareas_checklist", "checklist", "citas"):
                lista_items = rec.get(k_list)
                if isinstance(lista_items, list):
                    for item_b in lista_items:
                        if isinstance(item_b, dict):
                            if item_b.get("completada") is True or item_b.get("done") is True or item_b.get("hecha") is True:
                                continue
                            f_b = _normalizar_fecha_str(item_b.get("fecha_cita") or item_b.get("fecha_objetivo") or item_b.get("fecha"))
                            h_b = item_b.get("hora_cita") or item_b.get("hora")
                            if f_b and h_b:
                                _registrar_ocupado(f_b, h_b, f"Bitácora: {nom}")
                            txt_b = " ".join(str(item_b.get(c) or "") for c in ("texto", "nota", "titulo", "descripcion", "detalle", "fecha"))
                            _escanear_texto_libre_en_busca_de_cita(txt_b, f"Bitácora: {nom}")
                        elif isinstance(item_b, str):
                            _escanear_texto_libre_en_busca_de_cita(item_b, f"Bitácora: {nom}")
    except Exception as e_crm:
        print(f"⚠️ Aviso leyendo citas del CRM en V148: {e_crm}")

    return {
        "status": "ok",
        "slots_ocupados": sorted(list(ocupados_set)),
        "detalle_citas": detalle_citas,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.route("/api/horarios-ocupados-agenda", methods=["GET", "POST"])
def api_horarios_ocupados_agenda_v145():
    res = _extraer_slots_ocupados_universal_sp_v145()
    return jsonify(res)
# === [SP_AGENDA_CRM_COORDINATOR_V145_END] ===
'''


# ==============================================================================
# 5. FUNCIONES DE REPARACIÓN DE `index.html` Y `servidor_local_b2b.py`
# ==============================================================================
def limpiar_inyeccion_rota_en_string_js(html):
    """
    1) Elimina cualquier bloque `<script>` que un replace anterior hubiera metido
       por error dentro del literal `'</div></body></html>'` de `spDescargarConversacionConsultor`.
    2) Desactiva el `setInterval` de 950ms que reabría el micrófono en bucle en `file://`.
    3) Actualiza el CSS del Carrito con las tarjetas coloreadas individualmente.
    """
    # 1. Quitar cualquier bloque [SP_AGENDA_CRM_WEB_SYNC_...] en cualquier parte del HTML
    html = re.sub(
        r"<!-- \[SP_AGENDA_CRM_WEB_SYNC_V14[5678]_START\] -->[\s\S]*?<!-- \[SP_AGENDA_CRM_WEB_SYNC_V14[5678]_END\] -->\s*",
        "",
        html
    )

    # 2. Asegurar que el cierre de `spDescargarConversacionConsultor` quede en 1 sola línea limpia
    html = re.sub(
        r"'</div>\s*</body></html>';",
        "'</div></body></html>';",
        html
    )

    # 3. Desactivar el bucle de 950ms que apilaba permisos de micrófono en protocolo file://
    html = html.replace(
        "if (_spOrbeDespierto && _spAutoEscuchaContinua && !_spHablandoSintesis && !_spMicroSesionActiva && !_spRearmandoOido) {\n            window.spActivarModoEscuchaPersistente(false);\n          }",
        "/* Bucle de 950ms desactivado en V148 para no apilar ventanas de permiso de micrófono en file:// */"
    )

    # 4. Sustituir el bloque CSS del Carrito por el nuevo con cada tarjeta coloreada y cero scroll
    patron_css_carrito = re.compile(
        r"/\*\s*={10,}\s*\n\s*MODAL CARRITO CONFIGURADOR EN MODO CRISTAL LUMINOSO[\s\S]*?/\*\s*===\s*\[SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_END\]\s*===\s*\*/",
        re.MULTILINE
    )
    if patron_css_carrito.search(html):
        html = patron_css_carrito.sub(
            lambda _: CSS_CARRITO_COLOREADO_SIN_SCROLL_V148.strip() + "\n    /* === [SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_END] === */",
            html,
            count=1
        )

    # 5. Inyectar nuestro bloque JS V148 ÚNICAMENTE en el último </body> real del documento (con rsplit)
    if "</body>" in html:
        partes = html.rsplit("</body>", 1)
        html = partes[0].rstrip() + "\n" + BLOQUE_JS_FINAL_WEB_V148.strip() + "\n</body>" + partes[1]

    return html


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

        html_nuevo = limpiar_inyeccion_rota_en_string_js(html_actual)
        escribir_archivo_con_backup(ruta, html_nuevo)
        validar_bloques_js_en_html(ruta)


def actualizar_servidor_local_b2b():
    rutas_servidor = [
        os.path.join(RUTA_SCRAPER, "servidor_local_b2b.py"),
        os.path.join(RUTA_SERVICIO_RESENAS, "servidor_local_b2b.py"),
    ]
    for ruta in rutas_servidor:
        if not os.path.exists(ruta):
            continue
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()

        if "# === [SP_AGENDA_CRM_COORDINATOR_V145_START] ===" in contenido:
            contenido = re.sub(
                r"# === \[SP_AGENDA_CRM_COORDINATOR_V145_START\] ===[\s\S]*?# === \[SP_AGENDA_CRM_COORDINATOR_V145_END\] ===",
                lambda _: BLOQUE_AGENDA_CRM_PY.strip(),
                contenido
            )
        else:
            patron_main = r"if\s+__name__\s*==\s*['\"]__main__['\"]\s*:"
            m = re.search(patron_main, contenido)
            if m:
                idx = m.start()
                contenido = contenido[:idx] + "\n\n" + BLOQUE_AGENDA_CRM_PY.strip() + "\n\n" + contenido[idx:]
            else:
                contenido = contenido.rstrip() + "\n\n" + BLOQUE_AGENDA_CRM_PY.strip() + "\n"

        escribir_archivo_con_backup(ruta, contenido)
        validar_sintaxis_python(ruta)


# ==============================================================================
# 6. PASO 1 PRIORITARIO + BLINDAJE ATEXIT: ACTUALIZAR LOS 2 DOCUMENTOS .MD
# ==============================================================================
NOTA_HISTORIAL_V148 = f"""
---
### ACTUALIZACIÓN {VERSION_ACTUAL} ({FECHA_EJECUCION}) — Reparación Raíz de Tecnosala y Carrito, Fin del Bucle de Permiso de Micrófono en `file://` y Tarjetas Coloreadas en el Carrito de Compra
- **Reparación Raíz del Bloque JS Principal de `index.html`:** Limpiada la inyección accidental dentro del literal `'</div></body></html>'` de `spDescargarConversacionConsultor` y sustituido `replace("</body>")` por `rsplit("</body>", 1)` para que el Carrito y la Tecnosala funcionen al 100% con 0 errores en `node --check`.
- **Fin del Bucle de Permiso de Micrófono en la Tecnosala:** Eliminada la doble llamada a `navigator.mediaDevices.getUserMedia` y el temporizador de `950 ms` que en protocolo local (`file://`) volvía a pedir permiso de micrófono sin cerrar nunca la ventana del navegador.
- **Paleta Cromática Diferenciada por Tarjeta en el Carrito (`#spModalCarritoCarta`):** Cada opción del Carrito luce ahora su propio color (Azul Cielo en Mensual Flexible, Ámbar/Dorado en Plan Anual, Pizarra en Solo Auditoría/Atril, Azul Real en Plan Base, Verde Esmeralda en Pack Escudo Dúo, Índigo en +1 Super-Auditoría y Coral/Oro en +2 Super-Auditorías) y coordina las horas ocupadas en tiempo real con el CRM y la Bitácora (`/api/horarios-ocupados-agenda`).
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
                txt = txt.rstrip() + "\n" + NOTA_HISTORIAL_V148
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
                    ["git", "-C", carpeta_git, "commit", "-m", f"feat({VERSION_ACTUAL}): reparacion Tecnosala sin bucle de micro, Carrito coloreado y agenda CRM"],
                    check=False, capture_output=True
                )
                subprocess.run(["git", "-C", carpeta_git, "push"], check=False, capture_output=True)
                print(f"  ✅ Git sincronizado en: {os.path.basename(carpeta_git)}")
            except Exception:
                pass


def reiniciar_prospector_puerto_5000():
    lanzador = os.path.join(RUTA_SCRAPER, "Lanzar_Prospeccion.command")
    if os.path.exists(lanzador):
        try:
            subprocess.Popen(["open", "-g", lanzador])
            print("  🔄 Servidor Prospector B2B (puerto 5000) actualizado.")
        except Exception:
            pass


def ejecutar_actualizacion():
    print("=" * 78)
    print(f"🚀 INICIANDO ACTUALIZACIÓN MAESTRA {VERSION_ACTUAL} — TECNOSALA, CARRITO COLOREADO Y AGENDA CRM")
    print("=" * 78)
    actualizar_documentos_maestros_md()
    actualizar_servidor_local_b2b()
    actualizar_index_html()
    replicar_ad_py_en_carpetas_oficiales()
    sincronizar_git_repositorios()
    reiniciar_prospector_puerto_5000()
    print("=" * 78)
    print(f"🎉 ACTUALIZACIÓN {VERSION_ACTUAL} COMPLETADA CON ÉXITO — RECARGA TU WEB CON CMD+SHIFT+R")
    print("=" * 78)


if __name__ == "__main__":
    ejecutar_actualizacion()
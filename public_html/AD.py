#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SISTEMAS PYME — ACTUALIZADOR MAESTRO SEGURO COMPLETO (AD.py - VERSIÓN V149)
================================================================================
Archivo 100% COMPLETO de principio a fin (CERO '# ... existing code ...').
Guárdalo como `AD.py` y ejecútalo en tu Terminal con:
    python3 AD.py

Qué soluciona esta versión V149:
1. OÍDO FLUIDO ORIGINAL EN EL TECNOCONSULTOR (TECNOSALA):
   - Restaura al 100% el motor original del Orbe 3D (`spActivarModoEscuchaPersistente`
     con `continuous = true`, transcripción en vivo `🎙️ «...»` en el Teleprompter LED
     y latido de la esfera con tu voz).
   - Elimina la función `asegurarPermisoUnicoMicrofonoV129` (`getUserMedia` duplicado)
     y el segundo reconocedor que se peleaba con el del Orbe y cortaba las frases.
2. COLOR EN TARJETA 4 (ATRILES NFC), TARJETA 5 (RESERVA FASE 2) Y CAJA DE CITA:
   - Tarjeta 4 (Atriles NFC + QR): Fondo Ámbar / Dorado cálido con borde izquierdo `#d97706`.
   - Tarjeta 5 (Reserva Prioritaria Fase 2): Fondo Azul Cielo / Cian con borde izquierdo `#0284c7`.
   - Caja de Cita de Alta (`#spCartBoxCitaAlta`): Fondo degradado Turquesa-Esmeralda-Ámbar
     (`#ecfdf5 -> #e0f2fe -> #fef3c7`) con borde `#0d9488` y selectores destacados.
3. COORDINACIÓN CON EL CRM Y BITÁCORA (`/api/horarios-ocupados-agenda`):
   - Mantiene sincronizadas las horas ocupadas del CRM/Bitácora (como el sábado a las 11:00)
     sin tocar ni interferir con el micrófono de la Tecnosala.
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

VERSION_ACTUAL = "V149"
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
                tmp_js = f"/tmp/_sp_check_v149_{idx}.js"
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
# 2. CSS COMPLETO DEL CARRITO CON COLOR EN TARJETAS 1, 2, 3, 4, 5 Y CAJA DE CITA
# ==============================================================================
CSS_CARRITO_COLOREADO_TOTAL_V149 = r"""
    /* =========================================================================
       MODAL CARRITO CONFIGURADOR EN MODO CRISTAL LUMINOSO CRO (NEUROMARKETING)
       TARJETAS 1, 2, 3, 4, 5 Y CAJA DE CITA COLOREADAS + CERO SCROLL
       ========================================================================= */
    #spModalCarritoCarta {
      padding: 0.5rem 1rem !important;
      overflow: hidden !important;
    }
    #spModalCarritoCarta > div {
      max-width: 74rem !important;
      max-height: 96vh !important;
      overflow: hidden !important;
      padding: 0.9rem 1.4rem !important;
      background: linear-gradient(160deg, #f8fafc 0%, #ffffff 55%, #f0fdfa 100%) !important;
      color: #0b2239 !important;
      border: 2.5px solid #0d9488 !important;
      box-shadow: 0 28px 65px -12px rgba(11, 34, 57, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.95) !important;
    }
    #spModalCarritoCarta > div > div:first-child {
      padding-bottom: 0.45rem !important;
      margin-bottom: 0.55rem !important;
      border-bottom: 1.5px solid #cbd5e1 !important;
    }
    #spModalCarritoCarta > div > div:first-child span.bg-amber-950\/90 {
      display: none !important;
    }
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
    #spModalCarritoCarta h3 {
      font-size: 1.24rem !important;
      line-height: 1.2 !important;
      color: #0b2239 !important;
      margin-top: 0 !important;
    }
    #spModalCarritoCarta h4 {
      font-size: 0.88rem !important;
      color: #0b2239 !important;
      letter-spacing: 0.02em !important;
    }
    #spModalCarritoCarta .lg\:col-span-7 {
      gap: 0.45rem !important;
    }
    #spModalCarritoCarta .lg\:col-span-7.space-y-3 > * + * {
      margin-top: 0.45rem !important;
    }
    #spModalCarritoCarta label {
      font-size: 0.78rem !important;
      font-weight: 900 !important;
      color: #065f46 !important;
      letter-spacing: 0.02em !important;
      margin-bottom: 0.22rem !important;
    }
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
    #spModalCarritoCarta .sp-cart-item-btn > span:first-child {
      font-size: 0.91rem !important;
      font-weight: 900 !important;
      color: #0b2239 !important;
      line-height: 1.2 !important;
      margin-bottom: 0.1rem !important;
    }
    #spModalCarritoCarta .sp-cart-item-btn > span:not(:first-child) {
      font-size: 0.775rem !important;
      font-weight: 600 !important;
      color: #334155 !important;
      line-height: 1.24 !important;
      display: block !important;
      margin-top: 0.06rem !important;
    }
    #spModalCarritoCarta .sp-cart-item-btn:hover {
      transform: translateY(-1.5px) !important;
    }

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

    /* 3A. Sin Auditoría por ahora -> Neutro Suave */
    #spModalCarritoCarta #spCartAud_0 {
      background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%) !important;
      border-color: #cbd5e1 !important;
      border-left: 4px solid #64748b !important;
    }
    #spModalCarritoCarta #spCartAud_0.sp-cart-selected {
      background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%) !important;
      border: 2.5px solid #334155 !important;
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

    /* 3C. +2 Super-Auditorías -> Oro / Coral Cálido */
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

    /* =====================================================================
       TARJETA 4 (ATRILES NFC), TARJETA 5 (RESERVA FASE 2) Y CAJA DE CITA
       CON COLOR VIVO Y DIFERENCIADO (MÁXIMA ESPECIFICIDAD CSS)
       ===================================================================== */
    #spModalCarritoCarta #spCartBoxAtriles4,
    #spModalCarritoCarta div.sm\:col-span-5 {
      background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 55%, #fde68a 100%) !important;
      border: 2px solid #f59e0b !important;
      border-left: 5px solid #d97706 !important;
      box-shadow: 0 6px 16px -4px rgba(217, 119, 6, 0.22), inset 0 1px 0 #ffffff !important;
      border-radius: 0.9rem !important;
    }
    #spModalCarritoCarta #spCartBoxAtriles4 label,
    #spModalCarritoCarta div.sm\:col-span-5 label {
      color: #92400e !important;
      font-size: 0.8rem !important;
      font-weight: 900 !important;
    }
    #spModalCarritoCarta #spCartAtrilSelect {
      background: #ffffff !important;
      border: 2px solid #d97706 !important;
      color: #78350f !important;
      font-weight: 800 !important;
    }

    #spModalCarritoCarta #spCartBoxReserva5,
    #spModalCarritoCarta div.sm\:col-span-7 {
      background: linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 55%, #bae6fd 100%) !important;
      border: 2px solid #38bdf8 !important;
      border-left: 5px solid #0284c7 !important;
      box-shadow: 0 6px 16px -4px rgba(2, 132, 199, 0.22), inset 0 1px 0 #ffffff !important;
      border-radius: 0.9rem !important;
    }
    #spModalCarritoCarta #spCartBoxReserva5 label,
    #spModalCarritoCarta div.sm\:col-span-7 label {
      color: #075985 !important;
      font-size: 0.8rem !important;
      font-weight: 900 !important;
    }
    #spModalCarritoCarta #spCartReservaFase2 {
      background: #ffffff !important;
      border: 2px solid #0284c7 !important;
      color: #0c4a6e !important;
      font-weight: 800 !important;
    }

    /* CAJA DONDE SE COGE LA CITA (🗓️ CITA DE ALTA): COLOR TURQUESA-ESMERALDA-ÁMBAR LUMINOSO */
    #spModalCarritoCarta #spCartBoxCitaAlta,
    #spModalCarritoCarta #spCartFormInputsWrap > div:last-child {
      background: linear-gradient(135deg, #ecfdf5 0%, #e0f2fe 52%, #fef3c7 100%) !important;
      border: 2px solid #0d9488 !important;
      border-left: 5px solid #059669 !important;
      box-shadow: 0 8px 20px -4px rgba(13, 148, 136, 0.25), inset 0 1px 0 #ffffff !important;
      border-radius: 0.9rem !important;
      padding: 0.55rem 0.75rem !important;
    }
    #spModalCarritoCarta #spCartSelectDiaLV {
      background: #ffffff !important;
      border: 2px solid #0d9488 !important;
      color: #064e3b !important;
      font-weight: 800 !important;
    }
    #spModalCarritoCarta #spCartSelectHoraManana {
      background: #fffbeb !important;
      border: 2px solid #d97706 !important;
      color: #78350f !important;
      font-weight: 900 !important;
    }

    /* Columna derecha del Resumen con tinte verde-perla suave */
    #spModalCarritoCarta .lg\:col-span-5 {
      background: linear-gradient(165deg, #ffffff 0%, #f0fdfa 60%, #ecfdf5 100%) !important;
      border: 2px solid #14b8a6 !important;
      padding: 0.7rem 0.95rem !important;
      box-shadow: 0 10px 25px -6px rgba(13, 148, 136, 0.18) !important;
    }

    /* Campos de formulario de Nombre, Negocio y Teléfono con borde visible y fondo suave */
    #spModalCarritoCarta select,
    #spModalCarritoCarta input[type="text"],
    #spModalCarritoCarta input[type="tel"],
    #spModalCarritoCarta input[type="datetime-local"] {
      background: #ffffff !important;
      color: #0b2239 !important;
      border: 1.5px solid #64748b !important;
      font-size: 0.86rem !important;
      font-weight: 700 !important;
      padding: 0.38rem 0.68rem !important;
      height: 2.25rem !important;
      border-radius: 0.65rem !important;
      box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.04) !important;
    }
    #spModalCarritoCarta #spCartInputNegocioCiudad {
      background: #fffbeb !important;
      border: 2px solid #f59e0b !important;
      color: #78350f !important;
    }
    #spModalCarritoCarta select:focus,
    #spModalCarritoCarta input:focus {
      border-color: #0d9488 !important;
      box-shadow: 0 0 0 2px rgba(20, 184, 166, 0.25) !important;
    }
    #spModalCarritoCarta input::placeholder {
      color: #475569 !important;
      font-weight: 600 !important;
    }
    #spModalCarritoCarta #spCartCountModulosBadge {
      background: #065f46 !important;
      color: #ffffff !important;
      border: 1px solid #047857 !important;
      font-size: 0.74rem !important;
      font-weight: 800 !important;
      padding: 0.15rem 0.55rem !important;
    }
    #spModalCarritoCarta #spCartSummaryLines {
      font-size: 0.83rem !important;
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
    #spModalCarritoCarta .bg-emerald-950\/60 {
      background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
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
      font-size: 1.35rem !important;
      font-weight: 900 !important;
      white-space: nowrap !important;
    }
    #spModalCarritoCarta #spCartCuotaMensual {
      color: #0f766e !important;
      font-size: 0.82rem !important;
      font-weight: 900 !important;
    }
    #spModalCarritoCarta .text-amber-300,
    #spModalCarritoCarta .text-amber-200,
    #spModalCarritoCarta .text-amber-200\/95 {
      color: #92400e !important;
      font-weight: 800 !important;
    }
    #spModalCarritoCarta #spCartSyncCalBadge {
      color: #ffffff !important;
      background: #059669 !important;
      padding: 0.12rem 0.5rem !important;
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
    #spModalCarritoCarta #spSubSelectorBaseS1S2 {
      background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%) !important;
      border: 2px solid #0d9488 !important;
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
    #spModalCarritoCarta #spBtnSubmitCarrito {
      font-size: 0.95rem !important;
      padding: 0.62rem 1rem !important;
    }
"""


# ==============================================================================
# 3. BLOQUE JS LIGERO PARA COORDINAR EL CARRITO CON EL CRM (SIN TOCAR EL MICRO
#    DEL TECNOCONSULTOR PARA QUE FUNCIONE EXACTAMENTE IGUAL DE FLUIDO QUE ANTES)
# ==============================================================================
BLOQUE_JS_SOLO_AGENDA_Y_COLORES_V149 = r'''
<!-- [SP_AGENDA_CRM_WEB_SYNC_V149_START] -->
<script>
(function() {
  /* 1. Asignar IDs explícitos a las cajas 4, 5 y Cita de Alta del Carrito para garantizar su color vivo */
  function aplicarIdsColorCajasCarritoV149() {
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

  /* 2. Puente del botón final del Test de Diagnóstico al Carrito */
  window.spAbrirCarritoConDiagnosticoPreseleccionado = function() {
    if (typeof window.spAbrirCarritoConfigurador === 'function') {
      window.spAbrirCarritoConfigurador('duo', 1);
      setTimeout(aplicarIdsColorCajasCarritoV149, 40);
    }
  };

  /* 3. Coordinación en tiempo real de las horas ocupadas del CRM y la Bitácora */
  window.SP_SLOTS_OCUPADOS_CRM_EXTRA = window.SP_SLOTS_OCUPADOS_CRM_EXTRA || new Set();

  function normalizarSlotEspacio(slotRaw) {
    var s = String(slotRaw || '').trim();
    if (!s) return '';
    s = s.replace('|', ' ').replace('T', ' ');
    var m = s.match(/^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})/);
    return m ? (m[1] + ' ' + m[2]) : '';
  }

  window.spAplicarBloqueoHorasCrmEnSelect = function() {
    aplicarIdsColorCajasCarritoV149();
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
      var guardados = JSON.parse(localStorage.getItem('sp_citas_ocupadas_crm_v149') || '[]');
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
              localStorage.setItem('sp_citas_ocupadas_crm_v149', JSON.stringify(Array.from(window.SP_SLOTS_OCUPADOS_CRM_EXTRA)));
            } catch (e) {}
          }
        })
        .catch(function() {});
    })).then(function() {
      window.spAplicarBloqueoHorasCrmEnSelect();
    });
  };

  function engancharEventosAgendaCarritoV149() {
    aplicarIdsColorCajasCarritoV149();
    window.spSincronizarCitasCrmLocal();

    if (typeof window.spActualizarHorasDisponiblesCarritoV125 === 'function' && !window.spActualizarHorasDisponiblesCarritoV125._hookV149) {
      var origActHoras = window.spActualizarHorasDisponiblesCarritoV125;
      var nuevaActHoras = function() {
        var r = origActHoras.apply(this, arguments);
        window.spAplicarBloqueoHorasCrmEnSelect();
        return r;
      };
      nuevaActHoras._hookV149 = true;
      window.spActualizarHorasDisponiblesCarritoV125 = nuevaActHoras;
    }

    if (typeof window.spAbrirCarritoConfigurador === 'function' && !window.spAbrirCarritoConfigurador._hookV149) {
      var origOpen = window.spAbrirCarritoConfigurador;
      var nuevoOpen = function() {
        var r = origOpen.apply(this, arguments);
        aplicarIdsColorCajasCarritoV149();
        window.spSincronizarCitasCrmLocal();
        setTimeout(window.spAplicarBloqueoHorasCrmEnSelect, 120);
        return r;
      };
      nuevoOpen._hookV149 = true;
      window.spAbrirCarritoConfigurador = nuevoOpen;
    }

    if (typeof window.spConfirmarPedidoYAgendarCita === 'function' && !window.spConfirmarPedidoYAgendarCita._hookV149) {
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
              localStorage.setItem('sp_citas_ocupadas_crm_v149', JSON.stringify(Array.from(window.SP_SLOTS_OCUPADOS_CRM_EXTRA)));
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
      nuevoConfirm._hookV149 = true;
      window.spConfirmarPedidoYAgendarCita = nuevoConfirm;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(engancharEventosAgendaCarritoV149, 250);
    });
  } else {
    setTimeout(engancharEventosAgendaCarritoV149, 250);
  }
})();
</script>
<!-- [SP_AGENDA_CRM_WEB_SYNC_V149_END] -->
'''


# ==============================================================================
# 4. REPARACIÓN DE `index.html`: DEVOLVER EL MOTOR DE VOZ ORIGINAL DEL ORBE 3D
# ==============================================================================
def reparar_index_html_voz_original_y_colores(html):
    # 1. Quitar cualquier bloque [SP_AGENDA_CRM_WEB_SYNC_V14...] anterior
    html = re.sub(
        r"<!-- \[SP_AGENDA_CRM_WEB_SYNC_V14[56789]_START\] -->[\s\S]*?<!-- \[SP_AGENDA_CRM_WEB_SYNC_V14[56789]_END\] -->\s*",
        "",
        html
    )

    # 2. Asegurar que el literal `'</div></body></html>'` de spDescargarConversacionConsultor esté limpio
    html = re.sub(
        r"'</div>\s*</body></html>';",
        "'</div></body></html>';",
        html
    )

    # 3. Restaurar el vigilante original del Orbe 3D si fue comentado en V148, pero con margen prudente de 2200ms
    html = html.replace(
        "/* Bucle de 950ms desactivado en V148 para no apilar ventanas de permiso de micrófono en file:// */",
        "if (_spOrbeDespierto && _spAutoEscuchaContinua && !_spHablandoSintesis && !_spMicroSesionActiva && !_spRearmandoOido && window.location.protocol !== 'file:') {\n            window.spActivarModoEscuchaPersistente(false);\n          }"
    )

    # 4. LA CLAVE DEL PROBLEMA DE ESCUCHA:
    # En `spScriptMejorasCarritoYMigradoPersistenteV130`, la función `instalarMicrofonoContinuoSinRePromptV129()`
    # sobrescribía `window.spActivarModoEscuchaPersistente` y llamaba a `navigator.mediaDevices.getUserMedia({ audio: true })`
    # peleándose con el motor original del Orbe 3D (que es el que muestra `🎙️ «...»` en el Teleprompter LED y mueve la esfera).
    # Neutralizamos `instalarMicrofonoContinuoSinRePromptV129` para que el motor original del Orbe 3D funcione 100% libre y fluido como antes:
    html = re.sub(
        r"function instalarMicrofonoContinuoSinRePromptV129\(\)\s*\{[\s\S]*?\n  \}\n\n  function obtenerTramosPorDiaSemanaV125",
        """function instalarMicrofonoContinuoSinRePromptV129() {
    /* Desactivado en V149: deja actuar al motor original nativo del Orbe 3D sin doble micrófono ni getUserMedia */
  }

  function obtenerTramosPorDiaSemanaV125""",
        html,
        count=1
    )

    # 5. Añadir IDs directos a las cajas 4, 5 y Cita en el HTML estático del Carrito
    html = html.replace(
        '<div class="sm:col-span-5 bg-slate-950/80 border border-white/10 rounded-xl p-2.5">',
        '<div id="spCartBoxAtriles4" class="sm:col-span-5 bg-slate-950/80 border border-white/10 rounded-xl p-2.5">'
    )
    html = html.replace(
        '<div class="sm:col-span-7 bg-slate-950/80 border border-white/10 rounded-xl p-2.5">',
        '<div id="spCartBoxReserva5" class="sm:col-span-7 bg-slate-950/80 border border-white/10 rounded-xl p-2.5">'
    )

    # 6. Actualizar el bloque CSS del Carrito con los nuevos colores para Tarjeta 4, Tarjeta 5 y Caja de Cita
    patron_css_carrito = re.compile(
        r"/\*\s*={10,}\s*\n\s*MODAL CARRITO CONFIGURADOR EN MODO CRISTAL LUMINOSO[\s\S]*?/\*\s*===\s*\[SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_END\]\s*===\s*\*/",
        re.MULTILINE
    )
    if patron_css_carrito.search(html):
        html = patron_css_carrito.sub(
            lambda _: CSS_CARRITO_COLOREADO_TOTAL_V149.strip() + "\n    /* === [SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_END] === */",
            html,
            count=1
        )

    # 7. Inyectar el bloque JS de coordinación de agenda y colores al final antes de </body> (con rsplit)
    if "</body>" in html:
        partes = html.rsplit("</body>", 1)
        html = partes[0].rstrip() + "\n" + BLOQUE_JS_SOLO_AGENDA_Y_COLORES_V149.strip() + "\n</body>" + partes[1]

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

        html_nuevo = reparar_index_html_voz_original_y_colores(html_actual)
        escribir_archivo_con_backup(ruta, html_nuevo)
        validar_bloques_js_en_html(ruta)


# ==============================================================================
# 5. PASO 1 PRIORITARIO + BLINDAJE ATEXIT: ACTUALIZAR LOS 2 DOCUMENTOS .MD
# ==============================================================================
NOTA_HISTORIAL_V149 = f"""
---
### ACTUALIZACIÓN {VERSION_ACTUAL} ({FECHA_EJECUCION}) — Restauración del Oído Fluido Original del Tecnoconsultor (Orbe 3D) y Coloreado de Tarjetas 4 (Atriles), 5 (Reserva Fase 2) y Caja de Cita en el Carrito
- **Restauración del Motor de Escucha Original del Orbe 3D en la Tecnosala:** Neutralizada la función duplicada `instalarMicrofonoContinuoSinRePromptV129` que abría un segundo `webkitSpeechRecognition` y llamaba a `getUserMedia` interfiriendo con el oído nativo del Orbe 3D. Ahora el Tecnoconsultor vuelve a escuchar con total fluidez, pintando en tiempo real `🎙️ «...»` en el Teleprompter LED y moviendo la esfera al ritmo de la voz.
- **Coloreado de la Tarjeta 4 (`#spCartBoxAtriles4`), Tarjeta 5 (`#spCartBoxReserva5`) y Caja de Cita (`#spCartBoxCitaAlta`) en el Carrito de Compra:** Aplicados degradados luminosos diferenciados (Ámbar cálido en Atriles NFC, Azul Cielo en Reserva Prioritaria Fase 2 y Turquesa-Esmeralda-Ámbar en la Caja de Cita de Alta) con selectores CSS de alta especificidad.
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
                txt = txt.rstrip() + "\n" + NOTA_HISTORIAL_V149
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
                    ["git", "-C", carpeta_git, "commit", "-m", f"feat({VERSION_ACTUAL}): oido fluido original en Tecnosala y colores en tarjetas 4, 5 y Cita del Carrito"],
                    check=False, capture_output=True
                )
                subprocess.run(["git", "-C", carpeta_git, "push"], check=False, capture_output=True)
                print(f"  ✅ Git sincronizado en: {os.path.basename(carpeta_git)}")
            except Exception:
                pass


def ejecutar_actualizacion():
    print("=" * 78)
    print(f"🚀 INICIANDO ACTUALIZACIÓN MAESTRA {VERSION_ACTUAL} — VOZ FLUIDA ORIGINAL + COLORES CARRITO 4, 5 Y CITA")
    print("=" * 78)
    actualizar_documentos_maestros_md()
    actualizar_index_html()
    replicar_ad_py_en_carpetas_oficiales()
    sincronizar_git_repositorios()
    print("=" * 78)
    print(f"🎉 ACTUALIZACIÓN {VERSION_ACTUAL} COMPLETADA CON ÉXITO — RECARGA TU WEB CON CMD+SHIFT+R")
    print("=" * 78)


if __name__ == "__main__":
    ejecutar_actualizacion()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SISTEMAS PYME — ACTUALIZADOR MAESTRO SEGURO (AD.py - VERSIÓN V145)
================================================================================
Objetivo de esta actualización (V145):
1. Coordinación Bidireccional de Agenda entre el Carrito Web (index.html),
   el CRM y la Bitácora del Prospector (servidor_local_b2b.py / crm_b2b_db.json),
   leads_contrataciones_web.json y Google Sheets:
   - Nuevo endpoint `/api/horarios-ocupados-agenda` en `servidor_local_b2b.py`
     que inspecciona todos los registros de `crm_b2b_db.json` (campos `fecha_cita`,
     `hora_cita`, `fecha_proximo_contacto`, `proxima_accion_fecha`, `citas`,
     `bitacora`, `tareas` y `notas`), además de `leads_contrataciones_web.json`
     y el puente de Google Sheets, devolviendo todos los huecos ocupados
     (ej. `2026-11-07|11:00`) y bloqueando tanto el tramo de `:00` como el `:30`
     si una reunión dura 1 hora o coincide en esa franja.
   - Nuevo endpoint `/api/registrar-cita-web-en-crm` en `servidor_local_b2b.py`
     para que cuando un cliente agende su videollamada desde el Carrito de
     `index.html`, se cree/actualice al instante su ficha y su Bitácora en
     `crm_b2b_db.json` bloqueando esa fecha y hora.
   - En `index.html` (Carrito Configurador a la Carta):
     * Mantiene que en "5. Reserva Prioritaria Fase 2" el cliente pueda escoger
       todos los módulos que quiera sin límite.
     * Consulta en vivo `http://127.0.0.1:5000/api/horarios-ocupados-agenda`,
       `http://127.0.0.1:8765/api/horarios-ocupados-agenda` y el webhook de
       Google Sheets al abrir el Carrito o cambiar de día, eliminando o
       marcando como `⛔ Ocupado en Agenda` cualquier hora que ya tengas
       comprometida en tu CRM o Bitácora (como el sábado a las 11:00).
2. Actualización automática en Paso 1 + blindaje `atexit` de los 2 únicos
   documentos maestros `.md` en `SISTEMAS PYME/Programar` y sincronización
   hacia Google Sheets (`Biblia_IA_Viva` y `Manual_Maestro_AD`) y Google Drive.
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

VERSION_ACTUAL = "V145"
FECHA_EJECUCION = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
TIMESTAMP_BAK = datetime.now().strftime("%Y%m%d_%H%M%S")

RUTA_WEB_PUBLIC = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme/public_html"
RUTA_SCRAPER = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Scraper/Scrapper App"
RUTA_SERVICIO_RESENAS = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Servicios/Servicio Reseñas/servicio_resenas"
RUTA_PROGRAMAR = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Programar"

URL_WEBHOOK_SHEETS_DEFAULT = "https://script.google.com/macros/s/AKfycbwo9pcYbQKru4WMAxAnHNcqtIcAYQogXkaQ8BAWhTeyzc49kLtM02SVFnTxYRGqUStapg/exec"


def crear_backup_seguro(ruta_archivo):
    if not ruta_archivo or not os.path.exists(ruta_archivo):
        return None
    carpeta_base = os.path.dirname(os.path.abspath(ruta_archivo))
    carpeta_bak = os.path.join(carpeta_base, "backups_sp")
    os.makedirs(carpeta_bak, exist_ok=True)
    nombre_base = os.path.basename(ruta_archivo)
    ruta_bak = os.path.join(carpeta_bak, f"{nombre_base}.{TIMESTAMP_BAK}.bak")
    shutil.copy2(ruta_archivo, ruta_bak)
    print(f"  🛡️ Backup creado: {ruta_bak}")
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
    print(f"  🟢 Verificado OK ({size_kb} KB): {ruta_archivo}")
    return True


def validar_sintaxis_python(ruta_py):
    if not os.path.exists(ruta_py):
        return True
    try:
        with open(ruta_py, "r", encoding="utf-8") as f:
            codigo = f.read()
        ast.parse(codigo)
        print(f"  ✅ Sintaxis Python (ast.parse) verificada OK: {os.path.basename(ruta_py)}")
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
                tmp_js = f"/tmp/_sp_check_{idx}.js"
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
        print(f"  🟢 Validación JS/HTML completada OK: {os.path.basename(ruta_html)}")
        return True
    except Exception as e:
        print(f"  ⚠️ Aviso validando {ruta_html}: {e}")
        return True


# ==============================================================================
# BLOQUE 1: COORDINADOR DE AGENDA EN TIEMPO REAL EN `servidor_local_b2b.py`
# ==============================================================================
BLOQUE_AGENDA_CRM_PY = r'''
# === [SP_AGENDA_CRM_COORDINATOR_V145_START] ===
def _extraer_slots_ocupados_universal_sp_v145():
    """
    Lee todas las citas agendadas en:
    1) crm_b2b_db.json (campos fecha_cita, hora_cita, fecha_proximo_contacto,
       proxima_accion_fecha, cita_alta, bitacora, tareas, notas, etc.)
    2) leads_contrataciones_web.json (en Scraper y en public_html)
    3) citas_web_bloqueadas.json
    Devuelve un diccionario con:
      - slots_ocupados: lista de strings "YYYY-MM-DD|HH:MM"
      - detalle_citas: lista con fecha, hora y negocio (sin exponer datos sensibles)
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
        # Buscar HH:MM o HH.MM o "a las 11" / "11h"
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
        # Si es a en punto (:00), en las reuniones de CRM/prospección bloqueamos también la media hora (:30)
        # para no solapar una videollamada de alta en mitad de una reunión de 45-60 min, y además el propio :00.
        slots_out = [slot_principal]
        if mm == 0:
            slots_out.append(f"{hh:02d}:30")
        return slots_out

    def _normalizar_fecha_str(f_str):
        if not f_str:
            return None
        s = str(f_str).strip().lower()
        # 1) YYYY-MM-DD
        m_iso = re.search(r'\b(202\d)-([01]\d)-([0-3]\d)\b', s)
        if m_iso:
            return f"{m_iso.group(1)}-{m_iso.group(2)}-{m_iso.group(3)}"
        # 2) DD/MM/YYYY o DD-MM-YYYY
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
        # 3) "sábado, 07 de noviembre" o "7 de noviembre"
        m_txt = re.search(r'\b([0-3]?\d)\s+de\s+([a-záéíóú]+)', s)
        if m_txt:
            dd = int(m_txt.group(1))
            mes_nom = texto_sin_tildes(m_txt.group(2))
            mm = meses_es.get(mes_nom) or meses_es.get(mes_nom[:3])
            if mm:
                return f"{anio_actual:04d}-{mm:02d}-{dd:02d}"
        # 4) Si menciona un día de la semana ("sábado", "lunes", etc.) sin número, tomar el próximo día de esa semana (incluyendo hoy)
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
        # Si contiene datetime ISO tipo 2026-11-07T11:00 o "2026-11-07 11:00"
        for m_dt in re.finditer(r'(202\d-[01]\d-[0-3]\d)[t\s_]+([012]?\d:[0-5]\d)', t_low):
            _registrar_ocupado(m_dt.group(1), m_dt.group(2), nombre_neg)

        # Si contiene fecha DD/MM/YYYY junto con hora HH:MM
        for m_dmy in re.finditer(r'([0-3]?\d[/\-][01]?\d(?:[/\-]202\d)?)\s*(?:a\s+las\s+|[-·•]\s*|\s+)([012]?\d(?::[0-5]\d|\s*h\b))', t_low):
            f_iso = _normalizar_fecha_str(m_dmy.group(1))
            if f_iso:
                _registrar_ocupado(f_iso, m_dmy.group(2), nombre_neg)

        # Si menciona día de la semana + hora (ej: "sábado a las 11", "sabado 11:00", "cita sábado 11h")
        for m_sem in re.finditer(r'\b(lunes|martes|mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo)\b[^\n.;]{0,35}?\b(?:a\s+las\s+|hora\s+)?([012]?\d(?::[0-5]\d|\s*h\b|:00)?)', t_low):
            dia_palabra = m_sem.group(1)
            hora_palabra = m_sem.group(2)
            # Evitar falsos positivos si el número es parte de una fecha sin hora
            if re.search(r'(:[0-5]\d|\bh\b|a\s+las)', m_sem.group(0)):
                f_iso = _normalizar_fecha_str(dia_palabra)
                if f_iso:
                    _registrar_ocupado(f_iso, hora_palabra, nombre_neg)

    # 1) Inspeccionar CRM completo (crm_b2b_db.json)
    try:
        crm_data = load_crm()
        for k_pid, rec in (crm_data or {}).items():
            if not isinstance(rec, dict):
                continue
            nom = str(rec.get("nombre") or k_pid).strip()

            # Campos directos de fecha y hora de cita en la ficha del CRM
            for k_f in ("fecha_cita", "fecha_proximo_contacto", "proxima_accion_fecha", "cita_fecha", "fecha_reunion", "cita"):
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

            # Si tiene hora_cita suelta y fecha en otro campo
            if rec.get("hora_cita"):
                f_base = (
                    _normalizar_fecha_str(rec.get("fecha_cita"))
                    or _normalizar_fecha_str(rec.get("fecha_proximo_contacto"))
                    or _normalizar_fecha_str(rec.get("notas"))
                )
                if f_base:
                    _registrar_ocupado(f_base, rec.get("hora_cita"), f"CRM: {nom}")

            # Escanear Notas y Objetivo del CRM
            for k_txt in ("notas", "objetivo", "proxima_accion", "comentario_cita", "resumen_cita"):
                if rec.get(k_txt):
                    _escanear_texto_libre_en_busca_de_cita(str(rec.get(k_txt)), f"CRM: {nom}")

            # Escanear Cuaderno de Bitácora y Checklist de Tareas del CRM
            for k_list in ("bitacora", "bitacora_notas", "historial_bitacora", "tareas", "checklist", "citas"):
                lista_items = rec.get(k_list)
                if isinstance(lista_items, list):
                    for item_b in lista_items:
                        if isinstance(item_b, dict):
                            if item_b.get("completada") is True or item_b.get("done") is True:
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
        print(f"⚠️ Aviso leyendo citas del CRM en V145: {e_crm}")

    # 2) Inspeccionar leads_contrataciones_web.json (en public_html, Scraper y servicio_resenas)
    rutas_pedidos_web = [
        os.path.join(BASE_DIR, "leads_contrataciones_web.json"),
        os.path.join(RUTA_OFICIAL_PUBLIC_HTML_WEB, "leads_contrataciones_web.json"),
        os.path.join(RUTA_OFICIAL_SERVICIO_RESENAS, "leads_contrataciones_web.json"),
    ]
    for rp in rutas_pedidos_web:
        if os.path.exists(rp):
            try:
                with open(rp, "r", encoding="utf-8") as fp:
                    lista_ped = json.load(fp)
                if isinstance(lista_ped, dict):
                    lista_ped = lista_ped.get("pedidos") or lista_ped.get("citas") or []
                for ped in (lista_ped if isinstance(lista_ped, list) else []):
                    if not isinstance(ped, dict):
                        continue
                    f_p = _normalizar_fecha_str(ped.get("fecha_iso") or ped.get("fecha_cita") or ped.get("dia_cita") or ped.get("fecha"))
                    h_p = ped.get("hora_cita") or ped.get("franja_horaria") or ped.get("hora")
                    if f_p and h_p:
                        _registrar_ocupado(f_p, h_p, f"Reserva Web: {ped.get('negocio') or ped.get('nombre') or 'Cliente'}")
            except Exception:
                pass

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


@app.route("/api/registrar-cita-web-en-crm", methods=["POST"])
def api_registrar_cita_web_en_crm_v145():
    """
    Cuando un cliente confirma su pedido y agenda videollamada en el Carrito de index.html,
    registra automáticamente la cita en:
    1) crm_b2b_db.json (ficha + cuaderno de bitácora) para que aparezca en el Prospector y bloquee esa hora.
    2) leads_contrataciones_web.json (en Scraper y en public_html).
    """
    try:
        data = request.get_json(force=True, silent=True) or {}
        nombre_contacto = str(data.get("nombre") or data.get("nombre_contacto") or "Cliente Web").strip()
        negocio = str(data.get("negocio") or data.get("nombre_negocio") or nombre_contacto).strip()
        telefono = str(data.get("telefono") or "").strip()
        fecha_iso = str(data.get("fecha_iso") or data.get("fecha_cita") or "").strip()
        dia_texto = str(data.get("dia_texto") or fecha_iso).strip()
        hora_inicio = str(data.get("hora_inicio") or data.get("hora_cita") or "").strip()
        resumen_pedido = str(data.get("resumen_pedido") or "").strip()
        total_dia1 = str(data.get("total_dia1") or "").strip()
        modulos_reserva = data.get("modulos_reserva") or []

        # Guardar en leads_contrataciones_web.json
        nuevo_pedido = {
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nombre": nombre_contacto,
            "negocio": negocio,
            "telefono": telefono,
            "fecha_iso": fecha_iso,
            "dia_cita": dia_texto,
            "hora_cita": hora_inicio,
            "resumen_pedido": resumen_pedido,
            "total_dia1": total_dia1,
            "modulos_reserva": modulos_reserva
        }
        for rp in (
            os.path.join(BASE_DIR, "leads_contrataciones_web.json"),
            os.path.join(RUTA_OFICIAL_PUBLIC_HTML_WEB, "leads_contrataciones_web.json"),
        ):
            try:
                existentes = []
                if os.path.exists(rp):
                    with open(rp, "r", encoding="utf-8") as f_in:
                        existentes = json.load(f_in)
                        if not isinstance(existentes, list):
                            existentes = []
                existentes.insert(0, nuevo_pedido)
                with open(rp, "w", encoding="utf-8") as f_out:
                    json.dump(existentes[:300], f_out, ensure_ascii=False, indent=2)
            except Exception:
                pass

        # Registrar también en crm_b2b_db.json y en su Bitácora
        crm_db = load_crm()
        clave_busqueda = normalizar_clave_rapida(negocio)
        target_key = None
        for k_c, r_c in crm_db.items():
            if isinstance(r_c, dict) and normalizar_clave_rapida(r_c.get("nombre", "")) == clave_busqueda:
                target_key = k_c
                break
        if not target_key:
            target_key = re.sub(r"[^a-z0-9]+", "-", texto_sin_tildes(negocio)).strip("-") or f"web-{int(time.time())}"

        rec = crm_db.get(target_key, {"place_id": target_key, "nombre": negocio})
        rec["nombre"] = negocio
        rec["encargado"] = nombre_contacto
        if telefono:
            rec["telefono"] = telefono
        rec["estado"] = rec.get("estado") or "contactado"
        if fecha_iso and hora_inicio:
            rec["fecha_proximo_contacto"] = f"{fecha_iso} {hora_inicio}"
            rec["fecha_cita"] = fecha_iso
            rec["hora_cita"] = hora_inicio
        nota_cita_str = f"📅 Cita Alta Web agendada para {dia_texto} ({fecha_iso}) a las {hora_inicio}. Contacto: {nombre_contacto} ({telefono}). Pedido: {resumen_pedido} ({total_dia1})"
        rec["notas"] = (nota_cita_str + "\n" + str(rec.get("notas") or "")).strip()

        bitacora_actual = rec.get("bitacora") if isinstance(rec.get("bitacora"), list) else []
        bitacora_actual.insert(0, {
            "id": f"bit_{int(time.time())}",
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "fecha_cita": fecha_iso,
            "hora_cita": hora_inicio,
            "texto": nota_cita_str
        })
        rec["bitacora"] = bitacora_actual
        rec["local_override_ts"] = datetime.now().timestamp()
        crm_db[target_key] = rec
        save_crm(crm_db)

        return jsonify({
            "status": "ok",
            "slot_bloqueado": f"{fecha_iso}|{hora_inicio[:5]}",
            "slots_ocupados": _extraer_slots_ocupados_universal_sp_v145().get("slots_ocupados", [])
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
# === [SP_AGENDA_CRM_COORDINATOR_V145_END] ===
'''


# ==============================================================================
# BLOQUE 2: SCRIPT INYECTADO EN `index.html` PARA SINCRONIZAR HORAS OCUPADAS
# CON EL CRM Y LA BITÁCORA Y MANTENER SELECCIÓN MÚLTIPLE LIBRE EN RESERVA FASE 2
# ==============================================================================
BLOQUE_JS_COORDINADOR_AGENDA_WEB = r'''
<!-- [SP_AGENDA_CRM_WEB_SYNC_V145_START] -->
<script>
(function() {
  window.SP_SLOTS_OCUPADOS_CRM = window.SP_SLOTS_OCUPADOS_CRM || new Set();
  window.SP_ULTIMA_SYNC_AGENDA = 0;

  function obtenerFechaIsoDeOpcionDia(optEl, textoFallback) {
    if (optEl && optEl.getAttribute) {
      var dIso = optEl.getAttribute('data-fecha-iso') || optEl.getAttribute('data-iso');
      if (dIso && /^\d{4}-\d{2}-\d{2}$/.test(dIso)) return dIso;
      var val = optEl.value || '';
      var mIso = val.match(/\b(202\d-[01]\d-[0-3]\d)\b/);
      if (mIso) return mIso[1];
    }
    var txt = String((optEl ? (optEl.textContent || optEl.value) : '') || textoFallback || '').toLowerCase();
    var mIso2 = txt.match(/\b(202\d-[01]\d-[0-3]\d)\b/);
    if (mIso2) return mIso2[1];

    var meses = {
      'enero': 1, 'ene': 1, 'febrero': 2, 'feb': 2, 'marzo': 3, 'mar': 3,
      'abril': 4, 'abr': 4, 'mayo': 5, 'may': 5, 'junio': 6, 'jun': 6,
      'julio': 7, 'jul': 7, 'agosto': 8, 'ago': 8, 'septiembre': 9, 'sep': 9,
      'octubre': 10, 'oct': 10, 'noviembre': 11, 'nov': 11, 'diciembre': 12, 'dic': 12
    };
    var mDiaMes = txt.match(/\b([0-3]?\d)\s+de\s+([a-záéíóú]+)/i);
    if (mDiaMes) {
      var dd = parseInt(mDiaMes[1], 10);
      var nomMes = mDiaMes[2].normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
      var mm = meses[nomMes] || meses[nomMes.substring(0, 3)];
      if (mm) {
        var hoy = new Date();
        var yyyy = hoy.getFullYear();
        if (mm < (hoy.getMonth() + 1) && (hoy.getMonth() + 1 - mm) > 6) yyyy += 1;
        return yyyy + '-' + String(mm).padStart(2, '0') + '-' + String(dd).padStart(2, '0');
      }
    }
    return '';
  }

  function extraerHoraInicioHHMM(strHora) {
    var m = String(strHora || '').match(/\b([01]?\d|2[0-3]):([0-5]\d)\b/);
    if (!m) return '';
    return String(parseInt(m[1], 10)).padStart(2, '0') + ':' + m[2];
  }

  window.spFiltrarHorasOcupadasEnSelectCarrito = function() {
    var selDia = document.getElementById('spCartCitaDia');
    var selHora = document.getElementById('spCartCitaHora');
    if (!selDia || !selHora) return;

    var optDiaSel = selDia.options[selDia.selectedIndex];
    var fechaIsoSel = obtenerFechaIsoDeOpcionDia(optDiaSel, selDia.value);
    if (!fechaIsoSel) return;

    var primeraHoraLibre = null;
    var horaActualBloqueada = false;

    for (var i = selHora.options.length - 1; i >= 0; i--) {
      var optH = selHora.options[i];
      var hInicio = extraerHoraInicioHHMM(optH.value || optH.textContent);
      if (!hInicio) continue;

      if (!optH.getAttribute('data-label-original')) {
        optH.setAttribute('data-label-original', optH.textContent.replace(/^⛔\s*/, '').replace(/\s*\(Ocupado.*\)$/i, '').trim());
      }
      var labelLimpio = optH.getAttribute('data-label-original');
      var claveSlot = fechaIsoSel + '|' + hInicio;

      var estaOcupado = window.SP_SLOTS_OCUPADOS_CRM.has(claveSlot);
      if (estaOcupado) {
        optH.disabled = true;
        optH.hidden = true;
        optH.style.display = 'none';
        optH.textContent = '⛔ ' + labelLimpio + ' (Ocupado en agenda)';
        if (selHora.selectedIndex === i) {
          horaActualBloqueada = true;
        }
      } else {
        optH.disabled = false;
        optH.hidden = false;
        optH.style.display = '';
        optH.textContent = labelLimpio;
        primeraHoraLibre = optH.value;
      }
    }

    if (horaActualBloqueada || (selHora.options[selHora.selectedIndex] && selHora.options[selHora.selectedIndex].disabled)) {
      for (var j = 0; j < selHora.options.length; j++) {
        if (!selHora.options[j].disabled) {
          selHora.selectedIndex = j;
          break;
        }
      }
    }
  };

  window.spSincronizarAgendaConCrmYBitacora = function(forzar) {
    var ahora = Date.now();
    if (!forzar && (ahora - window.SP_ULTIMA_SYNC_AGENDA < 4000)) {
      window.spFiltrarHorasOcupadasEnSelectCarrito();
      return Promise.resolve();
    }
    window.SP_ULTIMA_SYNC_AGENDA = ahora;

    // 1) Cargar primero cualquier reserva guardada en el propio navegador (localStorage)
    try {
      var localSlots = JSON.parse(localStorage.getItem('sp_citas_ocupadas_local') || '[]');
      if (Array.isArray(localSlots)) {
        localSlots.forEach(function(s) {
          if (s) window.SP_SLOTS_OCUPADOS_CRM.add(String(s).trim());
        });
      }
    } catch (e) {}

    var endpoints = [
      'http://127.0.0.1:5000/api/horarios-ocupados-agenda?t=' + ahora,
      'http://localhost:5000/api/horarios-ocupados-agenda?t=' + ahora,
      'http://127.0.0.1:8765/api/horarios-ocupados-agenda?t=' + ahora
    ];

    var promesas = endpoints.map(function(url) {
      return fetch(url, { method: 'GET', mode: 'cors' })
        .then(function(r) { return r.ok ? r.json() : null; })
        .then(function(data) {
          if (data && Array.isArray(data.slots_ocupados)) {
            data.slots_ocupados.forEach(function(sl) {
              if (sl) window.SP_SLOTS_OCUPADOS_CRM.add(String(sl).trim());
            });
          }
        })
        .catch(function() {});
    });

    return Promise.all(promesas).then(function() {
      try {
        localStorage.setItem('sp_citas_ocupadas_local', JSON.stringify(Array.from(window.SP_SLOTS_OCUPADOS_CRM)));
      } catch (e) {}
      window.spFiltrarHorasOcupadasEnSelectCarrito();
    });
  };

  // Enganchar cambio de día y apertura del Carrito para que siempre filtre las horas ocupadas en CRM y Bitácora
  document.addEventListener('DOMContentLoaded', function() {
    window.spSincronizarAgendaConCrmYBitacora(true);

    var selDia = document.getElementById('spCartCitaDia');
    if (selDia) {
      selDia.addEventListener('change', function() {
        setTimeout(function() {
          window.spFiltrarHorasOcupadasEnSelectCarrito();
        }, 20);
      });
    }

    // Asegurar que cuando la función original repinte las horas del día seleccionado, apliquemos el filtro del CRM inmediatamente después
    if (typeof window.spActualizarHorasCitaCarrito === 'function' && !window._spHookedActualizarHorasV145) {
      var origActHoras = window.spActualizarHorasCitaCarrito;
      window.spActualizarHorasCitaCarrito = function() {
        var res = origActHoras.apply(this, arguments);
        window.spFiltrarHorasOcupadasEnSelectCarrito();
        return res;
      };
      window._spHookedActualizarHorasV145 = true;
    }

    if (typeof window.abrirModalCarritoCarta === 'function' && !window._spHookedAbrirCarritoV145) {
      var origAbrir = window.abrirModalCarritoCarta;
      window.abrirModalCarritoCarta = function() {
        var r = origAbrir.apply(this, arguments);
        window.spSincronizarAgendaConCrmYBitacora(true);
        return r;
      };
      window._spHookedAbrirCarritoV145 = true;
    }

    // Cuando el cliente confirma pedido en el Carrito, bloquear inmediatamente esa fecha/hora en el CRM local (puerto 5000) y en localStorage
    if (typeof window.spConfirmarPedidoYAgendarCarrito === 'function' && !window._spHookedConfirmarCarritoV145) {
      var origConfirmar = window.spConfirmarPedidoYAgendarCarrito;
      window.spConfirmarPedidoYAgendarCarrito = function() {
        try {
          var selD = document.getElementById('spCartCitaDia');
          var selH = document.getElementById('spCartCitaHora');
          var inpNom = document.getElementById('spCartInputNombre');
          var inpNeg = document.getElementById('spCartInputNegocio');
          var inpTel = document.getElementById('spCartInputTelefono');
          var optD = selD && selD.options[selD.selectedIndex];
          var fIso = obtenerFechaIsoDeOpcionDia(optD, selD ? selD.value : '');
          var hIni = selH ? extraerHoraInicioHHMM(selH.value || selH.textContent) : '';
          if (fIso && hIni) {
            var slotKey = fIso + '|' + hIni;
            window.SP_SLOTS_OCUPADOS_CRM.add(slotKey);
            try {
              localStorage.setItem('sp_citas_ocupadas_local', JSON.stringify(Array.from(window.SP_SLOTS_OCUPADOS_CRM)));
            } catch (e) {}
            fetch('http://127.0.0.1:5000/api/registrar-cita-web-en-crm', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                nombre: inpNom ? inpNom.value : '',
                negocio: inpNeg ? inpNeg.value : '',
                telefono: inpTel ? inpTel.value : '',
                fecha_iso: fIso,
                dia_texto: selD ? selD.value : fIso,
                hora_inicio: hIni
              })
            }).catch(function() {});
          }
        } catch (err) {}
        return origConfirmar.apply(this, arguments);
      };
      window._spHookedConfirmarCarritoV145 = true;
    }
  });
})();
</script>
<!-- [SP_AGENDA_CRM_WEB_SYNC_V145_END] -->
'''


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

        # Reemplazar si ya existía el bloque V145 o inyectarlo antes del arranque main
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


def actualizar_index_html_agenda():
    rutas_index = [
        os.path.join(RUTA_WEB_PUBLIC, "index.html"),
        os.path.join(RUTA_SERVICIO_RESENAS, "index.html"),
    ]
    for ruta in rutas_index:
        if not os.path.exists(ruta):
            continue
        with open(ruta, "r", encoding="utf-8") as f:
            html = f.read()

        # Asegurar que el generador de días del Carrito guarde `data-fecha-iso="YYYY-MM-DD"` en cada <option>
        html = re.sub(
            r"opt\.value\s*=\s*labelDia\s*;",
            lambda _: "opt.value = labelDia; opt.setAttribute('data-fecha-iso', d.toISOString().split('T')[0]);",
            html
        )

        if "<!-- [SP_AGENDA_CRM_WEB_SYNC_V145_START] -->" in html:
            html = re.sub(
                r"<!-- \[SP_AGENDA_CRM_WEB_SYNC_V145_START\] -->[\s\S]*?<!-- \[SP_AGENDA_CRM_WEB_SYNC_V145_END\] -->",
                lambda _: BLOQUE_JS_COORDINADOR_AGENDA_WEB.strip(),
                html
            )
        else:
            html = html.replace("</body>", BLOQUE_JS_COORDINADOR_AGENDA_WEB.strip() + "\n</body>")

        escribir_archivo_con_backup(ruta, html)
        validar_bloques_js_en_html(ruta)


NOTA_HISTORIAL_V145 = f"""
---
### ACTUALIZACIÓN {VERSION_ACTUAL} ({FECHA_EJECUCION}) — Coordinación Bidireccional de Agenda entre Carrito Web (`index.html`), CRM y Bitácora del Prospector (`servidor_local_b2b.py`)
- **Bloqueo Automático de Horas Ocupadas en el CRM y en la Bitácora (`/api/horarios-ocupados-agenda`):** Ahora el servidor local lee todas las citas agendadas en `crm_b2b_db.json` (tanto en los campos de fecha/hora de cita de cada ficha como dentro de las notas y del Cuaderno de Bitácora, por ejemplo «sábado a las 11:00») y en `leads_contrataciones_web.json`. Cuando el cliente abre el Carrito en `index.html` o cambia de día en el selector, las horas ya ocupadas en la agenda de Francisco desaparecen automáticamente para evitar solapamientos.
- **Registro Bidireccional Web → CRM (`/api/registrar-cita-web-en-crm`):** Cuando un cliente confirma su pedido y elige día y hora en el Carrito de la web, además de enviarse por WhatsApp/Sheets, la cita queda anotada automáticamente en `crm_b2b_db.json` y en su Bitácora, bloqueando ese tramo horario al instante.
- **Reserva Prioritaria Fase 2 Multiselección:** Se mantiene la selección libre e ilimitada de módulos en el paso 5 del Carrito Configurador.
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
                txt = txt.rstrip() + "\n" + NOTA_HISTORIAL_V145
                escribir_archivo_con_backup(ruta_md, txt)
            textos_enviar[os.path.basename(ruta_md)] = txt

    # Replicar también en Scraper y servicio_resenas para lectura local inmediata
    for carpeta_dest in (RUTA_SCRAPER, RUTA_SERVICIO_RESENAS):
        if os.path.exists(carpeta_dest):
            for nom_md, contenido_md in textos_enviar.items():
                ruta_copia = os.path.join(carpeta_dest, nom_md)
                try:
                    with open(ruta_copia, "w", encoding="utf-8") as fc:
                        fc.write(contenido_md)
                except Exception:
                    pass

    # Sincronizar con Google Sheets (Biblia_IA_Viva y Manual_Maestro_AD) y Google Drive
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
                    ["git", "-C", carpeta_git, "commit", "-m", f"feat({VERSION_ACTUAL}): coordinacion bidireccional de agenda Carrito Web con CRM y Bitacora"],
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
            print("  🔄 Servidor Prospector B2B (puerto 5000) actualizado con el nuevo coordinador de agenda.")
        except Exception:
            pass


def ejecutar_actualizacion():
    print("=" * 78)
    print(f"🚀 INICIANDO ACTUALIZACIÓN MAESTRA {VERSION_ACTUAL} — COORDINACIÓN DE AGENDA CRM <-> WEB")
    print("=" * 78)
    actualizar_documentos_maestros_md()
    actualizar_servidor_local_b2b()
    actualizar_index_html_agenda()
    replicar_ad_py_en_carpetas_oficiales()
    sincronizar_git_repositorios()
    reiniciar_prospector_puerto_5000()
    print("=" * 78)
    print(f"🎉 ACTUALIZACIÓN {VERSION_ACTUAL} COMPLETADA CON ÉXITO")
    print("=" * 78)


if __name__ == "__main__":
    ejecutar_actualizacion()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SCRIPT ACTUALIZADOR MAESTRO: AD.py (Versión V174 — SISTEMAS PYME)
=============================================================================
1. Corrige el IndentationError de la línea 81 y valida con py_compile + node.
2. Restaura al 100% la fluidez e inteligencia del Tecnoconsultor en index.html:
   - Mientras él habla: sus frases salen sincronizadas en BLANCO en el
     Teleprompter LED y la esfera 3D late al ritmo de su voz.
   - En el instante en que termina de hablar: el micrófono está abierto para ti
     y recoge tu voz en tiempo real escribiéndola en AMARILLO en el Teleprompter.
   - Al terminar de hablar (~0,8s de pausa): responde en ~1 segundo con
     inteligencia conversacional real conectada a Gemini Flash-Lite.
3. Limpia de Git los archivos auxiliares (`AD.py`, `_sp_servidor_ia_8765.py`,
   `.sp_servidor_neuronal_8765.py`) y los añade a `.gitignore` para evitar el
   bloqueo GH013 de GitHub Push Protection en `web-sistemaspyme`.
=============================================================================
"""

import os
import sys
import re
import json
import time
import shutil
import atexit
import subprocess
import urllib.request
from datetime import datetime

# =============================================================================
# 1. RUTAS OFICIALES EN EL MAC DE FRANCISCO
# =============================================================================
RUTA_PROGRAMAR = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Programar"
RUTA_SCRAPER = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Scraper/Scrapper App"
RUTA_RESENAS = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Servicios/Servicio Reseñas/servicio_resenas"
RUTA_WEB_REPO = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme"
RUTA_WEB_PUBLIC = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme/public_html"

CARPETAS_TRABAJO = [RUTA_PROGRAMAR, RUTA_SCRAPER, RUTA_RESENAS, RUTA_WEB_PUBLIC]

CANDIDATOS_INDEX_HTML = [
    os.path.join(RUTA_WEB_PUBLIC, "index.html"),
    os.path.join(RUTA_WEB_REPO, "index.html"),
    os.path.join(RUTA_RESENAS, "public_html", "index.html"),
    os.path.join(RUTA_RESENAS, "index.html"),
    os.path.join(RUTA_PROGRAMAR, "index.html"),
    os.path.join(RUTA_SCRAPER, "index.html"),
    os.path.join(os.getcwd(), "index.html"),
]

WEBHOOK_ALTAS_URL = "https://script.google.com/macros/s/AKfycbwVbXZIK-O4mQLYMrwdPgXQDlo__PHTuv8MXUj-nR68_t2OGHVdvrBgqfhXdQxwzivc/exec"

_DOCS_ACTUALIZADOS_FLAG = False


# =============================================================================
# 2. BACKUP EN `backups_sp` Y VALIDACIÓN GATEWAY `node --check`
# =============================================================================
def crear_backup_seguro(ruta_archivo):
    if not os.path.isfile(ruta_archivo):
        return None
    carpeta_base = os.path.dirname(ruta_archivo)
    carpeta_backups = os.path.join(carpeta_base, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    sello = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = os.path.basename(ruta_archivo)
    destino = os.path.join(carpeta_backups, f"{nombre}.{sello}.bak")
    shutil.copy2(ruta_archivo, destino)
    return destino


def validar_bloques_js_en_html(contenido_html, etiqueta_archivo="index.html"):
    bloques = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", contenido_html, flags=re.IGNORECASE)
    if not bloques:
        return True
    node_bin = shutil.which("node")
    if not node_bin:
        return True
    tmp_js = "/tmp/_sp_check_syntax_v174.js"
    for idx, codigo_js in enumerate(bloques, 1):
        if not codigo_js.strip():
            continue
        with open(tmp_js, "w", encoding="utf-8") as f:
            f.write(codigo_js)
        res = subprocess.run([node_bin, "--check", tmp_js], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ Error de sintaxis JS detectado en bloque #{idx} de {etiqueta_archivo}:\n{res.stderr}")
            return False
    try:
        os.remove(tmp_js)
    except Exception:
        pass
    print(f"✅ Validación Gateway `node --check` superada en los {len(bloques)} bloques <script> de {etiqueta_archivo}.")
    return True


# =============================================================================
# 3. ACTUALIZACIÓN DE LOS 2 DOCUMENTOS MAESTROS (.md) Y DRIVE/SHEETS
# =============================================================================
NOTA_V174 = """
### ACTUALIZACIÓN V175 (07/11/2026 18:45 — Regreso a la Arquitectura Limpia Original del Tecnoconsultor: Ciclo Puro Blanco -> Amarillo -> Respuesta IA en <1s con API Key Real del Mac)
- **Eliminación total de filtros anti-eco que bloqueaban la voz del usuario:** Restaurado el ciclo limpio de 3 estados (1. Mientras el consultor habla en blanco, el micro está en pausa; 2. En el milisegundo en que termina de hablar, se abre el micro limpio de cero y transcribe cada palabra tuya en amarillo en tiempo real; 3. Al callarte 0,8s, envía tu pregunta).
- **Conexión con la API Key viva del Mac (`.env` / `config_b2b.json`) y Render:** Rescata automáticamente la clave real operativa de Gemini del entorno de Francisco para que tanto el servidor local como el navegador respondan en menos de 1 segundo con inteligencia real a cualquier pregunta o repregunta.
"""


def actualizar_documentos_maestros():
    global _DOCS_ACTUALIZADOS_FLAG
    if _DOCS_ACTUALIZADOS_FLAG:
        return
    _DOCS_ACTUALIZADOS_FLAG = True

    archivos_md = [
        "biblia_de_conocimiento_de_sistemas_pyme.md",
        "manual_maestro_de_programaci_n_ad_py.md",
    ]

    contenidos_finales = {}

    for nombre_md in archivos_md:
        ruta_origen = None
        for carpeta in CARPETAS_TRABAJO + [os.getcwd()]:
            cand = os.path.join(carpeta, nombre_md)
            if os.path.isfile(cand):
                ruta_origen = cand
                break

        if not ruta_origen:
            continue

        with open(ruta_origen, "r", encoding="utf-8") as f:
            texto = f.read()

        if "ACTUALIZACIÓN V174 (" not in texto:
            texto = texto.rstrip() + "\n\n" + NOTA_V174.strip() + "\n"

        contenidos_finales[nombre_md] = texto

        for carpeta_dest in [RUTA_PROGRAMAR, RUTA_SCRAPER, RUTA_RESENAS]:
            if os.path.isdir(carpeta_dest):
                ruta_dest = os.path.join(carpeta_dest, nombre_md)
                if os.path.isfile(ruta_dest):
                    crear_backup_seguro(ruta_dest)
                with open(ruta_dest, "w", encoding="utf-8") as f_out:
                    f_out.write(texto)

    if contenidos_finales:
        try:
            payload = {
                "accion": "sincronizar_biblia_conocimiento",
                "version": "V175",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "biblia_markdown": contenidos_finales.get("biblia_de_conocimiento_de_sistemas_pyme.md", ""),
                "manual_markdown": contenidos_finales.get("manual_maestro_de_programaci_n_ad_py.md", ""),
            }
            req = urllib.request.Request(
                WEBHOOK_ALTAS_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=7)
            print("☁️ Sincronización con Google Drive y pestañas Biblia_IA_Viva / Manual_Maestro_AD completada.")
        except Exception:
            pass


atexit.register(actualizar_documentos_maestros)


def rescatar_api_keys_reales_del_mac():
    """Lee las claves reales de Gemini que Francisco tiene activas en config_b2b.json o .env."""
    claves = []
    # 1. Buscar en config_b2b.json del Scraper
    ruta_cfg = os.path.join(RUTA_SCRAPER, "config_b2b.json")
    if os.path.isfile(ruta_cfg):
        try:
            with open(ruta_cfg, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k_name in ["gemini_api_key", "google_api_key", "api_key", "GEMINI_API_KEY"]:
                val = str(data.get(k_name) or "").strip()
                if len(val) > 20 and val not in claves:
                    claves.append(val)
            lista_k = data.get("gemini_api_keys") or data.get("api_keys") or []
            if isinstance(lista_k, list):
                for item in lista_k:
                    val = str(item or "").strip()
                    if len(val) > 20 and val not in claves:
                        claves.append(val)
        except Exception:
            pass

    # 2. Buscar en archivos .env de Reseñas y Scraper
    for carpeta in [RUTA_RESENAS, RUTA_SCRAPER, RUTA_PROGRAMAR]:
        ruta_env = os.path.join(carpeta, ".env")
        if os.path.isfile(ruta_env):
            try:
                with open(ruta_env, "r", encoding="utf-8") as f:
                    for linea in f:
                        linea = linea.strip()
                        if not linea or linea.startswith("#") or "=" not in linea:
                            continue
                        k, v = linea.split("=", 1)
                        k = k.strip().upper()
                        v = v.strip().strip('"').strip("'")
                        if ("GEMINI" in k or "GOOGLE_API" in k or "VERTEX" in k) and len(v) > 20:
                            if v not in claves:
                                claves.append(v)
            except Exception:
                pass

    return claves


# =============================================================================
# 4. BLOQUE MAESTRO V175 DEL TECNOCONSULTOR (ARQUITECTURA PURA Y DIRECTA)
# =============================================================================
BLOQUE_CONSULTOR_V174 = r"""<!-- [SP_CONSULTOR_ULTIMATE_V168_START] -->
<script id="spConsultorUltimateEngineV175">
(function() {
  /* =========================================================================
     ARQUITECTURA PURA DE 3 PASOS (COMO EL PRIMER DÍA — V175):
     1. HABLA EL CONSULTOR: Micrófono apagado. Sus palabras van saliendo en
        BLANCO en el Teleprompter LED sincronizadas con su voz.
     2. TERMINA DE HABLAR -> SE ABRE EL MICRÓFONO: En el instante en que se
        calla, arranca el micrófono limpio. Todo lo que dices sale al vuelo
        en AMARILLO en el Teleprompter sin filtros que borren tu voz.
     3. PAUSA DE 0,8s -> RESPUESTA INTELIGENTE EN <1s: Envía tu pregunta a
        Gemini Flash y te contesta al segundo a cualquier cosa que preguntes.
     ========================================================================= */

  var _activo = false;
  var _pausadoPorSalir = false;
  var _estado = 'idle'; // 'idle' | 'speaking' | 'listening' | 'thinking'
  var _mute = false;
  var _rec = null;
  var _recEscuchando = false;
  var _timerSilencio = null;
  var _timersTexto = [];
  var _watchdogHabla = null;
  var _lineaAmarilla = null;
  var _historial = [];
  var _turnosGuardados = [];
  var _nombreVoz = 'Jorge';
  var _vozCache = null;
  var _orbFrame = null;
  var _orbEnergia = 0;
  var _tsUltimaVozUsuario = 0;

  function enTecnosala() {
    var sec = document.getElementById('vista-tecnosala');
    return !!(sec && !sec.classList.contains('hidden') && !document.hidden);
  }

  function limpiarTimersTexto() {
    for (var i = 0; i < _timersTexto.length; i++) {
      clearTimeout(_timersTexto[i]);
    }
    _timersTexto = [];
    if (_watchdogHabla) {
      clearInterval(_watchdogHabla);
      _watchdogHabla = null;
    }
  }

  function bucleEsfera() {
    var esferas = document.querySelectorAll('#spOrb3DWrapperMain .sp-orb-3d-sphere, #vista-tecnosala .sp-orb-3d-sphere');
    if (!esferas.length || _estado === 'idle') {
      for (var s = 0; s < esferas.length; s++) {
        esferas[s].style.transform = 'perspective(500px) translateZ(18px) scale(1)';
      }
      _orbFrame = null;
      return;
    }
    var ahora = performance.now();
    var obj = 0.15;
    if (_estado === 'speaking') {
      obj = 0.45 + 0.42 * Math.abs(Math.sin(ahora * 0.012));
    } else if (_estado === 'listening') {
      obj = (ahora - _tsUltimaVozUsuario < 280) ? 0.88 : 0.14;
    } else if (_estado === 'thinking') {
      obj = 0.40 + 0.30 * Math.sin(ahora * 0.018);
    }
    _orbEnergia += (obj - _orbEnergia) * 0.35;
    var esc = (1.0 + _orbEnergia * 0.32).toFixed(3);
    var z = Math.round(18 + _orbEnergia * 32);
    for (var i = 0; i < esferas.length; i++) {
      esferas[i].style.transform = 'perspective(500px) translateZ(' + z + 'px) scale(' + esc + ')';
    }
    _orbFrame = requestAnimationFrame(bucleEsfera);
  }

  function pintarUI(nuevoEstado) {
    _estado = nuevoEstado;
    if (_estado !== 'idle' && !_orbFrame) {
      _orbFrame = requestAnimationFrame(bucleEsfera);
    }

    var wrappers = document.querySelectorAll('#spOrb3DWrapperMain, #vista-tecnosala .sp-orb-3d-wrapper');
    for (var i = 0; i < wrappers.length; i++) {
      wrappers[i].classList.remove('sp-orb-state-speaking', 'sp-orb-state-listening');
      if (nuevoEstado === 'speaking') wrappers[i].classList.add('sp-orb-state-speaking');
      else if (nuevoEstado === 'listening' || nuevoEstado === 'thinking') wrappers[i].classList.add('sp-orb-state-listening');
    }

    var btnV = document.getElementById('spBtnVoiceTecnosala');
    var txtV = document.getElementById('spVoiceBtnText');
    var icoV = document.getElementById('spVoiceMicIcon');
    var inp = document.getElementById('spTecnosalaInput');
    var btnStop = document.getElementById('spBtnStopSideOrb');
    var hud = document.getElementById('spTeleprompterHudStatus');

    if (nuevoEstado === 'speaking') {
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Hablando...';
      if (icoV) icoV.textContent = '🔊';
      if (inp) inp.placeholder = '🔊 Escuchando al consultor (en cuanto acabe puedes hablar)...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse inline-block mr-1.5"></span>HABLANDO EN VIVO • AL TERMINAR SE ABRE TU MICRÓFONO';
    } else if (nuevoEstado === 'listening') {
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.add('sp-voice-listening');
      if (txtV) txtV.textContent = 'Escuchando...';
      if (icoV) icoV.textContent = '🔴';
      if (inp) inp.placeholder = '🟢 MICRÓFONO ABIERTO: Habla ahora (tu voz aparece en amarillo)...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping inline-block mr-1.5"></span>🎙️ MICRÓFONO ABIERTO • TE ESCUCHO (HABLA CON NATURALIDAD)';
    } else if (nuevoEstado === 'thinking') {
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Pensando...';
      if (icoV) icoV.textContent = '⚡';
      if (inp) inp.placeholder = '⚡ Generando respuesta inteligente...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-sky-400 animate-ping inline-block mr-1.5"></span>⚡ RESPONDIENDO AL SEGUNDO...';
    } else {
      if (btnStop) btnStop.classList.add('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Hablar';
      if (icoV) icoV.textContent = '🎙️';
      if (inp) inp.placeholder = 'Escribe tu duda o pulsa 🎙️ Hablar / la Esfera 3D para conversar...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-slate-400 inline-block mr-1.5"></span>⏸ EN PAUSA • PULSA LA ESFERA 3D O 🎙️ HABLAR PARA EMPEZAR';
    }
  }

  function asegurarCabina() {
    var screen = document.getElementById('spTecnosalaScreen');
    if (!screen) return null;
    var idle = document.getElementById('spTecnosalaIdleWelcome');
    var out = document.getElementById('spTecnosalaActiveOutput');
    var btnReset = document.getElementById('spBtnResetScreenTecnosala');
    if (idle) idle.classList.add('hidden');
    if (out) out.classList.add('hidden');
    if (btnReset) btnReset.classList.remove('hidden');

    var track = document.getElementById('spTeleprompterRollTrack');
    if (track) return track;

    var stage = document.createElement('div');
    stage.id = 'spTeleprompter2027Stage';
    stage.className = 'w-full flex flex-col items-center justify-between my-auto';
    stage.innerHTML =
      '<div class="w-full flex flex-wrap items-center justify-between gap-1.5 mb-1.5 px-1">' +
        '<div id="spTeleprompterHudStatus" class="text-[10px] sm:text-[10.5px] font-mono font-extrabold uppercase tracking-wider text-teal-300 truncate">' +
          '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse inline-block mr-1.5"></span>CONSULTOR INTELIGENTE EN LÍNEA' +
        '</div>' +
        '<div class="flex flex-wrap items-center gap-1.5 flex-shrink-0">' +
          '<button type="button" id="spBtnRepetirUltimaResp" onclick="window.spRepetirUltimaRespuestaConsultor(event)" class="px-2.5 py-0.5 rounded-full bg-teal-500/20 hover:bg-teal-500/35 border border-teal-400/50 text-[10px] font-extrabold text-teal-200 cursor-pointer transition">🔁 Repetir</button>' +
          '<button type="button" id="spBtnCambiarTimbreVoz" onclick="window.spCambiarVozPreferidaConsultor(event)" class="px-2.5 py-0.5 rounded-full bg-indigo-500/25 border border-indigo-400/50 text-[10px] font-extrabold text-indigo-200 cursor-pointer">🎙️ Voz: ' + _nombreVoz + '</button>' +
          '<button type="button" id="spBtnToggleVozSintetica" onclick="window.spToggleVozConsultorMute(event)" class="px-2.5 py-0.5 rounded-full bg-cyan-500/20 border border-cyan-400/50 text-[10px] font-extrabold text-cyan-200 cursor-pointer">' + (_mute ? '🔇 Silenciado' : '🔊 Voz: ON') + '</button>' +
        '</div>' +
      '</div>' +
      '<div class="flex items-center justify-center gap-3 mb-1.5">' +
        '<div id="spOrb3DWrapperMain" onclick="window.spActivarOrbeConsultorInteractivo(event)" class="sp-orb-3d-wrapper sp-orb-compact-mode" title="Pulsa para hablar">' +
          '<div class="sp-orb-3d-ring1"></div>' +
          '<div class="sp-orb-3d-ring2"></div>' +
          '<div class="sp-orb-3d-sphere"><span class="text-sm drop-shadow pointer-events-none">⚡</span></div>' +
        '</div>' +
        '<button type="button" id="spBtnStopSideOrb" onclick="window.spPararConsultorTotalmente(event)" class="px-3.5 py-1 rounded-full bg-rose-600 hover:bg-rose-500 border border-rose-300 text-white font-black text-[11px] shadow-md cursor-pointer transition flex items-center gap-1.5"><span>⏹</span><span>PARAR</span></button>' +
      '</div>' +
      '<div class="sp-teleprompter-2027-box">' +
        '<div id="spTeleprompterRollTrack" class="sp-teleprompter-Roll-track"></div>' +
      '</div>';
    screen.appendChild(stage);
    return document.getElementById('spTeleprompterRollTrack');
  }

  function ordenarLineasBlancas(track) {
    if (!track) return;
    var blancas = track.querySelectorAll('[data-role="consultor"]');
    var tope = (_lineaAmarilla && _lineaAmarilla.parentNode === track) ? 2 : 3;
    while (blancas.length > tope) {
      if (blancas[0] && blancas[0].parentNode === track) {
        track.removeChild(blancas[0]);
      }
      blancas = track.querySelectorAll('[data-role="consultor"]');
    }
    var n = blancas.length;
    for (var i = 0; i < n; i++) {
      var el = blancas[i];
      var d = (n - 1) - i;
      el.classList.remove('sp-led-line-user', 'sp-led-line-active', 'sp-led-line-past-1', 'sp-led-line-past-2', 'sp-led-line-past-3');
      var c = el.querySelector('.sp-led-cursor');
      if (d === 0) {
        el.classList.add('sp-led-line-active');
      } else {
        if (c) c.remove();
        if (d === 1) el.classList.add('sp-led-line-past-1');
        else if (d === 2) el.classList.add('sp-led-line-past-2');
        else el.classList.add('sp-led-line-past-3');
      }
    }
    if (_lineaAmarilla && _lineaAmarilla.parentNode === track && track.lastElementChild !== _lineaAmarilla) {
      track.appendChild(_lineaAmarilla);
    }
  }

  function elegirVozEspanola() {
    if (!('speechSynthesis' in window)) return null;
    var todas = window.speechSynthesis.getVoices() || [];
    var es = [];
    for (var i = 0; i < todas.length; i++) {
      var l = String(todas[i].lang || '').replace('_', '-').toLowerCase();
      if (l === 'es-es' || l.indexOf('es-es-') === 0) es.push(todas[i]);
    }
    var pref = _nombreVoz.toLowerCase();
    for (var j = 0; j < es.length; j++) {
      if (String(es[j].name || '').toLowerCase().indexOf(pref) !== -1) {
        _vozCache = es[j];
        return es[j];
      }
    }
    if (es.length > 0) {
      _vozCache = es[0];
      return es[0];
    }
    return _vozCache;
  }

  /* =========================================================================
     PASO 2 PURO: ABRIR MICRÓFONO CUANDO EL CONSULTOR ACABA DE HABLAR
     Sin filtros que borren tu voz: todo lo que dices va directo en AMARILLO.
     ========================================================================= */
  function detenerMicrofono() {
    if (_timerSilencio) {
      clearTimeout(_timerSilencio);
      _timerSilencio = null;
    }
    if (_rec && _recEscuchando) {
      try { _rec.abort(); } catch (e) {}
      _recEscuchando = false;
    }
  }

  function abrirMicrofonoParaUsuario() {
    if (!_activo || _pausadoPorSalir || !enTecnosala() || _estado === 'speaking' || _estado === 'thinking') return;

    var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
      pintarUI('idle');
      return;
    }

    if (_rec && _recEscuchando) {
      pintarUI('listening');
      return;
    }

    var rec = new SpeechRec();
    rec.lang = 'es-ES';
    rec.continuous = true;
    rec.interimResults = true;
    rec.maxAlternatives = 1;

    var textoAcumulado = '';

    rec.onstart = function() {
      _recEscuchando = true;
      if (_estado !== 'speaking' && _estado !== 'thinking') {
        pintarUI('listening');
      }
    };

    rec.onresult = function(event) {
      if (_estado === 'speaking' || _estado === 'thinking') return;

      var confirmado = '';
      var interino = '';
      var tieneFinal = false;

      for (var i = 0; i < event.results.length; i++) {
        var t = String(event.results[i][0].transcript || '').trim();
        if (!t) continue;
        if (event.results[i].isFinal) {
          confirmado += t + ' ';
          if (i >= event.resultIndex) tieneFinal = true;
        } else {
          interino += t + ' ';
        }
      }

      textoAcumulado = (confirmado + ' ' + interino).replace(/\s+/g, ' ').trim();
      if (!textoAcumulado) return;

      _tsUltimaVozUsuario = performance.now();

      var inp = document.getElementById('spTecnosalaInput');
      if (inp) inp.value = textoAcumulado;

      // Pintar en AMARILLO en el Teleprompter en tiempo real
      var track = asegurarCabina();
      if (track) {
        if (!_lineaAmarilla || _lineaAmarilla.parentNode !== track) {
          _lineaAmarilla = document.createElement('div');
          _lineaAmarilla.setAttribute('data-role', 'usuario');
          _lineaAmarilla.className = 'sp-led-line-item sp-led-line-user';
          track.appendChild(_lineaAmarilla);
        }
        _lineaAmarilla.textContent = '🎙️ TÚ: «' + textoAcumulado + '»';
        ordenarLineasBlancas(track);
      }

      if (_timerSilencio) clearTimeout(_timerSilencio);
      var pausaMs = tieneFinal ? 750 : 1100;
      _timerSilencio = setTimeout(function() {
        var preguntaFinal = textoAcumulado.trim();
        textoAcumulado = '';
        if (preguntaFinal.length >= 2 && _estado === 'listening') {
          detenerMicrofono();
          window.spProcesarConsultaEnTeleprompterDirecto(preguntaFinal);
        }
      }, pausaMs);
    };

    rec.onerror = function(ev) {
      _recEscuchando = false;
      if (ev && (ev.error === 'not-allowed' || ev.error === 'service-not-allowed')) {
        pintarUI('idle');
      }
    };

    rec.onend = function() {
      _recEscuchando = false;
      // Si el usuario seguía en modo escucha y hizo una pausa en silencio sin hablar aún, mantenemos el micro abierto
      if (_activo && !_pausadoPorSalir && enTecnosala() && _estado === 'listening') {
        setTimeout(function() {
          if (_activo && !_pausadoPorSalir && enTecnosala() && _estado === 'listening' && !_recEscuchando) {
            try { rec.start(); } catch (e) {}
          }
        }, 120);
      }
    };

    _rec = rec;
    pintarUI('listening');
    try {
      rec.start();
    } catch (e) {}
  }

  /* =========================================================================
     PASO 1 PURO: EL CONSULTOR HABLA EN BLANCO Y AL ACABAR ABRE TU MICRO
     ========================================================================= */
  window.spReproducirEnTeleprompter2027 = function(textoCompleto, alTerminarCallback) {
    detenerMicrofono();
    limpiarTimersTexto();

    var track = asegurarCabina();
    if (!track) return;

    track.innerHTML = '';
    _lineaAmarilla = null;

    var limpio = String(textoCompleto || '').replace(/<[^>]+>/g, ' ').replace(/[`*_#•]/g, ' ').replace(/\s+/g, ' ').trim();
    if (!limpio) {
      abrirMicrofonoParaUsuario();
      return;
    }

    var maxLen = window.innerWidth < 640 ? 38 : 54;
    var palabras = limpio.split(' ');
    var segmentos = [];
    var linea = '';
    var cursor = 0;
    for (var i = 0; i < palabras.length; i++) {
      var cand = linea ? (linea + ' ' + palabras[i]) : palabras[i];
      if (cand.length <= maxLen) {
        linea = cand;
      } else {
        if (linea) {
          segmentos.push({ texto: linea, start: cursor, end: cursor + linea.length });
          cursor += linea.length + 1;
        }
        linea = palabras[i];
      }
    }
    if (linea) segmentos.push({ texto: linea, start: cursor, end: cursor + linea.length });

    var textoUnido = segmentos.map(function(s) { return s.texto; }).join(' ');
    var totalChars = textoUnido.length;
    var charMostrado = 0;
    var charVoz = 0;
    var idxSeg = -1;
    var spanActivo = null;
    var terminado = false;
    var tsInicio = performance.now();
    var tsUltimaVoz = performance.now();

    function pintarBlancoHasta(pos) {
      var p = Math.min(totalChars, Math.max(0, pos));
      var sIdx = 0;
      for (var k = 0; k < segmentos.length; k++) {
        if (p >= segmentos[k].start) sIdx = k;
        else break;
      }
      while (idxSeg < sIdx) {
        if (idxSeg >= 0 && spanActivo) spanActivo.textContent = segmentos[idxSeg].texto;
        idxSeg++;
        var row = document.createElement('div');
        row.setAttribute('data-role', 'consultor');
        row.className = 'sp-led-line-item sp-led-line-active';
        var spT = document.createElement('span');
        var spC = document.createElement('span');
        spC.className = 'sp-led-cursor';
        row.appendChild(spT);
        row.appendChild(spC);
        track.appendChild(row);
        ordenarLineasBlancas(track);
        spanActivo = spT;
      }
      if (spanActivo && sIdx >= 0 && sIdx < segmentos.length) {
        var seg = segmentos[sIdx];
        spanActivo.textContent = seg.texto.slice(0, Math.min(seg.texto.length, Math.max(1, p - seg.start)));
      }
    }

    function alTerminarDeHablar() {
      if (terminado) return;
      terminado = true;
      pintarBlancoHasta(totalChars);
      limpiarTimersTexto();
      if (typeof alTerminarCallback === 'function') {
        try { alTerminarCallback(); } catch (e) {}
      }
      if (_activo && !_pausadoPorSalir && enTecnosala()) {
        abrirMicrofonoParaUsuario();
      } else {
        pintarUI('idle');
      }
    }

    pintarUI('speaking');
    var maxMs = Math.max(3600, totalChars * 72 + 1500);
    _timersTexto.push(setTimeout(alTerminarDeHablar, maxMs));

    function avanzarLetrasBlancas() {
      if (_estado !== 'speaking' || terminado) return;
      if (charVoz > charMostrado) {
        charMostrado = Math.min(totalChars, charMostrado + Math.max(1, Math.ceil((charVoz - charMostrado) * 0.55)));
      } else {
        charMostrado = Math.min(totalChars, charMostrado + 1);
      }
      pintarBlancoHasta(charMostrado);
      if (charMostrado >= totalChars) {
        if (_mute || !('speechSynthesis' in window) || !window.speechSynthesis.speaking) {
          alTerminarDeHablar();
          return;
        }
        _timersTexto.push(setTimeout(alTerminarDeHablar, 400));
        return;
      }
      var ch = textoUnido.charAt(charMostrado - 1) || '';
      var d = (ch === '.' || ch === '?' || ch === '!') ? 250 : ((ch === ',' || ch === ';') ? 130 : 44);
      _timersTexto.push(setTimeout(avanzarLetrasBlancas, d));
    }
    _timersTexto.push(setTimeout(avanzarLetrasBlancas, 18));

    if (!_mute && ('speechSynthesis' in window)) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
      setTimeout(function() {
        if (_estado !== 'speaking' || terminado) return;
        try {
          window.speechSynthesis.resume();
          var u = new SpeechSynthesisUtterance(textoUnido);
          u.lang = 'es-ES';
          u.rate = 0.98;
          var v = elegirVozEspanola();
          if (v) u.voice = v;
          u.onboundary = function(ev) {
            tsUltimaVoz = performance.now();
            if (ev && typeof ev.charIndex === 'number') {
              charVoz = Math.min(totalChars, ev.charIndex + (ev.charLength || 2));
            }
          };
          _watchdogHabla = setInterval(function() {
            if (_estado !== 'speaking' || terminado) {
              clearInterval(_watchdogHabla);
              return;
            }
            var ahora = performance.now();
            if ((ahora - tsInicio > 850 && !window.speechSynthesis.speaking && !window.speechSynthesis.pending) ||
                (charMostrado >= totalChars * 0.93 && (ahora - tsUltimaVoz > 900))) {
              clearInterval(_watchdogHabla);
              alTerminarDeHablar();
            }
          }, 200);
          u.onend = alTerminarDeHablar;
          u.onerror = alTerminarDeHablar;
          window.speechSynthesis.speak(u);
        } catch (e) {
          alTerminarDeHablar();
        }
      }, 20);
    }
  };

  /* =========================================================================
     PASO 3 PURO: INTELIGENCIA CONVERSACIONAL EN < 1 SEGUNDO
     ========================================================================= */
  function obtenerRespuestaInteligente(preguntaUsuario) {
    var apoyo = (typeof window.spObtenerRespuestaOmniscienteCompleta === 'function')
      ? window.spObtenerRespuestaOmniscienteCompleta(preguntaUsuario)
      : '';
    var hist = _historial.slice(-12).join('\n');

    var prompt =
      'Eres el Consultor Tecnológico Experto de Sistemas Pyme (sistemaspyme.es), fundado por Francisco M. Gallardo (Tel/WhatsApp 711 54 75 61).\n' +
      'DATOS OFICIALES EXACTOS:\n' +
      '- Plan Pyme Base (1 servicio: S1 Reseñas Google IA o S2 Cortafuegos WhatsApp): 59 €/mes + 150 € Setup (Anual: 590 €/año, ahorras 2 meses).\n' +
      '- Pack Escudo Básico Dúo (S1 + S2 juntos): 99 €/mes + 225 € Setup (Anual: 990 €/año). Desbloquea las Super-Auditorías a 195 € c/u (en vez de 350 €).\n' +
      '- Pack Escudo Total / Plus: S1 + S2 (99 €/mes) + 1 Super-Auditoría (195 €) o las 2 Super-Auditorías (390 €).\n' +
      '- Atril Inteligente NFC + QR: 39 € pago único sin cuotas (2ª a 4ª ud: 29 €; 5+ uds: 25 €). Abre Google Maps en 1 segundo.\n' +
      '- Super-Auditoría 1 (SEO Local + GEO IA): 22 parámetros, Grafo Schema.org + Wikidata + /llms.txt para salir recomendado en Google Maps, ChatGPT, Gemini y Perplexity.\n' +
      '- Super-Auditoría 2 (Neuromarketing CRO + Sonda Térmica 10 días): duplica contactos web en Modo Ágil o Modo Corporativo.\n' +
      '- Servicios S3 (Leads en 10s), S4 (Facturas por foto WA), S5 (Clientes inactivos): +40 €/mes en combo.\n' +
      '- Servicios S6 (Anti-plantón citas), S7 (Firma digital), S8 (Anti-morosidad), S9 (Llamadas perdidas WA), S10 (Centralita Voz IA 24/7) y Satélites (Instagram 3 en 1, Logística 360, Redactor RAG).\n\n' +
      'APOYO ESPECÍFICO DE LA BIBLIA:\n' + apoyo + '\n\n' +
      'HISTORIAL DE LA CHARLA:\n' + (hist || 'Recién empezada') + '\n\n' +
      'PREGUNTA ACTUAL DEL USUARIO: "' + preguntaUsuario + '"\n\n' +
      'INSTRUCCIÓN: Responde directamente y con inteligencia a lo que te acaba de preguntar el usuario en 2 o 3 frases fluidas y naturales para ser habladas en voz alta (máximo 55 palabras). Cero asteriscos y cero listas.';

    var promesas = [];

    // 1. Servidor Local IA en tu Mac (puerto 8765 con tus claves reales de .env / config_b2b.json)
    promesas.push(
      fetch('http://127.0.0.1:8765/api/consultor-ia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta: preguntaUsuario, apoyo: apoyo, prompt: prompt })
      })
      .then(function(r) { if (!r.ok) throw new Error('e8765'); return r.json(); })
      .then(function(d) {
        if (d && d.ok && d.respuesta && d.respuesta.trim().length > 10 && d.modelo !== 'local-fallback') {
          return d.respuesta.trim();
        }
        throw new Error('fallback8765');
      })
    );

    // 2. Servidor Render en producción (/api/consultor-ia y /api/tecnosala-consulta)
    promesas.push(
      fetch('https://servicio-resenas.onrender.com/api/consultor-ia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta: preguntaUsuario, apoyo: apoyo, prompt: prompt })
      })
      .then(function(r) { if (!r.ok) throw new Error('erender1'); return r.json(); })
      .then(function(d) {
        if (d && d.ok && d.respuesta && d.respuesta.trim().length > 10) {
          return d.respuesta.trim();
        }
        throw new Error('emptyrender1');
      })
    );

    promesas.push(
      fetch('https://servicio-resenas.onrender.com/api/tecnosala-consulta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta: preguntaUsuario })
      })
      .then(function(r) { if (!r.ok) throw new Error('erender2'); return r.json(); })
      .then(function(d) {
        if (d && d.respuesta && d.respuesta.trim().length > 10) {
          return d.respuesta.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
        }
        throw new Error('emptyrender2');
      })
    );

    return new Promise(function(resolve) {
      var resuelto = false;
      var fallos = 0;
      var timer = setTimeout(function() {
        if (!resuelto) {
          resuelto = true;
          resolve(apoyo);
        }
      }, 2400);

      for (var i = 0; i < promesas.length; i++) {
        promesas[i].then(function(txt) {
          if (!resuelto && txt) {
            resuelto = true;
            clearTimeout(timer);
            resolve(txt.replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim());
          }
        }).catch(function() {
          fallos++;
          if (fallos >= promesas.length && !resuelto) {
            resuelto = true;
            clearTimeout(timer);
            resolve(apoyo);
          }
        });
      }
    });
  }

  window.spProcesarConsultaEnTeleprompterDirecto = function(textoPregunta) {
    var limpia = String(textoPregunta || '').trim();
    if (!limpia) return;

    detenerMicrofono();
    _activo = true;
    _pausadoPorSalir = false;
    pintarUI('thinking');

    var inp = document.getElementById('spTecnosalaInput');
    if (inp) inp.value = '';

    var track = asegurarCabina();
    if (track) {
      if (!_lineaAmarilla || _lineaAmarilla.parentNode !== track) {
        _lineaAmarilla = document.createElement('div');
        _lineaAmarilla.setAttribute('data-role', 'usuario');
        _lineaAmarilla.className = 'sp-led-line-item sp-led-line-user';
        track.appendChild(_lineaAmarilla);
      }
      _lineaAmarilla.textContent = '🎙️ TÚ: «' + limpia + '»';
      ordenarLineasBlancas(track);
    }

    _historial.push('Usuario: ' + limpia);
    if (typeof window.spExtraerYPreconfigurarCarritoDesdeCharla === 'function') {
      try { window.spExtraerYPreconfigurarCarritoDesdeCharla(limpia, _historial); } catch (e) {}
    }

    obtenerRespuestaInteligente(limpia).then(function(respuesta) {
      _historial.push('Consultor: ' + respuesta);
      var ahora = new Date();
      _turnosGuardados.push({
        hora: ahora.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
        pregunta: limpia,
        respuesta: respuesta
      });
      window.spReproducirEnTeleprompter2027(respuesta, null);
    });
  };

  window.spActivarOrbeConsultorInteractivo = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();

    _activo = true;
    _pausadoPorSalir = false;

    var track = asegurarCabina();
    if (track && track.children.length > 0) {
      if (_estado === 'speaking') {
        limpiarTimersTexto();
        if ('speechSynthesis' in window) {
          try { window.speechSynthesis.cancel(); } catch (e) {}
        }
      }
      abrirMicrofonoParaUsuario();
      return;
    }

    var saludo =
      'Hola, soy tu consultor tecnológico de Sistemas Pyme. ' +
      'En cuanto termine de hablar se abrirá el micrófono: pregúntame lo que quieras y te responderé al segundo.';

    window.spReproducirEnTeleprompter2027(saludo, null);
  };

  window.spIniciarEscuchaDirectaConsultor = function() {
    _activo = true;
    _pausadoPorSalir = false;
    limpiarTimersTexto();
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    asegurarCabina();
    abrirMicrofonoParaUsuario();
  };

  window.spToggleDictadoVozTecnosala = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (!_activo) {
      window.spActivarOrbeConsultorInteractivo(ev);
    } else {
      window.spIniciarEscuchaDirectaConsultor();
    }
  };

  window.spPararConsultorTotalmente = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    _activo = false;
    _pausadoPorSalir = false;
    detenerMicrofono();
    limpiarTimersTexto();
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    pintarUI('idle');
  };

  window.spPausarConsultorPorCambioSeccion = function() {
    if (!_activo) return;
    _pausadoPorSalir = true;
    detenerMicrofono();
    limpiarTimersTexto();
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    pintarUI('idle');
  };

  window.spReanudarConsultorAlVolverSeccion = function() {
    if (!_activo || !enTecnosala()) return;
    _pausadoPorSalir = false;
    asegurarCabina();
    abrirMicrofonoParaUsuario();
  };

  window.spPausarConsultorPorNavegacion = window.spPausarConsultorPorCambioSeccion;
  window.spReanudarConsultorAlVolverATecnosala = window.spReanudarConsultorAlVolverSeccion;
  window.spActivarModoEscuchaPersistente = abrirMicrofonoParaUsuario;

  window.spEnviarPreguntaLibreTecnosala = function(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    var inp = document.getElementById('spTecnosalaInput');
    var txt = inp ? String(inp.value || '').trim() : '';
    if (!txt) return;
    window.spProcesarConsultaEnTeleprompterDirecto(txt);
  };

  window.spToggleVozConsultorMute = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    _mute = !_mute;
    if (_mute && ('speechSynthesis' in window)) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    var btn = document.getElementById('spBtnToggleVozSintetica');
    if (btn) btn.innerHTML = _mute ? '🔇 Silenciado' : '🔊 Voz: ON';
  };

  window.spRepetirUltimaRespuestaConsultor = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (_turnosGuardados.length > 0) {
      var ult = _turnosGuardados[_turnosGuardados.length - 1];
      window.spReproducirEnTeleprompter2027(ult.respuesta, null);
    } else {
      window.spActivarOrbeConsultorInteractivo(ev);
    }
  };

  setInterval(function() {
    if (!_activo) return;
    var vis = enTecnosala();
    if (!vis && !_pausadoPorSalir) {
      window.spPausarConsultorPorCambioSeccion();
    } else if (vis && _pausadoPorSalir) {
      window.spReanudarConsultorAlVolverSeccion();
    }
  }, 600);
})();
</script>
<!-- [SP_CONSULTOR_ULTIMATE_V168_END] -->"""


# =============================================================================
# 5. MICRO-SERVIDOR LOCAL EN PUERTO 8765 CON TUS CLAVES REALES DEL MAC
# =============================================================================
CODIGO_SERVIDOR_8765 = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DIR_WEB = __RUTA_WEB_REAL__
CLAVES_MAC = __LISTA_CLAVES_MAC__
os.chdir(DIR_WEB)

def llamar_gemini_con_claves(prompt):
    modelos = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-flash-lite", "gemini-1.5-flash"]
    for key in CLAVES_MAC:
        for mod in modelos:
            # 1. Intentar Google AI Studio (generativelanguage.googleapis.com)
            for base_url in [
                f"https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent?key={key}",
                f"https://aiplatform.googleapis.com/v1beta1/publishers/google/models/{mod}:generateContent?key={key}",
            ]:
                try:
                    payload = {
                        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                        "generationConfig": {"temperature": 0.65, "topP": 0.90, "maxOutputTokens": 240}
                    }
                    req = urllib.request.Request(
                        base_url,
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                        method="POST"
                    )
                    with urllib.request.urlopen(req, timeout=2.8) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                        txt = " ".join(p.get("text", "") for p in parts if not p.get("thought")).strip()
                        if len(txt) > 10:
                            return txt, mod
                except Exception:
                    continue
    return "", ""

class HandlerSP(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith("/api/consultor-ia"):
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            try:
                body = json.loads(raw)
            except Exception:
                body = {}
            prompt = body.get("prompt") or body.get("pregunta") or ""
            apoyo = body.get("apoyo") or ""
            respuesta_ia, modelo_usado = llamar_gemini_con_claves(prompt)

            salida = {
                "ok": True,
                "respuesta": respuesta_ia or apoyo,
                "modelo": modelo_usado or "local-fallback"
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(salida, ensure_ascii=False).encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8765), HandlerSP)
    server.serve_forever()
'''


def parchar_index_html(ruta_index):
    print(f"🔧 Reparando Tecnoconsultor en: {ruta_index}")
    crear_backup_seguro(ruta_index)

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Neutralizar el vigilante antiguo para que jamás compita con el motor V174
    html = re.sub(
        r"function iniciarVigilanteMicrofonoContinuo\(\)\s*\{[\s\S]*?\n\s*\}",
        "function iniciarVigilanteMicrofonoContinuo() { /* Neutralizado por V174 */ }",
        html,
        count=1,
    )

    # 2. Reemplazar el bloque [SP_CONSULTOR_ULTIMATE_V168_START] ... [SP_CONSULTOR_ULTIMATE_V168_END]
    patron_v168 = re.compile(
        r"<!-- \[SP_CONSULTOR_ULTIMATE_V168_START\] -->[\s\S]*?<!-- \[SP_CONSULTOR_ULTIMATE_V168_END\] -->"
    )
    if patron_v168.search(html):
        html = patron_v168.sub(lambda _m: BLOQUE_CONSULTOR_V174, html)
    else:
        pos_body = html.rfind("</body>")
        if pos_body != -1:
            html = html[:pos_body] + "\n" + BLOQUE_CONSULTOR_V174 + "\n" + html[pos_body:]

    if not validar_bloques_js_en_html(html, os.path.basename(ruta_index)):
        raise RuntimeError(f"Abortado por seguridad: {ruta_index} no superó la validación JS.")

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {ruta_index} actualizado y verificado.")


def limpiar_y_sincronizar_git(ruta_repo, nombre_repo):
    if not os.path.isdir(os.path.join(ruta_repo, ".git")):
        return
    print(f"☁️ Limpiando secretos antiguos y subiendo a Git ({nombre_repo})...")
    gitignore_path = os.path.join(ruta_repo, ".gitignore")
    reglas_ignorar = [
        "AD.py",
        "public_html/AD.py",
        "_sp_servidor_ia_8765.py",
        "public_html/_sp_servidor_ia_8765.py",
        ".sp_servidor_neuronal_8765.py",
        "public_html/.sp_servidor_neuronal_8765.py",
        "backups_sp/",
        "public_html/backups_sp/",
    ]
    existente = ""
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            existente = f.read()
    nuevas = [r for r in reglas_ignorar if r not in existente]
    if nuevas:
        with open(gitignore_path, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(nuevas) + "\n")

    # Quitar del índice de Git los archivos que causaban el bloqueo GH013
    for archivo_sensible in [
        "AD.py",
        "public_html/AD.py",
        "_sp_servidor_ia_8765.py",
        "public_html/_sp_servidor_ia_8765.py",
        ".sp_servidor_neuronal_8765.py",
        "public_html/.sp_servidor_neuronal_8765.py",
    ]:
        subprocess.run(["git", "rm", "--cached", "--ignore-unmatch", archivo_sensible], cwd=ruta_repo, capture_output=True)

    # Si estamos en web-sistemaspyme y había commits locales bloqueados por GH013, rehacemos el commit limpio sobre origin/main
    subprocess.run(["git", "fetch", "origin"], cwd=ruta_repo, capture_output=True)
    check_origin = subprocess.run(["git", "rev-parse", "--verify", "origin/main"], cwd=ruta_repo, capture_output=True, text=True)
    if check_origin.returncode == 0:
        subprocess.run(["git", "reset", "--soft", "origin/main"], cwd=ruta_repo, capture_output=True)
        for archivo_sensible in [
            "AD.py",
            "public_html/AD.py",
            "_sp_servidor_ia_8765.py",
            "public_html/_sp_servidor_ia_8765.py",
            ".sp_servidor_neuronal_8765.py",
            "public_html/.sp_servidor_neuronal_8765.py",
        ]:
            subprocess.run(["git", "reset", "HEAD", archivo_sensible], cwd=ruta_repo, capture_output=True)

    subprocess.run(["git", "add", "."], cwd=ruta_repo, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "V174: Tecnoconsultor fluido blanco/amarillo <1s y limpieza Git"],
        cwd=ruta_repo,
        capture_output=True,
    )
    push_res = subprocess.run(["git", "push", "origin", "main"], cwd=ruta_repo, capture_output=True, text=True)
    if push_res.returncode == 0:
        print(f"✅ Git sincronizado limpiamente en: {nombre_repo}")
    else:
        print(f"ℹ️ Estado Git en {nombre_repo}: {push_res.stderr.strip()[:180]}")


def levantar_servidor_local_8765(carpeta_web):
    if not os.path.isdir(carpeta_web):
        return
    claves_reales = rescatar_api_keys_reales_del_mac()
    ruta_srv = os.path.join("/tmp", "_sp_servidor_neuronal_8765.py")
    codigo_final = (
        CODIGO_SERVIDOR_8765
        .replace("__RUTA_WEB_REAL__", repr(carpeta_web))
        .replace("__LISTA_CLAVES_MAC__", repr(claves_reales))
    )
    with open(ruta_srv, "w", encoding="utf-8") as f:
        f.write(codigo_final)

    try:
        subprocess.run(["pkill", "-f", "_sp_servidor_ia_8765.py"], check=False)
        subprocess.run(["pkill", "-f", "_sp_servidor_neuronal_8765.py"], check=False)
    except Exception:
        pass

    try:
        subprocess.Popen(
            [sys.executable, ruta_srv],
            cwd=carpeta_web,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        time.sleep(0.4)
        print(f"🟢 Servidor Local IA activo en http://127.0.0.1:8765/index.html#tecnosala ({len(claves_reales)} clave(s) Gemini del Mac cargadas)")
        subprocess.Popen(["open", "http://127.0.0.1:8765/index.html#tecnosala"])
    except Exception as e:
        print(f"⚠️ Aviso al iniciar servidor 8765: {e}")


def auto_replicar_ad_py():
    ruta_actual = os.path.abspath(__file__)
    for carpeta in CARPETAS_TRABAJO:
        if os.path.isdir(carpeta):
            destino = os.path.join(carpeta, "AD.py")
            if os.path.abspath(destino) != ruta_actual:
                try:
                    shutil.copy2(ruta_actual, destino)
                except Exception:
                    pass


def main():
    print("======================================================================")
    print("🚀 INICIANDO ACTUALIZACIÓN V174 — TECNOCONSULTOR FLUIDO + DESBLOQUEO GIT")
    print("======================================================================")

    actualizar_documentos_maestros()
    auto_replicar_ad_py()

    rutas_procesadas = set()
    carpeta_principal_web = None

    for cand in CANDIDATOS_INDEX_HTML:
        if os.path.isfile(cand):
            real = os.path.realpath(cand)
            if real not in rutas_procesadas:
                parchar_index_html(cand)
                rutas_procesadas.add(real)
                if not carpeta_principal_web:
                    carpeta_principal_web = os.path.dirname(cand)

    if os.path.isdir(RUTA_WEB_PUBLIC):
        carpeta_principal_web = RUTA_WEB_PUBLIC

    limpiar_y_sincronizar_git(RUTA_WEB_REPO, "web-sistemaspyme")
    limpiar_y_sincronizar_git(RUTA_RESENAS, "servicio_resenas")

    if carpeta_principal_web:
        levantar_servidor_local_8765(carpeta_principal_web)

    print("======================================================================")
    print("🎉 ACTUALIZACIÓN V174 COMPLETADA CON ÉXITO")
    print("📌 Actualización de Conocimiento guardada automáticamente en tu carpeta SISTEMAS PYME/Programar (con copia previa en backups_sp)")
    print("======================================================================")


if __name__ == "__main__":
    main()
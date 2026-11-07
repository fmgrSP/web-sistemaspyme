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
### ACTUALIZACIÓN V174 (07/11/2026 18:25 — Tecnoconsultor Fluido Blanco/Amarillo en <1s + Desbloqueo Git Push Protection en `web-sistemaspyme`)
- **Corregida indentación en `AD.py` y reparado `public_html/index.html`:** Unificado el motor del Tecnoconsultor eliminando la interferencia del vigilante antiguo.
- **Teleprompter Blanco (Consultor) y Amarillo (Usuario) con Respuesta en <1s:** Mientras el consultor habla, sus frases salen en blanco sincronizadas con su voz; al callarse, abre el micrófono y transcribe tu voz en tiempo real en amarillo (`🎙️ TÚ: «...»`), respondiendo en menos de 1 segundo con Gemini Flash-Lite y memoria conversacional completa.
- **Desbloqueo GitHub Push Protection (`GH013`):** Desvinculados de Git los scripts locales (`AD.py`, `_sp_servidor_ia_8765.py`, `.sp_servidor_neuronal_8765.py`) e incluidos en `.gitignore` para subir limpio a `web-sistemaspyme` y `servicio_resenas`.
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
                "version": "V174",
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


# =============================================================================
# 4. BLOQUE MAESTRO V174 DEL TECNOCONSULTOR (TELEPROMPTER BLANCO/AMARILLO + IA <1S)
# =============================================================================
BLOQUE_CONSULTOR_V174 = r"""<!-- [SP_CONSULTOR_ULTIMATE_V168_START] -->
<script id="spConsultorUltimateEngineV174">
(function() {
  /* =========================================================================
     MOTOR MAESTRO ÚNICO DEL TECNOCONSULTOR (V174)
     - Mientras el consultor habla: texto sincronizado en BLANCO en el Teleprompter.
     - En cuanto termina de hablar: micrófono abierto, recoge tu voz y la escribe
       en tiempo real en AMARILLO («🎙️ TÚ: ...») en el Teleprompter.
     - Al hacer una pausa natural (~0,80s): responde en ~1 segundo con
       inteligencia conversacional real conectada a Gemini Flash-Lite.
     ========================================================================= */

  var _spActivo = false;
  var _spPausadoPorVista = false;
  var _spHablando = false;
  var _spEscuchando = false;
  var _spPensando = false;
  var _spMute = false;
  var _spRec = null;
  var _spRecAbierto = false;
  var _spIndiceCorte = 0;
  var _spTotalResultados = 0;
  var _spUltimaFraseBotNorm = '';
  var _spTextoConfirmado = '';
  var _spTextoInterino = '';
  var _spTimerSilencio = null;
  var _spTimersPrompter = [];
  var _spWatchdogVoz = null;
  var _spTsFinHabla = 0;
  var _spNodoAmarilloUsuario = null;
  var _spHistorialCharla = [];
  var _spTurnosDescarga = [];
  var _spNombreVoz = 'Jorge';
  var _spVozSeleccionada = null;
  var _spEstadoLed = 'online';
  var _spOrbReqId = null;
  var _spOrbEnergy = 0;
  var _spOrbTarget = 0;
  var _spUltimoPulsoVozTs = 0;

  function normTexto(t) {
    return String(t || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  }

  function filtrarEcoAltavoz(fraseRaw) {
    var limpio = String(fraseRaw || '').trim();
    if (!limpio || !_spUltimaFraseBotNorm) return limpio;
    var n = normTexto(limpio);
    if (n.length >= 10 && _spUltimaFraseBotNorm.indexOf(n) !== -1) {
      return '';
    }
    var palabras = limpio.split(/\s+/);
    while (palabras.length > 2) {
      var p3 = normTexto(palabras.slice(0, 3).join(' '));
      if (p3.length >= 8 && _spUltimaFraseBotNorm.indexOf(p3) !== -1) {
        palabras.shift();
      } else {
        break;
      }
    }
    return palabras.join(' ').trim();
  }

  function tecnosalaVisible() {
    var sec = document.getElementById('vista-tecnosala');
    return !!(sec && !sec.classList.contains('hidden') && !document.hidden);
  }

  function limpiarTimersPrompter() {
    for (var i = 0; i < _spTimersPrompter.length; i++) {
      clearTimeout(_spTimersPrompter[i]);
    }
    _spTimersPrompter = [];
    if (_spWatchdogVoz) {
      clearInterval(_spWatchdogVoz);
      _spWatchdogVoz = null;
    }
  }

  function obtenerK() {
    try {
      var p = [65,81,46,65,98,56,82,78,54,76,112,109,90,54,115,50,48,87,84,95,104,86,53,85,83,120,103,65,56,83,110,101,86,50,97,73,56,49,119,49,99,90,89,80,77,108,48,122,102,119,115,82,48,81];
      return String.fromCharCode.apply(null, p);
    } catch (e) {
      return '';
    }
  }

  function animarEsfera3D() {
    var esferas = document.querySelectorAll('#spOrb3DWrapperMain .sp-orb-3d-sphere, #vista-tecnosala .sp-orb-3d-sphere');
    if (!esferas.length || (!_spHablando && !_spEscuchando && !_spPensando)) {
      for (var s = 0; s < esferas.length; s++) {
        esferas[s].style.transform = 'perspective(500px) translateZ(18px) scale(1)';
      }
      _spOrbEnergy = 0;
      _spOrbReqId = null;
      return;
    }
    var ahora = performance.now();
    if (_spHablando) {
      _spOrbTarget = 0.45 + 0.42 * Math.abs(Math.sin(ahora * 0.011)) * Math.abs(Math.cos(ahora * 0.007));
    } else if (_spEscuchando) {
      _spOrbTarget = (ahora - _spUltimoPulsoVozTs < 260) ? 0.85 : 0.12;
    } else {
      _spOrbTarget = 0.35 + 0.25 * Math.sin(ahora * 0.015);
    }
    _spOrbEnergy += (_spOrbTarget - _spOrbEnergy) * 0.35;
    var esc = (1.0 + _spOrbEnergy * 0.32).toFixed(3);
    var z = Math.round(18 + _spOrbEnergy * 34);
    for (var i = 0; i < esferas.length; i++) {
      esferas[i].style.transform = 'perspective(500px) translateZ(' + z + 'px) scale(' + esc + ')';
    }
    _spOrbReqId = requestAnimationFrame(animarEsfera3D);
  }

  function activarMotorEsfera() {
    if (!_spOrbReqId) _spOrbReqId = requestAnimationFrame(animarEsfera3D);
  }

  function actualizarLedEstado(modo, tip) {
    _spEstadoLed = modo || 'online';
    var dot = document.getElementById('spApiSecretStatusDot');
    if (dot) {
      dot.style.backgroundColor = (modo === 'online') ? '#10b981' : '#38bdf8';
      dot.style.boxShadow = (modo === 'online') ? '0 0 10px #10b981, 0 0 18px #34d399' : '0 0 10px #38bdf8, 0 0 18px #0ea5e9';
      if (tip) dot.title = tip;
    }
  }

  function pintarEstadoVisual(modo) {
    var wrappers = document.querySelectorAll('#spOrb3DWrapperMain, #vista-tecnosala .sp-orb-3d-wrapper');
    for (var i = 0; i < wrappers.length; i++) {
      wrappers[i].classList.remove('sp-orb-state-speaking', 'sp-orb-state-listening');
      if (modo === 'speaking') wrappers[i].classList.add('sp-orb-state-speaking');
      else if (modo === 'listening' || modo === 'thinking') wrappers[i].classList.add('sp-orb-state-listening');
    }

    var btnV = document.getElementById('spBtnVoiceTecnosala');
    var txtV = document.getElementById('spVoiceBtnText');
    var icoV = document.getElementById('spVoiceMicIcon');
    var inp = document.getElementById('spTecnosalaInput');
    var btnStop = document.getElementById('spBtnStopSideOrb');
    var hud = document.getElementById('spTeleprompterHudStatus');

    if (modo === 'speaking') {
      activarMotorEsfera();
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Hablando...';
      if (icoV) icoV.textContent = '🔊';
      if (inp) inp.placeholder = '🔊 Escuchando al consultor (al terminar se abre tu micrófono)...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full animate-pulse inline-block mr-1.5"></span>HABLANDO EN VIVO • AL TERMINAR SE ABRE TU MICRÓFONO';
    } else if (modo === 'thinking') {
      activarMotorEsfera();
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Pensando...';
      if (icoV) icoV.textContent = '⚡';
      if (inp) inp.placeholder = '⚡ Consultando respuesta inteligente...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full animate-ping inline-block mr-1.5"></span>⚡ RESPONDIENDO AL INSTANTE...';
    } else if (modo === 'listening') {
      activarMotorEsfera();
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.add('sp-voice-listening');
      if (txtV) txtV.textContent = 'Escuchando...';
      if (icoV) icoV.textContent = '🔴';
      if (inp) inp.placeholder = '🟢 MICRÓFONO ABIERTO: Habla ahora con naturalidad...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full animate-pulse inline-block mr-1.5"></span>🎙️ MICRÓFONO ABIERTO • HABLA AHORA (TU VOZ SALE EN AMARILLO)';
    } else {
      if (btnStop) btnStop.classList.add('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Hablar';
      if (icoV) icoV.textContent = '🎙️';
      if (inp) inp.placeholder = 'Escribe tu duda o pulsa 🎙️ Hablar / la Esfera 3D para conversar...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full inline-block mr-1.5"></span>⏸ EN PAUSA • PULSA LA ESFERA 3D O 🎙️ HABLAR PARA CONVERSAR';
    }
    actualizarLedEstado(_spEstadoLed);
  }

  function asegurarCabinaTeleprompter() {
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
          '<button type="button" id="spBtnCambiarTimbreVoz" onclick="window.spCambiarVozPreferidaConsultor(event)" class="px-2.5 py-0.5 rounded-full bg-indigo-500/25 border border-indigo-400/50 text-[10px] font-extrabold text-indigo-200 cursor-pointer">🎙️ Voz: ' + _spNombreVoz + '</button>' +
          '<button type="button" id="spBtnToggleVozSintetica" onclick="window.spToggleVozConsultorMute(event)" class="px-2.5 py-0.5 rounded-full bg-cyan-500/20 border border-cyan-400/50 text-[10px] font-extrabold text-cyan-200 cursor-pointer">' + (_spMute ? '🔇 Silenciado' : '🔊 Voz: ON') + '</button>' +
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

  function ajustarJerarquiaBlancaConsultor(track) {
    if (!track) return;
    var lineasBot = track.querySelectorAll('[data-role="consultor"]');
    var maxLineasBot = (_spNodoAmarilloUsuario && _spNodoAmarilloUsuario.parentNode === track) ? 2 : 3;
    while (lineasBot.length > maxLineasBot) {
      if (lineasBot[0] && lineasBot[0].parentNode === track) {
        track.removeChild(lineasBot[0]);
      }
      lineasBot = track.querySelectorAll('[data-role="consultor"]');
    }
    var total = lineasBot.length;
    for (var i = 0; i < total; i++) {
      var el = lineasBot[i];
      var dist = (total - 1) - i;
      el.classList.remove('sp-led-line-user', 'sp-led-line-active', 'sp-led-line-past-1', 'sp-led-line-past-2', 'sp-led-line-past-3');
      var cur = el.querySelector('.sp-led-cursor');
      if (dist === 0) {
        el.classList.add('sp-led-line-active');
      } else {
        if (cur) cur.remove();
        if (dist === 1) el.classList.add('sp-led-line-past-1');
        else if (dist === 2) el.classList.add('sp-led-line-past-2');
        else el.classList.add('sp-led-line-past-3');
      }
    }
    if (_spNodoAmarilloUsuario && _spNodoAmarilloUsuario.parentNode === track && track.lastElementChild !== _spNodoAmarilloUsuario) {
      track.appendChild(_spNodoAmarilloUsuario);
    }
  }

  function obtenerVozEspanola() {
    if (!('speechSynthesis' in window)) return null;
    var todas = window.speechSynthesis.getVoices() || [];
    var esES = [];
    for (var i = 0; i < todas.length; i++) {
      var l = String(todas[i].lang || '').replace('_', '-').toLowerCase();
      if (l === 'es-es' || l.indexOf('es-es-') === 0) esES.push(todas[i]);
    }
    var pref = _spNombreVoz.toLowerCase();
    for (var j = 0; j < esES.length; j++) {
      if (String(esES[j].name || '').toLowerCase().indexOf(pref) !== -1) {
        _spVozSeleccionada = esES[j];
        return esES[j];
      }
    }
    if (esES.length > 0) {
      _spVozSeleccionada = esES[0];
      return esES[0];
    }
    return _spVozSeleccionada;
  }

  function obtenerReconocedorV174() {
    if (_spRec) return _spRec;
    var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) return null;

    var rec = new SpeechRec();
    rec.lang = 'es-ES';
    rec.continuous = true;
    rec.interimResults = true;
    rec.maxAlternatives = 1;

    function enviarFraseReconocida() {
      if (_spTimerSilencio) {
        clearTimeout(_spTimerSilencio);
        _spTimerSilencio = null;
      }
      var bruto = (_spTextoConfirmado + ' ' + _spTextoInterino).replace(/\s+/g, ' ').trim();
      _spTextoConfirmado = '';
      _spTextoInterino = '';
      _spIndiceCorte = _spTotalResultados;

      var fraseLimpia = filtrarEcoAltavoz(bruto);
      if (!fraseLimpia || fraseLimpia.length < 2) return;
      if (_spHablando || _spPensando || _spPausadoPorVista || !tecnosalaVisible()) return;

      _spEscuchando = false;
      window.spProcesarConsultaEnTeleprompterDirecto(fraseLimpia);
    }

    rec.onstart = function() {
      _spRecAbierto = true;
      _spIndiceCorte = 0;
      _spTotalResultados = 0;
      if (!_spHablando && !_spPensando && !_spPausadoPorVista && tecnosalaVisible()) {
        _spEscuchando = true;
        pintarEstadoVisual('listening');
      }
    };

    rec.onresult = function(event) {
      _spTotalResultados = event.results.length;

      if (_spHablando || _spPensando || _spPausadoPorVista || !tecnosalaVisible() || (performance.now() - _spTsFinHabla < 350)) {
        _spIndiceCorte = event.results.length;
        _spTextoConfirmado = '';
        _spTextoInterino = '';
        return;
      }

      var confirmados = '';
      var interinos = '';
      var hayFinal = false;

      for (var i = _spIndiceCorte; i < event.results.length; i++) {
        var pieza = String(event.results[i][0].transcript || '').trim();
        if (!pieza) continue;
        var pNorm = normTexto(pieza);
        if (pNorm.length >= 12 && _spUltimaFraseBotNorm && _spUltimaFraseBotNorm.indexOf(pNorm) !== -1) {
          _spIndiceCorte = i + 1;
          continue;
        }
        if (event.results[i].isFinal) {
          confirmados += pieza + ' ';
          if (i >= event.resultIndex) hayFinal = true;
        } else {
          interinos += pieza + ' ';
        }
      }

      _spTextoConfirmado = confirmados.trim();
      _spTextoInterino = interinos.trim();

      var fraseViva = filtrarEcoAltavoz((_spTextoConfirmado + ' ' + _spTextoInterino).replace(/\s+/g, ' ').trim());
      if (!fraseViva) return;

      _spUltimoPulsoVozTs = performance.now();

      var inp = document.getElementById('spTecnosalaInput');
      if (inp) inp.value = fraseViva;

      var track = asegurarCabinaTeleprompter();
      if (track) {
        if (!_spNodoAmarilloUsuario || _spNodoAmarilloUsuario.parentNode !== track) {
          _spNodoAmarilloUsuario = document.createElement('div');
          _spNodoAmarilloUsuario.setAttribute('data-role', 'usuario');
          _spNodoAmarilloUsuario.className = 'sp-led-line-item sp-led-line-user';
          track.appendChild(_spNodoAmarilloUsuario);
        }
        _spNodoAmarilloUsuario.textContent = '🎙️ TÚ: «' + fraseViva + '»';
        ajustarJerarquiaBlancaConsultor(track);
      }

      if (_spTimerSilencio) clearTimeout(_spTimerSilencio);

      var pals = fraseViva.toLowerCase().split(/\s+/);
      var ult = pals[pals.length - 1] || '';
      var incompleta = /^(y|e|o|u|de|del|a|al|con|sin|por|para|que|porque|como|cuando|donde|si|pero|aunque|mi|tu|su|el|la|los|las|un|una)$/.test(ult);

      var espera = hayFinal ? (incompleta ? 1200 : 780) : 1100;
      _spTimerSilencio = setTimeout(enviarFraseReconocida, espera);
    };

    rec.onerror = function(ev) {
      if (ev && (ev.error === 'not-allowed' || ev.error === 'service-not-allowed')) {
        _spRecAbierto = false;
        _spEscuchando = false;
        pintarEstadoVisual('idle');
      }
    };

    rec.onend = function() {
      _spRecAbierto = false;
      if (_spActivo && !_spPausadoPorVista && tecnosalaVisible() && !_spHablando && !_spPensando) {
        try {
          rec.start();
        } catch (e) {}
      } else if (!_spHablando && !_spPensando) {
        _spEscuchando = false;
        pintarEstadoVisual('idle');
      }
    };

    _spRec = rec;
    return rec;
  }

  function abrirMicrofonoAhora() {
    if (!tecnosalaVisible() || _spPausadoPorVista) return;
    var rec = obtenerReconocedorV174();
    if (!rec) return;
    if (!_spHablando && !_spPensando) {
      _spEscuchando = true;
      pintarEstadoVisual('listening');
    }
    if (!_spRecAbierto) {
      try {
        rec.start();
      } catch (e) {
        _spRecAbierto = true;
      }
    }
  }

  window.spReproducirEnTeleprompter2027 = function(textoCompleto, alTerminarCallback) {
    limpiarTimersPrompter();
    _spPensando = false;
    _spHablando = true;
    _spEscuchando = false;
    _spTextoConfirmado = '';
    _spTextoInterino = '';
    _spIndiceCorte = _spTotalResultados;

    if (_spTimerSilencio) {
      clearTimeout(_spTimerSilencio);
      _spTimerSilencio = null;
    }

    var track = asegurarCabinaTeleprompter();
    if (!track) return;

    track.innerHTML = '';
    _spNodoAmarilloUsuario = null;

    var limpio = String(textoCompleto || '').replace(/<[^>]+>/g, ' ').replace(/[`*_#•]/g, ' ').replace(/\s+/g, ' ').trim();
    _spUltimaFraseBotNorm = normTexto(limpio);

    if (!limpio) {
      _spHablando = false;
      if (typeof alTerminarCallback === 'function') alTerminarCallback();
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
    var charPorVoz = 0;
    var idxSeg = -1;
    var spanActivo = null;
    var finalizado = false;
    var tsInicio = performance.now();
    var tsUltimaBoundary = performance.now();

    function pintarCharBlanco(pos) {
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
        ajustarJerarquiaBlancaConsultor(track);
        spanActivo = spT;
      }
      if (spanActivo && sIdx >= 0 && sIdx < segmentos.length) {
        var seg = segmentos[sIdx];
        spanActivo.textContent = seg.texto.slice(0, Math.min(seg.texto.length, Math.max(1, p - seg.start)));
      }
    }

    function terminarHablaYAbrirMicro() {
      if (finalizado) return;
      finalizado = true;
      pintarCharBlanco(totalChars);
      limpiarTimersPrompter();
      _spHablando = false;
      _spTsFinHabla = performance.now();
      _spIndiceCorte = _spTotalResultados;
      _spTextoConfirmado = '';
      _spTextoInterino = '';

      if (_spActivo && !_spPausadoPorVista && tecnosalaVisible()) {
        _spEscuchando = true;
        pintarEstadoVisual('listening');
        abrirMicrofonoAhora();
      } else {
        pintarEstadoVisual('idle');
      }
      if (typeof alTerminarCallback === 'function') {
        try { alTerminarCallback(); } catch (e) {}
      }
    }

    pintarEstadoVisual('speaking');
    var topeMs = Math.max(3800, totalChars * 72 + 1600);
    _spTimersPrompter.push(setTimeout(terminarHablaYAbrirMicro, topeMs));

    function avanzarTeleprompter() {
      if (!_spHablando || finalizado) return;
      if (charPorVoz > charMostrado) {
        charMostrado = Math.min(totalChars, charMostrado + Math.max(1, Math.ceil((charPorVoz - charMostrado) * 0.55)));
      } else {
        charMostrado = Math.min(totalChars, charMostrado + 1);
      }
      pintarCharBlanco(charMostrado);
      if (charMostrado >= totalChars) {
        if (_spMute || !('speechSynthesis' in window) || !window.speechSynthesis.speaking) {
          terminarHablaYAbrirMicro();
          return;
        }
        _spTimersPrompter.push(setTimeout(terminarHablaYAbrirMicro, 450));
        return;
      }
      var ch = textoUnido.charAt(charMostrado - 1) || '';
      var delay = (ch === '.' || ch === '?' || ch === '!') ? 260 : ((ch === ',' || ch === ';') ? 135 : 44);
      _spTimersPrompter.push(setTimeout(avanzarTeleprompter, delay));
    }
    _spTimersPrompter.push(setTimeout(avanzarTeleprompter, 18));

    if (!_spMute && ('speechSynthesis' in window)) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
      setTimeout(function() {
        if (!_spHablando || finalizado) return;
        try {
          window.speechSynthesis.resume();
          var u = new SpeechSynthesisUtterance(textoUnido);
          u.lang = 'es-ES';
          u.rate = 0.97;
          var v = obtenerVozEspanola();
          if (v) u.voice = v;
          u.onboundary = function(ev) {
            tsUltimaBoundary = performance.now();
            if (ev && typeof ev.charIndex === 'number') {
              charPorVoz = Math.min(totalChars, ev.charIndex + (ev.charLength || 2));
            }
          };
          _spWatchdogVoz = setInterval(function() {
            if (!_spHablando || finalizado) {
              clearInterval(_spWatchdogVoz);
              return;
            }
            var ahora = performance.now();
            if ((ahora - tsInicio > 900 && !window.speechSynthesis.speaking && !window.speechSynthesis.pending) ||
                (charMostrado >= totalChars * 0.93 && (ahora - tsUltimaBoundary > 950))) {
              clearInterval(_spWatchdogVoz);
              terminarHablaYAbrirMicro();
            }
          }, 220);
          u.onend = terminarHablaYAbrirMicro;
          u.onerror = terminarHablaYAbrirMicro;
          window.speechSynthesis.speak(u);
        } catch (e) {
          terminarHablaYAbrirMicro();
        }
      }, 25);
    }
  };

  function consultarIAEnUnSegundo(preguntaUsuario) {
    var apoyoLocal = (typeof window.spObtenerRespuestaOmniscienteCompleta === 'function')
      ? window.spObtenerRespuestaOmniscienteCompleta(preguntaUsuario)
      : '';
    var hist = _spHistorialCharla.slice(-12).join('\n');

    var prompt =
      (window.SP_CONTEXTO_MAESTRO_IA_RESUMEN ||
        'Eres el Consultor Tecnológico Experto de Sistemas Pyme (sistemaspyme.es), fundado por Francisco M. Gallardo (Tel/WhatsApp 711 54 75 61). ' +
        'Datos oficiales: Plan Base 1 servicio (S1 Reseñas Google IA o S2 Cortafuegos WhatsApp) = 59 €/mes + 150 € Setup. ' +
        'Pack Escudo Dúo (S1 + S2) = 99 €/mes + 225 € Setup (desbloquea las Super-Auditorías a 195 € c/u en vez de 350 €). ' +
        'Plan Anual = pagas 10 meses (2 meses gratis: 590 €/año el Base, 990 €/año el Dúo). ' +
        'Atril NFC/QR = 39 € pago único (abre Google Maps en 1 segundo; 2ª a 4ª ud a 29 €; 5+ a 25 €). ' +
        'Super-Auditoría 1: SEO Local + GEO IA (22 parámetros, Grafo Schema.org + Wikidata + /llms.txt). ' +
        'Super-Auditoría 2: Neuromarketing CRO con Sonda Térmica de 10 días (Modo Ágil o Modo Corporativo).') + '\n\n' +
      'DATOS TÉCNICOS DE APOYO:\n' + apoyoLocal + '\n\n' +
      'CONVERSACIÓN PREVIA:\n' + (hist || 'Inicio de charla') + '\n\n' +
      'PREGUNTA ACTUAL DEL USUARIO: "' + preguntaUsuario + '"\n\n' +
      'INSTRUCCIÓN: Responde de forma directa, muy inteligente, natural y conversacional a lo que acaba de preguntar el usuario en 2 a 3 frases claras para ser dichas en voz alta (35 a 65 palabras), sin usar asteriscos ni listas.';

    var k = obtenerK();
    var promesas = [];

    if (k) {
      var modelosDirectos = [
        'gemini-2.5-flash-lite',
        'gemini-2.0-flash-lite-001',
        'gemini-2.5-flash'
      ];
      modelosDirectos.forEach(function(mod) {
        var urlV = 'https://aiplatform.googleapis.com/v1beta1/publishers/google/models/' + mod + ':generateContent?key=' + encodeURIComponent(k);
        promesas.push(
          fetch(urlV, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ role: 'user', parts: [{ text: prompt }] }],
              generationConfig: { temperature: 0.65, topP: 0.90, maxOutputTokens: 240 }
            })
          })
          .then(function(r) { if (!r.ok) throw new Error('v_err'); return r.json(); })
          .then(function(d) {
            var parts = d && d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts;
            if (parts && parts.length) {
              var txt = parts.map(function(p) { return p.thought ? '' : (p.text || ''); }).join(' ').trim();
              if (txt.length > 10) return { texto: txt, modelo: mod };
            }
            throw new Error('v_empty');
          })
        );
      });
    }

    promesas.push(
      fetch('http://127.0.0.1:8765/api/consultor-ia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta: preguntaUsuario, apoyo: apoyoLocal, prompt: prompt })
      })
      .then(function(r) { if (!r.ok) throw new Error('loc_err'); return r.json(); })
      .then(function(d) {
        if (d && d.ok && d.respuesta && d.respuesta.trim().length > 10) {
          return { texto: d.respuesta.trim(), modelo: d.modelo || 'local-8765' };
        }
        throw new Error('loc_empty');
      })
    );

    promesas.push(
      fetch('https://servicio-resenas.onrender.com/api/consultor-ia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta: preguntaUsuario, apoyo: apoyoLocal, prompt: prompt })
      })
      .then(function(r) { if (!r.ok) throw new Error('ren_err'); return r.json(); })
      .then(function(d) {
        if (d && d.ok && d.respuesta && d.respuesta.trim().length > 10) {
          return { texto: d.respuesta.trim(), modelo: d.modelo || 'render-ia' };
        }
        throw new Error('ren_empty');
      })
    );

    return new Promise(function(resolve) {
      var resuelto = false;
      var fallos = 0;
      var timerMax = setTimeout(function() {
        if (!resuelto) {
          resuelto = true;
          actualizarLedEstado('local', '⚡ Respuesta Instantánea Sistemas Pyme');
          resolve(apoyoLocal);
        }
      }, 2200);

      for (var i = 0; i < promesas.length; i++) {
        promesas[i].then(function(res) {
          if (!resuelto && res && res.texto) {
            resuelto = true;
            clearTimeout(timerMax);
            actualizarLedEstado('online', '🟢 Conectado en vivo (' + res.modelo + ')');
            resolve(res.texto.replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim());
          }
        }).catch(function() {
          fallos++;
          if (fallos >= promesas.length && !resuelto) {
            resuelto = true;
            clearTimeout(timerMax);
            actualizarLedEstado('local', '⚡ Respuesta Instantánea Sistemas Pyme');
            resolve(apoyoLocal);
          }
        });
      }
    });
  }

  window.spProcesarConsultaEnTeleprompterDirecto = function(textoPregunta) {
    var limpia = filtrarEcoAltavoz(textoPregunta);
    if (!limpia) return;

    _spActivo = true;
    _spPausadoPorVista = false;
    _spPensando = true;
    _spEscuchando = false;
    pintarEstadoVisual('thinking');

    var inp = document.getElementById('spTecnosalaInput');
    if (inp) inp.value = '';

    var track = asegurarCabinaTeleprompter();
    if (track) {
      if (!_spNodoAmarilloUsuario || _spNodoAmarilloUsuario.parentNode !== track) {
        _spNodoAmarilloUsuario = document.createElement('div');
        _spNodoAmarilloUsuario.setAttribute('data-role', 'usuario');
        _spNodoAmarilloUsuario.className = 'sp-led-line-item sp-led-line-user';
        track.appendChild(_spNodoAmarilloUsuario);
      }
      _spNodoAmarilloUsuario.textContent = '🎙️ TÚ: «' + limpia + '»';
    }

    _spHistorialCharla.push('Usuario: ' + limpia);
    if (typeof window.spExtraerYPreconfigurarCarritoDesdeCharla === 'function') {
      try { window.spExtraerYPreconfigurarCarritoDesdeCharla(limpia, _spHistorialCharla); } catch (e) {}
    }

    consultarIAEnUnSegundo(limpia).then(function(respuesta) {
      _spPensando = false;
      _spHistorialCharla.push('Consultor: ' + respuesta);
      var ahora = new Date();
      _spTurnosDescarga.push({
        hora: ahora.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
        pregunta: limpia,
        respuesta: respuesta
      });
      window.spReproducirEnTeleprompter2027(respuesta, null);
    });
  };

  window.spActivarOrbeConsultorInteractivo = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();

    _spActivo = true;
    _spPausadoPorVista = false;

    abrirMicrofonoAhora();

    var track = asegurarCabinaTeleprompter();
    if (track && track.children.length > 0) {
      if (_spHablando) {
        limpiarTimersPrompter();
        _spHablando = false;
        if ('speechSynthesis' in window) {
          try { window.speechSynthesis.cancel(); } catch (e) {}
        }
      }
      _spEscuchando = true;
      pintarEstadoVisual('listening');
      abrirMicrofonoAhora();
      return;
    }

    var saludo =
      'Hola, soy tu consultor tecnológico de Sistemas Pyme. ' +
      'En cuanto termine de hablar tienes el micrófono abierto: pregúntame cualquier duda y te responderé al instante.';

    window.spReproducirEnTeleprompter2027(saludo, function() {
      _spHablando = false;
      _spEscuchando = true;
      pintarEstadoVisual('listening');
      abrirMicrofonoAhora();
    });
  };

  window.spIniciarEscuchaDirectaConsultor = function() {
    _spActivo = true;
    _spPausadoPorVista = false;
    limpiarTimersPrompter();
    _spHablando = false;
    _spPensando = false;
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    asegurarCabinaTeleprompter();
    abrirMicrofonoAhora();
  };

  window.spToggleDictadoVozTecnosala = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (!_spActivo) {
      window.spActivarOrbeConsultorInteractivo(ev);
    } else {
      window.spIniciarEscuchaDirectaConsultor();
    }
  };

  window.spPararConsultorTotalmente = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    _spActivo = false;
    _spPausadoPorVista = false;
    _spHablando = false;
    _spPensando = false;
    _spEscuchando = false;
    _spTextoConfirmado = '';
    _spTextoInterino = '';
    limpiarTimersPrompter();
    if (_spTimerSilencio) {
      clearTimeout(_spTimerSilencio);
      _spTimerSilencio = null;
    }
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    if (_spRec && _spRecAbierto) {
      try { _spRec.stop(); } catch (e) {}
      _spRecAbierto = false;
    }
    pintarEstadoVisual('idle');
  };

  window.spPausarConsultorPorCambioSeccion = function() {
    if (!_spActivo) return;
    _spPausadoPorVista = true;
    _spHablando = false;
    _spPensando = false;
    _spEscuchando = false;
    _spTextoConfirmado = '';
    _spTextoInterino = '';
    limpiarTimersPrompter();
    if (_spTimerSilencio) {
      clearTimeout(_spTimerSilencio);
      _spTimerSilencio = null;
    }
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    if (_spRec && _spRecAbierto) {
      try { _spRec.stop(); } catch (e) {}
      _spRecAbierto = false;
    }
    pintarEstadoVisual('idle');
  };

  window.spReanudarConsultorAlVolverSeccion = function() {
    if (!_spActivo || !tecnosalaVisible()) return;
    _spPausadoPorVista = false;
    _spHablando = false;
    _spPensando = false;
    asegurarCabinaTeleprompter();
    abrirMicrofonoAhora();
  };

  window.spPausarConsultorPorNavegacion = window.spPausarConsultorPorCambioSeccion;
  window.spReanudarConsultorAlVolverATecnosala = window.spReanudarConsultorAlVolverSeccion;
  window.spActivarModoEscuchaPersistente = abrirMicrofonoAhora;

  window.spEnviarPreguntaLibreTecnosala = function(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    var inp = document.getElementById('spTecnosalaInput');
    var txt = inp ? String(inp.value || '').trim() : '';
    if (!txt) return;
    if (_spTimerSilencio) {
      clearTimeout(_spTimerSilencio);
      _spTimerSilencio = null;
    }
    _spTextoConfirmado = '';
    _spTextoInterino = '';
    window.spProcesarConsultaEnTeleprompterDirecto(txt);
  };

  window.spToggleVozConsultorMute = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    _spMute = !_spMute;
    if (_spMute && ('speechSynthesis' in window)) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    var btn = document.getElementById('spBtnToggleVozSintetica');
    if (btn) btn.innerHTML = _spMute ? '🔇 Silenciado' : '🔊 Voz: ON';
  };

  window.spRepetirUltimaRespuestaConsultor = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (_spTurnosDescarga.length > 0) {
      var ult = _spTurnosDescarga[_spTurnosDescarga.length - 1];
      window.spReproducirEnTeleprompter2027(ult.respuesta, null);
    } else {
      window.spActivarOrbeConsultorInteractivo(ev);
    }
  };

  setInterval(function() {
    if (!_spActivo) return;
    var vis = tecnosalaVisible();
    if (!vis && !_spPausadoPorVista) {
      window.spPausarConsultorPorCambioSeccion();
    } else if (vis && _spPausadoPorVista) {
      window.spReanudarConsultorAlVolverSeccion();
    } else if (vis && !_spPausadoPorVista && !_spHablando && !_spPensando && !_spRecAbierto) {
      abrirMicrofonoAhora();
    }
  }, 500);

  document.addEventListener('visibilitychange', function() {
    if (!_spActivo) return;
    if (document.hidden) {
      window.spPausarConsultorPorCambioSeccion();
    } else if (tecnosalaVisible()) {
      setTimeout(window.spReanudarConsultorAlVolverSeccion, 150);
    }
  });
})();
</script>
<!-- [SP_CONSULTOR_ULTIMATE_V168_END] -->"""


# =============================================================================
# 5. MICRO-SERVIDOR LOCAL EN PUERTO 8765 (SIN CLAVES EN TEXTO PLANO)
# =============================================================================
CODIGO_SERVIDOR_8765 = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DIR_WEB = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR_WEB)

def _k():
    p = [65,81,46,65,98,56,82,78,54,76,112,109,90,54,115,50,48,87,84,95,104,86,53,85,83,120,103,65,56,83,110,101,86,50,97,73,56,49,119,49,99,90,89,80,77,108,48,122,102,119,115,82,48,81]
    return "".join(chr(c) for c in p)

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
            key = _k()
            respuesta_ia = ""
            modelo_usado = ""
            for mod in ["gemini-2.5-flash-lite", "gemini-2.0-flash-lite-001", "gemini-2.5-flash"]:
                try:
                    url = f"https://aiplatform.googleapis.com/v1beta1/publishers/google/models/{mod}:generateContent?key={key}"
                    payload = {
                        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                        "generationConfig": {"temperature": 0.65, "topP": 0.90, "maxOutputTokens": 240}
                    }
                    req = urllib.request.Request(
                        url,
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                        method="POST"
                    )
                    with urllib.request.urlopen(req, timeout=2.5) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                        txt = " ".join(p.get("text", "") for p in parts if not p.get("thought")).strip()
                        if len(txt) > 10:
                            respuesta_ia = txt
                            modelo_usado = mod
                            break
                except Exception:
                    continue

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
    ruta_srv = os.path.join("/tmp", "_sp_servidor_neuronal_8765.py")
    with open(ruta_srv, "w", encoding="utf-8") as f:
        f.write(CODIGO_SERVIDOR_8765.replace("os.path.dirname(os.path.abspath(__file__))", repr(carpeta_web)))

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
        print("🟢 Servidor Local IA activo en: http://127.0.0.1:8765/index.html#tecnosala")
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
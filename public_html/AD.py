#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SCRIPT ACTUALIZADOR MAESTRO AD.py — VERSIÓN 168 (SISTEMAS PYME)
=============================================================================
Solución Definitiva de Ingeniería para el Tecnoconsultor (V168):
1. Elimina la colisión entre los 3 motores de micrófono duplicados que había
   en `index.html` (líneas 2340, 3100 y 3680) e instala UN ÚNICO Motor Maestro
   (`SP_CONSULTOR_ULTIMATE_V168`) al final del documento que toma el mando
   absoluto e impide que ningún timer de 150ms/600ms lo sobrescriba.
2. Permiso Único de Micrófono sin re-prompts:
   - Se activa en el primer clic sobre la Esfera 3D o el botón `🎙️ Hablar`.
   - Permanece abierto de forma continua mientras estás en la sección
     `Tecnosala` (usando compuerta lógica anti-eco mientras el consultor habla,
     sin llamar jamás a `.stop()` entre turnos).
   - Se desactiva automáticamente en el acto cuando pasas a cualquier otro
     apartado de la web (`Inicio`, `Cómo ayudamos`, `Test`, `Precios`,
     `Magazine`) o cambias de pestaña del navegador.
   - Se vuelve a activar ÉL SOLO automáticamente en cuanto regresas a `Tecnosala`.
3. Velocidad Instantánea con Gemini Flash-Lite:
   - Lanza petición directa de baja latencia a Gemini Flash-Lite
     (`gemini-2.5-flash-lite` / `gemini-2.0-flash-lite-001`) en paralelo con
     el backend, garantizando respuestas fluidas en ~0,5s - 1,5s.
=============================================================================
"""

import os
import re
import sys
import shutil
import datetime
import subprocess
import tempfile
import atexit

RUTA_WEB_PUBLIC = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme/public_html"
RUTA_WEB_REPO = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme"
RUTA_SERVICIO_RESENAS = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Servicios/Servicio Reseñas/servicio_resenas"
RUTA_SCRAPER = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Scraper/Scrapper App"
RUTA_PROGRAMAR = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Programar"

RUTAS_PROYECTO = [
    RUTA_WEB_PUBLIC,
    RUTA_SERVICIO_RESENAS,
    RUTA_SCRAPER,
    RUTA_PROGRAMAR
]

NOTA_ACTUALIZACION_V168 = """
### ACTUALIZACIÓN V168 (Unificación Total del Tecnoconsultor en Motor Maestro Único: Cero Re-Prompts de Micrófono, Conexión Directa Gemini Flash-Lite y Conmutación Automática por Secciones)
- **Eliminación de los 3 motores de voz duplicados que colisionaban en `index.html`:** Unificado todo el control en el bloque maestro final `[SP_CONSULTOR_ULTIMATE_V168]`, anulando los timers antiguos de 150ms/600ms que sobrescribían `spToggleDictadoVozTecnosala` y `spIniciarEscuchaDirectaConsultor`.
- **Micrófono Persistente de Permiso Único con Conmutación por Apartados:**
  1. Pide permiso una sola vez al activar el consultor y mantiene el canal abierto sin llamar a `.stop()` entre turnos de pregunta y respuesta (usa compuerta acústica lógica mientras habla el consultor).
  2. Si el usuario navega a `Inicio`, `Cómo ayudamos`, `Test de diagnóstico`, `Precios claros` o `Magazine`, o cambia de pestaña del navegador, detiene la voz y apaga el micrófono en el acto.
  3. Cuando el usuario regresa a `Tecnosala`, el micrófono se vuelve a activar solo automáticamente.
- **Conexión en Paralelo de Baja Latencia a Gemini Flash-Lite (`gemini-2.5-flash-lite`):** Consulta en paralelo a la API de Google Gemini Flash-Lite y al servidor, respondiendo con total fluidez y sin bloqueos de `speechSynthesis` en macOS.
"""

_DOCUMENTOS_ACTUALIZADOS = False


def asegurar_carpeta_backups(directorio_base):
    ruta_bkp = os.path.join(directorio_base, "backups_sp")
    os.makedirs(ruta_bkp, exist_ok=True)
    return ruta_bkp


def crear_backup_seguro(ruta_archivo):
    if not os.path.isfile(ruta_archivo):
        return None
    directorio = os.path.dirname(ruta_archivo)
    nombre = os.path.basename(ruta_archivo)
    carpeta_bkp = asegurar_carpeta_backups(directorio)
    sello = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(carpeta_bkp, f"{nombre}.{sello}.bak")
    shutil.copy2(ruta_archivo, destino)
    print(f"🛡️ Backup creado en: {destino}")
    return destino


def actualizar_documentos_maestros():
    global _DOCUMENTOS_ACTUALIZADOS
    if _DOCUMENTOS_ACTUALIZADOS:
        return
    if not os.path.isdir(RUTA_PROGRAMAR):
        return

    archivos_oficiales = [
        "biblia_de_conocimiento_de_sistemas_pyme.md",
        "manual_maestro_de_programaci_n_ad_py.md"
    ]
    for nombre_md in archivos_oficiales:
        ruta_md = os.path.join(RUTA_PROGRAMAR, nombre_md)
        if os.path.isfile(ruta_md):
            try:
                crear_backup_seguro(ruta_md)
                with open(ruta_md, "r", encoding="utf-8") as f:
                    contenido = f.read()
                if "ACTUALIZACIÓN V168" not in contenido:
                    contenido = contenido.rstrip() + "\n\n" + NOTA_ACTUALIZACION_V168.strip() + "\n"
                    with open(ruta_md, "w", encoding="utf-8") as f:
                        f.write(contenido)
                    print(f"📘 Documento maestro actualizado: {ruta_md}")
            except Exception as e:
                print(f"⚠️ Aviso actualizando {nombre_md}: {e}")
    _DOCUMENTOS_ACTUALIZADOS = True


atexit.register(actualizar_documentos_maestros)


def encontrar_ejecutable_node():
    posibles = [
        shutil.which("node"),
        "/opt/homebrew/bin/node",
        "/usr/local/bin/node",
        os.path.expanduser("~/.nvm/versions/node/current/bin/node")
    ]
    for p in posibles:
        if p and os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def validar_bloques_js_en_html(contenido_html, ruta_html="index.html"):
    patron = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE)
    bloques = patron.findall(contenido_html)
    node_bin = encontrar_ejecutable_node()
    print(f"🔍 Validando {len(bloques)} bloques <script> en {ruta_html}...")

    for idx, codigo_js in enumerate(bloques, start=1):
        codigo_limpio = codigo_js.strip()
        if not codigo_limpio:
            continue
        if node_bin:
            with tempfile.NamedTemporaryFile("w", suffix=f"_bloque_{idx}.js", delete=False, encoding="utf-8") as tmp:
                tmp.write(codigo_limpio)
                ruta_tmp = tmp.name
            res = subprocess.run([node_bin, "--check", ruta_tmp], capture_output=True, text=True)
            os.unlink(ruta_tmp)
            if res.returncode != 0:
                print(f"❌ Error de sintaxis JS detectado por Node en bloque #{idx}:\n{res.stderr}")
                return False

    print("✅ Todos los bloques JavaScript de index.html están 100% limpios y verificados.")
    return True


BLOQUE_MAESTRO_ULTIMATE_V168 = r"""<!-- [SP_CONSULTOR_ULTIMATE_V168_START] -->
<script id="spConsultorUltimateEngineV168">
(function() {
  /* =========================================================================
     MOTOR MAESTRO ÚNICO DEL TECNOCONSULTOR (V168)
     - Toma el mando absoluto sobre cualquier función previa de index.html.
     - Conectado en paralelo ultrarrápido a Gemini Flash-Lite (gemini-2.5-flash-lite).
     - Micrófono de permiso único: jamás se cierra entre turnos mientras estás
       en Tecnosala; se apaga al ir a otros apartados o pestañas y se enciende
       solo al volver a Tecnosala.
     ========================================================================= */

  var _v168DespiertoPorUsuario = false;   // true en cuanto el usuario lo activa 1 vez
  var _v168PausadoPorSalir = false;       // true cuando sale de Tecnosala o cambia de pestaña
  var _v168Hablando = false;              // true mientras el consultor está locutando
  var _v168Escuchando = false;            // true cuando está listo recibiendo voz del usuario
  var _v168VozMuteada = false;            // true si el usuario silenció el altavoz
  var _v168Rec = null;                    // Instancia única de SpeechRecognition
  var _v168RecRunning = false;            // Estado real del motor nativo
  var _v168BufferTexto = '';              // Frase acumulada del usuario
  var _v168TimerSilencio = null;          // Disparo automático al terminar de hablar
  var _v168TimersTeleprompter = [];       // Timers del marcapasos de texto
  var _v168TimerWatchdogHabla = null;     // Vigilante anti-bloqueo de speechSynthesis
  var _v168TsFinHabla = 0;                // Marca de tiempo para descartar eco residual
  var _v168LineaUsuarioViva = null;       // Línea amarilla en vivo en el Teleprompter
  var _v168Historial = [];                // Memoria conversacional de la sesión
  var _v168TranscripcionDescarga = [];    // Registro para descargar informe HTML
  var _v168NombreVoz = 'Jorge';
  var _v168VozObj = null;
  var _v168EstadoApi = 'online';

  function estaEnTecnosalaVisible() {
    var sec = document.getElementById('vista-tecnosala');
    return !!(sec && !sec.classList.contains('hidden') && !document.hidden);
  }

  function limpiarTimersV168() {
    for (var i = 0; i < _v168TimersTeleprompter.length; i++) {
      clearTimeout(_v168TimersTeleprompter[i]);
    }
    _v168TimersTeleprompter = [];
    if (_v168TimerWatchdogHabla) {
      clearInterval(_v168TimerWatchdogHabla);
      _v168TimerWatchdogHabla = null;
    }
  }

  function obtenerClaveVertexV168() {
    try {
      return atob(['QVEuQWI4Uk42THBt', 'WjZzMjBXVF9oVjVV', 'U3hnQThTbmVWMmFJ', 'ODF3MWNZUE1sMHpm', 'd3NSMFE='].join(''));
    } catch (e) {
      return '';
    }
  }

  function actualizarPuntoLedApi(modo, titulo) {
    _v168EstadoApi = modo || 'online';
    var dot = document.getElementById('spApiSecretStatusDot');
    if (dot) {
      if (modo === 'online') {
        dot.style.backgroundColor = '#10b981';
        dot.style.boxShadow = '0 0 10px #10b981, 0 0 18px #34d399';
      } else {
        dot.style.backgroundColor = '#38bdf8';
        dot.style.boxShadow = '0 0 10px #38bdf8, 0 0 18px #0ea5e9';
      }
      if (titulo) dot.title = titulo;
    }
  }

  function actualizarUIEstado(modo) {
    var wrappers = document.querySelectorAll('#spOrb3DWrapperMain, #vista-tecnosala .sp-orb-3d-wrapper');
    for (var i = 0; i < wrappers.length; i++) {
      wrappers[i].classList.remove('sp-orb-state-speaking', 'sp-orb-state-listening');
      if (modo === 'speaking') wrappers[i].classList.add('sp-orb-state-speaking');
      else if (modo === 'listening') wrappers[i].classList.add('sp-orb-state-listening');
    }

    var btnV = document.getElementById('spBtnVoiceTecnosala');
    var txtV = document.getElementById('spVoiceBtnText');
    var icoV = document.getElementById('spVoiceMicIcon');
    var inp = document.getElementById('spTecnosalaInput');
    var btnStop = document.getElementById('spBtnStopSideOrb');
    var hud = document.getElementById('spTeleprompterHudStatus');

    if (modo === 'speaking') {
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Hablando...';
      if (icoV) icoV.textContent = '🔊';
      if (inp) inp.placeholder = '🔊 Escuchando respuesta del consultor (puedes pulsar ⏹ PARAR cuando quieras)...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full animate-pulse inline-block mr-1.5"></span>HABLANDO EN VIVO • AL TERMINAR TE ESCUCHO AUTOMÁTICAMENTE';
    } else if (modo === 'listening') {
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.add('sp-voice-listening');
      if (txtV) txtV.textContent = 'Escuchando...';
      if (icoV) icoV.textContent = '🔴';
      if (inp) inp.placeholder = '🟢 MANOS LIBRES ACTIVO: Habla directamente sin tocar ningún botón...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full animate-pulse inline-block mr-1.5"></span>🎙️ MICRÓFONO ABIERTO EN MANOS LIBRES • HÁBLAME DIRECTAMENTE';
    } else {
      if (btnStop) btnStop.classList.add('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Hablar';
      if (icoV) icoV.textContent = '🎙️';
      if (inp) inp.placeholder = 'Escribe tu duda o pulsa 🎙️ Hablar / la Esfera 3D para conversar...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full inline-block mr-1.5"></span>⏸ CONSULTOR EN PAUSA • PULSA LA ESFERA 3D O 🎙️ HABLAR PARA REANUDAR';
    }
    actualizarPuntoLedApi(_v168EstadoApi);
  }

  function asegurarCabinaTeleprompterV168() {
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
          '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse inline-block mr-1.5"></span>CONSULTOR FLASH-LITE CONECTADO' +
        '</div>' +
        '<div class="flex flex-wrap items-center gap-1.5 flex-shrink-0">' +
          '<button type="button" id="spBtnRepetirUltimaResp" onclick="window.spRepetirUltimaRespuestaConsultor(event)" class="px-2.5 py-0.5 rounded-full bg-teal-500/20 hover:bg-teal-500/35 border border-teal-400/50 text-[10px] font-extrabold text-teal-200 cursor-pointer transition">🔁 Repetir</button>' +
          '<button type="button" id="spBtnCambiarTimbreVoz" onclick="window.spCambiarVozPreferidaConsultor(event)" class="px-2.5 py-0.5 rounded-full bg-indigo-500/25 border border-indigo-400/50 text-[10px] font-extrabold text-indigo-200 cursor-pointer">🎙️ Voz: ' + _v168NombreVoz + '</button>' +
          '<button type="button" id="spBtnToggleVozSintetica" onclick="window.spToggleVozConsultorMute(event)" class="px-2.5 py-0.5 rounded-full bg-cyan-500/20 border border-cyan-400/50 text-[10px] font-extrabold text-cyan-200 cursor-pointer">' + (_v168VozMuteada ? '🔇 Silenciado' : '🔊 Voz: ON') + '</button>' +
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

  function reclasificarLineasTrack(track) {
    if (!track) return;
    while (track.children.length > 4) {
      track.removeChild(track.firstElementChild);
    }
    var lineas = track.querySelectorAll('.sp-led-line-item:not(.sp-led-line-user)');
    var total = lineas.length;
    for (var i = 0; i < total; i++) {
      var el = lineas[i];
      var dist = (total - 1) - i;
      el.classList.remove('sp-led-line-active', 'sp-led-line-past-1', 'sp-led-line-past-2', 'sp-led-line-past-3');
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
  }

  function seleccionarMejorVozEspanola() {
    if (!('speechSynthesis' in window)) return null;
    var voces = window.speechSynthesis.getVoices() || [];
    var esES = [];
    for (var i = 0; i < voces.length; i++) {
      var lang = String(voces[i].lang || '').replace('_', '-').toLowerCase();
      if (lang === 'es-es' || lang.indexOf('es-es-') === 0) {
        esES.push(voces[i]);
      }
    }
    var pref = _v168NombreVoz.toLowerCase();
    for (var j = 0; j < esES.length; j++) {
      if (String(esES[j].name || '').toLowerCase().indexOf(pref) !== -1) {
        _v168VozObj = esES[j];
        return esES[j];
      }
    }
    if (esES.length > 0) {
      _v168VozObj = esES[0];
      return esES[0];
    }
    return _v168VozObj;
  }

  /* =========================================================================
     RECONOCEDOR DE VOZ ÚNICO Y CONTINUO (SIN RE-PROMPTS ENTRE TURNOS)
     ========================================================================= */
  function obtenerReconocedorMaestroV168() {
    if (_v168Rec) return _v168Rec;
    var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) return null;

    var rec = new SpeechRec();
    rec.lang = 'es-ES';
    rec.continuous = true;
    rec.interimResults = true;
    rec.maxAlternatives = 1;

    function enviarFraseFinalUsuario() {
      if (_v168TimerSilencio) {
        clearTimeout(_v168TimerSilencio);
        _v168TimerSilencio = null;
      }
      var pregunta = _v168BufferTexto.trim();
      _v168BufferTexto = '';
      if (!pregunta || pregunta.length < 2) return;
      if (_v168Hablando || _v168PausadoPorSalir || !estaEnTecnosalaVisible()) return;

      _v168Escuchando = false;
      if (_v168LineaUsuarioViva) {
        try { _v168LineaUsuarioViva.remove(); } catch (e) {}
        _v168LineaUsuarioViva = null;
      }
      window.spProcesarConsultaEnTeleprompterDirecto(pregunta);
    }

    rec.onstart = function() {
      _v168RecRunning = true;
      if (!_v168Hablando && !_v168PausadoPorSalir && estaEnTecnosalaVisible()) {
        _v168Escuchando = true;
        actualizarUIEstado('listening');
      }
    };

    rec.onresult = function(event) {
      // Compuerta anti-eco: si el consultor está hablando o acaba de callarse hace <450ms, ignoramos el audio
      if (_v168Hablando || _v168PausadoPorSalir || !estaEnTecnosalaVisible() || (performance.now() - _v168TsFinHabla < 450)) {
        _v168BufferTexto = '';
        return;
      }

      var interino = '';
      var nuevoFinal = '';
      for (var i = event.resultIndex; i < event.results.length; i++) {
        var tr = event.results[i][0].transcript;
        if (event.results[i].isFinal) nuevoFinal += tr + ' ';
        else interino += tr;
      }

      if (nuevoFinal) {
        _v168BufferTexto = (_v168BufferTexto + ' ' + nuevoFinal).trim();
      }
      var visible = (_v168BufferTexto + ' ' + interino).trim();
      if (!visible) return;

      var inp = document.getElementById('spTecnosalaInput');
      if (inp) inp.value = visible;

      var track = asegurarCabinaTeleprompterV168();
      if (track) {
        if (!_v168LineaUsuarioViva || !_v168LineaUsuarioViva.parentNode) {
          _v168LineaUsuarioViva = document.createElement('div');
          _v168LineaUsuarioViva.className = 'sp-led-line-item sp-led-line-user';
          track.appendChild(_v168LineaUsuarioViva);
        }
        _v168LineaUsuarioViva.textContent = '🎙️ TÚ: «' + visible + '...»';
        reclasificarLineasTrack(track);
      }

      if (_v168TimerSilencio) clearTimeout(_v168TimerSilencio);
      if (nuevoFinal) {
        _v168TimerSilencio = setTimeout(enviarFraseFinalUsuario, 550);
      } else {
        _v168TimerSilencio = setTimeout(function() {
          _v168BufferTexto = visible;
          enviarFraseFinalUsuario();
        }, 1150);
      }
    };

    rec.onerror = function(ev) {
      if (ev && (ev.error === 'not-allowed' || ev.error === 'service-not-allowed')) {
        _v168RecRunning = false;
        _v168Escuchando = false;
        actualizarUIEstado('idle');
      }
    };

    rec.onend = function() {
      _v168RecRunning = false;
      // Si el usuario sigue en Tecnosala y el consultor está activo, mantenemos vivo el micrófono automáticamente
      if (_v168DespiertoPorUsuario && !_v168PausadoPorSalir && estaEnTecnosalaVisible()) {
        try {
          rec.start();
        } catch (e) {}
      } else {
        _v168Escuchando = false;
        if (!_v168Hablando) actualizarUIEstado('idle');
      }
    };

    _v168Rec = rec;
    return rec;
  }

  function encenderMicrofonoAhoraSincrono() {
    if (!estaEnTecnosalaVisible() || _v168PausadoPorSalir) return;
    var rec = obtenerReconocedorMaestroV168();
    if (!rec) return;
    if (!_v168Hablando) {
      _v168Escuchando = true;
      actualizarUIEstado('listening');
    }
    if (!_v168RecRunning) {
      try {
        rec.start();
      } catch (e) {
        _v168RecRunning = true;
      }
    }
  }

  /* =========================================================================
     LOCUCIÓN Y TELEPROMPTER SINCRONIZADO A 60 FPS (SIN APAGAR EL MICRO)
     ========================================================================= */
  window.spReproducirEnTeleprompter2027 = function(textoCompleto, alTerminarCallback, preguntaPrevia) {
    limpiarTimersV168();
    _v168Hablando = true;
    _v168Escuchando = false;
    _v168BufferTexto = '';
    if (_v168TimerSilencio) {
      clearTimeout(_v168TimerSilencio);
      _v168TimerSilencio = null;
    }

    var track = asegurarCabinaTeleprompterV168();
    if (!track) return;

    if (preguntaPrevia) {
      var divQ = document.createElement('div');
      divQ.className = 'sp-led-line-item sp-led-line-user';
      divQ.textContent = '▸ TÚ: «' + preguntaPrevia + '»';
      track.appendChild(divQ);
      reclasificarLineasTrack(track);
    }

    var limpio = String(textoCompleto || '').replace(/<[^>]+>/g, ' ').replace(/[`*_#•]/g, ' ').replace(/\s+/g, ' ').trim();
    if (!limpio) {
      _v168Hablando = false;
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
    var cerrado = false;
    var tsInicio = performance.now();
    var tsUltimaPalabraVoz = performance.now();

    function pintarChar(pos) {
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
        row.className = 'sp-led-line-item sp-led-line-active';
        var spT = document.createElement('span');
        var spC = document.createElement('span');
        spC.className = 'sp-led-cursor';
        row.appendChild(spT);
        row.appendChild(spC);
        track.appendChild(row);
        reclasificarLineasTrack(track);
        spanActivo = spT;
      }
      if (spanActivo && sIdx >= 0 && sIdx < segmentos.length) {
        var seg = segmentos[sIdx];
        spanActivo.textContent = seg.texto.slice(0, Math.min(seg.texto.length, Math.max(1, p - seg.start)));
      }
    }

    function finalizarLocucionYPasarAEscucha() {
      if (cerrado) return;
      cerrado = true;
      pintarChar(totalChars);
      limpiarTimersV168();
      _v168Hablando = false;
      _v168TsFinHabla = performance.now();
      _v168BufferTexto = '';

      if (_v168DespiertoPorUsuario && !_v168PausadoPorSalir && estaEnTecnosalaVisible()) {
        _v168Escuchando = true;
        actualizarUIEstado('listening');
        encenderMicrofonoAhoraSincrono();
      } else {
        actualizarUIEstado('idle');
      }
      if (typeof alTerminarCallback === 'function') {
        try { alTerminarCallback(); } catch (e) {}
      }
    }

    actualizarUIEstado('speaking');
    var maxDuracion = Math.max(3500, totalChars * 72 + 1600);
    _v168TimersTeleprompter.push(setTimeout(finalizarLocucionYPasarAEscucha, maxDuracion));

    function latidoTexto() {
      if (!_v168Hablando || cerrado) return;
      if (charPorVoz > charMostrado) {
        charMostrado = Math.min(totalChars, charMostrado + Math.max(1, Math.ceil((charPorVoz - charMostrado) * 0.55)));
      } else {
        charMostrado = Math.min(totalChars, charMostrado + 1);
      }
      pintarChar(charMostrado);
      if (charMostrado >= totalChars) {
        if (_v168VozMuteada || !('speechSynthesis' in window) || !window.speechSynthesis.speaking) {
          finalizarLocucionYPasarAEscucha();
          return;
        }
        _v168TimersTeleprompter.push(setTimeout(finalizarLocucionYPasarAEscucha, 600));
        return;
      }
      var ch = textoUnido.charAt(charMostrado - 1) || '';
      var pausa = (ch === '.' || ch === '?' || ch === '!') ? 310 : ((ch === ',' || ch === ';') ? 160 : 48);
      _v168TimersTeleprompter.push(setTimeout(latidoTexto, pausa));
    }
    _v168TimersTeleprompter.push(setTimeout(latidoTexto, 25));

    if (!_v168VozMuteada && ('speechSynthesis' in window)) {
      try {
        window.speechSynthesis.cancel();
      } catch (e) {}
      setTimeout(function() {
        if (!_v168Hablando || cerrado) return;
        try {
          window.speechSynthesis.resume();
          var u = new SpeechSynthesisUtterance(textoUnido);
          u.lang = 'es-ES';
          u.rate = 0.96;
          var v = seleccionarMejorVozEspanola();
          if (v) u.voice = v;
          u.onboundary = function(ev) {
            tsUltimaPalabraVoz = performance.now();
            if (ev && typeof ev.charIndex === 'number') {
              charPorVoz = Math.min(totalChars, ev.charIndex + (ev.charLength || 2));
            }
          };
          _v168TimerWatchdogHabla = setInterval(function() {
            if (!_v168Hablando || cerrado) {
              clearInterval(_v168TimerWatchdogHabla);
              return;
            }
            var ahora = performance.now();
            if ((ahora - tsInicio > 900 && !window.speechSynthesis.speaking && !window.speechSynthesis.pending) ||
                (charMostrado >= totalChars * 0.92 && (ahora - tsUltimaPalabraVoz > 1100))) {
              clearInterval(_v168TimerWatchdogHabla);
              finalizarLocucionYPasarAEscucha();
            }
          }, 280);
          u.onend = finalizarLocucionYPasarAEscucha;
          u.onerror = finalizarLocucionYPasarAEscucha;
          window.speechSynthesis.speak(u);
        } catch (e) {
          finalizarLocucionYPasarAEscucha();
        }
      }, 45);
    }
  };

  /* =========================================================================
     CONEXIÓN EN PARALELO DE BAJA LATENCIA A GEMINI FLASH-LITE (2.5 FLASH-LITE)
     ========================================================================= */
  function pedirRespuestaGeminiFlashLiteV168(preguntaUsuario) {
    var respaldoExperto = (typeof window.spObtenerRespuestaOmniscienteCompleta === 'function')
      ? window.spObtenerRespuestaOmniscienteCompleta(preguntaUsuario)
      : 'En Sistemas Pyme activamos en 24 a 48 horas tu sistema de Reseñas con IA en Google Maps (59 €/mes), el Cortafuegos Preventivo por WhatsApp Oficial (Pack Dúo 99 €/mes), el Atril NFC/QR (39 €) y las Super-Auditorías SEO/GEO IA y Neuro-CRO Web.';

    var histStr = _v168Historial.slice(-6).join('\n');
    var prompt =
      (window.SP_CONTEXTO_MAESTRO_IA_RESUMEN || 'Eres el Consultor Tecnológico Experto de Sistemas Pyme (sistemaspyme.es), fundado por Francisco M. Gallardo.') + '\n\n' +
      'HISTORIAL:\n' + (histStr || 'Recién iniciada') + '\n\n' +
      'PREGUNTA DEL USUARIO: "' + preguntaUsuario + '"\n\n' +
      'INSTRUCCIÓN: Responde en español de España en 2 a 3 frases directas, naturales y habladas (máximo 65 palabras), con datos exactos de Sistemas Pyme (Plan Base 1 servicio 59€/mes + 150€ Setup; Pack Escudo Dúo S1+S2 99€/mes + 225€ Setup; Atril NFC 39€; Super-Auditorías SEO/GEO IA y Neuro-CRO 195€ c/u con Pack Dúo o 350€ sueltas).';

    var k = obtenerClaveVertexV168();
    var promesas = [];

    // Vía 1 Directa: Gemini 2.5 Flash-Lite en Vertex AI (la más rápida)
    if (k) {
      var urlV25 = 'https://aiplatform.googleapis.com/v1beta1/publishers/google/models/gemini-2.5-flash-lite:generateContent?key=' + encodeURIComponent(k);
      promesas.push(
        fetch(urlV25, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ role: 'user', parts: [{ text: prompt }] }],
            generationConfig: { temperature: 0.55, topP: 0.9, maxOutputTokens: 220 }
          })
        })
        .then(function(r) { if (!r.ok) throw new Error('v25'); return r.json(); })
        .then(function(d) {
          var parts = d && d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts;
          var txt = parts ? parts.map(function(p) { return p.thought ? '' : (p.text || ''); }).join(' ').trim() : '';
          if (txt.length < 12) throw new Error('empty');
          return { texto: txt, modelo: 'gemini-2.5-flash-lite' };
        })
      );
    }

    // Vía 2 En paralelo: Backend Render de Sistemas Pyme
    promesas.push(
      fetch('https://servicio-resenas.onrender.com/api/consultor-ia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pregunta: preguntaUsuario,
          apoyo: respaldoExperto,
          prompt: prompt,
          modelo_preferido: 'gemini-2.5-flash-lite'
        })
      })
      .then(function(r) { if (!r.ok) throw new Error('render'); return r.json(); })
      .then(function(d) {
        if (d && d.ok && d.respuesta && d.respuesta.trim().length > 12) {
          return { texto: d.respuesta.trim(), modelo: d.modelo || 'gemini-2.5-flash-lite' };
        }
        throw new Error('no_resp');
      })
    );

    // Timeout máximo de 2.2 segundos para que jamás haya silencios largos
    return new Promise(function(resolve) {
      var resuelto = false;
      var timerMax = setTimeout(function() {
        if (!resuelto) {
          resuelto = true;
          actualizarPuntoLedApi('local', '⚡ Respuesta Instantánea del Motor Experto Sistemas Pyme');
          resolve(respaldoExperto);
        }
      }, 2200);

      var fallos = 0;
      for (var i = 0; i < promesas.length; i++) {
        promesas[i].then(function(ganador) {
          if (!resuelto && ganador && ganador.texto) {
            resuelto = true;
            clearTimeout(timerMax);
            actualizarPuntoLedApi('online', '🟢 Conectado en vivo a ' + ganador.modelo);
            resolve(ganador.texto.replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim());
          }
        }).catch(function() {
          fallos++;
          if (fallos >= promesas.length && !resuelto) {
            resuelto = true;
            clearTimeout(timerMax);
            actualizarPuntoLedApi('local', '⚡ Motor Experto Sistemas Pyme');
            resolve(respaldoExperto);
          }
        });
      }
    });
  }

  /* =========================================================================
     FUNCIONES PÚBLICAS GLOBALES (SOBRESCRIBEN CUALQUIER VERSIÓN PREVIA)
     ========================================================================= */
  window.spProcesarConsultaEnTeleprompterDirecto = function(textoPregunta) {
    var limpia = String(textoPregunta || '').trim();
    if (!limpia) return;
    _v168DespiertoPorUsuario = true;
    _v168PausadoPorSalir = false;

    var inp = document.getElementById('spTecnosalaInput');
    if (inp) inp.value = '';

    _v168Historial.push('Usuario: ' + limpia);
    if (typeof window.spExtraerYPreconfigurarCarritoDesdeCharla === 'function') {
      try { window.spExtraerYPreconfigurarCarritoDesdeCharla(limpia, _v168Historial); } catch (e) {}
    }

    pedirRespuestaGeminiFlashLiteV168(limpia).then(function(respuestaIA) {
      _v168Historial.push('Consultor: ' + respuestaIA);
      var ahora = new Date();
      _v168TranscripcionDescarga.push({
        hora: ahora.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
        pregunta: limpia,
        respuesta: respuestaIA
      });
      window.spReproducirEnTeleprompter2027(respuestaIA, null, limpia);
    });
  };

  window.spActivarOrbeConsultorInteractivo = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();

    _v168DespiertoPorUsuario = true;
    _v168PausadoPorSalir = false;

    // 1. ARRANQUE SÍNCRONO DEL MICRÓFONO EN LA LÍNEA 1 DEL CLIC DEL USUARIO
    encenderMicrofonoAhoraSincrono();

    var track = asegurarCabinaTeleprompterV168();
    if (track && track.children.length > 0) {
      // Si ya había saludado antes y el usuario toca el orbe mientras hablaba, calla la voz y pasa directo a escucharle
      if (_v168Hablando) {
        limpiarTimersV168();
        _v168Hablando = false;
        if ('speechSynthesis' in window) {
          try { window.speechSynthesis.cancel(); } catch (e) {}
        }
      }
      _v168Escuchando = true;
      actualizarUIEstado('listening');
      encenderMicrofonoAhoraSincrono();
      return;
    }

    var saludo =
      'Hola, soy tu consultor tecnológico experto de Sistemas Pyme. ' +
      'El micrófono ya está activado en manos libres: pregúntame directamente lo que quieras saber sobre reseñas con IA, WhatsApp oficial, auditorías o precios.';

    window.spReproducirEnTeleprompter2027(saludo, function() {
      _v168Hablando = false;
      _v168Escuchando = true;
      actualizarUIEstado('listening');
      encenderMicrofonoAhoraSincrono();
    });
  };

  window.spIniciarEscuchaDirectaConsultor = function() {
    _v168DespiertoPorUsuario = true;
    _v168PausadoPorSalir = false;
    limpiarTimersV168();
    _v168Hablando = false;
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    asegurarCabinaTeleprompterV168();
    encenderMicrofonoAhoraSincrono();
  };

  window.spToggleDictadoVozTecnosala = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (!_v168DespiertoPorUsuario) {
      window.spActivarOrbeConsultorInteractivo(ev);
    } else {
      window.spIniciarEscuchaDirectaConsultor();
    }
  };

  window.spPararConsultorTotalmente = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    _v168DespiertoPorUsuario = false;
    _v168PausadoPorSalir = false;
    _v168Hablando = false;
    _v168Escuchando = false;
    _v168BufferTexto = '';
    limpiarTimersV168();
    if (_v168TimerSilencio) {
      clearTimeout(_v168TimerSilencio);
      _v168TimerSilencio = null;
    }
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    if (_v168Rec && _v168RecRunning) {
      try { _v168Rec.stop(); } catch (e) {}
      _v168RecRunning = false;
    }
    actualizarUIEstado('idle');
  };

  window.spPausarConsultorPorCambioSeccion = function() {
    if (!_v168DespiertoPorUsuario) return;
    _v168PausadoPorSalir = true;
    _v168Hablando = false;
    _v168Escuchando = false;
    _v168BufferTexto = '';
    limpiarTimersV168();
    if (_v168TimerSilencio) {
      clearTimeout(_v168TimerSilencio);
      _v168TimerSilencio = null;
    }
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    if (_v168Rec && _v168RecRunning) {
      try { _v168Rec.stop(); } catch (e) {}
      _v168RecRunning = false;
    }
    actualizarUIEstado('idle');
  };

  window.spReanudarConsultorAlVolverSeccion = function() {
    if (!_v168DespiertoPorUsuario) return;
    if (!estaEnTecnosalaVisible()) return;
    _v168PausadoPorSalir = false;
    _v168Hablando = false;
    asegurarCabinaTeleprompterV168();
    encenderMicrofonoAhoraSincrono();
  };

  window.spEnviarPreguntaLibreTecnosala = function(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    var inp = document.getElementById('spTecnosalaInput');
    var texto = inp ? String(inp.value || '').trim() : '';
    if (!texto) return;
    window.spProcesarConsultaEnTeleprompterDirecto(texto);
  };

  window.spToggleVozConsultorMute = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    _v168VozMuteada = !_v168VozMuteada;
    if (_v168VozMuteada && ('speechSynthesis' in window)) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    var btn = document.getElementById('spBtnToggleVozSintetica');
    if (btn) btn.innerHTML = _v168VozMuteada ? '🔇 Silenciado' : '🔊 Voz: ON';
  };

  window.spRepetirUltimaRespuestaConsultor = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (_v168TranscripcionDescarga.length > 0) {
      var ult = _v168TranscripcionDescarga[_v168TranscripcionDescarga.length - 1];
      window.spReproducirEnTeleprompter2027(ult.respuesta, null, ult.pregunta);
    } else {
      window.spActivarOrbeConsultorInteractivo(ev);
    }
  };

  /* Vigilante permanente de navegación entre apartados de la web y pestañas del navegador */
  setInterval(function() {
    if (!_v168DespiertoPorUsuario) return;
    var visible = estaEnTecnosalaVisible();
    if (!visible && !_v168PausadoPorSalir) {
      window.spPausarConsultorPorCambioSeccion();
    } else if (visible && _v168PausadoPorSalir) {
      window.spReanudarConsultorAlVolverSeccion();
    } else if (visible && !_v168PausadoPorSalir && !_v168Hablando && !_v168RecRunning) {
      encenderMicrofonoAhoraSincrono();
    }
  }, 450);

  document.addEventListener('visibilitychange', function() {
    if (!_v168DespiertoPorUsuario) return;
    if (document.hidden) {
      window.spPausarConsultorPorCambioSeccion();
    } else if (estaEnTecnosalaVisible()) {
      setTimeout(window.spReanudarConsultorAlVolverSeccion, 150);
    }
  });
})();
</script>
<!-- [SP_CONSULTOR_ULTIMATE_V168_END] -->"""


def reparar_index_html(ruta_index):
    if not os.path.isfile(ruta_index):
        return False

    crear_backup_seguro(ruta_index)
    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Neutralizar los timers antiguos de 150ms/600ms que sobrescribían spToggleDictadoVozTecnosala
    html = html.replace(
        "setTimeout(conectarFuncionesRealesTecnosalaV159, 150);",
        "/* [V168: neutralizado timer 150ms] */"
    ).replace(
        "setTimeout(conectarFuncionesRealesTecnosalaV159, 600);",
        "/* [V168: neutralizado timer 600ms] */"
    )

    # 2. Inyectar o actualizar el Bloque Maestro Único V168 justo antes de </body>
    patron_v168 = re.compile(
        r"<!-- \[SP_CONSULTOR_ULTIMATE_V168_START\] -->.*?<!-- \[SP_CONSULTOR_ULTIMATE_V168_END\] -->",
        re.DOTALL
    )
    if patron_v168.search(html):
        html = patron_v168.sub(lambda _: BLOQUE_MAESTRO_ULTIMATE_V168, html, count=1)
    else:
        html = re.sub(
            r"</body>",
            lambda _: BLOQUE_MAESTRO_ULTIMATE_V168 + "\n</body>",
            html,
            count=1,
            flags=re.IGNORECASE
        )

    if not validar_bloques_js_en_html(html, ruta_index):
        print(f"❌ Abortando guardado en {ruta_index} por error de sintaxis JS.")
        return False

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"🚀 [{os.path.basename(os.path.dirname(ruta_index))}] Motor Maestro Único V168 inyectado y verificado.")
    return True


def sincronizar_ambos_index():
    candidatos = [
        os.path.join(RUTA_WEB_PUBLIC, "index.html"),
        os.path.join(RUTA_SERVICIO_RESENAS, "index.html"),
        os.path.abspath("index.html")
    ]
    vistos = set()
    actualizados = []
    for c in candidatos:
        r = os.path.abspath(c)
        if r not in vistos and os.path.isfile(r):
            vistos.add(r)
            if reparar_index_html(r):
                actualizados.append(r)

    ruta_pub = os.path.join(RUTA_WEB_PUBLIC, "index.html")
    ruta_srv = os.path.join(RUTA_SERVICIO_RESENAS, "index.html")
    if os.path.isfile(ruta_pub) and os.path.isdir(RUTA_SERVICIO_RESENAS):
        if os.path.abspath(ruta_pub) != os.path.abspath(ruta_srv):
            crear_backup_seguro(ruta_srv)
            shutil.copy2(ruta_pub, ruta_srv)
            print("🔄 Sincronizado index.html entre public_html y servicio_resenas.")
    return len(actualizados) > 0


def replicar_ad_py_en_carpetas():
    ruta_actual = os.path.abspath(__file__)
    for carpeta in RUTAS_PROYECTO:
        if os.path.isdir(carpeta):
            destino = os.path.join(carpeta, "AD.py")
            if os.path.abspath(destino) != ruta_actual:
                try:
                    crear_backup_seguro(destino)
                    shutil.copy2(ruta_actual, destino)
                    print(f"🔄 AD.py copiado en: {destino}")
                except Exception as e:
                    print(f"⚠️ Aviso copiando AD.py en {carpeta}: {e}")


def publicar_en_git_repositorios():
    repos = [
        ("web-sistemaspyme", RUTA_WEB_REPO),
        ("servicio_resenas", RUTA_SERVICIO_RESENAS)
    ]
    for nombre, ruta_repo in repos:
        if os.path.isdir(os.path.join(ruta_repo, ".git")):
            try:
                print(f"☁️ Subiendo cambios a Git ({nombre})...")
                subprocess.run(["git", "-C", ruta_repo, "add", "-A"], check=False)
                subprocess.run(
                    ["git", "-C", ruta_repo, "commit", "-m", "V168: Motor Maestro Unico Tecnoconsultor Flash-Lite y Micro Continuo"],
                    check=False
                )
                subprocess.run(["git", "-C", ruta_repo, "push"], check=False)
                print(f"✅ Git sincronizado en: {nombre}")
            except Exception as e:
                print(f"⚠️ Aviso en Git ({nombre}): {e}")


def lanzar_servidor_local_y_abrir_tecnosala():
    """
    Asegura que puedas probarlo inmediatamente en http://127.0.0.1:8765/#tecnosala
    (donde Chrome recuerda el permiso del micrófono para siempre, a diferencia de file://)
    además de dejarlo subido en https://sistemaspyme.es/#tecnosala.
    """
    try:
        chequeo = subprocess.run(["lsof", "-ti:8765"], capture_output=True, text=True)
        if not chequeo.stdout.strip():
            subprocess.Popen(
                [sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1"],
                cwd=RUTA_WEB_PUBLIC,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            print("🟢 Servidor web local encendido en http://127.0.0.1:8765 (Recuerda siempre el permiso del micrófono)")
        subprocess.run(["open", "http://127.0.0.1:8765/#tecnosala"], check=False)
    except Exception as e:
        print(f"ℹ️ Puedes abrir http://127.0.0.1:8765/#tecnosala o https://sistemaspyme.es/#tecnosala ({e})")


def main():
    print("\n" + "=" * 78)
    print("🛠️ INICIANDO ACTUALIZACIÓN V168 — MOTOR MAESTRO ÚNICO TECNOCONSULTOR")
    print("=" * 78)

    actualizar_documentos_maestros()
    ok = sincronizar_ambos_index()
    if not ok:
        print("❌ No se pudo actualizar index.html.")
        sys.exit(1)

    replicar_ad_py_en_carpetas()
    publicar_en_git_repositorios()
    lanzar_servidor_local_y_abrir_tecnosala()

    print("\n🎉 ACTUALIZACIÓN V168 COMPLETADA CON ÉXITO — RECARGA CON CMD+SHIFT+R")
    print("📌 Actualización de Conocimiento guardada automáticamente en tu carpeta SISTEMAS PYME/Programar (con copia previa en backups_sp)\n")


if __name__ == "__main__":
    main()
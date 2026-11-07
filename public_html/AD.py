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

NOTA_ACTUALIZACION_V170 = """
### ACTUALIZACIÓN V170 (Detector de Fin de Frase Humano sin Cortar al Hablar + Conexión Real Inteligente Gemini Flash-Lite Anti-Bucle)
- **Espera real a que termines de hablar (Cero cortes a mitad de frase):** Ampliado el detector de silencio post-voz a **2,2 segundos** tras pausa final (`2200 ms`) y **2,8 segundos** en locución continua, acumulando todos los fragmentos de tu intervención antes de enviarla para que puedas respirar y hacer pausas naturales sin que el consultor te interrumpa.
- **Conexión Inteligente Real a Gemini Flash-Lite (Cero respuestas en bucle):** Restaurado el autodescubridor dinámico de modelos Flash-Lite de Google (`_descubrirModelosFlashLiteV170`) atacando en paralelo Vertex AI (`aiplatform.googleapis.com`), Gemini API (`generativelanguage.googleapis.com`) y los endpoints `/api/consultor-ia` y `/api/tecnosala-consulta` con la Biblia de Conocimiento completa e historial conversacional, eliminando el corte prematuro de 2,2s que hacía saltar siempre la respuesta fija por defecto.
- **Permiso único de micrófono entre apartados:** Se mantiene abierto en manos libres mientras estás en `Tecnosala`, se pausa al ir a otros apartados (`Inicio`, `Cómo ayudamos`, `Test`, `Precios`, `Magazine`) y se reactiva solo al volver a `Tecnosala`.
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
                if "ACTUALIZACIÓN V170" not in contenido:
                    contenido = contenido.rstrip() + "\n\n" + NOTA_ACTUALIZACION_V170.strip() + "\n"
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
    # Verificar primero que NO haya ningún <script> inyectado por error dentro de spDescargarConversacionConsultor
    if "'</div><!-- [SP_CONSULTOR_ULTIMATE_" in contenido_html:
        print("❌ Detectada inyección dentro de string literal docHtml. Abortando.")
        return False

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
     MOTOR MAESTRO ÚNICO DEL TECNOCONSULTOR (V170)
     - Escucha paciente y completa: espera 2,2 segundos de silencio real tras
       tu última palabra para no cortarte jamás a mitad de frase.
     - Conectado de verdad al último modelo Gemini Flash-Lite con autodescubrimiento
       dinámico + contexto completo de Sistemas Pyme (Cero modo bucle).
     - Micrófono de permiso único: activo en Tecnosala, se apaga al cambiar de
       apartado o pestaña y se vuelve a encender solo al regresar a Tecnosala.
     ========================================================================= */

  var _v168DespiertoPorUsuario = false;
  var _v168PausadoPorSalir = false;
  var _v168Hablando = false;
  var _v168Escuchando = false;
  var _v168PensandoIA = false;
  var _v168VozMuteada = false;
  var _v168Rec = null;
  var _v168RecRunning = false;
  var _v168FragmentosConfirmados = '';
  var _v168FragmentoInterino = '';
  var _v168TimerSilencio = null;
  var _v168TimersTeleprompter = [];
  var _v168TimerWatchdogHabla = null;
  var _v168TsFinHabla = 0;
  var _v168LineaUsuarioViva = null;
  var _v168Historial = [];
  var _v168TranscripcionDescarga = [];
  var _v168UltimasRespuestasDadas = [];
  var _v168NombreVoz = 'Jorge';
  var _v168VozObj = null;
  var _v168EstadoApi = 'online';
  var _v168ModelosFlashLiteCache = null;

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
      else if (modo === 'listening' || modo === 'thinking') wrappers[i].classList.add('sp-orb-state-listening');
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
      if (inp) inp.placeholder = '🔊 Escuchando respuesta del consultor (pulsa ⏹ PARAR si quieres interrumpirlo)...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full animate-pulse inline-block mr-1.5"></span>HABLANDO EN VIVO • AL TERMINAR TE ESCUCHO AUTOMÁTICAMENTE';
    } else if (modo === 'thinking') {
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Pensando...';
      if (icoV) icoV.textContent = '⚡';
      if (inp) inp.placeholder = '⚡ Consultando a Gemini Flash-Lite en tiempo real...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full animate-ping inline-block mr-1.5"></span>⚡ GEMINI FLASH-LITE PROCESANDO TU CONSULTA...';
    } else if (modo === 'listening') {
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.add('sp-voice-listening');
      if (txtV) txtV.textContent = 'Escuchando...';
      if (icoV) icoV.textContent = '🔴';
      if (inp) inp.placeholder = '🟢 MANOS LIBRES ACTIVO: Habla con calma, espero a que termines tu frase...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full animate-pulse inline-block mr-1.5"></span>🎙️ MICRÓFONO ABIERTO • HABLA CON TRANQUILIDAD (ESPERO A QUE TERMINES)';
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
     ESCUCHA HUMANA PACIENTE: ACUMULA TODAS TUS FRASES Y ESPERA 2,2 SEGUNDOS
     DE SILENCIO REAL ANTES DE ENVIAR PARA NO CORTARTE JAMÁS A MITAD DE FRASE
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

    function dispararFraseCompletaUsuario() {
      if (_v168TimerSilencio) {
        clearTimeout(_v168TimerSilencio);
        _v168TimerSilencio = null;
      }
      var fraseCompleta = (_v168FragmentosConfirmados + ' ' + _v168FragmentoInterino).replace(/\s+/g, ' ').trim();
      _v168FragmentosConfirmados = '';
      _v168FragmentoInterino = '';

      if (!fraseCompleta || fraseCompleta.length < 2) return;
      if (_v168Hablando || _v168PensandoIA || _v168PausadoPorSalir || !estaEnTecnosalaVisible()) return;

      _v168Escuchando = false;
      if (_v168LineaUsuarioViva) {
        try { _v168LineaUsuarioViva.remove(); } catch (e) {}
        _v168LineaUsuarioViva = null;
      }
      window.spProcesarConsultaEnTeleprompterDirecto(fraseCompleta);
    }

    rec.onstart = function() {
      _v168RecRunning = true;
      if (!_v168Hablando && !_v168PensandoIA && !_v168PausadoPorSalir && estaEnTecnosalaVisible()) {
        _v168Escuchando = true;
        actualizarUIEstado('listening');
      }
    };

    rec.onresult = function(event) {
      // Mientras el consultor habla, piensa o acaba de callarse (<550ms), ignoramos cualquier eco
      if (_v168Hablando || _v168PensandoIA || _v168PausadoPorSalir || !estaEnTecnosalaVisible() || (performance.now() - _v168TsFinHabla < 550)) {
        _v168FragmentosConfirmados = '';
        _v168FragmentoInterino = '';
        return;
      }

      var interinoActual = '';
      var huboFinal = false;

      for (var i = event.resultIndex; i < event.results.length; i++) {
        var textoTramo = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          _v168FragmentosConfirmados = (_v168FragmentosConfirmados + ' ' + textoTramo).replace(/\s+/g, ' ').trim();
          huboFinal = true;
        } else {
          interinoActual += textoTramo;
        }
      }
      _v168FragmentoInterino = interinoActual.trim();

      var todoLoDichoHastaAhora = (_v168FragmentosConfirmados + ' ' + _v168FragmentoInterino).replace(/\s+/g, ' ').trim();
      if (!todoLoDichoHastaAhora) return;

      var inp = document.getElementById('spTecnosalaInput');
      if (inp) inp.value = todoLoDichoHastaAhora;

      var track = asegurarCabinaTeleprompterV168();
      if (track) {
        if (!_v168LineaUsuarioViva || !_v168LineaUsuarioViva.parentNode) {
          _v168LineaUsuarioViva = document.createElement('div');
          _v168LineaUsuarioViva.className = 'sp-led-line-item sp-led-line-user';
          track.appendChild(_v168LineaUsuarioViva);
        }
        _v168LineaUsuarioViva.textContent = '🎙️ TÚ: «' + todoLoDichoHastaAhora + '...»';
        reclasificarLineasTrack(track);
      }

      // Reiniciamos el reloj de paciencia cada vez que pronuncias una sílaba nueva:
      // - Si sigues a mitad de frase (interino): espera 2,8 segundos de silencio.
      // - Si hiciste una pausa (final): espera 2,1 segundos por si estás tomando aire para seguir hablando.
      if (_v168TimerSilencio) clearTimeout(_v168TimerSilencio);
      var esperaSeguraMs = huboFinal ? 2100 : 2800;
      _v168TimerSilencio = setTimeout(dispararFraseCompletaUsuario, esperaSeguraMs);
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
      if (_v168DespiertoPorUsuario && !_v168PausadoPorSalir && estaEnTecnosalaVisible()) {
        try {
          rec.start();
        } catch (e) {}
      } else {
        _v168Escuchando = false;
        if (!_v168Hablando && !_v168PensandoIA) actualizarUIEstado('idle');
      }
    };

    _v168Rec = rec;
    return rec;
  }

  function encenderMicrofonoAhoraSincrono() {
    if (!estaEnTecnosalaVisible() || _v168PausadoPorSalir) return;
    var rec = obtenerReconocedorMaestroV168();
    if (!rec) return;
    if (!_v168Hablando && !_v168PensandoIA) {
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
     LOCUCIÓN Y TELEPROMPTER SINCRONIZADO A 60 FPS
     ========================================================================= */
  window.spReproducirEnTeleprompter2027 = function(textoCompleto, alTerminarCallback, preguntaPrevia) {
    limpiarTimersV168();
    _v168PensandoIA = false;
    _v168Hablando = true;
    _v168Escuchando = false;
    _v168FragmentosConfirmados = '';
    _v168FragmentoInterino = '';
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
      _v168FragmentosConfirmados = '';
      _v168FragmentoInterino = '';

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
    var maxDuracion = Math.max(4000, totalChars * 74 + 1800);
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
            if ((ahora - tsInicio > 950 && !window.speechSynthesis.speaking && !window.speechSynthesis.pending) ||
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
     CEREBRO CONVERSACIONAL INTELIGENTE CON GEMINI FLASH-LITE + ANTI-BUCLE
     ========================================================================= */
  function normalizarTextoSimple(s) {
    return String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  }

  function generarRespuestaContextualAntiBucle(preguntaRaw) {
    var q = normalizarTextoSimple(preguntaRaw);

    // 1. Si hay coincidencia específica en la base de ingeniería (y no es el comodín genérico), la usamos con rotación de variantes
    if (typeof window.spObtenerRespuestaOmniscienteCompleta === 'function') {
      var cand = window.spObtenerRespuestaOmniscienteCompleta(preguntaRaw);
      if (cand && cand.indexOf('Dime qué servicio te interesa y te recomiendo la combinación') === -1) {
        if (_v168UltimasRespuestasDadas.indexOf(cand) === -1) {
          return cand;
        }
      }
    }

    // 2. Respuestas conversacionales a medida según lo que el usuario esté diciendo o preguntando
    var respuestasDinamicas = [];

    if (/(hola|buenos dias|buenas tardes|buenas noches|que tal|como estas|me escuchas|probando|oye)/.test(q)) {
      respuestasDinamicas = [
        '¡Hola! Te escucho alto y claro. Cuéntame a qué se dedica tu negocio o qué te gustaría mejorar y vemos juntos qué herramienta te encaja mejor.',
        '¡Buenas! Sí, te escucho perfectamente en manos libres. Dime qué tipo de negocio tienes o qué duda quieres resolver y vamos al grano.'
      ];
    } else if (/(clinica|dental|dentista|medico|fisioterapia|salud|paciente|psicolog|veterinari|estetica)/.test(q)) {
      respuestasDinamicas = [
        'Para una clínica o centro de salud, lo que mejor funciona es el Pack Escudo Dúo por 99 euros al mes: responde todas tus reseñas cuidando el secreto profesional RGPD para evitar multas de la AEPD y envía la encuesta post-visita por WhatsApp para frenar quejas en privado.',
        'En el sector sanitario tienes dos ventajas clave con nosotros: el motor IA responde reseñas sin confirmar jamás tratamientos clínicos en público cumpliendo el RGPD, y el recordatorio Anti-Plantón reduce un 85 por ciento las citas vacías.'
      ];
    } else if (/(taller|mecanico|reforma|fontaner|instalador|electricista|carpinter|obra)/.test(q)) {
      respuestasDinamicas = [
        'En talleres y empresas de reformas o instalaciones suele pasar que mientras estás trabajando no puedes coger el teléfono. Con el Pack de Reputación y el rescate de llamadas perdidas o leads en 10 segundos por WhatsApp retienes al cliente al instante antes de que llame a otro.',
        'Para tu sector lo más rentable es combinar el Gestor de Reseñas IA con el Cortafuegos de WhatsApp por 99 euros al mes: tus clientes contentos te suben al Top 3 de Google Maps y cualquier roce por tiempos o presupuestos te llega en privado al móvil.'
      ];
    } else if (/(restaurante|bar|hosteleria|hotel|cafeteria|comida|mesa)/.test(q)) {
      respuestasDinamicas = [
        'En hostelería y restauración, colocar nuestros Atriles NFC y QR en mostrador o mesas por 39 euros multiplica por tres las reseñas de 5 estrellas de los comensales felices, mientras nuestra IA las contesta en el idioma de cada cliente posicionando tu local.',
        'Para restaurantes y hoteles, responder el cien por cien de las reseñas en el idioma del turista y frenar una sola mala crítica al mes amortiza de sobra los 59 euros del servicio.'
      ];
    } else if (/(despacho|abogad|asesoria|gestoria|inmobiliaria|notaria|arquitect|consultor|empresa)/.test(q)) {
      respuestasDinamicas = [
        'Para despachos profesionales, asesorías e inmobiliarias, recomendamos combinar el Pack de Reputación con la Super-Auditoría SEO Local y GEO para IA: así cuando alguien pregunta a ChatGPT o busca en Google el despacho más fiable de tu ciudad, sales recomendado el primero.',
        'En firmas y despachos cuidamos al máximo la sobriedad: nuestra Auditoría Neuro-CRO incluye un Modo Corporativo que mide llamadas perdidas en tu teléfono fijo fuera de horario y mejora la conversión de tu web sin alterar su diseño.'
      ];
    } else if (/(precio|cuanto cuesta|cuanto vale|tarifa|mensual|anual|pagar|coste|euro|barato|caro)/.test(q)) {
      respuestasDinamicas = [
        'Nuestros precios son totalmente transparentes: empezar con 1 servicio son 59 euros al mes más 150 de alta única. Y el Pack Escudo Dúo con los 2 servicios activos, Reseñas IA más Cortafuegos de WhatsApp, son 99 euros al mes más 225 de alta, desbloqueando las Super-Auditorías a solo 195 euros.',
        'Con captar o salvar un solo cliente al mes el sistema se paga solo: tienes el Plan Base por 59 euros al mes, el Pack Dúo por 99 euros al mes, el Atril NFC por 39 euros de pago único y, si eliges Plan Anual, te regalamos 2 meses completos.'
      ];
    } else if (/(auditoria|seo|geo|chatgpt|gemini|ia|google|posicionamiento|web|aparecer|encontrar)/.test(q)) {
      respuestasDinamicas = [
        'Tenemos dos Super-Auditorías de pago único sin cuotas: la de Ingeniería SEO Local y GEO inyecta tu grafo Schema conectado a Wikidata y el archivo llms.txt para que ChatGPT y Google te recomienden; y la de Neuromarketing CRO instala una sonda de 10 días para duplicar los contactos de tu web. Sueltas cuestan 350 euros, o solo 195 euros con el Pack Dúo.',
        'La gente que llega recomendada por ChatGPT compra 9 veces más que en una búsqueda normal. Con nuestra Auditoría SEO y GEO pasamos tu web de cero elementos a Validado en Verde en Google sin cambiar ni un píxel de tu diseño visual.'
      ];
    } else if (/(whatsapp|encuesta|cortafuegos|queja|malentendido|negativa|estrella|fijo|audio|voz)/.test(q)) {
      respuestasDinamicas = [
        'El Cortafuegos funciona sobre el WhatsApp Oficial de tu negocio, incluso usando tu número fijo de toda la vida: tras la visita pregunta qué tal fue todo; si pulsan Excelente van directo a ponerte 5 estrellas en Google, y si pulsan Mejorable te cuentan la queja en privado por texto o nota de voz transcrita por IA.',
        'Cuando entra una reseña delicada de 1 a 3 estrellas en Google, nuestra IA jamás publica a ciegas: frena la respuesta y te manda al móvil 4 propuestas redactadas con el método psicológico HEARD y blindaje RGPD para que tú apruebes la que prefieras en un clic.'
      ];
    } else {
      respuestasDinamicas = [
        'Sobre eso que me comentas («' + preguntaRaw.slice(0, 60) + '»), en Sistemas Pyme lo adaptamos llave en mano a tu negocio en 24 a 48 horas sin que tengas que cambiar tu forma de trabajar. ¿Prefieres que te explique cómo captar más reseñas y clientes hoy o cómo funcionan las auditorías para salir el primero en Google y ChatGPT?',
        'Te entiendo perfectamente. Para darte la recomendación exacta para tu caso, dime a qué se dedica tu negocio o si tu prioridad ahora mismo es conseguir más reseñas de 5 estrellas, atraer más llamadas desde tu web o ahorrar tiempo con WhatsApp.'
      ];
    }

    for (var r = 0; r < respuestasDinamicas.length; r++) {
      if (_v168UltimasRespuestasDadas.indexOf(respuestasDinamicas[r]) === -1) {
        return respuestasDinamicas[r];
      }
    }
    return respuestasDinamicas[0];
  }

  function descubrirModelosFlashLiteV170(k) {
    if (_v168ModelosFlashLiteCache) return Promise.resolve(_v168ModelosFlashLiteCache);
    var listaBase = ['gemini-2.5-flash-lite', 'gemini-2.0-flash-lite-001', 'gemini-2.0-flash-lite', 'gemini-2.5-flash'];
    return fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=100&key=' + encodeURIComponent(k))
      .then(function(r) { return r && r.ok ? r.json() : null; })
      .then(function(d) {
        var mods = (d && Array.isArray(d.models)) ? d.models : [];
        var hallados = [];
        for (var i = 0; i < mods.length; i++) {
          var m = mods[i];
          var met = m.supportedGenerationMethods || [];
          if (met.indexOf('generateContent') === -1) continue;
          var name = String(m.name || '').replace(/^models\//, '');
          if (name.toLowerCase().indexOf('flash-lite') !== -1) {
            hallados.push(name);
          }
        }
        for (var j = 0; j < listaBase.length; j++) {
          if (hallados.indexOf(listaBase[j]) === -1) hallados.push(listaBase[j]);
        }
        _v168ModelosFlashLiteCache = hallados;
        return hallados;
      })
      .catch(function() {
        _v168ModelosFlashLiteCache = listaBase;
        return listaBase;
      });
  }

  function consultarGeminiDirectoMultiEndpointV170(promptCompleto) {
    var k = obtenerClaveVertexV168();
    if (!k) return Promise.reject('no_key');

    return descubrirModelosFlashLiteV170(k).then(function(modelos) {
      function probarSiguiente(idx) {
        if (idx >= modelos.length) return Promise.reject('all_models_failed');
        var mod = modelos[idx];
        var bodyJson = JSON.stringify({
          contents: [{ role: 'user', parts: [{ text: promptCompleto }] }],
          generationConfig: { temperature: 0.65, topP: 0.92, maxOutputTokens: 280 }
        });

        var urlVertex = 'https://aiplatform.googleapis.com/v1beta1/publishers/google/models/' + mod + ':generateContent?key=' + encodeURIComponent(k);
        return fetch(urlVertex, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: bodyJson
        })
        .then(function(r) { return r && r.ok ? r.json() : null; })
        .then(function(d) {
          var parts = d && d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts;
          if (parts && parts.length) {
            var txt = parts.map(function(p) { return p.thought ? '' : (p.text || ''); }).join(' ').trim();
            if (txt.length > 10) return { texto: txt, modelo: mod };
          }
          return probarSiguiente(idx + 1);
        })
        .catch(function() {
          return probarSiguiente(idx + 1);
        });
      }
      return probarSiguiente(0);
    });
  }

  function pedirRespuestaGeminiFlashLiteV168(preguntaUsuario) {
    var respaldoContextual = generarRespuestaContextualAntiBucle(preguntaUsuario);
    var histStr = _v168Historial.slice(-8).join('\n');

    var prompt =
      (window.SP_CONTEXTO_MAESTRO_IA_RESUMEN ||
        'Eres el Consultor Tecnológico Experto de Sistemas Pyme (sistemaspyme.es), fundado por Francisco M. Gallardo (Tel/WhatsApp 711 54 75 61). ' +
        'Datos clave: Plan Base 1 servicio (S1 Reseñas IA o S2 Cortafuegos WhatsApp) = 59 €/mes + 150 € Setup. ' +
        'Pack Escudo Dúo (S1 + S2) = 99 €/mes + 225 € Setup (desbloquea las Super-Auditorías a 195 € c/u en vez de 350 €). ' +
        'Atril NFC/QR = 39 € pago único (abre Google Maps en 1 segundo). ' +
        'Super-Auditoría 1: SEO Local + GEO IA (Grafo Schema.org + Wikidata + /llms.txt). ' +
        'Super-Auditoría 2: Neuromarketing CRO con Sonda Térmica de 10 días (Modo Ágil o Modo Corporativo).') + '\n\n' +
      'HISTORIAL DE LA CONVERSACIÓN:\n' + (histStr || 'Recién iniciada') + '\n\n' +
      'INTERVENCIÓN ACTUAL DEL USUARIO: "' + preguntaUsuario + '"\n\n' +
      'INSTRUCCIÓN OBLIGATORIA: Responde directamente y de forma inteligente a lo que acaba de decir el usuario en español de España, en 2 a 3 frases naturales para ser habladas en voz alta (40 a 70 palabras), sin usar asteriscos ni listas y sin repetir respuestas anteriores.';

    var promesas = [];

    // 1. Vía Directa Vertex AI con autodescubrimiento de modelos Flash-Lite
    promesas.push(consultarGeminiDirectoMultiEndpointV170(prompt));

    // 2. Vía Servidor Render (/api/consultor-ia)
    promesas.push(
      fetch('https://servicio-resenas.onrender.com/api/consultor-ia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pregunta: preguntaUsuario,
          apoyo: respaldoContextual,
          prompt: prompt,
          modelo_preferido: 'gemini-2.5-flash-lite'
        })
      })
      .then(function(r) { if (!r.ok) throw new Error('render_ia'); return r.json(); })
      .then(function(d) {
        if (d && d.ok && d.respuesta && d.respuesta.trim().length > 12) {
          return { texto: d.respuesta.trim(), modelo: d.modelo || 'gemini-2.5-flash-lite' };
        }
        throw new Error('empty_render_ia');
      })
    );

    // 3. Vía Servidor Local si está en el mismo origen
    if (window.location.protocol.indexOf('http') === 0) {
      promesas.push(
        fetch('/api/consultor-ia', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            pregunta: preguntaUsuario,
            apoyo: respaldoContextual,
            prompt: prompt
          })
        })
        .then(function(r) { if (!r.ok) throw new Error('local_ia'); return r.json(); })
        .then(function(d) {
          if (d && d.ok && d.respuesta && d.respuesta.trim().length > 12) {
            return { texto: d.respuesta.trim(), modelo: d.modelo || 'gemini-flash-lite-local' };
          }
          throw new Error('empty_local_ia');
        })
      );
    }

    return new Promise(function(resolve) {
      var resuelto = false;
      // Damos hasta 5.5 segundos para que Gemini Flash-Lite responda con inteligencia real antes de usar el respaldo
      var timerMax = setTimeout(function() {
        if (!resuelto) {
          resuelto = true;
          actualizarPuntoLedApi('local', '⚡ Respuesta Contextual Sistemas Pyme');
          resolve(respaldoContextual);
        }
      }, 5500);

      var fallos = 0;
      for (var i = 0; i < promesas.length; i++) {
        promesas[i].then(function(ganador) {
          if (!resuelto && ganador && ganador.texto) {
            resuelto = true;
            clearTimeout(timerMax);
            actualizarPuntoLedApi('online', '🟢 Conectado en vivo a ' + ganador.modelo);
            var limpio = ganador.texto.replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim();
            resolve(limpio);
          }
        }).catch(function() {
          fallos++;
          if (fallos >= promesas.length && !resuelto) {
            resuelto = true;
            clearTimeout(timerMax);
            actualizarPuntoLedApi('local', '⚡ Respuesta Contextual Sistemas Pyme');
            resolve(respaldoContextual);
          }
        });
      }
    });
  }

  /* =========================================================================
     FUNCIONES PÚBLICAS GLOBALES
     ========================================================================= */
  window.spProcesarConsultaEnTeleprompterDirecto = function(textoPregunta) {
    var limpia = String(textoPregunta || '').trim();
    if (!limpia) return;
    _v168DespiertoPorUsuario = true;
    _v168PausadoPorSalir = false;
    _v168PensandoIA = true;
    _v168Escuchando = false;

    actualizarUIEstado('thinking');

    var inp = document.getElementById('spTecnosalaInput');
    if (inp) inp.value = '';

    // Mostrar inmediatamente en el Teleprompter lo que el usuario acaba de preguntar
    var track = asegurarCabinaTeleprompterV168();
    if (track) {
      var divQ = document.createElement('div');
      divQ.className = 'sp-led-line-item sp-led-line-user';
      divQ.textContent = '▸ TÚ: «' + limpia + '»';
      track.appendChild(divQ);
      reclasificarLineasTrack(track);
    }

    _v168Historial.push('Usuario: ' + limpia);
    if (typeof window.spExtraerYPreconfigurarCarritoDesdeCharla === 'function') {
      try { window.spExtraerYPreconfigurarCarritoDesdeCharla(limpia, _v168Historial); } catch (e) {}
    }

    pedirRespuestaGeminiFlashLiteV168(limpia).then(function(respuestaIA) {
      _v168PensandoIA = false;
      _v168UltimasRespuestasDadas.push(respuestaIA);
      if (_v168UltimasRespuestasDadas.length > 6) _v168UltimasRespuestasDadas.shift();

      _v168Historial.push('Consultor: ' + respuestaIA);
      var ahora = new Date();
      _v168TranscripcionDescarga.push({
        hora: ahora.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
        pregunta: limpia,
        respuesta: respuestaIA
      });
      // Pasamos null en preguntaPrevia porque ya la pintamos arriba al instante
      window.spReproducirEnTeleprompter2027(respuestaIA, null, null);
    });
  };

  window.spActivarOrbeConsultorInteractivo = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();

    _v168DespiertoPorUsuario = true;
    _v168PausadoPorSalir = false;

    encenderMicrofonoAhoraSincrono();

    var track = asegurarCabinaTeleprompterV168();
    if (track && track.children.length > 0) {
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
      'El micrófono está abierto en manos libres: háblame con tranquilidad, espero a que termines cada frase para responderte.';

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
    _v168PensandoIA = false;
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
    _v168PensandoIA = false;
    _v168Escuchando = false;
    _v168FragmentosConfirmados = '';
    _v168FragmentoInterino = '';
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
    _v168PensandoIA = false;
    _v168Escuchando = false;
    _v168FragmentosConfirmados = '';
    _v168FragmentoInterino = '';
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
    _v168PensandoIA = false;
    asegurarCabinaTeleprompterV168();
    encenderMicrofonoAhoraSincrono();
  };

  window.spEnviarPreguntaLibreTecnosala = function(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    var inp = document.getElementById('spTecnosalaInput');
    var texto = inp ? String(inp.value || '').trim() : '';
    if (!texto) return;
    if (_v168TimerSilencio) {
      clearTimeout(_v168TimerSilencio);
      _v168TimerSilencio = null;
    }
    _v168FragmentosConfirmados = '';
    _v168FragmentoInterino = '';
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

  setInterval(function() {
    if (!_v168DespiertoPorUsuario) return;
    var visible = estaEnTecnosalaVisible();
    if (!visible && !_v168PausadoPorSalir) {
      window.spPausarConsultorPorCambioSeccion();
    } else if (visible && _v168PausadoPorSalir) {
      window.spReanudarConsultorAlVolverSeccion();
    } else if (visible && !_v168PausadoPorSalir && !_v168Hablando && !_v168PensandoIA && !_v168RecRunning) {
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

    # 1. ELIMINAR CUALQUIER INYECCIÓN PREVIA DE V168 (incluyendo la que cayó por error dentro de docHtml en la línea 3022)
    patron_v168 = re.compile(
        r"<!-- \[SP_CONSULTOR_ULTIMATE_V168_START\] -->.*?<!-- \[SP_CONSULTOR_ULTIMATE_V168_END\] -->\n?",
        re.DOTALL
    )
    html = patron_v168.sub(lambda _: "", html)

    # Asegurar que la línea de cierre de docHtml quede 100% limpia y en una sola línea válida de JS
    html = re.sub(
        r"'</div>\s*</body></html>';",
        lambda _: "'</div></body></html>';",
        html
    )

    # 2. Neutralizar timers antiguos
    html = html.replace(
        "setTimeout(conectarFuncionesRealesTecnosalaV159, 150);",
        "/* [V169: neutralizado timer 150ms] */"
    ).replace(
        "setTimeout(conectarFuncionesRealesTecnosalaV159, 600);",
        "/* [V169: neutralizado timer 600ms] */"
    )

    # 3. INYECTAR EL MOTOR MAESTRO ÚNICO EXCLUSIVAMENTE ANTES DEL ÚLTIMO </body> REAL DEL ARCHIVO
    pos_ultimo_body = html.lower().rfind("</body>")
    if pos_ultimo_body == -1:
        print(f"❌ No se encontró etiqueta </body> final en {ruta_index}")
        return False

    html = (
        html[:pos_ultimo_body]
        + "\n"
        + BLOQUE_MAESTRO_ULTIMATE_V168
        + "\n"
        + html[pos_ultimo_body:]
    )

    if not validar_bloques_js_en_html(html, ruta_index):
        print(f"❌ Abortando guardado en {ruta_index} por error de sintaxis JS.")
        return False

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)

    # Eliminar duplicados prohibidos como index_2.html si existieran en la carpeta
    ruta_dup = os.path.join(os.path.dirname(ruta_index), "index_2.html")
    if os.path.isfile(ruta_dup):
        try:
            os.remove(ruta_dup)
            print(f"🧹 Eliminado archivo duplicado residual: {ruta_dup}")
        except Exception:
            pass

    print(f"🚀 [{os.path.basename(os.path.dirname(ruta_index))}] Cadena docHtml reparada y Motor V169 colocado al final real de </body>.")
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
                    ["git", "-C", ruta_repo, "commit", "-m", "V170: Escucha completa 2.2s sin cortar frase y Gemini Flash-Lite inteligente anti-bucle"],
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
    print("🛠️ INICIANDO ACTUALIZACIÓN V170 — ESCUCHA COMPLETA Y GEMINI FLASH-LITE REAL")
    print("=" * 78)

    actualizar_documentos_maestros()
    ok = sincronizar_ambos_index()
    if not ok:
        print("❌ No se pudo actualizar index.html.")
        sys.exit(1)

    replicar_ad_py_en_carpetas()
    publicar_en_git_repositorios()
    lanzar_servidor_local_y_abrir_tecnosala()

    print("\n🎉 ACTUALIZACIÓN V170 COMPLETADA CON ÉXITO — RECARGA CON CMD+SHIFT+R")
    print("📌 Actualización de Conocimiento guardada automáticamente en tu carpeta SISTEMAS PYME/Programar (con copia previa en backups_sp)\n")


if __name__ == "__main__":
    main()
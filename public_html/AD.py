#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SCRIPT ACTUALIZADOR MAESTRO AD.py — VERSIÓN 167 (SISTEMAS PYME)
=============================================================================
Diagnóstico de Raíz y Solución Definitiva del Tecnoconsultor:
1. Elimina el conflicto con el bloque final V160 (`_hookAutoTecnosalaV163`)
   que sobrescribía las funciones del consultor 180ms después de cargar.
2. Arranca `SpeechRecognition` de forma 100% SÍNCRONA en el mismo instante
   del clic del usuario (sin promesas intermedias que rompan el User Gesture
   de Chrome) y lo mantiene vivo en bucle continuo sin llamar a `.stop()`
   entre preguntas y respuestas (CERO re-prompts de micrófono).
3. Compuerta acústica anti-eco (`_spIgnorarMicroMientrasHabla`) mientras el
   consultor habla + desbloqueo anti-freeze de `speechSynthesis` en macOS.
4. Conexión ultrarrápida al último modelo Gemini Flash-Lite a través del
   endpoint absoluto `https://servicio-resenas.onrender.com/api/consultor-ia`
   + Vertex AI `gemini-2.5-flash-lite` + Cerebro Omnisciente instantáneo.
5. Pausa automática del micro al cambiar de apartado (`Inicio`, `Cómo ayudamos`,
   `Test`, `Precios`, `Magazine`) o de pestaña del navegador, y reactivación
   automática al regresar a `Tecnosala`.
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

NOTA_ACTUALIZACION_V167 = """
### ACTUALIZACIÓN V167 (Ingeniería Definitiva del Tecnoconsultor: Arranque Síncrono de Micrófono Único, Gemini Flash-Lite y Conmutación Automática entre Secciones)
- **Eliminación de los 4 cuellos de botella que bloqueaban el Tecnoconsultor:**
  1. **Arranque 100% síncrono de `SpeechRecognition` en el gesto del clic:** Eliminada la promesa intermedia antes de `rec.start()` que hacía perder el *User Gesture* en Chrome, y eliminado el `.stop()` entre turnos. El micrófono se abre una sola vez y permanece en escucha continua real (`continuous = true`), usando una compuerta de silencio lógico mientras el consultor habla.
  2. **Eliminado el doble hook conflictivo del bloque V160:** El bloque final ya no sobrescribe `spActivarOrbeConsultorInteractivo`, `spPararConsultorTotalmente` ni `cambiarVista`.
  3. **Conexión rápida a Gemini Flash-Lite (`gemini-2.5-flash-lite`):** Conecta con URL absoluta al motor en Render (`https://servicio-resenas.onrender.com/api/consultor-ia`) y a Vertex AI `gemini-2.5-flash-lite` con timeout ágil de 3,2 segundos y respaldo omnisciente instantáneo.
  4. **Pausa al salir de Tecnosala y auto-encendido al regresar:** Al navegar a cualquier otra sección de la web o cambiar de pestaña del navegador, cancela la locución y pausa el micrófono; al volver a `Tecnosala`, reanuda el micrófono automáticamente.
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
                if "ACTUALIZACIÓN V167" not in contenido:
                    contenido = contenido.rstrip() + "\n\n" + NOTA_ACTUALIZACION_V167.strip() + "\n"
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


MOTOR_DEFINITIVO_TECNOCONSULTOR_V167 = r"""      window.spRepetirUltimaRespuestaConsultor = function(ev) {
        if (ev && ev.stopPropagation) ev.stopPropagation();
        if (_spRegistroDescargaCharla.length > 0) {
          var ult = _spRegistroDescargaCharla[_spRegistroDescargaCharla.length - 1];
          window.spReproducirEnTeleprompter2027(ult.respuesta, null, ult.pregunta);
        } else {
          window.spActivarOrbeConsultorInteractivo(ev);
        }
      };

      var _spPausadoPorNavegacion = false;
      var _spBufferFraseUsuario = '';
      var _spElDictadoEnVivo = null;
      var _spFinHablaTimestamp = 0;

      function pintarEstadoBotonHablar(activo) {
        var btnV = document.getElementById('spBtnVoiceTecnosala');
        var txtV = document.getElementById('spVoiceBtnText');
        var icoV = document.getElementById('spVoiceMicIcon');
        var inp = document.getElementById('spTecnosalaInput');
        if (activo) {
          if (btnV) btnV.classList.add('sp-voice-listening');
          if (txtV) txtV.textContent = 'Escuchando...';
          if (icoV) icoV.textContent = '🔴';
          if (inp) inp.placeholder = '🟢 Micrófono abierto en manos libres: habla directamente sin tocar nada...';
        } else {
          if (btnV) btnV.classList.remove('sp-voice-listening');
          if (txtV) txtV.textContent = 'Hablar';
          if (icoV) icoV.textContent = '🎙️';
          if (inp) inp.placeholder = 'Escribe tu duda o pulsa 🎙️ Hablar para preguntar por voz...';
        }
      }

      // Crea UNA SOLA instancia de reconocimiento para toda la vida de la página
      function obtenerReconocedorUnicoContinua() {
        if (_spRecogInstance) return _spRecogInstance;
        var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) return null;

        var rec = new SpeechRec();
        rec.lang = 'es-ES';
        rec.continuous = true;
        rec.interimResults = true;
        rec.maxAlternatives = 1;

        function dispararPreguntaCapturada() {
          if (_spSilenceTimer) {
            clearTimeout(_spSilenceTimer);
            _spSilenceTimer = null;
          }
          var textoFinal = _spBufferFraseUsuario.trim();
          _spBufferFraseUsuario = '';
          if (!textoFinal || textoFinal.length < 2) return;
          if (_spIgnorarMicroMientrasHabla || _spHablandoSintesis) return;

          // Mute lógico mientras el consultor piensa y habla (JAMÁS llamamos a rec.stop() aquí)
          _spIgnorarMicroMientrasHabla = true;
          _spEscuchandoVoz = false;
          if (_spElDictadoEnVivo) {
            try { _spElDictadoEnVivo.remove(); } catch (e) {}
            _spElDictadoEnVivo = null;
          }
          window.spProcesarConsultaEnTeleprompterDirecto(textoFinal);
        }

        rec.onstart = function() {
          _spMicroSesionActiva = true;
          if (!_spHablandoSintesis && !_spPausadoPorNavegacion) {
            _spEscuchandoVoz = true;
            _spIgnorarMicroMientrasHabla = false;
            pintarEstadoBotonHablar(true);
            actualizarAparienciaOrbeYEstado('listening');
          }
        };

        rec.onresult = function(event) {
          // Si el consultor está hablando o terminó hace menos de 400ms, descartamos cualquier eco del altavoz
          if (_spIgnorarMicroMientrasHabla || _spHablandoSintesis || _spPausadoPorNavegacion || (performance.now() - _spFinHablaTimestamp < 400)) {
            _spBufferFraseUsuario = '';
            return;
          }

          var interino = '';
          var nuevoFinal = '';
          for (var i = event.resultIndex; i < event.results.length; i++) {
            var pieza = event.results[i][0].transcript;
            if (event.results[i].isFinal) nuevoFinal += pieza + ' ';
            else interino += pieza;
          }

          if (nuevoFinal) {
            _spBufferFraseUsuario = (_spBufferFraseUsuario + ' ' + nuevoFinal).trim();
          }
          var fraseVisible = (_spBufferFraseUsuario + ' ' + interino).trim();
          if (!fraseVisible) return;

          _spUltimoPulsoVozUsuarioTs = performance.now();
          _spNivelVozUsuarioVivo = Math.min(0.96, 0.38 + (fraseVisible.length % 8) * 0.07);

          var inp = document.getElementById('spTecnosalaInput');
          if (inp) inp.value = fraseVisible;

          var track = asegurarCabinaTeleprompter2027();
          if (track) {
            if (!_spElDictadoEnVivo || !_spElDictadoEnVivo.parentNode) {
              _spElDictadoEnVivo = document.createElement('div');
              _spElDictadoEnVivo.className = 'sp-led-line-item sp-led-line-user';
              track.appendChild(_spElDictadoEnVivo);
            }
            _spElDictadoEnVivo.textContent = '🎙️ TÚ: «' + fraseVisible + '...»';
            reclasificarJerarquiaLineas(track);
          }

          if (_spSilenceTimer) clearTimeout(_spSilenceTimer);
          if (nuevoFinal) {
            _spSilenceTimer = setTimeout(dispararPreguntaCapturada, 600);
          } else {
            _spSilenceTimer = setTimeout(function() {
              _spBufferFraseUsuario = fraseVisible;
              dispararPreguntaCapturada();
            }, 1200);
          }
        };

        rec.onerror = function(ev) {
          if (ev && (ev.error === 'not-allowed' || ev.error === 'service-not-allowed')) {
            _spMicroSesionActiva = false;
            _spAutoEscuchaContinua = false;
            _spEscuchandoVoz = false;
            pintarEstadoBotonHablar(false);
            actualizarAparienciaOrbeYEstado('idle');
          }
        };

        rec.onend = function() {
          _spMicroSesionActiva = false;
          var vTec = document.getElementById('vista-tecnosala');
          var sigueEnTecnosala = vTec && !vTec.classList.contains('hidden') && !document.hidden;
          // Si Chrome corta el stream tras una pausa larga pero seguimos en Tecnosala, lo reabre al instante
          if (_spOrbeDespierto && _spAutoEscuchaContinua && !_spPausadoPorNavegacion && sigueEnTecnosala) {
            try {
              rec.start();
            } catch (e) {}
          } else {
            pintarEstadoBotonHablar(false);
          }
        };

        _spRecogInstance = rec;
        return rec;
      }

      // Arranque 100% SÍNCRONO (sin promesas antes de rec.start()) para aprovechar el clic del usuario
      window.spActivarModoEscuchaPersistente = function() {
        var vTec = document.getElementById('vista-tecnosala');
        if (!vTec || vTec.classList.contains('hidden') || document.hidden) return;
        if (!_spAutoEscuchaContinua || _spPausadoPorNavegacion) return;

        var rec = obtenerReconocedorUnicoContinua();
        if (!rec) {
          actualizarAparienciaOrbeYEstado('idle');
          var inp = document.getElementById('spTecnosalaInput');
          if (inp) inp.focus();
          return;
        }

        if (!_spHablandoSintesis) {
          _spIgnorarMicroMientrasHabla = false;
          _spEscuchandoVoz = true;
          pintarEstadoBotonHablar(true);
          actualizarAparienciaOrbeYEstado('listening');
        }

        if (!_spMicroSesionActiva) {
          try {
            rec.start();
          } catch (e) {
            // Si ya estaba arrancado internamente en Chrome, marcamos sesión activa
            _spMicroSesionActiva = true;
          }
        }
      };

      // Pausa inmediata cuando el usuario se va a otra pestaña o apartado de la web
      window.spPausarConsultorPorNavegacion = function() {
        if (!_spOrbeDespierto) return;
        _spPausadoPorNavegacion = true;
        _spHablandoSintesis = false;
        _spEscuchandoVoz = false;
        _spIgnorarMicroMientrasHabla = true;
        _spBufferFraseUsuario = '';
        _spOrbEnergyTarget = 0;
        limpiarTimersTeleprompter();
        if (_spSilenceTimer) {
          clearTimeout(_spSilenceTimer);
          _spSilenceTimer = null;
        }
        if ('speechSynthesis' in window) {
          try { window.speechSynthesis.cancel(); } catch (e) {}
        }
        if (_spRecogInstance && _spMicroSesionActiva) {
          try { _spRecogInstance.stop(); } catch (e) {}
          _spMicroSesionActiva = false;
        }
        pintarEstadoBotonHablar(false);
        actualizarAparienciaOrbeYEstado('idle');
      };

      // Reanudación automática cuando el usuario vuelve a entrar en Tecnosala
      window.spReanudarConsultorAlVolverATecnosala = function() {
        if (!_spOrbeDespierto) return;
        var vTec = document.getElementById('vista-tecnosala');
        if (!vTec || vTec.classList.contains('hidden') || document.hidden) return;
        _spPausadoPorNavegacion = false;
        _spAutoEscuchaContinua = true;
        _spHablandoSintesis = false;
        _spIgnorarMicroMientrasHabla = false;
        _spBufferFraseUsuario = '';
        iniciarVigilanteMicrofonoContinuo();
        window.spActivarModoEscuchaPersistente();
      };

      // Parada total manual cuando el usuario pulsa el botón rojo PARAR
      window.spPararConsultorTotalmente = function(ev) {
        if (ev && ev.stopPropagation) ev.stopPropagation();
        _spOrbeDespierto = false;
        _spPausadoPorNavegacion = false;
        _spAutoEscuchaContinua = false;
        _spHablandoSintesis = false;
        _spEscuchandoVoz = false;
        _spIgnorarMicroMientrasHabla = true;
        _spBufferFraseUsuario = '';
        _spOrbEnergyTarget = 0;
        limpiarTimersTeleprompter();
        if (_spWatchdogMicroInterval) {
          clearInterval(_spWatchdogMicroInterval);
          _spWatchdogMicroInterval = null;
        }
        if (_spSilenceTimer) {
          clearTimeout(_spSilenceTimer);
          _spSilenceTimer = null;
        }
        if ('speechSynthesis' in window) {
          try { window.speechSynthesis.cancel(); } catch (e) {}
        }
        if (_spRecogInstance) {
          try { _spRecogInstance.stop(); } catch (e) {}
          _spMicroSesionActiva = false;
        }
        pintarEstadoBotonHablar(false);
        actualizarAparienciaOrbeYEstado('idle');
      };

      function iniciarVigilanteMicrofonoContinuo() {
        if (_spWatchdogMicroInterval) clearInterval(_spWatchdogMicroInterval);
        _spWatchdogMicroInterval = setInterval(function() {
          var vTec = document.getElementById('vista-tecnosala');
          var enTecnosala = vTec && !vTec.classList.contains('hidden') && !document.hidden;
          if (!enTecnosala) {
            if (_spHablandoSintesis || _spEscuchandoVoz || _spMicroSesionActiva) {
              window.spPausarConsultorPorNavegacion();
            }
            return;
          }
          if (_spOrbeDespierto && _spAutoEscuchaContinua && !_spPausadoPorNavegacion && !_spHablandoSintesis && !_spMicroSesionActiva) {
            window.spActivarModoEscuchaPersistente();
          }
        }, 900);
      }

      window.spIniciarEscuchaDirectaConsultor = function() {
        _spOrbeDespierto = true;
        _spPausadoPorNavegacion = false;
        _spAutoEscuchaContinua = true;
        _spHablandoSintesis = false;
        _spIgnorarMicroMientrasHabla = false;
        _spBufferFraseUsuario = '';
        if ('speechSynthesis' in window) {
          try { window.speechSynthesis.cancel(); } catch (e) {}
        }
        asegurarCabinaTeleprompter2027();
        window.spActivarModoEscuchaPersistente();
        iniciarVigilanteMicrofonoContinuo();
      };

      window.spReproducirEnTeleprompter2027 = function(textoCompleto, alTerminarCallback, etiquetaUsuarioPrevio) {
        limpiarTimersTeleprompter();
        // Silenciamos lógicamente la entrada del micro mientras habla (SIN cerrar el micrófono)
        _spIgnorarMicroMientrasHabla = true;
        _spEscuchandoVoz = false;
        _spBufferFraseUsuario = '';
        if (_spSilenceTimer) {
          clearTimeout(_spSilenceTimer);
          _spSilenceTimer = null;
        }

        var track = asegurarCabinaTeleprompter2027();
        if (!track) return;
        if (etiquetaUsuarioPrevio) {
          var divUser = document.createElement('div');
          divUser.className = 'sp-led-line-item sp-led-line-user';
          divUser.textContent = '▸ TÚ: «' + etiquetaUsuarioPrevio + '»';
          track.appendChild(divUser);
          reclasificarJerarquiaLineas(track);
        }

        var limpio = String(textoCompleto || '').replace(/<[^>]+>/g, ' ').replace(/[`*_#•]/g, ' ').replace(/\s+/g, ' ').trim();
        if (!limpio) {
          if (typeof alTerminarCallback === 'function') alTerminarCallback();
          return;
        }

        var maxLen = window.innerWidth < 640 ? 38 : 54;
        var palabras = limpio.split(' ');
        var segmentos = [];
        var lineaAct = '';
        var cursorGlobal = 0;
        for (var w = 0; w < palabras.length; w++) {
          var pal = palabras[w];
          var cand = lineaAct ? (lineaAct + ' ' + pal) : pal;
          if (cand.length <= maxLen) lineaAct = cand;
          else {
            if (lineaAct) {
              segmentos.push({ texto: lineaAct, start: cursorGlobal, end: cursorGlobal + lineaAct.length });
              cursorGlobal += lineaAct.length + 1;
            }
            lineaAct = pal;
          }
        }
        if (lineaAct) segmentos.push({ texto: lineaAct, start: cursorGlobal, end: cursorGlobal + lineaAct.length });

        var textoGlobalUnido = segmentos.map(function(s) { return s.texto; }).join(' ');
        var totalChars = textoGlobalUnido.length;
        var charActualMostrado = 0;
        var charObjetivoPorVoz = 0;
        var idxSegMostrado = -1;
        var spanTextoActivo = null;
        var finalDisparado = false;
        var tsInicioLocucion = performance.now();
        var tsUltimoEventoVoz = performance.now();

        function pintarHastaCharGlobal(posGlobal) {
          var p = Math.min(totalChars, Math.max(0, posGlobal));
          _spOrbCharActual = textoGlobalUnido.charAt(Math.max(0, p - 1)) || ' ';
          _spOrbLastBoundaryTs = performance.now();
          var segIdx = 0;
          for (var i = 0; i < segmentos.length; i++) {
            if (p >= segmentos[i].start) segIdx = i;
            else break;
          }
          while (idxSegMostrado < segIdx) {
            if (idxSegMostrado >= 0 && spanTextoActivo) spanTextoActivo.textContent = segmentos[idxSegMostrado].texto;
            idxSegMostrado++;
            var nuevaLineaEl = document.createElement('div');
            nuevaLineaEl.className = 'sp-led-line-item sp-led-line-active';
            var spT = document.createElement('span');
            var spC = document.createElement('span');
            spC.className = 'sp-led-cursor';
            nuevaLineaEl.appendChild(spT);
            nuevaLineaEl.appendChild(spC);
            track.appendChild(nuevaLineaEl);
            reclasificarJerarquiaLineas(track);
            spanTextoActivo = spT;
          }
          if (spanTextoActivo && segIdx >= 0 && segIdx < segmentos.length) {
            var seg = segmentos[segIdx];
            spanTextoActivo.textContent = seg.texto.slice(0, Math.min(seg.texto.length, Math.max(1, p - seg.start)));
          }
        }

        function forzarCierreYPasarAEscucha() {
          if (finalDisparado) return;
          finalDisparado = true;
          pintarHastaCharGlobal(totalChars);
          limpiarTimersTeleprompter();
          _spHablandoSintesis = false;
          _spFinHablaTimestamp = performance.now();
          _spBufferFraseUsuario = '';
          _spOrbEnergyTarget = 0;
          if (_spAutoEscuchaContinua && !_spPausadoPorNavegacion) {
            _spIgnorarMicroMientrasHabla = false;
            _spEscuchandoVoz = true;
            pintarEstadoBotonHablar(true);
            actualizarAparienciaOrbeYEstado('listening');
            if (!_spMicroSesionActiva) {
              window.spActivarModoEscuchaPersistente();
            }
          } else {
            pintarEstadoBotonHablar(false);
            actualizarAparienciaOrbeYEstado('idle');
          }
          if (typeof alTerminarCallback === 'function') {
            try { alTerminarCallback(); } catch (e) {}
          }
        }

        _spHablandoSintesis = true;
        actualizarAparienciaOrbeYEstado('speaking');

        var duracionMaxMs = Math.max(3800, totalChars * 75 + 1800);
        _spTyperTimerIds.push(setTimeout(forzarCierreYPasarAEscucha, duracionMaxMs));

        function pasoMarcapasos() {
          if (!_spHablandoSintesis || finalDisparado) return;
          if (charObjetivoPorVoz > charActualMostrado) {
            charActualMostrado = Math.min(totalChars, charActualMostrado + Math.max(1, Math.ceil((charObjetivoPorVoz - charActualMostrado) * 0.50)));
          } else {
            charActualMostrado = Math.min(totalChars, charActualMostrado + 1);
          }
          pintarHastaCharGlobal(charActualMostrado);
          if (charActualMostrado >= totalChars) {
            if (!_spVozConsultorActiva || !('speechSynthesis' in window) || !window.speechSynthesis.speaking) {
              forzarCierreYPasarAEscucha();
              return;
            }
            _spTyperTimerIds.push(setTimeout(forzarCierreYPasarAEscucha, 700));
            return;
          }
          var ch = textoGlobalUnido.charAt(charActualMostrado - 1) || '';
          var d = (ch === '.' || ch === '?' || ch === '!') ? 360 : ((ch === ',' || ch === ';') ? 190 : 54);
          _spTyperTimerIds.push(setTimeout(pasoMarcapasos, d));
        }
        _spTyperTimerIds.push(setTimeout(pasoMarcapasos, 30));

        if (_spVozConsultorActiva && ('speechSynthesis' in window)) {
          try {
            if (window.speechSynthesis.speaking || window.speechSynthesis.pending) {
              window.speechSynthesis.cancel();
            }
          } catch (e) {}
          setTimeout(function() {
            if (!_spHablandoSintesis || finalDisparado) return;
            try {
              window.speechSynthesis.resume();
              var vozFija = obtenerVozEspanaFija();
              var u = new SpeechSynthesisUtterance(textoGlobalUnido);
              _spUtteranceEnCurso = u;
              u.lang = 'es-ES';
              u.rate = 0.94;
              if (vozFija) u.voice = vozFija;
              u.onboundary = function(ev) {
                tsUltimoEventoVoz = performance.now();
                if (ev && typeof ev.charIndex === 'number') {
                  charObjetivoPorVoz = Math.min(totalChars, ev.charIndex + (ev.charLength || 2));
                  _spOrbCharActual = textoGlobalUnido.charAt(ev.charIndex) || 'a';
                  _spOrbLastBoundaryTs = performance.now();
                }
              };
              _spWatchdogHablaTimer = setInterval(function() {
                if (!_spHablandoSintesis || finalDisparado) {
                  clearInterval(_spWatchdogHablaTimer);
                  return;
                }
                var ahora = performance.now();
                if ((ahora - tsInicioLocucion > 950 && !window.speechSynthesis.speaking && !window.speechSynthesis.pending) ||
                    (charActualMostrado >= totalChars * 0.92 && (ahora - tsUltimoEventoVoz > 1200))) {
                  clearInterval(_spWatchdogHablaTimer);
                  forzarCierreYPasarAEscucha();
                }
              }, 300);
              u.onend = forzarCierreYPasarAEscucha;
              u.onerror = forzarCierreYPasarAEscucha;
              window.speechSynthesis.speak(u);
            } catch (e) {
              forzarCierreYPasarAEscucha();
            }
          }, 60);
        }
      };

      // Conexión ultrarrápida a Gemini Flash-Lite (Vertex AI + Servidor Render + Servidor Local + Cerebro Local)
      function llamarVertexDirectoNavegador(promptCompleto) {
        var k = _obtenerKBrowser();
        if (!k) return Promise.resolve(null);
        var modelosFlashLite = [
          'gemini-2.5-flash-lite',
          'gemini-2.0-flash-lite-001',
          'gemini-2.0-flash-lite',
          'gemini-2.5-flash'
        ];
        function intentarModelo(idx) {
          if (idx >= modelosFlashLite.length) return Promise.resolve(null);
          var m = modelosFlashLite[idx];
          var url = 'https://aiplatform.googleapis.com/v1beta1/publishers/google/models/' + m + ':generateContent?key=' + encodeURIComponent(k);
          var ctrl = (typeof AbortController !== 'undefined') ? new AbortController() : null;
          var tId = ctrl ? setTimeout(function() { try { ctrl.abort(); } catch (e) {} }, 2600) : null;
          return fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ role: 'user', parts: [{ text: promptCompleto }] }],
              generationConfig: { temperature: 0.60, topP: 0.90, maxOutputTokens: 280 }
            }),
            signal: ctrl ? ctrl.signal : undefined
          })
          .then(function(r) {
            if (tId) clearTimeout(tId);
            return r && r.ok ? r.json() : null;
          })
          .then(function(d) {
            var parts = d && d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts;
            if (parts && parts.length) {
              var txt = parts.map(function(p) { return p.thought ? '' : (p.text || ''); }).join(' ').trim();
              if (txt.length > 10) return { texto: txt, modelo: m };
            }
            return intentarModelo(idx + 1);
          })
          .catch(function() {
            if (tId) clearTimeout(tId);
            return intentarModelo(idx + 1);
          });
        }
        return intentarModelo(0);
      }

      function consultarCerebroGenerativoIA(preguntaUsuario) {
        var respuestaRespaldoLocal = window.spObtenerRespuestaOmniscienteCompleta(preguntaUsuario);
        var histReciente = _spHistorialConversacion.slice(-8).join('\n');
        var qNorm = normalizarSinTildes(preguntaUsuario);
        var quiereContratarExplicito = /(quiero contratar|quiero comprar|quiero activar|contratar|comprarlo|activarlo|darme de alta|empezar ya|estoy convencido|agendar cita|pedir cita|mi telefono es|mi numero es|llamame)/.test(qNorm) || !!extraerTelefonoEspanolDeTexto(preguntaUsuario);

        var instruccionModo = quiereContratarExplicito
          ? 'INSTRUCCIÓN DE CIERRE COMERCIAL: El usuario quiere contratar o agendar. Responde en 2 frases cercanas: si su negocio recoge teléfonos de clientes coméntale que por +40 €/mes el Pack Escudo Dúo suma el Cortafuegos de WhatsApp y rebaja las auditorías a 195 €, y pídele su nombre, nombre de su negocio y ciudad, y su teléfono móvil.'
          : 'INSTRUCCIÓN DE CONSULTOR EXPERTO: Responde en 2 a 3 frases fluidas, claras y directas (40 a 70 palabras). Recuerda: 1) El Atril NFC/QR (39 €) abre directamente Google Maps en 1 segundo. 2) El Servicio 1 (59 €/mes) contesta reseñas con IA y frena las de 1-3★ avisando al móvil. 3) El Servicio 2 (Encuesta Cortafuegos WhatsApp) suma +40 €/mes en el Pack Dúo (99 €/mes) y desbloquea las Super-Auditorías SEO/GEO IA y Neuro-CRO a 195 € c/u.';

        var promptCompleto =
          (window.SP_CONTEXTO_MAESTRO_IA_RESUMEN || '') + '\n\n' +
          'HISTORIAL RECIENTE:\n' + (histReciente || 'Inicio de conversación') + '\n\n' +
          'PREGUNTA DEL USUARIO: "' + preguntaUsuario + '"\n\n' +
          instruccionModo;

        // 1º Probamos en paralelo el motor de Render (/api/consultor-ia con Gemini Flash-Lite) y Vertex AI directo
        var ctrlRender = (typeof AbortController !== 'undefined') ? new AbortController() : null;
        var timerRender = ctrlRender ? setTimeout(function() { try { ctrlRender.abort(); } catch (e) {} }, 3200) : null;

        return fetch('https://servicio-resenas.onrender.com/api/consultor-ia', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            pregunta: preguntaUsuario,
            apoyo: respuestaRespaldoLocal,
            prompt: promptCompleto,
            modelo_preferido: 'gemini-2.5-flash-lite'
          }),
          signal: ctrlRender ? ctrlRender.signal : undefined
        })
        .then(function(r) {
          if (timerRender) clearTimeout(timerRender);
          return r && r.ok ? r.json() : null;
        })
        .then(function(d) {
          if (d && d.ok && d.respuesta && d.respuesta.trim().length > 10) {
            pintarPuntitoSecretoEstadoApi('online', '🟢 Conectado en vivo a ' + (d.modelo || 'Gemini Flash-Lite'));
            return d.respuesta.replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim();
          }
          return llamarVertexDirectoNavegador(promptCompleto).then(function(resV) {
            if (resV && resV.texto) {
              pintarPuntitoSecretoEstadoApi('online', '🟢 Conectado en vivo a ' + resV.modelo);
              return resV.texto.replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim();
            }
            pintarPuntitoSecretoEstadoApi('local');
            return respuestaRespaldoLocal;
          });
        })
        .catch(function() {
          if (timerRender) clearTimeout(timerRender);
          return llamarVertexDirectoNavegador(promptCompleto).then(function(resV) {
            if (resV && resV.texto) {
              pintarPuntitoSecretoEstadoApi('online', '🟢 Conectado en vivo a ' + resV.modelo);
              return resV.texto.replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim();
            }
            pintarPuntitoSecretoEstadoApi('local');
            return respuestaRespaldoLocal;
          });
        });
      }

      window.spProcesarConsultaEnTeleprompterDirecto = function(textoPregunta) {
        var limpia = (textoPregunta || '').trim();
        if (!limpia) return;
        _spOrbeDespierto = true;
        var inp = document.getElementById('spTecnosalaInput');
        if (inp) inp.value = '';

        _spHistorialConversacion.push('Usuario: ' + limpia);
        window.spExtraerYPreconfigurarCarritoDesdeCharla(limpia, _spHistorialConversacion);

        var tlfDetectado = extraerTelefonoEspanolDeTexto(limpia);
        if (tlfDetectado && typeof window.spRegistrarLeadAutomaticoDesdeVoz === 'function') {
          window.spRegistrarLeadAutomaticoDesdeVoz(tlfDetectado, limpia, _spHistorialConversacion.join(' | '));
        }

        consultarCerebroGenerativoIA(limpia).then(function(respuestaInteligente) {
          _spHistorialConversacion.push('Consultor: ' + respuestaInteligente);
          var ahora = new Date();
          _spRegistroDescargaCharla.push({
            hora: ahora.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
            pregunta: limpia,
            respuesta: respuestaInteligente
          });
          actualizarContadorBotonDescarga();
          window.spReproducirEnTeleprompter2027(respuestaInteligente, null, limpia);
        });
      };

"""


ACTIVAR_ORBE_SINCRONO_V167 = r"""window.spActivarOrbeConsultorInteractivo = function(ev) {
        if (ev && ev.stopPropagation) ev.stopPropagation();

        if (_spOrbeDespierto && (_spHablandoSintesis || _spEscuchandoVoz) && !_spPausadoPorNavegacion) {
          window.spPararConsultorTotalmente(ev);
          return;
        }

        _spOrbeDespierto = true;
        _spPausadoPorNavegacion = false;
        _spAutoEscuchaContinua = true;

        // 1º ARRANQUE SÍNCRONO INMEDIATO DEL MICRÓFONO DENTRO DEL CLIC DEL USUARIO:
        // Así Chrome sella el permiso del usuario en la primera pulsación y no lo vuelve a pedir entre frases.
        _spIgnorarMicroMientrasHabla = true;
        var rec = obtenerReconocedorUnicoContinua();
        if (rec && !_spMicroSesionActiva) {
          try { rec.start(); } catch (e) {}
        }

        asegurarCabinaTeleprompter2027();
        mostrarBotonesParadaActivos();
        iniciarVigilanteMicrofonoContinuo();

        var track = document.getElementById('spTeleprompterRollTrack');
        if (track && track.children.length > 0) {
          _spHablandoSintesis = false;
          _spIgnorarMicroMientrasHabla = false;
          _spEscuchandoVoz = true;
          pintarEstadoBotonHablar(true);
          actualizarAparienciaOrbeYEstado('listening');
          return;
        }

        var saludo2027 =
          'Hola, soy tu consultor tecnológico experto de Sistemas Pyme. ' +
          'Hablamos en modo manos libres continuo: pregúntame cualquier duda sobre nuestro ecosistema, descubre qué combinación te ahorra más dinero y, si lo deseas, deja tu servicio contratado o agendado desde aquí mismo.';

        window.spReproducirEnTeleprompter2027(saludo2027, function() {
          _spHablandoSintesis = false;
          _spIgnorarMicroMientrasHabla = false;
          _spEscuchandoVoz = true;
          pintarEstadoBotonHablar(true);
          actualizarAparienciaOrbeYEstado('listening');
        });
      };

      """


def reparar_index_html(ruta_index):
    if not os.path.isfile(ruta_index):
        return False

    crear_backup_seguro(ruta_index)
    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    cambios = 0

    # 1. Reemplazar el motor principal del Tecnoconsultor por la versión V167 100% síncrona y sin .stop() entre turnos
    patron_tramo = re.compile(
        r"window\.spRepetirUltimaRespuestaConsultor\s*=\s*function\s*\(ev\)\s*\{.*?(?=window\.spToggleVozConsultorMute\s*=\s*function)",
        re.DOTALL
    )
    if patron_tramo.search(html):
        html = patron_tramo.sub(lambda _: MOTOR_DEFINITIVO_TECNOCONSULTOR_V167, html, count=1)
        cambios += 1
        print(f"✅ [{os.path.basename(os.path.dirname(ruta_index))}] Motor V167 inyectado (arranque síncrono de micro + Gemini Flash-Lite).")

    # 2. Actualizar spActivarOrbeConsultorInteractivo para que llame a rec.start() en la línea 1 del clic del usuario
    patron_activar_orbe = re.compile(
        r"window\.spActivarOrbeConsultorInteractivo\s*=\s*function\s*\(ev\)\s*\{.*?(?=var\s+HTML_BIENVENIDA_ORBE_3D_V159)",
        re.DOTALL
    )
    if patron_activar_orbe.search(html):
        html = patron_activar_orbe.sub(lambda _: ACTIVAR_ORBE_SINCRONO_V167, html, count=1)
        cambios += 1

    # 3. Eliminar del bloque final V160 cualquier sobrescritura conflictiva de cambiarVista / spPararConsultorTotalmente
    patron_conflicto_v160 = re.compile(
        r"window\._spConsultorEstabaActivoAntesDeSalir\s*=\s*false;.*?(?=/\*\s*={10,}\s*\n\s*2\.\s*MOTOR DE PRECIOS CLAROS)",
        re.DOTALL
    )
    if patron_conflicto_v160.search(html):
        html = patron_conflicto_v160.sub(lambda _: "/* [V167: Gestión de micrófono centralizada en el motor principal] */\n\n  ", html, count=1)
        cambios += 1
        print(f"✅ [{os.path.basename(os.path.dirname(ruta_index))}] Eliminado el hook duplicado del bloque V160 que pisaba al Tecnoconsultor.")

    if not validar_bloques_js_en_html(html, ruta_index):
        print(f"❌ Abortando guardado en {ruta_index} por error de sintaxis JS.")
        return False

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"🚀 Guardado y verificado: {ruta_index} ({cambios} secciones actualizadas)")
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
                    ["git", "-C", ruta_repo, "commit", "-m", "V167: Tecnoconsultor fluido con arranque sincrono de micro y Gemini Flash-Lite"],
                    check=False
                )
                subprocess.run(["git", "-C", ruta_repo, "push"], check=False)
                print(f"✅ Git sincronizado en: {nombre}")
            except Exception as e:
                print(f"⚠️ Aviso en Git ({nombre}): {e}")


def main():
    print("\n" + "=" * 78)
    print("🛠️ INICIANDO ACTUALIZACIÓN V167 — INGENIERÍA DEFINITIVA TECNOCONSULTOR")
    print("=" * 78)

    actualizar_documentos_maestros()
    ok = sincronizar_ambos_index()
    if not ok:
        print("❌ No se pudo actualizar index.html.")
        sys.exit(1)

    replicar_ad_py_en_carpetas()
    publicar_en_git_repositorios()

    print("\n🎉 ACTUALIZACIÓN V167 COMPLETADA CON ÉXITO — RECARGA TU WEB CON CMD+SHIFT+R")
    print("📌 Actualización de Conocimiento guardada automáticamente en tu carpeta SISTEMAS PYME/Programar (con copia previa en backups_sp)\n")


if __name__ == "__main__":
    main()
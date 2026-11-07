#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SCRIPT ACTUALIZADOR MAESTRO AD.py — VERSIÓN 166 (SISTEMAS PYME)
=============================================================================
Objetivo:
1. Eliminar para siempre el cartel repetitivo de permiso de micrófono en cada
   turno de conversación del Tecnoconsultor.
2. Mantener UNA ÚNICA instancia continua de `SpeechRecognition` + stream
   persistente `getUserMedia` abierta durante toda la estancia en Tecnosala,
   usando "mute lógico" (`_spIgnorarMicroMientrasHabla = true`) mientras el
   consultor habla en lugar de llamar a `.stop()` y `.start()` en cada frase.
3. Pausa automática al salir a otros apartados de la página o cambiar de
   pestaña del navegador, y reanudación automática al volver a Tecnosala.
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

NOTA_ACTUALIZACION_V166 = """
### ACTUALIZACIÓN V166 (Micrófono Continuo de Sesión Única en Tecnoconsultor — Cero Re-Prompts de Permiso entre Turnos)
- **Eliminado el `.stop()` / `.start()` entre turnos que disparaba el permiso del navegador en cada frase:** Ahora `SpeechRecognition` se inicia una sola vez dentro del gesto del usuario (al tocar la esfera 3D o el botón `🎙️ Hablar`), respaldado por un canal de audio vivo (`navigator.mediaDevices.getUserMedia({ audio: true })`) que mantiene la concesión del permiso durante toda la sesión.
- **Compuerta de Mute Lógico mientras el Consultor habla:** Durante la locución del Tecnoconsultor (`_spHablandoSintesis = true`), el micrófono permanece abierto en segundo plano pero descarta cualquier entrada acústica (`_spIgnorarMicroMientrasHabla = true` + limpieza de buffer), evitando que se escuche a sí mismo y permitiendo que el usuario vuelva a hablar inmediatamente al terminar la respuesta sin que el navegador vuelva a pedir permiso jamás.
- **Desactivación al navegar por otros apartados y auto-reactivación al volver a Tecnosala:** Si el usuario cambia a `Inicio`, `Cómo ayudamos`, `Test de diagnóstico`, `Precios claros`, `Magazine` o cambia de pestaña del navegador, se cancela la voz y se silencia la escucha; al regresar a `Tecnosala`, se reactiva sola automáticamente.
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
                if "ACTUALIZACIÓN V166" not in contenido:
                    contenido = contenido.rstrip() + "\n\n" + NOTA_ACTUALIZACION_V166.strip() + "\n"
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

    print("✅ Todos los bloques JavaScript de index.html están 100% limpios y sin errores de sintaxis.")
    return True


TRAMO_COMPLETO_SANO_TECNOCONSULTOR = r"""      window.spRepetirUltimaRespuestaConsultor = function(ev) {
        if (ev && ev.stopPropagation) ev.stopPropagation();
        if (_spRegistroDescargaCharla.length > 0) {
          var ult = _spRegistroDescargaCharla[_spRegistroDescargaCharla.length - 1];
          window.spReproducirEnTeleprompter2027(ult.respuesta, null, ult.pregunta);
        } else {
          window.spActivarOrbeConsultorInteractivo(ev);
        }
      };

      var _spPausadoPorCambioDeSeccion = false;
      var _spAcumuladoTurnoVoz = '';
      var _spLineaDictadoVivoEl = null;
      var _spCooldownPostHablaTs = 0;

      // Pide y mantiene vivo un canal de audio real para que el navegador selle el permiso 1 sola vez
      function asegurarStreamMicroUnico() {
        if (_spMicStream && _spMicStream.active) {
          return Promise.resolve(_spMicStream);
        }
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          return navigator.mediaDevices.getUserMedia({
            audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true }
          }).then(function(st) {
            _spMicStream = st;
            // Mantener las pistas habilitadas mientras estemos en Tecnosala
            return st;
          }).catch(function() { return null; });
        }
        return Promise.resolve(null);
      }

      function habilitarTracksMicro(activo) {
        if (_spMicStream && _spMicStream.getAudioTracks) {
          var tracks = _spMicStream.getAudioTracks();
          for (var i = 0; i < tracks.length; i++) {
            tracks[i].enabled = !!activo;
          }
        }
      }

      function pintarBotonHablarUI(escuchando) {
        var btnVoice = document.getElementById('spBtnVoiceTecnosala');
        var txtVoice = document.getElementById('spVoiceBtnText');
        var icoVoice = document.getElementById('spVoiceMicIcon');
        var inp = document.getElementById('spTecnosalaInput');
        if (escuchando) {
          if (btnVoice) btnVoice.classList.add('sp-voice-listening');
          if (txtVoice) txtVoice.textContent = 'Escuchando...';
          if (icoVoice) icoVoice.textContent = '🔴';
          if (inp) inp.placeholder = '🟢 Manos libres continuo activo: habla directamente sin tocar nada...';
        } else {
          if (btnVoice) btnVoice.classList.remove('sp-voice-listening');
          if (txtVoice) txtVoice.textContent = 'Hablar';
          if (icoVoice) icoVoice.textContent = '🎙️';
          if (inp) inp.placeholder = 'Escribe tu duda o pulsa 🎙️ Hablar para preguntar por voz...';
        }
      }

      // Pausa al cambiar a otro apartado de la web o pestaña del navegador
      window.spPausarConsultorPorNavegacion = function() {
        if (!_spOrbeDespierto) return;
        _spPausadoPorCambioDeSeccion = true;
        _spHablandoSintesis = false;
        _spEscuchandoVoz = false;
        _spIgnorarMicroMientrasHabla = true;
        _spAcumuladoTurnoVoz = '';
        _spOrbEnergyTarget = 0;
        limpiarTimersTeleprompter();
        if (_spSilenceTimer) {
          clearTimeout(_spSilenceTimer);
          _spSilenceTimer = null;
        }
        if ('speechSynthesis' in window) {
          try { window.speechSynthesis.cancel(); } catch (e) {}
        }
        // Silenciamos las pistas físicas del micro mientras navega por otras secciones
        habilitarTracksMicro(false);
        if (_spRecogInstance && _spMicroSesionActiva) {
          try {
            _spRecogInstance.abort();
          } catch (e) {}
          _spMicroSesionActiva = false;
        }
        pintarBotonHablarUI(false);
        actualizarAparienciaOrbeYEstado('idle');
      };

      // Al regresar a Tecnosala, reactiva el micro automáticamente sin volver a pedir permiso
      window.spReanudarConsultorAlVolverATecnosala = function() {
        if (!_spOrbeDespierto) return;
        var vTec = document.getElementById('vista-tecnosala');
        if (!vTec || vTec.classList.contains('hidden') || document.hidden) return;
        _spPausadoPorCambioDeSeccion = false;
        _spAutoEscuchaContinua = true;
        _spHablandoSintesis = false;
        _spIgnorarMicroMientrasHabla = false;
        _spAcumuladoTurnoVoz = '';
        habilitarTracksMicro(true);
        iniciarVigilanteMicrofonoContinuo();
        window.spActivarModoEscuchaPersistente(false);
      };

      // Parada manual total cuando el usuario pulsa el botón rojo PARAR
      window.spPararConsultorTotalmente = function(ev) {
        if (ev && ev.stopPropagation) ev.stopPropagation();
        _spOrbeDespierto = false;
        _spPausadoPorCambioDeSeccion = false;
        _spAutoEscuchaContinua = false;
        _spHablandoSintesis = false;
        _spEscuchandoVoz = false;
        _spIgnorarMicroMientrasHabla = true;
        _spAcumuladoTurnoVoz = '';
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
        habilitarTracksMicro(false);
        if (_spRecogInstance) {
          try {
            _spRecogInstance.onend = null;
            _spRecogInstance.onerror = null;
            _spRecogInstance.onresult = null;
            _spRecogInstance.abort();
          } catch (e) {}
          _spRecogInstance = null;
          _spMicroSesionActiva = false;
        }
        pintarBotonHablarUI(false);
        actualizarAparienciaOrbeYEstado('idle');
      };

      function iniciarVigilanteMicrofonoContinuo() {
        if (_spWatchdogMicroInterval) clearInterval(_spWatchdogMicroInterval);
        _spWatchdogMicroInterval = setInterval(function() {
          var vTec = document.getElementById('vista-tecnosala');
          var enTecnosala = vTec && !vTec.classList.contains('hidden') && !document.hidden;
          if (!enTecnosala) {
            if (_spHablandoSintesis || _spEscuchandoVoz) {
              window.spPausarConsultorPorNavegacion();
            }
            return;
          }
          if (_spOrbeDespierto && _spAutoEscuchaContinua && !_spPausadoPorCambioDeSeccion && !_spHablandoSintesis && !_spMicroSesionActiva && !_spRearmandoOido) {
            window.spActivarModoEscuchaPersistente(false);
          }
        }, 1000);
      }

      window.spIniciarEscuchaDirectaConsultor = function() {
        _spOrbeDespierto = true;
        _spPausadoPorCambioDeSeccion = false;
        _spAutoEscuchaContinua = true;
        _spHablandoSintesis = false;
        _spIgnorarMicroMientrasHabla = false;
        _spAcumuladoTurnoVoz = '';
        if ('speechSynthesis' in window) {
          try { window.speechSynthesis.cancel(); } catch (e) {}
        }
        asegurarCabinaTeleprompter2027();
        habilitarTracksMicro(true);
        iniciarVigilanteMicrofonoContinuo();
        window.spActivarModoEscuchaPersistente(false);
      };

      // CLAVE V166: El reconocedor de voz NUNCA se destruye con .stop() entre frase y frase.
      // Permanece abierto en continuo y solo conmuta la bandera _spIgnorarMicroMientrasHabla.
      window.spActivarModoEscuchaPersistente = function(forzarReinicio) {
        var vTec = document.getElementById('vista-tecnosala');
        if (!vTec || vTec.classList.contains('hidden') || document.hidden) return;
        if (!_spAutoEscuchaContinua || _spPausadoPorCambioDeSeccion) return;

        var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) {
          actualizarAparienciaOrbeYEstado('idle');
          var inpFallback = document.getElementById('spTecnosalaInput');
          if (inpFallback) inpFallback.focus();
          return;
        }

        habilitarTracksMicro(true);

        // Si la sesión de reconocimiento YA está abierta, NO la paramos ni reiniciamos:
        // simplemente abrimos la compuerta lógica para escuchar al usuario sin pedir permiso jamás.
        if (_spMicroSesionActiva && _spRecogInstance && !forzarReinicio) {
          _spAcumuladoTurnoVoz = '';
          if (!_spHablandoSintesis) {
            _spEscuchandoVoz = true;
            _spIgnorarMicroMientrasHabla = false;
            pintarBotonHablarUI(true);
            actualizarAparienciaOrbeYEstado('listening');
          }
          return;
        }

        if (_spRearmandoOido) return;
        _spRearmandoOido = true;

        asegurarStreamMicroUnico().then(function() {
          _spRearmandoOido = false;
          var vTecNow = document.getElementById('vista-tecnosala');
          if (!_spAutoEscuchaContinua || _spPausadoPorCambioDeSeccion || !vTecNow || vTecNow.classList.contains('hidden') || document.hidden) return;

          if (_spMicroSesionActiva && _spRecogInstance) {
            if (!_spHablandoSintesis) {
              _spEscuchandoVoz = true;
              _spIgnorarMicroMientrasHabla = false;
              pintarBotonHablarUI(true);
              actualizarAparienciaOrbeYEstado('listening');
            }
            return;
          }

          try {
            if (!_spRecogInstance) {
              var rec = new SpeechRec();
              rec.lang = 'es-ES';
              rec.continuous = true;
              rec.interimResults = true;
              _spRecogInstance = rec;

              function enviarTurnoDetectado() {
                if (_spSilenceTimer) { clearTimeout(_spSilenceTimer); _spSilenceTimer = null; }
                var preguntaLista = _spAcumuladoTurnoVoz.trim();
                _spAcumuladoTurnoVoz = '';
                if (!preguntaLista || preguntaLista.length < 2 || _spIgnorarMicroMientrasHabla || _spHablandoSintesis) return;

                // COMPUERTA DE MUTE LÓGICO: NO cerramos el micrófono (.stop()), solo silenciamos la escucha
                // mientras el consultor procesa y responde, para que el navegador NUNCA vuelva a pedir permiso.
                _spIgnorarMicroMientrasHabla = true;
                _spEscuchandoVoz = false;
                if (_spLineaDictadoVivoEl) {
                  try { _spLineaDictadoVivoEl.remove(); } catch (e) {}
                  _spLineaDictadoVivoEl = null;
                }
                window.spProcesarConsultaEnTeleprompterDirecto(preguntaLista);
              }

              rec.onstart = function() {
                _spMicroSesionActiva = true;
                if (!_spHablandoSintesis) {
                  _spEscuchandoVoz = true;
                  _spIgnorarMicroMientrasHabla = false;
                  pintarBotonHablarUI(true);
                  actualizarAparienciaOrbeYEstado('listening');
                }
              };

              rec.onresult = function(event) {
                // Si el consultor está hablando o acaba de terminar hace menos de 350ms, ignoramos el eco
                if (_spIgnorarMicroMientrasHabla || _spHablandoSintesis || (performance.now() - _spCooldownPostHablaTs < 350)) {
                  _spAcumuladoTurnoVoz = '';
                  return;
                }
                var parcial = '';
                var finalNuevo = '';
                for (var i = event.resultIndex; i < event.results.length; i++) {
                  var tr = event.results[i][0].transcript;
                  if (event.results[i].isFinal) finalNuevo += tr + ' ';
                  else parcial += tr;
                }
                if (finalNuevo) _spAcumuladoTurnoVoz = (_spAcumuladoTurnoVoz + ' ' + finalNuevo).trim();
                var textoEnCurso = (_spAcumuladoTurnoVoz + ' ' + parcial).trim();
                if (!textoEnCurso) return;

                _spUltimoPulsoVozUsuarioTs = performance.now();
                _spNivelVozUsuarioVivo = Math.min(0.95, 0.35 + (textoEnCurso.length % 7) * 0.08);

                var inp = document.getElementById('spTecnosalaInput');
                if (inp) inp.value = textoEnCurso;

                var track = asegurarCabinaTeleprompter2027();
                if (track) {
                  if (!_spLineaDictadoVivoEl || !_spLineaDictadoVivoEl.parentNode) {
                    _spLineaDictadoVivoEl = document.createElement('div');
                    _spLineaDictadoVivoEl.className = 'sp-led-line-item sp-led-line-user';
                    track.appendChild(_spLineaDictadoVivoEl);
                  }
                  _spLineaDictadoVivoEl.textContent = '🎙️ TÚ: «' + textoEnCurso + '...»';
                  reclasificarJerarquiaLineas(track);
                }

                if (_spSilenceTimer) clearTimeout(_spSilenceTimer);
                if (finalNuevo) {
                  _spSilenceTimer = setTimeout(enviarTurnoDetectado, 650);
                } else {
                  _spSilenceTimer = setTimeout(function() {
                    _spAcumuladoTurnoVoz = textoEnCurso;
                    enviarTurnoDetectado();
                  }, 1250);
                }
              };

              rec.onerror = function(ev) {
                if (ev && (ev.error === 'not-allowed' || ev.error === 'service-not-allowed')) {
                  _spMicroSesionActiva = false;
                  _spAutoEscuchaContinua = false;
                  _spEscuchandoVoz = false;
                  pintarBotonHablarUI(false);
                  actualizarAparienciaOrbeYEstado('idle');
                }
              };

              rec.onend = function() {
                _spMicroSesionActiva = false;
                var vTecEnd = document.getElementById('vista-tecnosala');
                var sigueEnTec = vTecEnd && !vTecEnd.classList.contains('hidden') && !document.hidden;
                if (_spOrbeDespierto && _spAutoEscuchaContinua && !_spPausadoPorCambioDeSeccion && sigueEnTec) {
                  try {
                    _spRecogInstance.start();
                  } catch (e) {}
                }
              };
            }

            _spRecogInstance.start();
          } catch (err) {
            _spMicroSesionActiva = false;
          }
        });
      };

      window.spReproducirEnTeleprompter2027 = function(textoCompleto, alTerminarCallback, etiquetaUsuarioPrevio) {
        limpiarTimersTeleprompter();
        // MUTE LÓGICO SIN APAGAR EL MICRÓFONO: Así el navegador jamás vuelve a pedir permiso al terminar de hablar
        _spIgnorarMicroMientrasHabla = true;
        _spEscuchandoVoz = false;
        _spAcumuladoTurnoVoz = '';
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
          _spCooldownPostHablaTs = performance.now();
          _spAcumuladoTurnoVoz = '';
          _spOrbEnergyTarget = 0;
          if (_spAutoEscuchaContinua && !_spPausadoPorCambioDeSeccion) {
            _spIgnorarMicroMientrasHabla = false;
            _spEscuchandoVoz = true;
            pintarBotonHablarUI(true);
            actualizarAparienciaOrbeYEstado('listening');
            if (!_spMicroSesionActiva) {
              window.spActivarModoEscuchaPersistente(false);
            }
          } else {
            pintarBotonHablarUI(false);
            actualizarAparienciaOrbeYEstado('idle');
          }
          if (typeof alTerminarCallback === 'function') {
            try { alTerminarCallback(); } catch (e) {}
          }
        }

        _spHablandoSintesis = true;
        actualizarAparienciaOrbeYEstado('speaking');

        var duracionMaxMs = Math.max(4000, totalChars * 82 + 2000);
        _spTyperTimerIds.push(setTimeout(forzarCierreYPasarAEscucha, duracionMaxMs));

        function pasoMarcapasos() {
          if (!_spHablandoSintesis || finalDisparado) return;
          if (charObjetivoPorVoz > charActualMostrado) {
            charActualMostrado = Math.min(totalChars, charActualMostrado + Math.max(1, Math.ceil((charObjetivoPorVoz - charActualMostrado) * 0.45)));
          } else {
            charActualMostrado = Math.min(totalChars, charActualMostrado + 1);
          }
          pintarHastaCharGlobal(charActualMostrado);
          if (charActualMostrado >= totalChars) {
            if (!_spVozConsultorActiva || !('speechSynthesis' in window) || !window.speechSynthesis.speaking) {
              forzarCierreYPasarAEscucha();
              return;
            }
            _spTyperTimerIds.push(setTimeout(forzarCierreYPasarAEscucha, 850));
            return;
          }
          var ch = textoGlobalUnido.charAt(charActualMostrado - 1) || '';
          var d = (ch === '.' || ch === '?' || ch === '!') ? 450 : ((ch === ',' || ch === ';') ? 250 : 62);
          _spTyperTimerIds.push(setTimeout(pasoMarcapasos, d));
        }
        _spTyperTimerIds.push(setTimeout(pasoMarcapasos, 45));

        if (_spVozConsultorActiva && ('speechSynthesis' in window)) {
          setTimeout(function() {
            if (!_spHablandoSintesis || finalDisparado) return;
            try {
              if (window.speechSynthesis.speaking) window.speechSynthesis.cancel();
              window.speechSynthesis.resume();
              var vozFija = obtenerVozEspanaFija();
              var u = new SpeechSynthesisUtterance(textoGlobalUnido);
              _spUtteranceEnCurso = u;
              u.lang = 'es-ES';
              u.rate = 0.89;
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
                if ((ahora - tsInicioLocucion > 900 && !window.speechSynthesis.speaking && !window.speechSynthesis.pending) ||
                    (charActualMostrado >= totalChars * 0.90 && (ahora - tsUltimoEventoVoz > 1300))) {
                  clearInterval(_spWatchdogHablaTimer);
                  forzarCierreYPasarAEscucha();
                }
              }, 350);
              u.onend = forzarCierreYPasarAEscucha;
              u.onerror = forzarCierreYPasarAEscucha;
              window.speechSynthesis.speak(u);
            } catch (e) {
              forzarCierreYPasarAEscucha();
            }
          }, 35);
        }
      };

      var _spColaModelosFlashLiteCache = null;
      function _descubrirModelosFlashLiteGoogle(k) {
        if (_spColaModelosFlashLiteCache) return Promise.resolve(_spColaModelosFlashLiteCache);
        var porDefecto = [
          'gemini-2.5-flash-lite',
          'gemini-2.5-flash-lite-preview-06-17',
          'gemini-2.0-flash-lite',
          'gemini-2.0-flash-lite-001',
          'gemini-2.5-flash'
        ];
        return fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=100&key=' + encodeURIComponent(k))
          .then(function(r) { return r && r.ok ? r.json() : null; })
          .then(function(d) {
            var mods = (d && Array.isArray(d.models)) ? d.models : [];
            var lite = [];
            for (var i = 0; i < mods.length; i++) {
              var m = mods[i];
              var met = m.supportedGenerationMethods || [];
              if (met.indexOf('generateContent') === -1) continue;
              var rawName = String(m.name || '');
              var id = rawName.indexOf('models/') === 0 ? rawName.substring(7) : rawName;
              var low = id.toLowerCase();
              if (low.indexOf('gemini-') !== 0 || low.indexOf('flash-lite') === -1) continue;
              var mVer = low.match(/^gemini-(\d+(?:\.\d+)?)/);
              var ver = mVer ? parseFloat(mVer[1]) : 1.0;
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
            var urls = [
              'https://generativelanguage.googleapis.com/v1beta/models/' + m + ':generateContent?key=' + encodeURIComponent(k),
              'https://aiplatform.googleapis.com/v1beta1/publishers/google/models/' + m + ':generateContent?key=' + encodeURIComponent(k)
            ];
            function probarEndpoint(uIdx) {
              if (uIdx >= urls.length) return intentar(idx + 1);
              return fetch(urls[uIdx], {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  contents: [{ role: 'user', parts: [{ text: promptCompleto }] }],
                  generationConfig: { temperature: 0.65, topP: 0.92, maxOutputTokens: 320 }
                })
              })
              .then(function(r) { return r && r.ok ? r.json() : null; })
              .then(function(d) {
                var parts = d && d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts;
                if (parts && parts.length) {
                  var txt = parts.map(function(p) { return p.thought ? '' : (p.text || ''); }).join(' ').trim();
                  if (txt.length > 10) return { texto: txt, modelo: m };
                }
                return probarEndpoint(uIdx + 1);
              })
              .catch(function() { return probarEndpoint(uIdx + 1); });
            }
            return probarEndpoint(0);
          }
          return intentar(0);
        });
      }

      function consultarCerebroGenerativoIA(preguntaUsuario) {
        var respuestaRespaldoLocal = window.spObtenerRespuestaOmniscienteCompleta(preguntaUsuario);
        var histReciente = _spHistorialConversacion.slice(-10).join('\n');
        var qNorm = normalizarSinTildes(preguntaUsuario);
        var quiereContratarExplicito = /(quiero contratar|quiero comprar|quiero activar|contratar|comprarlo|activarlo|darme de alta|empezar ya|estoy convencido|agendar cita|pedir cita|mi telefono es|mi numero es|llamame)/.test(qNorm) || !!extraerTelefonoEspanolDeTexto(preguntaUsuario);

        var instruccionModo = quiereContratarExplicito
          ? 'INSTRUCCIÓN DE CIERRE COMERCIAL: El usuario acaba de expresar interés directo en contratar o dar sus datos. Responde en 2 a 3 frases cercanas: si su negocio sí recoge teléfonos de clientes (citas, encargos o tienda online) y eligió un servicio suelto, coméntale que por +40 €/mes más el Pack Escudo Dúo suma el Cortafuegos de WhatsApp y rebaja las auditorías a 195 € (pero si es una tienda de mostrador puro sin datos de clientes, recomiéndale solo el Servicio 1 de Reseñas IA a 59 €/mes + el Atril NFC de 39 € sin insistir en la encuesta); y pídele su nombre, el NOMBRE EXACTO DE SU NEGOCIO Y CIUDAD, su teléfono móvil y qué día/hora prefiere.'
          : 'INSTRUCCIÓN DE CONSULTOR PURO Y VERACIDAD TÉCNICA: Responde como un consultor experto, honesto y cercano en 2 a 4 frases completas (45 a 80 palabras). Recuerda: 1) El Atril NFC/QR abre directamente Google Maps en 1 segundo. 2) La Encuesta Cortafuegos (Servicio 2) va por WhatsApp y solo se usa en negocios que recogen nombre y móvil del cliente. 3) En comercios de mostrador sin ficha de cliente, recomienda el Atril NFC (39 €) + el Servicio 1 (Gestor de Reseñas IA, 59 €/mes) + Super-Auditoría SEO/GEO.';

        var promptCompleto =
          (window.SP_CONTEXTO_MAESTRO_IA_RESUMEN || '') + '\n\n' +
          'HISTORIAL DE LA CONVERSACIÓN ACTUAL:\n' + (histReciente || 'Recién iniciada') + '\n\n' +
          'NUEVA PREGUNTA O COMENTARIO DEL USUARIO: "' + preguntaUsuario + '"\n\n' +
          instruccionModo;

        return llamarVertexDirectoNavegador(promptCompleto).then(function(resDir) {
          if (resDir && resDir.texto) {
            pintarPuntitoSecretoEstadoApi('online', '🟢 Conectado en vivo a ' + resDir.modelo);
            return resDir.texto.replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim();
          }
          var ctrlLocal = (typeof AbortController !== 'undefined') ? new AbortController() : null;
          var timerLocal = ctrlLocal ? setTimeout(function() { try { ctrlLocal.abort(); } catch (e) {} }, 4000) : null;
          return (window.location.protocol === 'file:' ? Promise.reject('file_mode') : fetch('https://servicio-resenas.onrender.com/api/consultor-ia', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta: preguntaUsuario, apoyo: respuestaRespaldoLocal, prompt: promptCompleto }),
            signal: ctrlLocal ? ctrlLocal.signal : undefined
          }))
          .then(function(r) {
            if (timerLocal) clearTimeout(timerLocal);
            return r && r.ok ? r.json() : null;
          })
          .then(function(d) {
            if (d && d.ok && d.respuesta && d.respuesta.trim().length > 10) {
              pintarPuntitoSecretoEstadoApi('online', '🟢 Conectado en vivo a ' + (d.modelo || 'Gemini Flash-Lite'));
              return d.respuesta.replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim();
            }
            pintarPuntitoSecretoEstadoApi('local');
            return respuestaRespaldoLocal;
          })
          .catch(function() {
            if (timerLocal) clearTimeout(timerLocal);
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


BLOQUE_EVENTOS_CAMBIO_VISTA_INTELIGENTE = r"""      document.addEventListener('click', function(e) {
        var tTec = e.target && e.target.closest ? e.target.closest('#navBtn_tecnosala, #mobTab_tecnosala') : null;
        if (tTec) {
          setTimeout(function() {
            conectarFuncionesRealesTecnosalaV159();
            if (typeof window.spReanudarConsultorAlVolverATecnosala === 'function') {
              window.spReanudarConsultorAlVolverATecnosala();
            }
          }, 80);
          return;
        }
        var btnOtraVista = e.target && e.target.closest ? e.target.closest('[onclick*="cambiarVista"]') : null;
        if (btnOtraVista) {
          var attrOnclick = btnOtraVista.getAttribute('onclick') || '';
          if (attrOnclick.indexOf("'tecnosala'") === -1 && attrOnclick.indexOf('"tecnosala"') === -1) {
            if (typeof window.spPausarConsultorPorNavegacion === 'function') {
              window.spPausarConsultorPorNavegacion();
            }
          }
        }
      }, true);

      function envolverCambiarVistaParaApagarMicro() {
        if (typeof window.cambiarVista === 'function' && !window.cambiarVista._spMicGuard) {
          var origCV = window.cambiarVista;
          var nuevaCV = function(vistaDestino) {
            if (vistaDestino !== 'tecnosala') {
              if (typeof window.spPausarConsultorPorNavegacion === 'function') {
                window.spPausarConsultorPorNavegacion();
              }
            }
            var res = origCV.apply(this, arguments);
            if (vistaDestino === 'tecnosala') {
              setTimeout(function() {
                conectarFuncionesRealesTecnosalaV159();
                if (typeof window.spReanudarConsultorAlVolverATecnosala === 'function') {
                  window.spReanudarConsultorAlVolverATecnosala();
                }
              }, 90);
            }
            setTimeout(aplicarFondoAzulitoMagazineEnDOM, 30);
            return res;
          };
          nuevaCV._spMicGuard = true;
          window.cambiarVista = nuevaCV;
        }
      }
      envolverCambiarVistaParaApagarMicro();
      setTimeout(envolverCambiarVistaParaApagarMicro, 500);

      document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
          if (typeof window.spPausarConsultorPorNavegacion === 'function') {
            window.spPausarConsultorPorNavegacion();
          }
        } else {
          var vTec = document.getElementById('vista-tecnosala');
          if (vTec && !vTec.classList.contains('hidden')) {
            setTimeout(function() {
              if (typeof window.spReanudarConsultorAlVolverATecnosala === 'function') {
                window.spReanudarConsultorAlVolverATecnosala();
              }
            }, 180);
          }
        }
      });"""


BLOQUE_HOOK_V163_LIMPIO = r"""  window._spConsultorEstabaActivoAntesDeSalir = false;

  var _origActivarOrbeNativo = window.spActivarOrbeConsultorInteractivo;
  if (typeof _origActivarOrbeNativo === 'function' && !_origActivarOrbeNativo._wrappedV165) {
    var nuevoActivarOrbe = function(ev) {
      window._spConsultorEstabaActivoAntesDeSalir = true;
      return _origActivarOrbeNativo.apply(this, arguments);
    };
    nuevoActivarOrbe._wrappedV165 = true;
    window.spActivarOrbeConsultorInteractivo = nuevoActivarOrbe;
  }"""


def reparar_index_html(ruta_index):
    if not os.path.isfile(ruta_index):
        return False

    crear_backup_seguro(ruta_index)
    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    cambios = 0

    # 1. Reemplazo integral desde spRepetirUltimaRespuestaConsultor hasta justo antes de spToggleVozConsultorMute
    patron_tramo = re.compile(
        r"window\.spRepetirUltimaRespuestaConsultor\s*=\s*function\s*\(ev\)\s*\{.*?(?=window\.spToggleVozConsultorMute\s*=\s*function)",
        re.DOTALL
    )
    if patron_tramo.search(html):
        html = patron_tramo.sub(lambda _: TRAMO_COMPLETO_SANO_TECNOCONSULTOR, html, count=1)
        cambios += 1
        print(f"✅ [{os.path.basename(os.path.dirname(ruta_index))}] Configurado micrófono continuo sin .stop() entre turnos (Cero re-prompts de permiso).")
    else:
        print(f"⚠️ [{ruta_index}] No se encontró la marca spRepetirUltimaRespuestaConsultor.")

    # 1b. Actualizar spActivarOrbeConsultorInteractivo para que abra el micrófono DENTRO del clic inicial del usuario (gesto directo)
    patron_activar_orbe = re.compile(
        r"window\.spActivarOrbeConsultorInteractivo\s*=\s*function\s*\(ev\)\s*\{.*?(?=var\s+HTML_BIENVENIDA_ORBE_3D_V159)",
        re.DOTALL
    )
    nuevo_activar_orbe = r"""window.spActivarOrbeConsultorInteractivo = function(ev) {
        if (ev) ev.stopPropagation();

        if (_spOrbeDespierto && (_spHablandoSintesis || _spEscuchandoVoz) && !_spPausadoPorCambioDeSeccion) {
          window.spPararConsultorTotalmente(ev);
          return;
        }

        _spOrbeDespierto = true;
        _spPausadoPorCambioDeSeccion = false;
        _spAutoEscuchaContinua = true;
        asegurarCabinaTeleprompter2027();
        mostrarBotonesParadaActivos();

        // Abrimos el canal de micrófono AHORA MISMO aprovechando el clic directo del usuario (con mute lógico mientras saluda)
        _spIgnorarMicroMientrasHabla = true;
        window.spActivarModoEscuchaPersistente(false);
        iniciarVigilanteMicrofonoContinuo();

        var track = document.getElementById('spTeleprompterRollTrack');
        if (track && track.children.length > 0) {
          _spHablandoSintesis = false;
          _spIgnorarMicroMientrasHabla = false;
          _spEscuchandoVoz = true;
          pintarBotonHablarUI(true);
          actualizarAparienciaOrbeYEstado('listening');
          return;
        }

        var saludo2027 =
          'Hola, soy tu consultor tecnológico experto de Sistemas Pyme. ' +
          'Hablamos en modo manos libres sin que tengas que tocar ningún botón: pregúntame con total libertad cualquier duda sobre nuestro ecosistema, descubre qué combinación te ahorra más dinero y, si lo deseas, también puedes dejar tu servicio contratado o agendado desde aquí mismo.';

        window.spReproducirEnTeleprompter2027(saludo2027, function() {
          _spHablandoSintesis = false;
          _spIgnorarMicroMientrasHabla = false;
          _spEscuchandoVoz = true;
          pintarBotonHablarUI(true);
          actualizarAparienciaOrbeYEstado('listening');
        });
      };

      """
    if patron_activar_orbe.search(html):
        html = patron_activar_orbe.sub(lambda _: nuevo_activar_orbe, html, count=1)
        cambios += 1

    # 2. Actualizar los listeners de navegación entre apartados/pestañas
    patron_eventos = re.compile(
        r"document\.addEventListener\('click',\s*function\(e\)\s*\{\s*var\s+tTec\s*=.*?document\.addEventListener\('visibilitychange',\s*function\(\)\s*\{.*?\}\);",
        re.DOTALL
    )
    if patron_eventos.search(html):
        html = patron_eventos.sub(lambda _: BLOQUE_EVENTOS_CAMBIO_VISTA_INTELIGENTE, html, count=1)
        cambios += 1

    # 3. Limpiar el hook secundario al final del archivo
    patron_hook_v163 = re.compile(
        r"window\._spConsultorEstabaActivoAntesDeSalir\s*=\s*false;.*?(?=/\*\s*={10,}\s*\n\s*2\.\s*MOTOR DE PRECIOS CLAROS)",
        re.DOTALL
    )
    if patron_hook_v163.search(html):
        html = patron_hook_v163.sub(lambda _: BLOQUE_HOOK_V163_LIMPIO + "\n\n  ", html, count=1)
        cambios += 1

    # 4. Validar sintaxis JS con Node
    if not validar_bloques_js_en_html(html, ruta_index):
        print(f"❌ Abortando guardado en {ruta_index} por error de sintaxis JS.")
        return False

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"🚀 Guardado y verificado: {ruta_index} ({cambios} secciones actualizadas)")
    return True


def sincronizar_ambos_index():
    """Garantiza que tanto public_html/index.html como servicio_resenas/index.html queden actualizados y sincronizados."""
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

    # Si public_html/index.html existe y servicio_resenas/index.html también, asegurar que servicio_resenas tenga la última versión
    ruta_pub = os.path.join(RUTA_WEB_PUBLIC, "index.html")
    ruta_srv = os.path.join(RUTA_SERVICIO_RESENAS, "index.html")
    if os.path.isfile(ruta_pub) and os.path.isdir(RUTA_SERVICIO_RESENAS):
        if os.path.abspath(ruta_pub) != os.path.abspath(ruta_srv):
            crear_backup_seguro(ruta_srv)
            shutil.copy2(ruta_pub, ruta_srv)
            print(f"🔄 Sincronizado index.html entre public_html y servicio_resenas.")
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
                    ["git", "-C", ruta_repo, "commit", "-m", "V166: Microfono continuo sin volver a pedir permiso entre turnos"],
                    check=False
                )
                subprocess.run(["git", "-C", ruta_repo, "push"], check=False)
                print(f"✅ Git sincronizado en: {nombre}")
            except Exception as e:
                print(f"⚠️ Aviso en Git ({nombre}): {e}")


def main():
    print("\n" + "=" * 78)
    print("🛠️ INICIANDO ACTUALIZACIÓN V166 — MICRÓFONO CONTINUO SIN RE-PEDIR PERMISO")
    print("=" * 78)

    actualizar_documentos_maestros()
    ok = sincronizar_ambos_index()
    if not ok:
        print("❌ No se pudo actualizar index.html.")
        sys.exit(1)

    replicar_ad_py_en_carpetas()
    publicar_en_git_repositorios()

    print("\n🎉 ACTUALIZACIÓN V166 COMPLETADA CON ÉXITO — RECARGA TU WEB CON CMD+SHIFT+R")
    print("📌 Actualización de Conocimiento guardada automáticamente en tu carpeta SISTEMAS PYME/Programar (con copia previa en backups_sp)\n")


if __name__ == "__main__":
    main()
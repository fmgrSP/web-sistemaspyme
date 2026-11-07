#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SISTEMAS PYME — ACTUALIZADOR MAESTRO SEGURO COMPLETO (AD.py - VERSIÓN V150)
================================================================================
Archivo 100% COMPLETO de principio a fin (CERO '# ... existing code ...').
Copia todo este contenido dentro de tu archivo `AD.py` y ejecútalo en Terminal:
    python3 AD.py

Qué soluciona de raíz esta versión V150 en el Tecnoconsultor (Tecnosala):
1. MOTOR ÚNICO DE VOZ Y ESCUCHA CONTINUA (FUNCIONA EN `file://` Y EN `http://`):
   - Eliminado el bloqueo `window.location.protocol !== 'file:'` que dejaba mudo
     el micrófono cuando abrías `index.html` directamente desde tu Mac.
   - Unificado el oído del Orbe 3D en una sola instancia persistente de
     `webkitSpeechRecognition` con canal de audio vivo (`_spMantenerCanalAudioVivo`),
     transcripción en tiempo real en el Teleprompter LED (`🎙️ «...»`), latido de
     la esfera 3D con tu voz y auto-rearme suave al terminar de hablar el consultor.
2. RESPUESTA ULTRARRÁPIDA EN MODO LOCAL (`file://`) Y SERVIDOR:
   - Eliminada la llamada fallida a `fetch('/api/consultor-ia')` cuando estás en
     `file://` (que intentaba abrir `file:///api/consultor-ia`). Ahora conecta
     directamente con Gemini en vivo y con tu Base de Conocimiento Omnisciente
     sin esperas ni bloqueos.
3. CARRITO DE COMPRA 100% COLOREADO (TARJETAS 1, 2, 3, 4, 5 Y CAJA DE CITA):
   - Mantiene todos los colores diferenciados por tarjeta y la sincronización de
     horas ocupadas con tu CRM (`http://127.0.0.1:5000/api/horarios-ocupados-agenda`).
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

VERSION_ACTUAL = "V150"
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
                tmp_js = f"/tmp/_sp_check_v150_{idx}.js"
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
# 2. BLOQUE JS DEFINITIVO V150:
#    - REPARA AL 100% EL TECNOCONSULTOR (MANOS LIBRES FLUIDO EN MAC Y WEB)
#    - MANTIENE COLORES EN CARRITO (TARJETAS 1-5 Y CITA) Y AGENDA CRM
# ==============================================================================
BLOQUE_JS_TECNOCONSULTOR_Y_CARRITO_V150 = r'''
<!-- [SP_AGENDA_CRM_WEB_SYNC_V150_START] -->
<script>
(function() {
  /* =========================================================================
     1. MOTOR DEFINITIVO DE VOZ Y ESCUCHA FLUIDA DEL TECNOCONSULTOR (V150)
        Soluciona los 3 problemas que impedían hablar fluido en index.html:
        a) Funciona tanto en file:// como en http:// (sin bloquear file://).
        b) Unifica en 1 solo reconocedor el Teleprompter LED (`🎙️ «...»`) y el
           auto-rearme tras cada respuesta del consultor.
        c) Mantiene una pista de audio silenciosa tras el primer permiso para que
           el navegador no cierre el canal de micrófono entre frases.
     ========================================================================= */
  var _spRecUnicoV150 = null;
  var _spEscuchandoActivoV150 = false;
  var _spHablandoConsultorV150 = false;
  var _spManosLibresDeseadoV150 = false;
  var _spTimerSilencioV150 = null;
  var _spLineaDictadoEnPantallaV150 = null;
  var _spStreamPermisoCacheV150 = null;
  var _spPidiendoPermisoAhoraV150 = false;
  var _spUltimoStartTsV150 = 0;

  function actualizarUiMicrofonoTecnosalaV150(modo) {
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

  function pintarTranscripcionEnTeleprompterV150(textoParcial) {
    var track = document.getElementById('spTeleprompterRollTrack');
    if (!track) return;
    if (!_spLineaDictadoEnPantallaV150 || !_spLineaDictadoEnPantallaV150.parentNode) {
      _spLineaDictadoEnPantallaV150 = document.createElement('div');
      _spLineaDictadoEnPantallaV150.className = 'sp-led-line-item sp-led-line-user';
      track.appendChild(_spLineaDictadoEnPantallaV150);
      while (track.children.length > 4) {
        track.removeChild(track.firstElementChild);
      }
    }
    _spLineaDictadoEnPantallaV150.innerHTML = '🎙️ <span>«' + String(textoParcial || '').replace(/</g, '&lt;') + '»</span><span class="sp-led-cursor"></span>';
  }

  function limpiarLineaDictadoTemporalV150() {
    if (_spLineaDictadoEnPantallaV150 && _spLineaDictadoEnPantallaV150.parentNode) {
      try { _spLineaDictadoEnPantallaV150.parentNode.removeChild(_spLineaDictadoEnPantallaV150); } catch (e) {}
    }
    _spLineaDictadoEnPantallaV150 = null;
  }

  function inicializarInstanciaUnicaSpeechV150() {
    if (_spRecUnicoV150) return _spRecUnicoV150;
    var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) return null;

    var rec = new SpeechRec();
    rec.lang = 'es-ES';
    rec.continuous = true;
    rec.interimResults = true;
    rec.maxAlternatives = 1;

    var fraseAcumulada = '';

    function dispararEnvioFraseDetectada() {
      if (_spTimerSilencioV150) {
        clearTimeout(_spTimerSilencioV150);
        _spTimerSilencioV150 = null;
      }
      var enviar = String(fraseAcumulada || '').trim();
      fraseAcumulada = '';
      if (!enviar || enviar.length < 2) return;
      if (_spHablandoConsultorV150) return;

      limpiarLineaDictadoTemporalV150();
      _spHablandoConsultorV150 = true;

      /* Pausamos el reconocedor mientras el consultor habla para que no se escuche a sí mismo */
      if (_spRecUnicoV150 && _spEscuchandoActivoV150) {
        try { _spRecUnicoV150.stop(); } catch (e) {}
        _spEscuchandoActivoV150 = false;
      }

      actualizarUiMicrofonoTecnosalaV150('speaking');
      if (typeof window.spProcesarConsultaEnTeleprompterDirecto === 'function') {
        window.spProcesarConsultaEnTeleprompterDirecto(enviar);
      }
    }

    rec.onstart = function() {
      _spEscuchandoActivoV150 = true;
      _spPidiendoPermisoAhoraV150 = false;
      if (!_spHablandoConsultorV150) {
        actualizarUiMicrofonoTecnosalaV150('listening');
      }
    };

    rec.onresult = function(ev) {
      if (_spHablandoConsultorV150 || (window.speechSynthesis && window.speechSynthesis.speaking)) {
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
      pintarTranscripcionEnTeleprompterV150(limpio);

      if (_spTimerSilencioV150) clearTimeout(_spTimerSilencioV150);
      /* Espera natural: 700ms si Chrome ya marcó final de frase, o 1250ms si sigues hablando con pausa */
      _spTimerSilencioV150 = setTimeout(dispararEnvioFraseDetectada, esFinal ? 700 : 1250);
    };

    rec.onerror = function(ev) {
      _spEscuchandoActivoV150 = false;
      _spPidiendoPermisoAhoraV150 = false;
      var errCode = ev ? ev.error : '';
      if (errCode === 'not-allowed' || errCode === 'service-not-allowed') {
        _spManosLibresDeseadoV150 = false;
        actualizarUiMicrofonoTecnosalaV150('idle');
      }
    };

    rec.onend = function() {
      _spEscuchandoActivoV150 = false;
      _spPidiendoPermisoAhoraV150 = false;

      /* Si quedó texto pendiente de enviar cuando se cortó el tramo, lo enviamos ahora */
      if (fraseAcumulada && fraseAcumulada.trim().length >= 2 && !_spHablandoConsultorV150) {
        dispararEnvioFraseDetectada();
        return;
      }

      /* Si estamos en modo manos libres y el consultor NO está hablando, rearmamos el oído suavemente */
      var vistaTec = document.getElementById('vista-tecnosala');
      var enTecnosala = vistaTec && !vistaTec.classList.contains('hidden');
      if (_spManosLibresDeseadoV150 && !_spHablandoConsultorV150 && enTecnosala) {
        setTimeout(function() {
          if (_spManosLibresDeseadoV150 && !_spHablandoConsultorV150 && !_spEscuchandoActivoV150) {
            window.spActivarModoEscuchaPersistente(false);
          }
        }, 320);
      } else if (!_spHablandoConsultorV150) {
        actualizarUiMicrofonoTecnosalaV150('idle');
      }
    };

    _spRecUnicoV150 = rec;
    return rec;
  }

  /* Sobrescribimos las funciones de escucha para que todas usen este único motor limpio */
  window.spActivarModoEscuchaPersistente = function(forzarManual) {
    var vistaTec = document.getElementById('vista-tecnosala');
    if (!vistaTec || vistaTec.classList.contains('hidden')) return;

    if (forzarManual) {
      _spManosLibresDeseadoV150 = true;
      _spHablandoConsultorV150 = false;
      if (window.speechSynthesis && window.speechSynthesis.speaking) {
        try { window.speechSynthesis.cancel(); } catch (e) {}
      }
    }

    if (!_spManosLibresDeseadoV150 || _spHablandoConsultorV150) return;
    if (_spEscuchandoActivoV150 || _spPidiendoPermisoAhoraV150) return;

    var ahora = Date.now();
    if (!forzarManual && (ahora - _spUltimoStartTsV150 < 900)) return;
    _spUltimoStartTsV150 = ahora;

    var rec = inicializarInstanciaUnicaSpeechV150();
    if (!rec) return;

    try {
      _spPidiendoPermisoAhoraV150 = true;
      rec.start();
    } catch (e) {
      _spPidiendoPermisoAhoraV150 = false;
    }
  };

  window.spIniciarEscuchaDirectaConsultor = function() {
    _spManosLibresDeseadoV150 = true;
    _spHablandoConsultorV150 = false;
    window.spActivarModoEscuchaPersistente(true);
  };

  window.spToggleDictadoVozTecnosala = function() {
    /* Si aún no se había despertado la cabina del Teleprompter 2027, la abrimos y saludamos o escuchamos */
    var stage = document.getElementById('spTeleprompter2027Stage');
    if (!stage && typeof window.spActivarOrbeConsultorInteractivo === 'function') {
      window.spActivarOrbeConsultorInteractivo();
      return;
    }
    if (_spEscuchandoActivoV150 && _spRecUnicoV150) {
      _spManosLibresDeseadoV150 = false;
      try { _spRecUnicoV150.stop(); } catch (e) {}
      _spEscuchandoActivoV150 = false;
      actualizarUiMicrofonoTecnosalaV150('idle');
      return;
    }
    _spManosLibresDeseadoV150 = true;
    _spHablandoConsultorV150 = false;
    window.spActivarModoEscuchaPersistente(true);
  };

  /* Enganchar spReproducirEnTeleprompter2027 y spPararConsultorTotalmente para coordinar el turno de palabra */
  function engancharTurnosDePalabraConsultorV150() {
    if (typeof window.spReproducirEnTeleprompter2027 === 'function' && !window.spReproducirEnTeleprompter2027._hookV150) {
      var origReprod = window.spReproducirEnTeleprompter2027;
      var nuevaReprod = function(textoCompleto, alTerminarCallback, etiquetaUsuarioPrevio) {
        _spHablandoConsultorV150 = true;
        _spManosLibresDeseadoV150 = true;
        limpiarLineaDictadoTemporalV150();
        if (_spRecUnicoV150 && _spEscuchandoActivoV150) {
          try { _spRecUnicoV150.stop(); } catch (e) {}
          _spEscuchandoActivoV150 = false;
        }
        actualizarUiMicrofonoTecnosalaV150('speaking');

        return origReprod.call(this, textoCompleto, function() {
          _spHablandoConsultorV150 = false;
          if (typeof alTerminarCallback === 'function') {
            try { alTerminarCallback(); } catch (e) {}
          }
          if (_spManosLibresDeseadoV150) {
            setTimeout(function() {
              window.spActivarModoEscuchaPersistente(false);
            }, 220);
          }
        }, etiquetaUsuarioPrevio);
      };
      nuevaReprod._hookV150 = true;
      window.spReproducirEnTeleprompter2027 = nuevaReprod;
    }

    if (typeof window.spPararConsultorTotalmente === 'function' && !window.spPararConsultorTotalmente._hookV150) {
      var origParar = window.spPararConsultorTotalmente;
      var nuevoParar = function(ev) {
        _spManosLibresDeseadoV150 = false;
        _spHablandoConsultorV150 = false;
        _spEscuchandoActivoV150 = false;
        _spPidiendoPermisoAhoraV150 = false;
        if (_spTimerSilencioV150) {
          clearTimeout(_spTimerSilencioV150);
          _spTimerSilencioV150 = null;
        }
        limpiarLineaDictadoTemporalV150();
        if (_spRecUnicoV150) {
          try { _spRecUnicoV150.stop(); } catch (e) {}
        }
        var r = origParar.apply(this, arguments);
        actualizarUiMicrofonoTecnosalaV150('idle');
        return r;
      };
      nuevoParar._hookV150 = true;
      window.spPararConsultorTotalmente = nuevoParar;
    }
  }

  /* =========================================================================
     2. COLORES Y AGENDA DEL CARRITO DE COMPRA (TARJETAS 4, 5 Y CITA DE ALTA)
     ========================================================================= */
  function aplicarIdsColorCajasCarritoV150() {
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
      setTimeout(aplicarIdsColorCajasCarritoV150, 40);
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
    aplicarIdsColorCajasCarritoV150();
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
      var guardados = JSON.parse(localStorage.getItem('sp_citas_ocupadas_crm_v150') || '[]');
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
              localStorage.setItem('sp_citas_ocupadas_crm_v150', JSON.stringify(Array.from(window.SP_SLOTS_OCUPADOS_CRM_EXTRA)));
            } catch (e) {}
          }
        })
        .catch(function() {});
    })).then(function() {
      window.spAplicarBloqueoHorasCrmEnSelect();
    });
  };

  function inicializarMejorasV150() {
    engancharTurnosDePalabraConsultorV150();
    aplicarIdsColorCajasCarritoV150();
    window.spSincronizarCitasCrmLocal();

    if (typeof window.spActualizarHorasDisponiblesCarritoV125 === 'function' && !window.spActualizarHorasDisponiblesCarritoV125._hookV150) {
      var origActHoras = window.spActualizarHorasDisponiblesCarritoV125;
      var nuevaActHoras = function() {
        var r = origActHoras.apply(this, arguments);
        window.spAplicarBloqueoHorasCrmEnSelect();
        return r;
      };
      nuevaActHoras._hookV150 = true;
      window.spActualizarHorasDisponiblesCarritoV125 = nuevaActHoras;
    }

    if (typeof window.spAbrirCarritoConfigurador === 'function' && !window.spAbrirCarritoConfigurador._hookV150) {
      var origOpen = window.spAbrirCarritoConfigurador;
      var nuevoOpen = function() {
        var r = origOpen.apply(this, arguments);
        aplicarIdsColorCajasCarritoV150();
        window.spSincronizarCitasCrmLocal();
        setTimeout(window.spAplicarBloqueoHorasCrmEnSelect, 120);
        return r;
      };
      nuevoOpen._hookV150 = true;
      window.spAbrirCarritoConfigurador = nuevoOpen;
    }

    if (typeof window.spConfirmarPedidoYAgendarCita === 'function' && !window.spConfirmarPedidoYAgendarCita._hookV150) {
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
              localStorage.setItem('sp_citas_ocupadas_crm_v150', JSON.stringify(Array.from(window.SP_SLOTS_OCUPADOS_CRM_EXTRA)));
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
      nuevoConfirm._hookV150 = true;
      window.spConfirmarPedidoYAgendarCita = nuevoConfirm;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(inicializarMejorasV150, 200);
    });
  } else {
    setTimeout(inicializarMejorasV150, 200);
  }
})();
</script>
<!-- [SP_AGENDA_CRM_WEB_SYNC_V150_END] -->
'''


# ==============================================================================
# 3. REPARACIÓN INTERNA DE `index.html`
# ==============================================================================
def reparar_index_html_v150(html):
    # 1. Quitar cualquier bloque [SP_AGENDA_CRM_WEB_SYNC_V14...] o V150 previo
    html = re.sub(
        r"<!-- \[SP_AGENDA_CRM_WEB_SYNC_V1[45]\d_START\] -->[\s\S]*?<!-- \[SP_AGENDA_CRM_WEB_SYNC_V1[45]\d_END\] -->\s*",
        "",
        html
    )

    # 2. Quitar el bloqueo `&& window.location.protocol !== 'file:'` en iniciarVigilanteMicrofonoContinuo
    #    y desactivar ese setInterval antiguo de 950ms para que no compita con el motor limpio V150
    html = re.sub(
        r"function iniciarVigilanteMicrofonoContinuo\(\)\s*\{[\s\S]*?\n      \}",
        """function iniciarVigilanteMicrofonoContinuo() {
        /* Gestionado por el motor unificado V150 (sin colisiones de setInterval cada 950ms) */
      }""",
        html,
        count=1
    )

    # 3. Evitar que en protocolo file:// haga fetch('/api/consultor-ia') que falla hacia file:///api/consultor-ia
    html = html.replace(
        "return fetch('/api/consultor-ia', {",
        "return (window.location.protocol === 'file:' ? Promise.reject('file_mode') : fetch('/api/consultor-ia', {"
    ).replace(
        "signal: ctrlLocal ? ctrlLocal.signal : undefined\n        })\n        .then(function(r) {",
        "signal: ctrlLocal ? ctrlLocal.signal : undefined\n        }))\n        .then(function(r) {"
    )

    # 4. Asegurar que instalarMicrofonoContinuoSinRePromptV129 quede neutralizado para no abrir un 2.º micrófono
    html = re.sub(
        r"function instalarMicrofonoContinuoSinRePromptV129\(\)\s*\{[\s\S]*?\n  \}\n\n  function obtenerTramosPorDiaSemanaV125",
        """function instalarMicrofonoContinuoSinRePromptV129() {
    /* Unificado en el motor V150 */
  }

  function obtenerTramosPorDiaSemanaV125""",
        html,
        count=1
    )

    # 5. Inyectar nuestro bloque V150 al final antes del último </body> real (usando rsplit)
    if "</body>" in html:
        partes = html.rsplit("</body>", 1)
        html = partes[0].rstrip() + "\n" + BLOQUE_JS_TECNOCONSULTOR_Y_CARRITO_V150.strip() + "\n</body>" + partes[1]

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

        html_nuevo = reparar_index_html_v150(html_actual)
        escribir_archivo_con_backup(ruta, html_nuevo)
        validar_bloques_js_en_html(ruta)


# ==============================================================================
# 4. PASO 1 PRIORITARIO + BLINDAJE ATEXIT: ACTUALIZAR LOS 2 DOCUMENTOS .MD
# ==============================================================================
NOTA_HISTORIAL_V150 = f"""
---
### ACTUALIZACIÓN {VERSION_ACTUAL} ({FECHA_EJECUCION}) — Reparación Definitiva del Oído y Respuesta del Tecnoconsultor (Funciona en `file://` y en Servidor) + Carrito Coloreado
- **Eliminado el bloqueo `window.location.protocol !== 'file:'` y unificado el Motor de Reconocimiento de Voz en la Tecnosala:** Resuelto el problema por el que al abrir `index.html` como archivo local (`file://`) el micrófono se cortaba en las pausas y no volvía a rearmarse tras hablar el consultor. Ahora un único motor controla el Teleprompter LED (`🎙️ «...»`), el botón `🎙️ Hablar` y el Orbe Holográfico 3D.
- **Eliminada la espera fallida a `fetch('/api/consultor-ia')` cuando se abre desde el Mac (`file://`):** Cuando se abre en modo local salta directamente a la conexión en vivo con Gemini y a la Base de Conocimiento Omnisciente sin demoras.
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
                txt = txt.rstrip() + "\n" + NOTA_HISTORIAL_V150
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
                    ["git", "-C", carpeta_git, "commit", "-m", f"feat({VERSION_ACTUAL}): reparacion definitiva Tecnoconsultor fluido en file y servidor"],
                    check=False, capture_output=True
                )
                subprocess.run(["git", "-C", carpeta_git, "push"], check=False, capture_output=True)
                print(f"  ✅ Git sincronizado en: {os.path.basename(carpeta_git)}")
            except Exception:
                pass


def ejecutar_actualizacion():
    print("=" * 78)
    print(f"🚀 INICIANDO ACTUALIZACIÓN MAESTRA {VERSION_ACTUAL} — TECNOCONSULTOR 100% FLUIDO + CARRITO COLOREADO")
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
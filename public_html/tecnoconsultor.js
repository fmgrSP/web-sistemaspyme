/**
 * ============================================================================
 * ARCHIVO INDEPENDIENTE: tecnoconsultor.js (SISTEMAS PYME — V176)
 * ============================================================================
 * Contiene en exclusiva toda la lógica del Consultor Tecnológico Inteligente:
 * 1. Control del Orbe Holográfico 3D y Teleprompter LED.
 * 2. Locución con voz española (en BLANCO en el Teleprompter).
 * 3. Reconocimiento de voz por micrófono (en AMARILLO en tiempo real).
 * 4. Conexión con IA Gemini Flash-Lite y respaldo de Base de Conocimiento.
 * 5. Puente automático hacia el Carrito Configurador de index.html.
 * ============================================================================
 */
(function() {
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
  var _contadorVariantes = {};

  function normalizarSinTildes(str) {
    return String(str || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  }

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
     BÚSQUEDA LOCAL EN LA BASE DE CONOCIMIENTO HUMANA (RESPALDO INSTANTÁNEO)
     ========================================================================= */
  window.spObtenerRespuestaOmniscienteCompleta = function(preguntaRaw) {
    var qNorm = normalizarSinTildes(preguntaRaw);
    var bd = window.SP_BASE_CONOCIMIENTO_HUMANA || [];
    var mejorItem = null;
    var mejorPts = 0;
    for (var i = 0; i < bd.length; i++) {
      var it = bd[i];
      var pts = 0;
      for (var j = 0; j < (it.claves || []).length; j++) {
        var kw = normalizarSinTildes(it.claves[j]);
        if (kw && qNorm.indexOf(kw) !== -1) {
          pts += (kw.split(' ').length >= 2) ? 45 : 15;
        }
      }
      if (pts > mejorPts) {
        mejorPts = pts;
        mejorItem = it;
      }
    }
    if (mejorItem && mejorPts > 0) {
      var piscina = [mejorItem.respuesta].concat(mejorItem.variantes || []);
      var k = mejorItem.id || 'def';
      var idx = (_contadorVariantes[k] || 0) % piscina.length;
      _contadorVariantes[k] = idx + 1;
      return piscina[idx];
    }
    return 'En Sistemas Pyme te ayudamos a multiplicar tus reseñas de 5 estrellas con IA, a posicionar tu web en Google y ChatGPT y a automatizar tu WhatsApp en 24 a 48 horas. Dime qué área de tu negocio quieres mejorar y lo vemos al detalle.';
  };

  /* =========================================================================
     CONTROL DEL MICRÓFONO (SE ABRE CUANDO EL CONSULTOR ACABA DE HABLAR)
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
     LOCUCIÓN EN BLANCO EN EL TELEPROMPTER Y APERTURA AUTOMÁTICA DE MICRO AL FINAL
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
     CONEXIÓN CON IA GEMINI (< 1s) + RESPALDO OMNISCIENTE
     ========================================================================= */
  function obtenerRespuestaInteligente(preguntaUsuario) {
    var apoyo = window.spObtenerRespuestaOmniscienteCompleta(preguntaUsuario);
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
      }, 2200);

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

  /* =========================================================================
     API PÚBLICA CONECTADA A LOS BOTONES DE LA TECNOSALA EN `index.html`
     ========================================================================= */
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

  window.spEjecutarConsultaTecnosala = function(claveFaq) {
    var mapaTitulos = {
      rgpd: '¿Cómo evitáis multas de Protección de Datos en reseñas?',
      fijo: '¿Puedo usar el teléfono fijo de siempre de mi local?',
      informe360: '¿Qué incluye el Informe Mensual 360°?',
      instalacion: '¿Tengo que cambiar el programa que ya uso?',
      seogeo: '¿Cómo lográis que ChatGPT y Google me recomienden?',
      precios: '¿Cuánto cuesta y cómo se amortiza?'
    };
    var preg = mapaTitulos[claveFaq] || claveFaq;
    window.spProcesarConsultaEnTeleprompterDirecto(preg);
  };

  window.spCambiarVozPreferidaConsultor = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (!('speechSynthesis' in window)) return;
    var todas = window.speechSynthesis.getVoices() || [];
    var es = todas.filter(function(v) { return /^es[-_]es/i.test(v.lang || ''); });
    if (!es.length) return;
    var actual = elegirVozEspanola();
    var idx = 0;
    for (var i = 0; i < es.length; i++) {
      if (actual && es[i].name === actual.name) { idx = i; break; }
    }
    var sig = es[(idx + 1) % es.length];
    _vozCache = sig;
    _nombreVoz = String(sig.name || 'Voz').replace(/^Microsoft\s+/i, '').split(/[\s(]/)[0];
    var btn = document.getElementById('spBtnCambiarTimbreVoz');
    if (btn) btn.innerHTML = '🎙️ Voz: ' + _nombreVoz;
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

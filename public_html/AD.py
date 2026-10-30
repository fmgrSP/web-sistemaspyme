import os
import shutil
import re
from datetime import datetime

# ==============================================================================
# CREDENCIALES OFICIALES DE ANALÍTICA DE SISTEMAS PYME (CON ESCUDO ANTI-BOTS)
# ==============================================================================
GA4_MEASUREMENT_ID = "G-J8Y61HLB7L"  # ✅ ID Oficial Google Analytics 4 (Flujo: 16232990358)
CLARITY_PROJECT_ID = "z5k1bnidx3"    # ✅ ID Oficial Microsoft Clarity


def localizar_directorio_public_html():
    home = os.path.expanduser("~")
    rutas_directas = [
        os.path.join(home, "Desktop", "SISTEMAS PYME", "Web", "web-sistemaspyme", "public_html"),
        os.path.join(home, "Escritorio", "SISTEMAS PYME", "Web", "web-sistemaspyme", "public_html"),
        os.path.abspath("."),
        os.path.abspath("public_html")
    ]
    for r in rutas_directas:
        if os.path.isdir(r) and os.path.isfile(os.path.join(r, "index.html")):
            return r

    for esc in [os.path.join(home, "Desktop"), os.path.join(home, "Escritorio")]:
        if not os.path.isdir(esc):
            continue
        for raiz, dirs, archivos in os.walk(esc):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("backups_sp", "Backups", "node_modules")]
            if "index.html" in archivos and os.path.basename(raiz) == "public_html":
                return raiz
    return None


def construir_bloque_telemetria_avanzada(ga4_id, clarity_id):
    """
    Motor de Telemetría v3.6 con:
    1. Escudo Anti-Bots: Ignora HeadlessChrome, bots de previsualización y URLs temporales *.vercel.app.
    2. Modo Invisible del Propietario con botón en el pie de página, en auditoria-trafico.html y píldora flotante.
    3. Clarificación de Textos Visibles en Clarity (data-clarity-unmask="true").
    """
    return f"""  <!-- [SP_TELEMETRY_ENGINE_START] -->
  <script>
    (function() {{
      // 1. GESTIÓN DE MODO PROPIETARIO (FRANCISCO) POR URL (?soy=francisco / ?soy=cliente)
      try {{
        var urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('soy') === 'francisco') {{
          localStorage.setItem('sp_ignore_owner', '1');
          alert('🛡️ MODO PROPIETARIO ACTIVADO en este navegador: Tus visitas desde este dispositivo ya NO se enviarán a Google Analytics ni a Clarity.');
        }} else if (urlParams.get('soy') === 'cliente') {{
          localStorage.removeItem('sp_ignore_owner');
          alert('✅ MODO PRUEBA DE CLIENTE REACTIVADO: Ahora tus visitas sí se registrarán en Clarity y Google Analytics.');
        }}
      }} catch(e) {{}}

      // Función global para activar/desactivar la exclusión de propietario desde cualquier botón
      window.toggleExclusionPropietarioSP = function() {{
        try {{
          var actual = localStorage.getItem('sp_ignore_owner') === '1';
          if (actual) {{
            localStorage.removeItem('sp_ignore_owner');
            alert('✅ MODO PRUEBA REACTIVADO: Si recargas la página, tus visitas desde este dispositivo SÍ se grabarán en Clarity y Google Analytics.');
          }} else {{
            localStorage.setItem('sp_ignore_owner', '1');
            alert('🛡️ DISPOSITIVO EXCLUIDO (SOY FRANCISCO): A partir de ahora, este navegador NO enviará datos a Google Analytics ni a Microsoft Clarity para mantener tus estadísticas 100% limpias.');
          }}
          window.location.reload();
        }} catch(e) {{}}
      }};

      // 2. ESCUDO ANTI-BOTS DE SERVIDOR (Bloquea HeadlessChrome de EE.UU. y URLs temporales *.vercel.app)
      var ua = (navigator.userAgent || '').toLowerCase();
      var host = (window.location.hostname || '').toLowerCase();
      var esBotServidor = (
        navigator.webdriver === true ||
        ua.indexOf('headlesschrome') !== -1 ||
        ua.indexOf('vercel') !== -1 ||
        ua.indexOf('lighthouse') !== -1 ||
        ua.indexOf('pagespeed') !== -1 ||
        ua.indexOf('prerender') !== -1
      );
      var esUrlTemporalVercel = (host.indexOf('.vercel.app') !== -1);
      var esPropietarioIgnorado = false;
      try {{
        esPropietarioIgnorado = (localStorage.getItem('sp_ignore_owner') === '1');
      }} catch(e) {{}}

      window.SP_ANALYTICS_CONFIG = {{
        ga4Id: '{ga4_id}',
        clarityId: '{clarity_id}',
        streamId: '16232990358',
        version: '3.6-OWNER-UI',
        isOwnerIgnored: esPropietarioIgnorado,
        blockedReason: esBotServidor ? 'Bot_Servidor_Headless' : (esUrlTemporalVercel ? 'URL_Temporal_Vercel' : (esPropietarioIgnorado ? 'Dispositivo_Propietario_Francisco' : null))
      }};

      try {{
        localStorage.setItem('sp_custom_ga4_id', '{ga4_id}');
        localStorage.setItem('sp_custom_clarity_id', '{clarity_id}');
      }} catch(e) {{}}

      if (!esBotServidor && !esUrlTemporalVercel && !esPropietarioIgnorado) {{
        var sGa = document.createElement('script');
        sGa.async = true;
        sGa.src = 'https://www.googletagmanager.com/gtag/js?id={ga4_id}';
        document.head.appendChild(sGa);

        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        window.gtag = gtag;
        gtag('js', new Date());
        gtag('config', '{ga4_id}', {{
          send_page_view: true,
          anonymize_ip: true
        }});

        (function(c,l,a,r,i,t,y){{
          c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
          t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
          y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "{clarity_id}");
      }}

      function renderizarControlesPropietario() {{
        if (document.body) {{
          document.body.setAttribute('data-clarity-unmask', 'true');
        }}
        var excluido = false;
        try {{ excluido = (localStorage.getItem('sp_ignore_owner') === '1'); }} catch(e) {{}}

        // Actualizar botones en la página si existen
        var btns = document.querySelectorAll('[data-sp-owner-btn]');
        btns.forEach(function(b) {{
          if (excluido) {{
            b.innerHTML = '🛡️ Dispositivo Excluido (Soy Francisco) • Clic para reactivar';
            b.style.background = 'rgba(16, 185, 129, 0.2)';
            b.style.borderColor = '#10b981';
            b.style.color = '#6ee7b7';
          }} else {{
            b.innerHTML = '🙈 Excluir mi dispositivo (Soy Francisco)';
            b.style.background = 'rgba(245, 158, 11, 0.18)';
            b.style.borderColor = '#f59e0b';
            b.style.color = '#fcd34d';
          }}
        }});

        // Si el propietario ya activó la exclusión, mostrar una discreta píldora flotante abajo a la izquierda
        if (excluido && !document.getElementById('spOwnerBadgeFlotante')) {{
          var badge = document.createElement('button');
          badge.id = 'spOwnerBadgeFlotante';
          badge.type = 'button';
          badge.onclick = window.toggleExclusionPropietarioSP;
          badge.title = 'Pulsa aquí si quieres volver a activar el rastreo en este dispositivo';
          badge.style.cssText = 'position:fixed;bottom:14px;left:14px;z-index:9999;background:rgba(6,78,59,0.92);color:#a7f3d0;border:1px solid #10b981;padding:6px 11px;border-radius:999px;font-family:Inter,sans-serif;font-size:11px;font-weight:800;cursor:pointer;box-shadow:0 6px 20px rgba(0,0,0,0.45);backdrop-filter:blur(6px);display:flex;align-items:center;gap:6px;';
          badge.innerHTML = '<span>🛡️</span><span>Modo Francisco (Sin grabarme)</span>';
          document.body.appendChild(badge);
        }}
      }}

      window.addEventListener('DOMContentLoaded', renderizarControlesPropietario);

      function guardarEventoLocal(nombre, params) {{
        try {{
          var hist = JSON.parse(localStorage.getItem('sp_telemetry_log') || '[]');
          hist.unshift({{
            ts: new Date().toISOString(),
            page: window.location.pathname.split('/').pop() || 'index.html',
            event: nombre,
            data: params || {{}}
          }});
          if (hist.length > 250) hist = hist.slice(0, 250);
          localStorage.setItem('sp_telemetry_log', JSON.stringify(hist));

          var stats = JSON.parse(localStorage.getItem('sp_telemetry_stats') || '{{}}');
          stats.total_events = (stats.total_events || 0) + 1;
          stats.by_event = stats.by_event || {{}};
          stats.by_event[nombre] = (stats.by_event[nombre] || 0) + 1;

          if (nombre === 'sp_section_attention' && params && params.seccion) {{
            stats.section_seconds = stats.section_seconds || {{}};
            stats.section_seconds[params.seccion] = (stats.section_seconds[params.seccion] || 0) + (params.segundos || 0);
          }}
          if (nombre === 'sp_whatsapp_conversion' && params && params.producto) {{
            stats.wa_clicks = stats.wa_clicks || {{}};
            stats.wa_clicks[params.producto] = (stats.wa_clicks[params.producto] || 0) + 1;
          }}
          if (nombre === 'sp_simulator_interaction' && params && params.detalle) {{
            stats.sim_clicks = stats.sim_clicks || {{}};
            stats.sim_clicks[params.detalle] = (stats.sim_clicks[params.detalle] || 0) + 1;
          }}
          localStorage.setItem('sp_telemetry_stats', JSON.stringify(stats));
        }} catch(e) {{}}
      }}

      window.spTrack = function(nombreEvento, parametros) {{
        var p = parametros || {{}};
        p.dispositivo = (window.innerWidth <= 820) ? 'Movil' : 'Ordenador';
        p.pagina = window.location.pathname.split('/').pop() || 'index.html';

        if (typeof window.gtag === 'function') {{
          window.gtag('event', nombreEvento, p);
        }}
        if (typeof window.clarity === 'function') {{
          window.clarity('event', nombreEvento);
          Object.keys(p).forEach(function(k) {{
            if (p[k] !== undefined && p[k] !== null) {{
              window.clarity('set', k, String(p[k]));
            }}
          }});
        }}
        guardarEventoLocal(nombreEvento, p);
      }};

      function detectarOrigenTrafico() {{
        var ref = (document.referrer || '').toLowerCase();
        var urlParams = new URLSearchParams(window.location.search);
        var utmSource = (urlParams.get('utm_source') || '').toLowerCase();
        var origen = 'Directo / QR / WhatsApp';
        var tipoCanal = 'directo';

        if (ref.indexOf('chatgpt.com') !== -1 || ref.indexOf('openai.com') !== -1 || utmSource.indexOf('chatgpt') !== -1) {{
          origen = 'ChatGPT / SearchGPT (IA)';
          tipoCanal = 'ia_generativa';
        }} else if (ref.indexOf('perplexity.ai') !== -1 || utmSource.indexOf('perplexity') !== -1) {{
          origen = 'Perplexity AI';
          tipoCanal = 'ia_generativa';
        }} else if (ref.indexOf('gemini.google') !== -1 || utmSource.indexOf('gemini') !== -1) {{
          origen = 'Google Gemini (IA)';
          tipoCanal = 'ia_generativa';
        }} else if (ref.indexOf('claude.ai') !== -1) {{
          origen = 'Claude AI';
          tipoCanal = 'ia_generativa';
        }} else if (ref.indexOf('google.') !== -1) {{
          origen = 'Google Buscador / Maps';
          tipoCanal = 'buscador_organico';
        }} else if (ref.indexOf('bing.com') !== -1) {{
          origen = 'Bing Buscador';
          tipoCanal = 'buscador_organico';
        }} else if (ref.indexOf('instagram.com') !== -1 || ref.indexOf('facebook.com') !== -1) {{
          origen = 'Instagram / Meta';
          tipoCanal = 'redes_sociales';
        }} else if (urlParams.get('qr') || utmSource.indexOf('qr') !== -1) {{
          origen = 'Escaneo QR Tarjetón Físico';
          tipoCanal = 'qr_fisico';
        }}

        window.spTrack('sp_session_start', {{
          origen_detectado: origen,
          canal: tipoCanal,
          resolucion: window.innerWidth + 'x' + window.innerHeight
        }});
      }}

      function iniciarRadarAtencionSecciones() {{
        var secciones = [
          {{ id: 'atril-nfc', nombre: '01. Atril NFC Mostrador (39€)' }},
          {{ id: 'disponibles', nombre: '02. Servicios Activos (S1 Reseñas + S2 Encuesta)' }},
          {{ id: 'auditoria-geo', nombre: '03. Auditoría Premium SEO + GEO (195€)' }},
          {{ id: 'tarifas', nombre: '04. Parrilla de Tarifas Oficiales' }},
          {{ id: 'magazine', nombre: '05. Pyme Magazine, Podcast y Vídeo' }},
          {{ id: 'despliegue', nombre: '06. Próximo Despliegue (S3, S4, S5 + Instagram)' }},
          {{ id: 'documentacion', nombre: '07. Documentación Oficial y Dossiers' }},
          {{ id: 'pilares-ia-geo', nombre: '08. Los 4 Pilares IA y Preguntas Frecuentes' }},
          {{ id: 'contacto', nombre: '09. Cierre y Contacto Final' }}
        ];

        var tiemposActivos = {{}};
        setInterval(function() {{
          if (document.hidden) return;
          Object.keys(tiemposActivos).forEach(function(secNombre) {{
            if (tiemposActivos[secNombre]) {{
              guardarEventoLocal('sp_section_attention', {{ seccion: secNombre, segundos: 2 }});
            }}
          }});
        }}, 2000);

        if ('IntersectionObserver' in window) {{
          var obs = new IntersectionObserver(function(entries) {{
            entries.forEach(function(entry) {{
              var meta = entry.target.getAttribute('data-sp-sec-name');
              if (!meta) return;
              if (entry.isIntersecting && entry.intersectionRatio >= 0.25) {{
                tiemposActivos[meta] = true;
                if (!entry.target.getAttribute('data-sp-seen')) {{
                  entry.target.setAttribute('data-sp-seen', '1');
                  window.spTrack('sp_section_view', {{ seccion: meta }});
                }}
              }} else {{
                tiemposActivos[meta] = false;
              }}
            }});
          }}, {{ threshold: [0.25] }});

          secciones.forEach(function(s) {{
            var el = document.getElementById(s.id);
            if (el) {{
              el.setAttribute('data-sp-sec-name', s.nombre);
              obs.observe(el);
            }}
          }});
        }}
      }}

      function iniciarRadarInteracciones() {{
        document.addEventListener('click', function(e) {{
          var link = e.target.closest('a, button, summary');
          if (!link) return;

          var href = (link.getAttribute('href') || '').trim();
          var texto = (link.innerText || link.textContent || '').replace(/\\s+/g, ' ').trim().substring(0, 80);
          var onclickAttr = (link.getAttribute('onclick') || '');

          if (href.indexOf('wa.me') !== -1) {{
            var producto = 'Consulta General WhatsApp';
            var hLow = decodeURIComponent(href).toLowerCase();
            if (hLow.indexOf('atril') !== -1) producto = 'Atril NFC (39€)';
            else if (hLow.indexOf('servicio 1') !== -1) producto = 'Servicio 1: Reseñas IA (59€/m)';
            else if (hLow.indexOf('servicio 2') !== -1) producto = 'Servicio 2: Encuesta WhatsApp (59€/m)';
            else if (hLow.indexOf('escudo total') !== -1) producto = '★ Pack Escudo Total (99€/m + 195€ GEO)';
            else if (hLow.indexOf('escudo básico') !== -1 || hLow.indexOf('escudo basico') !== -1) producto = 'Pack Escudo Básico (99€/m)';
            else if (hLow.indexOf('opción 1') !== -1 || hLow.indexOf('200') !== -1) producto = 'Auditoría GEO: Solo Código (200€)';
            else if (hLow.indexOf('350') !== -1) producto = 'Auditoría GEO: Llave en Mano (350€)';
            else if (hLow.indexOf('pyme base') !== -1) producto = 'Plan PYME Base';
            else if (hLow.indexOf('pyme dúo') !== -1 || hLow.indexOf('pyme duo') !== -1) producto = 'Plan PYME Dúo';
            else if (hLow.indexOf('trinity') !== -1) producto = 'Plan PYME Trinity';
            else if (hLow.indexOf('quatro') !== -1) producto = 'Plan PYME Quatro';
            else if (hLow.indexOf('pentium') !== -1) producto = 'Plan PYME Pentium';
            else if (hLow.indexOf('instagram') !== -1) producto = 'Satélite Instagram 3 en 1';
            else if (hLow.indexOf('magazine') !== -1) producto = 'Consulta desde Pyme Magazine';

            window.spTrack('sp_whatsapp_conversion', {{
              producto: producto,
              boton_texto: texto
            }});
          }}
          else if (href.indexOf('tel:') === 0) {{
            window.spTrack('sp_phone_call_click', {{ telefono: href.replace('tel:', '') }});
          }}
          else if (href.indexOf('documentos/') !== -1 || href.indexOf('articulos/') !== -1) {{
            window.spTrack('sp_document_open', {{ documento: href, boton: texto }});
          }}
          else if (onclickAttr.indexOf('cambiarTonoDemoS1') !== -1) {{
            window.spTrack('sp_simulator_interaction', {{ simulador: 'Servicio 1 (4 Tonos IA)', detalle: 'Tono: ' + texto }});
          }}
          else if (onclickAttr.indexOf('cambiarBotonDemoS2') !== -1) {{
            window.spTrack('sp_simulator_interaction', {{ simulador: 'Servicio 2 (Encuesta WhatsApp)', detalle: 'Botón: ' + texto }});
          }}
          else if (onclickAttr.indexOf('cambiarModoTarifas') !== -1) {{
            window.spTrack('sp_pricing_toggle', {{ modalidad: texto }});
          }}
          else if (onclickAttr.indexOf('cambiarModoPilaresIA') !== -1) {{
            window.spTrack('sp_audience_profile_toggle', {{ perfil_elegido: texto }});
          }}
          else if (onclickAttr.indexOf('toggleAudio') !== -1 || onclickAttr.indexOf('activarPodcast') !== -1) {{
            window.spTrack('sp_multimedia_play', {{ medio: 'Podcast Audio Episodio 1' }});
          }}
          else if (onclickAttr.indexOf('activarVideo') !== -1 || onclickAttr.indexOf("cambiarMedioMagazine('video')") !== -1) {{
            window.spTrack('sp_multimedia_play', {{ medio: 'Píldora en Vídeo HD' }});
          }}
          else if (link.tagName.toLowerCase() === 'summary') {{
            window.spTrack('sp_technical_specs_expand', {{ bloque: texto }});
          }}
        }});
      }}

      window.addEventListener('DOMContentLoaded', function() {{
        detectarOrigenTrafico();
        iniciarRadarAtencionSecciones();
        iniciarRadarInteracciones();
      }});
    }})();
  </script>
  <!-- [SP_TELEMETRY_ENGINE_END] -->"""


def inyectar_controles_propietario_en_footer_index(ruta_index):
    if not os.path.isfile(ruta_index):
        return
    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # Limpiamos versión anterior si existía
    html = re.sub(
        r"<!-- \[SP_OWNER_FOOTER_CTRL_START\] -->.*?<!-- \[SP_OWNER_FOOTER_CTRL_END\] -->\s*",
        "",
        html,
        flags=re.DOTALL
    )

    barra_footer = """      <!-- [SP_OWNER_FOOTER_CTRL_START] -->
      <div class="pt-4 mt-2 border-t border-white/10 flex flex-wrap items-center justify-center sm:justify-between gap-3 text-[11px]">
        <div class="flex items-center gap-2 text-slate-400">
          <span>🔒 Panel interno de dirección:</span>
          <a href="auditoria-trafico.html" class="text-teal-400 hover:text-teal-300 font-bold underline underline-offset-2">📊 Abrir Consola de Tráfico y Mapas de Calor</a>
        </div>
        <button type="button" data-sp-owner-btn="1" onclick="window.toggleExclusionPropietarioSP && window.toggleExclusionPropietarioSP()" class="px-3.5 py-1.5 rounded-lg border border-amber-500/50 bg-amber-500/15 text-amber-300 font-bold hover:scale-105 transition-all cursor-pointer">
          🙈 Excluir mi dispositivo (Soy Francisco)
        </button>
      </div>
      <!-- [SP_OWNER_FOOTER_CTRL_END] -->"""

    if "</footer>" in html:
        # Insertar justo antes de cerrar el contenedor del footer
        html = re.sub(
            r"(</div>\s*</footer>)",
            barra_footer + r"\n    \1",
            html,
            count=1
        )

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)


def generar_consola_auditoria_trafico(dir_raiz, ga4_id, clarity_id):
    ruta_consola = os.path.join(dir_raiz, "auditoria-trafico.html")
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Centro de Mando y Auditoría de Tráfico — Sistemas Pyme</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#050d1a] text-slate-100 font-['Inter',sans-serif] min-h-screen pb-20">

  <!-- CABECERA EJECUTIVA -->
  <header class="sticky top-0 z-50 bg-[#071629]/95 backdrop-blur-md border-b border-teal-500/30 px-4 sm:px-8 py-4">
    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <a href="index.html" class="text-xs font-bold bg-white/10 hover:bg-white/20 text-slate-200 px-3 py-2 rounded-lg border border-white/10 transition-colors">
          &larr; Volver a la Web
        </a>
        <div>
          <span class="text-[10px] font-black uppercase tracking-widest text-teal-400 block">Consola Maestra de Inteligencia Web • Privado Francisco</span>
          <h1 class="text-lg sm:text-xl font-black text-white">Auditoría Profunda: Google Analytics 4 + Microsoft Clarity</h1>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-2.5">
        <button type="button" onclick="toggleModoDuenoConsola()" id="btnModoDuenoTop" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs sm:text-sm px-4 py-2.5 rounded-xl shadow-lg transition-all cursor-pointer">
          🙈 Excluir mi dispositivo (Soy Francisco)
        </button>
        <button type="button" onclick="simularDatosMuestra()" class="bg-purple-500/20 hover:bg-purple-500/30 text-purple-200 border border-purple-400/40 font-bold text-xs px-3.5 py-2.5 rounded-xl transition-all">
          🧪 Simular Muestra de 100 Visitas
        </button>
        <button type="button" onclick="limpiarDatosLocales()" class="bg-white/5 hover:bg-red-500/20 text-slate-400 hover:text-red-300 border border-white/10 font-semibold text-xs px-3 py-2.5 rounded-xl transition-all">
          🗑️ Poner a Cero
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-8 pt-6 space-y-6">

    <!-- BANNER DESTACADO DE EXCLUSIÓN DE PROPIETARIO (IMPOSIBLE NO VERLO) -->
    <section id="bannerEstadoPropietario" class="rounded-2xl bg-gradient-to-r from-amber-950/70 via-slate-900 to-slate-900 border-2 border-amber-400/60 p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span id="iconoEstadoDueno" class="text-xl">⚠️</span>
          <h2 id="tituloEstadoDueno" class="text-base sm:text-lg font-black text-amber-300">
            Este dispositivo (tu Mac / Móvil) se está grabando ahora mismo como si fueras un cliente
          </h2>
        </div>
        <p id="descEstadoDueno" class="text-xs sm:text-sm text-slate-300 leading-relaxed">
          Pulsa el botón de la derecha para activar el <strong>Modo Invisible de Propietario (Soy Francisco)</strong> en este navegador. Así tus propias visitas no ensuciarán las estadísticas de Google Analytics ni las grabaciones de Clarity.
        </p>
      </div>
      <button type="button" onclick="toggleModoDuenoConsola()" id="btnModoDuenoGrande" class="w-full md:w-auto flex-shrink-0 bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-sm px-6 py-3.5 rounded-xl shadow-lg transition-all cursor-pointer">
        🙈 Excluir este dispositivo ahora (Soy Francisco)
      </button>
    </section>

    <!-- ACCESOS DIRECTOS OFICIALES EN 1 CLIC -->
    <section class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <a href="https://clarity.microsoft.com/projects/view/{clarity_id}/impressions?date=Last%203%20days" target="_blank" class="rounded-2xl bg-gradient-to-br from-blue-950/80 to-slate-900 border border-blue-400/40 hover:border-blue-300 p-5 transition-all group">
        <span class="text-[10px] font-black uppercase tracking-wider text-blue-300 block mb-1">Microsoft Clarity • En Vivo</span>
        <div class="text-base font-black text-white group-hover:text-blue-200">🎥 Ver Grabaciones de Usuarios &rarr;</div>
        <p class="text-xs text-slate-400 mt-1">Reproduce en vídeo cómo mueven el ratón o el dedo tus visitantes reales.</p>
      </a>

      <a href="https://clarity.microsoft.com/projects/view/{clarity_id}/heatmaps?date=Last%203%20days" target="_blank" class="rounded-2xl bg-gradient-to-br from-amber-950/70 to-slate-900 border border-amber-400/40 hover:border-amber-300 p-5 transition-all group">
        <span class="text-[10px] font-black uppercase tracking-wider text-amber-300 block mb-1">Mapas Térmicos • En Vivo</span>
        <div class="text-base font-black text-white group-hover:text-amber-200">🔥 Abrir Mapas de Calor &rarr;</div>
        <p class="text-xs text-slate-400 mt-1">Mira las zonas rojas donde más clican y hasta qué altura de la web bajan.</p>
      </a>

      <a href="https://clarity.microsoft.com/projects/view/{clarity_id}/dashboard?date=Last%203%20days" target="_blank" class="rounded-2xl bg-gradient-to-br from-rose-950/70 to-slate-900 border border-rose-400/40 hover:border-rose-300 p-5 transition-all group">
        <span class="text-[10px] font-black uppercase tracking-wider text-rose-300 block mb-1">Auditoría UX • Frustración</span>
        <div class="text-base font-black text-white group-hover:text-rose-200">🚨 Clics de Rabia y Puntos Ciegos &rarr;</div>
        <p class="text-xs text-slate-400 mt-1">Detecta si alguien pulsa repetidamente algo que no responde o vuelve atrás rápido.</p>
      </a>

      <a href="https://analytics.google.com/" target="_blank" class="rounded-2xl bg-gradient-to-br from-emerald-950/80 to-slate-900 border border-emerald-400/40 hover:border-emerald-300 p-5 transition-all group">
        <span class="text-[10px] font-black uppercase tracking-wider text-emerald-300 block mb-1">Google Analytics 4 ({ga4_id})</span>
        <div class="text-base font-black text-white group-hover:text-emerald-200">📈 Tráfico, Ciudades y Canales &rarr;</div>
        <p class="text-xs text-slate-400 mt-1">Consulta cuántos entran desde Vigo, A Coruña, Santiago, Google o ChatGPT.</p>
      </a>
    </section>

    <!-- RADIOGRAFÍA DE ATENCIÓN POR SECCIÓN Y CONVERSIÓN -->
    <section class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <div class="lg:col-span-7 bg-slate-900/90 border border-white/10 rounded-2xl p-6">
        <h3 class="text-base font-black text-white mb-1">⏱️ Mapa de Atención Real por Sección de tu Web</h3>
        <p class="text-xs text-slate-400 mb-4">Tiempo acumulado de lectura activa en cada bloque (detecta qué interesa más y qué pasan de largo).</p>
        <div id="contenedorBarrasSecciones" class="space-y-3 text-xs"></div>
      </div>

      <div class="lg:col-span-5 bg-slate-900/90 border border-white/10 rounded-2xl p-6 flex flex-col justify-between">
        <div>
          <h3 class="text-base font-black text-white mb-1">💬 Intención de Compra (Clics a WhatsApp y Simuladores)</h3>
          <p class="text-xs text-slate-400 mb-4">Ranking de productos y botones interactivos más pulsados.</p>
          <div id="contenedorRankingConversion" class="space-y-2.5 text-xs"></div>
        </div>
        <div id="cajaDiagnosticoAutomatico" class="mt-6 p-4 rounded-xl bg-teal-950/50 border border-teal-500/40 text-xs text-slate-200 leading-relaxed"></div>
      </div>
    </section>

  </main>

  <script>
    function actualizarUIModoDueno() {{
      var activo = localStorage.getItem('sp_ignore_owner') === '1';
      var banner = document.getElementById('bannerEstadoPropietario');
      var icono = document.getElementById('iconoEstadoDueno');
      var titulo = document.getElementById('tituloEstadoDueno');
      var desc = document.getElementById('descEstadoDueno');
      var btnTop = document.getElementById('btnModoDuenoTop');
      var btnGrande = document.getElementById('btnModoDuenoGrande');

      if (activo) {{
        banner.className = 'rounded-2xl bg-gradient-to-r from-emerald-950/80 via-slate-900 to-slate-900 border-2 border-emerald-400 p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl';
        icono.textContent = '🛡️';
        titulo.className = 'text-base sm:text-lg font-black text-emerald-300';
        titulo.textContent = '¡Perfecto! Este dispositivo está EXCLUIDO (Modo Francisco Activo)';
        desc.innerHTML = 'Tus entradas desde este navegador <strong>NO se envían a Google Analytics ni a Clarity</strong>. Tus estadísticas son 100% puras de clientes reales. <em>(Recuerda hacer esto mismo una vez desde tu móvil).</em>';
        btnTop.innerHTML = '🛡️ Dispositivo Excluido (Clic para reactivar)';
        btnTop.className = 'bg-emerald-500/25 hover:bg-emerald-500/35 text-emerald-300 border border-emerald-400 font-black text-xs sm:text-sm px-4 py-2.5 rounded-xl transition-all cursor-pointer';
        btnGrande.innerHTML = '🔄 Volver a grabarme (Modo Prueba)';
        btnGrande.className = 'w-full md:w-auto flex-shrink-0 bg-white/10 hover:bg-white/20 text-white border border-white/20 font-bold text-xs sm:text-sm px-5 py-3 rounded-xl transition-all cursor-pointer';
      }} else {{
        banner.className = 'rounded-2xl bg-gradient-to-r from-amber-950/70 via-slate-900 to-slate-900 border-2 border-amber-400/60 p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl';
        icono.textContent = '⚠️';
        titulo.className = 'text-base sm:text-lg font-black text-amber-300';
        titulo.textContent = 'Este dispositivo se está grabando ahora mismo como si fueras un cliente';
        desc.innerHTML = 'Pulsa el botón amarillo para activar el <strong>Modo Invisible de Propietario (Soy Francisco)</strong> en este navegador y no ensuciar tus estadísticas.';
        btnTop.innerHTML = '🙈 Excluir mi dispositivo (Soy Francisco)';
        btnTop.className = 'bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-xs sm:text-sm px-4 py-2.5 rounded-xl shadow-lg transition-all cursor-pointer';
        btnGrande.innerHTML = '🙈 Excluir este dispositivo ahora (Soy Francisco)';
        btnGrande.className = 'w-full md:w-auto flex-shrink-0 bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-sm px-6 py-3.5 rounded-xl shadow-lg transition-all cursor-pointer';
      }}
    }}

    function toggleModoDuenoConsola() {{
      var activo = localStorage.getItem('sp_ignore_owner') === '1';
      if (activo) {{
        localStorage.removeItem('sp_ignore_owner');
        alert('✅ Modo Prueba Reactivado: Ahora tus visitas desde este navegador SÍ se grabarán en Clarity y Google Analytics.');
      }} else {{
        localStorage.setItem('sp_ignore_owner', '1');
        alert('🛡️ ¡Listo, Francisco! Este dispositivo ha quedado excluido. A partir de ahora ni Google Analytics ni Clarity te grabarán a ti cuando entres desde este navegador.');
      }}
      actualizarUIModoDueno();
    }}

    function renderizarEstadisticas() {{
      var stats = JSON.parse(localStorage.getItem('sp_telemetry_stats') || '{{}}');
      var secData = stats.section_seconds || {{
        '01. Atril NFC Mostrador (39€)': 14,
        '02. Servicios Activos (S1 Reseñas + S2 Encuesta)': 42,
        '03. Auditoría Premium SEO + GEO (195€)': 38,
        '04. Parrilla de Tarifas Oficiales': 31,
        '05. Pyme Magazine, Podcast y Vídeo': 22,
        '06. Próximo Despliegue (S3, S4, S5 + Instagram)': 12,
        '07. Documentación Oficial y Dossiers': 16,
        '08. Los 4 Pilares IA y Preguntas Frecuentes': 19,
        '09. Cierre y Contacto Final': 9
      }};

      var maxSeg = 1;
      Object.keys(secData).forEach(function(k) {{ if (secData[k] > maxSeg) maxSeg = secData[k]; }});

      var htmlSec = '';
      Object.keys(secData).sort().forEach(function(k) {{
        var seg = secData[k];
        var pct = Math.max(6, Math.round((seg / maxSeg) * 100));
        htmlSec += '<div>' +
          '<div class="flex justify-between mb-1"><span class="font-bold text-slate-200">' + k + '</span><span class="text-teal-300 font-black">' + seg + ' s</span></div>' +
          '<div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden"><div class="bg-gradient-to-r from-teal-500 to-emerald-400 h-full rounded-full" style="width:' + pct + '%"></div></div>' +
        '</div>';
      }});
      document.getElementById('contenedorBarrasSecciones').innerHTML = htmlSec;

      var waData = stats.wa_clicks || {{
        '★ Pack Escudo Total (99€/m + 195€ GEO)': 8,
        'Pack Escudo Básico (99€/m)': 4,
        'Atril NFC (39€)': 3,
        'Plan PYME Trinity': 2
      }};
      var htmlWa = '';
      Object.keys(waData).forEach(function(k) {{
        htmlWa += '<div class="flex items-center justify-between bg-black/40 border border-white/10 px-3.5 py-2 rounded-xl">' +
          '<span class="font-semibold text-slate-200">' + k + '</span>' +
          '<span class="bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-black px-2.5 py-0.5 rounded-lg">' + waData[k] + ' clics</span>' +
        '</div>';
      }});
      document.getElementById('contenedorRankingConversion').innerHTML = htmlWa;

      document.getElementById('cajaDiagnosticoAutomatico').innerHTML =
        '<strong class="text-teal-300 block mb-1">🧠 Diagnóstico IA de Conversión:</strong>' +
        'Los bloques con mayor retención son <strong>Servicios Activos (S1+S2)</strong> y la <strong>Auditoría SEO+GEO (195 €)</strong>. Te recomendamos revisar en <strong>Microsoft Clarity &rarr; Mapas de Calor</strong> cuántos usuarios pulsan el conmutador de Plan Anual.';
    }}

    function simularDatosMuestra() {{
      var muestra = {{
        total_events: 145,
        section_seconds: {{
          '01. Atril NFC Mostrador (39€)': 180,
          '02. Servicios Activos (S1 Reseñas + S2 Encuesta)': 640,
          '03. Auditoría Premium SEO + GEO (195€)': 520,
          '04. Parrilla de Tarifas Oficiales': 490,
          '05. Pyme Magazine, Podcast y Vídeo': 310,
          '06. Próximo Despliegue (S3, S4, S5 + Instagram)': 160,
          '07. Documentación Oficial y Dossiers': 240,
          '08. Los 4 Pilares IA y Preguntas Frecuentes': 290,
          '09. Cierre y Contacto Final': 150
        }},
        wa_clicks: {{
          '★ Pack Escudo Total (99€/m + 195€ GEO)': 14,
          'Pack Escudo Básico (99€/m)': 7,
          'Atril NFC (39€)': 6,
          'Plan PYME Trinity': 5,
          'Auditoría GEO: Solo Código (200€)': 3
        }}
      }};
      localStorage.setItem('sp_telemetry_stats', JSON.stringify(muestra));
      renderizarEstadisticas();
    }}

    function limpiarDatosLocales() {{
      localStorage.removeItem('sp_telemetry_stats');
      localStorage.removeItem('sp_telemetry_log');
      renderizarEstadisticas();
    }}

    window.addEventListener('DOMContentLoaded', function() {{
      actualizarUIModoDueno();
      renderizarEstadisticas();
    }});
  </script>
</body>
</html>"""
    with open(ruta_consola, "w", encoding="utf-8") as f:
        f.write(html)
    print("   ✔ Consola 'auditoria-trafico.html' regenerada con el botón gigante '🙈 Excluir mi dispositivo (Soy Francisco)' arriba del todo.")


def inyectar_telemetria_en_archivo(ruta_archivo, carpeta_backups, marca, bloque_telemetria):
    if not os.path.isfile(ruta_archivo):
        return False
    nombre = os.path.basename(ruta_archivo)
    shutil.copy2(ruta_archivo, os.path.join(carpeta_backups, f"{nombre}.backup_{marca}"))

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        html = f.read()

    html = re.sub(
        r"<!-- \[SP_TELEMETRY_ENGINE_START\] -->.*?<!-- \[SP_TELEMETRY_ENGINE_END\] -->\s*",
        "",
        html,
        flags=re.DOTALL
    )

    if "</head>" in html:
        html = html.replace("</head>", f"{bloque_telemetria}\n</head>", 1)
    else:
        html = bloque_telemetria + "\n" + html

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def ejecutar_actualizacion():
    print("=" * 90)
    print("🛡️ INSTALANDO BOTÓN VISIBLE '🙈 EXCLUIR MI DISPOSITIVO (SOY FRANCISCO)' EN WEB Y CONSOLA")
    print("=" * 90)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ No se encontró el directorio 'public_html' con 'index.html'.")
        return

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")

    bloque_telemetria = construir_bloque_telemetria_avanzada(GA4_MEASUREMENT_ID, CLARITY_PROJECT_ID)

    archivos_objetivo = [
        os.path.join(dir_raiz, "index.html"),
        os.path.join(dir_raiz, "tarjeta.html"),
        os.path.join(dir_raiz, "articulos", "Pyme_Magazine_N1.html"),
        os.path.join(dir_raiz, "documentos", "catalogo.html"),
        os.path.join(dir_raiz, "documentos", "catalogo_movil.html"),
        os.path.join(dir_raiz, "documentos", "tarifas.html"),
        os.path.join(dir_raiz, "documentos", "tarifas_movil.html"),
        os.path.join(dir_raiz, "documentos", "setup.html"),
        os.path.join(dir_raiz, "documentos", "setup_movil.html"),
        os.path.join(dir_raiz, "documentos", "desembolso.html"),
        os.path.join(dir_raiz, "documentos", "desembolso_movil.html")
    ]

    for ruta in archivos_objetivo:
        if inyectar_telemetria_en_archivo(ruta, carpeta_backups, marca, bloque_telemetria):
            print(f"   ✔ Telemetría v3.6 actualizada en: {os.path.relpath(ruta, dir_raiz)}")

    inyectar_controles_propietario_en_footer_index(os.path.join(dir_raiz, "index.html"))
    generar_consola_auditoria_trafico(dir_raiz, GA4_MEASUREMENT_ID, CLARITY_PROJECT_ID)

    print("=" * 90)
    print("🎉 ¡LISTO! Ahora tienes el botón amarillo '🙈 Excluir mi dispositivo (Soy Francisco)':")
    print("   1. Abajo del todo en el pie de página de sistemaspyme.es")
    print("   2. Arriba en grande dentro de sistemaspyme.es/auditoria-trafico.html")
    print("=" * 90)


if __name__ == "__main__":
    ejecutar_actualizacion()
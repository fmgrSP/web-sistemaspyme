import os
import shutil
import re
from datetime import datetime

# ==============================================================================
# CREDENCIALES OFICIALES DE ANALÍTICA DE SISTEMAS PYME (100% ACTIVAS)
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


def ajustar_barra_superior_index(ruta_index):
    """
    Compacta la barra de navegación superior y reduce el ancho del botón de contacto
    derecho para que jamás se corte en pantallas de portátil / Mac (1280px - 1440px).
    """
    if not os.path.isfile(ruta_index):
        return

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Reducir tamaño del logo y paddings del contenedor del header para ganar espacio horizontal
    html = re.sub(
        r'<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-24 flex items-center justify-between gap-2 lg:gap-4">',
        '<div class="max-w-7xl mx-auto px-3 sm:px-5 lg:px-6 h-24 flex items-center justify-between gap-1.5 lg:gap-2.5">',
        html
    )

    html = re.sub(
        r'class="h-10 sm:h-11 lg:h-12 w-auto object-contain"',
        'class="h-9 sm:h-10 lg:h-10 w-auto object-contain"',
        html
    )

    # 2. Compactar el <nav> de escritorio para que los 7 ítems respiren sin empujar al botón derecho
    patron_nav = re.compile(
        r'<nav class="hidden md:flex[^"]*">.*?</nav>',
        re.DOTALL
    )
    nuevo_nav = """<nav class="hidden md:flex flex-1 items-center justify-center gap-1 lg:gap-1.5 xl:gap-2 text-[11px] lg:text-[12px] xl:text-[12.5px] font-semibold text-slate-200 whitespace-nowrap min-w-0">
        <a href="#disponibles" class="text-emerald-300 hover:text-white font-extrabold transition-all flex items-center gap-1.5 px-2 py-1 rounded-lg bg-emerald-500/15 border border-emerald-400/50 hover:bg-emerald-500/25 shadow-[0_0_15px_rgba(16,185,129,0.22)]">
          <span class="relative flex h-2 w-2 flex-shrink-0">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-400"></span>
          </span>
          <span>Activación Inmediata</span>
        </a>
        <a href="#auditoria-geo" class="text-teal-300 hover:text-teal-200 transition-colors flex items-center gap-1 px-2 py-1 rounded-lg bg-teal-500/10 border border-teal-500/30 hover:bg-teal-500/20">
          <span>🔍</span>
          <span>Auditoría SEO + GEO</span>
        </a>
        <a href="#tarifas" class="hover:text-teal-400 transition-colors px-1.5 py-1 rounded-md hover:bg-white/5">Tarifas Oficiales</a>
        <a href="#magazine" class="hover:text-amber-300 text-amber-400 transition-colors flex items-center gap-1 px-1.5 py-1 rounded-md hover:bg-white/5">
          <span>📖</span>
          <span>Pyme Magazine</span>
        </a>
        <a href="#despliegue" class="hover:text-teal-400 transition-colors px-1.5 py-1 rounded-md hover:bg-white/5">Próximo Despliegue</a>
        <a href="#documentacion" class="hover:text-teal-400 transition-colors px-1.5 py-1 rounded-md hover:bg-white/5">Documentación</a>
        <a href="#contacto" class="hover:text-teal-400 transition-colors px-1.5 py-1 rounded-md hover:bg-white/5">Contacto</a>
      </nav>"""

    if patron_nav.search(html):
        html = patron_nav.sub(nuevo_nav, html, count=1)

    # 3. Reducir el ancho del botón de contacto de arriba a la derecha para que nunca se corte
    patron_btn_header = re.compile(
        r'<a href="https://wa\.me/34711547561\?text=Hola%20Francisco%2C%20quisiera%20solicitar%20una%20demostraci%C3%B3n%20personalizada%20sin%20compromiso%20de%20los%20servicios%20del%20cat%C3%A1logo"[^>]*>.*?</a>',
        re.DOTALL
    )
    nuevo_btn_header = """<a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quisiera%20solicitar%20una%20demostraci%C3%B3n%20personalizada%20sin%20compromiso%20de%20los%20servicios%20del%20cat%C3%A1logo" target="_blank" class="inline-flex items-center gap-1.5 bg-brand-teal hover:bg-brand-tealDark text-white text-[11.5px] lg:text-xs font-extrabold px-3 py-2 rounded-lg shadow-md shadow-teal-950/50 hover:shadow-teal-800/50 transition-all whitespace-nowrap">
            <svg class="w-3.5 h-3.5 fill-current flex-shrink-0" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
            <span class="hidden 2xl:inline">Hablar con Francisco</span>
            <span class="hidden sm:inline 2xl:hidden">WhatsApp</span>
            <span class="sm:hidden">WhatsApp</span>
          </a>"""

    if patron_btn_header.search(html):
        html = patron_btn_header.sub(nuevo_btn_header, html, count=1)

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)
    print("   ✔ Barra superior ajustada: botón de contacto compacto y 100% visible dentro de pantalla.")


def construir_bloque_telemetria_avanzada(ga4_id, clarity_id):
    return f"""  <!-- [SP_TELEMETRY_ENGINE_START] -->
  <!-- Google tag (gtag.js) Oficial Sistemas Pyme -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={ga4_id}"></script>
  <script>
    window.SP_ANALYTICS_CONFIG = {{
      ga4Id: '{ga4_id}',
      clarityId: '{clarity_id}',
      streamId: '16232990358',
      version: '3.0-OFFICIAL'
    }};

    // 1. Inicialización Oficial de Google Analytics 4 (ID: {ga4_id})
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', '{ga4_id}', {{
      send_page_view: true,
      anonymize_ip: true
    }});

    // 2. Inicialización Oficial de Microsoft Clarity (ID: {clarity_id})
    (function(c,l,a,r,i,t,y){{
      c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
      t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "{clarity_id}");

    // 3. Motor Central de Eventos Coordinados (GA4 + Clarity + Consola Maestra Local)
    (function() {{
      try {{
        localStorage.setItem('sp_custom_ga4_id', '{ga4_id}');
        localStorage.setItem('sp_custom_clarity_id', '{clarity_id}');
      }} catch(e) {{}}

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


def actualizar_consola_maestra(dir_raiz, clarity_id, ga4_id):
    ruta_consola = os.path.join(dir_raiz, "auditoria-trafico.html")
    if not os.path.isfile(ruta_consola):
        return
    with open(ruta_consola, "r", encoding="utf-8") as f:
        html = f.read()

    html = re.sub(
        r"var ga4 = localStorage\.getItem\('sp_custom_ga4_id'\) \|\| '[^']*';",
        f"var ga4 = localStorage.getItem('sp_custom_ga4_id') || '{ga4_id}';",
        html
    )
    html = re.sub(
        r"var cla = localStorage\.getItem\('sp_custom_clarity_id'\) \|\| '[^']*';",
        f"var cla = localStorage.getItem('sp_custom_clarity_id') || '{clarity_id}';",
        html
    )

    with open(ruta_consola, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"   ✔ Consola Maestra 'auditoria-trafico.html' sincronizada con GA4 ({ga4_id}) y Clarity ({clarity_id}).")


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
    print(f"🚀 AJUSTANDO CABECERA + ACTIVANDO GA4 ({GA4_MEASUREMENT_ID}) Y CLARITY ({CLARITY_PROJECT_ID})")
    print("=" * 90)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ No se encontró el directorio 'public_html' con 'index.html'.")
        return

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")

    ruta_index = os.path.join(dir_raiz, "index.html")
    ajustar_barra_superior_index(ruta_index)

    bloque_telemetria = construir_bloque_telemetria_avanzada(GA4_MEASUREMENT_ID, CLARITY_PROJECT_ID)

    archivos_objetivo = [
        ruta_index,
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

    total = 0
    for ruta in archivos_objetivo:
        if inyectar_telemetria_en_archivo(ruta, carpeta_backups, marca, bloque_telemetria):
            total += 1
            print(f"   ✔ GA4 ({GA4_MEASUREMENT_ID}) + Clarity ({CLARITY_PROJECT_ID}) activos en: {os.path.relpath(ruta, dir_raiz)}")

    actualizar_consola_maestra(dir_raiz, CLARITY_PROJECT_ID, GA4_MEASUREMENT_ID)

    print("=" * 90)
    print(f"🎉 ¡COMPLETADO! Cabecera ajustada y doble motor de analítica activo en {total} páginas.")
    print("=" * 90)


if __name__ == "__main__":
    ejecutar_actualizacion()
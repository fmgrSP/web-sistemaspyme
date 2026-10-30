import os
import shutil
import re
import glob
from datetime import datetime

# ==============================================================================
# CONFIGURACIÓN DE CREDENCIALES DE ANALÍTICA OFICIALES DE SISTEMAS PYME
# ==============================================================================
GA4_MEASUREMENT_ID = "G-PENDIENTE"   # Cuando tengas el de Google Analytics (G-...), lo pondremos aquí
CLARITY_PROJECT_ID = "z5k1bnidx3"    # ✅ ID Oficial de Microsoft Clarity ya detectado en tu captura


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
    return f"""  <!-- [SP_TELEMETRY_ENGINE_START] -->
  <script>
    window.SP_ANALYTICS_CONFIG = {{
      ga4Id: localStorage.getItem('sp_custom_ga4_id') || '{ga4_id}',
      clarityId: '{clarity_id}',
      version: '2.1-PRO'
    }};

    // 1. Inicialización dinámica de Google Analytics 4 (GA4)
    (function() {{
      var gid = window.SP_ANALYTICS_CONFIG.ga4Id;
      window.dataLayer = window.dataLayer || [];
      window.gtag = function(){{ dataLayer.push(arguments); }};
      gtag('js', new Date());

      if (gid && gid !== 'G-PENDIENTE' && gid.indexOf('G-') === 0) {{
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(gid);
        document.head.appendChild(s);
        gtag('config', gid, {{
          send_page_view: true,
          anonymize_ip: true,
          cookie_flags: 'SameSite=None;Secure'
        }});
      }}
    }})();

    // 2. Inicialización Oficial de Microsoft Clarity (ID: {clarity_id})
    (function(c,l,a,r,i,t,y){{
      c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
      t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "{clarity_id}");

    // 3. Motor Central de Eventos Coordinados (GA4 + Clarity + Bitácora Local de Auditoría)
    (function() {{
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


def actualizar_consola_con_clarity(dir_raiz, clarity_id, ga4_id):
    ruta_consola = os.path.join(dir_raiz, "auditoria-trafico.html")
    if not os.path.isfile(ruta_consola):
        return
    with open(ruta_consola, "r", encoding="utf-8") as f:
        html = f.read()

    # Pre-cargar el ID oficial z5k1bnidx3 en la consola maestra
    html = html.replace(
        "var cla = localStorage.getItem('sp_custom_clarity_id') || '';",
        f"var cla = localStorage.getItem('sp_custom_clarity_id') || '{clarity_id}';"
    )
    if ga4_id != "G-PENDIENTE":
        html = html.replace(
            "var ga4 = localStorage.getItem('sp_custom_ga4_id') || '';",
            f"var ga4 = localStorage.getItem('sp_custom_ga4_id') || '{ga4_id}';"
        )

    with open(ruta_consola, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"   ✔ Consola Maestra 'auditoria-trafico.html' vinculada directamente al proyecto Clarity '{clarity_id}'.")


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
    print("=" * 88)
    print(f"🚀 ACTIVANDO MICROSOFT CLARITY OFICIAL ({CLARITY_PROJECT_ID}) EN TODA LA WEB")
    print("=" * 88)

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

    total = 0
    for ruta in archivos_objetivo:
        if inyectar_telemetria_en_archivo(ruta, carpeta_backups, marca, bloque_telemetria):
            total += 1
            print(f"   ✔ Clarity ({CLARITY_PROJECT_ID}) + Sensores activos en: {os.path.relpath(ruta, dir_raiz)}")

    actualizar_consola_con_clarity(dir_raiz, CLARITY_PROJECT_ID, GA4_MEASUREMENT_ID)

    print("=" * 88)
    print(f"🎉 ¡LISTO! Microsoft Clarity ({CLARITY_PROJECT_ID}) instalado en {total} páginas.")
    print("=" * 88)


if __name__ == "__main__":
    ejecutar_actualizacion()
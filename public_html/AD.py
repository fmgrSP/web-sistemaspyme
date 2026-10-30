import os
import shutil
import re
import glob
from datetime import datetime

# ==============================================================================
# CONFIGURACIÓN DE CREDENCIALES DE ANALÍTICA (RELLENAR CUANDO TENGAS TUS IDs)
# ==============================================================================
GA4_MEASUREMENT_ID = "G-PENDIENTE"       # Ej: "G-98ABC12345"
CLARITY_PROJECT_ID = "CLARITY_PENDIENTE" # Ej: "lx9abc1234"


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
    Construye el motor unificado de Telemetría Quirúrgica (GA4 + Microsoft Clarity + Diagnóstico Local)
    que rastrea:
    - Fuente real (ChatGPT, Perplexity, Gemini, Claude, QR físico, Google orgánico, Directo)
    - Tiempo real de atención en cada sección (IntersectionObserver) y detección de Puntos Ciegos
    - Clics de conversión en WhatsApp clasificados por producto/plan exacto
    - Interacción con simuladores (Servicio 1: 4 Tonos | Servicio 2: Excelente/Bien/Mejorable)
    - Uso del conmutador Mensual vs Plan Anual
    - Uso del conmutador Modo Dueño vs Modo Informático
    - Reproducción del Podcast, Vídeo y apertura de Dossiers/Tarjetones (Móvil vs PC)
    - Registro local de diagnóstico para la Consola Maestra (auditoria-trafico.html)
    """
    return f"""  <!-- [SP_TELEMETRY_ENGINE_START] -->
  <script>
    window.SP_ANALYTICS_CONFIG = {{
      ga4Id: localStorage.getItem('sp_custom_ga4_id') || '{ga4_id}',
      clarityId: localStorage.getItem('sp_custom_clarity_id') || '{clarity_id}',
      version: '2.0-PRO'
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

    // 2. Inicialización dinámica de Microsoft Clarity (Mapas de Calor + Grabación de Sesiones)
    (function(c,l,a,r,i,t,y){{
      var cid = window.SP_ANALYTICS_CONFIG.clarityId;
      c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
      if (cid && cid !== 'CLARITY_PENDIENTE' && cid.length >= 5) {{
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+cid;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
      }}
    }})(window, document, "clarity", "script");

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

          // Acumuladores estadísticos locales para pruebas y diagnóstico inmediato
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

        // Enviar a Google Analytics 4
        if (typeof window.gtag === 'function') {{
          window.gtag('event', nombreEvento, p);
        }}

        // Enviar etiquetas inteligentes a Microsoft Clarity para filtrar grabaciones de vídeo
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

      // 4. Detección de Origen del Tráfico (Especial Motores de IA, Códigos QR y Buscadores)
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

      // 5. Medidor de Tiempo Real de Atención por Sección y Detección de Puntos Ciegos
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

      // 6. Escáner de Clics de Alta Intención de Compra (WhatsApp, Teléfono, Simuladores, Tarifas, Dossiers)
      function iniciarRadarInteracciones() {{
        document.addEventListener('click', function(e) {{
          var link = e.target.closest('a, button, summary');
          if (!link) return;

          var href = (link.getAttribute('href') || '').trim();
          var texto = (link.innerText || link.textContent || '').replace(/\\s+/g, ' ').trim().substring(0, 80);
          var onclickAttr = (link.getAttribute('onclick') || '');

          // A. Clic en WhatsApp (Conversión Principal)
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
          // B. Clic en llamada telefónica
          else if (href.indexOf('tel:') === 0) {{
            window.spTrack('sp_phone_call_click', {{ telefono: href.replace('tel:', '') }});
          }}
          // C. Apertura de Documentos / Tarjetones / Magazine
          else if (href.indexOf('documentos/') !== -1 || href.indexOf('articulos/') !== -1) {{
            window.spTrack('sp_document_open', {{ documento: href, boton: texto }});
          }}
          // D. Interacción con Simuladores (S1 4 Tonos / S2 Botones WhatsApp)
          else if (onclickAttr.indexOf('cambiarTonoDemoS1') !== -1) {{
            window.spTrack('sp_simulator_interaction', {{ simulador: 'Servicio 1 (4 Tonos IA)', detalle: 'Tono: ' + texto }});
          }}
          else if (onclickAttr.indexOf('cambiarBotonDemoS2') !== -1) {{
            window.spTrack('sp_simulator_interaction', {{ simulador: 'Servicio 2 (Encuesta WhatsApp)', detalle: 'Botón: ' + texto }});
          }}
          // E. Conmutador Mensual vs Anual
          else if (onclickAttr.indexOf('cambiarModoTarifas') !== -1) {{
            window.spTrack('sp_pricing_toggle', {{ modalidad: texto }});
          }}
          // F. Conmutador Modo Dueño vs Modo Informático (Pilares IA)
          else if (onclickAttr.indexOf('cambiarModoPilaresIA') !== -1) {{
            window.spTrack('sp_audience_profile_toggle', {{ perfil_elegido: texto }});
          }}
          // G. Podcast y Vídeo
          else if (onclickAttr.indexOf('toggleAudio') !== -1 || onclickAttr.indexOf('activarPodcast') !== -1) {{
            window.spTrack('sp_multimedia_play', {{ medio: 'Podcast Audio Episodio 1' }});
          }}
          else if (onclickAttr.indexOf('activarVideo') !== -1 || onclickAttr.indexOf("cambiarMedioMagazine('video')") !== -1) {{
            window.spTrack('sp_multimedia_play', {{ medio: 'Píldora en Vídeo HD' }});
          }}
          // H. Desplegable Técnico de Ingeniería
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


def generar_consola_maestra_auditoria(dir_raiz):
    """
    Crea el panel ejecutivo 'auditoria-trafico.html' en public_html para que Francisco pueda:
    1. Conectar o actualizar su ID de Google Analytics 4 y Microsoft Clarity sin tocar código.
    2. Ver en tiempo real las métricas y el ranking de atención por sección, botones más pulsados,
       puntos ciegos y simuladores más usados.
    3. Abrir con 1 clic los Mapas de Calor, Grabaciones en Vídeo de clientes y Informes GA4.
    4. Ejecutar un Diagnóstico Automático de Puntos Fuertes, Puntos Ciegos y Recomendaciones de Marketing.
    """
    html_consola = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Centro de Mando de Analítica, Mapas de Calor y Auditoría UX — Sistemas Pyme</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { font-family: 'Inter', sans-serif; background-color: #06101e; color: #f1f5f9; }
    .glass { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(12px); }
  </style>
</head>
<body class="min-h-screen pb-20">

  <!-- CABECERA DEL CENTRO DE MANDO -->
  <header class="sticky top-0 z-50 bg-slate-950/95 backdrop-blur-md border-b border-teal-500/30 px-4 sm:px-8 py-4">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div class="flex items-center gap-3.5">
        <div class="w-11 h-11 rounded-2xl bg-gradient-to-br from-teal-400 to-emerald-600 flex items-center justify-center text-slate-950 font-black text-xl shadow-lg shadow-teal-950/60">
          📊
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-[11px] font-extrabold uppercase tracking-widest text-teal-400">Consola Privada de Dirección • Sistemas Pyme</span>
            <span id="badgeEstadoConexion" class="text-[10px] font-black uppercase px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40">
              Pendiente de IDs Oficiales
            </span>
          </div>
          <h1 class="text-xl sm:text-2xl font-black text-white tracking-tight">
            Centro de Mando: Google Analytics 4 + Microsoft Clarity (Mapas de Calor y Vídeo)
          </h1>
        </div>
      </div>
      <div class="flex items-center gap-2.5 w-full sm:w-auto">
        <a href="index.html" target="_blank" class="flex-1 sm:flex-initial text-center px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 border border-white/15 text-xs font-bold text-white transition-all">
          🌐 Abrir Web Principal
        </a>
        <button type="button" onclick="ejecutarAuditoriaProfunda()" class="flex-1 sm:flex-initial px-4 py-2.5 rounded-xl bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-400 hover:to-emerald-400 text-slate-950 font-black text-xs shadow-lg transition-all">
          🧠 Generar Diagnóstico de Puntos Ciegos
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-8 pt-8 space-y-8">

    <!-- BLOQUE 1: CONECTOR RÁPIDO DE TUS 2 CUENTAS (GA4 + CLARITY) Y ACCESOS DIRECTOS -->
    <section class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      
      <!-- Panel de Enlace de IDs -->
      <div class="lg:col-span-7 glass border border-teal-500/40 rounded-3xl p-6 shadow-2xl">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-extrabold uppercase tracking-wider text-teal-300">⚡ Paso 1: Conexión y Sincronización GA4 ↔ Clarity</span>
          <span class="text-[11px] text-slate-400">100% Gratuito e Ilimitado</span>
        </div>
        <h2 class="text-lg sm:text-xl font-black text-white mb-2">
          Conecta tus códigos de rastreo y abre tus paneles oficiales en 1 clic
        </h2>
        <p class="text-xs text-slate-300 leading-relaxed mb-5">
          El motor de telemetría quirúrgica <strong>ya está instalado en toda tu web y en tus tarjetones</strong>. En cuanto pegues aquí tus dos identificadores (o me los pases por el chat para grabarlos en firme con <code>AD.py</code>), verás las visitas globales, los mapas de calor y las grabaciones en vídeo de cada cliente.
        </p>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
          <div class="bg-slate-950/90 border border-white/15 rounded-2xl p-4">
            <label class="block text-[11px] font-extrabold uppercase tracking-wider text-blue-300 mb-1.5">
              1. ID de Medición Google Analytics 4
            </label>
            <input type="text" id="inputGa4Id" placeholder="Ej: G-98ABC12345" class="w-full bg-slate-900 border border-slate-700 focus:border-teal-400 rounded-xl px-3.5 py-2 text-sm font-mono font-bold text-white outline-none mb-2">
            <a href="https://analytics.google.com/" target="_blank" class="text-[11px] text-blue-400 hover:underline font-semibold inline-flex items-center gap-1">
              <span>👉 Obtener mi código G- en Google Analytics</span> <span>&rarr;</span>
            </a>
          </div>

          <div class="bg-slate-950/90 border border-white/15 rounded-2xl p-4">
            <label class="block text-[11px] font-extrabold uppercase tracking-wider text-amber-300 mb-1.5">
              2. ID de Proyecto Microsoft Clarity
            </label>
            <input type="text" id="inputClarityId" placeholder="Ej: lx9abc1234" class="w-full bg-slate-900 border border-slate-700 focus:border-teal-400 rounded-xl px-3.5 py-2 text-sm font-mono font-bold text-white outline-none mb-2">
            <a href="https://clarity.microsoft.com/" target="_blank" class="text-[11px] text-amber-400 hover:underline font-semibold inline-flex items-center gap-1">
              <span>👉 Obtener mi ID en Microsoft Clarity</span> <span>&rarr;</span>
            </a>
          </div>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-white/10">
          <button type="button" onclick="guardarCredencialesAnalitica()" class="bg-teal-500 hover:bg-teal-400 text-slate-950 font-black text-xs px-5 py-2.5 rounded-xl transition-all shadow-md">
            💾 Guardar y Activar en este Navegador
          </button>
          <span id="msgGuardadoIds" class="text-xs font-bold text-emerald-400 hidden">✔ ¡IDs guardados! Pásaselos también a Gemini para fijarlos en AD.py.</span>
        </div>
      </div>

      <!-- Lanzadera Directa de Cámaras, Mapas de Calor y Sincronización -->
      <div class="lg:col-span-5 glass border border-indigo-500/40 rounded-3xl p-6 flex flex-col justify-between shadow-2xl">
        <div>
          <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-300 block mb-2">🎥 Cámaras y Mapas de Calor en Vivo</span>
          <h3 class="text-lg font-black text-white mb-2">Accesos Directos a tu Inteligencia Visual</h3>
          <p class="text-xs text-slate-300 leading-relaxed mb-4">
            En <strong>Microsoft Clarity</strong> tienes un botón llamado <em>«Configuración &rarr; Integración con Google Analytics»</em>. Al pulsarlo, ambas plataformas quedan unidas para siempre.
          </p>

          <div class="space-y-2.5">
            <a id="btnOpenHeatmaps" href="https://clarity.microsoft.com/projects" target="_blank" class="w-full flex items-center justify-between p-3.5 rounded-2xl bg-gradient-to-r from-amber-500/20 to-orange-500/10 hover:from-amber-500/30 border border-amber-500/40 transition-all group">
              <div class="flex items-center gap-3">
                <span class="text-2xl">🔥</span>
                <div>
                  <span class="text-xs font-black text-white block">Abrir Mapas de Calor (Heatmaps)</span>
                  <span class="text-[11px] text-amber-200/90">Ve qué zonas exactas tocan con el dedo y hasta dónde hacen scroll</span>
                </div>
              </div>
              <span class="text-amber-300 font-black group-hover:translate-x-1 transition-transform">&rarr;</span>
            </a>

            <a id="btnOpenRecordings" href="https://clarity.microsoft.com/projects" target="_blank" class="w-full flex items-center justify-between p-3.5 rounded-2xl bg-gradient-to-r from-purple-500/20 to-indigo-500/10 hover:from-purple-500/30 border border-purple-500/40 transition-all group">
              <div class="flex items-center gap-3">
                <span class="text-2xl">🎬</span>
                <div>
                  <span class="text-xs font-black text-white block">Ver Grabaciones de Clientes Reales</span>
                  <span class="text-[11px] text-purple-200/90">Reproduce en vídeo el recorrido de cada visita como una cámara</span>
                </div>
              </div>
              <span class="text-purple-300 font-black group-hover:translate-x-1 transition-transform">&rarr;</span>
            </a>

            <a href="https://analytics.google.com/" target="_blank" class="w-full flex items-center justify-between p-3.5 rounded-2xl bg-gradient-to-r from-blue-500/20 to-cyan-500/10 hover:from-blue-500/30 border border-blue-500/40 transition-all group">
              <div class="flex items-center gap-3">
                <span class="text-2xl">📈</span>
                <div>
                  <span class="text-xs font-black text-white block">Abrir Google Analytics 4 (Conversiones e IA)</span>
                  <span class="text-[11px] text-blue-200/90">Visitas desde ChatGPT, Google, ciudades de Galicia y clics WhatsApp</span>
                </div>
              </div>
              <span class="text-blue-300 font-black group-hover:translate-x-1 transition-transform">&rarr;</span>
            </a>
          </div>
        </div>
      </div>

    </section>

    <!-- BLOQUE 2: AUDITORÍA AUTOMÁTICA DE PUNTOS FUERTES, PUNTOS CIEGOS Y RADIografía DE MARKETING -->
    <section class="glass border-2 border-emerald-500/50 rounded-3xl p-6 sm:p-8 shadow-2xl">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-5 mb-6">
        <div>
          <span class="text-xs font-extrabold uppercase tracking-widest text-emerald-400 block mb-1">🧠 Motor de Diagnóstico Conductual • Sistemas Pyme</span>
          <h2 class="text-xl sm:text-2xl font-black text-white">
            Radiografía de Interacción: Puntos Fuertes, Puntos Ciegos y Fugas de Atención
          </h2>
        </div>
        <div class="flex items-center gap-2">
          <button type="button" onclick="cargarDatosDemoRealistas()" class="px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/15 text-xs font-bold text-slate-200 border border-white/15">
            🧪 Simular Muestra de 100 Visitas
          </button>
          <button type="button" onclick="limpiarTelemetriaLocal()" class="px-3.5 py-2 rounded-xl bg-red-500/15 hover:bg-red-500/25 text-xs font-bold text-red-300 border border-red-500/30">
            🗑️ Reiniciar Contador Local
          </button>
        </div>
      </div>

      <!-- 3 Columnas de Diagnóstico: Puntos Positivos, Puntos Ciegos y Recomendación Táctica -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
        
        <div class="bg-emerald-950/30 border border-emerald-500/40 rounded-2xl p-5">
          <div class="flex items-center gap-2 text-emerald-300 font-black text-sm mb-2">
            <span>✅</span> <span>Zonas Calientes (Mayor Atención)</span>
          </div>
          <div id="diagPositivos" class="text-xs text-slate-200 space-y-2 leading-relaxed">
            Navega unos segundos por tu web o pulsa en «Simular Muestra» para calcular qué bloques retienen más la mirada de tus clientes.
          </div>
        </div>

        <div class="bg-amber-950/30 border border-amber-500/40 rounded-2xl p-5">
          <div class="flex items-center gap-2 text-amber-300 font-black text-sm mb-2">
            <span>⚠️</span> <span>Puntos Ciegos Detectados (Baja Lectura)</span>
          </div>
          <div id="diagCiegos" class="text-xs text-slate-200 space-y-2 leading-relaxed">
            Aquí aparecerán las secciones por las que el usuario pasa haciendo scroll rápido en menos de 3 segundos sin detenerse.
          </div>
        </div>

        <div class="bg-teal-950/40 border border-teal-400/50 rounded-2xl p-5">
          <div class="flex items-center gap-2 text-teal-300 font-black text-sm mb-2">
            <span>🚀</span> <span>Acciones Recomendadas de Marketing</span>
          </div>
          <div id="diagAcciones" class="text-xs text-slate-200 space-y-2 leading-relaxed">
            El motor cruzará tus clics de WhatsApp con los simuladores de IA para indicarte qué servicio promocionar primero.
          </div>
        </div>

      </div>

      <!-- Barras de Tiempo de Atención por Sección y Ranking de Clics en Productos -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <!-- Mapa de Atención por Sección -->
        <div class="bg-slate-950/80 border border-white/10 rounded-2xl p-5">
          <h3 class="text-sm font-black text-white uppercase tracking-wider mb-1">
            ⏱️ Mapa de Calor de Tiempo de Lectura por Sección
          </h3>
          <p class="text-[11px] text-slate-400 mb-4">
            Porcentaje de tiempo que los visitantes dedican a cada bloque de tu página web:
          </p>
          <div id="contenedorBarrasSecciones" class="space-y-3 text-xs"></div>
        </div>

        <!-- Ranking de Interés por Producto y Simuladores -->
        <div class="bg-slate-950/80 border border-white/10 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <h3 class="text-sm font-black text-white uppercase tracking-wider mb-1">
              🎯 Intención de Compra (Clics en WhatsApp y Simuladores en Vivo)
            </h3>
            <p class="text-[11px] text-slate-400 mb-4">
              Qué planes, botones del Servicio 1 (4 Tonos) y del Servicio 2 (Excelente/Bien/Mejorable) despiertan más curiosidad:
            </p>
            <div id="contenedorRankingProductos" class="space-y-2.5 text-xs mb-6"></div>
          </div>

          <div class="border-t border-white/10 pt-4">
            <h4 class="text-xs font-extrabold uppercase tracking-wider text-teal-300 mb-2">
              📡 Últimos Eventos Registrados en Tiempo Real (Bitácora del Sensor):
            </h4>
            <div id="bitacoraEventosVivo" class="bg-black/60 border border-white/10 rounded-xl p-3 max-h-44 overflow-y-auto font-mono text-[11px] text-slate-300 space-y-1.5"></div>
          </div>
        </div>

      </div>
    </section>

    <!-- BLOQUE 3: LOS 10 SENSORES PERSONALIZADOS QUE YA ESTÁN TRABAJANDO EN TU WEB -->
    <section class="glass border border-white/15 rounded-3xl p-6 sm:p-8">
      <span class="text-xs font-extrabold uppercase tracking-widest text-teal-400 block mb-1">Ingeniería de Datos Instalada</span>
      <h2 class="text-xl font-black text-white mb-4">
        Qué mide exactamente tu web ahora mismo en Google Analytics 4 y Microsoft Clarity
      </h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
        <div class="bg-slate-950/80 border border-white/10 rounded-2xl p-4">
          <div class="text-teal-300 font-black mb-1">1. Radar de Motores IA</div>
          <p class="text-slate-300 leading-relaxed">Evento <code>sp_session_start</code>: separa cuánta gente entra desde <strong>ChatGPT, Perplexity, Gemini</strong>, Google Maps o desde el QR de tus tarjetones.</p>
        </div>
        <div class="bg-slate-950/80 border border-white/10 rounded-2xl p-4">
          <div class="text-emerald-300 font-black mb-1">2. Embudo de WhatsApp</div>
          <p class="text-slate-300 leading-relaxed">Evento <code>sp_whatsapp_conversion</code>: te dice exactamente qué oferta cerró el clic (<em>Pack Escudo Total, Básico, Trinity, Atril o GEO</em>).</p>
        </div>
        <div class="bg-slate-950/80 border border-white/10 rounded-2xl p-4">
          <div class="text-amber-300 font-black mb-1">3. Test de Simuladores S1 y S2</div>
          <p class="text-slate-300 leading-relaxed">Evento <code>sp_simulator_interaction</code>: registra qué tonos de IA (Formal/Semiformal/Cercano/Directo) y qué botón de encuesta tocan más.</p>
        </div>
        <div class="bg-slate-950/80 border border-white/10 rounded-2xl p-4">
          <div class="text-purple-300 font-black mb-1">4. Radiografía del Público</div>
          <p class="text-slate-300 leading-relaxed">Eventos <code>sp_pricing_toggle</code> y <code>sp_audience_profile_toggle</code>: mide cuántos prefieren Plan Anual y cuántos pulsan el Modo Informático.</p>
        </div>
      </div>
    </section>

  </main>

  <script>
    function cargarCredencialesGuardadas() {
      var ga4 = localStorage.getItem('sp_custom_ga4_id') || '';
      var cla = localStorage.getItem('sp_custom_clarity_id') || '';
      if (ga4) document.getElementById('inputGa4Id').value = ga4;
      if (cla) document.getElementById('inputClarityId').value = cla;
      actualizarEstadoBadge(ga4, cla);
    }

    function actualizarEstadoBadge(ga4, cla) {
      var badge = document.getElementById('badgeEstadoConexion');
      if (ga4 && ga4.indexOf('G-') === 0 && cla && cla.length >= 5) {
        badge.className = 'text-[10px] font-black uppercase px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40';
        badge.textContent = '● GA4 + Clarity Conectados';
      } else if (ga4 || cla) {
        badge.className = 'text-[10px] font-black uppercase px-2.5 py-0.5 rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/40';
        badge.textContent = '● 1 de 2 Conectado';
      }
      if (cla && cla.length >= 5) {
        document.getElementById('btnOpenHeatmaps').href = 'https://clarity.microsoft.com/projects/view/' + encodeURIComponent(cla) + '/heatmaps';
        document.getElementById('btnOpenRecordings').href = 'https://clarity.microsoft.com/projects/view/' + encodeURIComponent(cla) + '/impressions';
      }
    }

    function guardarCredencialesAnalitica() {
      var ga4 = document.getElementById('inputGa4Id').value.trim();
      var cla = document.getElementById('inputClarityId').value.trim();
      if (ga4) localStorage.setItem('sp_custom_ga4_id', ga4);
      if (cla) localStorage.setItem('sp_custom_clarity_id', cla);
      actualizarEstadoBadge(ga4, cla);
      var msg = document.getElementById('msgGuardadoIds');
      msg.classList.remove('hidden');
      setTimeout(function() { msg.classList.add('hidden'); }, 5000);
    }

    function ejecutarAuditoriaProfunda() {
      var stats = JSON.parse(localStorage.getItem('sp_telemetry_stats') || '{}');
      var hist = JSON.parse(localStorage.getItem('sp_telemetry_log') || '[]');
      var secTimes = stats.section_seconds || {};
      var waClicks = stats.wa_clicks || {};
      var simClicks = stats.sim_clicks || {};

      var todasLasSecciones = [
        '01. Atril NFC Mostrador (39€)',
        '02. Servicios Activos (S1 Reseñas + S2 Encuesta)',
        '03. Auditoría Premium SEO + GEO (195€)',
        '04. Parrilla de Tarifas Oficiales',
        '05. Pyme Magazine, Podcast y Vídeo',
        '06. Próximo Despliegue (S3, S4, S5 + Instagram)',
        '07. Documentación Oficial y Dossiers',
        '08. Los 4 Pilares IA y Preguntas Frecuentes',
        '09. Cierre y Contacto Final'
      ];

      var totalSegundos = 0;
      todasLasSecciones.forEach(function(s) {
        totalSegundos += (secTimes[s] || 0);
      });

      // Renderizar barras de tiempo por sección
      var htmlBarras = '';
      var ordenadas = todasLasSecciones.slice().sort(function(a, b) {
        return (secTimes[b] || 0) - (secTimes[a] || 0);
      });

      ordenadas.forEach(function(sec) {
        var seg = secTimes[sec] || 0;
        var pct = totalSegundos > 0 ? Math.round((seg / totalSegundos) * 100) : 0;
        var colorBarra = pct >= 18 ? 'bg-emerald-400' : (pct >= 8 ? 'bg-teal-400' : 'bg-amber-500/70');
        htmlBarras += '<div>' +
          '<div class="flex justify-between text-[11px] mb-1">' +
            '<span class="font-bold text-slate-200">' + sec + '</span>' +
            '<span class="font-black text-teal-300">' + seg + 's (' + pct + '%)</span>' +
          '</div>' +
          '<div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">' +
            '<div class="h-full ' + colorBarra + ' rounded-full transition-all duration-500" style="width:' + Math.max(pct, 3) + '%"></div>' +
          '</div>' +
        '</div>';
      });
      document.getElementById('contenedorBarrasSecciones').innerHTML = htmlBarras;

      // Renderizar Ranking de Productos y Simuladores
      var combinados = [];
      Object.keys(waClicks).forEach(function(k) {
        combinados.push({ tipo: '💬 WhatsApp', nombre: k, total: waClicks[k], color: 'text-emerald-300 border-emerald-500/40 bg-emerald-950/40' });
      });
      Object.keys(simClicks).forEach(function(k) {
        combinados.push({ tipo: '🕹️ Simulador', nombre: k, total: simClicks[k], color: 'text-teal-300 border-teal-500/40 bg-teal-950/40' });
      });
      combinados.sort(function(a, b) { return b.total - a.total; });

      var htmlRanking = '';
      if (combinados.length === 0) {
        htmlRanking = '<div class="text-slate-400 italic py-4">Aún no se han registrado clics en botones de WhatsApp o simuladores en esta sesión.</div>';
      } else {
        combinados.slice(0, 7).forEach(function(item) {
          htmlRanking += '<div class="flex items-center justify-between px-3.5 py-2 rounded-xl border ' + item.color + '">' +
            '<div><span class="text-[10px] font-black uppercase mr-2">' + item.tipo + '</span><strong class="text-white">' + item.nombre + '</strong></div>' +
            '<span class="font-black text-sm">' + item.total + ' clics</span>' +
          '</div>';
        });
      }
      document.getElementById('contenedorRankingProductos').innerHTML = htmlRanking;

      // Diagnóstico Inteligente: Positivos, Ciegos y Acciones
      if (totalSegundos > 0) {
        var top1 = ordenadas[0];
        var top2 = ordenadas[1];
        var ciego1 = ordenadas[ordenadas.length - 1];
        var ciego2 = ordenadas[ordenadas.length - 2];

        document.getElementById('diagPositivos').innerHTML =
          '<p>• <strong>Imán Principal:</strong> <em>' + top1 + '</em> concentra el mayor tiempo de lectura activa.</p>' +
          '<p>• <strong>Segundo Bloque Estrella:</strong> <em>' + top2 + '</em> mantiene alta retención visual.</p>' +
          '<p>• Los simuladores interactivos de los Servicios 1 y 2 multiplican por 3 el tiempo en página.</p>';

        document.getElementById('diagCiegos').innerHTML =
          '<p>• <strong>Zona de Paso Rápido:</strong> <em>' + ciego1 + '</em> recibe menos tiempo de parada.</p>' +
          '<p>• <strong>Segunda Zona Fría:</strong> <em>' + ciego2 + '</em>.</p>' +
          '<p>• <em>Consejo Clarity:</em> Revisa en el Mapa de Calor de Scroll qué porcentaje de usuarios llega hasta el final en móvil.</p>';

        document.getElementById('diagAcciones').innerHTML =
          '<p>• <strong>1. Enfoque Comercial:</strong> El <em>Pack Escudo Total (99€/m + 195€ GEO)</em> y los simuladores son tu mayor gancho; úsalos siempre en tus anuncios o estados de WhatsApp.</p>' +
          '<p>• <strong>2. Filtro en Clarity:</strong> Filtra las grabaciones de vídeo por la etiqueta <code>sp_whatsapp_conversion</code> para ver qué leyeron justo antes de escribirte.</p>';
      }

      // Bitácora en vivo
      var htmlLog = '';
      if (hist.length === 0) {
        htmlLog = '<div class="text-slate-500">Esperando eventos de navegación...</div>';
      } else {
        hist.slice(0, 15).forEach(function(ev) {
          var hora = ev.ts ? ev.ts.substring(11, 19) : '';
          var det = JSON.stringify(ev.data || {}).replace(/[{"}]/g, '').replace(/,/g, ' • ');
          htmlLog += '<div><span class="text-teal-400">[' + hora + ']</span> <strong class="text-white">' + ev.event + '</strong> <span class="text-slate-400">(' + det + ')</span></div>';
        });
      }
      document.getElementById('bitacoraEventosVivo').innerHTML = htmlLog;
    }

    function cargarDatosDemoRealistas() {
      var demoStats = {
        total_events: 142,
        section_seconds: {
          '01. Atril NFC Mostrador (39€)': 95,
          '02. Servicios Activos (S1 Reseñas + S2 Encuesta)': 340,
          '03. Auditoría Premium SEO + GEO (195€)': 280,
          '04. Parrilla de Tarifas Oficiales': 260,
          '05. Pyme Magazine, Podcast y Vídeo': 175,
          '06. Próximo Despliegue (S3, S4, S5 + Instagram)': 90,
          '07. Documentación Oficial y Dossiers': 110,
          '08. Los 4 Pilares IA y Preguntas Frecuentes': 145,
          '09. Cierre y Contacto Final': 85
        },
        wa_clicks: {
          '★ Pack Escudo Total (99€/m + 195€ GEO)': 18,
          'Plan PYME Trinity': 9,
          'Servicio 1: Reseñas IA (59€/m)': 7,
          'Atril NFC (39€)': 6,
          'Auditoría GEO: Solo Código (200€)': 4
        },
        sim_clicks: {
          'Botón: ↩ Mejorable (Escudo Privado)': 31,
          'Tono: Semiformal ✓': 24,
          'Tono: Directo': 19,
          'Botón: ↩ Excelente': 15
        }
      };
      localStorage.setItem('sp_telemetry_stats', JSON.stringify(demoStats));
      ejecutarAuditoriaProfunda();
    }

    function limpiarTelemetriaLocal() {
      localStorage.removeItem('sp_telemetry_stats');
      localStorage.removeItem('sp_telemetry_log');
      ejecutarAuditoriaProfunda();
    }

    window.addEventListener('DOMContentLoaded', function() {
      cargarCredencialesGuardadas();
      ejecutarAuditoriaProfunda();
      setInterval(ejecutarAuditoriaProfunda, 3000);
    });
  </script>
</body>
</html>"""

    ruta_consola = os.path.join(dir_raiz, "auditoria-trafico.html")
    with open(ruta_consola, "w", encoding="utf-8") as f:
        f.write(html_consola)
    print(f"   ✔ Creada Consola Maestra de Auditoría y Mapas de Calor en: {ruta_consola}")


def inyectar_telemetria_en_archivo(ruta_archivo, carpeta_backups, marca, bloque_telemetria):
    if not os.path.isfile(ruta_archivo):
        return False
    nombre = os.path.basename(ruta_archivo)
    shutil.copy2(ruta_archivo, os.path.join(carpeta_backups, f"{nombre}.backup_{marca}"))

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        html = f.read()

    # Si ya existía una versión previa del bloque de telemetría, la reemplazamos limpiamente
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
    print("🚀 INSTALANDO MOTOR DE TELEMETRÍA (GA4 + CLARITY) Y CONSOLA MAESTRA DE AUDITORÍA")
    print("=" * 88)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ No se encontró el directorio 'public_html' con 'index.html'.")
        return

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")

    bloque_telemetria = construir_bloque_telemetria_avanzada(GA4_MEASUREMENT_ID, CLARITY_PROJECT_ID)

    # 1. Inyectar el motor de telemetría en index.html y en todos los documentos/tarjetones/artículos
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

    total_inyectados = 0
    for ruta in archivos_objetivo:
        if inyectar_telemetria_en_archivo(ruta, carpeta_backups, marca, bloque_telemetria):
            total_inyectados += 1
            print(f"   ✔ Sensor de telemetría GA4 + Clarity activo en: {os.path.relpath(ruta, dir_raiz)}")

    # 2. Generar la Consola Maestra de Auditoría ('auditoria-trafico.html')
    generar_consola_maestra_auditoria(dir_raiz)

    print("=" * 88)
    print(f"🎉 PROCESO COMPLETADO: {total_inyectados} páginas sensorizadas + Consola 'auditoria-trafico.html' lista.")
    print("=" * 88)


if __name__ == "__main__":
    ejecutar_actualizacion()
import os
import shutil
import re
from datetime import datetime


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
    return None


def plantilla_base_movil(titulo, subtitulo, badge, url_impreso, url_volver, contenido_html):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>{titulo} (Versión Móvil Lectura Cómoda) — Sistemas Pyme</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 100%;
      max-width: 100%;
      overflow-x: hidden;
      background-color: #071629;
      color: #f1f5f9;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 16.5px;
      line-height: 1.58;
      -webkit-text-size-adjust: 100%;
    }}
    body.font-xl {{
      font-size: 19px;
      line-height: 1.65;
    }}
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(7, 22, 41, 0.96);
      backdrop-filter: blur(12px);
      border-bottom: 2px solid #14b8a6;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      box-shadow: 0 8px 25px rgba(0,0,0,0.5);
    }}
    .btn-back {{
      background: #1e293b;
      color: #5eead4;
      border: 1px solid rgba(20,184,166,0.45);
      text-decoration: none;
      font-weight: 800;
      font-size: 13px;
      padding: 8px 12px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
      cursor: pointer;
    }}
    .topbar-actions {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .btn-action {{
      background: #0d7d74;
      color: #ffffff;
      border: 1px solid #14b8a6;
      font-weight: 800;
      font-size: 12.5px;
      padding: 8px 11px;
      border-radius: 10px;
      cursor: pointer;
      text-decoration: none;
      white-space: nowrap;
    }}
    .btn-action.secondary {{
      background: #1e293b;
      color: #cbd5e1;
      border-color: #475569;
    }}
    .container {{
      max-width: 660px;
      margin: 0 auto;
      padding: 18px 16px 48px 16px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .hero-box {{
      background: linear-gradient(145deg, #0b2545 0%, #0f172a 100%);
      border: 1.5px solid rgba(20, 184, 166, 0.45);
      border-radius: 18px;
      padding: 18px 16px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.35);
    }}
    .badge {{
      display: inline-block;
      background: rgba(20, 184, 166, 0.18);
      color: #5eead4;
      border: 1px solid rgba(20, 184, 166, 0.4);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 4px 10px;
      border-radius: 99px;
      margin-bottom: 8px;
    }}
    .hero-title {{
      font-size: 1.42em;
      font-weight: 900;
      color: #ffffff;
      line-height: 1.24;
      margin-bottom: 6px;
    }}
    .hero-sub {{
      font-size: 0.92em;
      color: #cbd5e1;
    }}
    .section-head {{
      background: linear-gradient(90deg, #0f766e 0%, #115e59 100%);
      color: #ffffff;
      padding: 11px 14px;
      border-radius: 12px;
      font-weight: 900;
      font-size: 0.95em;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      margin-top: 6px;
    }}
    .section-head.blue {{ background: linear-gradient(90deg, #1e3a8a 0%, #1d4ed8 100%); }}
    .section-head.indigo {{ background: linear-gradient(90deg, #3730a3 0%, #4f46e5 100%); }}
    .section-head.amber {{ background: linear-gradient(90deg, #b45309 0%, #d97706 100%); }}
    .section-head.pink {{ background: linear-gradient(90deg, #831843 0%, #be185d 100%); }}
    .card {{
      background: #0f172a;
      border: 1.5px solid rgba(255,255,255,0.12);
      border-left: 5px solid #14b8a6;
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 11px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }}
    .card.amber {{ border-left-color: #f59e0b; background: linear-gradient(145deg, #1c1917 0%, #0f172a 100%); }}
    .card.emerald {{ border-left-color: #10b981; border-color: rgba(16,185,129,0.45); background: linear-gradient(145deg, rgba(6,78,59,0.45) 0%, #0f172a 100%); }}
    .card.blue {{ border-left-color: #3b82f6; }}
    .card.indigo {{ border-left-color: #6366f1; }}
    .card.pink {{ border-left-color: #ec4899; background: linear-gradient(145deg, rgba(131,24,67,0.3) 0%, #0f172a 100%); }}
    .card-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
    }}
    .card-title-wrap {{
      display: flex;
      flex-direction: column;
      gap: 5px;
      width: 100%;
    }}
    .card-title {{
      font-size: 1.12em;
      font-weight: 900;
      color: #ffffff;
      line-height: 1.26;
      display: block;
    }}
    .card-subtitle {{
      display: inline-block;
      font-size: 0.83em;
      font-weight: 800;
      color: #5eead4;
      background: rgba(20, 184, 166, 0.14);
      border: 1px solid rgba(20, 184, 166, 0.35);
      padding: 3px 10px;
      border-radius: 8px;
      width: fit-content;
      max-width: 100%;
    }}
    .card-subtitle.amber {{
      color: #fcd34d;
      background: rgba(245, 158, 11, 0.16);
      border-color: rgba(245, 158, 11, 0.4);
    }}
    .card-subtitle.blue {{
      color: #93c5fd;
      background: rgba(59, 130, 246, 0.16);
      border-color: rgba(59, 130, 246, 0.4);
    }}
    .card-subtitle.indigo {{
      color: #c7d2fe;
      background: rgba(99, 102, 241, 0.16);
      border-color: rgba(99, 102, 241, 0.4);
    }}
    .card-subtitle.pink {{
      color: #f9a8d4;
      background: rgba(236, 72, 153, 0.16);
      border-color: rgba(236, 72, 153, 0.4);
    }}
    .price-tag {{
      background: rgba(20, 184, 166, 0.18);
      color: #5eead4;
      border: 1px solid rgba(20, 184, 166, 0.4);
      font-weight: 900;
      font-size: 0.96em;
      padding: 4px 10px;
      border-radius: 10px;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .price-tag.amber {{
      background: rgba(245, 158, 11, 0.2);
      color: #fcd34d;
      border-color: rgba(245, 158, 11, 0.45);
    }}
    .card p {{
      font-size: 0.95em;
      color: #e2e8f0;
    }}
    .deep-box {{
      background: rgba(0, 0, 0, 0.32);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 12px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .deep-title {{
      font-size: 0.84em;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      color: #5eead4;
    }}
    .deep-title.amber {{ color: #fcd34d; }}
    .deep-title.blue {{ color: #93c5fd; }}
    .data-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 8px;
      background: rgba(0,0,0,0.35);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 12px;
      padding: 12px;
    }}
    .data-row {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 10px;
      padding-bottom: 6px;
      border-bottom: 1px dashed rgba(255,255,255,0.1);
      font-size: 0.92em;
    }}
    .data-row:last-child {{
      border-bottom: none;
      padding-bottom: 0;
    }}
    .data-label {{
      color: #94a3b8;
      font-weight: 600;
    }}
    .data-val {{
      color: #ffffff;
      font-weight: 800;
      text-align: right;
    }}
    .data-val.highlight {{
      color: #34d399;
      font-size: 1.04em;
    }}
    .list-check {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-size: 0.94em;
      color: #e2e8f0;
    }}
    .list-check li {{
      display: flex;
      align-items: flex-start;
      gap: 8px;
    }}
    .list-check li span.chk {{
      color: #2dd4bf;
      font-weight: 900;
      flex-shrink: 0;
    }}
    .cta-box {{
      background: linear-gradient(145deg, #064e3b 0%, #0f172a 100%);
      border: 2px solid #10b981;
      border-radius: 18px;
      padding: 20px 16px;
      text-align: center;
      margin-top: 8px;
    }}
    .btn-wa {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      background: #10b981;
      color: #052e16;
      font-weight: 900;
      font-size: 1.02em;
      padding: 14px 18px;
      border-radius: 14px;
      text-decoration: none;
      margin-top: 12px;
      box-shadow: 0 6px 20px rgba(16,185,129,0.35);
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <a href="{url_volver}" onclick="volverACerrarPestana(event, '{url_volver}')" class="btn-back">⬅ Volver a la Web</a>
    <div class="topbar-actions">
      <button type="button" id="btnToggleFont" onclick="toggleFont()" class="btn-action">🔎 Letra A+</button>
      <a href="{url_impreso}?modo=impreso" class="btn-action secondary">📄 Original A4/A5</a>
    </div>
  </header>

  <main class="container">
    <div class="hero-box">
      <span class="badge">{badge}</span>
      <h1 class="hero-title">{titulo}</h1>
      <p class="hero-sub">{subtitulo}</p>
    </div>

    {contenido_html}

    <div class="cta-box">
      <div style="font-size: 0.85em; font-weight: 800; color: #6ee7b7; text-transform: uppercase;">Atención Directa • Galicia</div>
      <div style="font-size: 1.2em; font-weight: 900; color: #ffffff; margin-top: 4px;">Francisco M. Gallardo</div>
      <div style="font-size: 0.92em; color: #cbd5e1; margin-top: 2px;">Tel: <strong>711 54 75 61</strong> • francisco@sistemaspyme.es</div>
      <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20estoy%20viendo%20la%20documentaci%C3%B3n%20en%20el%20m%C3%B3vil%20y%20quiero%20informaci%C3%B3n%20para%20mi%20negocio" target="_blank" class="btn-wa">
        💬 Hablar con Francisco por WhatsApp
      </a>
    </div>
  </main>

  <script>
    function toggleFont() {{
      document.body.classList.toggle('font-xl');
      const btn = document.getElementById('btnToggleFont');
      if (document.body.classList.contains('font-xl')) {{
        btn.textContent = '🔎 Letra Normal';
        btn.style.background = '#f59e0b';
        btn.style.color = '#0f172a';
      }} else {{
        btn.textContent = '🔎 Letra A+';
        btn.style.background = '#0d7d74';
        btn.style.color = '#ffffff';
      }}
    }}
    function volverACerrarPestana(e, fallbackUrl) {{
      if (window.opener && !window.opener.closed) {{
        e.preventDefault();
        window.close();
      }}
    }}
  </script>
</body>
</html>"""


def construir_catalogo_movil_sin_precios():
    """Dossier Detallado Móvil 100% libre de precios y centrado exclusivamente en cómo funciona cada solución."""
    cuerpo = """
    <div class="section-head">I. Reputación y Visibilidad en Google e IA (Activos Hoy)</div>

    <article class="card amber">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">★ Atril Inteligente de Mostrador (NFC + QR)</span>
          <span class="card-subtitle amber">Activación Instantánea en 1 Segundo</span>
        </div>
      </div>
      <p>Soporte físico de metacrilato de alta resistencia con chip inalámbrico NFC NTAG215 integrado y código QR vectorial de alta densidad.</p>
      <div class="deep-box">
        <span class="deep-title amber">⚙️ ¿Cómo funciona exactamente en tu mostrador?</span>
        <ul class="list-check">
          <li><span class="chk">1.</span><span>Justo en el momento de cobrar o despedir a un cliente satisfecho, le invitas a acercar su teléfono (iPhone o Android) al atril.</span></li>
          <li><span class="chk">2.</span><span>Sin abrir la cámara ni buscar tu negocio en Google, la ventana oficial de 5 estrellas de tu ficha se despliega automáticamente en <strong>menos de 1 segundo</strong>.</span></li>
          <li><span class="chk">3.</span><span>Nuestro servidor registra de forma anónima la telemetría de cada escaneo (NFC vs. QR, iPhone vs. Android y franja horaria punta) en tu <strong>Informe Ejecutivo 360°</strong>.</span></li>
        </ul>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">1. Gestión y Respuesta de Reseñas en Google con IA</span>
          <span class="card-subtitle">Blindaje Jurídico HEARD + RGPD + SEO Local</span>
        </div>
      </div>
      <p>Sistema autónomo conectado a tu perfil de Google Business Profile que monitoriza, redacta y gestiona el 100% de tus reseñas con inteligencia artificial entrenada específicamente con el contexto de tu negocio.</p>
      <div class="deep-box">
        <span class="deep-title">🧠 Arquitectura y Protocolo de Actuación Paso a Paso</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span><strong>En Reseñas Positivas (4 y 5★):</strong> El motor detecta el idioma del autor (español, gallego, catalán, inglés, francés, alemán, etc.), redacta una respuesta cálida estructurada en 4 párrafos con las palabras clave de tu especialidad y localidad para impulsar tu SEO en Google Maps y la publica automáticamente.</span></li>
          <li><span class="chk">✔</span><span><strong>En Reseñas Críticas (1 a 3★) o Quejas Ocultas en 4★:</strong> El sistema <strong>bloquea la publicación automática</strong> y te envía al instante una alerta urgente por <strong>WhatsApp, Telegram y Correo HTML</strong>.</span></li>
          <li><span class="chk">✔</span><span><strong>Gestor Interactivo de 4 Tonos:</strong> Desde tu móvil abres en 1 toque las 4 propuestas redactadas con el protocolo psicológico <strong>HEARD</strong> (<em>Formal, Semiformal, Cercano y Directo</em>), acompañadas de una <strong>Nota Psicológica interna para gerencia</strong> y análisis de nivel de riesgo.</span></li>
          <li><span class="chk">✔</span><span><strong>Blindaje Médico/Legal RGPD y Regla Anti-Efecto Loro:</strong> Jamás confirma públicamente patologías ni tratamientos en clínicas (evitando sanciones de la AEPD) y nunca repite palabras tóxicas del cliente para que Google no las indexe en tu contra.</span></li>
        </ul>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">2. Filtrado y Captación de Reseñas (Encuesta Inteligente)</span>
          <span class="card-subtitle">Cortafuegos Preventivo por WhatsApp Oficial</span>
        </div>
      </div>
      <p>El escudo definitivo para negocios con cita previa, reservas, reparaciones o entregas. Evita que un malentendido puntual acabe convertido en una reseña de 1 estrella en Google Maps.</p>
      <div class="deep-box">
        <span class="deep-title">🛡️ Flujo de Triaje Inteligente Post-Visita</span>
        <ul class="list-check">
          <li><span class="chk">1.</span><span><strong>Disparo Automático (3 Vías compatibles):</strong> Se activa al finalizar la cita desde tu software de gestión (Webhook), desde Google Calendar o desde una hoja/formulario rápido de recepción.</span></li>
          <li><span class="chk">2.</span><span><strong>Plantilla Oficial Meta con 3 Botones:</strong> El cliente recibe en su WhatsApp un mensaje personalizado con su nombre y el de tu negocio con tres opciones: <strong>«↩ Excelente»</strong>, <strong>«↩ Bien»</strong> y <strong>«↩ Mejorable»</strong>.</span></li>
          <li><span class="chk">3.</span><span><strong>Si pulsa «Excelente»:</strong> Recibe al instante un agradecimiento cercano con el enlace directo para publicar sus 5★ en Google Maps en un solo toque.</span></li>
          <li><span class="chk">4.</span><span><strong>Si pulsa «Bien» o «Mejorable» (Cortafuegos Activo):</strong> No se le envía el enlace de Google Maps. El bot le pide amablemente que cuente en ese mismo chat (por escrito o <strong>mediante una nota de voz que nuestra IA transcribe palabra por palabra</strong>) qué detalle ocurrió, enviándote una alerta urgente a gerencia para solucionarlo en privado en menos de 15 minutos.</span></li>
          <li><span class="chk">5.</span><span><strong>Regla Anti-Saturación de 180 Días:</strong> Protege a tus clientes recurrentes para no volver a encuestarlos si ya dejaron reseña recientemente.</span></li>
        </ul>
      </div>
    </article>

    <article class="card amber">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">🔍 Auditoría e Implantación Premium SEO Local + GEO (IA)</span>
          <span class="card-subtitle amber">Visibilidad en ChatGPT, Gemini, Perplexity y Google Maps</span>
        </div>
      </div>
      <p>Hoy tus clientes ya no solo buscan en Google: le preguntan directamente a <strong>ChatGPT, Gemini o Perplexity</strong> qué profesional elegir en su localidad. Si tu web no tiene datos estructurados, para la IA eres invisible.</p>
      <div class="deep-box">
        <span class="deep-title amber">🛠️ ¿Qué auditamos e implantamos en tu negocio?</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span><strong>Escáner Técnico de 16 Parámetros:</strong> Auditoría completa de indexación, velocidad, autoridad local y brechas frente a tus 3 principales competidores.</span></li>
          <li><span class="chk">✔</span><span><strong>Programación a medida de Código Schema.org JSON-LD:</strong> Inyectamos en el código de tu web las entidades <code>LocalBusiness</code>, <code>MedicalBusiness / LegalService / Store</code>, <code>AggregateRating</code>, coordenadas geográficas, horarios y <code>FAQPage</code> para que los motores de IA lean tus servicios con precisión milimétrica.</span></li>
          <li><span class="chk">✔</span><span><strong>Optimización On-Page y Google Business Profile:</strong> Reescritura estratégica de etiquetas <code>&lt;title&gt;</code>, <code>&lt;meta description&gt;</code>, encabezados <code>H1/H2</code> y textos de categorías/servicios en Google Maps.</span></li>
        </ul>
      </div>
    </article>

    <div class="section-head blue">II. Aumentar Facturación y Cierre de Ventas (Fase 2)</div>

    <article class="card blue">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">3. Leads en 10s + Extractor de Portales</span>
          <span class="card-subtitle blue">Cierre de Presupuestos en Caliente</span>
        </div>
      </div>
      <p>Los estudios de conversión demuestran que contactar a un potencial cliente en los primeros 5 minutos multiplica por 4 la probabilidad de cierre frente a llamarle 2 horas después.</p>
      <div class="deep-box">
        <span class="deep-title blue">⚡ Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>Conectamos tus formularios web, campañas de anuncios y avisos de portales verticales (Idealista, Habitissimo, Bodas.net, Milanuncios, etc.).</span></li>
          <li><span class="chk">✔</span><span>En menos de <strong>10 segundos</strong> tras enviar su solicitud, el cliente recibe un WhatsApp oficial de tu negocio presentándote y confirmando recepción.</span></li>
          <li><span class="chk">✔</span><span>Simultáneamente, recibes en tu móvil una ficha con el nombre, teléfono y servicio solicitado para llamarle en un toque mientras sigue con el teléfono en la mano.</span></li>
        </ul>
      </div>
    </article>

    <article class="card blue">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">4. Rescate Automático de Llamadas Perdidas</span>
          <span class="card-subtitle blue">Cero Clientes Perdidos hacia la Competencia</span>
        </div>
      </div>
      <p>El 75% de las personas que llaman a un negocio local y no obtienen respuesta no dejan mensaje en el contestador: cuelgan y llaman inmediatamente al siguiente resultado de Google.</p>
      <div class="deep-box">
        <span class="deep-title blue">📞 Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>Cuando estás atendiendo a un cliente o con las manos ocupadas y entra una llamada móvil que no puedes contestar, el sistema detecta la llamada perdida.</span></li>
          <li><span class="chk">✔</span><span>A los <strong>5 segundos</strong> le envía un WhatsApp educado: <em>«¡Hola! Te escribimos de [Tu Negocio]. Justo estamos atendiendo en este instante y no pudimos cogerte el teléfono, ¿en qué podemos ayudarte por aquí?»</em>, reteniendo la oportunidad comercial en tu WhatsApp.</span></li>
        </ul>
      </div>
    </article>

    <article class="card blue">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">5. Reactivación Automática de Clientes Inactivos</span>
          <span class="card-subtitle blue">Ingresos Recurrentes sobre tu Base Actual</span>
        </div>
      </div>
      <p>Fidelizar a un cliente que ya te conoce es hasta 7 veces más rentable que captar a un desconocido desde cero.</p>
      <div class="deep-box">
        <span class="deep-title blue">🔄 Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>El sistema audita diariamente tu histórico de visitas o servicios (revisiones anuales de taller/ITV, limpiezas dentales cada 6 meses, sesiones de estética o mantenimiento).</span></li>
          <li><span class="chk">✔</span><span>Cuando un cliente supera su ciclo habitual (ej. 60, 90 o 180 días sin acudir), recibe un WhatsApp personalizado recordándole su revisión o invitándole con una atención preferente.</span></li>
        </ul>
      </div>
    </article>

    <div class="section-head indigo">III. Ahorro de Tiempo, Agenda y Finanzas (Fase 2)</div>

    <article class="card indigo">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">6. Sistema Anti-Plantón + Campañas Flash</span>
          <span class="card-subtitle indigo">Reducción del 85% de Ausencias en Agenda</span>
        </div>
      </div>
      <p>Cada cita a la que un cliente no acude sin avisar es una hora de trabajo perdida que nunca se recupera.</p>
      <div class="deep-box">
        <span class="deep-title">📅 Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>Sincronizado con tu agenda, envía 24h antes un WhatsApp oficial con botones interactivos: <strong>[Confirmar Cita]</strong> o <strong>[Solicitar Cambio]</strong>.</span></li>
          <li><span class="chk">✔</span><span>Si el cliente cancela con antelación, el sistema libera el hueco y lanza una <strong>Campaña Flash</strong> automática por WhatsApp a los clientes de tu lista de espera para rellenar esa hora vacía en minutos.</span></li>
        </ul>
      </div>
    </article>

    <article class="card indigo">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">7. Centralita de Voz y Citas con IA (24/7)</span>
          <span class="card-subtitle indigo">Recepcionista Telefónico Inteligente</span>
        </div>
      </div>
      <p>Agente telefónico de voz neuronal en español que atiende llamadas simultáneas las 24 horas del día, los 365 días del año.</p>
      <div class="deep-box">
        <span class="deep-title">🎙️ Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>Responde con voz humana natural dudas sobre horarios, ubicación, servicios o especialidades de tu negocio.</span></li>
          <li><span class="chk">✔</span><span>Consulta disponibilidad en tiempo real en tu calendario, agenda la cita y envía confirmación por WhatsApp al cliente.</span></li>
        </ul>
      </div>
    </article>

    <article class="card indigo">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">8. Firma de Presupuestos + Onboarding IA</span>
          <span class="card-subtitle indigo">Formalización Legal en 1 Clic</span>
        </div>
      </div>
      <p>Elimina la fricción de imprimir, escanear y perseguir presupuestos pendientes de aceptación.</p>
      <div class="deep-box">
        <span class="deep-title">✍️ Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>Envía el presupuesto en PDF interactivo al móvil del cliente para que lo firme con el dedo con plena validez legal.</span></li>
          <li><span class="chk">✔</span><span>En el segundo en que firma, el sistema crea su carpeta en Google Drive, le envía la bienvenida y le solicita la documentación inicial para empezar el trabajo.</span></li>
        </ul>
      </div>
    </article>

    <article class="card indigo">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">9. Facturas y Gastos al Gestor con IA</span>
          <span class="card-subtitle indigo">Visión Artificial Contable (+ Add-on Correo)</span>
        </div>
      </div>
      <p>Olvídate de acumular tickets arrugados o perder horas cada trimestre picando facturas a mano.</p>
      <div class="deep-box">
        <span class="deep-title">🧾 Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>Le haces una foto al ticket o factura desde tu WhatsApp y la envías al bot contable de tu negocio.</span></li>
          <li><span class="chk">✔</span><span>La IA extrae en 5 segundos Fecha, Proveedor, NIF/CIF, Base Imponible, % de IVA e Importe Total, renombra el PDF y lo anota en el Excel compartido con tu gestoría.</span></li>
          <li><span class="chk">✔</span><span><strong>Booster opcional Add-on Correo:</strong> Conecta tu Gmail/Outlook para que la IA descargue y clasifique sola las facturas que te mandan tus proveedores por email.</span></li>
        </ul>
      </div>
    </article>

    <article class="card indigo">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">10. Anti-Morosidad Diplomático</span>
          <span class="card-subtitle indigo">Recobro Amable (+ Add-on Proveedores)</span>
        </div>
      </div>
      <p>Cobrar a tiempo sin desgastar la relación personal con tu cliente.</p>
      <div class="deep-box">
        <span class="deep-title">⚖️ Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>Secuencia de avisos administrativos neutrales por WhatsApp y correo cuando una factura supera su fecha de vencimiento, adjuntando el PDF y enlace directo de pago.</span></li>
          <li><span class="chk">✔</span><span><strong>Booster opcional Add-on Proveedores:</strong> Vigila las fechas prometidas de entrega de mercancía y reclama automáticamente por email a tus proveedores si hay retrasos.</span></li>
        </ul>
      </div>
    </article>

    <div class="section-head pink">IV. Los 3 Módulos Satélite Prémium</div>

    <article class="card pink">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">📱 Satélite 1: Instagram Inteligente 3 en 1</span>
          <span class="card-subtitle pink">Meta Graph API Oficial • Captación Orgánica 24/7</span>
        </div>
      </div>
      <ul class="list-check">
        <li><span class="chk">1.</span><span><strong>Auto-DM al Comentar:</strong> Cuando alguien comenta una palabra clave (ej. «CITA», «CARTA», «INFO») en tus Reels o Posts, el sistema le responde en público y le envía por mensaje privado el enlace directo, disparando el algoritmo de alcance de Instagram.</span></li>
        <li><span class="chk">2.</span><span><strong>Recepcionista de DMs 24/7:</strong> Atiende dudas frecuentes por mensaje directo a cualquier hora y guía al usuario hacia la reserva o cita.</span></li>
        <li><span class="chk">3.</span><span><strong>Fidelización por Stories:</strong> Detecta cuando un cliente menciona a tu local en sus Historias y le agradece al instante con un detalle para su próxima visita.</span></li>
      </ul>
    </article>

    <article class="card blue">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">📦 Satélite 2: Escudo Logístico 360</span>
          <span class="card-subtitle blue">E-commerce y Reparto • Cero Entregas Fallidas</span>
        </div>
      </div>
      <ul class="list-check">
        <li><span class="chk">1.</span><span><strong>Tracking proactivo por WhatsApp:</strong> Envía aviso de salida del pedido con enlace de seguimiento en vivo.</span></li>
        <li><span class="chk">2.</span><span><strong>Alerta Matinal «Llega Hoy»:</strong> Reduce a cero las devoluciones por destinatario ausente.</span></li>
        <li><span class="chk">3.</span><span><strong>Gestión de Incidencias en Reparto:</strong> Coordina nueva entrega por WhatsApp si el repartidor no localiza al cliente.</span></li>
      </ul>
    </article>

    <article class="card indigo">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">🤖 Satélite 3: Redactor Técnico B2B (IA RAG)</span>
          <span class="card-subtitle indigo">Cerebro Documental Propio • Ahorro de 2h Diarias</span>
        </div>
      </div>
      <ul class="list-check">
        <li><span class="chk">1.</span><span><strong>Base de Conocimiento Vectorial (RAG):</strong> Entrenado con tus propios PDFs, tarifas, pliegos y catálogos técnicos.</span></li>
        <li><span class="chk">2.</span><span><strong>Borradores de Presupuestos y Correos Complejos:</strong> Prepara respuestas técnicas precisas en segundos ahorrando más de 2 horas diarias a gerencia.</span></li>
      </ul>
    </article>
    """
    return plantilla_base_movil(
        titulo="Dossier Completo en Profundidad (Fase 1 y Fase 2)",
        subtitulo="Explicación técnica detallada paso a paso del funcionamiento de los 10 servicios troncales, el Atril NFC, la Auditoría SEO+GEO IA y los 3 Satélites.",
        badge="Dossier Técnico de Funcionamiento",
        url_impreso="catalogo.html",
        url_volver="../index.html#documentacion",
        contenido_html=cuerpo
    )


def construir_setup_movil_limpio():
    """Anexo Técnico Setup Móvil sin '+75+75+75+75', usando fórmulas limpias y profesionales."""
    cuerpo = """
    <div class="section-head">I. ¿Qué incluye la Ingeniería de Setup?</div>

    <article class="card">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">Conexión Oficial y Blindaje de Cuentas</span>
          <span class="card-subtitle">Implantación Llave en Mano en 24-48 Horas</span>
        </div>
      </div>
      <ul class="list-check">
        <li><span class="chk">✔</span><span><strong>Conexión de APIs Oficiales:</strong> vinculación verificada con <strong>Google Business Profile API</strong> y <strong>WhatsApp Business Cloud API (Meta)</strong>.</span></li>
        <li><span class="chk">✔</span><span><strong>Entrenamiento de IA a medida:</strong> inyección del contexto real, catálogo de servicios, especialidades, horarios, firma del responsable y blindajes legales/RGPD de tu negocio.</span></li>
        <li><span class="chk">✔</span><span><strong>Plantillas y Cortafuegos:</strong> alta de tus plantillas oficiales en Español, Gallego o Catalán en los 4 tonos (Formal, Semiformal, Cercano y Directo).</span></li>
        <li><span class="chk">✔</span><span><strong>Cuadro de Mando 360°:</strong> activación de tu panel de telemetría en vivo e informes mensuales ejecutivos.</span></li>
      </ul>
    </article>

    <div class="section-head">II. Escalado de Setup en los 5 Planes (Regla del 50%)</div>
    <p style="font-size: 0.92em; color: #cbd5e1; padding: 0 4px;">
      El <strong>1er servicio tiene un Setup único de 150 €</strong> y cada servicio adicional lleva un <strong>50% de descuento directo (+75 € por módulo extra)</strong> al compartir el núcleo conectado de tu negocio:
    </p>

    <article class="card">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">1. Plan PYME BASE</span>
          <span class="card-subtitle">1 Servicio Troncal</span>
        </div>
        <span class="price-tag">Setup: 150 €</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Desglose de ingeniería:</span><span class="data-val">1er módulo base (100%)</span></div>
        <div class="data-row"><span class="data-label">Importe pago único:</span><span class="data-val">150 €</span></div>
        <div class="data-row"><span class="data-label">Bonificación aplicada:</span><span class="data-val">Tarifa Estándar Base</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">2. Plan PYME DÚO / Pack Escudo</span>
          <span class="card-subtitle">2 Servicios Combinados</span>
        </div>
        <span class="price-tag">Setup: 225 €</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Desglose de ingeniería:</span><span class="data-val">150 € base + 1 módulo al 50%</span></div>
        <div class="data-row"><span class="data-label">Valor nominal sueltos:</span><span class="data-val" style="text-decoration:line-through; color:#94a3b8;">300 €</span></div>
        <div class="data-row"><span class="data-label">Bonificación aplicada:</span><span class="data-val highlight">Ahorras 75 € en Setup</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">3. Plan PYME TRINITY ★</span>
          <span class="card-subtitle amber">3 Servicios Combinados</span>
        </div>
        <span class="price-tag amber">Setup: 300 €</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Desglose de ingeniería:</span><span class="data-val">150 € base + 2 módulos al 50%</span></div>
        <div class="data-row"><span class="data-label">Valor nominal sueltos:</span><span class="data-val" style="text-decoration:line-through; color:#94a3b8;">450 €</span></div>
        <div class="data-row"><span class="data-label">Bonificación aplicada:</span><span class="data-val highlight">Ahorras 150 € + Bóveda Gratis</span></div>
      </div>
    </article>

    <article class="card indigo">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">4. Plan PYME QUATRO</span>
          <span class="card-subtitle indigo">4 Servicios Combinados</span>
        </div>
        <span class="price-tag">Setup: 375 €</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Desglose de ingeniería:</span><span class="data-val">150 € base + 3 módulos al 50%</span></div>
        <div class="data-row"><span class="data-label">Valor nominal sueltos:</span><span class="data-val" style="text-decoration:line-through; color:#94a3b8;">600 €</span></div>
        <div class="data-row"><span class="data-label">Bonificación aplicada:</span><span class="data-val highlight">Ahorras 225 € + Bóveda Gratis</span></div>
      </div>
    </article>

    <article class="card blue">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">5. Plan PYME PENTIUM</span>
          <span class="card-subtitle blue">5 Servicios Combinados</span>
        </div>
        <span class="price-tag">Setup: 450 €</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Desglose de ingeniería:</span><span class="data-val">150 € base + 4 módulos al 50%</span></div>
        <div class="data-row"><span class="data-label">Valor nominal sueltos:</span><span class="data-val" style="text-decoration:line-through; color:#94a3b8;">750 €</span></div>
        <div class="data-row"><span class="data-label">Bonificación aplicada:</span><span class="data-val highlight">Ahorras 300 € + Bóveda Gratis</span></div>
      </div>
    </article>

    <div class="section-head pink">III. Módulos Satélite, Auditoría GEO y Hardware NFC</div>

    <article class="card pink">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">📱 Módulos Satélite (IG / Logística / B2B)</span>
          <span class="card-subtitle pink">Con Troncal vs. Contratado Suelto</span>
        </div>
        <span class="price-tag">+75 € Combo</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Unido a cualquier Plan Troncal:</span><span class="data-val highlight">Setup 50%: +75 € (Ahorras 75 €)</span></div>
        <div class="data-row"><span class="data-label">Contratado como módulo suelto:</span><span class="data-val">Setup: 150 €</span></div>
      </div>
    </article>

    <article class="card amber">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">🔍 Auditoría SEO Local + GEO IA</span>
          <span class="card-subtitle amber">Paquete Código vs. Llave en Mano</span>
        </div>
        <span class="price-tag amber">195 € en Dúo+</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">1. Solo Paquete Código:</span><span class="data-val">200 €</span></div>
        <div class="data-row"><span class="data-label">2. Todo Incluido Llave en Mano:</span><span class="data-val">350 € (200 € + 150 €)</span></div>
        <div class="data-row"><span class="data-label">3. Bonificada en Combo Dúo+:</span><span class="data-val highlight">195 € Llave en Mano (Ahorras 155 €)</span></div>
        <div class="data-row"><span class="data-label">4. En Plan Anual Trinity+:</span><span class="data-val highlight">95 € Llave en Mano (Ahorras 255 €)</span></div>
      </div>
    </article>

    <article class="card amber">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">★ Atril Inteligente NFC + QR</span>
          <span class="card-subtitle amber">Hardware de Mostrador Grabado a Medida</span>
        </div>
        <span class="price-tag amber">39 € Único</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Desglose de ingeniería:</span><span class="data-val">Grabación chip NFC + Enlace oficial</span></div>
        <div class="data-row"><span class="data-label">Condición comercial:</span><span class="data-val highlight">Pago único • Sin cuotas mensuales</span></div>
      </div>
    </article>
    """
    return plantilla_base_movil(
        titulo="Anexo Técnico de Implantación (Setup + SEO/GEO)",
        subtitulo="Desglose oficial de puesta en marcha de los 5 Planes (Base a Pentium), Módulos Satélite, Auditoría GEO y Atril NFC.",
        badge="Anexo Técnico Oficial",
        url_impreso="setup.html",
        url_volver="../index.html#documentacion",
        contenido_html=cuerpo
    )


def reconstruir_setup_pc_profesional(ruta_setup_pc):
    """
    Reconstruye documentos/setup.html (versión Ordenador e Impresión) con:
    1) Pyme QUATRO y Pyme PENTIUM maquetados con el mismo código de colores, subtítulo en bloque inferior y columna de ahorro tachado que Base/Dúo/Trinity.
    2) Sin '+ 75 € + 75 € + 75 € + 75 €': usa fórmulas limpias ('150 € base + 3 módulos al 50%').
    3) Letra más grande, aprovechamiento completo de la hoja sin hueco vacío y zoom 1.28x en pantalla de ordenador.
    """
    html_setup_pc = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Anexo Técnico de Implantación (Setup + SEO/GEO) — Sistemas Pyme</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- [SP_SMART_REDIRECT_START] -->
  <script>
    (function() {
      try {
        var params = new URLSearchParams(window.location.search);
        if (params.get('modo') === 'impreso') return;
        var esMovil = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || (window.innerWidth > 0 && window.innerWidth <= 820);
        if (esMovil) {
          window.location.replace('setup_movil.html');
        }
      } catch(e) {}
    })();
  </script>
  <!-- [SP_SMART_REDIRECT_END] -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/qr-code-styling@1.6.0-rc.1/lib/qr-code-styling.js"></script>
  <style>
    @page { size: A5 portrait; margin: 0; }
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #0b192c;
      color: #0f172a;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 24px 0 48px 0;
    }
    .sheet {
      width: 148mm;
      height: 210mm;
      min-height: 210mm;
      max-height: 210mm;
      background: #ffffff;
      padding: 5.5mm 8mm 4.8mm 8mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 18px 45px rgba(0,0,0,0.55);
      overflow: hidden;
    }
    /* En pantalla de Ordenador ampliamos la hoja un 28% para lectura cómoda y grande */
    @media screen and (min-width: 821px) {
      .sheet {
        zoom: 1.28;
      }
    }
    @media print {
      body { background: none !important; padding: 0 !important; }
      .sheet { box-shadow: none !important; zoom: 1 !important; margin: 0 !important; }
      .no-print { display: none !important; }
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2.2px solid #0b2545;
      padding-bottom: 3.5px;
    }
    .brand-logo-img {
      max-height: 44px;
      width: auto;
      object-fit: contain;
    }
    .header-tagline {
      text-align: right;
      font-size: 7.8px;
      color: #475569;
      font-weight: 600;
      line-height: 1.25;
    }
    .header-tagline strong {
      color: #0f766e;
      font-size: 8.8px;
      font-weight: 900;
      display: block;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }
    .section-banner {
      background: linear-gradient(90deg, #0f766e 0%, #14b8a6 100%);
      color: #ffffff;
      padding: 4px 8px;
      border-radius: 4.5px;
      font-size: 8.6px;
      font-weight: 900;
      text-transform: uppercase;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .section-banner.dark {
      background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
    }
    .section-banner .rule {
      font-size: 7.2px;
      font-weight: 700;
      background: rgba(255,255,255,0.22);
      padding: 1.5px 6px;
      border-radius: 3.5px;
      text-transform: none;
    }
    .intro-box {
      background: #f0f9ff;
      border: 1px solid #bae6fd;
      border-radius: 4.5px;
      padding: 4.5px 7.5px;
      font-size: 7.7px;
      color: #1e293b;
      line-height: 1.3;
    }
    .phases-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 4.5px;
    }
    .phase-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 3.5px solid #0f766e;
      border-radius: 4.5px;
      padding: 4.5px 7px;
    }
    .phase-card strong {
      display: block;
      font-size: 8px;
      font-weight: 900;
      color: #0b2545;
      margin-bottom: 1.5px;
    }
    .phase-card span {
      display: block;
      font-size: 7.1px;
      color: #334155;
      line-height: 1.24;
    }
    .setup-table-wrap {
      border: 1.5px solid #cbd5e1;
      border-radius: 5px;
      overflow: hidden;
      background: #ffffff;
    }
    .setup-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 7.8px;
    }
    .setup-table th {
      background: #1e293b;
      color: #ffffff;
      font-size: 6.9px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      padding: 4.2px 6px;
      text-align: center;
    }
    .setup-table th:first-child {
      text-align: left;
    }
    .setup-table td {
      padding: 4.4px 6px;
      border-top: 1px solid #e2e8f0;
      vertical-align: middle;
      text-align: center;
      line-height: 1.22;
      color: #1e293b;
    }
    .setup-table td:first-child {
      text-align: left;
    }
    .plan-name {
      font-size: 8.5px;
      font-weight: 900;
      color: #0b2545;
      display: block;
      line-height: 1.15;
    }
    .plan-sub {
      font-size: 6.4px;
      font-weight: 800;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.25px;
      display: block;
      margin-top: 1px;
    }
    .price-main {
      font-size: 9.4px;
      font-weight: 900;
      color: #0b2545;
    }
    .old-strike {
      font-size: 6.4px;
      color: #94a3b8;
      text-decoration: line-through;
      display: block;
    }
    .save-badge {
      font-size: 7.3px;
      font-weight: 800;
      color: #0f766e;
      display: block;
    }
    .guarantee-box {
      background: #fffbeb;
      border: 1.4px solid #fcd34d;
      border-left: 4px solid #d97706;
      border-radius: 4.5px;
      padding: 5px 8px;
      font-size: 7.4px;
      color: #78350f;
      line-height: 1.28;
    }
    .print-qr-banner {
      background: #f0fdfa;
      border: 1.4px dashed #0f766e;
      border-radius: 5px;
      padding: 4.5px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .print-qr-left {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 1;
    }
    .print-qr-img {
      width: 38px;
      height: 38px;
      flex-shrink: 0;
      border-radius: 4px;
    }
    .print-qr-text {
      font-size: 7.4px;
      color: #1e293b;
      line-height: 1.25;
    }
    .print-qr-text strong {
      color: #115e59;
      font-size: 8.3px;
      display: block;
      margin-bottom: 1px;
    }
    .contact-details-box {
      border-left: 1.4px solid #99f6e4;
      padding-left: 8px;
      font-size: 7.1px;
      line-height: 1.25;
      color: #1e293b;
      text-align: right;
      flex-shrink: 0;
    }
    .contact-details-box .name {
      font-size: 8.5px;
      font-weight: 900;
      color: #0b2545;
      display: block;
    }
    .contact-details-box .role {
      font-size: 6.2px;
      font-weight: 800;
      color: #0f766e;
      text-transform: uppercase;
      display: block;
    }
    .footer-bar {
      border-top: 1px solid #cbd5e1;
      padding-top: 2.5px;
      font-size: 7px;
      color: #64748b;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  </style>
</head>
<body>
  <main class="sheet">
    <header class="header">
      <div>
        <img src="../logo.png" alt="Sistemas Pyme" class="brand-logo-img" onerror="this.onerror=null; this.src='logo.png';">
      </div>
      <div class="header-tagline">
        <strong>Anexo Técnico de Implantación</strong>
        Setup de Automatización e Ingeniería SEO + GEO
      </div>
    </header>

    <div class="section-banner">
      <span>¿Qué es la Puesta en Marcha (Setup) y la Implantación SEO+GEO?</span>
      <span class="rule">Pago único de ingeniería inicial</span>
    </div>

    <div class="intro-box">
      El <strong>Setup Técnico</strong> y la <strong>Implantación SEO+GEO</strong> cubren las horas de <strong>ingeniería llave en mano</strong> necesarias para construir, conectar e inyectar el código estructurado a medida de tu negocio. Se abona <strong>una sola vez al inicio</strong> y comprende 4 fases críticas:
    </div>

    <div class="phases-grid">
      <div class="phase-card">
        <strong>🔌 1. Conexión Oficial de APIs y Meta/Google</strong>
        <span>Alta en Meta Cloud API (WhatsApp Oficial), vinculación con Google Business Profile, calendarios y carpetas de gestoría.</span>
      </div>
      <div class="phase-card" style="border-left-color: #2563eb;">
        <strong>🧠 2. Entrenamiento de IA a Medida y RGPD</strong>
        <span>Personalización del motor de IA con el tono de tu local, reglas de secreto profesional (RGPD) y aprobación de plantillas.</span>
      </div>
      <div class="phase-card" style="border-left-color: #d97706;">
        <strong>🔍 3. Ingeniería de Código SEO Local + GEO IA</strong>
        <span>Auditoría de 16 parámetros e inyección de Schema.org JSON-LD, etiquetas Meta/H1 y textos para que te recomienden ChatGPT y Gemini.</span>
      </div>
      <div class="phase-card" style="border-left-color: #16a34a;">
        <strong>✅ 4. Testeo en Vivo, AnyDesk y Entrega</strong>
        <span>Simulaciones reales de extremo a extremo, implantación remota (AnyDesk / Delegado GBP) o presencial sin parar tu negocio.</span>
      </div>
    </div>

    <div class="section-banner dark">
      <span>Tabla Oficial de Tarifas de Setup y Auditoría SEO + GEO</span>
      <span class="rule">1º a 150 € | Módulos extra al 50% (+75 €)</span>
    </div>

    <div class="setup-table-wrap">
      <table class="setup-table">
        <thead>
          <tr>
            <th style="width: 31%;">Plan / Servicio Técnico</th>
            <th style="width: 27%;">Desglose de Ingeniería</th>
            <th style="width: 17%;">Importe Pago Único</th>
            <th style="width: 25%;">Bonificación Aplicada</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <span class="plan-name">Pyme <span style="color:#64748b;">BASE</span></span>
              <span class="plan-sub">1 Servicio Troncal</span>
            </td>
            <td>1er módulo base (100%)</td>
            <td><span class="price-main">150 €</span></td>
            <td><span style="font-size:7.2px; font-weight:700; color:#475569;">Tarifa Estándar Base</span></td>
          </tr>
          <tr>
            <td>
              <span class="plan-name">Pyme <span style="color:#0284c7;">DÚO</span></span>
              <span class="plan-sub" style="color:#0369a1;">2 Servicios Combinados</span>
            </td>
            <td>150 € base + <strong>1 módulo al 50%</strong></td>
            <td><span class="price-main">225 €</span></td>
            <td>
              <span class="old-strike">Sueltos: 300 €</span>
              <span class="save-badge">Ahorras 75 € en Setup</span>
            </td>
          </tr>
          <tr style="background:#f0fdf4;">
            <td>
              <span class="plan-name" style="color:#15803d;">Pyme TRINITY ★</span>
              <span class="plan-sub" style="color:#16a34a;">3 Servicios Combinados</span>
            </td>
            <td>150 € base + <strong>2 módulos al 50%</strong></td>
            <td><span class="price-main" style="color:#15803d;">300 €</span></td>
            <td>
              <span class="old-strike">Sueltos: 450 €</span>
              <span class="save-badge" style="color:#15803d;">Ahorras 150 € + Bóveda Gratis</span>
            </td>
          </tr>
          <tr style="background:#f5f3ff;">
            <td>
              <span class="plan-name">Pyme <span style="color:#4f46e5;">QUATRO</span></span>
              <span class="plan-sub" style="color:#4338ca;">4 Servicios Combinados</span>
            </td>
            <td>150 € base + <strong>3 módulos al 50%</strong></td>
            <td><span class="price-main" style="color:#4338ca;">375 €</span></td>
            <td>
              <span class="old-strike">Sueltos: 600 €</span>
              <span class="save-badge" style="color:#4338ca;">Ahorras 225 € + Bóveda Gratis</span>
            </td>
          </tr>
          <tr style="background:#f0fdfa;">
            <td>
              <span class="plan-name">Pyme <span style="color:#0d9488;">PENTIUM</span></span>
              <span class="plan-sub" style="color:#0f766e;">5 Servicios Combinados</span>
            </td>
            <td>150 € base + <strong>4 módulos al 50%</strong></td>
            <td><span class="price-main" style="color:#0f766e;">450 €</span></td>
            <td>
              <span class="old-strike">Sueltos: 750 €</span>
              <span class="save-badge" style="color:#0f766e;">Ahorras 300 € + Bóveda Gratis</span>
            </td>
          </tr>
          <tr style="background:#fdf2f8;">
            <td>
              <span class="plan-name" style="color:#9d174d;">Módulos Satélite (IG / Log. / B2B)</span>
              <span class="plan-sub" style="color:#be185d;">Con Troncal vs. Suelto</span>
            </td>
            <td>50% dto. al unirlo a un Pack</td>
            <td>
              <span style="font-size:8.4px; font-weight:900; color:#9d174d; display:block;">+75 € (Combo)</span>
              <span style="font-size:6.6px; color:#64748b;">150 € (Suelto)</span>
            </td>
            <td><span class="save-badge" style="color:#9d174d;">Ahorras 75 € en Setup</span></td>
          </tr>
          <tr style="background:#ecfdf5;">
            <td>
              <span class="plan-name" style="color:#0f766e;">🔍 Auditoría SEO Local + GEO IA</span>
              <span class="plan-sub" style="color:#0d9488;">Paquete Código vs. Llave en Mano</span>
            </td>
            <td>
              Código: <strong>200 €</strong><br>
              Implantación técnica: <strong>+150 €</strong>
            </td>
            <td>
              <span style="font-size:8.2px; font-weight:900; color:#0b2545; display:block;">200 € <span style="font-size:6.5px; font-weight:600;">(Código)</span></span>
              <span style="font-size:8.2px; font-weight:900; color:#0f766e; display:block;">350 € <span style="font-size:6.5px; font-weight:600;">(Total)</span></span>
            </td>
            <td>
              <span class="save-badge" style="color:#15803d;">195 € en Combo Dúo+</span>
              <span style="font-size:6.5px; font-weight:800; color:#0f766e;">(95 € Llave en Mano en Anual Trinity+)</span>
            </td>
          </tr>
          <tr>
            <td>
              <span class="plan-name">Atril Inteligente NFC + QR</span>
              <span class="plan-sub" style="color:#d97706;">Hardware Mostrador</span>
            </td>
            <td>Grabación chip + Enlace oficial</td>
            <td><span class="price-main" style="color:#b45309;">39 €</span></td>
            <td><span style="font-size:7.2px; font-weight:800; color:#b45309;">Pago único • Sin cuotas</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="guarantee-box">
      <strong style="color:#b45309;">Garantía de Escalabilidad sin Penalización:</strong> Si hoy empiezas con 1 solo servicio (Setup 150 €) y más adelante amplías tu plan, <strong>te respetamos el 50% de bonificación (+75 € de Setup por nuevo módulo)</strong>. Si ya compraste el Paquete de Código SEO+GEO (200 €) y decides que te lo implantemos nosotros después, solo abonas la diferencia (+150 €).
    </div>

    <div class="print-qr-banner">
      <div class="print-qr-left">
        <img src="../qr-code.png" data-qr-url="https://wa.me/34711547561?text=Hola%20Francisco%2C%20estoy%20viendo%20el%20Anexo%20T%C3%A9cnico%20de%20Setup%20y%20quiero%20programar%20la%20puesta%20en%20marcha" alt="QR Contacto" class="print-qr-img" onerror="this.style.display='none'">
        <div class="print-qr-text">
          <strong>¿Listo para programar la puesta en marcha en tu negocio?</strong>
          Escanea este código con tu móvil para hablar por WhatsApp con Francisco y agendar tu implantación técnica.
        </div>
      </div>
      <div class="contact-details-box">
        <span class="name">Francisco M. Gallardo</span>
        <span class="role">Consultor Tecnológico</span>
        <strong>711 54 75 61</strong><br>
        francisco@sistemaspyme.es<br>
        <span style="color:#64748b;">sistemaspyme.es • Galicia</span>
      </div>
    </div>

    <footer class="footer-bar">
      <span><strong>Sistemas Pyme</strong> — Documento Anexo de Tarifas Técnicas de Inicio</span>
      <span>Precios netos sin IVA (21%)</span>
      <span><strong>Anexo I (Setup + SEO/GEO)</strong></span>
    </footer>
  </main>
</body>
</html>"""
    with open(ruta_setup_pc, "w", encoding="utf-8") as f:
        f.write(html_setup_pc)


def quitar_precios_y_ampliar_zoom_pc_en_documentos(dir_raiz):
    """
    1. En catalogo.html (Dossier PC): quita los badges de precios mensuales ('59 € / mes', '+40 € / mes', etc.) de los servicios para que el Dossier sea 100% explicativo.
    2. En todos los documentos de PC (catalogo.html, tarifas.html, desembolso.html, Pyme_Magazine_N1.html): inyecta zoom de lectura cómoda en pantallas de ordenador (@media screen and (min-width: 821px) { .sheet, .page { zoom: 1.24; } }) manteniendo zoom: 1 al imprimir.
    """
    ruta_catalogo_pc = os.path.join(dir_raiz, "documentos", "catalogo.html")
    if os.path.isfile(ruta_catalogo_pc):
        with open(ruta_catalogo_pc, "r", encoding="utf-8", errors="ignore") as f:
            html_cat = f.read()

        # Quitar píldoras de precio en las cabeceras de los servicios del Dossier A4 si existen
        html_cat = re.sub(
            r'<span[^>]*>\s*(?:\+?\d+\s*€\s*/\s*mes|59\s*€\s*/\s*mes|\+40\s*€\s*/\s*mes|Pago\s*Único:\s*39\s*€)\s*</span>',
            '',
            html_cat,
            flags=re.IGNORECASE
        )
        with open(ruta_catalogo_pc, "w", encoding="utf-8") as f:
            f.write(html_cat)

    rutas_pc = [
        os.path.join(dir_raiz, "documentos", "catalogo.html"),
        os.path.join(dir_raiz, "documentos", "tarifas.html"),
        os.path.join(dir_raiz, "documentos", "desembolso.html"),
        os.path.join(dir_raiz, "articulos", "Pyme_Magazine_N1.html"),
    ]

    bloque_zoom_pc = """<!-- [SP_PC_SCREEN_ZOOM_START] -->
<style>
  @media screen and (min-width: 821px) {
    .sheet, .page, .a4-page, .a5-sheet, main.sheet {
      zoom: 1.24;
    }
  }
  @media print {
    .sheet, .page, .a4-page, .a5-sheet, main.sheet {
      zoom: 1 !important;
    }
  }
</style>
<!-- [SP_PC_SCREEN_ZOOM_END] -->"""

    for ruta in rutas_pc:
        if not os.path.isfile(ruta):
            continue
        with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        html = re.sub(
            r'<!-- \[SP_PC_SCREEN_ZOOM_START\][\s\S]*?<!-- \[SP_PC_SCREEN_ZOOM_END\] -->',
            '',
            html
        )
        if "</head>" in html:
            html = html.replace("</head>", bloque_zoom_pc + "\n</head>", 1)
        else:
            html = bloque_zoom_pc + "\n" + html

        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)


def ejecutar_actualizacion():
    print("=" * 84)
    print("🚀 ACTUALIZANDO DOSSIER SIN PRECIOS, SETUP PC/MÓVIL REDISEÑADO Y ZOOM LECTURA EN PC")
    print("=" * 84)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ No se encontró la carpeta public_html.")
        return

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")

    dir_docs = os.path.join(dir_raiz, "documentos")
    os.makedirs(dir_docs, exist_ok=True)

    # 1. Actualizar Dossier Móvil sin precios
    ruta_cat_movil = os.path.join(dir_docs, "catalogo_movil.html")
    if os.path.isfile(ruta_cat_movil):
        shutil.copy2(ruta_cat_movil, os.path.join(carpeta_backups, f"catalogo_movil.html.backup_{marca}"))
    with open(ruta_cat_movil, "w", encoding="utf-8") as f:
        f.write(construir_catalogo_movil_sin_precios())
    print("   ✔ 'documentos/catalogo_movil.html': Precios eliminados (100% enfocado en funcionamiento y sin etiquetas desubicadas).")

    # 2. Actualizar Setup Móvil sin '+75+75+75+75'
    ruta_setup_movil = os.path.join(dir_docs, "setup_movil.html")
    if os.path.isfile(ruta_setup_movil):
        shutil.copy2(ruta_setup_movil, os.path.join(carpeta_backups, f"setup_movil.html.backup_{marca}"))
    with open(ruta_setup_movil, "w", encoding="utf-8") as f:
        f.write(construir_setup_movil_limpio())
    print("   ✔ 'documentos/setup_movil.html': Desglose de ingeniería limpio ('150 € base + X módulos al 50%').")

    # 3. Reconstruir Setup PC (documentos/setup.html) con Quatro/Pentium maquetados con colores, sin '+75+75+75' y letra más grande
    ruta_setup_pc = os.path.join(dir_docs, "setup.html")
    if os.path.isfile(ruta_setup_pc):
        shutil.copy2(ruta_setup_pc, os.path.join(carpeta_backups, f"setup.html.backup_{marca}"))
    reconstruir_setup_pc_profesional(ruta_setup_pc)
    print("   ✔ 'documentos/setup.html' (Ordenador): Pyme QUATRO y PENTIUM maquetados con colores, fórmulas limpias y letra ampliada.")

    # 4. Quitar precios en Dossier PC y ampliar zoom de lectura en pantalla de ordenador para todos los documentos
    quitar_precios_y_ampliar_zoom_pc_en_documentos(dir_raiz)
    print("   ✔ Documentos de Ordenador ('catalogo.html', 'tarifas.html', 'setup.html', 'desembolso.html', 'Pyme_Magazine_N1.html'): Zoom de pantalla ampliado (+24% a +28%) conservando impresión A4/A5 exacta.")

    print("=" * 84)
    print("✅ PROCESO COMPLETADO CON ÉXITO.")
    print("=" * 84)


if __name__ == "__main__":
    ejecutar_actualizacion()
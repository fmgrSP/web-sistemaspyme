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
      gap: 3px;
    }}
    .card-title {{
      font-size: 1.12em;
      font-weight: 900;
      color: #ffffff;
      line-height: 1.25;
      display: block;
    }}
    .card-subtitle {{
      display: inline-block;
      font-size: 0.84em;
      font-weight: 800;
      color: #5eead4;
      background: rgba(20, 184, 166, 0.14);
      border: 1px solid rgba(20, 184, 166, 0.35);
      padding: 2px 9px;
      border-radius: 8px;
      width: fit-content;
      white-space: nowrap;
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
    .price-tag {{
      background: rgba(20, 184, 166, 0.18);
      color: #5eead4;
      border: 1px solid rgba(20, 184, 166, 0.4);
      font-weight: 900;
      font-size: 0.98em;
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


def construir_tarifas_movil():
    cuerpo = """
    <div class="section-head">I. Planes Modulares (Cara A)</div>

    <article class="card">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">1. Plan PYME BASE</span>
          <span class="card-subtitle">1 Servicio Activo</span>
        </div>
        <span class="price-tag">59 € / mes</span>
      </div>
      <p>1 servicio troncal activo a libre elección (Gestión de Reseñas IA o Encuesta WhatsApp).</p>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Cuota Mensual (Vía 1):</span><span class="data-val">59 € / mes</span></div>
        <div class="data-row"><span class="data-label">Setup Único de Ingeniería:</span><span class="data-val">150 €</span></div>
        <div class="data-row"><span class="data-label">Plan Anual (Vía 2 - 10 meses):</span><span class="data-val highlight">590 € / año (Ahorras 118 €)</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">2. Plan PYME DÚO / Pack Escudo</span>
          <span class="card-subtitle">2 Servicios Activos</span>
        </div>
        <span class="price-tag">99 € / mes</span>
      </div>
      <p>Combina <strong>Servicio 1 (Reseñas IA) + Servicio 2 (Encuesta WhatsApp)</strong>. El 2º servicio suma solo +40 €/mes y su Setup lleva un 50% de descuento (+75 €).</p>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Cuota Mensual (Vía 1):</span><span class="data-val">99 € / mes (Ahorras 19 €/m)</span></div>
        <div class="data-row"><span class="data-label">Setup Dúo Bonificado:</span><span class="data-val">225 € (150 € + 75 €)</span></div>
        <div class="data-row"><span class="data-label">Plan Anual (Vía 2 - 10 meses):</span><span class="data-val highlight">990 € / año (Ahorras 198 €)</span></div>
        <div class="data-row"><span class="data-label">Ventaja Auditoría SEO+GEO:</span><span class="data-val highlight">Bonificada a 195 € (Ahorras 155 €)</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">3. Plan PYME TRINITY ★</span>
          <span class="card-subtitle amber">3 Servicios Activos</span>
        </div>
        <span class="price-tag amber">139 € / mes</span>
      </div>
      <p>3 servicios combinados activos a libre elección. <strong>Incluye GRATIS la Bóveda Segura de Contraseñas (valorada en 150 €).</strong></p>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Cuota Mensual (Vía 1):</span><span class="data-val">139 € / mes (Ahorras 38 €/m)</span></div>
        <div class="data-row"><span class="data-label">Setup Trinity Bonificado:</span><span class="data-val">300 €</span></div>
        <div class="data-row"><span class="data-label">Plan Anual (Vía 2 - 10 meses):</span><span class="data-val highlight">1.390 € / año (Ahorras 278 €)</span></div>
        <div class="data-row"><span class="data-label">Auditoría SEO+GEO en Anual:</span><span class="data-val highlight">Por solo 95 € Llave en Mano</span></div>
      </div>
    </article>

    <article class="card blue">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">4. Plan PYME QUATRO</span>
          <span class="card-subtitle blue">4 Servicios Activos</span>
        </div>
        <span class="price-tag">179 € / mes</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Cuota Mensual (Vía 1):</span><span class="data-val">179 € / mes (Ahorras 57 €/m)</span></div>
        <div class="data-row"><span class="data-label">Setup Quatro:</span><span class="data-val">375 €</span></div>
        <div class="data-row"><span class="data-label">Plan Anual (Vía 2 - 10 meses):</span><span class="data-val highlight">1.790 € / año (Ahorras 358 €)</span></div>
        <div class="data-row"><span class="data-label">Incluye:</span><span class="data-val">Bóveda Gratis + GEO a 95 € en Anual</span></div>
      </div>
    </article>

    <article class="card indigo">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">5. Plan PYME PENTIUM</span>
          <span class="card-subtitle indigo">5 Servicios Activos</span>
        </div>
        <span class="price-tag">219 € / mes</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Cuota Mensual (Vía 1):</span><span class="data-val">219 € / mes (Ahorras 76 €/m)</span></div>
        <div class="data-row"><span class="data-label">Setup Pentium:</span><span class="data-val">450 €</span></div>
        <div class="data-row"><span class="data-label">Plan Anual (Vía 2 - 10 meses):</span><span class="data-val highlight">2.190 € / año (Ahorras 438 €)</span></div>
        <div class="data-row"><span class="data-label">Del 6º al 10º servicio:</span><span class="data-val">+30 € / mes (+75 € Setup)</span></div>
      </div>
    </article>

    <div class="section-head amber">II. Auditoría e Implantación Premium SEO + GEO IA</div>
    <article class="card amber">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">🔍 Posicionamiento en Google, ChatGPT y Gemini</span>
          <span class="card-subtitle amber">Pago Único • Sin Cuotas</span>
        </div>
        <span class="price-tag amber">195 € en Dúo+</span>
      </div>
      <p>Escáner de 16 parámetros + código estructurado e implantación en tu Web y Google Maps para que las IAs recomienden tu negocio.</p>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">1. Solo Paquete Código:</span><span class="data-val">200 € (Para tu informático)</span></div>
        <div class="data-row"><span class="data-label">2. Todo Incluido (Suelta / Base):</span><span class="data-val">350 € (Código 200€ + Mano obra 150€)</span></div>
        <div class="data-row"><span class="data-label">3. Con Pack Escudo / Dúo+:</span><span class="data-val highlight">195 € Llave en Mano (Ahorras 155 €)</span></div>
        <div class="data-row"><span class="data-label">4. Con Plan Anual Trinity+:</span><span class="data-val highlight">95 € Llave en Mano (Ahorras 255 €)</span></div>
      </div>
    </article>

    <div class="section-head indigo">III. Las 2 Vías de Contratación (Cara B)</div>
    <article class="card">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">🔄 Vía 1: Modalidad Mensual Flexible</span>
          <span class="card-subtitle">Domiciliación SEPA Mes a Mes</span>
        </div>
      </div>
      <ul class="list-check">
        <li><span class="chk">✔</span><span><strong>Compromiso inicial de solo 3 meses</strong> de rodaje; después cancelable o ajustable con 30 días de preaviso.</span></li>
        <li><span class="chk">✔</span><span><strong>Setup Nominal:</strong> 150 € el 1er servicio y <strong>+75 € (50% dto.)</strong> por cada servicio adicional.</span></li>
        <li><span class="chk">✔</span><span><strong>Desembolso Día 1:</strong> Setup Nominal + Cuota del Mes 1.</span></li>
      </ul>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">⭐ Vía 2: Plan Anual (Pagas 10 Meses y Disfrutas 12)</span>
          <span class="card-subtitle amber">2 Mensualidades Gratis (-16,6%)</span>
        </div>
      </div>
      <ul class="list-check">
        <li><span class="chk">✔</span><span><strong>Te regalamos 2 mensualidades completas</strong> (16,6% de descuento directo sobre todo el año).</span></li>
        <li><span class="chk">✔</span><span><strong>Auditoría SEO+GEO Llave en Mano:</strong> a <strong>195 €</strong> en Plan Dúo Anual y a solo <strong>95 €</strong> desde Plan Anual Trinity+.</span></li>
        <li><span class="chk">✔</span><span><strong>Desembolso Día 1:</strong> Setup Nominal + 10 Mensualidades (con 12 meses de servicio garantizado).</span></li>
      </ul>
    </article>
    """
    return plantilla_base_movil(
        titulo="Tarifas Oficiales y Planes Modulares",
        subtitulo="Versión adaptada a lectura móvil con letra grande y desglose completo de Vía 1 (Mensual) y Vía 2 (Plan Anual).",
        badge="Tarjetón Oficial de Tarifas",
        url_impreso="tarifas.html",
        url_volver="../index.html#tarifas",
        contenido_html=cuerpo
    )


def construir_desembolso_movil():
    cuerpo = """
    <div class="section-head">Comparativa de Desembolso Día 1 por Plan</div>

    <article class="card">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">1. Plan PYME BASE</span>
          <span class="card-subtitle">1 Servicio Activo</span>
        </div>
        <span class="price-tag">59 €/m</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Setup Único de Ingeniería:</span><span class="data-val">150 €</span></div>
        <div class="data-row"><span class="data-label">🔄 Día 1 en Vía 1 (Mensual):</span><span class="data-val">209 € (150€ Setup + 59€ Mes 1)</span></div>
        <div class="data-row"><span class="data-label">⭐ Día 1 en Vía 2 (Anual 10m):</span><span class="data-val highlight">740 € (150€ Setup + 590€ Año)</span></div>
        <div class="data-row"><span class="data-label">Si sumas Auditoría GEO Llave en Mano:</span><span class="data-val">+350 € (Total alta + GEO: 500 €)</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">2. PACK ESCUDO / PLAN DÚO ★</span>
          <span class="card-subtitle">2 Servicios Activos</span>
        </div>
        <span class="price-tag amber">99 €/m</span>
      </div>
      <p><strong>Efecto Anclaje:</strong> Contratar 2 servicios + la Auditoría GEO cuesta <strong>420 € de entrada</strong> (225€ Setup + 195€ GEO), es decir, <strong>80 € menos que contratar 1 solo servicio + GEO (500 €)</strong>.</p>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Setup Dúo (2º al 50%):</span><span class="data-val">225 € (Ahorras 75 €)</span></div>
        <div class="data-row"><span class="data-label">🔄 Día 1 Escudo Básico (Mensual):</span><span class="data-val">324 € (225€ Setup + 99€ Mes 1)</span></div>
        <div class="data-row"><span class="data-label">🚀 Día 1 Escudo Total + GEO (Mensual):</span><span class="data-val highlight">519 € (225€ + 195€ GEO + 99€ Mes 1)</span></div>
        <div class="data-row"><span class="data-label">⭐ Día 1 en Vía 2 (Anual 10m):</span><span class="data-val highlight">1.215 € (225€ Setup + 990€ Año)</span></div>
        <div class="data-row"><span class="data-label">Ahorro Anual Total con GEO:</span><span class="data-val highlight">Ahorras 428 € el 1er año</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">3. Plan PYME TRINITY ★</span>
          <span class="card-subtitle amber">3 Servicios Activos</span>
        </div>
        <span class="price-tag">139 €/m</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Setup Trinity (2º y 3º al 50%):</span><span class="data-val">300 € (Ahorras 150 €)</span></div>
        <div class="data-row"><span class="data-label">Bóveda de Contraseñas (150 €):</span><span class="data-val highlight">GRATIS (0 €)</span></div>
        <div class="data-row"><span class="data-label">🔄 Día 1 en Vía 1 (Mensual):</span><span class="data-val">439 € (300€ Setup + 139€ Mes 1)</span></div>
        <div class="data-row"><span class="data-label">⭐ Día 1 en Vía 2 (Anual 10m):</span><span class="data-val highlight">1.690 € (300€ Setup + 1.390€ Año)</span></div>
        <div class="data-row"><span class="data-label">Auditoría GEO en Trinity Anual:</span><span class="data-val highlight">Solo +95 € Llave en Mano</span></div>
      </div>
    </article>

    <article class="card blue">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">4. Plan PYME QUATRO</span>
          <span class="card-subtitle blue">4 Servicios Activos</span>
        </div>
        <span class="price-tag">179 €/m</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Setup Quatro Bonificado:</span><span class="data-val">375 € (Ahorras 225 €)</span></div>
        <div class="data-row"><span class="data-label">🔄 Día 1 en Vía 1 (Mensual):</span><span class="data-val">554 € (375€ Setup + 179€ Mes 1)</span></div>
        <div class="data-row"><span class="data-label">⭐ Día 1 en Vía 2 (Anual 10m):</span><span class="data-val highlight">2.165 € (375€ Setup + 1.790€ Año)</span></div>
      </div>
    </article>

    <article class="card indigo">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">5. Plan PYME PENTIUM</span>
          <span class="card-subtitle indigo">5 Servicios Activos</span>
        </div>
        <span class="price-tag">219 €/m</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Setup Pentium Bonificado:</span><span class="data-val">450 € (Ahorras 300 €)</span></div>
        <div class="data-row"><span class="data-label">🔄 Día 1 en Vía 1 (Mensual):</span><span class="data-val">669 € (450€ Setup + 219€ Mes 1)</span></div>
        <div class="data-row"><span class="data-label">⭐ Día 1 en Vía 2 (Anual 10m):</span><span class="data-val highlight">2.640 € (450€ Setup + 2.190€ Año)</span></div>
      </div>
    </article>
    """
    return plantilla_base_movil(
        titulo="Tabla Desglosada de Puesta en Marcha y Desembolso Día 1",
        subtitulo="Importes exactos de inicio en Vía 1 (Mensual Flexible) y Vía 2 (Plan Anual con 2 meses gratis).",
        badge="Desglose Financiero Día 1",
        url_impreso="desembolso.html",
        url_volver="../index.html#tarifas",
        contenido_html=cuerpo
    )


def construir_setup_movil():
    cuerpo = """
    <div class="section-head">I. ¿Qué incluye la Ingeniería de Setup?</div>

    <article class="card">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">Conexión Oficial y Blindaje de Cuentas</span>
          <span class="card-subtitle">Implantación en 24-48 Horas</span>
        </div>
        <span class="price-tag">Llave en Mano</span>
      </div>
      <ul class="list-check">
        <li><span class="chk">✔</span><span><strong>Conexión de APIs Oficiales:</strong> vinculación verificada con <strong>Google Business Profile API</strong> y <strong>WhatsApp Business Cloud API (Meta)</strong>.</span></li>
        <li><span class="chk">✔</span><span><strong>Entrenamiento de IA a medida:</strong> inyección del contexto real, catálogo de servicios, especialidades, horarios, firma del responsable y blindajes legales/RGPD de tu negocio.</span></li>
        <li><span class="chk">✔</span><span><strong>Plantillas y Cortafuegos:</strong> alta de tus plantillas oficiales en Español, Gallego o Catalán en los 4 tonos (Formal, Semiformal, Cercano y Directo).</span></li>
        <li><span class="chk">✔</span><span><strong>Cuadro de Mando 360°:</strong> activación de tu panel de telemetría en vivo e informes mensuales ejecutivos.</span></li>
      </ul>
    </article>

    <div class="section-head">II. Escalado de Setup en los 5 Planes Troncales (Regla del 50%)</div>
    <p style="font-size: 0.92em; color: #cbd5e1; padding: 0 4px;">
      El <strong>1er servicio tiene un Setup único de 150 €</strong> y cada servicio adicional lleva un <strong>50% de descuento directo (+75 €)</strong> porque reutilizamos el núcleo conectado de tu negocio:
    </p>

    <article class="card">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">1. Plan PYME BASE</span>
          <span class="card-subtitle">1 Servicio Activo</span>
        </div>
        <span class="price-tag">Setup: 150 €</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Puesta en marcha técnica:</span><span class="data-val">150 € (Pago único)</span></div>
        <div class="data-row"><span class="data-label">Cuota mensual del plan:</span><span class="data-val">59 € / mes</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">2. Plan PYME DÚO / Pack Escudo</span>
          <span class="card-subtitle">2 Servicios Activos</span>
        </div>
        <span class="price-tag">Setup: 225 €</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Desglose Setup (150 € + 75 €):</span><span class="data-val highlight">225 € (Ahorras 75 €)</span></div>
        <div class="data-row"><span class="data-label">Cuota mensual del plan:</span><span class="data-val">99 € / mes (Ahorras 19 €/m)</span></div>
        <div class="data-row"><span class="data-label">Ventaja Auditoría SEO+GEO:</span><span class="data-val highlight">Desbloqueada a 195 €</span></div>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">3. Plan PYME TRINITY ★</span>
          <span class="card-subtitle amber">3 Servicios Activos</span>
        </div>
        <span class="price-tag amber">Setup: 300 €</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Desglose Setup (150 € + 75 € + 75 €):</span><span class="data-val highlight">300 € (Ahorras 150 €)</span></div>
        <div class="data-row"><span class="data-label">Cuota mensual del plan:</span><span class="data-val">139 € / mes (Ahorras 38 €/m)</span></div>
        <div class="data-row"><span class="data-label">Bono Bóveda de Contraseñas (150 €):</span><span class="data-val highlight">GRATIS (0 €)</span></div>
        <div class="data-row"><span class="data-label">Auditoría GEO en Trinity Anual:</span><span class="data-val highlight">Por solo 95 € Llave en Mano</span></div>
      </div>
    </article>

    <article class="card blue">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">4. Plan PYME QUATRO</span>
          <span class="card-subtitle blue">4 Servicios Activos</span>
        </div>
        <span class="price-tag">Setup: 375 €</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Desglose Setup (150 € + 3×75 €):</span><span class="data-val highlight">375 € (Ahorras 225 €)</span></div>
        <div class="data-row"><span class="data-label">Cuota mensual del plan:</span><span class="data-val">179 € / mes (Ahorras 57 €/m)</span></div>
        <div class="data-row"><span class="data-label">Bonos incluidos:</span><span class="data-val">Bóveda Gratis + GEO 195€ (95€ Anual)</span></div>
      </div>
    </article>

    <article class="card indigo">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">5. Plan PYME PENTIUM</span>
          <span class="card-subtitle indigo">5 Servicios Activos</span>
        </div>
        <span class="price-tag">Setup: 450 €</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Desglose Setup (150 € + 4×75 €):</span><span class="data-val highlight">450 € (Ahorras 300 €)</span></div>
        <div class="data-row"><span class="data-label">Cuota mensual del plan:</span><span class="data-val">219 € / mes (Ahorras 76 €/m)</span></div>
        <div class="data-row"><span class="data-label">Módulos extra (del 6º al 10º):</span><span class="data-val">+75 € Setup (+30 €/mes cuota)</span></div>
      </div>
    </article>

    <div class="section-head pink">III. Módulos Satélite y Hardware NFC</div>

    <article class="card pink">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">📱 Módulos Satélite Prémium</span>
          <span class="card-subtitle">Instagram 3 en 1 • Logística 360 • Redactor B2B</span>
        </div>
        <span class="price-tag">Setup: 75 €</span>
      </div>
      <p>Conexión con Meta Graph API Oficial (Instagram), portales de transporte o base documental vectorial RAG.</p>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Vinculado a cualquier plan troncal:</span><span class="data-val highlight">Setup 50%: 75 € (+40 €/mes)</span></div>
        <div class="data-row"><span class="data-label">Contratado como módulo suelto:</span><span class="data-val">Setup: 150 € (69 €/mes)</span></div>
      </div>
    </article>

    <article class="card amber">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">★ Atril Inteligente de Mostrador (NFC + QR)</span>
          <span class="card-subtitle amber">Hardware Físico Grabado a Medida</span>
        </div>
        <span class="price-tag amber">39 € Único</span>
      </div>
      <p>Incluye grabación del chip inalámbrico NFC y código QR dinámico apuntando a tu pantalla directa de reseñas en Google Maps con telemetría de escaneos iOS/Android.</p>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">Pago único por unidad:</span><span class="data-val highlight">39 € (Sin cuotas mensuales)</span></div>
        <div class="data-row"><span class="data-label">Plazo de entrega:</span><span class="data-val">24-48h listo para colocar</span></div>
      </div>
    </article>

    <div class="section-head amber">IV. Anexo Técnico: Auditoría Premium SEO + GEO IA</div>
    <article class="card amber">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">🔍 Los 16 Parámetros de Visibilidad en Google e IA</span>
          <span class="card-subtitle amber">Google Maps + ChatGPT + Gemini + Perplexity</span>
        </div>
        <span class="price-tag amber">195 € en Dúo+</span>
      </div>
      <ul class="list-check">
        <li><span class="chk">✔</span><span><strong>Inyección de código estructurado Schema.org JSON-LD:</strong> entidades <code>LocalBusiness</code>, <code>AggregateRating</code> y <code>FAQPage</code> para que ChatGPT, Gemini y Perplexity lean tus datos sin errores.</span></li>
        <li><span class="chk">✔</span><span><strong>Optimización de cabeceras Web:</strong> etiquetas <code>&lt;title&gt;</code>, <code>&lt;meta description&gt;</code> y jerarquía semántica <code>H1/H2</code> orientada a búsquedas locales.</span></li>
        <li><span class="chk">✔</span><span><strong>Optimización de Google Business Profile:</strong> descripción oficial, categorías secundarias, atributos y catálogo de servicios.</span></li>
      </ul>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">1. Solo Paquete de Código:</span><span class="data-val">200 €</span></div>
        <div class="data-row"><span class="data-label">2. Llave en Mano (Suelta o con Base):</span><span class="data-val">350 € (200 € + 150 €)</span></div>
        <div class="data-row"><span class="data-label">3. Bonificada desde Pack Escudo / Dúo+:</span><span class="data-val highlight">195 € (Ahorras 155 €)</span></div>
        <div class="data-row"><span class="data-label">4. Bonificada en Plan Anual Trinity+:</span><span class="data-val highlight">95 € (Ahorras 255 €)</span></div>
      </div>
    </article>
    """
    return plantilla_base_movil(
        titulo="Anexo Técnico de Setup, Satélites, Hardware y Auditoría GEO",
        subtitulo="Desglose completo de puesta en marcha de los 5 Planes (Base a Pentium), Módulos Satélite, Atril NFC y Auditoría SEO+GEO.",
        badge="Ingeniería de Puesta en Marcha",
        url_impreso="setup.html",
        url_volver="../index.html#documentacion",
        contenido_html=cuerpo
    )


def construir_catalogo_movil():
    cuerpo = """
    <div class="section-head">I. Reputación y Visibilidad en Google e IA (Activos Hoy)</div>

    <article class="card amber">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">★ Atril Inteligente de Mostrador (NFC + QR)</span>
          <span class="card-subtitle amber">Hardware Sin Cuotas • Activación en 1 Segundo</span>
        </div>
        <span class="price-tag amber">39 € Único</span>
      </div>
      <p>Soporte físico de metacrilato de alta resistencia con chip inalámbrico NFC NTAG215 integrado y código QR vectorial de alta densidad.</p>
      <div class="deep-box">
        <span class="deep-title amber">⚙️ ¿Cómo funciona exactamente en tu mostrador?</span>
        <ul class="list-check">
          <li><span class="chk">1.</span><span>Justo en el momento de cobrar o despedir a un cliente contento, le invitas a acercar su teléfono (iPhone o Android) al atril.</span></li>
          <li><span class="chk">2.</span><span>Sin abrir la cámara ni buscar tu negocio en Google, la ventana oficial de 5 estrellas de tu ficha se despliega automáticamente en <strong>menos de 1 segundo</strong>.</span></li>
          <li><span class="chk">3.</span><span>Nuestro servidor registra de forma anónima la métrica de cada escaneo (NFC vs. QR, iPhone vs. Android y franja horaria punta) en tu <strong>Informe Ejecutivo 360°</strong>.</span></li>
        </ul>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">1. Gestión y Respuesta de Reseñas en Google con IA</span>
          <span class="card-subtitle">Blindaje Jurídico HEARD + RGPD + SEO Local</span>
        </div>
        <span class="price-tag">59 € / mes</span>
      </div>
      <p>Sistema autónomo conectado a tu perfil de Google Business Profile que monitoriza, redacta y gestiona el 100% de tus reseñas con inteligencia artificial entrenada específicamente con el contexto de tu negocio.</p>
      <div class="deep-box">
        <span class="deep-title">🧠 Arquitectura y Protocolo de Actuación Paso a Paso</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span><strong>En Reseñas Positivas (4 y 5★):</strong> El motor detecta el idioma del autor (español, gallego, catalán, inglés, francés, alemán, etc.), redacta una respuesta cálida estructurada en 4 párrafos con las palabras clave de tu especialidad y localidad para impulsar tu SEO en Google Maps y la publica automáticamente.</span></li>
          <li><span class="chk">✔</span><span><strong>En Reseñas Críticas (1 a 3★) o Quejas Ocultas en 4★:</strong> El sistema <strong>bloquea la publicación automática</strong> y te envía al instante una alerta urgente por <strong>WhatsApp, Telegram y Correo HTML</strong>.</span></li>
          <li><span class="chk">✔</span><span><strong>Gestor Interactivo de 4 Tonos:</strong> Desde tu móvil abres en 1 toque las 4 propuestas redactadas con el protocolo psicológico <strong>HEARD</strong> (<em>Formal, Semiformal, Cercano y Directo</em>), acompañadas de una <strong>Nota Psicológica interna para gerencia</strong> y aviso de riesgo legal.</span></li>
          <li><span class="chk">✔</span><span><strong>Blindaje Médico/Legal RGPD y Regla Anti-Efecto Loro:</strong> Jamás confirma públicamente patologías ni tratamientos en clínicas (evitando multas de la AEPD) y nunca repite palabras tóxicas del cliente (como «estafa» o «caro») para que Google no las indexe en tu contra.</span></li>
        </ul>
      </div>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">2. Filtrado y Captación de Reseñas (Encuesta Inteligente)</span>
          <span class="card-subtitle">Cortafuegos Preventivo por WhatsApp Oficial</span>
        </div>
        <span class="price-tag">59 € / mes</span>
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
          <span class="card-subtitle amber">Visibilidad en ChatGPT, Gemini, Perplexity y Google</span>
        </div>
        <span class="price-tag amber">195 € en Dúo+</span>
      </div>
      <p>Hoy tus clientes ya no solo buscan en Google: le preguntan directamente a <strong>ChatGPT, Gemini o Perplexity</strong> qué profesional elegir en su localidad. Si tu web no tiene datos estructurados, para la IA eres invisible.</p>
      <div class="deep-box">
        <span class="deep-title amber">🛠️ ¿Qué auditamos e implantamos en tu negocio?</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span><strong>Escáner Técnico de 16 Parámetros:</strong> Auditoría completa de indexación, velocidad, autoridad local y brechas frente a tus 3 principales competidores.</span></li>
          <li><span class="chk">✔</span><span><strong>Programación a medida de Código Schema.org JSON-LD:</strong> Inyectamos en el código de tu web las entidades <code>LocalBusiness</code>, <code>MedicalBusiness / LegalService / Store</code>, <code>AggregateRating</code>, coordenadas geográficas, horarios y <code>FAQPage</code> para que los motores de IA lean tus servicios con precisión milimétrica.</span></li>
          <li><span class="chk">✔</span><span><strong>Optimización On-Page y Google Business Profile:</strong> Reescritura estratégica de etiquetas <code>&lt;title&gt;</code>, <code>&lt;meta description&gt;</code>, encabezados <code>H1/H2</code> y textos de categorías/servicios en Google Maps.</span></li>
          <li><span class="chk">✔</span><span><strong>3 Modalidades:</strong> Solo Paquete Código (200 €), Todo Incluido Llave en Mano (350 €), o <strong>Bonificada a 195 € con Pack Escudo</strong> (y <strong>95 € en Plan Anual Trinity+</strong>).</span></li>
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
        <span class="price-tag">+40 €/m</span>
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
        <span class="price-tag">+40 €/m</span>
      </div>
      <p>El 75% de las personas que llaman a un negocio local y no obtienen respuesta no dejan mensaje en el contestador: cuelgan y llaman inmediatamente al siguiente resultado de Google.</p>
      <div class="deep-box">
        <span class="deep-title blue">📞 Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>Cuando estás atendiendo a un cliente o con las manos ocupadas y entra una llamada móvil que no puedes contestar, el sistema detecta la llamada perdida.</span></li>
          <li><span class="chk">✔</span><span>A los <strong>5 segundos</strong> le envía un WhatsApp educado: <em>«¡Hola! Te escribimos de [Tu Negocio]. Justo estamos atendiendo en este instante y no pudimos cogerte el teléfono, ¿en qué podemos ayudarte por aquí?»</em>, reteniendo la venta en tu WhatsApp.</span></li>
        </ul>
      </div>
    </article>

    <article class="card blue">
      <div class="card-top">
        <div class="card-title-wrap">
          <span class="card-title">5. Reactivación Automática de Clientes Inactivos</span>
          <span class="card-subtitle blue">Ingresos Recurrentes sobre tu Base Actual</span>
        </div>
        <span class="price-tag">+40 €/m</span>
      </div>
      <p>Venderle de nuevo a un cliente que ya te conoce es 7 veces más rentable que captar a un desconocido desde cero.</p>
      <div class="deep-box">
        <span class="deep-title blue">🔄 Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>El sistema audita diariamente tu histórico de visitas o servicios (revisiones anuales de taller/ITV, limpiezas dentales cada 6 meses, sesiones de estética o mantenimiento).</span></li>
          <li><span class="chk">✔</span><span>Cuando un cliente supera su ciclo habitual (ej. 60, 90 o 180 días sin acudir), recibe un WhatsApp personalizado recordándole su revisión o invitándole con un detalle preferente.</span></li>
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
        <span class="price-tag">+40 €/m</span>
      </div>
      <p>Cada cita a la que un cliente no acude sin avisar es una hora de facturación perdida que nunca se recupera (4 citas perdidas a la semana a 30 € suponen <strong>480 € perdidos al mes</strong>).</p>
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
        <span class="price-tag">+40 €/m</span>
      </div>
      <p>Agente telefónico de voz neuronal en español que atiende llamadas simultáneas las 24 horas del día, los 365 días del año.</p>
      <div class="deep-box">
        <span class="deep-title">🎙️ Funcionamiento Técnico</span>
        <ul class="list-check">
          <li><span class="chk">✔</span><span>Responde con voz humana natural dudas sobre horarios, ubicación, tarifas o servicios de tu negocio.</span></li>
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
        <span class="price-tag">+40 €/m</span>
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
        <span class="price-tag">+40 €/m</span>
      </div>
      <p>Olvídate de acumular tickets arrugados en la guantera del coche o perder horas cada trimestre picando facturas.</p>
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
        <span class="price-tag">+40 €/m</span>
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
          <span class="card-subtitle">Meta Graph API Oficial • +40 €/m en combo (69 €/m suelto)</span>
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
          <span class="card-subtitle blue">E-commerce y Reparto • +40 €/m en combo (69 €/m suelto)</span>
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
          <span class="card-subtitle indigo">Cerebro Documental Propio • +40 €/m en combo (69 €/m suelto)</span>
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
        subtitulo="Explicación técnica detallada paso a paso de los 10 servicios troncales, el Atril NFC, la Auditoría SEO+GEO IA y los 3 Satélites.",
        badge="Dossier Técnico Detallado • 4 Páginas",
        url_impreso="catalogo.html",
        url_volver="../index.html#documentacion",
        contenido_html=cuerpo
    )


def construir_magazine_movil():
    cuerpo = """
    <div class="section-head">01. El Juego Oculto de los Google Local Guides</div>
    <article class="card">
      <p>En Google Maps no todas las reseñas pesan igual. La reseña de un <strong>Google Local Guide</strong> (usuarios con insignia de estrella naranja que escriben reseñas detalladas y suben fotos) tiene hasta <strong>10 veces más impacto en el posicionamiento de tu ficha</strong> que una puntuación vacía.</p>
      <p>Con el <strong>Atril NFC de mostrador</strong> y la <strong>Encuesta Post-Visita por WhatsApp</strong> logras que ningún cliente satisfecho se marche sin dejar su valoración.</p>
    </article>

    <div class="section-head amber">02. La Trampa del «Efecto Loro» en el SEO</div>
    <article class="card amber">
      <p>Cuando un cliente enfadado escribe palabras tóxicas en una reseña (como <em>«estafa», «caro», «sucio» o «mal trato»</em>) y el dueño responde repitiendo esas mismas palabras para defenderse (<em>«No somos ninguna estafa...»</em>), el algoritmo de Google indexa por partida doble ese término negativo asociado a tu local.</p>
      <p>Nuestro motor de IA aplica la <strong>Regla Anti-Efecto Loro</strong>: jamás repite términos dañinos y los sustituye por lenguaje diplomático de alta autoridad.</p>
    </article>

    <div class="section-head blue">03. Método Psicológico HEARD y Blindaje RGPD</div>
    <article class="card blue">
      <p>Desarrollado originalmente por Disney para la recuperación de clientes, el protocolo <strong>HEARD (Hear, Empathize, Apologize, Resolve, Diagnose)</strong> desactiva la hostilidad del lector futuro en 4 párrafos estructurados.</p>
      <p>Además, en clínicas médicas, dentales, fisioterapia o despachos jurídicos, nuestro sistema aplica <strong>Blindaje RGPD estricto</strong>: nunca confirma públicamente qué tratamiento o patología tuvo el paciente aunque él mismo lo mencione, evitando sanciones de la AEPD.</p>
    </article>

    <div class="section-head indigo">04. El Cortafuegos Privado de WhatsApp</div>
    <article class="card emerald">
      <p>La mejor reseña negativa es la que nunca llega a publicarse en Google Maps. Al enviar la encuesta interactiva 2 horas después de la cita:</p>
      <ul class="list-check">
        <li><span class="chk">🌟</span><span><strong>Si pulsa «Excelente»:</strong> Va directo en 1 toque a publicar sus 5★ en Google Maps.</span></li>
        <li><span class="chk">🛡️</span><span><strong>Si pulsa «Bien» o «Mejorable»:</strong> Se abre un canal privado en WhatsApp (texto o nota de voz transcrita por IA) y recibes una alerta urgente para solucionarlo en persona antes de que toque internet.</span></li>
      </ul>
    </article>
    """
    return plantilla_base_movil(
        titulo="Pyme Magazine Nº 1: La Nueva Regla del «Boca a Boca»",
        subtitulo="Informe Ejecutivo: Psicología de las reseñas en Google Maps, Regla Anti-Efecto Loro, Blindaje RGPD y Cortafuegos de WhatsApp.",
        badge="Pyme Magazine • Fascículo Nº 1",
        url_impreso="Pyme_Magazine_N1.html",
        url_volver="../index.html#magazine",
        contenido_html=cuerpo
    )


def separar_quatro_y_pentium_en_setup_pc(ruta_setup_pc):
    """Separa en filas independientes PYME QUATRO y PYME PENTIUM en documentos/setup.html (versión ordenador)."""
    if not os.path.isfile(ruta_setup_pc):
        return False
    with open(ruta_setup_pc, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    patron_fila_conjunta = re.compile(
        r'<tr[^>]*>\s*<td[^>]*>[^<]*(?:QUATRO\s*(?:/|y|-)\s*PENTIUM|4\s*ó\s*5\s*serv|375\s*€\s*/\s*450\s*€)[\s\S]*?</tr>',
        re.IGNORECASE
    )

    filas_separadas = """<tr>
              <td><strong>Plan PYME QUATRO</strong> <span style="font-size:6px; color:#64748b;">(4 Servicios combinados)</span></td>
              <td>150 € + 75 € + 75 € + 75 €</td>
              <td><strong style="color:#0f766e;">375 €</strong> <span style="font-size:5.8px; color:#16a34a; font-weight:700;">(Ahorras 225 €)</span></td>
              <td><strong>179 € / mes</strong> <span style="font-size:5.8px; color:#64748b;">(1.790 €/año)</span></td>
            </tr>
            <tr>
              <td><strong>Plan PYME PENTIUM</strong> <span style="font-size:6px; color:#64748b;">(5 Servicios combinados)</span></td>
              <td>150 € + 75 € + 75 € + 75 € + 75 €</td>
              <td><strong style="color:#0f766e;">450 €</strong> <span style="font-size:5.8px; color:#16a34a; font-weight:700;">(Ahorras 300 €)</span></td>
              <td><strong>219 € / mes</strong> <span style="font-size:5.8px; color:#64748b;">(2.190 €/año)</span></td>
            </tr>"""

    nuevo_html, n = patron_fila_conjunta.subn(filas_separadas, html)
    if n == 0:
        # Búsqueda alternativa por si el texto de la celda tiene etiquetas intermedias
        patron_alt = re.compile(
            r'<tr[^>]*>(?:(?!</tr).)*?QUATRO(?:(?!</tr).)*?PENTIUM(?:(?!</tr).)*?</tr>',
            re.IGNORECASE | re.DOTALL
        )
        nuevo_html, n = patron_alt.subn(filas_separadas, html)

    if n > 0:
        with open(ruta_setup_pc, "w", encoding="utf-8") as f:
            f.write(nuevo_html)
        return True
    return False


def inyectar_autoredireccion_inteligente_en_original(ruta_original, nombre_archivo_movil):
    if not os.path.isfile(ruta_original):
        return
    with open(ruta_original, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    html = re.sub(
        r'<!-- \[SP_SMART_REDIRECT_START\][\s\S]*?<!-- \[SP_SMART_REDIRECT_END\] -->',
        '',
        html
    )

    bloque_redirect = f"""<!-- [SP_SMART_REDIRECT_START] -->
<script>
  (function() {{
    try {{
      var params = new URLSearchParams(window.location.search);
      if (params.get('modo') === 'impreso') return;
      var esMovil = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || (window.innerWidth > 0 && window.innerWidth <= 820);
      if (esMovil) {{
        window.location.replace('{nombre_archivo_movil}');
      }}
    }} catch(e) {{}}
  }})();
</script>
<!-- [SP_SMART_REDIRECT_END] -->"""

    if "<head>" in html:
        html = html.replace("<head>", "<head>\n" + bloque_redirect, 1)
    else:
        html = bloque_redirect + "\n" + html

    with open(ruta_original, "w", encoding="utf-8") as f:
        f.write(html)


def actualizar_index_target_blank_y_router(ruta_index):
    """Configura todos los enlaces a documentos y artículos en index.html para abrirse en PESTAÑA NUEVA (target='_blank')."""
    if not os.path.isfile(ruta_index):
        return
    with open(ruta_index, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # 1. Asegurar que los enlaces directos a documentos/ tengan target="_blank" rel="noopener"
    for doc_href in (
        "documentos/catalogo.html",
        "documentos/tarifas.html",
        "documentos/setup.html",
        "documentos/desembolso.html",
        "articulos/Pyme_Magazine_N1.html"
    ):
        patron_a = re.compile(r'(<a\s+[^>]*href="' + re.escape(doc_href) + r'"[^>]*)(>)', re.IGNORECASE)
        def _add_blank(m):
            tag_open = m.group(1)
            if 'target="_blank"' not in tag_open:
                tag_open += ' target="_blank" rel="noopener"'
            return tag_open + m.group(2)
        html = patron_a.sub(_add_blank, html)

    # 2. Actualizar abrirArticuloMagazine para que abra en pestaña nueva (window.open)
    patron_fn_mag = re.compile(
        r'async function abrirArticuloMagazine\(e,\s*defaultHref\)\s*\{[\s\S]*?\n    \}',
        re.MULTILINE
    )
    nueva_fn_mag = """async function abrirArticuloMagazine(e, defaultHref) {
      if (e) e.preventDefault();
      var esMovil = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth <= 820;
      var destino = esMovil ? 'articulos/Pyme_Magazine_N1_movil.html' : defaultHref;
      window.open(destino, '_blank', 'noopener');
    }"""
    html = patron_fn_mag.sub(nueva_fn_mag, html)

    # 3. Reemplazar el router de documentos para que abra SIEMPRE en una pestaña nueva (_blank)
    html = re.sub(
        r'<!-- \[SP_INDEX_DOC_ROUTER_START\][\s\S]*?<!-- \[SP_INDEX_DOC_ROUTER_END\] -->',
        '',
        html
    )

    script_router = """<!-- [SP_INDEX_DOC_ROUTER_START] -->
<script>
  (function() {
    function esDispositivoMovilSP() {
      return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth <= 820;
    }
    const mapaMovil = {
      'documentos/catalogo.html': 'documentos/catalogo_movil.html',
      'documentos/tarifas.html': 'documentos/tarifas_movil.html',
      'documentos/setup.html': 'documentos/setup_movil.html',
      'documentos/desembolso.html': 'documentos/desembolso_movil.html',
      'articulos/Pyme_Magazine_N1.html': 'articulos/Pyme_Magazine_N1_movil.html'
    };
    document.addEventListener('click', function(e) {
      const link = e.target.closest('a[href]');
      if (!link) return;
      const href = link.getAttribute('href') || '';
      if (mapaMovil[href]) {
        e.preventDefault();
        e.stopPropagation();
        const urlFinal = esDispositivoMovilSP() ? mapaMovil[href] : href;
        window.open(urlFinal, '_blank', 'noopener');
      }
    }, true);
  })();
</script>
<!-- [SP_INDEX_DOC_ROUTER_END] -->"""

    if "</body>" in html:
        html = html.replace("</body>", script_router + "\n</body>", 1)
    else:
        html = html + "\n" + script_router

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)


def ejecutar_actualizacion():
    print("=" * 84)
    print("🚀 ACTUALIZANDO DOSSIER EXTENSO MÓVIL, SUBTÍTULOS DE SERVICIOS, SETUP Y PESTAÑA NUEVA")
    print("=" * 84)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ No se encontró public_html.")
        return

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

    ruta_index = os.path.join(dir_raiz, "index.html")
    shutil.copy2(ruta_index, os.path.join(carpeta_backups, f"index.html.backup_{marca_tiempo}"))

    dir_docs = os.path.join(dir_raiz, "documentos")
    dir_arts = os.path.join(dir_raiz, "articulos")
    os.makedirs(dir_docs, exist_ok=True)
    os.makedirs(dir_arts, exist_ok=True)

    # Backup de setup.html PC antes de separar Quatro y Pentium
    ruta_setup_pc = os.path.join(dir_docs, "setup.html")
    if os.path.isfile(ruta_setup_pc):
        shutil.copy2(ruta_setup_pc, os.path.join(carpeta_backups, f"setup.html.backup_{marca_tiempo}"))
        if separar_quatro_y_pentium_en_setup_pc(ruta_setup_pc):
            print("   ✔ 'documentos/setup.html' (PC): Planes PYME QUATRO y PYME PENTIUM separados en 2 filas.")
        else:
            print("   ℹ️ 'documentos/setup.html' (PC) revisado.")

    # Actualizar los 5 documentos móviles
    archivos_movil = [
        (os.path.join(dir_docs, "tarifas_movil.html"), construir_tarifas_movil(), os.path.join(dir_docs, "tarifas.html"), "tarifas_movil.html"),
        (os.path.join(dir_docs, "desembolso_movil.html"), construir_desembolso_movil(), os.path.join(dir_docs, "desembolso.html"), "desembolso_movil.html"),
        (os.path.join(dir_docs, "setup_movil.html"), construir_setup_movil(), os.path.join(dir_docs, "setup.html"), "setup_movil.html"),
        (os.path.join(dir_docs, "catalogo_movil.html"), construir_catalogo_movil(), os.path.join(dir_docs, "catalogo.html"), "catalogo_movil.html"),
        (os.path.join(dir_arts, "Pyme_Magazine_N1_movil.html"), construir_magazine_movil(), os.path.join(dir_arts, "Pyme_Magazine_N1.html"), "Pyme_Magazine_N1_movil.html"),
    ]

    for ruta_movil, contenido, ruta_orig, nombre_corto_movil in archivos_movil:
        with open(ruta_movil, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"   ✔ Actualizado: {os.path.relpath(ruta_movil, dir_raiz)}")
        if os.path.isfile(ruta_orig):
            inyectar_autoredireccion_inteligente_en_original(ruta_orig, nombre_corto_movil)

    # Configurar apertura en pestaña nueva en index.html
    actualizar_index_target_blank_y_router(ruta_index)
    print("   ✔ 'index.html': Todos los documentos ahora se abren en una PESTAÑA NUEVA (_blank).")
    print("=" * 84)
    print("✅ PROCESO COMPLETADO CON ÉXITO.")
    print("=" * 84)


if __name__ == "__main__":
    ejecutar_actualizacion()
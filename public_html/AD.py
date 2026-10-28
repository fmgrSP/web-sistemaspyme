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
      line-height: 1.55;
      -webkit-text-size-adjust: 100%;
    }}
    body.font-xl {{
      font-size: 19px;
      line-height: 1.62;
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
      max-width: 640px;
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
      font-size: 1.45em;
      font-weight: 900;
      color: #ffffff;
      line-height: 1.22;
      margin-bottom: 6px;
    }}
    .hero-sub {{
      font-size: 0.92em;
      color: #cbd5e1;
    }}
    .section-head {{
      background: linear-gradient(90deg, #0f766e 0%, #115e59 100%);
      color: #ffffff;
      padding: 10px 14px;
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
    .card {{
      background: #0f172a;
      border: 1.5px solid rgba(255,255,255,0.12);
      border-left: 5px solid #14b8a6;
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }}
    .card.amber {{ border-left-color: #f59e0b; background: linear-gradient(145deg, #1c1917 0%, #0f172a 100%); }}
    .card.emerald {{ border-left-color: #10b981; border-color: rgba(16,185,129,0.45); background: linear-gradient(145deg, rgba(6,78,59,0.45) 0%, #0f172a 100%); }}
    .card.blue {{ border-left-color: #3b82f6; }}
    .card.indigo {{ border-left-color: #6366f1; }}
    .card-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
    }}
    .card-title {{
      font-size: 1.12em;
      font-weight: 900;
      color: #ffffff;
      line-height: 1.25;
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
      font-size: 1.05em;
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
    <a href="{url_volver}" class="btn-back">⬅ Volver a la Web</a>
    <div class="topbar-actions">
      <button type="button" id="btnToggleFont" onclick="toggleFont()" class="btn-action">🔎 Letra A+</button>
      <a href="{url_impreso}?modo=impreso" class="btn-action secondary">📄 Ver Original A4/A5</a>
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
  </script>
</body>
</html>"""


def construir_tarifas_movil():
    cuerpo = """
    <div class="section-head">I. Planes Modulares (Cara A)</div>

    <article class="card">
      <div class="card-top">
        <span class="card-title">1. Plan PYME BASE (1 Servicio)</span>
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
        <span class="card-title">2. Plan PYME DÚO / Pack Escudo (2 Servicios)</span>
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
        <span class="card-title">3. Plan PYME TRINITY ★ (3 Servicios)</span>
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
        <span class="card-title">4. Plan PYME QUATRO (4 Servicios)</span>
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
        <span class="card-title">5. Plan PYME PENTIUM (5 Servicios)</span>
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
        <span class="card-title">🔍 Posicionamiento en Google, ChatGPT y Gemini</span>
        <span class="price-tag amber">Pago Único</span>
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
        <span class="card-title">🔄 Vía 1: Modalidad Mensual Flexible</span>
        <span class="price-tag">SEPA Mes a Mes</span>
      </div>
      <ul class="list-check">
        <li><span class="chk">✔</span><span><strong>Compromiso inicial de solo 3 meses</strong> de rodaje; después cancelable o ajustable con 30 días de preaviso.</span></li>
        <li><span class="chk">✔</span><span><strong>Setup Nominal:</strong> 150 € el 1er servicio y <strong>+75 € (50% dto.)</strong> por cada servicio adicional.</span></li>
        <li><span class="chk">✔</span><span><strong>Desembolso Día 1:</strong> Setup Nominal + Cuota del Mes 1.</span></li>
      </ul>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <span class="card-title">⭐ Vía 2: Plan Anual (Pagas 10 Meses y Disfrutas 12)</span>
        <span class="price-tag amber">2 Meses Gratis</span>
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
        <span class="card-title">1. Plan PYME BASE (1 Servicio)</span>
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
        <span class="card-title">2. PACK ESCUDO / DÚO ★ (2 Servicios)</span>
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
        <span class="card-title">3. Plan PYME TRINITY ★ (3 Servicios)</span>
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
        <span class="card-title">4. Plan PYME QUATRO (4 Servicios)</span>
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
        <span class="card-title">5. Plan PYME PENTIUM (5 Servicios)</span>
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
    <div class="section-head">¿Qué incluye la Ingeniería de Setup?</div>

    <article class="card">
      <div class="card-top">
        <span class="card-title">1. Conexión Oficial y Blindaje de Cuentas</span>
        <span class="price-tag">24-48h</span>
      </div>
      <ul class="list-check">
        <li><span class="chk">✔</span><span>Vinculación oficial con <strong>Google Business Profile API</strong> y <strong>WhatsApp Business Cloud API (Meta)</strong>.</span></li>
        <li><span class="chk">✔</span><span>Entrenamiento del motor de IA con el contexto real, servicios, tarifas, tono y guardrails RGPD de tu negocio.</span></li>
        <li><span class="chk">✔</span><span>Activación de tu Cuadro de Mando 360° e informes mensuales ejecutivos.</span></li>
      </ul>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <span class="card-title">2. Regla del 50% en Módulos Adicionales</span>
        <span class="price-tag amber">Ahorro 50%</span>
      </div>
      <div class="data-grid">
        <div class="data-row"><span class="data-label">1er Servicio Troncal:</span><span class="data-val">150 € (Pago único)</span></div>
        <div class="data-row"><span class="data-label">Cada Servicio Adicional (2º en adelante):</span><span class="data-val highlight">+75 € (50% de descuento)</span></div>
        <div class="data-row"><span class="data-label">Pack Escudo (2 Servicios):</span><span class="data-val">225 € en total (Ahorras 75 €)</span></div>
        <div class="data-row"><span class="data-label">Plan Trinity (3 Servicios):</span><span class="data-val">300 € + Bóveda Contraseñas Gratis</span></div>
      </div>
    </article>

    <div class="section-head amber">3. Anexo Técnico: Auditoría Premium SEO + GEO IA</div>
    <article class="card amber">
      <div class="card-top">
        <span class="card-title">🔍 Los 16 Parámetros de Visibilidad en Google e IA</span>
        <span class="price-tag amber">195 € en Dúo+</span>
      </div>
      <ul class="list-check">
        <li><span class="chk">✔</span><span><strong>Inyección de código estructurado Schema.org JSON-LD:</strong> entidades <code>LocalBusiness</code>, <code>AggregateRating</code> y <code>FAQPage</code> para que ChatGPT, Gemini y Perplexity lean tus datos sin errores.</span></li>
        <li><span class="chk">✔</span><span><strong>Optimización de cabeceras Web:</strong> etiquetas <code>&lt;title&gt;</code>, <code>&lt;meta description&gt;</code> y jerarquía semántica <code>H1/H2</code> orientada a búsquedas locales.</span></li>
        <li><span class="chk">✔</span><span><strong>Optimización de Google Business Profile:</strong> descripción oficial, categorías secundarias, atributos y catálogo de servicios.</span></li>
      </ul>
    </article>
    """
    return plantilla_base_movil(
        titulo="Anexo Técnico de Setup y Auditoría SEO + GEO",
        subtitulo="Desglose de los trabajos de ingeniería de puesta en marcha y optimización para buscadores e Inteligencias Artificiales.",
        badge="Ingeniería de Puesta en Marcha",
        url_impreso="setup.html",
        url_volver="../index.html#tarifas",
        contenido_html=cuerpo
    )


def construir_catalogo_movil():
    cuerpo = """
    <div class="section-head">I. Reputación y Visibilidad (Activos Hoy)</div>

    <article class="card amber">
      <div class="card-top">
        <span class="card-title">★ Atril Inteligente de Mostrador (NFC + QR)</span>
        <span class="price-tag amber">39 € Único</span>
      </div>
      <p>Soporte físico de metacrilato con chip NFC y código QR. El cliente acerca su móvil al pagar y abre tu pantalla de reseñas de Google Maps en <strong>1 segundo</strong>. Sin cuotas mensuales.</p>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <span class="card-title">1. Gestión y Respuesta de Reseñas en Google con IA</span>
        <span class="price-tag">59 € / mes</span>
      </div>
      <p>Responde y publica automáticamente en las reseñas de 4 y 5★ en el idioma del cliente potenciando tu SEO local. En reseñas de 1 a 3★ frena la publicación y te envía alerta urgente con tu <strong>Gestor de 4 Tonos (Formal, Semiformal, Cercano, Directo)</strong>, método HEARD y blindaje RGPD.</p>
    </article>

    <article class="card emerald">
      <div class="card-top">
        <span class="card-title">2. Filtrado y Captación de Reseñas (Encuesta WhatsApp)</span>
        <span class="price-tag">59 € / mes</span>
      </div>
      <p>Mensaje oficial de WhatsApp 2h tras la cita con 3 botones: <strong>«Excelente»</strong> (lleva en 1 toque a Google Maps), <strong>«Bien»</strong> y <strong>«Mejorable»</strong> (retienen la sugerencia o queja en privado por texto o nota de voz transcrita por IA).</p>
    </article>

    <article class="card amber">
      <div class="card-top">
        <span class="card-title">🔍 Auditoría e Implantación Premium SEO + GEO (IA)</span>
        <span class="price-tag amber">195 € en Dúo+</span>
      </div>
      <p>Traduce tu web y tu ficha de Google Maps al lenguaje interno de <strong>ChatGPT, Gemini y Google</strong> (código Schema.org JSON-LD + 16 parámetros). Suelta: 200 € (solo código) o 350 € (llave en mano). Bonificada a <strong>195 € con Pack Escudo</strong> o <strong>95 € en Plan Anual Trinity+</strong>.</p>
    </article>

    <div class="section-head blue">II. Facturación y Cierre de Ventas (Hoja de Ruta)</div>

    <article class="card blue">
      <div class="card-top"><span class="card-title">3. Leads en 10s + Extractor de Portales</span><span class="price-tag">+40 €/m</span></div>
      <p>WhatsApp inmediato en 10 segundos a quien pide presupuesto en tu web, redes o portales, con aviso urgente a tu móvil para cerrar en caliente.</p>
    </article>

    <article class="card blue">
      <div class="card-top"><span class="card-title">4. Rescate Automático de Llamadas Perdidas</span><span class="price-tag">+40 €/m</span></div>
      <p>Si no puedes atender el teléfono, envía un WhatsApp formal a los 5 segundos reteniendo al cliente antes de que llame a otro negocio.</p>
    </article>

    <article class="card blue">
      <div class="card-top"><span class="card-title">5. Reactivación de Clientes Inactivos</span><span class="price-tag">+40 €/m</span></div>
      <p>Detecta clientes que llevan más de 60-90 días sin acudir y les envía una invitación personalizada por WhatsApp para volver.</p>
    </article>

    <div class="section-head indigo">III. Ahorro de Tiempo y Gestión</div>

    <article class="card indigo">
      <div class="card-top"><span class="card-title">6. Sistema Anti-Plantón + Campañas Flash</span><span class="price-tag">+40 €/m</span></div>
      <p>Recordatorio 24h antes por WhatsApp con botones de Confirmar o Reubicar, cubriendo huecos libres automáticamente con tu lista de espera.</p>
    </article>

    <article class="card indigo">
      <div class="card-top"><span class="card-title">7. Centralita de Voz y Citas con IA (24/7)</span><span class="price-tag">+40 €/m</span></div>
      <p>Agente telefónico con voz natural que atiende llamadas, resuelve dudas y agenda citas en tu calendario.</p>
    </article>

    <article class="card indigo">
      <div class="card-top"><span class="card-title">8. Firma de Presupuestos + Onboarding IA</span><span class="price-tag">+40 €/m</span></div>
      <p>Firma digital legal desde el móvil y puesta en marcha automática del expediente del cliente.</p>
    </article>

    <article class="card indigo">
      <div class="card-top"><span class="card-title">9. Facturas y Gastos al Gestor con IA</span><span class="price-tag">+40 €/m</span></div>
      <p>Envía una foto del ticket o factura por WhatsApp y la IA extrae NIF, base e IVA directo al Excel de tu gestoría (+ Add-on Correo opcional).</p>
    </article>

    <article class="card indigo">
      <div class="card-top"><span class="card-title">10. Anti-Morosidad Diplomático</span><span class="price-tag">+40 €/m</span></div>
      <p>Seguimiento neutral de facturas vencidas por WhatsApp con enlace de pago (+ Add-on Proveedores opcional).</p>
    </article>
    """
    return plantilla_base_movil(
        titulo="Dossier Completo de Servicios (Fase 1 y Fase 2)",
        subtitulo="Catálogo integral de soluciones tácticas de reputación, posicionamiento GEO IA, captación y eficiencia.",
        badge="Dossier Oficial Sistemas Pyme",
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


def inyectar_autoredireccion_inteligente_en_original(ruta_original, nombre_archivo_movil):
    if not os.path.isfile(ruta_original):
        return
    with open(ruta_original, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # Limpiar posibles redirecciones previas
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


def inyectar_router_inteligente_en_index(ruta_index):
    if not os.path.isfile(ruta_index):
        return
    with open(ruta_index, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

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
      if (mapaMovil[href] && esDispositivoMovilSP()) {
        e.preventDefault();
        e.stopPropagation();
        window.location.href = mapaMovil[href];
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


def ejecutar_creacion_y_coordinacion_movil():
    print("=" * 82)
    print("📱 CREANDO DOCUMENTOS ESPECÍFICOS PARA MÓVIL Y ENRUTADOR INTELIGENTE (MÓVIL vs PC)")
    print("=" * 82)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ No se encontró public_html.")
        return

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Backup de index.html
    ruta_index = os.path.join(dir_raiz, "index.html")
    shutil.copy2(ruta_index, os.path.join(carpeta_backups, f"index.html.backup_{marca_tiempo}"))

    dir_docs = os.path.join(dir_raiz, "documentos")
    dir_arts = os.path.join(dir_raiz, "articulos")
    os.makedirs(dir_docs, exist_ok=True)
    os.makedirs(dir_arts, exist_ok=True)

    # 1. Crear los 5 archivos específicos para móvil
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
        print(f"   ✔ Creado documento nativo para móvil: {os.path.relpath(ruta_movil, dir_raiz)}")

        if os.path.isfile(ruta_orig):
            inyectar_autoredireccion_inteligente_en_original(ruta_orig, nombre_corto_movil)
            print(f"   ✔ Conectada detección móvil automática en: {os.path.relpath(ruta_orig, dir_raiz)}")

    # 2. Inyectar el enrutador inteligente en index.html
    inyectar_router_inteligente_en_index(ruta_index)
    print("   ✔ Conectado enrutador inteligente en index.html (Móvil -> *_movil.html | PC -> Original).")
    print("=" * 82)
    print("🚀 PROCESO COMPLETADO: Documentos móviles con letra grande y detección inteligente listos.")
    print("=" * 82)


if __name__ == "__main__":
    ejecutar_creacion_y_coordinacion_movil()
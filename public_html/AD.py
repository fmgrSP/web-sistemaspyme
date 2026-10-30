import os
import re

# ==============================================================================
# CREDENCIALES OFICIALES DE ANALÍTICA DE SISTEMAS PYME
# ==============================================================================
GA4_MEASUREMENT_ID = "G-J8Y61HLB7L"
CLARITY_PROJECT_ID = "z5k1bnidx3"


def localizar_directorio_public_html():
    home = os.path.expanduser("~")
    rutas = [
        os.path.join(home, "Desktop", "SISTEMAS PYME", "Web", "web-sistemaspyme", "public_html"),
        os.path.join(home, "Escritorio", "SISTEMAS PYME", "Web", "web-sistemaspyme", "public_html"),
        os.path.abspath("."),
        os.path.abspath("public_html"),
    ]
    for r in rutas:
        if os.path.isdir(r) and os.path.isfile(os.path.join(r, "index.html")):
            return r
    return None


# ==============================================================================
# 1. CONTENIDO DE PYME_MAGAZINE_N1.HTML (FORMATO A4 REAL AUTOENCUADRADO CON LETRA GRANDE)
# ==============================================================================
PYME_MAGAZINE_N1_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Pyme Magazine Nº 1 — La Nueva Regla del «Boca a Boca» | Sistemas Pyme</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,700;0,800;1,600&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4 portrait;
      margin: 0;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    :root {
      --navy: #0b2545;
      --dark: #071629;
      --teal: #0d7d74;
      --teal-light: #f0fdfa;
      --emerald: #10b981;
      --amber: #d97706;
      --slate-50: #f8fafc;
      --slate-100: #f1f5f9;
      --slate-200: #e2e8f0;
      --slate-600: #475569;
      --slate-700: #334155;
      --slate-800: #1e293b;
    }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #071629;
      color: #0f172a;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 14px 8px 48px 8px;
      gap: 18px;
    }
    .top-bar {
      position: sticky;
      top: 10px;
      z-index: 999;
      width: 100%;
      max-width: 210mm;
      background: rgba(11, 37, 69, 0.96);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(20, 184, 166, 0.45);
      border-radius: 14px;
      padding: 10px 16px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.55);
      color: #fff;
    }
    .top-bar-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .btn-nav {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
      text-decoration: none;
      font-weight: 700;
      font-size: 13px;
      padding: 8px 14px;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      transition: all 0.2s;
      cursor: pointer;
    }
    .btn-nav:hover {
      background: #0d7d74;
      border-color: #14b8a6;
    }
    .btn-nav.primary {
      background: #0d7d74;
      border-color: #2dd4bf;
    }
    .btn-nav.amber {
      background: #d97706;
      border-color: #fbbf24;
    }
    .a4-page {
      width: 100%;
      max-width: 210mm;
      background: #ffffff;
      border-radius: 10px;
      padding: 12mm 14mm;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.65);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }
    @media (max-width: 768px) {
      body {
        padding: 8px 4px 36px 4px;
        gap: 14px;
      }
      .a4-page {
        padding: 20px 16px;
        border-radius: 12px;
      }
    }
    @media print {
      body {
        background: none !important;
        padding: 0 !important;
        gap: 0 !important;
      }
      .no-print {
        display: none !important;
      }
      .a4-page {
        width: 210mm !important;
        min-height: 297mm !important;
        max-height: 297mm !important;
        padding: 11mm 14mm !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        page-break-after: always !important;
      }
    }
    .mag-header {
      border-bottom: 3px solid var(--navy);
      padding-bottom: 10px;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 8px;
    }
    .mag-brand {
      font-size: 13px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: var(--teal);
    }
    .mag-issue {
      font-size: 12px;
      font-weight: 800;
      color: var(--slate-600);
      background: var(--slate-100);
      padding: 4px 10px;
      border-radius: 6px;
      border: 1px solid var(--slate-200);
    }
    .hero-article {
      background: linear-gradient(135deg, #0b2545 0%, #0d7d74 100%);
      color: #ffffff;
      border-radius: 12px;
      padding: 22px 24px;
      margin-bottom: 18px;
      box-shadow: 0 8px 20px rgba(11, 37, 69, 0.2);
    }
    .hero-kicker {
      display: inline-block;
      font-size: 11.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1px;
      background: rgba(255, 255, 255, 0.16);
      color: #5eead4;
      padding: 4px 10px;
      border-radius: 99px;
      margin-bottom: 10px;
    }
    .hero-title {
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 28px;
      line-height: 1.18;
      font-weight: 800;
      margin-bottom: 10px;
    }
    .hero-lead {
      font-size: 15px;
      line-height: 1.5;
      color: #e2e8f0;
      font-weight: 500;
    }
    .editorial-section {
      margin-bottom: 16px;
    }
    .sec-title {
      font-size: 18px;
      font-weight: 900;
      color: var(--navy);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
      border-left: 4px solid var(--teal);
      padding-left: 10px;
      line-height: 1.25;
    }
    .editorial-p {
      font-size: 14.5px;
      line-height: 1.62;
      color: var(--slate-800);
      margin-bottom: 10px;
    }
    .highlight-box {
      background: #f0fdfa;
      border: 1.5px solid #99f6e4;
      border-left: 5px solid var(--teal);
      border-radius: 10px;
      padding: 14px 16px;
      margin: 12px 0;
    }
    .highlight-box h4 {
      font-size: 15px;
      font-weight: 800;
      color: var(--navy);
      margin-bottom: 5px;
    }
    .highlight-box p {
      font-size: 14px;
      line-height: 1.55;
      color: var(--slate-700);
    }
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
      margin: 12px 0;
    }
    @media (max-width: 640px) {
      .grid-2 {
        grid-template-columns: 1fr;
      }
      .hero-title {
        font-size: 24px;
      }
      .editorial-p {
        font-size: 15.5px;
        line-height: 1.65;
      }
      .sec-title {
        font-size: 18.5px;
      }
    }
    .card-box {
      background: var(--slate-50);
      border: 1px solid var(--slate-200);
      border-radius: 10px;
      padding: 14px;
    }
    .card-box strong {
      display: block;
      font-size: 15px;
      color: var(--navy);
      margin-bottom: 5px;
    }
    .card-box p {
      font-size: 13.8px;
      line-height: 1.52;
      color: var(--slate-700);
    }
    .page-footer {
      border-top: 1.5px solid var(--slate-200);
      padding-top: 10px;
      margin-top: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: var(--slate-600);
      font-weight: 600;
      flex-wrap: wrap;
      gap: 6px;
    }
  </style>
</head>
<body>

  <nav class="top-bar no-print">
    <div class="top-bar-left">
      <a href="../index.html#magazine" class="btn-nav">← Volver a la Web</a>
      <a href="../index.html#play-podcast" class="btn-nav amber">🎧 Escuchar en Podcast</a>
    </div>
    <div style="display:flex; gap:8px; flex-wrap:wrap;">
      <button type="button" onclick="window.print()" class="btn-nav primary">🖨️ Imprimir / Guardar PDF A4</button>
    </div>
  </nav>

  <!-- PÁGINA 1 -->
  <article class="a4-page">
    <div>
      <header class="mag-header">
        <div>
          <div class="mag-brand">📖 PYME MAGAZINE • PUBLICACIÓN EJECUTIVA DE SISTEMAS PYME</div>
          <div style="font-size: 12.5px; color: #475569; font-weight: 600; margin-top: 2px;">Ingeniería de Reputación, Automatización e Inteligencia Artificial para Negocios Locales</div>
        </div>
        <span class="mag-issue">FASCÍCULO Nº 1 • EDICIÓN OFICIAL</span>
      </header>

      <div class="hero-article">
        <span class="hero-kicker">Informe Especial • Psicología del Consumidor y Google Maps</span>
        <h1 class="hero-title">La Nueva Regla del «Boca a Boca»: Por qué 10 clientes felices callan mientras 1 enfadado hunde tu nota media</h1>
        <p class="hero-lead">
          El 97% de los clientes mira tus estrellas en Google Maps y pregunta a ChatGPT o Gemini antes de cruzar tu puerta. Descubre el «Efecto Umbral», el juego oculto de los Google Local Guides y cómo blindar tu negocio en piloto automático.
        </p>
      </div>

      <section class="editorial-section">
        <h2 class="sec-title">01. El «Efecto Umbral» (Doorway Effect) y la Asimetría del Silencio</h2>
        <p class="editorial-p">
          Piensa en lo que ocurre todos los días en cualquier clínica, taller mecánico, restaurante o comercio: atiendes de diez a un cliente, te da las gracias con una sonrisa y le pides amablemente si puede dejarte una reseña en Google cuando llegue a casa. El cliente te dice que sí con total sinceridad. Sin embargo, <strong>en cuanto cruza la puerta de tu local, se sube al coche y entra al tráfico, su cerebro borra la tarea</strong>.
        </p>
        <p class="editorial-p">
          La neurociencia denomina a este fenómeno <strong>«Efecto Umbral»</strong>: al cambiar de escenario físico, la memoria de trabajo archiva lo anterior. ¿El resultado? <strong>Más del 90% de tus clientes encantados jamás llegan a escribir su reseña</strong>, mientras que el único cliente que sufrió un malentendido mantiene el cortisol alto durante dos horas y escribe una crítica de 1 estrella que leen miles de vecinos.
        </p>

        <div class="highlight-box">
          <h4>💡 La Solución en Mostrador o Mesas: Captura en 1 Segundo antes de cruzar la puerta</h4>
          <p>
            Con el <strong>Atril Inteligente de Mostrador (NFC + QR)</strong> (39 € la 1ª unidad, o 29 €/ud. adicional y 25 €/ud. en packs de 5+ para negocios con varias mesas, gabinetes o tocadores), el cliente acerca su móvil al pagar y se le abre tu pantalla oficial de 5★ en <strong>1 segundo</strong>, antes de salir por la puerta.
          </p>
        </div>
      </section>

      <section class="editorial-section">
        <h2 class="sec-title">02. El Secreto de los «Google Local Guides» y la Trampa del «Efecto Loro»</h2>
        <p class="editorial-p">
          Google premia con puntos e insignias a millones de usuarios llamados <strong>Local Guides</strong> por escribir reseñas largas. Para el algoritmo de Google Maps, una reseña de un Local Guide pesa hasta 10 veces más y se clava arriba del todo en tu ficha durante meses.
        </p>
        <div class="grid-2">
          <div class="card-box">
            <strong>❌ El Error Fatal: El «Efecto Loro» en SEO</strong>
            <p>
              Cuando un dueño enfadado responde diciendo: <em>«No es verdad que seamos caros ni que el trato en nuestra clínica fuera lento»</em>, está repitiendo las palabras clave negativas (<strong>caro, lento</strong>). El robot de Google indexa tus propias palabras y hunde tu posicionamiento.
            </p>
          </div>
          <div class="card-box">
            <strong>✅ La Respuesta Inteligente con IA (Servicio 1)</strong>
            <p>
              En valoraciones de <strong>4 y 5★</strong>, nuestra IA publica al instante en el idioma del cliente inyectando tus servicios y ciudad para subirte en Google. Si entra una crítica (1 a 3★), <strong>pausa la publicación</strong> y te avisa al WhatsApp con tu <strong>Gestor de 4 Tonos</strong>.
            </p>
          </div>
        </div>
      </section>
    </div>

    <footer class="page-footer">
      <span><strong>Sistemas Pyme</strong> — Francisco M. Gallardo (Consultor Tecnológico • Tel: 711 54 75 61)</span>
      <span>sistemaspyme.es • Página 1 de 2</span>
    </footer>
  </article>

  <!-- PÁGINA 2 -->
  <article class="a4-page">
    <div>
      <header class="mag-header">
        <div>
          <div class="mag-brand">📖 PYME MAGAZINE • FASCÍCULO Nº 1</div>
          <div style="font-size: 12.5px; color: #475569; font-weight: 600; margin-top: 2px;">Protocolo HEARD, Blindaje RGPD, Cortafuegos de WhatsApp y las 2 Auditorías Gemelas</div>
        </div>
        <span class="mag-issue">CONTINUACIÓN • PÁG. 2</span>
      </header>

      <section class="editorial-section">
        <h2 class="sec-title">03. Protocolo Psicológico HEARD y Blindaje Médico/Legal RGPD</h2>
        <p class="editorial-p">
          Una respuesta a una reseña de 1 estrella <strong>no se escribe para convencer a quien puso la queja, sino para seducir a los 5.000 clientes futuros que la van a leer</strong>. Nuestro motor aplica el protocolo de Disney <strong>HEARD</strong> (Escuchar, Empatizar, Disculpar sin admitir falsedades, Resolver en privado y Diagnosticar) junto con un <strong>Escudo RGPD estricto</strong>: jamás confirma que el autor sea paciente o cliente (evitando multas de la AEPD de hasta 10.000 € en clínicas, asesorías y despachos).
        </p>
      </section>

      <section class="editorial-section">
        <h2 class="sec-title">04. El Cortafuegos Preventivo por WhatsApp (Servicio 2)</h2>
        <p class="editorial-p">
          La mejor reseña de 1 estrella es la que jamás llega a escribirse en Google. Con el <strong>Servicio 2: Filtrado y Captación de Reseñas (Encuesta Inteligente)</strong>, dos horas después de su cita o visita el cliente recibe un WhatsApp cercano con tres botones:
        </p>
        <div class="grid-2">
          <div class="card-box" style="background:#f0fdf4; border-color:#86efac;">
            <strong style="color:#166534;">🌟 Si pulsa «Excelente» → Directo a Google Maps</strong>
            <p>
              Le abrimos tu pantalla oficial de valoración en Google Maps en un solo toque desde el sofá de su casa, multiplicando hasta por 4 tu ritmo mensual de reseñas de 5 estrellas reales.
            </p>
          </div>
          <div class="card-box" style="background:#fffbeb; border-color:#fcd34d;">
            <strong style="color:#b45309;">🛡️ Si pulsa «Bien» o «Mejorable» → Retención Privada</strong>
            <p>
              Frena el envío a Google y le invita a contarte qué ocurrió por texto o <strong>nota de voz en privado</strong>. Nuestra IA transcribe el audio y te avisa al móvil al instante para solucionarlo en casa.
            </p>
          </div>
        </div>
      </section>

      <section class="editorial-section">
        <h2 class="sec-title">05. El Doble Escáner: Auditoría 1 (SEO+GEO IA) y Auditoría 2 (Neuromarketing CRO)</h2>
        <p class="editorial-p">
          Tener una reputación impecable se multiplica cuando tu web domina los dos lados de la moneda comercial:
        </p>
        <div class="grid-2">
          <div class="card-box">
            <strong>🔍 Auditoría 1: SEO Local + GEO (IA) — «Que te encuentren»</strong>
            <p>
              Escáner de 16 parámetros e inyección de código <code>Schema.org JSON-LD</code>, <code>llms.txt</code> y optimización de Google Maps para que <strong>ChatGPT, Gemini, Perplexity y Google</strong> recomienden tu negocio el primero.
            </p>
          </div>
          <div class="card-box">
            <strong>🧠 Auditoría 2: Neuromarketing y CRO — «Que te compren»</strong>
            <p>
              Radiografía psicológica (Kahneman, Ley de Hick) y mapas térmicos para detectar por qué se escapan las visitas de tu web, eliminar fricciones en formularios y disparar los contactos por WhatsApp.
            </p>
          </div>
        </div>

        <div class="highlight-box" style="background: linear-gradient(135deg, #0b2545 0%, #095852 100%); border-color:#14b8a6; color:#fff;">
          <h4 style="color:#5eead4; font-size:16px;">🚀 Oferta Estrella: Pack Escudo (99 €/mes) + Auditorías Bonificadas (195 € c/u)</h4>
          <p style="color:#f1f5f9; font-size:13.8px;">
            • <strong>Pack Escudo Básico (S1 + S2):</strong> <strong>99 €/mes</strong> (+225 € Setup Dúo).<br>
            • <strong>Ventaja en cualquiera de las 2 Auditorías:</strong> Sueltas cuestan 200 € (solo diagnóstico/código) o 350 € (llave en mano), pero al activar tu Pack Escudo o Plan Dúo+ te regalamos los 150 € de implantación y cada auditoría se queda en solo <strong>195 € pago único</strong> (o <strong>95 € c/u</strong> en Plan Anual Trinity+).
          </p>
        </div>
      </section>
    </div>

    <footer class="page-footer">
      <span>📞 Solicita tu diagnóstico gratuito por WhatsApp: <strong>711 54 75 61</strong> • francisco@sistemaspyme.es</span>
      <span>sistemaspyme.es • Página 2 de 2</span>
    </footer>
  </article>

</body>
</html>
"""


def actualizar_pyme_magazine(dir_raiz):
    carpeta_art = os.path.join(dir_raiz, "articulos")
    os.makedirs(carpeta_art, exist_ok=True)
    ruta_n1 = os.path.join(carpeta_art, "Pyme_Magazine_N1.html")
    with open(ruta_n1, "w", encoding="utf-8") as f:
        f.write(PYME_MAGAZINE_N1_HTML)
    print("   ✔ articulos/Pyme_Magazine_N1.html restaurado en formato A4 auto-encuadrado con letra grande (sin redirección móvil).")

    # Si existía Pyme_Magazine_N1_movil.html, le ponemos el mismo contenido A4 por si algún enlace antiguo apuntaba ahí
    ruta_n1_movil = os.path.join(carpeta_art, "Pyme_Magazine_N1_movil.html")
    if os.path.isfile(ruta_n1_movil):
        with open(ruta_n1_movil, "w", encoding="utf-8") as f:
            f.write(PYME_MAGAZINE_N1_HTML)


def adaptar_8_documentos_web(dir_raiz):
    carpeta_docs = os.path.join(dir_raiz, "documentos")
    if not os.path.isdir(carpeta_docs):
        print("⚠️ No se encontró la carpeta documentos/")
        return

    archivos_docs = [
        "catalogo.html",
        "catalogo_movil.html",
        "tarifas.html",
        "tarifas_movil.html",
        "setup.html",
        "setup_movil.html",
        "desembolso.html",
        "desembolso_movil.html",
    ]

    for nombre in archivos_docs:
        ruta = os.path.join(carpeta_docs, nombre)
        if not os.path.isfile(ruta):
            continue

        with open(ruta, "r", encoding="utf-8") as f:
            html = f.read()

        original = html

        # 1. Adaptar mención del Atril Inteligente (39 € + escala multi-puesto 29 € / 25 €) si aún no la tiene
        if "Ud. extra: 29 €" not in html and "29 €/ud" not in html:
            html = html.replace(
                "Pago Único: 39 €",
                "Pago Único: 39 € (Ud. extra: 29 € | 5+: 25 €)"
            )
            html = html.replace(
                "Pago único: 39 €",
                "Pago único: 39 € (Ud. extra: 29 € | 5+: 25 €)"
            )

        # 2. Adaptar títulos y descripciones de la Auditoría para incluir las 2 Auditorías Gemelas (SEO+GEO y Neuromarketing CRO)
        if "Neuromarketing" not in html and "Neuro CRO" not in html:
            # Títulos en Catálogo, Tarifas, Setup y Desembolso
            html = html.replace(
                "Auditoría e Implantación Premium SEO Local + GEO (IA)",
                "2 Auditorías de Ingeniería: (1) SEO Local + GEO IA y (2) Neuromarketing + Conversión Web (CRO)"
            )
            html = html.replace(
                "Auditoría Premium SEO Local + GEO (IA)",
                "Auditorías Premium: SEO+GEO (IA) y Neuromarketing Web (CRO)"
            )
            html = html.replace(
                "Auditoría SEO + GEO (IA)",
                "Auditorías SEO+GEO y Neuro CRO"
            )
            html = html.replace(
                "Auditoría SEO/GEO",
                "Auditorías SEO/GEO o Neuro CRO"
            )
            html = html.replace(
                "Auditoría GEO",
                "Auditoría (GEO o Neuro CRO)"
            )

            # Descripciones explicando las dos auditorías con el mismo precio por unidad (200 € / 350 € / 195 € c/u / 95 € c/u)
            html = html.replace(
                "Escáner de 16 parámetros e inyección de código Schema.org JSON-LD, etiquetas Meta/H1 y textos optimizados.",
                "Elige 1 o combina ambas (misma tarifa por auditoría: 200 € diagnóstico/código | 350 € llave en mano | <strong>195 € c/u con Pack Escudo/Dúo+</strong> | <strong>95 € c/u en Plan Anual Trinity+</strong>): <strong>1) Auditoría SEO+GEO IA</strong> (Schema.org JSON-LD y Google Maps para salir en ChatGPT/Google) y <strong>2) Auditoría de Neuromarketing y CRO</strong> (mapas de calor, psicología de conversión y eliminación de fugas de ventas)."
            )

        if html != original:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"   ✔ Adaptado con las 2 Auditorías Gemelas y Multi-Atril: documentos/{nombre}")
        else:
            print(f"   ✔ Ya estaba sincronizado: documentos/{nombre}")


if __name__ == "__main__":
    print("=" * 85)
    print("🚀 PASO 2: ACTUALIZANDO LOS 8 DOCUMENTOS WEB + RESTAURANDO PYME MAGAZINE N1 (A4 REAL)")
    print("=" * 85)
    d = localizar_directorio_public_html()
    if d:
        actualizar_pyme_magazine(d)
        adaptar_8_documentos_web(d)
    print("=" * 85)
    print("🎉 ¡PASO 2 COMPLETADO! Los 8 documentos y Pyme Magazine Nº 1 están listos.")
    print("=" * 85)
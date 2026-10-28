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

    for esc in [os.path.join(home, "Desktop"), os.path.join(home, "Escritorio")]:
        if not os.path.isdir(esc):
            continue
        for raiz, dirs, archivos in os.walk(esc):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("backups_sp", "Backups", "node_modules")]
            if "index.html" in archivos and os.path.basename(raiz) == "public_html":
                return raiz
    return None


def construir_desplegable_auditoria_completo():
    """
    Construye el nuevo desplegable técnico de la Auditoría SEO + GEO mucho más completo,
    estructurado en los 6 pilares de ingeniería del documento oficial.
    """
    return """            <!-- JERGA DE INGENIERO ENCAPSULADA EN DESPLEGABLE TÉCNICO COMPLETO (6 PILARES GEO/LLMO) -->
            <details class="group bg-black/40 border border-teal-500/40 rounded-xl px-4 py-3 text-xs text-slate-300 cursor-pointer transition-all">
              <summary class="font-bold text-teal-300 flex items-center justify-between select-none">
                <span>🛠️ Ver especificaciones técnicas de ingeniería incluidas (Para informáticos, agencias y dirección técnica)</span>
                <span class="text-teal-400 group-open:rotate-180 transition-transform ml-2">▼</span>
              </summary>
              <div class="pt-3 mt-3 border-t border-white/10 text-[11.5px] text-slate-300 leading-relaxed space-y-2.5">
                <p class="text-teal-200 font-semibold">
                  Despliegue técnico basado en arquitectura de Entidades Verificadas para el <em>Knowledge Graph</em> de Google y sistemas <strong>RAG (Retrieval-Augmented Generation)</strong> de SearchGPT, Perplexity, Gemini y Claude:
                </p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2.5 pt-1">
                  <div class="bg-slate-950/80 border border-white/10 rounded-lg p-2.5">
                    <strong class="text-emerald-400 block mb-0.5">1. Grafo Conectado Schema.org JSON-LD (@graph):</strong>
                    Inyección de subclase sectorial exacta (<code>Dentist</code>, <code>MedicalClinic</code>, <code>AutoRepair</code>, <code>Restaurant</code>, <code>LegalService</code>...) con nodos <code>@id</code>, <code>GeoCoordinates</code> de alta precisión, <code>hasOfferCatalog</code>, <code>AggregateRating</code>, <code>FAQPage</code> y desambiguación semántica mediante enlaces <code>sameAs</code> hacia <strong>Wikidata y Wikipedia</strong> en <code>areaServed</code> y <code>knowsAbout</code>.
                  </div>
                  <div class="bg-slate-950/80 border border-white/10 rounded-lg p-2.5">
                    <strong class="text-emerald-400 block mb-0.5">2. Reingeniería de GBP, Bing Places y NAP+W:</strong>
                    Selección quirúrgica de categoría primaria y hasta 9 secundarias en <strong>Google Business Profile</strong>, alta y sincronización en <strong>Bing Places</strong> (índice base de SearchGPT/OpenAI), catálogo de servicios long-tail con precios y estandarización carácter por carácter de tu <strong>NAP+W</strong>.
                  </div>
                  <div class="bg-slate-950/80 border border-white/10 rounded-lg p-2.5">
                    <strong class="text-emerald-400 block mb-0.5">3. Arquitectura On-Page «RAG-Friendly»:</strong>
                    Optimización de <code>&lt;title&gt;</code>, <code>&lt;meta description&gt;</code>, <code>canonical</code>, geo-tags (<code>ICBM</code> / <code>geo.position</code>) y jerarquía <code>H1/H2/H3</code> que replica prompts conversacionales reales con bloques de respuesta directa en las primeras 40 palabras y datos cuantitativos.
                  </div>
                  <div class="bg-slate-950/80 border border-white/10 rounded-lg p-2.5">
                    <strong class="text-emerald-400 block mb-0.5">4. Apertura a Agentes de IA (robots.txt + llms.txt):</strong>
                    Configuración de reglas de acceso para permitir la indexación y lectura en tiempo real a <code>OAI-SearchBot</code>, <code>ChatGPT-User</code>, <code>PerplexityBot</code>, <code>Google-Extended</code>, <code>ClaudeBot</code> y <code>bingbot</code>, junto con despliegue del archivo estándar <code>/llms.txt</code> y <code>sitemap.xml</code>.
                  </div>
                  <div class="bg-slate-950/80 border border-white/10 rounded-lg p-2.5">
                    <strong class="text-emerald-400 block mb-0.5">5. Ingeniería de Señales de Reseñas (UGC + Velocity):</strong>
                    Inducción semántica en solicitudes de reseña para que el usuario mencione servicio y ciudad de forma natural, más respuestas en &lt;24h con co-ocurrencia local.
                  </div>
                  <div class="bg-slate-950/80 border border-white/10 rounded-lg p-2.5">
                    <strong class="text-emerald-400 block mb-0.5">6. Trazabilidad y Atribución Híbrida (UTM &amp; Zero-Click):</strong>
                    Etiquetado de enlaces (<code>utm_source=google&amp;utm_medium=organic_local</code>) para medir llamadas directas, rutas en Google Maps y referencias desde motores de IA.
                  </div>
                </div>
              </div>
            </details>"""


def construir_seccion_rag_con_conmutador_dual():
    """
    Construye la sección 'Por qué los Motores de IA recomiendan a nuestros clientes' con un
    conmutador interactivo arriba:
    - Modo Dueño de Negocio (En Cristiano / Sencillo) -> ACTIVO POR DEFECTO
    - Modo Informático / Técnico (Ingeniería GEO & RAG)
    """
    return """  <!-- [SP_RAG_FRIENDLY_SECTION_START] -->
  <section id="estrategia-geo-llmo" class="scroll-mt-24 py-14 md:py-20 bg-slate-950/95 border-t border-white/10 relative overflow-hidden">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">

      <!-- Cabecera + Conmutador Interactivo (Modo Sencillo vs Modo Informático) -->
      <div class="text-center max-w-3xl mx-auto mb-8">
        <span id="badgeTopGeoMode" class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-teal-500/15 border border-teal-400/40 text-teal-300 text-xs font-extrabold uppercase tracking-wider mb-3">
          <span>🧭 Explicado de Forma Sencilla • Cómo te encuentran más clientes</span>
        </span>
        <h2 class="text-2xl sm:text-3xl lg:text-4xl font-black text-white tracking-tight leading-tight">
          Por qué los Motores de IA (ChatGPT, Gemini y Perplexity) y Google Maps Recomiendan a Nuestros Clientes
        </h2>
        <p id="introGeoMode" class="text-slate-300 text-sm sm:text-base mt-3 leading-relaxed">
          Hoy tus clientes ya no solo buscan en Google: también le preguntan directamente a <strong>ChatGPT o al móvil</strong> qué clínica, taller, restaurante o profesional es el más fiable de su zona. Así conseguimos que te elijan a ti:
        </p>

        <!-- BOTÓN CONMUTADOR DUAL: EXPLICACIÓN SENCILLA VS MODO TÉCNICO INFORMÁTICO -->
        <div class="mt-6 flex flex-col items-center justify-center">
          <div class="bg-slate-900 p-1.5 rounded-2xl border border-teal-500/40 inline-flex flex-wrap items-center justify-center gap-1.5 shadow-xl">
            <button type="button" id="btnGeoMundano" onclick="cambiarModoExplicacionGeo('mundano')" class="px-4 sm:px-5 py-2.5 rounded-xl text-xs sm:text-sm font-black transition-all bg-brand-teal text-white shadow-md flex items-center gap-2">
              <span>👔</span>
              <span>Explicación Sencilla (Para Dueños de Negocio)</span>
            </button>
            <button type="button" id="btnGeoTecnico" onclick="cambiarModoExplicacionGeo('tecnico')" class="px-4 sm:px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition-all text-slate-300 hover:text-white flex items-center gap-2">
              <span>💻</span>
              <span>Modo Informático / Técnico (Ingeniería IA)</span>
            </button>
          </div>
          <p id="subtituloModoGeo" class="text-[11.5px] text-teal-300 font-semibold mt-2">
            ✨ Estás viendo la <strong>versión clara y sin tecnicismos</strong>. (Si eres informático o quieres ver qué código tocamos por dentro, pulsa en «Modo Informático»).
          </p>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- VISTA 1 (POR DEFECTO): EXPLICACIÓN SENCILLA / MUNDANA PARA DUEÑOS DE PYME -->
      <!-- ========================================================================= -->
      <div id="gridPilaresMundano" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
        <article class="bg-slate-900/90 border-2 border-teal-500/40 rounded-2xl p-5 flex flex-col justify-between shadow-lg">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black uppercase tracking-wider text-teal-300">Paso 1 • Tu Escaparate</span>
              <span class="text-lg">📍</span>
            </div>
            <h3 class="text-base font-black text-white mb-2">Tu Ficha de Google y Mapas al 100%</h3>
            <p class="text-xs text-slate-200 leading-relaxed">
              Colocamos tu negocio en las categorías exactas por las que pagan tus mejores clientes, subimos tu catálogo de servicios con precios claros y dejamos tu nombre, dirección y teléfono idénticos en Google, Apple Maps y Bing (el buscador que usa ChatGPT).
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 text-[11px] font-bold text-emerald-400">
            ✔ Entre un 15% y 25% más de llamadas directas
          </div>
        </article>

        <article class="bg-slate-900/90 border-2 border-teal-500/40 rounded-2xl p-5 flex flex-col justify-between shadow-lg">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black uppercase tracking-wider text-teal-300">Paso 2 • Tu Fama Real</span>
              <span class="text-lg">⭐</span>
            </div>
            <h3 class="text-base font-black text-white mb-2">Reseñas Constantes que Hablan de Ti</h3>
            <p class="text-xs text-slate-200 leading-relaxed">
              Conseguimos que tus clientes felices dejen reseñas todas las semanas mencionando qué servicio les hiciste y en qué ciudad estás, y que todas queden respondidas en menos de 24h. Al ver movimiento real y constante, Google te sube al Top 3 de tu zona.
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 text-[11px] font-bold text-emerald-400">
            ✔ Nota media de 4.8★ o superior asegurada
          </div>
        </article>

        <article class="bg-slate-900/90 border-2 border-teal-500/40 rounded-2xl p-5 flex flex-col justify-between shadow-lg">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black uppercase tracking-wider text-teal-300">Paso 3 • Tu Carné Digital</span>
              <span class="text-lg">🪪</span>
            </div>
            <h3 class="text-base font-black text-white mb-2">Traducimos tu Web al Idioma de las IAs</h3>
            <p class="text-xs text-slate-200 leading-relaxed">
              Las Inteligencias Artificiales no "ven" tu web como una persona: necesitan una ficha técnica interna. Se la instalamos a tu web para que Google y ChatGPT sepan sin ninguna duda a qué te dedicas, en qué barrios trabajas y por qué eres la opción más fiable.
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 text-[11px] font-bold text-emerald-400">
            ✔ Google y ChatGPT entienden tu negocio al 100%
          </div>
        </article>

        <article class="bg-slate-900/90 border-2 border-teal-500/40 rounded-2xl p-5 flex flex-col justify-between shadow-lg">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black uppercase tracking-wider text-teal-300">Paso 4 • Puerta Abierta IA</span>
              <span class="text-lg">🤖</span>
            </div>
            <h3 class="text-base font-black text-white mb-2">Pase VIP para ChatGPT y Gemini</h3>
            <p class="text-xs text-slate-200 leading-relaxed">
              Muchas páginas web bloquean sin querer a los robots de ChatGPT y Gemini. Nosotros les abrimos la puerta principal y les dejamos un resumen masticado con tus precios, horarios y ventajas para que te recomienden cuando alguien pregunte en tu ciudad.
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 text-[11px] font-bold text-emerald-400">
            ✔ Recomendado cuando preguntan a la IA en tu zona
          </div>
        </article>
      </div>

      <!-- ========================================================================= -->
      <!-- VISTA 2 (MODO INFORMÁTICO / TÉCNICO): INGENIERÍA DE ENTIDADES Y RAG       -->
      <!-- ========================================================================= -->
      <div id="gridPilaresTecnico" class="hidden grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
        <article class="bg-slate-900/90 border border-indigo-400/50 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black uppercase tracking-wider text-indigo-300">Pilar 1 • Google &amp; Bing</span>
              <span class="text-lg">📍</span>
            </div>
            <h3 class="text-base font-black text-white mb-2">Taxonomía GBP, Bing Places y NAP+W</h3>
            <p class="text-xs text-slate-300 leading-relaxed">
              Selección quirúrgica de tu <strong>categoría principal y hasta 9 secundarias</strong>, catálogo de servicios long-tail con precios claros, estandarización carácter por carácter de tu <strong>NAP+W</strong> (Name, Address, Phone + Website) y sincronización con <strong>Bing Places</strong> (el índice del que bebe SearchGPT).
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 text-[11px] font-bold text-emerald-400">
            ✔ +15-25% en acciones directas GBP (UTM)
          </div>
        </article>

        <article class="bg-slate-900/90 border border-indigo-400/50 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black uppercase tracking-wider text-indigo-300">Pilar 2 • Review Signals</span>
              <span class="text-lg">⭐</span>
            </div>
            <h3 class="text-base font-black text-white mb-2">Review Velocity y Semántica UGC</h3>
            <p class="text-xs text-slate-300 leading-relaxed">
              Flujo constante de reseñas reales (sin activar filtros anti-spam <em>Review Guard</em>) inducidas por WhatsApp para que el cliente mencione de forma natural el <strong>servicio realizado y tu localidad</strong>, respondidas al 100% en menos de 24h con refuerzo semántico local.
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 text-[11px] font-bold text-emerald-400">
            ✔ Nota media objetivo ≥ 4.8★ y SoLV en Geo-Grid
          </div>
        </article>

        <article class="bg-slate-900/90 border border-indigo-400/50 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black uppercase tracking-wider text-indigo-300">Pilar 3 • Grafo JSON-LD</span>
              <span class="text-lg">🧬</span>
            </div>
            <h3 class="text-base font-black text-white mb-2">Schema Conectado a Wikidata (@id)</h3>
            <p class="text-xs text-slate-300 leading-relaxed">
              Desambiguación total ante el <em>Knowledge Graph</em> mediante subclase específica de tu sector (<code>Dentist</code>, <code>MedicalClinic</code>, <code>AutoRepair</code>, <code>LegalService</code>...) enlazando <code>areaServed</code> y <code>knowsAbout</code> mediante propiedades <code>sameAs</code> a <strong>Wikidata y Wikipedia</strong>.
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 text-[11px] font-bold text-emerald-400">
            ✔ Entidad verificada sin ambigüedad semántica
          </div>
        </article>

        <article class="bg-slate-900/90 border border-indigo-400/50 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black uppercase tracking-wider text-indigo-300">Pilar 4 • Rastreo IA (RAG)</span>
              <span class="text-lg">🤖</span>
            </div>
            <h3 class="text-base font-black text-white mb-2">Apertura a Bots IA y Chunks RAG</h3>
            <p class="text-xs text-slate-300 leading-relaxed">
              Configuración de <code>robots.txt</code> y <code>llms.txt</code> autorizando a <strong>OAI-SearchBot, ChatGPT-User, PerplexityBot, Google-Extended y ClaudeBot</strong>, junto con bloques de Pregunta-Respuesta directa (&lt;40 palabras) y tablas de precios que aumentan un <strong>+40% la citación en IA</strong>.
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 text-[11px] font-bold text-emerald-400">
            ✔ Top 3 en Share of Model (SOM) local
          </div>
        </article>
      </div>

      <!-- BLOQUE DE PREGUNTAS FRECUENTES ESTRUCTURADAS EN FORMATO "RAG-FRIENDLY" (H2/H3 CONVERSACIONALES) -->
      <div class="rounded-3xl bg-slate-900/80 border border-white/10 p-6 sm:p-8">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6 border-b border-white/10 pb-4">
          <div>
            <span class="text-[11px] font-extrabold uppercase tracking-widest text-teal-400 block">Respuestas Directas Verificadas (Dudas Frecuentes)</span>
            <h2 class="text-xl sm:text-2xl font-black text-white">Preguntas Frecuentes sobre Automatización IA, Reseñas y Posicionamiento GEO Local</h2>
          </div>
          <span class="text-[11px] font-bold text-slate-400 bg-black/40 px-3 py-1 rounded-lg border border-white/10 self-start sm:self-center">
            Respuestas claras al grano
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 text-left">
          <article class="bg-slate-950/80 border border-white/10 rounded-2xl p-5">
            <h3 class="text-sm sm:text-base font-black text-teal-300 mb-2">
              ¿Cómo hacer que mi negocio local aparezca recomendado en ChatGPT, Google Gemini y Google Maps?
            </h3>
            <p class="text-xs sm:text-[13px] text-slate-200 leading-relaxed">
              Para ser recomendado por <strong>ChatGPT (SearchGPT), Gemini y Perplexity</strong>, un negocio local debe consolidarse como una <strong>Entidad Verificada</strong> mediante tres acciones: inyectar código estructurado <code>Schema.org JSON-LD</code> conectado a Wikidata, mantener consistencia exacta de sus datos (Nombre, Dirección, Teléfono y Web) entre Google Business Profile y Bing Places, y generar un flujo constante de reseñas de 5★ respondidas con palabras clave de su servicio y ciudad.
            </p>
          </article>

          <article class="bg-slate-950/80 border border-white/10 rounded-2xl p-5">
            <h3 class="text-sm sm:text-base font-black text-teal-300 mb-2">
              ¿Cuánto cuesta automatizar las reseñas de Google y la Auditoría SEO Local + GEO en Galicia y España?
            </h3>
            <p class="text-xs sm:text-[13px] text-slate-200 leading-relaxed">
              En <strong>Sistemas Pyme</strong> el 1er servicio troncal cuesta <strong>59 €/mes</strong> (Setup único de 150 €). Al unir 2 servicios en el <strong>Pack Escudo</strong> (Reseñas IA + Encuesta Cortafuegos WhatsApp), el 2º módulo suma solo <strong>+40 €/mes (99 €/mes en total)</strong> y desbloquea la <strong>Auditoría e Implantación SEO Local + GEO Llave en Mano por solo 195 € de pago único</strong> (en lugar de 350 €, ahorrando los 150 € de implantación técnica).
            </p>
          </article>

          <article class="bg-slate-950/80 border border-white/10 rounded-2xl p-5">
            <h3 class="text-sm sm:text-base font-black text-teal-300 mb-2">
              ¿Cómo funciona el cortafuegos preventivo por WhatsApp para frenar reseñas de 1 estrella?
            </h3>
            <p class="text-xs sm:text-[13px] text-slate-200 leading-relaxed">
              Tras la visita o servicio, el cliente recibe un mensaje oficial por <strong>WhatsApp Business API</strong> con tres botones: <strong>«Excelente»</strong>, <strong>«Bien»</strong> y <strong>«Mejorable»</strong>. Quien pulsa «Excelente» va directo en 1 toque a puntuar 5★ en Google Maps; quien pulsa «Bien» o «Mejorable» es atendido en un <strong>canal privado de texto o nota de voz transcrita por IA</strong>, alertando al propietario al instante antes de que publique una queja en internet.
            </p>
          </article>

          <article class="bg-slate-950/80 border border-white/10 rounded-2xl p-5">
            <h3 class="text-sm sm:text-base font-black text-teal-300 mb-2">
              ¿En qué ciudades y sectores trabaja Sistemas Pyme e implanta sus sistemas en 24-48 horas?
            </h3>
            <p class="text-xs sm:text-[13px] text-slate-200 leading-relaxed">
              Realizamos implantaciones presenciales y remotas en toda <strong>Galicia (Santiago de Compostela, A Coruña, Vigo, Pontevedra, Lugo, Ourense y comarcas)</strong> y en el resto de <strong>España</strong> para clínicas dentales y médicas, salones de estética y peluquería, talleres mecánicos, restaurantes, hoteles, inmobiliarias, instaladores, asesorías y despachos profesionales, dejando todo operativo en <strong>24 a 48 horas</strong> sin cambiar su software actual.
            </p>
          </article>
        </div>
      </div>

    </div>
  </section>
  <!-- [SP_RAG_FRIENDLY_SECTION_END] -->"""


def construir_js_conmutador_geo():
    return """    // CONMUTADOR DE EXPLICACIÓN DE LOS 4 PILARES IA: MUNDANO (DUEÑOS DE PYME) VS TÉCNICO (INFORMÁTICOS)
    function cambiarModoExplicacionGeo(modo) {
      const gridMundano = document.getElementById('gridPilaresMundano');
      const gridTecnico = document.getElementById('gridPilaresTecnico');
      const btnMundano = document.getElementById('btnGeoMundano');
      const btnTecnico = document.getElementById('btnGeoTecnico');
      const badgeTop = document.getElementById('badgeTopGeoMode');
      const intro = document.getElementById('introGeoMode');
      const sub = document.getElementById('subtituloModoGeo');

      if (!gridMundano || !gridTecnico) return;

      if (modo === 'tecnico') {
        gridMundano.classList.add('hidden');
        gridMundano.classList.remove('grid');
        gridTecnico.classList.remove('hidden');
        gridTecnico.classList.add('grid');

        if (btnTecnico) btnTecnico.className = "px-4 sm:px-5 py-2.5 rounded-xl text-xs sm:text-sm font-black transition-all bg-gradient-to-r from-indigo-600 to-teal-600 text-white shadow-lg flex items-center gap-2";
        if (btnMundano) btnMundano.className = "px-4 sm:px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition-all text-slate-300 hover:text-white flex items-center gap-2";
        if (badgeTop) badgeTop.innerHTML = '<span>🧠 Ingeniería de Entidades Verificadas • Knowledge Graph &amp; RAG</span>';
        if (intro) intro.innerHTML = 'Los motores de Inteligencia Artificial ya no buscan simples palabras clave: usan sistemas <strong>RAG (Generación Aumentada por Recuperación)</strong> que cruzan tu web, tu ficha de Google Maps/Bing Places y el sentimiento de tus reseñas para decidir qué único negocio recomendar en tu ciudad.';
        if (sub) sub.innerHTML = '💻 Estás viendo las <strong>especificaciones técnicas avanzadas (SEO Local + GEO / LLMO)</strong>. Pulsa en «Explicación Sencilla» para volver al lenguaje claro.';
      } else {
        gridTecnico.classList.add('hidden');
        gridTecnico.classList.remove('grid');
        gridMundano.classList.remove('hidden');
        gridMundano.classList.add('grid');

        if (btnMundano) btnMundano.className = "px-4 sm:px-5 py-2.5 rounded-xl text-xs sm:text-sm font-black transition-all bg-brand-teal text-white shadow-md flex items-center gap-2";
        if (btnTecnico) btnTecnico.className = "px-4 sm:px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition-all text-slate-300 hover:text-white flex items-center gap-2";
        if (badgeTop) badgeTop.innerHTML = '<span>🧭 Explicado de Forma Sencilla • Cómo te encuentran más clientes</span>';
        if (intro) intro.innerHTML = 'Hoy tus clientes ya no solo buscan en Google: también le preguntan directamente a <strong>ChatGPT o al móvil</strong> qué clínica, taller, restaurante o profesional es el más fiable de su zona. Así conseguimos que te elijan a ti:';
        if (sub) sub.innerHTML = '✨ Estás viendo la <strong>versión clara y sin tecnicismos</strong>. (Si eres informático o quieres ver qué código tocamos por dentro, pulsa en «Modo Informático»).';
      }
    }"""


def ejecutar_actualizacion():
    print("=" * 86)
    print("🚀 ACTUALIZANDO DESPLEGABLE AUDITORÍA, ORDEN DE GARANTÍAS Y BOTÓN MODO SENCILLO/TÉCNICO")
    print("=" * 86)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ No se encontró el directorio 'public_html' con 'index.html'.")
        return

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")

    ruta_index = os.path.join(dir_raiz, "index.html")
    ruta_bk = os.path.join(carpeta_backups, f"index.html.backup_{marca}")
    shutil.copy2(ruta_index, ruta_bk)
    print(f"📦 Backup automático creado en: {ruta_bk}")

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    cambios = 0

    # 1. Ampliar el desplegable técnico de la Auditoría SEO + GEO con los 6 pilares completos
    print("🔍 [1/4] Ampliando el desplegable de especificaciones técnicas en la Auditoría SEO + GEO...")
    patron_details = re.compile(
        r"<!-- JERGA DE INGENIERO ENCAPSULADA.*?-->\s*<details\b.*?</details>",
        re.DOTALL
    )
    if patron_details.search(html):
        html = patron_details.sub(construir_desplegable_auditoria_completo(), html, count=1)
        cambios += 1
        print("   ✔ Desplegable técnico de la Auditoría ampliado con los 6 bloques de ingeniería GEO/LLMO.")
    else:
        # Fallback buscando el summary directamente
        patron_details_alt = re.compile(
            r"<details\b[^>]*>\s*<summary[^>]*>\s*<span>🛠️ Ver especificaciones técnicas.*?</details>",
            re.DOTALL
        )
        if patron_details_alt.search(html):
            html = patron_details_alt.sub(construir_desplegable_auditoria_completo(), html, count=1)
            cambios += 1
            print("   ✔ Desplegable técnico de la Auditoría actualizado.")

    # 2. Actualizar la sección de los 4 Pilares de la IA con el Conmutador Sencillo / Informático
    print("🔍 [2/4] Actualizando los 4 pilares de Motores IA con el botón 'Explicación Sencilla' vs 'Modo Informático'...")
    patron_rag = re.compile(
        r"<!-- \[SP_RAG_FRIENDLY_SECTION_START\] -->.*?<!-- \[SP_RAG_FRIENDLY_SECTION_END\] -->",
        re.DOTALL
    )
    nueva_seccion_rag = construir_seccion_rag_con_conmutador_dual()
    if patron_rag.search(html):
        html = patron_rag.sub(nueva_seccion_rag, html, count=1)
        cambios += 1
        print("   ✔ Sección de Motores IA actualizada con el botón conmutador Dual (Sencillo por defecto / Técnico).")

    # 3. Reubicar "GARANTÍAS Y VENTAJAS OPERATIVAS" justo encima de "CIERRE Y LLAMADA A LA ACCIÓN (#contacto)"
    print("🔍 [3/4] Moviendo 'Garantías y Ventajas Operativas' justo encima de la sección final de Contacto...")
    patron_garantias = re.compile(
        r"\s*<!-- GARANTÍAS OPERATIVAS -->\s*<section\b[^>]*>.*?</section>",
        re.DOTALL
    )
    match_garantias = patron_garantias.search(html)
    if match_garantias:
        bloque_garantias = match_garantias.group(0).strip()
        # Quitamos el bloque de garantías de donde estaba
        html = patron_garantias.sub("", html, count=1)
        # Lo insertamos justo antes del cierre de Contacto (#contacto)
        patron_contacto = re.compile(r"(\s*<!-- CIERRE Y LLAMADA A LA ACCIÓN -->|\s*<section id=\"contacto\")")
        if patron_contacto.search(html):
            html = patron_contacto.sub(f"\n\n  {bloque_garantias}\\1", html, count=1)
            cambios += 1
            print("   ✔ Sección 'Garantías y Ventajas Operativas' colocada justo encima de Contacto.")

    # 4. Inyectar la función JS cambiarModoExplicacionGeo
    print("🔍 [4/4] Añadiendo lógica interactiva JavaScript para alternar entre Explicación Sencilla y Modo Informático...")
    html = re.sub(
        r"\s*// CONMUTADOR DE EXPLICACIÓN DE LOS 4 PILARES IA:.*?function cambiarModoExplicacionGeo\(modo\)\s*\{.*?\n    \}",
        "",
        html,
        flags=re.DOTALL
    )
    js_geo = construir_js_conmutador_geo()
    if "function cambiarModoTarifas(modo)" in html:
        html = html.replace("function cambiarModoTarifas(modo)", f"{js_geo}\n\n    function cambiarModoTarifas(modo)", 1)
        cambios += 1
        print("   ✔ Función 'cambiarModoExplicacionGeo' inyectada correctamente.")

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)

    print("=" * 86)
    print(f"🎉 PROCESO COMPLETADO: '{ruta_index}' actualizado con éxito ({cambios} mejoras aplicadas).")
    print("=" * 86)


if __name__ == "__main__":
    ejecutar_actualizacion()
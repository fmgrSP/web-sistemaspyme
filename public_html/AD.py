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


BLOQUE_CONSULTOR_SUPERIOR = """
  <!-- ======================================================================= -->
  <!-- BLOQUE CONSULTOR PRESCRIPTOR (DESCARGA COGNITIVA: NO TE ABRUMES)        -->
  <!-- ======================================================================= -->
  <section id="consultor-personal" class="relative z-20 -mt-6 pb-10 sm:pb-14 px-4 sm:px-6">
    <div class="max-w-6xl mx-auto">
      <div class="rounded-3xl bg-gradient-to-br from-slate-900 via-teal-950/50 to-slate-950 border-2 border-teal-400/60 p-6 sm:p-8 shadow-2xl shadow-teal-950/50 relative overflow-hidden">
        <div class="absolute -top-20 -right-20 w-64 h-64 bg-teal-400/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-teal-500/30">
          <div class="space-y-2 max-w-3xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/20 border border-teal-400/40 text-teal-300 text-xs font-extrabold uppercase tracking-wider">
              <span>🩺 Asesoramiento Directo de Consultor • Cero Agobios</span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-black text-white leading-tight">
              Tranquilo: no tienes que estudiarte toda esta web ni saber qué herramienta elegir.
            </h2>
            <p class="text-sm sm:text-base text-slate-200 leading-relaxed">
              Contamos con un catálogo muy completo porque resolvemos muchos problemas distintos, pero <strong>mi trabajo como tu consultor tecnológico es ponértelo fácil</strong>. Si te apetece, explora la web con calma; y si prefieres ir al grano, <strong>simplemente dime qué te pasa o qué te trae de cabeza en tu negocio</strong>. Yo analizo tu caso personalmente y de forma gratuita, te digo qué necesitas exactamente y me encargo de solucionarlo todo.
            </p>
          </div>

          <div class="flex-shrink-0">
            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20prefiero%20contarte%20directamente%20qu%C3%A9%20necesito%20mejorar%20en%20mi%20negocio%20para%20que%20me%20asesores%20t%C3%BA" target="_blank" class="w-full lg:w-auto inline-flex items-center justify-center gap-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-sm px-6 py-4 rounded-2xl shadow-lg shadow-emerald-950/60 transition-all hover:scale-[1.02]">
              <span>💬 Cuéntame tu caso por WhatsApp</span>
              <span>&rarr;</span>
            </a>
          </div>
        </div>

        <!-- 4 BOTONES RÁPIDOS DE "DOLORES REALES" DEL DUEÑO DE NEGOCIO -->
        <div class="pt-5">
          <p class="text-xs font-extrabold uppercase tracking-wider text-teal-300 mb-3.5">
            👇 Pulsa directamente sobre lo que más te preocupa hoy en tu negocio y hablamos:
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
            
            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20lo%20que%20m%C3%A1s%20me%20interesa%20es%20conseguir%20m%C3%A1s%20visibilidad%20en%20Google%20e%20IA%2C%20m%C3%A1s%20rese%C3%B1as%20de%205%20estrellas%20y%20frenar%20quejas.%20%C2%BFQu%C3%A9%20me%20recomiendas%3F" target="_blank" class="group text-left p-4 rounded-2xl bg-slate-950/85 hover:bg-teal-950/70 border border-teal-500/30 hover:border-teal-400 transition-all flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-xl">⭐</span>
                  <span class="text-[10px] font-bold uppercase tracking-wider text-teal-400 group-hover:translate-x-0.5 transition-transform">Consultar &rarr;</span>
                </div>
                <div class="text-sm font-black text-white mb-1">«Quiero salir primero en Google/IA y más 5★»</div>
                <p class="text-xs text-slate-400 leading-snug">Que me recomienden antes que a mi competencia y frenar reseñas injustas.</p>
              </div>
            </a>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20siento%20que%20entra%20gente%20a%20mi%20web%20o%20me%20piden%20presupuesto%20pero%20se%20escapan%20sin%20comprar.%20%C2%BFPuedes%20analizar%20d%C3%B3nde%20fallo%3F" target="_blank" class="group text-left p-4 rounded-2xl bg-slate-950/85 hover:bg-blue-950/70 border border-blue-500/30 hover:border-blue-400 transition-all flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-xl">💸</span>
                  <span class="text-[10px] font-bold uppercase tracking-wider text-blue-400 group-hover:translate-x-0.5 transition-transform">Consultar &rarr;</span>
                </div>
                <div class="text-sm font-black text-white mb-1">«Me entra gente a la web o llaman, pero se escapan»</div>
                <p class="text-xs text-slate-400 leading-snug">Detectar por qué no terminan comprando y responder presupuestos al instante.</p>
              </div>
            </a>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20pierdo%20demasiado%20tiempo%20con%20citas%2C%20plantones%2C%20llamadas%20o%20facturas%20para%20el%20gestor.%20%C2%BFC%C3%B3mo%20puedo%20automatizarlo%3F" target="_blank" class="group text-left p-4 rounded-2xl bg-slate-950/85 hover:bg-indigo-950/70 border border-indigo-500/30 hover:border-indigo-400 transition-all flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-xl">⏳</span>
                  <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-400 group-hover:translate-x-0.5 transition-transform">Consultar &rarr;</span>
                </div>
                <div class="text-sm font-black text-white mb-1">«Pierdo horas en citas, plantones o papeles»</div>
                <p class="text-xs text-slate-400 leading-snug">Quitarme tareas repetitivas de encima: agenda, teléfono, presupuestos o facturas.</p>
              </div>
            </a>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20me%20gustar%C3%ADa%20que%20le%20eches%20un%20vistazo%20profesional%20a%20mi%20negocio%20y%20a%20mi%20web%20y%20me%20digas%20honestamente%20qu%C3%A9%20mejorar%C3%ADas" target="_blank" class="group text-left p-4 rounded-2xl bg-gradient-to-br from-emerald-950/90 to-slate-950 hover:from-emerald-900/80 border-2 border-emerald-400/60 transition-all flex flex-col justify-between shadow-lg">
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-xl">🩺</span>
                  <span class="text-[10px] font-black uppercase tracking-wider text-emerald-300 group-hover:translate-x-0.5 transition-transform">Diagnóstico Gratis &rarr;</span>
                </div>
                <div class="text-sm font-black text-emerald-300 mb-1">«Francisco, revisa mi negocio y dime tú»</div>
                <p class="text-xs text-slate-200 leading-snug">Pídeme un diagnóstico previo gratuito y yo te guío paso a paso sin compromiso.</p>
              </div>
            </a>

          </div>
        </div>
      </div>
    </div>
  </section>
"""


BLOQUE_DOS_AUDITORIAS_GEMELAS = """
      <!-- ========================================================================= -->
      <!-- LAS 2 AUDITORÍAS GEMELAS DE INGENIERÍA Y CONVERSIÓN (SEO+GEO Y NEURO CRO) -->
      <!-- ========================================================================= -->
      <div id="auditoria-geo" class="scroll-mt-24 pt-10">
      <div class="glow-reputacion backdrop-blur-md border-2 border-teal-400/70 rounded-3xl p-6 sm:p-8 lg:p-9 shadow-2xl shadow-teal-950/40 relative overflow-hidden">
        <div class="absolute -top-24 -right-24 w-72 h-72 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <!-- Cabecera General + Píldora Simétrica de Tarifas (Mismo precio para cada auditoría) -->
        <div class="flex flex-col lg:flex-row lg:items-start justify-between gap-6 mb-7 border-b border-teal-500/30 pb-6">
          <div class="flex-1">
            <div class="flex flex-wrap items-center gap-2.5 mb-3">
              <span class="w-9 h-9 rounded-xl bg-teal-500 text-slate-950 font-black text-lg flex items-center justify-center shadow">🔍</span>
              <span class="w-9 h-9 rounded-xl bg-amber-400 text-slate-950 font-black text-lg flex items-center justify-center shadow">🧠</span>
              <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-300 bg-emerald-950/90 px-3 py-1 rounded-full border border-emerald-500/40">
                ● 2 Auditorías de Alta Ingeniería • Pago Único sin Cuotas (Elige 1 o combina ambas)
              </span>
            </div>
            <h3 class="text-2xl sm:text-3xl font-black text-white leading-tight mb-2.5">
              Auditorías e Implantaciones Prémium: <span class="text-teal-300">1. Visibilidad SEO + GEO (IA)</span> y <span class="text-amber-300">2. Neuromarketing y Conversión Web (CRO)</span>
            </h3>
            <p class="text-sm sm:text-base text-slate-200 leading-relaxed">
              De nada sirve tener una web bonita si nadie te encuentra, ni atraer visitas si se marchan sin comprarte. Por eso disponemos de <strong>dos auditorías independientes con idéntica estructura de precios</strong>: la primera hace que <strong>Google, ChatGPT y Gemini te recomienden</strong>; la segunda analiza tu web con <strong>mapas de calor y neuromarketing para tapar fugas de ventas</strong>.
            </p>
          </div>

          <!-- Píldora desglosada a la derecha (Tarifa Oficial por cada Auditoría) -->
          <div class="bg-slate-950/90 border-2 border-teal-400/60 rounded-2xl p-4 sm:p-5 text-left lg:text-right flex-shrink-0 lg:min-w-[280px] shadow-xl">
            <div class="text-[11px] font-extrabold uppercase tracking-wider text-teal-400 mb-2">Tarifa Oficial (Por cada Auditoría)</div>
            <div class="flex items-center justify-between lg:justify-end gap-4 text-xs sm:text-sm text-slate-200 mb-1">
              <span>Diagnóstico + Paquete Técnico:</span>
              <strong class="text-white font-black whitespace-nowrap">200 € c/u</strong>
            </div>
            <div class="flex items-center justify-between lg:justify-end gap-4 text-xs sm:text-sm text-slate-300 border-b border-dashed border-teal-500/40 pb-2 mb-2">
              <span>Implantación llave en mano:</span>
              <strong class="text-teal-300 font-bold whitespace-nowrap">+150 € c/u</strong>
            </div>
            <div class="flex items-center justify-between lg:justify-end gap-4 text-base sm:text-lg font-black text-emerald-400">
              <span>Total Llave en Mano:</span>
              <span class="whitespace-nowrap">350 € c/u</span>
            </div>
            <div class="mt-2 text-[11px] font-bold text-amber-300 bg-amber-950/60 border border-amber-500/30 rounded-lg px-2.5 py-1 text-center">
              ★ Bonificadas a 195 € c/u desde Pack Dúo (o 95 € c/u en Anual Trinity+)
            </div>
          </div>
        </div>

        <!-- LAS 2 AUDITORÍAS LADO A LADO (PARA QUE TE ENCUENTREN vs PARA QUE TE COMPREN) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-7">
          
          <!-- AUDITORÍA 1: SEO LOCAL + GEO (IA) -->
          <div class="bg-slate-950/90 border-2 border-teal-500/50 hover:border-teal-400 rounded-2xl p-5 sm:p-6 flex flex-col justify-between shadow-lg">
            <div>
              <div class="flex items-center justify-between gap-2 mb-3">
                <span class="text-xs font-black uppercase tracking-wider text-teal-300 bg-teal-950 px-3 py-1 rounded-full border border-teal-500/40">
                  🔍 AUDITORÍA 1 • «PARA QUE TE ENCUENTREN»
                </span>
                <span class="text-xs font-extrabold text-emerald-400">Google Maps + ChatGPT + Gemini</span>
              </div>
              <h4 class="text-xl sm:text-2xl font-black text-white mb-2">
                Auditoría e Implantación SEO Local + GEO (IA)
              </h4>
              <p class="text-xs sm:text-sm text-slate-200 leading-relaxed mb-4">
                Analizamos tu presencia digital y <strong>traducimos tu página web y tu ficha de Google Maps al idioma interno que leen los buscadores y las Inteligencias Artificiales</strong> (ChatGPT, Gemini, Perplexity). Así, cuando un cliente pregunte por el mejor negocio de tu sector en tu ciudad, la IA te recomendará a ti frente a tu competencia.
              </p>
              <div class="bg-black/40 border border-teal-500/20 rounded-xl p-3.5 mb-4 text-xs text-slate-300 space-y-1.5">
                <div><strong class="text-teal-300">✔ Qué conseguimos:</strong> Pasar de ser invisible para la IA a aparecer citado y recomendado en búsquedas locales y conversacionales.</div>
                <div><strong class="text-teal-300">✔ Qué te instalamos:</strong> Grafo conectado <code>Schema.org JSON-LD</code> con Wikidata, apertura a bots de IA (<code>robots.txt</code> y <code>llms.txt</code>), bloques <em>RAG-Friendly</em> y optimización de Google Business Profile.</div>
              </div>
            </div>
            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20me%20interesa%20la%20Auditor%C3%ADa%201%3A%20Visibilidad%20SEO%20Local%20%2B%20GEO%20%28IA%29%20para%20mi%20negocio" target="_blank" class="w-full py-3 text-center rounded-xl bg-teal-600/30 hover:bg-teal-600 border border-teal-400/50 text-white font-bold text-xs transition-all block">
              Consultar Auditoría 1: SEO + GEO (IA) &rarr;
            </a>
          </div>

          <!-- AUDITORÍA 2: NEUROMARKETING, MAPAS DE CALOR Y CONVERSIÓN WEB (CRO) -->
          <div class="bg-slate-950/90 border-2 border-amber-500/50 hover:border-amber-400 rounded-2xl p-5 sm:p-6 flex flex-col justify-between shadow-lg">
            <div>
              <div class="flex items-center justify-between gap-2 mb-3">
                <span class="text-xs font-black uppercase tracking-wider text-amber-300 bg-amber-950/80 px-3 py-1 rounded-full border border-amber-500/40">
                  🧠 AUDITORÍA 2 • «PARA QUE TE COMPREN»
                </span>
                <span class="text-xs font-extrabold text-amber-300">Neuromarketing + Mapas de Calor</span>
              </div>
              <h4 class="text-xl sm:text-2xl font-black text-white mb-2">
                Auditoría de Neuromarketing, Mapas Térmicos y Conversión (CRO)
              </h4>
              <p class="text-xs sm:text-sm text-slate-200 leading-relaxed mb-4">
                El 80% de las visitas que entran en la web de una pyme se marchan sin llamar ni rellenar el formulario. Auditamos tu web bajo los principios del <strong>Neuromarketing (Kahneman, Ley de Hick, Fogg)</strong> y <strong>mapas reales de calor y atención</strong> para detectar puntos ciegos, clics de rabia y fugas de dinero, transformando tu web en un embudo de ventas.
              </p>
              <div class="bg-black/40 border border-amber-500/20 rounded-xl p-3.5 mb-4 text-xs text-slate-300 space-y-1.5">
                <div><strong class="text-amber-300">✔ Qué conseguimos:</strong> Que las visitas que ya entran en tu web dejen de escaparse y te contacten en 1 clic desde el móvil.</div>
                <div><strong class="text-amber-300">✔ Qué incluye:</strong> Dictamen Forense de Neuromarketing y Velocidad Móvil, análisis de fricción en formularios, sonda térmica de comportamiento y <strong>150 € de implantación de mejoras de conversión</strong> en tu web.</div>
              </div>
            </div>
            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20me%20interesa%20la%20Auditor%C3%ADa%202%3A%20Neuromarketing%2C%20Mapas%20de%20Calor%20y%20Conversi%C3%B3n%20Web%20%28CRO%29%20para%20mi%20p%C3%A1gina" target="_blank" class="w-full py-3 text-center rounded-xl bg-amber-500/25 hover:bg-amber-500 hover:text-slate-950 border border-amber-400/50 text-amber-200 font-bold text-xs transition-all block">
              Consultar Auditoría 2: Neuromarketing y CRO &rarr;
            </a>
          </div>

        </div>

        <!-- DESPLEGABLE SEMIPLEGADO TÉCNICO (VISTA RÁPIDA + BOTÓN DE EXPANSIÓN) -->
        <details class="group bg-black/35 border border-teal-500/30 rounded-2xl px-5 py-3.5 text-xs text-slate-300 cursor-pointer transition-all mb-7">
          <summary class="font-bold text-teal-300 flex items-center justify-between select-none">
            <span>🛠️ Ver ingeniería técnica detallada incluida en cada Auditoría (Para informáticos, agencias y directores técnicos)</span>
            <span class="text-teal-400 group-open:rotate-180 transition-transform bg-teal-500/15 px-2.5 py-1 rounded-lg">▼ Desplegar ficha</span>
          </summary>
          <div class="pt-4 mt-3 border-t border-white/10 grid grid-cols-1 md:grid-cols-2 gap-4 text-[11.5px] text-slate-300 leading-relaxed">
            <div class="bg-slate-950/70 p-3.5 rounded-xl border border-teal-500/20">
              <strong class="text-teal-300 block mb-1">🔍 Ingeniería de la Auditoría 1 (SEO Local + GEO IA):</strong>
              1. Grafo conectado <code>Schema.org JSON-LD</code> (<code>@id</code>, <code>areaServed</code> y <code>knowsAbout</code> vinculados a Wikidata/Wikipedia).<br>
              2. Taxonomía quirúrgica de Google Business Profile, Bing Places + IndexNow y consistencia estricta <code>NAP+W</code>.<br>
              3. Desbloqueo de <code>robots.txt</code> para bots RAG (<code>OAI-SearchBot</code>, <code>PerplexityBot</code>, <code>Google-Extended</code>, <code>ClaudeBot</code>) y archivo <code>llms.txt</code>.
            </div>
            <div class="bg-slate-950/70 p-3.5 rounded-xl border border-amber-500/20">
              <strong class="text-amber-300 block mb-1">🧠 Ingeniería de la Auditoría 2 (Neuromarketing y CRO):</strong>
              1. Diagnóstico de Sistema 1 vs. Sistema 2 (Kahneman), Ley de Hick en formularios y Modelo Comportamental de Fogg.<br>
              2. Instrumentación de Sonda Térmica (Microsoft Clarity + GA4) con detección de <em>Rage Clicks</em>, <em>Dead Clicks</em> y profundidad de <em>Scroll</em>.<br>
              3. Auditoría de <em>Core Web Vitals</em> (LCP/CLS móvil) e implantación de gatillos de conversión directa por WhatsApp.
            </div>
          </div>
        </details>

        <!-- Las 3 Formas de Contratar Cualquiera de las 2 Auditorías -->
        <div class="mb-5">
          <h4 class="text-xs font-extrabold uppercase tracking-widest text-teal-300 mb-3.5 text-center sm:text-left">
            Tarifas idénticas para cada Auditoría • Elige la modalidad que prefieras (Precio por cada una):
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <!-- Opción 1: Solo Diagnóstico y Paquete Técnico -->
            <div class="bg-black/40 border border-teal-500/30 hover:border-teal-400/60 rounded-2xl p-5 flex flex-col justify-between transition-all">
              <div>
                <div class="flex items-baseline justify-between gap-2 mb-2">
                  <span class="text-sm font-black text-white uppercase tracking-wide">1. Solo Diagnóstico / Código</span>
                  <span class="text-2xl font-black text-teal-300 whitespace-nowrap">200 € <span class="text-[11px] font-bold text-slate-400">c/u</span></span>
                </div>
                <span class="inline-block text-[10px] font-bold uppercase tracking-wider text-slate-300 bg-white/10 px-2.5 py-0.5 rounded mb-3">
                  Paquete Técnico «Hazlo tú mismo»
                </span>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Realizamos la auditoría completa (SEO+GEO o Neuromarketing CRO) y te entregamos el <strong>informe ejecutivo y el paquete de código/mejoras</strong> listo para que tu propio informático lo implante.
                </p>
              </div>
              <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20encargar%20la%20Modalidad%201%20%28Solo%20Diagn%C3%B3stico%20y%20Paquete%20T%C3%A9cnico%3A%20200%20%E2%82%AC%29%20de%20una%20Auditor%C3%ADa" target="_blank" class="mt-5 w-full py-2.5 text-center rounded-xl bg-white/10 hover:bg-teal-700 text-white font-bold text-xs transition-colors block">
                Solicitar Modalidad 1 (200 € c/u)
              </a>
            </div>

            <!-- Opción 2: Todo Incluido Llave en Mano -->
            <div class="bg-black/40 border border-teal-500/40 hover:border-teal-400 rounded-2xl p-5 flex flex-col justify-between transition-all">
              <div>
                <div class="flex items-baseline justify-between gap-2 mb-2">
                  <span class="text-sm font-black text-white uppercase tracking-wide">2. Todo Incluido</span>
                  <span class="text-2xl font-black text-teal-300 whitespace-nowrap">350 € <span class="text-[11px] font-bold text-slate-400">c/u</span></span>
                </div>
                <span class="inline-block text-[10px] font-bold uppercase tracking-wider text-teal-200 bg-teal-950/90 border border-teal-500/40 px-2.5 py-0.5 rounded mb-3">
                  Suelta o con Plan Base (1 Servicio)
                </span>
                <p class="text-xs text-slate-300 leading-relaxed">
                  <strong>Diagnóstico/Código (200 €) + Implantación (+150 €):</strong> nos encargamos personalmente de dejarlo todo instalado y funcionando en tu web y Google Maps. <em>(Tarifa suelta o con 1 único servicio).</em>
                </p>
              </div>
              <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20contratar%20una%20Auditor%C3%ADa%20Todo%20Incluido%20Llave%20en%20Mano%20%28350%20%E2%82%AC%29" target="_blank" class="mt-5 w-full py-2.5 text-center rounded-xl bg-teal-600/40 border border-teal-400/50 hover:bg-teal-600 text-white font-bold text-xs transition-colors block">
                Elegir Llave en Mano (350 € c/u)
              </a>
            </div>

            <!-- Opción 3: Bonificada con Pack Escudo / Dúo+ (195 € c/u) -->
            <div class="bg-gradient-to-b from-emerald-950/80 to-slate-950 border-2 border-emerald-400 rounded-2xl p-5 flex flex-col justify-between relative shadow-lg shadow-emerald-950/50">
              <div class="absolute -top-3 right-4 bg-emerald-400 text-slate-950 text-[10px] font-black uppercase px-2.5 py-0.5 rounded-full shadow">
                ★ Exclusivo desde Pack Dúo (2+ Servicios)
              </div>
              <div>
                <div class="flex items-baseline justify-between gap-2 mb-2">
                  <span class="text-sm font-black text-emerald-300 uppercase tracking-wide">3. Con Pack Dúo+ ★</span>
                  <span class="text-2xl font-black text-emerald-400 whitespace-nowrap">195 € <span class="text-[11px] font-bold text-emerald-200">c/u</span></span>
                </div>
                <span class="inline-block text-[10px] font-extrabold uppercase tracking-wider text-emerald-200 bg-emerald-900/60 border border-emerald-500/40 px-2.5 py-0.5 rounded mb-3">
                  Ahorras 155 € en cada Auditoría
                </span>
                <p class="text-xs text-slate-200 leading-relaxed">
                  Al activar tu <strong>Pack Escudo (Dúo 99 €/m) o superior</strong>, te regalamos los 150 € de mano de obra y cada auditoría Llave en Mano te queda en <strong>195 € de pago único</strong> (o <strong>95 € c/u en Plan Anual Trinity+</strong>).
                </p>
              </div>
              <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20activar%20mi%20Pack%20Escudo%20con%20Auditor%C3%ADa%20bonificada%20a%20195%20%E2%82%AC" target="_blank" class="mt-5 w-full py-2.5 text-center rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs transition-all shadow-md block">
                Activar Pack Dúo + Auditoría (195 € c/u) &rarr;
              </a>
            </div>

          </div>
        </div>

        <div class="flex flex-col sm:flex-row items-center justify-between gap-3 pt-4 border-t border-teal-500/30 text-xs text-slate-300">
          <span>💡 <strong>Transparencia Total:</strong> Puedes contratar solo la <strong>Auditoría 1 (SEO+GEO)</strong>, solo la <strong>Auditoría 2 (Neuromarketing CRO)</strong> o combinar ambas (a <strong>195 € cada una</strong> desde Plan Dúo, o <strong>95 € cada una</strong> desde Plan Anual Trinity, ahorrando 155 € o 255 € en cada implantación).</span>
        </div>
      </div>
      </div>
"""


def aplicar_paso_1_web_principal(dir_raiz):
    ruta_index = os.path.join(dir_raiz, "index.html")
    if not os.path.isfile(ruta_index):
        print("❌ No se encontró index.html")
        return

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Insertar o actualizar el Bloque Consultor Prescriptor justo después del HERO y antes de #disponibles
    html = re.sub(
        r"<!-- ======================================================================= -->\s*<!-- BLOQUE CONSULTOR PRESCRIPTOR.*?<!-- SECCIÓN I: SERVICIOS ACTIVOS",
        "<!-- SECCIÓN I: SERVICIOS ACTIVOS",
        html,
        flags=re.DOTALL,
    )
    html = html.replace(
        "<!-- SECCIÓN I: SERVICIOS ACTIVOS",
        BLOQUE_CONSULTOR_SUPERIOR.strip() + "\n\n  <!-- SECCIÓN I: SERVICIOS ACTIVOS",
        1,
    )

    # 2. Actualizar enlaces de navegación para reflejar "Auditorías IA + CRO"
    html = html.replace("<span>Auditoría SEO + GEO</span>", "<span>Auditorías IA + CRO</span>")
    html = html.replace("<span>Auditoría SEO + GEO (IA)</span>", "<span>Auditorías SEO+GEO y Neuro CRO</span>")
    html = html.replace("🔍 Ver Auditoría SEO + GEO (IA)", "🔍🧠 Ver las 2 Auditorías (SEO+GEO y Neuro CRO)")

    # 3. Reemplazar el bloque #auditoria-geo por el nuevo bloque de las 2 Auditorías Gemelas
    patron_auditoria = re.compile(
        r'<div id="auditoria-geo" class="scroll-mt-24 pt-10">.*?</div>\s*</div>\s*<!-- BANNER COMBINADO NEUROMARKETING',
        re.DOTALL,
    )
    if patron_auditoria.search(html):
        html = patron_auditoria.sub(
            BLOQUE_DOS_AUDITORIAS_GEMELAS.strip() + "\n\n      <!-- BANNER COMBINADO NEUROMARKETING",
            html,
            count=1,
        )

    # 4. Actualizar la Tarjeta 6 de #tarifas para que refleje las 2 Auditorías Gemelas (195 € c/u o 95 € c/u)
    html = html.replace(
        '<h3 class="text-xl font-black text-white mb-2">AUDITORÍA <span class="text-teal-300">SEO + GEO</span></h3>',
        '<h3 class="text-xl font-black text-white mb-2">2 AUDITORÍAS <span class="text-teal-300">GEO &amp; CRO</span></h3>',
    )
    html = html.replace(
        'Optimización completa para ser recomendado por las IAs y dominar Google Maps.',
        'Elige la Auditoría 1 (SEO+GEO IA) o la Auditoría 2 (Neuromarketing y Conversión CRO). Mismo precio por cada una:',
    )
    html = html.replace(
        'Ver Opciones de Auditoría SEO+GEO',
        'Ver las 2 Auditorías (195 € c/u en Dúo+)',
    )

    # 5. Hacer que la sección #despliegue tenga un botón de Vista Semiplegada / Expandible (resumen siempre visible)
    if 'id="btnToggleDespliegue"' not in html:
        boton_semiplegado = """
        <div class="mt-5 flex justify-center">
          <button type="button" id="btnToggleDespliegue" onclick="toggleSeccionDespliegue()" class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-500/15 hover:bg-blue-500/25 border border-blue-400/40 text-blue-200 text-xs font-extrabold transition-all shadow-md">
            <span id="iconoToggleDespliegue">➖</span>
            <span id="textoToggleDespliegue">Modo Lectura Rápida: Ocultar detalles técnicos de próximos módulos</span>
          </button>
        </div>
        """
        html = html.replace(
            'Cada nuevo módulo adicional que sumes a tu plan se integra con tarifa reducida de socio (<strong>+40 €/mes</strong> del 2º al 5º servicio, y <strong>+30 €/mes</strong> a partir del 6º).\n        </p>',
            'Cada nuevo módulo adicional que sumes a tu plan se integra con tarifa reducida de socio (<strong>+40 €/mes</strong> del 2º al 5º servicio, y <strong>+30 €/mes</strong> a partir del 6º).\n        </p>' + boton_semiplegado,
            1,
        )

    # 6. Quitar la mención de "en 5 minutos" en la sección final de Contacto para mantener la percepción de consultoría seria
    html = html.replace(
        "Escríbeme ahora por WhatsApp y en 5 minutos vemos el diagnóstico real y una demostración con el nombre de tu propio negocio.",
        "Dime qué te preocupa o dónde sientes que tu negocio pierde clientes o tiempo: estudiaré tu caso personalmente y te prepararé un diagnóstico gratuito a medida.",
    )

    # 7. Añadir función JS para el modo semiplegado de #despliegue si no existe
    if "function toggleSeccionDespliegue()" not in html:
        script_toggle = """
    function toggleSeccionDespliegue() {
      const sec = document.getElementById('despliegue');
      if (!sec) return;
      const parrafos = sec.querySelectorAll('p.text-sm.text-slate-300');
      const btnTexto = document.getElementById('textoToggleDespliegue');
      const btnIcono = document.getElementById('iconoToggleDespliegue');
      const estaCompacto = sec.getAttribute('data-compact') === '1';

      parrafos.forEach(p => {
        if (estaCompacto) {
          p.classList.remove('line-clamp-2', 'opacity-80');
        } else {
          p.classList.add('line-clamp-2', 'opacity-80');
        }
      });

      if (estaCompacto) {
        sec.setAttribute('data-compact', '0');
        if (btnIcono) btnIcono.textContent = '➖';
        if (btnTexto) btnTexto.textContent = 'Modo Lectura Rápida: Compactar descripciones de próximos módulos';
      } else {
        sec.setAttribute('data-compact', '1');
        if (btnIcono) btnIcono.textContent = '➕';
        if (btnTexto) btnTexto.textContent = 'Ver descripciones completas de los próximos módulos';
      }
    }
"""
        html = html.replace("function toggleMobileMenu()", script_toggle + "\n    function toggleMobileMenu()", 1)

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)

    print("   ✔ PASO 1 COMPLETADO EN index.html:")
    print("     • Bloque Consultor Prescriptor arriba del todo (sin mencionar 5 minutos + 4 botones de dolores).")
    print("     • Sección Unificada de las 2 Auditorías Gemelas (SEO+GEO y Neuromarketing CRO) a 200€ / 350€ / 195€ c/u / 95€ c/u.")
    print("     • Conmutador de Vista Semiplegada en Próximo Despliegue (100% indexable por Google e IA).")


if __name__ == "__main__":
    print("=" * 85)
    print("🚀 EJECUTANDO PASO 1: MODO CONSULTOR + 2 AUDITORÍAS GEMELAS EN INDEX.HTML")
    print("=" * 85)
    d = localizar_directorio_public_html()
    if d:
        aplicar_paso_1_web_principal(d)
    print("=" * 85)
    print("🎉 ¡PASO 1 LISTO! Revisa tu web principal antes de pasar al Paso 2.")
    print("=" * 85)
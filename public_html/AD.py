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


HERO_LIMPIO_SIN_BANNER = """  <!-- HERO SECTION -->
  <section class="relative pt-4 pb-1 sm:pt-5 sm:pb-1.5 md:pt-6 md:pb-2 overflow-hidden hero-glow">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
      
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-10 items-center">
        
        <div class="lg:col-span-7 text-center lg:text-left">

          <h1 style="line-height: 1.15;" class="text-3xl sm:text-4xl lg:text-[40px] font-black tracking-tight mb-3.5 sm:mb-4">
            <span class="text-white">Sistemas de Automatización e Inteligencia Artificial para</span><br />
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-300 to-emerald-400">Blindar, Posicionar y Escalar</span> 
            <span class="text-white">tu Negocio Local</span>
          </h1>

          <p class="text-base sm:text-[17px] text-slate-200 font-medium leading-snug mb-4 sm:mb-5 max-w-2xl mx-auto lg:mx-0">
            Haz que tu negocio sea recomendado por <strong>Google, ChatGPT y Gemini</strong>, multiplica tus reseñas de 5★, frena las quejas en privado y automatiza citas, ventas y facturas desde el WhatsApp que ya utilizas.
          </p>

          <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-center lg:justify-start gap-3">
            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quisiera%20solicitar%20una%20demostraci%C3%B3n%20personalizada%20y%20conocer%20las%20Auditor%C3%ADas%20para%20mi%20negocio" target="_blank" class="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 bg-brand-teal hover:bg-brand-tealDark text-white font-bold text-sm sm:text-base px-6 py-3 rounded-xl shadow-lg shadow-teal-900/40 transition-all hover:scale-[1.02]">
              <svg class="w-5 h-5 fill-current flex-shrink-0" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
              <span>Pedir Demostración en Vivo</span>
            </a>
            <a href="#auditoria-geo" class="w-full sm:w-auto inline-flex flex-col items-center justify-center bg-teal-500/15 hover:bg-teal-500/25 text-teal-200 px-6 py-2 rounded-xl border border-teal-400/40 transition-colors leading-tight text-center">
              <span class="font-bold text-sm sm:text-[15px] text-white">🔍🧠 Ver las 2 Auditorías</span>
              <span class="text-[11px] font-semibold text-teal-300 mt-0.5">(SEO+GEO y Neuro CRO)</span>
            </a>
          </div>

          <div class="mt-4 pt-3.5 border-t border-white/10 flex items-center justify-center lg:justify-start gap-4 text-left group/profile">
            <a href="tarjeta.html" class="w-16 h-16 sm:w-[72px] sm:h-[72px] rounded-full overflow-hidden border-[3px] border-teal-500/50 shadow-xl shadow-teal-900/30 flex-shrink-0 group-hover/profile:scale-105 group-hover/profile:border-teal-400 transition-all cursor-pointer block relative">
              <img src="perfil.jpeg" data-img-base="perfil,foto,avatar" data-img-fallback="https://placehold.co/100x100/0d7d74/ffffff?text=FG" alt="Francisco M. Gallardo" class="w-full h-full object-cover relative z-0" onerror="cargarSiguienteExtension(this)">
            </a>
            <div>
              <a href="tarjeta.html" class="text-base sm:text-lg font-bold text-white group-hover/profile:text-teal-300 transition-colors cursor-pointer block leading-tight">Francisco M. Gallardo</a>
              <p class="text-xs sm:text-sm text-slate-400 mt-0.5">Consultor Tecnológico Local • Galicia<br class="sm:hidden"><span class="hidden sm:inline"> • </span><a href="tel:+34711547561" class="hover:text-teal-300 transition-colors">711 54 75 61</a></p>
            </div>
          </div>

        </div>

        <div class="lg:col-span-5">
          <div id="atril-nfc" class="scroll-mt-24 relative rounded-2xl bg-gradient-to-b from-amber-500/10 via-slate-900 to-slate-950 p-5 sm:p-6 border-2 border-amber-500/30 shadow-2xl shadow-amber-950/20">
            
            <div class="flex items-center justify-between gap-2 mb-2.5">
              <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-amber-500/20 text-amber-300 text-[11px] font-bold uppercase tracking-wider border border-amber-500/30">
                ★ Hardware Disponible Hoy
              </span>
              <div class="text-amber-400 text-sm tracking-widest font-black">★★★★★</div>
            </div>

            <h3 class="text-lg sm:text-xl font-black text-white leading-tight mb-2">
              Atril Inteligente de Mostrador <br class="sm:hidden"><span class="whitespace-nowrap text-amber-300 sm:text-white">(NFC + QR)</span>
            </h3>

            <p class="text-xs sm:text-[13px] text-slate-300 leading-relaxed mb-4">
              Elegante soporte físico de metacrilato con chip inalámbrico integrado y QR. El cliente solo tiene que acercar su móvil al pagar y se le abre tu pantalla oficial de valoración en Google Maps en <strong class="text-amber-300">1 segundo</strong>. Asegura que te deje su reseña en el acto antes de que salga por la puerta. Enlace 100% legal, directo y sin intermediarios.
            </p>

            <div class="bg-black/40 rounded-xl p-3.5 border border-white/5 mb-4 flex items-center justify-between">
              <div>
                <span class="text-[11px] text-slate-400 block font-medium">Pago único sin cuotas mensuales:</span>
                <span class="text-2xl font-black text-amber-400 whitespace-nowrap">39 €</span>
                <span class="text-[10.5px] text-slate-400 block">Equipo propio grabado de por vida</span>
              </div>
              <div class="text-right">
                <span class="inline-block text-[11px] font-semibold text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-800/40">
                  Entrega 24-48h
                </span>
              </div>
            </div>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20encargar%20un%20Atril%20Inteligente%20NFC%20%2839%20%E2%82%AC%29%20para%20mi%20mostrador" target="_blank" class="w-full inline-flex items-center justify-center gap-2 bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-white font-bold text-sm py-3 px-4 rounded-xl shadow-lg transition-all">
              ⚡ Encargar Atril para mi Mostrador
            </a>

          </div>
        </div>

      </div>

    </div>
  </section>"""


BLOQUE_CONSULTOR_SUPERIOR = """  <!-- ======================================================================= -->
  <!-- BLOQUE CONSULTOR PRESCRIPTOR (PICO 100% SIMÉTRICO + TITULAR UNIGÉNERO)  -->
  <!-- ======================================================================= -->
  <section id="consultor-personal" class="relative z-20 mt-2.5 pb-10 sm:pb-14 px-4 sm:px-6">
    <div class="max-w-6xl mx-auto relative">
      <!-- Contenedor separado para que translate-x-1/2 y rotate-45 no interfieran entre sí y el vértice quede clavado en X=36px (centro exacto de la foto de 72px) -->
      <div class="hidden lg:flex absolute -top-[9px] left-[36px] -translate-x-1/2 z-30 pointer-events-none items-center justify-center">
        <div class="w-4 h-4 bg-slate-900 border-t-2 border-l-2 border-teal-400/80 rotate-45"></div>
      </div>

      <div class="rounded-3xl bg-gradient-to-br from-slate-900 via-teal-950/55 to-slate-950 border-2 border-teal-400/70 px-5 py-4 sm:px-7 sm:py-5 shadow-2xl shadow-teal-950/50 relative overflow-hidden">
        <div class="absolute -top-20 -right-20 w-64 h-64 bg-teal-400/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-5 pb-4 border-b border-teal-500/30">
          <div class="space-y-1.5 max-w-3xl">
            <div class="flex flex-wrap items-center gap-2">
              <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-teal-500/20 border border-teal-400/40 text-teal-300 text-[11px] font-extrabold uppercase tracking-wider">
                🩺 Mensaje Directo de Francisco • Cero Agobios
              </span>
            </div>
            <h2 class="text-xl sm:text-2xl lg:text-[26px] font-black text-white leading-snug">
              Con total tranquilidad: no tienes que estudiarte toda esta web ni saber qué herramienta elegir.
            </h2>
            <p class="text-xs sm:text-sm text-slate-200 leading-relaxed">
              Contamos con un catálogo muy completo porque resolvemos muchos problemas distintos, pero <strong>mi trabajo como tu consultor tecnológico es ponértelo fácil</strong>. Si te apetece, explora la web con calma; y si prefieres ir al grano, <strong>simplemente dime qué te pasa o qué te trae de cabeza en tu negocio</strong>. Yo analizo tu caso personalmente y de forma gratuita, te digo qué necesitas exactamente y me encargo de solucionarlo todo.
            </p>
          </div>

          <div class="flex-shrink-0">
            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20prefiero%20contarte%20directamente%20qu%C3%A9%20necesito%20mejorar%20en%20mi%20negocio%20para%20que%20me%20asesores%20t%C3%BA" target="_blank" class="w-full lg:w-auto inline-flex items-center justify-center gap-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs sm:text-sm px-5 py-3.5 rounded-2xl shadow-lg shadow-emerald-950/60 transition-all hover:scale-[1.02]">
              <span>💬 Cuéntame tu caso por WhatsApp</span>
              <span>&rarr;</span>
            </a>
          </div>
        </div>

        <!-- 4 BOTONES RÁPIDOS DE "DOLORES REALES" DEL DUEÑO/A DE NEGOCIO -->
        <div class="pt-3.5">
          <p class="text-[11px] font-extrabold uppercase tracking-wider text-teal-300 mb-2.5">
            👇 Pulsa directamente sobre lo que más te preocupa hoy en tu negocio y hablamos:
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            
            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20lo%20que%20m%C3%A1s%20me%20interesa%20es%20conseguir%20m%C3%A1s%20visibilidad%20en%20Google%20e%20IA%2C%20m%C3%A1s%20rese%C3%B1as%20de%205%20estrellas%20y%20frenar%20quejas.%20%C2%BFQu%C3%A9%20me%20recomiendas%3F" target="_blank" class="group text-left p-3.5 rounded-2xl bg-slate-950/85 hover:bg-teal-950/70 border border-teal-500/30 hover:border-teal-400 transition-all flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-1">
                  <span class="text-lg">⭐</span>
                  <span class="text-[10px] font-bold uppercase tracking-wider text-teal-400 group-hover:translate-x-0.5 transition-transform">Consultar &rarr;</span>
                </div>
                <div class="text-xs sm:text-sm font-black text-white mb-1">«Quiero salir primero en Google/IA y más 5★»</div>
                <p class="text-[11px] text-slate-400 leading-snug">Que me recomienden antes que a mi competencia y frenar reseñas injustas.</p>
              </div>
            </a>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20siento%20que%20entra%20gente%20a%20mi%20web%20o%20me%20piden%20presupuesto%20pero%20se%20escapan%20sin%20comprar.%20%C2%BFPuedes%20analizar%20d%C3%B3nde%20fallo%3F" target="_blank" class="group text-left p-3.5 rounded-2xl bg-slate-950/85 hover:bg-blue-950/70 border border-blue-500/30 hover:border-blue-400 transition-all flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-1">
                  <span class="text-lg">💸</span>
                  <span class="text-[10px] font-bold uppercase tracking-wider text-blue-400 group-hover:translate-x-0.5 transition-transform">Consultar &rarr;</span>
                </div>
                <div class="text-xs sm:text-sm font-black text-white mb-1">«Me entra gente a la web o llaman, pero se escapan»</div>
                <p class="text-[11px] text-slate-400 leading-snug">Detectar por qué no terminan comprando y responder presupuestos al instante.</p>
              </div>
            </a>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20pierdo%20demasiado%20tiempo%20con%20citas%2C%20plantones%2C%20llamadas%20o%20facturas%20para%20el%20gestor.%20%C2%BFC%C3%B3mo%20puedo%20automatizarlo%3F" target="_blank" class="group text-left p-3.5 rounded-2xl bg-slate-950/85 hover:bg-indigo-950/70 border border-indigo-500/30 hover:border-indigo-400 transition-all flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-1">
                  <span class="text-lg">⏳</span>
                  <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-400 group-hover:translate-x-0.5 transition-transform">Consultar &rarr;</span>
                </div>
                <div class="text-xs sm:text-sm font-black text-white mb-1">«Pierdo horas en citas, plantones o papeles»</div>
                <p class="text-[11px] text-slate-400 leading-snug">Quitarme tareas repetitivas de encima: agenda, teléfono, presupuestos o facturas.</p>
              </div>
            </a>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20me%20gustar%C3%ADa%20que%20le%20eches%20un%20vistazo%20profesional%20a%20mi%20negocio%20y%20a%20mi%20web%20y%20me%20digas%20honestamente%20qu%C3%A9%20mejorar%C3%ADas" target="_blank" class="group text-left p-3.5 rounded-2xl bg-gradient-to-br from-emerald-950/90 to-slate-950 hover:from-emerald-900/80 border-2 border-emerald-400/60 transition-all flex flex-col justify-between shadow-lg">
              <div>
                <div class="flex items-center justify-between mb-1">
                  <span class="text-lg">🩺</span>
                  <span class="text-[10px] font-black uppercase tracking-wider text-emerald-300 group-hover:translate-x-0.5 transition-transform">Diagnóstico Gratis &rarr;</span>
                </div>
                <div class="text-xs sm:text-sm font-black text-emerald-300 mb-1">«Francisco, revisa mi negocio y dime tú»</div>
                <p class="text-[11px] text-slate-200 leading-snug">Pídeme un diagnóstico previo gratuito y yo te guío paso a paso sin compromiso.</p>
              </div>
            </a>

          </div>
        </div>
      </div>
    </div>
  </section>"""


def actualizar_hero_y_bocadillo(dir_raiz):
    ruta_index = os.path.join(dir_raiz, "index.html")
    if not os.path.isfile(ruta_index):
        print("❌ No se encontró index.html")
        return

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    patron = re.compile(
        r'<!-- HERO SECTION -->.*?<!-- SECCIÓN I: SERVICIOS ACTIVOS',
        re.DOTALL
    )
    nuevo_bloque = (
        HERO_LIMPIO_SIN_BANNER.strip()
        + "\n\n"
        + BLOQUE_CONSULTOR_SUPERIOR.strip()
        + "\n\n  <!-- SECCIÓN I: SERVICIOS ACTIVOS"
    )

    if patron.search(html):
        html = patron.sub(nuevo_bloque, html)
    else:
        print("⚠️ No se encontró el bloque Hero + Consultor.")

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)

    print("   ✔ Piquito del bocadillo centrado matemáticamente con el eje vertical de tu foto (X=36px).")
    print("   ✔ Frase unigénero aplicada: «Con total tranquilidad: no tienes que estudiarte toda esta web ni saber qué herramienta elegir.»")


if __name__ == "__main__":
    print("=" * 85)
    print("🚀 CENTRANDO PICO DEL BOCADILLO Y APLICANDO TEXTO UNIGÉNERO")
    print("=" * 85)
    d = localizar_directorio_public_html()
    if d:
        actualizar_hero_y_bocadillo(d)
    print("=" * 85)
    print("🎉 ¡LISTO! Recarga sistemaspyme.es para verlo.")
    print("=" * 85)
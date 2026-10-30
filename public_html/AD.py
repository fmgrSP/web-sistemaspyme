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


HERO_CON_MULTI_ATRIL = """  <!-- HERO SECTION -->
  <section class="relative pt-6 pb-1 sm:pt-8 sm:pb-1.5 md:pt-9 lg:pt-10 md:pb-2 overflow-hidden hero-glow">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
      
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-10 items-center">
        
        <div class="lg:col-span-7 text-center lg:text-left">

          <h1 style="line-height: 1.15;" class="text-3xl sm:text-4xl lg:text-[40px] font-black tracking-tight mb-3 sm:mb-3.5">
            <span class="text-white">Sistemas de Automatización e Inteligencia Artificial para</span><br />
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-300 to-emerald-400">Blindar, Posicionar y Escalar</span> 
            <span class="text-white">tu Negocio Local</span>
          </h1>

          <p class="text-base sm:text-[17px] text-slate-200 font-medium leading-snug mb-3.5 sm:mb-4 max-w-2xl mx-auto lg:mx-0">
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

          <div class="mt-3.5 pt-3 border-t border-white/10 flex items-center justify-center lg:justify-start gap-4 text-left group/profile">
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

            <div class="bg-black/40 rounded-xl p-3.5 border border-white/5 mb-4 flex items-center justify-between gap-2">
              <div>
                <span class="text-[11px] text-slate-400 block font-medium">Pago único sin cuotas mensuales:</span>
                <div class="flex items-baseline gap-2">
                  <span class="text-2xl font-black text-amber-400 whitespace-nowrap">39 €</span>
                  <span class="text-[10.5px] font-bold text-amber-200/90 whitespace-nowrap">• Ud. extra: 29 € (5+: 25 €)</span>
                </div>
                <span class="text-[10.5px] text-slate-400 block">Ideal para 1 mostrador o varios puestos/mesas</span>
              </div>
              <div class="text-right flex-shrink-0">
                <span class="inline-block text-[11px] font-semibold text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-800/40">
                  Entrega 24-48h
                </span>
              </div>
            </div>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20encargar%20el%20Atril%20Inteligente%20NFC%20%2839%20%E2%82%AC%20o%20Pack%20Multi-Puesto%29%20para%20mi%20negocio" target="_blank" class="w-full inline-flex items-center justify-center gap-2 bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-white font-bold text-sm py-3 px-4 rounded-xl shadow-lg transition-all">
              ⚡ Encargar Atril (1 o Varios Puestos)
            </a>

          </div>
        </div>

      </div>

    </div>
  </section>"""


def actualizar_multi_atril(dir_raiz):
    ruta_index = os.path.join(dir_raiz, "index.html")
    if not os.path.isfile(ruta_index):
        print("❌ No se encontró index.html")
        return

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    patron = re.compile(
        r'<!-- HERO SECTION -->.*?</section>',
        re.DOTALL
    )
    if patron.search(html):
        html = patron.sub(HERO_CON_MULTI_ATRIL.strip(), html, count=1)
        with open(ruta_index, "w", encoding="utf-8") as f:
            f.write(html)
        print("   ✔ Precios por volumen de Atril NFC (39 € | Ud. extra: 29 € | 5+: 25 €) integrados sin alterar ni 1px la altura.")
    else:
        print("⚠️ No se encontró el bloque Hero.")


if __name__ == "__main__":
    print("=" * 85)
    print("🚀 INTEGRANDO ESCALA MULTI-PUESTO EN ATRIL NFC (MANTENIENDO ALTURA EXACTA)")
    print("=" * 85)
    d = localizar_directorio_public_html()
    if d:
        actualizar_multi_atril(d)
    print("=" * 85)
    print("🎉 ¡LISTO! Recarga sistemaspyme.es para verlo.")
    print("=" * 85)
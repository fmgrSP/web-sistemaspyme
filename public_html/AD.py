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
  <!-- BLOQUE CONSULTOR PRESCRIPTOR (BOCADILLO CON AIRE LIMPIO BAJO LA FOTO)   -->
  <!-- ======================================================================= -->
  <section id="consultor-personal" class="relative z-20 mt-3 sm:mt-4 pb-10 sm:pb-14 px-4 sm:px-6">
    <div class="max-w-6xl mx-auto relative">
      <!-- Triángulo conector tipo bocadillo: queda justo debajo de la foto de Francisco a 8px sin morderla -->
      <div class="hidden lg:block absolute -top-2.5 left-9 w-5 h-5 bg-slate-900 border-t-2 border-l-2 border-teal-400/70 rotate-45 z-30"></div>

      <div class="rounded-3xl bg-gradient-to-br from-slate-900 via-teal-950/50 to-slate-950 border-2 border-teal-400/60 p-6 sm:p-7 shadow-2xl shadow-teal-950/50 relative overflow-hidden">
        <div class="absolute -top-20 -right-20 w-64 h-64 bg-teal-400/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-5 border-b border-teal-500/30">
          <div class="space-y-2 max-w-3xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/20 border border-teal-400/40 text-teal-300 text-xs font-extrabold uppercase tracking-wider">
              <span>🩺 Mensaje Directo de Francisco • Cero Agobios</span>
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
        <div class="pt-4">
          <p class="text-xs font-extrabold uppercase tracking-wider text-teal-300 mb-3">
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


def ajustar_pico_bocadillo(dir_raiz):
    ruta_index = os.path.join(dir_raiz, "index.html")
    if not os.path.isfile(ruta_index):
        print("❌ No se encontró index.html")
        return

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # Asegurar que el Hero tenga un pb-3 md:pb-4 limpio para que el pico quede a ~8px por debajo del borde inferior de la foto sin morderla
    html = re.sub(
        r'<!-- HERO SECTION -->\s*<section class="relative [^"]*hero-glow">',
        '<!-- HERO SECTION -->\n  <section class="relative pt-2 pb-2 sm:pt-4 sm:pb-3 md:pt-5 md:pb-3 overflow-hidden hero-glow">',
        html,
    )

    # Reemplazar el bloque consultor con el nuevo margen mt-3 sm:mt-4 y pico calibrado en left-9 -top-2.5
    html = re.sub(
        r'<!-- ======================================================================= -->\s*<!-- BLOQUE CONSULTOR PRESCRIPTOR.*?<!-- SECCIÓN I: SERVICIOS ACTIVOS',
        BLOQUE_CONSULTOR_SUPERIOR.strip() + "\n\n  <!-- SECCIÓN I: SERVICIOS ACTIVOS",
        html,
        flags=re.DOTALL,
    )

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)

    print("   ✔ Pico del bocadillo ajustado en index.html: ahora queda justo debajo de tu foto a ~8px de distancia sin morder el círculo.")


if __name__ == "__main__":
    print("=" * 85)
    print("🚀 AJUSTANDO EL PICO DEL BOCADILLO PARA NO MORDER LA FOTO DE PERFIL")
    print("=" * 85)
    d = localizar_directorio_public_html()
    if d:
        ajustar_pico_bocadillo(d)
    print("=" * 85)
    print("🎉 ¡LISTO! Recarga sistemaspyme.es para verlo.")
    print("=" * 85)
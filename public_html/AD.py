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
  <!-- BLOQUE CONSULTOR PRESCRIPTOR (BOCADILLO PEGADO A FRANCISCO)             -->
  <!-- ======================================================================= -->
  <section id="consultor-personal" class="relative z-20 -mt-2 sm:-mt-3 pb-10 sm:pb-14 px-4 sm:px-6">
    <div class="max-w-6xl mx-auto relative">
      <!-- Triángulo conector tipo bocadillo de diálogo apuntando hacia la foto y nombre de Francisco -->
      <div class="hidden lg:block absolute -top-3 left-14 w-6 h-6 bg-slate-900 border-t-2 border-l-2 border-teal-400/70 rotate-45 z-30"></div>

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


def aplicar_ajustes_visuales_hero_y_consultor(dir_raiz):
    ruta_index = os.path.join(dir_raiz, "index.html")
    if not os.path.isfile(ruta_index):
        print("❌ No se encontró index.html")
        return

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Subir el bloque HERO más cerca de la barra superior y reducir el hueco inferior para acercar el bocadillo a la foto de Francisco
    html = re.sub(
        r'<!-- HERO SECTION -->\s*<section class="relative [^"]*hero-glow">',
        '<!-- HERO SECTION -->\n  <section class="relative pt-2 pb-4 sm:pt-4 sm:pb-5 md:pt-5 md:pb-6 overflow-hidden hero-glow">',
        html,
    )

    # Compactar ligeramente los márgenes internos del Hero para que la foto de Francisco suba y tenga aire por abajo en el primer pantallazo
    html = html.replace(
        'text-teal-300 text-xs font-semibold mb-4 sm:mb-6">',
        'text-teal-300 text-xs font-semibold mb-3 sm:mb-4">',
    )
    html = html.replace(
        'font-black tracking-tight leading-[1.20] sm:leading-[1.20] lg:leading-[1.20] mb-4 sm:mb-6">',
        'font-black tracking-tight leading-[1.18] sm:leading-[1.18] lg:leading-[1.18] mb-3 sm:mb-4">',
    )
    html = html.replace(
        'font-medium leading-relaxed mb-6 sm:mb-8 max-w-2xl mx-auto lg:mx-0">',
        'font-medium leading-relaxed mb-4 sm:mb-5 max-w-2xl mx-auto lg:mx-0">',
    )
    html = html.replace(
        'mt-6 pt-5 sm:mt-8 sm:pt-6 border-t border-white/10 flex items-center justify-center lg:justify-start gap-5 text-left group/profile">',
        'mt-5 pt-4 sm:mt-6 sm:pt-5 border-t border-white/10 flex items-center justify-center lg:justify-start gap-5 text-left group/profile">',
    )

    # 2. Formatear el botón "Ver las 2 Auditorías" en dos líneas exactas:
    #    Línea 1: 🔍🧠 Ver las 2 Auditorías
    #    Línea 2: (SEO+GEO y Neuro CRO)
    patron_btn_auditorias = re.compile(
        r'<a href="#auditoria-geo" class="w-full sm:w-auto inline-flex[^"]*">\s*🔍🧠 Ver las 2 Auditorías \(SEO\+GEO y Neuro CRO\)\s*</a>',
        re.DOTALL,
    )
    nuevo_btn_auditorias = """<a href="#auditoria-geo" class="w-full sm:w-auto inline-flex flex-col items-center justify-center bg-teal-500/15 hover:bg-teal-500/25 text-teal-200 font-bold px-6 py-2.5 rounded-xl border border-teal-400/40 transition-colors leading-tight text-center">
              <span class="text-sm sm:text-base font-extrabold whitespace-nowrap">🔍🧠 Ver las 2 Auditorías</span>
              <span class="text-xs font-semibold text-teal-300/95 whitespace-nowrap mt-0.5">(SEO+GEO y Neuro CRO)</span>
            </a>"""

    if patron_btn_auditorias.search(html):
        html = patron_btn_auditorias.sub(nuevo_btn_auditorias, html)
    else:
        # Si ya estaba modificado o con otra variante, reemplazar cualquier enlace a #auditoria-geo dentro del Hero
        html = re.sub(
            r'<a href="#auditoria-geo" class="w-full sm:w-auto inline-flex[^"]*">.*?</a>',
            nuevo_btn_auditorias,
            html,
            count=1,
            flags=re.DOTALL,
        )

    # 3. También asegurar que el botón de al lado (Pedir Demostración en Vivo) quede en 1 sola línea limpia y de la misma altura visual
    html = html.replace(
        'class="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 bg-brand-teal hover:bg-brand-tealDark text-white font-bold text-base px-7 py-3.5 rounded-xl shadow-lg shadow-teal-900/40 transition-all hover:scale-[1.02]"',
        'class="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 bg-brand-teal hover:bg-brand-tealDark text-white font-bold text-sm sm:text-base px-6 py-3.5 rounded-xl shadow-lg shadow-teal-900/40 transition-all hover:scale-[1.02] whitespace-nowrap"',
    )

    # 4. Actualizar el bloque #consultor-personal para que quede pegado a la foto de Francisco con el triángulo de diálogo
    html = re.sub(
        r'<!-- ======================================================================= -->\s*<!-- BLOQUE CONSULTOR PRESCRIPTOR.*?<!-- SECCIÓN I: SERVICIOS ACTIVOS',
        BLOQUE_CONSULTOR_SUPERIOR.strip() + "\n\n  <!-- SECCIÓN I: SERVICIOS ACTIVOS",
        html,
        flags=re.DOTALL,
    )

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)

    print("   ✔ Ajustes visuales aplicados en index.html:")
    print("     1. Hero subido más cerca de la barra principal -> Tu foto y nombre tienen ahora mucho más aire por abajo.")
    print("     2. Recuadro 'Tranquilo...' pegado a tu perfil con puntero de diálogo apuntando a tu foto y nombre.")
    print("     3. Botón 'Ver las 2 Auditorías' en 2 filas exactas: '🔍🧠 Ver las 2 Auditorías' arriba y '(SEO+GEO y Neuro CRO)' debajo.")


if __name__ == "__main__":
    print("=" * 85)
    print("🚀 APLICANDO AJUSTES VISUALES EN PORTADA Y BOCADILLO DE CONSULTOR")
    print("=" * 85)
    d = localizar_directorio_public_html()
    if d:
        aplicar_ajustes_visuales_hero_y_consultor(d)
    print("=" * 85)
    print("🎉 ¡LISTO! Recarga sistemaspyme.es para ver el nuevo encuadre.")
    print("=" * 85)
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
# WIDGET FLOTANTE «CONSEJERO EN 2 CLICS (CERO PEREZA / CERO TECLEO)»
# ==============================================================================
BLOQUE_ASISTENTE_FLOTANTE = """  <!-- ======================================================================= -->
  <!-- ASISTENTE FLOTANTE DE CONSEJO RÁPIDO (2 CLICS • CERO TECLEO)            -->
  <!-- ======================================================================= -->
  <div id="spAsistenteConsejo" class="fixed bottom-5 right-4 sm:right-6 z-[95] flex flex-col items-end">
    
    <!-- Ventana Desplegable con las 5 Opciones Masticadas (Oculta por defecto) -->
    <div id="spPanelConsejo" class="hidden mb-3 w-[92vw] max-w-[370px] rounded-2xl bg-slate-900/98 backdrop-blur-xl border-2 border-teal-400/70 shadow-[0_20px_60px_rgba(0,0,0,0.85)] overflow-hidden transition-all duration-200">
      
      <!-- Cabecera cálida con tu foto -->
      <div class="bg-gradient-to-r from-brand-navy via-slate-900 to-teal-950 p-4 border-b border-teal-500/30 flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="relative w-11 h-11 rounded-full overflow-hidden border-2 border-teal-400 flex-shrink-0">
            <img src="perfil.jpeg" data-img-base="perfil,foto,avatar" data-img-fallback="https://placehold.co/100x100/0d7d74/ffffff?text=FG" alt="Francisco" class="w-full h-full object-cover" onerror="cargarSiguienteExtension(this)">
          </div>
          <div>
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span class="text-[10px] font-extrabold uppercase tracking-wider text-emerald-300">Consejo Directo • Cero Líos</span>
            </div>
            <h4 class="text-sm font-black text-white leading-tight">¿Te ayudo a elegir o combinar?</h4>
          </div>
        </div>
        <button type="button" onclick="togglePanelConsejo(false)" class="w-7 h-7 rounded-lg bg-white/5 hover:bg-white/15 text-slate-300 hover:text-white flex items-center justify-center text-xs font-bold transition-colors">
          ✕
        </button>
      </div>

      <!-- Mensaje tranquilizador anti-bloqueo -->
      <div class="px-4 pt-3 pb-2 bg-slate-950/60 border-b border-white/5">
        <p class="text-[11.5px] text-slate-300 leading-snug">
          💡 <strong class="text-teal-300">No tengas que escribir nada:</strong> toca la duda que tengas aquí abajo (2 clics) y te asesoro sobre la marcha sin ningún compromiso:
        </p>
      </div>

      <!-- Las 5 Dudas Más Frecuentes listas para tocar en 1 clic -->
      <div class="p-3 space-y-2 max-h-[62vh] overflow-y-auto">
        
        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20estoy%20viendo%20tu%20web%20y%20tengo%20dudas%20sobre%20qu%C3%A9%20m%C3%B3dulos%20me%20convienen%2C%20por%20d%C3%B3nde%20empezar%20o%20c%C3%B3mo%20combinarlos." target="_blank" class="block w-full text-left p-2.5 rounded-xl bg-slate-950/90 hover:bg-teal-950/70 border border-white/10 hover:border-teal-400/60 transition-all group">
          <div class="flex items-center justify-between gap-2">
            <span class="text-xs font-extrabold text-white group-hover:text-teal-300">🧩 1. ¿Por dónde empiezo o cómo combino?</span>
            <span class="text-[10px] font-bold text-teal-400 flex-shrink-0">1 clic &rarr;</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-0.5 leading-snug">Dime qué módulos me convienen según mi negocio sin pagar de más.</p>
        </a>

        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20%C2%BFcu%C3%A1l%20es%20la%20mejor%20combinaci%C3%B3n%20de%20precios%20o%20Pack%20%28Escudo%20%2F%20D%C3%BAo%20%2F%20Trinity%29%20para%20ahorrar%20en%20mi%20caso%3F" target="_blank" class="block w-full text-left p-2.5 rounded-xl bg-slate-950/90 hover:bg-teal-950/70 border border-white/10 hover:border-teal-400/60 transition-all group">
          <div class="flex items-center justify-between gap-2">
            <span class="text-xs font-extrabold text-white group-hover:text-teal-300">💰 2. Mejor combinación para ahorrar</span>
            <span class="text-[10px] font-bold text-teal-400 flex-shrink-0">1 clic &rarr;</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-0.5 leading-snug">Lío entre Pack Escudo, Plan Dúo o cómo sumar otro servicio luego.</p>
        </a>

        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20tengo%20dudas%20sobre%20las%20Auditor%C3%ADas%20%28SEO%2BGEO%20o%20Neuromarketing%20CRO%29%20y%20si%20me%20compensa%20cogerlas%20sueltas%20o%20con%20Pack." target="_blank" class="block w-full text-left p-2.5 rounded-xl bg-slate-950/90 hover:bg-teal-950/70 border border-white/10 hover:border-teal-400/60 transition-all group">
          <div class="flex items-center justify-between gap-2">
            <span class="text-xs font-extrabold text-white group-hover:text-teal-300">🔍🧠 3. Dudas con las 2 Auditorías</span>
            <span class="text-[10px] font-bold text-teal-400 flex-shrink-0">1 clic &rarr;</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-0.5 leading-snug">¿Necesito la SEO+GEO, la de Neuromarketing o me sale mejor en Pack (195 €)?</p>
        </a>

        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20tengo%20dudas%20entre%20el%20Plan%20Mensual%20y%20el%20Plan%20Anual%20%282%20meses%20gratis%29%20o%20las%20facilidades%20de%20pago." target="_blank" class="block w-full text-left p-2.5 rounded-xl bg-slate-950/90 hover:bg-teal-950/70 border border-white/10 hover:border-teal-400/60 transition-all group">
          <div class="flex items-center justify-between gap-2">
            <span class="text-xs font-extrabold text-white group-hover:text-teal-300">📅 4. ¿Plan Mensual, Anual o Pagos?</span>
            <span class="text-[10px] font-bold text-teal-400 flex-shrink-0">1 clic &rarr;</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-0.5 leading-snug">Consultar diferencia real entre mensual flexible, anual y puesta en marcha.</p>
        </a>

        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20prefiero%20mandarte%20una%20nota%20de%20voz%20o%20que%20hablemos%202%20minutos%20para%20no%20tener%20que%20escribir%20y%20que%20me%20aconsejes%20t%C3%BA." target="_blank" class="block w-full text-left p-2.5 rounded-xl bg-emerald-950/60 hover:bg-emerald-900/70 border border-emerald-500/40 hover:border-emerald-400 transition-all group">
          <div class="flex items-center justify-between gap-2">
            <span class="text-xs font-black text-emerald-300">🎙️ 5. «Prefiero mandarte un audio o hablar»</span>
            <span class="text-[10px] font-black text-emerald-300 flex-shrink-0">Sin teclear &rarr;</span>
          </div>
          <p class="text-[11px] text-emerald-100/80 mt-0.5 leading-snug">Ábreme WhatsApp y te mando una nota de voz rápida para que me guíes tú.</p>
        </a>

      </div>
    </div>

    <!-- Botón Flotante Principal (Discreto, elegante y siempre accesible) -->
    <button type="button" id="spBtnAbrirConsejo" onclick="togglePanelConsejo()" class="group flex items-center gap-2.5 bg-gradient-to-r from-slate-900 via-teal-950 to-slate-900 hover:from-teal-900 hover:to-slate-900 text-white pl-2 pr-4 py-2 rounded-full border-2 border-teal-400/80 shadow-[0_10px_30px_rgba(13,125,116,0.45)] hover:scale-[1.03] transition-all">
      <div class="relative w-10 h-10 rounded-full overflow-hidden border-2 border-emerald-400 flex-shrink-0">
        <img src="perfil.jpeg" data-img-base="perfil,foto,avatar" data-img-fallback="https://placehold.co/100x100/0d7d74/ffffff?text=FG" alt="Francisco" class="w-full h-full object-cover" onerror="cargarSiguienteExtension(this)">
      </div>
      <div class="text-left leading-tight">
        <div class="flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          <span class="text-[10px] font-black uppercase tracking-wider text-emerald-300">¿Dudas o cómo combinar?</span>
        </div>
        <span class="text-xs sm:text-[13px] font-extrabold text-white block">Te aconsejo en 2 clics 💬</span>
      </div>
    </button>

  </div>
"""

JS_ASISTENTE_FLOTANTE = """
    // CONTROL DEL ASISTENTE FLOTANTE DE CONSEJO EN 2 CLICS
    function togglePanelConsejo(forzarEstado) {
      const panel = document.getElementById('spPanelConsejo');
      if (!panel) return;
      if (typeof forzarEstado === 'boolean') {
        if (forzarEstado) panel.classList.remove('hidden');
        else panel.classList.add('hidden');
      } else {
        panel.classList.toggle('hidden');
      }
    }
    document.addEventListener('click', (e) => {
      const wrap = document.getElementById('spAsistenteConsejo');
      const panel = document.getElementById('spPanelConsejo');
      if (wrap && panel && !panel.classList.contains('hidden') && !wrap.contains(e.target)) {
        panel.classList.add('hidden');
      }
    });
"""


def inyectar_asistente_y_regla_inpost(dir_raiz):
    ruta_index = os.path.join(dir_raiz, "index.html")
    if not os.path.isfile(ruta_index):
        return

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Eliminar versión previa del asistente flotante si existiera
    html = re.sub(
        r'  <!-- ======================================================================= -->\s*<!-- ASISTENTE FLOTANTE DE CONSEJO RÁPIDO.*?<!-- MODAL DE AVISO LEGAL -->',
        '  <!-- MODAL DE AVISO LEGAL -->',
        html,
        flags=re.DOTALL
    )

    # 2. Insertar el nuevo Asistente Flotante justo antes del Modal Legal
    if 'id="spAsistenteConsejo"' not in html:
        html = html.replace(
            '  <!-- MODAL DE AVISO LEGAL -->',
            BLOQUE_ASISTENTE_FLOTANTE + '\n  <!-- MODAL DE AVISO LEGAL -->',
            1
        )

    # 3. Insertar la función JS del asistente si no está
    if 'function togglePanelConsejo' not in html:
        html = html.replace(
            '    // CONTROL DEL MENÚ MÓVIL (Hamburguesa)',
            JS_ASISTENTE_FLOTANTE + '\n    // CONTROL DEL MENÚ MÓVIL (Hamburguesa)',
            1
        )

    # 4. Incorporar el principio "InPost (Cero Tecleo: solo tocar estrellas o 1 botón)" en el Servicio 2 y Atril
    html = html.replace(
        "Multiplica hasta x4 tus reseñas 5★",
        "Cero pereza: 1 clic o audio (sin obligar a escribir)"
    )

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)
    print("   ✔ Asistente Flotante «Te aconsejo en 2 clics (Cero Tecleo)» inyectado en index.html.")


if __name__ == "__main__":
    print("=" * 85)
    print("🚀 ACTIVANDO ASISTENTE FLOTANTE DE CONSEJO EN 2 CLICS + REGLA CERO TECLEO + PASO 2")
    print("=" * 85)
    d = localizar_directorio_public_html()
    if d:
        inyectar_asistente_y_regla_inpost(d)
        actualizar_pyme_magazine(d)
        adaptar_8_documentos_web(d)
    print("=" * 85)
    print("🎉 ¡LISTO! Botón flotante de consejo rápido + 8 documentos + Pyme Magazine N1 actualizados.")
    print("=" * 85)
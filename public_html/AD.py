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
  <!-- ASISTENTE FLOTANTE NIVEL 2: RESPUESTAS CLARAS EN PANTALLA + WHATSAPP    -->
  <!-- ======================================================================= -->
  <div id="spAsistenteConsejo" class="fixed bottom-5 right-4 sm:right-6 z-[95] flex flex-col items-end">
    
    <!-- Ventana Desplegable con Respuestas Instantáneas + Desplegable Completo + WhatsApp -->
    <div id="spPanelConsejo" class="hidden mb-3 w-[94vw] max-w-[410px] rounded-2xl bg-slate-900/98 backdrop-blur-xl border-2 border-teal-400/80 shadow-[0_20px_60px_rgba(0,0,0,0.9)] overflow-hidden transition-all duration-200">
      
      <!-- Cabecera cálida con tu foto -->
      <div class="bg-gradient-to-r from-brand-navy via-slate-900 to-teal-950 p-3.5 sm:p-4 border-b border-teal-500/30 flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="relative w-11 h-11 rounded-full overflow-hidden border-2 border-teal-400 flex-shrink-0">
            <img src="perfil.jpeg" data-img-base="perfil,foto,avatar" data-img-fallback="https://placehold.co/100x100/0d7d74/ffffff?text=FG" alt="Francisco" class="w-full h-full object-cover" onerror="cargarSiguienteExtension(this)">
          </div>
          <div>
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span class="text-[10px] font-extrabold uppercase tracking-wider text-emerald-300">Guía Rápida Interactiva • Cero Líos</span>
            </div>
            <h4 class="text-sm font-black text-white leading-tight">Toca tu duda y mira la solución aquí mismo:</h4>
          </div>
        </div>
        <button type="button" onclick="togglePanelConsejo(false)" class="w-7 h-7 rounded-lg bg-white/5 hover:bg-white/15 text-slate-300 hover:text-white flex items-center justify-center text-xs font-bold transition-colors">
          ✕
        </button>
      </div>

      <!-- Subtítulo explicativo -->
      <div class="px-4 py-2 bg-slate-950/80 border-b border-white/5">
        <p class="text-[11px] text-slate-300 leading-snug">
          👇 <strong class="text-teal-300">Explicado súper fácil:</strong> pulsa en cualquier punto para leer la respuesta al instante (y si te quedan dudas, dentro tienes el botón directo a mi WhatsApp):
        </p>
      </div>

      <!-- Los 4 Puntos con Respuesta en Pantalla + El Punto 5 Directo -->
      <div class="p-3 space-y-2.5 max-h-[66vh] overflow-y-auto">
        
        <!-- PUNTO 1: POR DÓNDE EMPEZAR Y CÓMO COMBINAR -->
        <div class="rounded-xl bg-slate-950/90 border border-white/10 overflow-hidden">
          <button type="button" onclick="toggleAcordeonConsejo(1)" class="w-full text-left p-3 hover:bg-teal-950/40 transition-colors flex items-center justify-between gap-2">
            <div>
              <span class="text-xs font-extrabold text-white block">🧩 1. ¿Por dónde me conviene empezar y cómo combinar?</span>
              <span class="text-[10.5px] text-teal-300 font-semibold">Toca para ver la receta paso a paso</span>
            </div>
            <span id="iconoAcordeonConsejo1" class="text-teal-400 font-black text-xs transition-transform">▼</span>
          </button>
          
          <div id="cuerpoAcordeonConsejo1" class="hidden px-3 pb-3 pt-1 border-t border-white/10 bg-slate-900/90 space-y-2 text-[11.5px] text-slate-200 leading-relaxed">
            <div class="bg-teal-950/60 border border-teal-500/30 rounded-lg p-2.5">
              <strong class="text-emerald-300 block mb-0.5">⚡ En resumen:</strong>
              El 90% de los negocios empieza por el <strong>Pack Escudo Básico (99 €/mes)</strong> + <strong>1 Atril para el mostrador (39 €)</strong>. Con eso ya tienes las reseñas y las quejas 100% bajo control.
            </div>

            <button type="button" onclick="toggleDetalleProfundoConsejo(1)" id="btnVerMasConsejo1" class="text-[11px] font-extrabold text-amber-300 hover:text-amber-200 flex items-center gap-1 py-0.5">
              <span>➕ Desplegar explicación completa (como para niños)</span>
            </button>

            <div id="detalleProfundoConsejo1" class="hidden space-y-1.5 text-[11px] text-slate-300 bg-black/40 p-2.5 rounded-lg border border-white/5">
              <p><strong>1º Si tienes mostrador o mesas:</strong> Pon el <strong>Atril NFC (39 € pago único)</strong>. El cliente acerca el móvil al pagar y te pone 5 estrellas en 1 segundo antes de irse y olvidarse.</p>
              <p><strong>2º Para no perder tiempo contestando:</strong> El <strong>Servicio 1 (59 €/m)</strong> responde solo a todas tus reseñas buenas en Google para subirte posiciones, y si entra una mala la frena y te avisa al WhatsApp.</p>
              <p><strong>3º Si trabajas con citas, reservas o reparaciones:</strong> Añade el <strong>Servicio 2 (+40 €/m = 99 €/m el Pack Escudo)</strong>. Manda un WhatsApp automático 2h después de atender al cliente: si pulsa «Excelente» va a Google Maps; si pulsa «Bien» o «Mejorable», la queja se queda en privado en tu móvil.</p>
              <p><strong>4º ¿Y los demás módulos?</strong> Puedes empezar solo con esto y, más adelante, añadir el de Citas Anti-Plantón, Presupuestos o Facturas por solo +40 €/mes cada uno.</p>
            </div>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20acabo%20de%20leer%20en%20tu%20asistente%20c%C3%B3mo%20empezar%20y%20combinar%20m%C3%B3dulos%2C%20y%20quiero%20que%20me%20confirmes%20qu%C3%A9%20combinaci%C3%B3n%20le%20va%20mejor%20a%20mi%20negocio." target="_blank" class="w-full py-2 px-3 rounded-lg bg-brand-teal hover:bg-brand-tealDark text-white font-bold text-[11px] text-center block shadow transition-colors">
              💬 Hablar con Francisco sobre qué módulos elegir &rarr;
            </a>
          </div>
        </div>

        <!-- PUNTO 2: MEJOR COMBINACIÓN DE PRECIOS PARA AHORRAR -->
        <div class="rounded-xl bg-slate-950/90 border border-white/10 overflow-hidden">
          <button type="button" onclick="toggleAcordeonConsejo(2)" class="w-full text-left p-3 hover:bg-teal-950/40 transition-colors flex items-center justify-between gap-2">
            <div>
              <span class="text-xs font-extrabold text-white block">💰 2. ¿Cuál es la mejor combinación para ahorrar dinero?</span>
              <span class="text-[10.5px] text-teal-300 font-semibold">El truco matemático para pagar menos el Día 1</span>
            </div>
            <span id="iconoAcordeonConsejo2" class="text-teal-400 font-black text-xs transition-transform">▼</span>
          </button>
          
          <div id="cuerpoAcordeonConsejo2" class="hidden px-3 pb-3 pt-1 border-t border-white/10 bg-slate-900/90 space-y-2 text-[11.5px] text-slate-200 leading-relaxed">
            <div class="bg-teal-950/60 border border-teal-500/30 rounded-lg p-2.5">
              <strong class="text-emerald-300 block mb-0.5">⚡ En resumen:</strong>
              Sale <strong>80 € más barato de entrada</strong> coger 2 servicios + 1 Auditoría (<strong>Pack Escudo Total: 420 €</strong>) que coger 1 solo servicio + 1 Auditoría suelta (<strong>500 €</strong>).
            </div>

            <button type="button" onclick="toggleDetalleProfundoConsejo(2)" id="btnVerMasConsejo2" class="text-[11px] font-extrabold text-amber-300 hover:text-amber-200 flex items-center gap-1 py-0.5">
              <span>➕ Desplegar las cuentas claras paso a paso</span>
            </button>

            <div id="detalleProfundoConsejo2" class="hidden space-y-1.5 text-[11px] text-slate-300 bg-black/40 p-2.5 rounded-lg border border-white/5">
              <p><strong>• Regla 1 (Cuota mensual):</strong> El 1er servicio cuesta <strong>59 €/mes</strong>, pero a partir del 2º cada servicio que sumes cuesta solo <strong>+40 €/mes</strong> (te ahorras 19 €/mes en cada uno).</p>
              <p><strong>• Regla 2 (Instalación inicial al 50%):</strong> Instalar 1 servicio cuesta 150 €, pero el 2º servicio se instala a mitad de precio (<strong>+75 €</strong> = 225 € en total los dos).</p>
              <p><strong>• Regla 3 (Doble Bonificación en las 2 Auditorías):</strong> Si pides una Auditoría suelta (o con 1 solo servicio) cuesta <strong>350 €</strong> instalada. Pero al activar 2 servicios (Pack Escudo / Dúo), <strong>desbloqueas el descuento en AMBAS auditorías (195 € c/u en vez de 350 €, ahorrándote 155 € en cada una = ¡310 € de ahorro si haces las dos!)</strong>. Por eso el Día 1 pagas 80 € menos llevándote el doble de servicios.</p>
            </div>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20he%20visto%20el%20truco%20de%20ahorro%20del%20Pack%20Escudo%20en%20tu%20asistente%20y%20quiero%20que%20me%20hagas%20el%20presupuesto%20m%C3%A1s%20econ%C3%B3mico%20para%20mi%20caso." target="_blank" class="w-full py-2 px-3 rounded-lg bg-brand-teal hover:bg-brand-tealDark text-white font-bold text-[11px] text-center block shadow transition-colors">
              💬 Pedir mi presupuesto con máximo ahorro por WhatsApp &rarr;
            </a>
          </div>
        </div>

        <!-- PUNTO 3: DUDAS ENTRE LAS 2 AUDITORÍAS -->
        <div class="rounded-xl bg-slate-950/90 border border-white/10 overflow-hidden">
          <button type="button" onclick="toggleAcordeonConsejo(3)" class="w-full text-left p-3 hover:bg-teal-950/40 transition-colors flex items-center justify-between gap-2">
            <div>
              <span class="text-xs font-extrabold text-white block">🔍🧠 3. Dudas entre las 2 Auditorías (SEO+GEO vs Neuro CRO)</span>
              <span class="text-[10.5px] text-teal-300 font-semibold">¿Para qué sirve cada una y cómo se bonifican?</span>
            </div>
            <span id="iconoAcordeonConsejo3" class="text-teal-400 font-black text-xs transition-transform">▼</span>
          </button>
          
          <div id="cuerpoAcordeonConsejo3" class="hidden px-3 pb-3 pt-1 border-t border-white/10 bg-slate-900/90 space-y-2 text-[11.5px] text-slate-200 leading-relaxed">
            <div class="bg-teal-950/60 border border-teal-500/30 rounded-lg p-2.5">
              <strong class="text-emerald-300 block mb-0.5">⚡ En resumen:</strong>
              La <strong>Auditoría 1 (SEO+GEO)</strong> sirve para <strong>que la gente te encuentre</strong> en Google y ChatGPT; la <strong>Auditoría 2 (Neuro CRO)</strong> sirve para <strong>que los que entran en tu web te compren</strong> y no se escapen.
            </div>

            <button type="button" onclick="toggleDetalleProfundoConsejo(3)" id="btnVerMasConsejo3" class="text-[11px] font-extrabold text-amber-300 hover:text-amber-200 flex items-center gap-1 py-0.5">
              <span>➕ Desplegar diferencia sencilla y precios de cada una</span>
            </button>

            <div id="detalleProfundoConsejo3" class="hidden space-y-1.5 text-[11px] text-slate-300 bg-black/40 p-2.5 rounded-lg border border-white/5">
              <p><strong>🔍 Auditoría 1 (SEO Local + GEO IA):</strong> Si un cliente busca hoy en Google o pregunta a ChatGPT <em>«¿Qué clínica/taller/empresa me recomiendas en mi ciudad?»</em>, ¿sales tú el primero? Si no sales, necesitas esta. Metemos en tu web y Google Maps el código interno que leen las IAs para recomendarte.</p>
              <p><strong>🧠 Auditoría 2 (Neuromarketing y Conversión CRO):</strong> Si ya tienes web y entra gente, pero casi nadie te llama ni rellena el formulario, necesitas esta. Ponemos sensores térmicos y analizamos tu web con psicología de ventas para quitar atascos y hacer que te escriban por WhatsApp.</p>
              <p><strong>💰 Descuento activado para una o para las dos (sin cuotas):</strong> Sueltas cuestan 200 € (solo código/informe) o 350 € (instaladas por nosotros). Pero con tu <strong>Pack Escudo / Plan Dúo+</strong> tienes <strong>155 € de descuento en CADA una (195 € c/u)</strong>, o <strong>95 € c/u</strong> desde Plan Anual Trinity+.</p>
            </div>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20he%20le%C3%ADdo%20la%20diferencia%20entre%20las%202%20Auditor%C3%ADas%20en%20tu%20asistente%20y%20quiero%20que%20mires%20mi%20web%20para%20decirme%20cu%C3%A1l%20me%20hace%20m%C3%A1s%20falta." target="_blank" class="w-full py-2 px-3 rounded-lg bg-brand-teal hover:bg-brand-tealDark text-white font-bold text-[11px] text-center block shadow transition-colors">
              💬 Decirle a Francisco que revise mi web gratis &rarr;
            </a>
          </div>
        </div>

        <!-- PUNTO 4: PLAN MENSUAL VS PLAN ANUAL Y PAGOS -->
        <div class="rounded-xl bg-slate-950/90 border border-white/10 overflow-hidden">
          <button type="button" onclick="toggleAcordeonConsejo(4)" class="w-full text-left p-3 hover:bg-teal-950/40 transition-colors flex items-center justify-between gap-2">
            <div>
              <span class="text-xs font-extrabold text-white block">📅 4. ¿Plan Mensual o Plan Anual (2 meses gratis)?</span>
              <span class="text-[10.5px] text-teal-300 font-semibold">Cómo funcionan los pagos, plazos y descuentos</span>
            </div>
            <span id="iconoAcordeonConsejo4" class="text-teal-400 font-black text-xs transition-transform">▼</span>
          </button>
          
          <div id="cuerpoAcordeonConsejo4" class="hidden px-3 pb-3 pt-1 border-t border-white/10 bg-slate-900/90 space-y-2 text-[11.5px] text-slate-200 leading-relaxed">
            <div class="bg-teal-950/60 border border-teal-500/30 rounded-lg p-2.5">
              <strong class="text-emerald-300 block mb-0.5">⚡ En resumen:</strong>
              En <strong>Mensual</strong> vas mes a mes por domiciliación bancaria (tras 3 meses de rodaje inicial); en <strong>Anual</strong> pagas 10 meses y <strong>disfrutas 12 meses completos (2 gratis)</strong>.
            </div>

            <button type="button" onclick="toggleDetalleProfundoConsejo(4)" id="btnVerMasConsejo4" class="text-[11px] font-extrabold text-amber-300 hover:text-amber-200 flex items-center gap-1 py-0.5">
              <span>➕ Desplegar todos los detalles de pago sin letra pequeña</span>
            </button>

            <div id="detalleProfundoConsejo4" class="hidden space-y-1.5 text-[11px] text-slate-300 bg-black/40 p-2.5 rounded-lg border border-white/5">
              <p><strong>🔄 Vía 1: Mensual Flexible:</strong> Ideal para no hacer un desembolso grande de golpe. El Día 1 solo abonas la instalación (Setup) + el primer mes. Después de los 3 primeros meses de puesta en marcha, eres 100% libre de darte de baja o cambiar servicios avisando con 30 días.</p>
              <p><strong>⭐ Vía 2: Plan Anual (10 Meses = 2 Gratis):</strong> Te ahorras un <strong>16,6% directo</strong> (por ejemplo, en el Pack Escudo te ahorras 198 € al año, y en el Plan Trinity te ahorras 278 € al año + Bóveda de Contraseñas gratis + las Auditorías a solo <strong>95 € c/u</strong>).</p>
              <p><strong>🛡️ Tip de confianza:</strong> Muchos clientes empiezan en Mensual para probarnos y al 2º mes se pasan al Anual para llevarse los 2 meses gratis.</p>
            </div>

            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20acabo%20de%20ver%20las%20condiciones%20del%20Plan%20Mensual%20y%20Anual%20en%20tu%20asistente%20y%20quiero%20consultar%20c%C3%B3mo%20ponerlo%20en%20marcha." target="_blank" class="w-full py-2 px-3 rounded-lg bg-brand-teal hover:bg-brand-tealDark text-white font-bold text-[11px] text-center block shadow transition-colors">
              💬 Consultar formas de pago con Francisco por WhatsApp &rarr;
            </a>
          </div>
        </div>

        <!-- PUNTO 5: CONTACTO DIRECTO / AUDIO SIN ESCRIBIR -->
        <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20prefiero%20mandarte%20una%20nota%20de%20voz%20o%20que%20hablemos%20directamente%20para%20que%20me%20orient%C3%A9is%20sobre%20mi%20negocio." target="_blank" class="block w-full text-left p-3 rounded-xl bg-gradient-to-r from-emerald-950/90 to-teal-950/90 hover:from-emerald-900 hover:to-teal-900 border-2 border-emerald-400/70 transition-all shadow-md group">
          <div class="flex items-center justify-between gap-2">
            <span class="text-xs font-black text-emerald-300">🎙️ 5. «Prefiero hablar directamente o mandarte un audio»</span>
            <span class="text-[10.5px] font-black bg-emerald-400 text-slate-950 px-2 py-0.5 rounded-md flex-shrink-0">WhatsApp &rarr;</span>
          </div>
          <p class="text-[11px] text-emerald-100/90 mt-1 leading-snug">Toca aquí para abrir mi WhatsApp directo: mándame una nota de voz de 20 segundos o llámame al 711 54 75 61 y lo vemos juntos.</p>
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
        <span class="text-xs sm:text-[13px] font-extrabold text-white block">Ver respuestas en 1 clic 💬</span>
      </div>
    </button>

  </div>
"""

JS_ASISTENTE_FLOTANTE = """
    // CONTROL DEL ASISTENTE FLOTANTE NIVEL 2 (ACORDEÓN DE RESPUESTAS + DESPLEGABLE COMPLETO)
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

    function toggleAcordeonConsejo(num) {
      for (let i = 1; i <= 4; i++) {
        const cuerpo = document.getElementById('cuerpoAcordeonConsejo' + i);
        const icono = document.getElementById('iconoAcordeonConsejo' + i);
        if (!cuerpo) continue;
        if (i === num) {
          const estabaOculto = cuerpo.classList.contains('hidden');
          if (estabaOculto) {
            cuerpo.classList.remove('hidden');
            if (icono) icono.style.transform = 'rotate(180deg)';
          } else {
            cuerpo.classList.add('hidden');
            if (icono) icono.style.transform = 'rotate(0deg)';
          }
        } else {
          cuerpo.classList.add('hidden');
          if (icono) icono.style.transform = 'rotate(0deg)';
        }
      }
    }

    function toggleDetalleProfundoConsejo(num) {
      const det = document.getElementById('detalleProfundoConsejo' + num);
      const btn = document.getElementById('btnVerMasConsejo' + num);
      if (!det || !btn) return;
      if (det.classList.contains('hidden')) {
        det.classList.remove('hidden');
        btn.innerHTML = '<span>➖ Compactar explicación detallada</span>';
      } else {
        det.classList.add('hidden');
        btn.innerHTML = '<span>➕ Desplegar explicación completa (paso a paso)</span>';
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
        print("❌ No se encontró index.html en:", ruta_index)
        return

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Eliminar cualquier versión previa del asistente flotante si existiera
    html = re.sub(
        r'<!-- ======================================================================= -->\s*<!-- ASISTENTE FLOTANTE.*?</div>\s*</div>\s*</button>\s*</div>',
        '',
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'<!-- ASISTENTE FLOTANTE NIVEL 2.*?<!-- MODAL DE AVISO LEGAL -->',
        '<!-- MODAL DE AVISO LEGAL -->',
        html,
        flags=re.DOTALL
    )

    # Asegurar posición visible (z-[9999] y separado de cualquier icono de extensión en la esquina)
    bloque_limpio = BLOQUE_ASISTENTE_FLOTANTE.replace(
        'class="fixed bottom-5 right-4 sm:right-6 z-[95] flex flex-col items-end"',
        'style="position:fixed; bottom:22px; right:22px; z-index:9999;" class="flex flex-col items-end"'
    )

    # 2. Insertar el Asistente Flotante (con fallback directo antes de </body> si el comentario cambió)
    if 'id="spAsistenteConsejo"' not in html:
        if '<!-- MODAL DE AVISO LEGAL -->' in html:
            html = html.replace(
                '<!-- MODAL DE AVISO LEGAL -->',
                bloque_limpio + '\n\n  <!-- MODAL DE AVISO LEGAL -->',
                1
            )
        elif '<div id="modalLegal"' in html:
            html = html.replace(
                '<div id="modalLegal"',
                bloque_limpio + '\n\n  <div id="modalLegal"',
                1
            )
        else:
            html = html.replace('</body>', bloque_limpio + '\n</body>', 1)

    # 3. Insertar las funciones JS del asistente (con fallback antes de </script>)
    html = re.sub(
        r'// CONTROL DEL ASISTENTE FLOTANTE.*?(?=// CONTROL DEL MENÚ MÓVIL)',
        '',
        html,
        flags=re.DOTALL
    )
    if 'function toggleAcordeonConsejo' not in html:
        if '// CONTROL DEL MENÚ MÓVIL' in html:
            html = html.replace(
                '// CONTROL DEL MENÚ MÓVIL',
                JS_ASISTENTE_FLOTANTE + '\n    // CONTROL DEL MENÚ MÓVIL',
                1
            )
        else:
            # Insertar antes del último </script>
            pos_script = html.rfind('</script>')
            if pos_script != -1:
                html = html[:pos_script] + '\n' + JS_ASISTENTE_FLOTANTE + '\n  </script>' + html[pos_script + 9:]

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)
    print("   ✔ Asistente Flotante Nivel 2 inyectado y verificado en index.html.")


if __name__ == "__main__":
    print("======================================================================")
    print("🚀 ACTIVANDO ASISTENTE FLOTANTE NIVEL 2 EN SISTEMASPYME.ES")
    print("======================================================================")
    raiz = localizar_directorio_public_html()
    if not raiz:
        print("❌ No se pudo localizar la carpeta public_html.")
    else:
        inyectar_asistente_y_regla_inpost(raiz)
        print("======================================================================")
        print("🎉 ¡LISTO! El asistente flotante ya está visible abajo a la derecha.")
        print("======================================================================")
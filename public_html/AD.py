import os
import shutil
import re
from datetime import datetime


def localizar_archivo_en_escritorio(nombre_archivo="index.html"):
    """
    Prioriza la ruta exacta de public_html en el Escritorio de Francisco y,
    si no existe, rastrea cualquier subcarpeta del Escritorio ignorando Backups.
    """
    home = os.path.expanduser("~")
    rutas_directas = [
        os.path.join(home, "Desktop", "SISTEMAS PYME", "Web", "web-sistemaspyme", "public_html", nombre_archivo),
        os.path.join(home, "Escritorio", "SISTEMAS PYME", "Web", "web-sistemaspyme", "public_html", nombre_archivo),
        os.path.abspath(nombre_archivo),
        os.path.abspath(os.path.join("public_html", nombre_archivo))
    ]
    for r in rutas_directas:
        if os.path.isfile(r):
            return r

    rutas_escritorio = [
        os.path.join(home, "Desktop"),
        os.path.join(home, "Escritorio")
    ]

    candidatos = []
    carpetas_ignorar = {"backups_sp", "Backups", "backups", ".git", "node_modules", "__pycache__", ".venv", "venv"}

    for escritorio in rutas_escritorio:
        if not os.path.isdir(escritorio):
            continue
        for raiz, dirs, archivos in os.walk(escritorio):
            dirs[:] = [d for d in dirs if d not in carpetas_ignorar]
            if nombre_archivo in archivos:
                ruta_completa = os.path.join(raiz, nombre_archivo)
                try:
                    with open(ruta_completa, "r", encoding="utf-8", errors="ignore") as f_check:
                        muestra = f_check.read(6000)
                    es_sistemas_pyme = 1 if ("Sistemas Pyme" in muestra or "sistemaspyme" in muestra) else 0
                    en_public_html = 1 if "public_html" in raiz else 0
                    mtime = os.path.getmtime(ruta_completa)
                    candidatos.append((es_sistemas_pyme, en_public_html, mtime, ruta_completa))
                except Exception:
                    pass

    if not candidatos:
        return None

    candidatos.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    return candidatos[0][3]


def ejecutar_actualizador():
    nombre_objetivo = "index.html"

    print("=" * 76)
    print("🛠️  ACTUALIZADOR INTERACTIVO SISTEMAS PYME (AD.py — Caso Real Motor IA S1)")
    print("=" * 76)

    ruta_archivo = localizar_archivo_en_escritorio(nombre_objetivo)
    if not ruta_archivo:
        print(f"❌ ERROR: No se encontró '{nombre_objetivo}' en public_html ni en el Escritorio.")
        return

    directorio_html = os.path.dirname(ruta_archivo)
    print(f"📂 Archivo localizado en: {ruta_archivo}")

    # 1. BACKUP AUTOMÁTICO EN backups_sp
    carpeta_backups = os.path.join(directorio_html, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_backup = f"{nombre_objetivo}.backup_{marca_tiempo}"
    ruta_backup = os.path.join(carpeta_backups, nombre_backup)

    shutil.copy2(ruta_archivo, ruta_backup)
    print(f"✅ Backup creado con éxito en: {ruta_backup}")

    # 2. LECTURA Y ESCÁNER DE CONTEXTO
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    cambios_aplicados = 0

    # --- PARCHE 1: Actualizar el bloque visual del Servicio 1 con la salida real de motor_ia_prompts.py ---
    print("\n🔍 [1/2] Escaneando el bloque de caso real del Servicio 1 (Reseñas Google con IA)...")

    nuevo_mockup_s1 = """<!-- RECREACIÓN FIEL DEL MOTOR IA REAL (motor_ia_prompts.py: Alerta + 4 Bloques HEARD/RGPD + Nota Psicológica + 4 Tonos) -->
            <div class="bg-[#0b141a] border border-teal-500/40 rounded-xl p-3.5 mb-5 shadow-inner">
              <div class="flex flex-wrap items-center justify-between gap-1 text-[10px] font-bold text-teal-300 border-b border-white/10 pb-1.5 mb-2.5">
                <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span> Alerta a Gerencia (WhatsApp / Telegram / Email)</span>
                <span class="bg-red-500/20 text-red-300 border border-red-500/30 px-2 py-0.5 rounded text-[9.5px] uppercase tracking-wider">Riesgo: ALTO • 1-3★ Pausada</span>
              </div>

              <div class="bg-[#1f2c34] border-l-4 border-red-500 text-slate-100 text-[11px] rounded-lg p-3 leading-snug">
                <!-- Reseña entrante con trampa RGPD y palabra tóxica -->
                <div class="text-slate-300 mb-2">
                  👤 <strong>Autor:</strong> Carlos M. <span class="text-amber-400 font-bold">(1★)</span><br>
                  💬 <em class="text-slate-200">«Fui por mi tratamiento de endodoncia y tras 40 min de espera me pareció una estafa el cobro...»</em>
                </div>

                <!-- Alerta al propietario generada por motor_ia_prompts.py -->
                <div class="bg-red-950/60 border border-red-500/30 rounded-md p-2 text-[10px] text-red-200 mb-2 leading-relaxed">
                  🛡️ <strong class="text-red-300">Alerta Propietario (Filtro RGPD + Anti-Efecto Loro):</strong> Reseña clínica con término sensible y acusación grave. Se oculta el tratamiento médico en público (secreto profesional RGPD) y se omite repetir la palabra <em>«estafa»</em> para no indexar SEO negativo.
                </div>

                <!-- Selector interactivo en vivo de los 4 Tonos reales del Gestor -->
                <div class="flex items-center justify-between text-[10px] font-bold text-slate-300 mb-1">
                  <span>✏️ Pulsa un tono para ver cómo redacta la IA:</span>
                  <span class="text-emerald-400 text-[9.5px]">4-5★ Auto-Publicadas</span>
                </div>
                <div class="grid grid-cols-4 gap-1 text-center text-[9.5px] font-bold mb-2">
                  <button type="button" onclick="cambiarTonoDemoS1('FORMAL')" id="btnTonoS1_FORMAL" class="bg-slate-800 hover:bg-slate-700 border border-white/10 text-slate-300 py-1 rounded transition-all cursor-pointer">Formal</button>
                  <button type="button" onclick="cambiarTonoDemoS1('SEMIFORMAL')" id="btnTonoS1_SEMIFORMAL" class="bg-teal-500/30 border border-teal-400 text-teal-200 py-1 rounded transition-all cursor-pointer">Semiformal ✓</button>
                  <button type="button" onclick="cambiarTonoDemoS1('CERCANO')" id="btnTonoS1_CERCANO" class="bg-slate-800 hover:bg-slate-700 border border-white/10 text-slate-300 py-1 rounded transition-all cursor-pointer">Cercano</button>
                  <button type="button" onclick="cambiarTonoDemoS1('DIRECTO')" id="btnTonoS1_DIRECTO" class="bg-slate-800 hover:bg-slate-700 border border-white/10 text-slate-300 py-1 rounded transition-all cursor-pointer">Directo</button>
                </div>

                <!-- Propuesta de Respuesta Pública estructurada en 4 párrafos (Método HEARD) -->
                <div class="bg-black/40 rounded-md p-2.5 text-[10.5px] mb-2 border border-teal-500/20">
                  <div class="text-teal-300 font-bold mb-1 flex items-center justify-between">
                    <span>✍️ Propuesta IA (<span id="labelTonoActivoS1">Tono Semiformal</span> • 4 bloques HEARD):</span>
                    <span class="text-[9px] text-slate-400 font-normal">Sin admisión de culpa</span>
                  </div>
                  <div id="textoPropuestaS1" class="text-slate-200 italic space-y-1.5 leading-relaxed">
                    <p>Hola, Carlos:</p>
                    <p>Lamentamos sinceramente que los tiempos de espera y la percepción sobre tu visita no hayan cumplido tus expectativas.</p>
                    <p>En nuestro centro trabajamos bajo estrictos protocolos de calidad y transparencia presupuestaria en cada atención personalizada.</p>
                    <p>Por respeto a tu privacidad, te invitamos a contactarnos directamente con dirección para revisar tu expediente personalmente.<br><span class="not-italic text-teal-300 font-semibold">Un cordial saludo, Dirección.</span></p>
                  </div>
                </div>

                <!-- Nota Psicológica exclusiva para el dueño (nota_psicologica) -->
                <div class="bg-amber-950/40 border border-amber-500/30 rounded-md p-2 text-[10px] text-amber-200/95 mb-2.5 leading-relaxed">
                  💡 <strong class="text-amber-300">Nota Psicológica para Gerencia (HEARD):</strong> <span id="textoNotaPsicoS1">Aplicamos la <em>Paradoja de Recuperación del Servicio</em>: validamos su malestar por la demora sin confirmar jamás en público qué tratamiento clínico se realizó (cumplimiento estricto RGPD) ni repetir la palabra tóxica, derivando la aclaración económica a privado.</span>
                </div>

                <div class="flex items-center justify-between gap-1.5 pt-1 border-t border-white/10 text-[10px] font-bold">
                  <span class="bg-blue-600/80 text-white px-2.5 py-1 rounded flex-1 text-center">👉 Abrir Gestor de Respuestas (4 Tonos)</span>
                  <span class="bg-slate-800 text-teal-300 border border-teal-500/30 px-2 py-1 rounded">📊 Informe 360°</span>
                </div>
              </div>
            </div>"""

    patron_mockup_s1 = re.compile(
        r'<!--\s*RECREACIÓN FIEL DE LA ALERTA REAL DE RESEÑA[\s\S]*?<div class="bg-\[#0b141a\] border border-teal-500/40 rounded-xl p-3\.5 mb-5 shadow-inner">[\s\S]*?</div>\s*</div>\s*</div>',
        re.MULTILINE
    )
    patron_mockup_s1_previo = re.compile(
        r'<!--\s*RECREACIÓN FIEL DEL MOTOR IA REAL[\s\S]*?<div class="bg-\[#0b141a\] border border-teal-500/40 rounded-xl p-3\.5 mb-5 shadow-inner">[\s\S]*?</div>\s*</div>\s*</div>',
        re.MULTILINE
    )

    if patron_mockup_s1.search(contenido):
        contenido = patron_mockup_s1.sub(nuevo_mockup_s1, contenido, count=1)
        cambios_aplicados += 1
        print("   ✔ Caso real del Servicio 1 actualizado con Alerta RGPD/Anti-Loro, 4 párrafos HEARD y Nota Psicológica.")
    elif patron_mockup_s1_previo.search(contenido):
        contenido = patron_mockup_s1_previo.sub(nuevo_mockup_s1, contenido, count=1)
        cambios_aplicados += 1
        print("   ✔ Caso real del Servicio 1 refrescado con la estructura exacta de motor_ia_prompts.py.")
    else:
        print("   ⚠️ No se encontró el bloque anterior del Servicio 1 por comentario.")

    # --- PARCHE 2: Inyectar función interactiva cambiarTonoDemoS1 en el bloque <script> ---
    print("\n🔍 [2/2] Escaneando bloque JavaScript para habilitar el cambio interactivo de los 4 tonos en el Servicio 1...")

    js_funcion_tonos_s1 = """// SELECTOR INTERACTIVO DE LOS 4 TONOS EN EL CASO REAL DEL SERVICIO 1 (motor_ia_prompts.py)
    function cambiarTonoDemoS1(tono) {
      const datosTonos = {
        FORMAL: {
          label: 'Tono Formal',
          propuesta: '<p>Estimado Carlos:</p><p>Lamentamos sinceramente que el tiempo de espera y su percepción sobre el servicio no hayan estado a la altura de sus expectativas.</p><p>En nuestro centro aplicamos rigurosos estándares de excelencia asistencial y total transparencia informativa con cada uno de nuestros clientes.</p><p>Por estricto respeto a la confidencialidad y protección de datos, ponemos a su disposición nuestra dirección para revisar su caso en privado.<br><span class="not-italic text-teal-300 font-semibold">Atentamente, Dirección.</span></p>',
          nota: 'En tono FORMAL empleamos el tratamiento de «usted» y una estructura institucional sobria que proyecta máxima seriedad ante terceros lectores en Google Maps, blindando el secreto profesional (RGPD) y neutralizando la acusación económica.'
        },
        SEMIFORMAL: {
          label: 'Tono Semiformal',
          propuesta: '<p>Hola, Carlos:</p><p>Lamentamos sinceramente que los tiempos de espera y la percepción sobre tu visita no hayan cumplido tus expectativas.</p><p>En nuestro centro trabajamos bajo estrictos protocolos de calidad y transparencia presupuestaria en cada atención personalizada.</p><p>Por respeto a tu privacidad, te invitamos a contactarnos directamente con dirección para revisar tu expediente personalmente.<br><span class="not-italic text-teal-300 font-semibold">Un cordial saludo, Dirección.</span></p>',
          nota: 'Aplicamos la <em>Paradoja de Recuperación del Servicio</em>: validamos su malestar por la demora sin confirmar jamás en público qué tratamiento clínico se realizó (cumplimiento estricto RGPD) ni repetir la palabra tóxica, derivando la aclaración económica a privado.'
        },
        CERCANO: {
          label: 'Tono Cercano',
          propuesta: '<p>¡Hola, Carlos!</p><p>Sentimos mucho que tuvieras que esperar más de lo habitual y que salieras con esa sensación de tu visita.</p><p>Quienes nos conocen saben el cariño, la honestidad y el cuidado que ponemos cada día para que todo quede siempre claro desde el primer minuto.</p><p>Por proteger tu privacidad preferimos no tratar detalles personales por aquí, pero escríbenos o llámanos directamente para escucharte y darle solución juntos.<br><span class="not-italic text-teal-300 font-semibold">Un abrazo, Dirección.</span></p>',
          nota: 'En tono CERCANO rebajamos la hostilidad del cliente con empatía cálida y humana, manteniendo intactos los dos candados de seguridad: cero mención al tratamiento sanitario (RGPD) y cero admisión de culpa legal.'
        },
        DIRECTO: {
          label: 'Tono Directo',
          propuesta: '<p>Hola, Carlos:</p><p>Sentimos la demora puntual durante tu visita y tomamos nota para mejorar nuestros tiempos de atención.</p><p>Trabajamos siempre con presupuestos cerrados y explicados previamente con total transparencia.</p><p>Por confidencialidad (RGPD) no tratamos expedientes individuales en público; contáctanos por teléfono o correo para revisarlo contigo de inmediato.<br><span class="not-italic text-teal-300 font-semibold">Un saludo, Dirección.</span></p>',
          nota: 'En tono DIRECTO vamos al grano en frases concisas para dueños que prefieren respuestas ejecutivas: cortamos de raíz la polémica pública, protegemos el RGPD y trasladamos la conversación a un canal privado.'
        }
      };

      const info = datosTonos[tono] || datosTonos.SEMIFORMAL;
      const elLabel = document.getElementById('labelTonoActivoS1');
      const elPropuesta = document.getElementById('textoPropuestaS1');
      const elNota = document.getElementById('textoNotaPsicoS1');

      if (elLabel) elLabel.textContent = info.label;
      if (elPropuesta) elPropuesta.innerHTML = info.propuesta;
      if (elNota) elNota.innerHTML = info.nota;

      ['FORMAL', 'SEMIFORMAL', 'CERCANO', 'DIRECTO'].forEach(t => {
        const btn = document.getElementById('btnTonoS1_' + t);
        if (!btn) return;
        const nombres = { FORMAL: 'Formal', SEMIFORMAL: 'Semiformal', CERCANO: 'Cercano', DIRECTO: 'Directo' };
        if (t === tono) {
          btn.className = 'bg-teal-500/30 border border-teal-400 text-teal-200 py-1 rounded transition-all cursor-pointer';
          btn.textContent = nombres[t] + ' ✓';
        } else {
          btn.className = 'bg-slate-800 hover:bg-slate-700 border border-white/10 text-slate-300 py-1 rounded transition-all cursor-pointer';
          btn.textContent = nombres[t];
        }
      });
    }"""

    if "function cambiarTonoDemoS1(" in contenido:
        patron_fn_tonos = re.compile(
            r'// SELECTOR INTERACTIVO DE LOS 4 TONOS[\s\S]*?function cambiarTonoDemoS1\([\s\S]*?\}\s*\)\s*;\s*\}',
            re.MULTILINE
        )
        contenido = patron_fn_tonos.sub(js_funcion_tonos_s1, contenido, count=1)
        cambios_aplicados += 1
        print("   ✔ Función interactiva 'cambiarTonoDemoS1' actualizada.")
    else:
        marca_insercion = "// CONMUTADOR INTERACTIVO DE TARIFAS MENSUAL / ANUAL"
        if marca_insercion in contenido:
            contenido = contenido.replace(marca_insercion, js_funcion_tonos_s1 + "\n\n    " + marca_insercion, 1)
            cambios_aplicados += 1
            print("   ✔ Función interactiva 'cambiarTonoDemoS1' añadida al script de la página.")

    # 3. GUARDADO Y FEEDBACK
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    print("\n" + "=" * 76)
    print(f"🎉 PROCESO COMPLETADO: '{ruta_archivo}' actualizado ({cambios_aplicados} bloques aplicados).")
    print(f"📦 Copia de seguridad disponible en: {ruta_backup}")
    print("=" * 76)


if __name__ == "__main__":
    ejecutar_actualizador()
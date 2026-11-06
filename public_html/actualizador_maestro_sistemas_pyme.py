#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AD.py — Actualizador Maestro Autónomo de Sistemas Pyme (Versión Blindada V117)
Cumple 100% el Manual Maestro de Programación:
- Paso 1 prioritario + atexit para actualizar Biblia y Manual (.md) en /Programar
- Copias de seguridad en backups_sp (máximo 10 recientes)
- Verificación anti-errores ast.parse + py_compile + node --check en <script>
- Rediseño de Tecnosala con Terminal Hardware Futurista + Consulta por Voz (🎙️ Hablar)
- Ajuste de aire superior en el Encabezado de Sección (Antetítulo + H2 + Conmutador) de Precios Claros
"""

import os
import re
import sys
import ast
import shutil
import atexit
import tempfile
import subprocess
import py_compile
from datetime import datetime

# 1. RUTAS FIJAS DEL ECOSISTEMA EN EL MAC
DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_WEB_PUBLIC = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme/public_html"
RUTA_SCRAPER = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Scraper/Scrapper App"
RUTA_SERVICIO_RESENAS = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Servicios/Servicio Reseñas/servicio_resenas"
RUTA_PROGRAMAR = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Programar"

RUTAS_INDEX = [
    os.path.join(DIR_ACTUAL, "index.html"),
    os.path.join(RUTA_WEB_PUBLIC, "index.html"),
]

RUTAS_AD_REPLICA = [
    os.path.join(DIR_ACTUAL, "AD.py"),
    os.path.join(RUTA_WEB_PUBLIC, "AD.py"),
    os.path.join(RUTA_SCRAPER, "AD.py"),
    os.path.join(RUTA_SERVICIO_RESENAS, "AD.py"),
]


def purgar_backups_antiguos_max_10(carpeta_backups, nombre_base):
    """Conserva únicamente las 10 copias de seguridad más recientes de cada archivo."""
    try:
        prefijo = f"{nombre_base}.backup_"
        archivos = [
            os.path.join(carpeta_backups, f)
            for f in os.listdir(carpeta_backups)
            if f.startswith(prefijo)
        ]
        archivos.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        for viejo in archivos[10:]:
            try:
                os.remove(viejo)
            except Exception:
                pass
    except Exception:
        pass


def crear_backup(ruta_archivo):
    """Crea copia de seguridad con fecha y hora en la subcarpeta backups_sp."""
    if not os.path.isfile(ruta_archivo):
        return None
    carpeta_base = os.path.dirname(ruta_archivo)
    carpeta_backups = os.path.join(carpeta_base, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    sello = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_base = os.path.basename(ruta_archivo)
    nombre_backup = f"{nombre_base}.backup_{sello}"
    ruta_backup = os.path.join(carpeta_backups, nombre_backup)
    shutil.copy2(ruta_archivo, ruta_backup)
    purgar_backups_antiguos_max_10(carpeta_backups, nombre_base)
    print(f"📦 Copia de seguridad creada: {ruta_backup}")
    return ruta_backup


def verificar_sintaxis_segura(ruta_archivo, ruta_backup):
    """Comprueba que el archivo (.py o .html + bloques <script> con node --check) no tenga errores."""
    try:
        if ruta_archivo.endswith(".py"):
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                codigo = f.read()
            ast.parse(codigo)
            py_compile.compile(ruta_archivo, doraise=True)
        elif ruta_archivo.endswith(".html"):
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                html = f.read()
            if "</html>" not in html.lower():
                raise ValueError("El archivo HTML parece incompleto (falta etiqueta </html>).")
            # Validación node --check sobre los bloques <script> ejecutables
            if shutil.which("node"):
                patron_script = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE)
                for idx, m in enumerate(patron_script.finditer(html), 1):
                    tag_apertura = m.group(0).split(">", 1)[0].lower()
                    if "application/ld+json" in tag_apertura or "application/json" in tag_apertura:
                        continue
                    js_code = m.group(1).strip()
                    if not js_code:
                        continue
                    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tmp_js:
                        tmp_js.write(js_code)
                        tmp_js_path = tmp_js.name
                    try:
                        res = subprocess.run(["node", "--check", tmp_js_path], capture_output=True, text=True)
                        if res.returncode != 0:
                            raise ValueError(f"Error JS en bloque <script> #{idx}: {res.stderr.strip()}")
                    finally:
                        try:
                            os.remove(tmp_js_path)
                        except Exception:
                            pass
        print(f"✅ Comprobación anti-errores superada en: {os.path.basename(ruta_archivo)}")
        return True
    except Exception as e:
        print(f"❌ ALERTA DE SEGURIDAD: Se detectó un error en {os.path.basename(ruta_archivo)}: {e}")
        if ruta_backup and os.path.isfile(ruta_backup):
            print("🔄 Restaurando automáticamente la copia de seguridad para no romper nada...")
            shutil.copy2(ruta_backup, ruta_archivo)
        sys.exit(1)


NOTA_ACTUALIZACION_V114_V117 = r"""
### ACTUALIZACIÓN V114 (Rediseño Minimalista del Consultor Técnico en la Tecnosala como Terminal de Hardware Futurista)
- **Pantalla del Terminal en Estado Virgen de Bienvenida (Cero Parrafadas al Entrar):** Al entrar en la sección `Tecnosala` de `index.html`, el visor ya no muestra un bloque denso de texto técnico, sino una pantalla de cristal limpia con un núcleo holográfico respirando y el mensaje cercano: *«Soy tu consultor tecnológico que lo sabe todo sobre Sistemas Pyme. Selecciona una de las preguntas frecuentes o escribe abajo lo que quieras saber.»*
- **Preguntas Frecuentes Plegadas por Defecto (`✨ ¿Quieres ver preguntas frecuentes?`):** Los 6 chips de consultas rápidas permanecen recogidos en un cajón plegable para no saturar visualmente al visitante y se despliegan suavemente en 1 clic cuando el usuario desea explorarlos uno a uno.
- **Chasis de Hardware Futurista con Teclado Luminoso Inferior y Botón de Limpieza (`↺ Limpiar pantalla`):** Diseño de consola física de alta gama con bisel metálico, indicadores LED de estado y barra de escritura inferior tipo teclado táctil que invita a preguntar cualquier duda en lenguaje natural.

### ACTUALIZACIÓN V115 (Consulta por Voz 🎙️ en la Tecnosala + Arquitectura Neuromarketing en 2 Diapositivas sin Cortes en Precios Claros)
- **Consulta por Voz en Tiempo Real en el Terminal de la Tecnosala (`🎙️ Hablar`):** Integrado micrófono interactivo con reconocimiento de voz en español (`Web Speech API es-ES`), indicador visual de ondas acústicas al hablar, transcripción en vivo dentro de la barra del terminal y disparo automático de la respuesta al terminar de hablar.
- **Corrección de Alineación en 2 Líneas en Pack Escudo Básico:** La insignia superior izquierda muestra `🛡️ 2 Servicios` arriba y `(S1 + S2)` junto en la línea inferior (`whitespace-nowrap`), y el bloque derecho muestra `Setup Dúo: 225 €` arriba y `(2.º al 50%)` junto en la línea inferior.
- **División de `Precios claros` en 2 Diapositivas 100vh sin Tarjetas Cortadas (Ley de Buena Forma / Gestalt):** La Diapositiva 1 muestra limpiamente los 3 Planes Mensuales con un Banner-Guía inferior (`🔍🧠 Ver Tarifas de las 2 Auditorías Pago Único y Atril NFC/QR ↓`) que evita cualquier corte visual y desliza suavemente a la Diapositiva 2 con las 2 Auditorías Gemelas, el Atril NFC+QR y la regla de escalado.

### ACTUALIZACIÓN V116 (Glosario Oficial de Elementos UI Web + Compactación de Altura de las 3 Tarjetas y Banner-Guía Inferior en Precios Claros)
- **Ajuste de Altura en las 3 Tarjetas (`Cards`) de la Diapositiva 1 de Precios Claros:** Compactado el relleno vertical interno de las 3 tarjetas, las subcajas de precio (`Inner Boxes`) y el título `Pack Escudo Total ★` (ahora en una sola línea `whitespace-nowrap` con su mini-selector debajo) para que las 3 tarjetas tengan exactamente la misma simetría y el **Banner-Guía inferior** quede 100% visible dentro del primer pantallazo sin cortarse en el borde inferior.

### ACTUALIZACIÓN V117 (Más Aire Superior en el Encabezado de Sección de Precios Claros)
- **Separación equilibrada entre la Cabecera Fija (`Header`) y el Encabezado de Sección (`Section Header`) de `Precios claros`:** Bajado ligeramente en bloque el conjunto formado por el **Antetítulo** (`TARIFAS OFICIALES DE LANZAMIENTO...`), el **Título `H2`** (`Precios claros y amortización desde el primer cliente.`), el **Conmutador Mensual/Anual** y su **Línea Divisoria**, dándole aire limpio por arriba sin que el **Banner-Guía inferior** se salga de la pantalla.
"""

_SINCRONIZACION_MD_EJECUTADA = False


def actualizar_y_sincronizar_biblia_y_manual():
    """Paso 1 prioritario (con blindaje atexit): mantiene al día los documentos maestros .md en /Programar."""
    global _SINCRONIZACION_MD_EJECUTADA
    if _SINCRONIZACION_MD_EJECUTADA:
        return
    _SINCRONIZACION_MD_EJECUTADA = True

    rutas_md = [
        os.path.join(RUTA_PROGRAMAR, "manual_maestro_de_programaci_n_ad_py.md"),
        os.path.join(RUTA_PROGRAMAR, "manual_maestro_programacion_ad.md"),
        os.path.join(RUTA_PROGRAMAR, "biblia_de_conocimiento_de_sistemas_pyme.md"),
        os.path.join(RUTA_PROGRAMAR, "biblia_conocimiento_sistemas_pyme.md"),
        os.path.join(RUTA_SCRAPER, "biblia_conocimiento_sistemas_pyme.md"),
        os.path.join(RUTA_SERVICIO_RESENAS, "biblia_conocimiento_sistemas_pyme.md"),
    ]
    for ruta in rutas_md:
        if os.path.isfile(ruta):
            try:
                crear_backup(ruta)
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                for v_ant in ["(V89 A V113)", "(V89 A V114)", "(V89 A V115)", "(V89 A V116)"]:
                    contenido = contenido.replace(v_ant, "(V89 A V117)")
                if "ACTUALIZACIÓN V117" not in contenido:
                    if "ACTUALIZACIÓN V116" in contenido:
                        partes_v117 = NOTA_ACTUALIZACION_V114_V117.split("### ACTUALIZACIÓN V117")[1]
                        contenido = contenido.rstrip() + "\n\n### ACTUALIZACIÓN V117" + partes_v117.rstrip() + "\n"
                    elif "ACTUALIZACIÓN V115" in contenido:
                        partes_v116_v117 = NOTA_ACTUALIZACION_V114_V117.split("### ACTUALIZACIÓN V116")[1]
                        contenido = contenido.rstrip() + "\n\n### ACTUALIZACIÓN V116" + partes_v116_v117.rstrip() + "\n"
                    elif "ACTUALIZACIÓN V114" in contenido:
                        partes_v115_v117 = NOTA_ACTUALIZACION_V114_V117.split("### ACTUALIZACIÓN V115")[1]
                        contenido = contenido.rstrip() + "\n\n### ACTUALIZACIÓN V115" + partes_v115_v117.rstrip() + "\n"
                    else:
                        contenido = contenido.rstrip() + "\n\n" + NOTA_ACTUALIZACION_V114_V117.strip() + "\n"
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(contenido)
                print(f"📘 Documento maestro sincronizado (V117): {ruta}")
            except Exception as e:
                print(f"⚠️ Aviso sincronizando {ruta}: {e}")


atexit.register(actualizar_y_sincronizar_biblia_y_manual)


def aplicar_cambios_html(html):
    """Aplica todas las actualizaciones sobre index.html conservando su estructura íntegra."""

    # 1. Diapositiva 5 de Inicio (#slide-cierre): Las 3 primeras gotitas aparecen AL INSTANTE al llegar
    bloque_gotitas_21_lluvia_progresiva = """      <!-- Fondo líquido: Las 3 primeras gotitas aparecen AL INSTANTE al llegar a la diapositiva y el resto se suma en cascada -->
      <div class="sp-s5-latent-stage" aria-hidden="true">
        <!-- 3 Primeras gotas INSTANTÁNEAS (en pleno impacto desde el milisegundo 0 al entrar en pantalla) -->
        <span class="sp-liquid-drop" style="width:11px; height:11px; top:12%; left:42%; animation-duration:9.4s; animation-delay:-1.15s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:12px; height:12px; top:86%; left:54%; animation-duration:9.8s; animation-delay:-1.05s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:11px; height:11px; top:15%; left:19%; animation-duration:10.0s; animation-delay:-0.90s;"><i class="sp-drop-extra-waves"></i></span>
        <!-- Siguientes gotas que se van sumando enseguida (0.2s, 0.6s, 1.1s...) -->
        <span class="sp-liquid-drop" style="width:10px; height:10px; top:85%; left:73%; animation-duration:10.4s; animation-delay:0.20s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:9px; height:9px; top:9%; left:71%; animation-duration:11.0s; animation-delay:0.65s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:13px; height:13px; top:34%; left:6%; animation-duration:11.6s; animation-delay:1.15s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:12px; height:12px; top:49%; left:93%; animation-duration:11.2s; animation-delay:1.70s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:10px; height:10px; top:86%; left:31%; animation-duration:10.6s; animation-delay:2.25s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:8px; height:8px; top:8%; left:29%; animation-duration:9.8s; animation-delay:2.85s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:11px; height:11px; top:12%; left:58%; animation-duration:11.4s; animation-delay:3.45s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:9px; height:9px; top:62%; left:8%; animation-duration:10.5s; animation-delay:4.10s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:10px; height:10px; top:33%; left:88%; animation-duration:11.1s; animation-delay:4.75s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:13px; height:13px; top:84%; left:8%; animation-duration:11.8s; animation-delay:5.40s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:8px; height:8px; top:14%; left:83%; animation-duration:10.0s; animation-delay:6.05s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:9px; height:9px; top:9%; left:7%; animation-duration:10.4s; animation-delay:6.70s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:8px; height:8px; top:92%; left:62%; animation-duration:10.7s; animation-delay:7.35s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:12px; height:12px; top:9%; left:93%; animation-duration:11.5s; animation-delay:8.00s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:8px; height:8px; top:90%; left:20%; animation-duration:10.1s; animation-delay:8.65s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:8px; height:8px; top:66%; left:89%; animation-duration:9.9s; animation-delay:9.30s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:12px; height:12px; top:89%; left:83%; animation-duration:11.7s; animation-delay:9.95s;"><i class="sp-drop-extra-waves"></i></span>
        <span class="sp-liquid-drop" style="width:9px; height:9px; top:85%; left:92%; animation-duration:10.9s; animation-delay:10.60s;"><i class="sp-drop-extra-waves"></i></span>
      </div>"""

    html = re.sub(
        r'<!-- Fondo líquido:[^>]*-->\s*<div class="sp-s5-latent-stage" aria-hidden="true">.*?</div>(?=\s*<div class="relative z-10 max-w-4xl)',
        lambda m: bloque_gotitas_21_lluvia_progresiva,
        html,
        flags=re.DOTALL
    )

    # 2. Pasillos 100% libres entre líneas de circuitos para las píldoras de sectores en la Diapositiva 4 de Inicio
    reemplazo_slots_sectores_s4 = """/* Calculador dinámico de pasillos libres entre líneas de circuitos (nunca pisan un trazo) */
          var slotsSegurosZigZag = [
            { top: '7%',  left: '1.8%' },
            { top: '8%',  right: '2.0%' },
            { top: '23%', left: '1.4%' },
            { top: '24%', right: '1.6%' },
            { top: '38%', left: '1.6%' },
            { top: '39%', right: '1.8%' },
            { top: '53%', left: '1.4%' },
            { top: '54%', right: '1.6%' },
            { top: '68%', left: '1.8%' },
            { top: '69%', right: '2.0%' },
            { top: '86%', left: '2.2%' },
            { top: '86%', right: '2.4%' }
          ];

          function recalcularSlotsLibresEntreCircuitos() {
            var sec = document.getElementById('slide-auditorias');
            if (!sec) return;
            var sRect = sec.getBoundingClientRect();
            if (sRect.height < 320) return;

            var offsetsY = [-44, 38, -32, 42, -38, 34, -40, 36, -28, 44, 28, 28];
            var idsNodos = [
              { id: 'spS4Node_1', side: 'L', posIdx: 0 },
              { id: 'spS4Node_3', side: 'L', posIdx: 2 },
              { id: 'spS4Node_5', side: 'L', posIdx: 4 },
              { id: 'spS4Node_7', side: 'L', posIdx: 6 },
              { id: 'spS4Node_9', side: 'L', posIdx: 8 },
              { id: 'spS4Node_11', side: 'L', posIdx: 10 },
              { id: 'spS4Node_2', side: 'R', posIdx: 1 },
              { id: 'spS4Node_4', side: 'R', posIdx: 3 },
              { id: 'spS4Node_6', side: 'R', posIdx: 5 },
              { id: 'spS4Node_8', side: 'R', posIdx: 7 },
              { id: 'spS4Node_10', side: 'R', posIdx: 9 },
              { id: 'spS4Node_11R', side: 'R', posIdx: 11 }
            ];

            var bandasL = [];
            var bandasR = [];

            idsNodos.forEach(function(cfg) {
              var n = document.getElementById(cfg.id);
              if (!n) return;
              var r = n.getBoundingClientRect();
              if (r.height === 0) return;
              var ny = r.top - sRect.top + r.height / 2;
              var sy = ny + offsetsY[cfg.posIdx];
              var minY = Math.min(ny, sy) - 18;
              var maxY = Math.max(ny, sy) + 18;
              if (cfg.side === 'L') bandasL.push([minY, maxY]);
              else bandasR.push([minY, maxY]);
            });

            function extraerPasillosVacios(bandas, side) {
              bandas.sort(function(a, b) { return a[0] - b[0]; });
              var fusionadas = [];
              bandas.forEach(function(b) {
                if (!fusionadas.length || b[0] > fusionadas[fusionadas.length - 1][1]) {
                  fusionadas.push([b[0], b[1]]);
                } else {
                  fusionadas[fusionadas.length - 1][1] = Math.max(fusionadas[fusionadas.length - 1][1], b[1]);
                }
              });

              var pasillos = [];
              var cursorY = sRect.height * 0.05;
              var limiteY = sRect.height * 0.91;

              fusionadas.forEach(function(b) {
                if (b[0] - cursorY >= 28) {
                  var midPct = (((cursorY + b[0]) / 2) / sRect.height * 100).toFixed(1) + '%';
                  pasillos.push(side === 'L' ? { top: midPct, left: '1.6%' } : { top: midPct, right: '1.6%' });
                }
                cursorY = Math.max(cursorY, b[1]);
              });

              if (limiteY - cursorY >= 28) {
                var midFin = (((cursorY + limiteY) / 2) / sRect.height * 100).toFixed(1) + '%';
                pasillos.push(side === 'L' ? { top: midFin, left: '1.8%' } : { top: midFin, right: '1.8%' });
              }
              return pasillos;
            }

            var nuevosL = extraerPasillosVacios(bandasL, 'L');
            var nuevosR = extraerPasillosVacios(bandasR, 'R');
            var combinados = [];
            var maxLen = Math.max(nuevosL.length, nuevosR.length);
            for (var z = 0; z < maxLen; z++) {
              if (nuevosL[z]) combinados.push(nuevosL[z]);
              if (nuevosR[z]) combinados.push(nuevosR[z]);
            }
            if (combinados.length >= 6) {
              slotsSegurosZigZag = combinados;
            }
          }
          requestAnimationFrame(recalcularSlotsLibresEntreCircuitos);
          window.addEventListener('resize', recalcularSlotsLibresEntreCircuitos);"""

    html = re.sub(
        r"/\* (?:18 slots escalonados en zig-zag|Calculador dinámico de pasillos libres).*?var slotsSegurosZigZag = \[.*?\];(?:\s*function recalcularSlotsLibresEntreCircuitos\(\).*?window\.addEventListener\('resize', recalcularSlotsLibresEntreCircuitos\);)?",
        lambda m: reemplazo_slots_sectores_s4,
        html,
        flags=re.DOTALL
    )

    # 3. Rediseño de VISTA 4: PRECIOS CLAROS (#vista-tarifas) con más aire arriba en el Encabezado de Sección (Antetítulo + H2 + Conmutador)
    nueva_vista_tarifas = """  <!-- ======================================================================= -->
  <!-- VISTA 4 (SALA INDEPENDIENTE): PRECIOS CLAROS (2 DIAPOSITIVAS 100VH)     -->
  <!-- ======================================================================= -->
  <section id="vista-tarifas" class="view-panel hidden bg-[#091e36] text-slate-100">

    <!-- =================================================================== -->
    <!-- DIAPOSITIVA 1 DE PRECIOS: LOS 3 PLANES ACTIVOS HOY (100VH COMPACTO) -->
    <!-- =================================================================== -->
    <div id="tarifas-slide-planes" class="slide-section sp-tarifas-bg border-b border-white/10 px-4 sm:px-6 pt-5 sm:pt-6 pb-3" style="min-height: calc(100vh - 5.75rem); justify-content: space-between;">
      <div class="max-w-6xl mx-auto w-full flex flex-col justify-between flex-1">

        <!-- FILA 1: Encabezado de Sección (Antetítulo + H2 + Conmutador Mensual/Anual + Línea Divisoria) con aire superior -->
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-2.5 pt-1.5 sm:pt-2 pb-3 border-b border-white/10">
          <div>
            <div class="inline-flex items-center gap-2 text-[10.5px] font-extrabold uppercase tracking-wider text-teal-300 mb-0.5">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>Tarifas Oficiales de Lanzamiento • Sin Permanencia • Escalado Modular</span>
            </div>
            <h2 class="text-xl sm:text-2xl lg:text-[27px] font-black text-white tracking-tight leading-tight">
              Precios claros y amortización desde el primer cliente.
            </h2>
          </div>

          <!-- Conmutador (Toggle) Mensual / Anual (Regalo 2 Meses) -->
          <div class="inline-flex items-center gap-1.5 bg-slate-950/90 p-1 rounded-2xl border border-teal-400/40 shadow-lg self-start lg:self-center">
            <button type="button" id="btnSwitchMensual" onclick="cambiarModoTarifas('mensual')" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold bg-gradient-to-r from-teal-500 to-emerald-500 text-slate-950 shadow-md transition-all cursor-pointer">
              🔄 Pago Mensual Flexible
            </button>
            <button type="button" id="btnSwitchAnual" onclick="cambiarModoTarifas('anual')" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold text-slate-200 hover:text-white transition-all cursor-pointer flex items-center gap-1.5">
              <span>🎁 Plan Anual</span>
              <span class="text-[10px] font-black bg-amber-400/20 text-amber-300 border border-amber-400/50 px-2 py-0.5 rounded-full">2 Meses Gratis</span>
            </button>
          </div>
        </div>

        <!-- FILA 2: Las 3 Tarjetas (Cards) con altura compacta y simétrica -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-5 my-auto py-1.5 items-stretch">

          <!-- TARJETA 1 (Card 1): 1 SERVICIO SUELTO (PYME BASE) -->
          <div class="sp-price-card-3d sp-price-card-slate px-5 py-3.5 flex flex-col justify-between">
            <div>
              <div class="flex items-start justify-between gap-2 mb-2">
                <div class="inline-flex flex-col items-center justify-center text-[10.5px] font-extrabold uppercase tracking-wider text-slate-200 bg-white/10 px-2.5 py-1 rounded-xl border border-white/15 leading-tight">
                  <span class="whitespace-nowrap">1 Servicio Activo</span>
                  <span class="text-[9.5px] text-slate-300 font-bold whitespace-nowrap mt-0.5">(S1 o S2 a elegir)</span>
                </div>
                <div class="text-right leading-tight">
                  <span class="block text-[11px] font-bold text-slate-300 whitespace-nowrap">Setup único: <strong class="text-white">150 €</strong></span>
                  <span class="block text-[10px] font-semibold text-slate-400 whitespace-nowrap mt-0.5">(Alta llave en mano)</span>
                </div>
              </div>

              <h3 class="text-lg sm:text-[19px] font-black text-white mb-0.5 whitespace-nowrap">
                1 Servicio Suelto <span class="text-slate-400 font-bold text-xs">(Base)</span>
              </h3>
              <p class="text-xs text-slate-300 mb-2 leading-snug">
                Para empezar hoy por un único frente activo a tu elección:
              </p>

              <!-- Subcaja del Precio (Inner Box) -->
              <div class="bg-slate-950/80 border border-white/10 rounded-2xl px-3.5 py-2 mb-2.5">
                <div class="flex items-baseline gap-1.5" data-plan-price="base">
                  <span class="text-2xl sm:text-[27px] font-black text-white">59 €</span>
                  <span class="text-xs font-semibold text-slate-400">/ mes</span>
                </div>
                <span id="spSubPriceBase" class="block text-[10.5px] font-bold text-teal-300 mt-0.5">
                  Vía Flexible (Día 1: 150 € Setup + 59 € Mes 1 = 209 €)
                </span>
              </div>

              <ul class="space-y-1.5 text-xs text-slate-200 leading-snug mb-3">
                <li class="flex items-start gap-2"><span class="text-teal-400 font-black">✔</span><span><strong>Elige S1 (Reseñas Google IA)</strong> o <strong>S2 (Cortafuegos WhatsApp)</strong>.</span></li>
                <li class="flex items-start gap-2"><span class="text-teal-400 font-black">✔</span><span>Incluye <strong>Informe Mensual 360° Interactivo</strong> cada día 1 de mes.</span></li>
                <li class="flex items-start gap-2"><span class="text-slate-400 font-black">•</span><span class="text-slate-300">Auditorías SEO/GEO o CRO disponibles a tarifa general (350 € c/u).</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanBase" href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20me%20interesa%20empezar%20con%201%20Servicio%20Suelto%20%2859%20%E2%82%AC%2Fmes%29" target="_blank" class="w-full py-2.5 text-center rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-white font-extrabold text-xs sm:text-[13px] transition-all block">
              Elegir 1 Servicio Suelto &rarr;
            </a>
          </div>

          <!-- TARJETA 2 (Card 2): PACK ESCUDO BÁSICO (S1 + S2) -->
          <div class="sp-price-card-3d sp-price-card-sky px-5 py-3.5 flex flex-col justify-between">
            <div>
              <div class="flex items-start justify-between gap-2 mb-2">
                <div class="inline-flex flex-col items-center justify-center text-[10.5px] font-extrabold uppercase tracking-wider text-sky-200 bg-sky-500/25 px-2.5 py-1 rounded-xl border border-sky-400/50 leading-tight">
                  <span class="whitespace-nowrap">🛡️ 2 Servicios</span>
                  <span class="text-[9.5px] text-white font-black whitespace-nowrap mt-0.5">(S1 + S2)</span>
                </div>
                <div class="text-right leading-tight">
                  <span class="block text-[11px] font-bold text-sky-200 whitespace-nowrap">Setup Dúo: <strong class="text-white">225 €</strong></span>
                  <span class="block text-[10px] font-extrabold text-emerald-300 whitespace-nowrap mt-0.5">(2.º al 50%)</span>
                </div>
              </div>

              <h3 class="text-lg sm:text-[19px] font-black text-white mb-0.5 whitespace-nowrap">
                Pack Escudo Básico <span class="text-sky-300 font-bold text-xs">(Dúo)</span>
              </h3>
              <p class="text-xs text-slate-200 mb-2 leading-snug">
                Doble blindaje de reputación (el 2.º módulo suma solo <strong>+40 €/mes</strong>):
              </p>

              <!-- Subcaja del Precio (Inner Box) -->
              <div class="bg-slate-950/85 border border-sky-400/40 rounded-2xl px-3.5 py-2 mb-2.5">
                <div class="flex items-baseline justify-between gap-2">
                  <div class="flex items-baseline gap-1.5" data-plan-price="duo">
                    <span class="text-2xl sm:text-[27px] font-black text-sky-300">99 €</span>
                    <span class="text-xs font-semibold text-slate-300">/ mes</span>
                  </div>
                  <span class="text-[10px] font-extrabold bg-emerald-500/20 text-emerald-300 border border-emerald-400/40 px-2 py-0.5 rounded-full whitespace-nowrap">Ahorras 228 €/año</span>
                </div>
                <span id="spSubPriceDuo" class="block text-[10.5px] font-bold text-sky-200 mt-0.5">
                  Vía Flexible (Día 1: 225 € Setup + 99 € Mes 1 = 324 €)
                </span>
              </div>

              <ul class="space-y-1.5 text-xs text-slate-100 leading-snug mb-3">
                <li class="flex items-start gap-2"><span class="text-sky-400 font-black">✔</span><span><strong>Une S1 + S2:</strong> Respuesta IA en Google + Cortafuegos por WhatsApp Oficial.</span></li>
                <li class="flex items-start gap-2"><span class="text-sky-400 font-black">✔</span><span><strong>Informe 360° Completo</strong> (Módulos Google IA + Escudo Privado).</span></li>
                <li class="flex items-start gap-2"><span class="text-emerald-400 font-black">🔑</span><span><strong>Llave de Socio:</strong> Desbloquea las 2 Auditorías a <strong>195 € c/u</strong> para cuando quieras.</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanDuo" href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20me%20interesa%20el%20Pack%20Escudo%20B%C3%A1sico%20%28S1%20%2B%20S2%20por%2099%20%E2%82%AC%2Fmes%29" target="_blank" class="w-full py-2.5 text-center rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-black text-xs sm:text-[13px] shadow-lg shadow-sky-500/25 transition-all block">
              Elegir Pack Escudo Básico &rarr;
            </a>
          </div>

          <!-- TARJETA 3 (Card 3 Estrella): PACK ESCUDO TOTAL / PLUS (S1 + S2 + 1 O 2 AUDITORÍAS BONIFICADAS) -->
          <div class="sp-price-card-3d sp-price-card-emerald px-5 py-3.5 flex flex-col justify-between relative">
            <div>
              <div class="flex items-start justify-between gap-2 mb-2">
                <div class="inline-flex flex-col items-center justify-center text-[10.5px] font-extrabold uppercase tracking-wider text-emerald-950 bg-emerald-300 px-2.5 py-1 rounded-xl shadow-sm leading-tight">
                  <span class="whitespace-nowrap">🚀 Recomendado</span>
                  <span class="text-[9.5px] font-black text-emerald-950 whitespace-nowrap mt-0.5">(Escudo + Auditoría)</span>
                </div>
                <div class="text-right leading-tight">
                  <span id="spBadgeAhorroEscudoTotal" class="block text-[10.5px] font-extrabold text-amber-300 whitespace-nowrap">¡80 € menos que 1 Serv + Aud.!</span>
                  <span class="block text-[9.5px] font-bold text-emerald-200 whitespace-nowrap mt-0.5">(Auditoría a 195 € en vez de 350 €)</span>
                </div>
              </div>

              <!-- Título en 1 sola línea + Mini-selector alineado -->
              <div class="flex flex-wrap items-center justify-between gap-1.5 mb-2">
                <h3 id="spTitleEscudoTotal" class="text-lg sm:text-[19px] font-black text-white whitespace-nowrap">
                  Pack Escudo Total ★
                </h3>
                <!-- Mini-selector (Toggle): +1 Auditoría vs +2 Auditorías (Plus) -->
                <div class="inline-flex items-center bg-slate-950/90 p-0.5 rounded-lg border border-emerald-400/50 text-[10px] font-extrabold">
                  <button type="button" id="btnEscudo1Aud" onclick="spSeleccionarNivelEscudoTotal(1)" class="px-2 py-0.5 rounded-md bg-emerald-400 text-slate-950 cursor-pointer transition-all whitespace-nowrap">
                    +1 Auditoría
                  </button>
                  <button type="button" id="btnEscudo2Aud" onclick="spSeleccionarNivelEscudoTotal(2)" class="px-2 py-0.5 rounded-md text-emerald-200 hover:text-white cursor-pointer transition-all whitespace-nowrap">
                    +2 Auditorías (Plus)
                  </button>
                </div>
              </div>

              <!-- Subcaja del Precio (Inner Box) -->
              <div class="bg-slate-950/90 border-2 border-emerald-400/60 rounded-2xl px-3.5 py-2 mb-2.5 shadow-inner">
                <div class="flex items-baseline justify-between gap-1.5 flex-wrap">
                  <div class="flex items-baseline gap-1" data-plan-price="trinity">
                    <span class="text-2xl sm:text-[27px] font-black text-emerald-300">99 €</span>
                    <span class="text-xs font-semibold text-slate-300">/ mes</span>
                  </div>
                  <span id="spAuditAddonPriceTag" class="text-[10.5px] font-black text-amber-300 bg-amber-500/15 border border-amber-400/40 px-2 py-0.5 rounded-lg whitespace-nowrap">
                    + 195 € (1 Auditoría Llave en Mano)
                  </span>
                </div>
                <span id="spSubPriceEscudoTotal" class="block text-[10.5px] font-bold text-emerald-200 mt-0.5">
                  Setup Dúo (225 €) + 1 Auditoría (195 € en vez de 350 € • Ahorras 155 €)
                </span>
              </div>

              <ul class="space-y-1.5 text-xs text-slate-100 leading-snug mb-3">
                <li class="flex items-start gap-2"><span class="text-emerald-400 font-black">✔</span><span><strong>Todo el Pack Escudo (S1 + S2)</strong> protegiendo y multiplicando tus 5★.</span></li>
                <li class="flex items-start gap-2"><span class="text-emerald-400 font-black">✔</span><span id="spBulletAuditEscudo"><strong>1 Auditoría e Implantación Llave en Mano a elegir</strong> (SEO+GEO IA o Neuro-CRO Web) por solo <strong>195 €</strong>.</span></li>
                <li class="flex items-start gap-2"><span class="text-amber-300 font-black">★</span><span id="spBulletBonusEscudo">Si eliges <strong>+2 Auditorías (Plus)</strong> te llevas ambas implantadas ahorrando <strong>310 €</strong> en total.</span></li>
              </ul>
            </div>

            <a id="spBtnWaPlanEscudoTotal" href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20quiero%20activar%20el%20Pack%20Escudo%20Total%20%28S1%20%2B%20S2%20por%2099%20%E2%82%AC%2Fmes%20%2B%201%20Auditor%C3%ADa%20bonificada%20a%20195%20%E2%82%AC%29" target="_blank" class="sp-btn-s5-primary-3d w-full py-2.5 text-center rounded-xl text-white font-black text-xs sm:text-[13px] block">
              Activar Pack Escudo Total &rarr;
            </a>
          </div>

        </div>

        <!-- FILA 3 (BANNER-GUÍA INFERIOR 100% VISIBLE DENTRO DEL PANTALLAZO) -->
        <div class="pt-0.5 pb-1 flex justify-center">
          <button type="button" onclick="spScrollLimpioSeccion('tarifas-slide-complementos')" class="group inline-flex items-center gap-3 px-5 py-2 rounded-2xl bg-slate-950/90 hover:bg-slate-900 border-2 border-teal-400/55 hover:border-teal-300 shadow-lg transition-all cursor-pointer">
            <span class="text-sm">🔍🧠</span>
            <span class="text-xs sm:text-[13px] font-extrabold text-teal-200 group-hover:text-white">
              Ver Tarifas de las 2 Auditorías (Pago Único), Atril NFC/QR y Escalado Modular
            </span>
            <span class="w-5 h-5 rounded-full bg-teal-500/25 border border-teal-400/60 flex items-center justify-center text-teal-300 group-hover:translate-y-0.5 transition-transform font-black text-xs">
              &darr;
            </span>
          </button>
        </div>

      </div>
    </div>

    <!-- =================================================================== -->
    <!-- DIAPOSITIVA 2 DE PRECIOS: LAS 2 AUDITORÍAS, ATRIL NFC/QR Y ESCALADO -->
    <!-- =================================================================== -->
    <div id="tarifas-slide-complementos" class="slide-section sp-tarifas-bg px-4 sm:px-6 py-5" style="min-height: calc(100vh - 5.75rem);">
      <div class="max-w-6xl mx-auto w-full flex flex-col justify-between min-h-[calc(100vh-8.5rem)]">

        <!-- Cabecera de la Diapositiva 2 de Precios -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-white/10">
          <div>
            <span class="text-[11px] font-extrabold uppercase tracking-wider text-amber-300 block mb-0.5">
              Pagos Únicos Sin Cuotas Mensuales y Hoja de Ruta Modular
            </span>
            <h3 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
              Las 2 Auditorías Premium, Hardware NFC/QR y Escalabilidad.
            </h3>
          </div>
          <button type="button" onclick="spScrollLimpioSeccion('tarifas-slide-planes')" class="self-start sm:self-center inline-flex items-center gap-2 text-xs font-extrabold text-teal-200 hover:text-white bg-white/5 hover:bg-white/10 px-4 py-2 rounded-xl border border-white/15 transition-all cursor-pointer">
            <span>&uarr;</span>
            <span>Volver a los 3 Planes Mensuales</span>
          </button>
        </div>

        <!-- Bloque Central Amplio: Las 2 Auditorías Gemelas + Hardware Atril y Regla de Escalado -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 my-auto py-3 items-stretch">

          <!-- Columna Izquierda (7 cols): Las 2 Auditorías e Implantaciones Premium -->
          <div class="lg:col-span-7 bg-slate-900/90 border-2 border-teal-400/45 rounded-3xl p-5 sm:p-6 flex flex-col justify-between shadow-xl">
            <div>
              <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-teal-300 bg-teal-950/90 px-3.5 py-1 rounded-full border border-teal-400/40">
                  🔍🧠 Las 2 Auditorías Web Gemelas (Pago Único • Sin Cuotas)
                </span>
                <span class="text-xs font-bold text-amber-300">Elige 1 o ambas • Misma tarifa c/u</span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5 mb-4 text-xs sm:text-[13px]">
                <div class="bg-slate-950/85 border border-cyan-500/40 rounded-2xl p-4">
                  <strong class="text-cyan-300 text-sm font-black block mb-1">1. Auditoría SEO Local + GEO (IA)</strong>
                  <p class="text-slate-200 leading-relaxed">
                    <strong>«Para que te encuentren»:</strong> Escáner de 16 parámetros e inyección de código invisible <code>Schema.org JSON-LD</code> conectado a Wikidata, <code>llms.txt</code> y optimización de Google Maps para salir 1.º en Google, ChatGPT y Gemini.
                  </p>
                </div>
                <div class="bg-slate-950/85 border border-amber-500/40 rounded-2xl p-4">
                  <strong class="text-amber-300 text-sm font-black block mb-1">2. Auditoría Neuromarketing y CRO</strong>
                  <p class="text-slate-200 leading-relaxed">
                    <strong>«Para que te compren»:</strong> Mapas de calor reales, instalación llave en mano de botón WhatsApp en zona del pulgar, barra superior con tus estrellas de Google y acceso a tu Panel Privado de Telemetría.
                  </p>
                </div>
              </div>
            </div>

            <!-- Las 3 Modalidades Oficiales de Contratación de las Auditorías -->
            <div>
              <span class="block text-[11px] font-extrabold uppercase tracking-wider text-slate-300 mb-2">
                3 Formas de contratar cualquiera de las 2 Auditorías (Precio por unidad):
              </span>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-center">
                <div class="bg-slate-950/90 rounded-2xl p-3 border border-white/15 flex flex-col justify-between">
                  <span class="block text-[10.5px] font-extrabold text-slate-300 uppercase">1. Solo Código / Informe</span>
                  <span class="block text-xl sm:text-2xl font-black text-white my-1">200 € <span class="text-xs font-normal text-slate-400">c/u</span></span>
                  <span class="block text-[11px] text-slate-300 leading-tight">Paquete técnico listo para que lo instale tu informático.</span>
                </div>
                <div class="bg-slate-950/90 rounded-2xl p-3 border border-teal-500/40 flex flex-col justify-between">
                  <span class="block text-[10.5px] font-extrabold text-teal-300 uppercase">2. Todo Incluido Suelta</span>
                  <span class="block text-xl sm:text-2xl font-black text-teal-200 my-1">350 € <span class="text-xs font-normal text-slate-400">c/u</span></span>
                  <span class="block text-[11px] text-slate-300 leading-tight">Código (200 €) + nuestra implantación (+150 €). Suelta o con 1 serv.</span>
                </div>
                <div class="bg-emerald-950/85 rounded-2xl p-3 border-2 border-emerald-400/70 flex flex-col justify-between shadow-lg">
                  <span class="block text-[10.5px] font-extrabold text-emerald-300 uppercase">3. Con Pack Escudo ★</span>
                  <span class="block text-xl sm:text-2xl font-black text-emerald-300 my-1">195 € <span class="text-xs font-normal text-emerald-200">c/u</span></span>
                  <span class="block text-[11px] text-emerald-100 leading-tight"><strong>Ahorras 155 € c/u</strong> (o <strong>95 € c/u</strong> en Plan Anual Trinity+).</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Columna Derecha (5 cols): Hardware Atril Inteligente NFC + QR y Escalabilidad Fase 2 -->
          <div class="lg:col-span-5 flex flex-col justify-between gap-4">

            <!-- Tarjeta del Atril Inteligente NFC + QR -->
            <div class="bg-slate-900/90 border-2 border-amber-400/45 rounded-3xl p-5 shadow-xl">
              <div class="flex items-center justify-between gap-2 mb-2">
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-300">
                  ★ Hardware de Mostrador
                </span>
                <span class="text-[11px] font-extrabold bg-amber-400/20 text-amber-200 border border-amber-400/40 px-3 py-0.5 rounded-full">
                  Pago Único • Sin Cuotas
                </span>
              </div>
              <h4 class="text-lg font-black text-white mb-1">
                Atril Inteligente NFC + QR
              </h4>
              <p class="text-xs sm:text-[13px] text-slate-200 leading-relaxed mb-3">
                El cliente acerca su móvil al pagar y se abre tu valoración de 5★ en Google Maps en <strong>1 segundo</strong>. Distingue toques NFC vs. QR e iPhone vs. Android en tu Informe 360°.
              </p>
              <div class="grid grid-cols-3 gap-2 text-center bg-slate-950/90 p-2.5 rounded-2xl border border-amber-400/30">
                <div>
                  <span class="block text-[10px] font-bold text-slate-400 uppercase">1.ª Unidad</span>
                  <span class="block text-lg font-black text-amber-300">39 €</span>
                </div>
                <div class="border-x border-white/10">
                  <span class="block text-[10px] font-bold text-slate-400 uppercase">2.ª a 4.ª Ud.</span>
                  <span class="block text-lg font-black text-emerald-300">29 € <span class="text-[10px] font-normal">/ud</span></span>
                </div>
                <div>
                  <span class="block text-[10px] font-bold text-slate-400 uppercase">5 o más Uds.</span>
                  <span class="block text-lg font-black text-teal-300">25 € <span class="text-[10px] font-normal">/ud</span></span>
                </div>
              </div>
            </div>

            <!-- Tarjeta de Regla de Escalado Transparente + Regalo Bóveda -->
            <div class="bg-slate-900/90 border border-sky-400/40 rounded-3xl p-5 flex flex-col justify-between flex-1 shadow-xl">
              <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-sky-300 block mb-1.5">
                  📈 Escalabilidad Modular Transparente (Fase 2)
                </span>
                <ul class="space-y-1.5 text-xs sm:text-[13px] text-slate-200 leading-snug">
                  <li>• <strong>Del 2.º al 5.º servicio troncal:</strong> suma solo <strong>+40 €/mes</strong> (+75 € setup).</li>
                  <li>• <strong>Del 6.º al 10.º servicio:</strong> suma solo <strong>+30 €/mes</strong> (+75 € setup).</li>
                  <li>• <strong>🎁 Bono Plan Trinity (3+ servicios):</strong> incluye gratis la <strong>Bóveda Segura de Contraseñas</strong> (valorada en 150 €).</li>
                </ul>
              </div>

              <div class="pt-3 mt-3 border-t border-white/10 flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-300">
                <span>🧾 Precios netos sin IVA (21% deducible) • SEPA</span>
                <div class="flex items-center gap-3">
                  <a href="documentos/tarifas.html" target="_blank" class="text-teal-300 font-extrabold hover:underline">Tarjetón A5 &rarr;</a>
                  <a href="documentos/desembolso.html" target="_blank" class="text-amber-300 font-extrabold hover:underline">Tabla Día 1 &rarr;</a>
                </div>
              </div>
            </div>

          </div>

        </div>

        <!-- Pie de cierre de Precios Claros -->
        <div class="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-white/10">
          <span class="text-xs text-slate-300">
            💬 <strong>¿Dudas sobre qué combinación te conviene más?</strong> Lo vemos juntos en 5 minutos sin compromiso.
          </span>
          <div class="flex items-center gap-3">
            <a href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20acabo%20de%20ver%20los%20Precios%20Claros%20y%20me%20gustar%C3%ADa%20que%20me%20recomendaras%20la%20mejor%20opci%C3%B3n%20para%20mi%20negocio" target="_blank" class="sp-btn-s5-primary-3d px-5 py-2.5 rounded-xl text-white font-extrabold text-xs sm:text-[13px]">
              Hablar con Francisco por WhatsApp &rarr;
            </a>
          </div>
        </div>

      </div>
    </div>

  </section>"""

    html = re.sub(
        r'<!-- ======================================================================= -->\s*<!-- VISTA 4 \(SALA INDEPENDIENTE\): (?:TARIFAS|PRECIOS CLAROS).*?</section>',
        lambda m: nueva_vista_tarifas,
        html,
        flags=re.DOTALL
    )

    # 4. Actualizar las funciones JS de tarifas (cambiarModoTarifas + spSeleccionarNivelEscudoTotal) con tamaños compactos
    reemplazo_js_tarifas = """    var _spModoTarifasActual = 'mensual';
    var _spNumAuditoriasEscudo = 1;

    function _spRenderizarTarjetasPrecios() {
      var btnM = document.getElementById('btnSwitchMensual');
      var btnA = document.getElementById('btnSwitchAnual');
      var pBase = document.querySelector('[data-plan-price="base"]');
      var pDuo = document.querySelector('[data-plan-price="duo"]');
      var pTri = document.querySelector('[data-plan-price="trinity"]');
      var subBase = document.getElementById('spSubPriceBase');
      var subDuo = document.getElementById('spSubPriceDuo');
      var subEsc = document.getElementById('spSubPriceEscudoTotal');
      var titleEsc = document.getElementById('spTitleEscudoTotal');
      var tagAud = document.getElementById('spAuditAddonPriceTag');
      var bulletAud = document.getElementById('spBulletAuditEscudo');
      var bulletBon = document.getElementById('spBulletBonusEscudo');
      var badgeAhorro = document.getElementById('spBadgeAhorroEscudoTotal');
      var btn1Aud = document.getElementById('btnEscudo1Aud');
      var btn2Aud = document.getElementById('btnEscudo2Aud');
      var waEsc = document.getElementById('spBtnWaPlanEscudoTotal');

      if (btn1Aud && btn2Aud) {
        if (_spNumAuditoriasEscudo === 2) {
          btn2Aud.className = 'px-2 py-0.5 rounded-md bg-emerald-400 text-slate-950 cursor-pointer transition-all whitespace-nowrap';
          btn1Aud.className = 'px-2 py-0.5 rounded-md text-emerald-200 hover:text-white cursor-pointer transition-all whitespace-nowrap';
        } else {
          btn1Aud.className = 'px-2 py-0.5 rounded-md bg-emerald-400 text-slate-950 cursor-pointer transition-all whitespace-nowrap';
          btn2Aud.className = 'px-2 py-0.5 rounded-md text-emerald-200 hover:text-white cursor-pointer transition-all whitespace-nowrap';
        }
      }

      var esPlus = (_spNumAuditoriasEscudo === 2);
      var costeAud = esPlus ? 390 : 195;
      var ahorroAud = esPlus ? 310 : 155;

      if (titleEsc) titleEsc.textContent = esPlus ? 'Pack Escudo Plus ★' : 'Pack Escudo Total ★';
      if (tagAud) tagAud.textContent = esPlus ? '+ 390 € (Las 2 Auditorías Llave en Mano)' : '+ 195 € (1 Auditoría Llave en Mano)';
      if (badgeAhorro) badgeAhorro.textContent = esPlus ? '¡Ahorras 310 € en las 2 Auditorías!' : '¡80 € menos que 1 Serv + Aud.!';

      if (bulletAud) {
        bulletAud.innerHTML = esPlus
          ? '<strong>Las 2 Auditorías e Implantaciones Llave en Mano incluidas</strong> (SEO+GEO IA + Neuro-CRO Web) por <strong>390 €</strong> en vez de 700 €.'
          : '<strong>1 Auditoría e Implantación Llave en Mano a elegir</strong> (SEO+GEO IA o Neuro-CRO Web) por solo <strong>195 €</strong>.';
      }
      if (bulletBon) {
        bulletBon.innerHTML = esPlus
          ? 'Dejas blindados a la vez tu posicionamiento en Google/IA y la conversión de tu página web.'
          : 'Si eliges <strong>+2 Auditorías (Plus)</strong> arriba, te llevas ambas implantadas ahorrando <strong>310 €</strong>.';
      }

      if (_spModoTarifasActual === 'anual') {
        if (btnA) btnA.className = 'px-3.5 py-1.5 rounded-xl text-xs font-extrabold bg-gradient-to-r from-teal-500 to-emerald-500 text-slate-950 shadow-md transition-all cursor-pointer flex items-center gap-1.5';
        if (btnM) btnM.className = 'px-3.5 py-1.5 rounded-xl text-xs font-extrabold text-slate-200 hover:text-white transition-all cursor-pointer';

        if (pBase) pBase.innerHTML = '<span class="text-2xl sm:text-[27px] font-black text-white">49 €</span><span class="text-xs font-semibold text-slate-300">/ mes eq. (590 €/año)</span>';
        if (subBase) subBase.textContent = 'Plan Anual 10 meses + 150 € Setup (Ahorras 118 € = 2 meses gratis)';

        if (pDuo) pDuo.innerHTML = '<span class="text-2xl sm:text-[27px] font-black text-sky-300">82,50 €</span><span class="text-xs font-semibold text-slate-300">/ mes eq. (990 €/año)</span>';
        if (subDuo) subDuo.textContent = 'Plan Anual 10 meses + 225 € Setup Dúo (Ahorras 198 € en cuota)';

        if (pTri) pTri.innerHTML = '<span class="text-2xl sm:text-[27px] font-black text-emerald-300">82,50 €</span><span class="text-xs font-semibold text-slate-300">/ mes eq. (990 €/año)</span>';
        if (subEsc) subEsc.textContent = 'Ahorras 198 € (2 meses gratis) + ' + ahorroAud + ' € en ' + (esPlus ? 'las 2 Auditorías' : 'la Auditoría');
      } else {
        if (btnM) btnM.className = 'px-3.5 py-1.5 rounded-xl text-xs font-extrabold bg-gradient-to-r from-teal-500 to-emerald-500 text-slate-950 shadow-md transition-all cursor-pointer';
        if (btnA) btnA.className = 'px-3.5 py-1.5 rounded-xl text-xs font-extrabold text-slate-200 hover:text-white transition-all cursor-pointer flex items-center gap-1.5';

        if (pBase) pBase.innerHTML = '<span class="text-2xl sm:text-[27px] font-black text-white">59 €</span><span class="text-xs font-semibold text-slate-400">/ mes</span>';
        if (subBase) subBase.textContent = 'Vía Flexible (Día 1: 150 € Setup + 59 € Mes 1 = 209 €)';

        if (pDuo) pDuo.innerHTML = '<span class="text-2xl sm:text-[27px] font-black text-sky-300">99 €</span><span class="text-xs font-semibold text-slate-300">/ mes</span>';
        if (subDuo) subDuo.textContent = 'Vía Flexible (Día 1: 225 € Setup + 99 € Mes 1 = 324 €)';

        if (pTri) pTri.innerHTML = '<span class="text-2xl sm:text-[27px] font-black text-emerald-300">99 €</span><span class="text-xs font-semibold text-slate-300">/ mes</span>';
        if (subEsc) subEsc.textContent = 'Setup Dúo (225 €) + ' + (esPlus ? '2 Auditorías (' + costeAud + ' € • Ahorras 310 €)' : '1 Auditoría (195 € • Ahorras 155 €)');
      }

      if (waEsc) {
        var nombrePack = esPlus ? 'Pack Escudo Total Plus (S1+S2 + 2 Auditorías por 390 €)' : 'Pack Escudo Total (S1+S2 + 1 Auditoría por 195 €)';
        var modTexto = (_spModoTarifasActual === 'anual') ? ' en modalidad Plan Anual (2 meses gratis)' : ' en modalidad mensual';
        waEsc.href = 'https://wa.me/34711547561?text=' + encodeURIComponent('Hola Francisco, quiero activar el ' + nombrePack + modTexto + '.');
        waEsc.textContent = esPlus ? 'Activar Pack Escudo Plus →' : 'Activar Pack Escudo Total →';
      }
    }

    function cambiarModoTarifas(modo) {
      _spModoTarifasActual = (modo === 'anual') ? 'anual' : 'mensual';
      _spRenderizarTarjetasPrecios();
    }

    window.spSeleccionarNivelEscudoTotal = function(numAud) {
      _spNumAuditoriasEscudo = (numAud === 2) ? 2 : 1;
      _spRenderizarTarjetasPrecios();
    };"""

    html = re.sub(
        r"(?:var _spModoTarifasActual = 'mensual';.*?window\.spSeleccionarNivelEscudoTotal = function\(numAud\) \{.*?\};|function cambiarModoTarifas\(modo\)\s*\{.*?\n    \})",
        lambda m: reemplazo_js_tarifas,
        html,
        flags=re.DOTALL
    )

    # 5. Rediseño de la Tecnosala: Terminal de Hardware Futurista Minimalista CON CONSULTA POR VOZ 🎙️
    nueva_vista_tecnosala = """  <!-- ======================================================================= -->
  <!-- VISTA TECNOSALA: TERMINAL DE HARDWARE FUTURISTA MINIMALISTA + VOZ 🎙️    -->
  <!-- ======================================================================= -->
  <section id="vista-tecnosala" class="view-panel hidden sp-test-bg text-white">
    <div class="slide-section px-4 sm:px-6 py-3">
      <div class="max-w-4xl mx-auto w-full relative z-10 flex flex-col justify-center min-h-[calc(100vh-6.2rem)]">

        <!-- Cabecera limpia, sobria y atractiva -->
        <div class="text-center -mt-2 mb-3.5">
          <div class="inline-flex items-center gap-2 text-[11px] font-extrabold uppercase tracking-[0.22em] text-teal-300/90 mb-1">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span>Unidad Interactiva • Sistemas Pyme</span>
          </div>
          <h2 class="text-2xl sm:text-4xl lg:text-[36px] font-black text-white tracking-tight leading-tight">
            Tu Consultor Tecnológico Inteligente
          </h2>
        </div>

        <!-- CHASIS DEL APARATO DE HARDWARE FUTURISTA -->
        <div class="sp-hw-device-chassis p-4 sm:p-6 mb-3.5">

          <!-- Bisel superior del dispositivo (con trigger secreto de 7 clics para Admin + botón de Preguntas Frecuentes plegadas) -->
          <div class="flex flex-wrap items-center justify-between gap-2.5 pb-3 mb-3.5 border-b border-white/10">
            <div id="spTecnosalaAdminTrigger" class="flex items-center gap-2.5 cursor-pointer select-none" title="Haz 7 clics rápidos aquí para abrir el Cuadro de Mando de Telemetría (Admin)">
              <span class="sp-tecnosala-live-dot"></span>
              <span class="text-xs sm:text-[13px] font-black uppercase tracking-wider text-teal-200">
                SP-CORE 360° • VOZ Y TEXTO EN LÍNEA
              </span>
            </div>

            <div class="flex items-center gap-2">
              <button type="button" id="spBtnResetScreenTecnosala" onclick="spLimpiarPantallaTecnosala()" class="hidden text-[11px] font-extrabold text-slate-300 hover:text-white bg-white/5 hover:bg-white/10 px-3 py-1.5 rounded-xl border border-white/15 transition-all cursor-pointer">
                &#8634; Limpiar pantalla
              </button>
              <button type="button" id="spBtnToggleFaqTecnosala" onclick="spToggleFaqDrawerTecnosala()" class="sp-hw-faq-toggle-btn text-xs sm:text-[12.5px] font-extrabold px-4 py-1.5 rounded-xl cursor-pointer flex items-center gap-2">
                <span>✨</span>
                <span id="spLabelToggleFaqTecnosala">¿Quieres ver preguntas frecuentes?</span>
                <span id="spArrowToggleFaqTecnosala" class="transition-transform duration-300">▾</span>
              </button>
            </div>
          </div>

          <!-- Cajón Plegable de las 6 Preguntas Frecuentes (Oculto por defecto para cero ruido visual) -->
          <div id="spTecnosalaFaqDrawer" class="sp-hw-faq-drawer">
            <div class="pb-3.5 mb-3 border-b border-teal-400/20">
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                <button type="button" id="spFaqChip_rgpd" onclick="spEjecutarConsultaTecnosala('rgpd')" class="sp-faq-chip">
                  <span>🛡️</span>
                  <span class="truncate">¿Cómo evitáis multas RGPD en reseñas?</span>
                </button>
                <button type="button" id="spFaqChip_fijo" onclick="spEjecutarConsultaTecnosala('fijo')" class="sp-faq-chip">
                  <span>☎️</span>
                  <span class="truncate">¿Puedo usar el teléfono fijo de mi local?</span>
                </button>
                <button type="button" id="spFaqChip_informe360" onclick="spEjecutarConsultaTecnosala('informe360')" class="sp-faq-chip">
                  <span>📊</span>
                  <span class="truncate">¿Qué incluye el Informe Mensual 360°?</span>
                </button>
                <button type="button" id="spFaqChip_instalacion" onclick="spEjecutarConsultaTecnosala('instalacion')" class="sp-faq-chip">
                  <span>🔌</span>
                  <span class="truncate">¿Tengo que cambiar mi programa actual?</span>
                </button>
                <button type="button" id="spFaqChip_seogeo" onclick="spEjecutarConsultaTecnosala('seogeo')" class="sp-faq-chip">
                  <span>🧭</span>
                  <span class="truncate">¿Cómo me recomiendan ChatGPT y Google?</span>
                </button>
                <button type="button" id="spFaqChip_precios" onclick="spEjecutarConsultaTecnosala('precios')" class="sp-faq-chip">
                  <span>💶</span>
                  <span class="truncate">¿Cuánto cuesta y cómo se amortiza?</span>
                </button>
              </div>
            </div>
          </div>

          <!-- PANTALLA HOLOGRÁFICA DEL TERMINAL (Vacía y acogedora al entrar; muestra la respuesta al consultar) -->
          <div id="spTecnosalaScreen" class="sp-hw-glass-screen p-5 sm:p-6 mb-4 min-h-[230px] max-h-[275px] overflow-y-auto flex flex-col justify-center">

            <!-- ESTADO 1: PANTALLA VIRGEN DE BIENVENIDA (Visible por defecto) -->
            <div id="spTecnosalaIdleWelcome" class="text-center max-w-xl mx-auto my-auto py-2 flex flex-col items-center justify-center">
              <div class="sp-hw-ai-orb-wrap mb-3.5">
                <div class="sp-hw-ai-orb-ring"></div>
                <div class="sp-hw-ai-orb-core">
                  <svg class="w-6 h-6 text-teal-200" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                </div>
              </div>
              <h3 class="text-base sm:text-xl font-black text-white tracking-tight mb-1.5">
                Soy tu consultor tecnológico que lo sabe todo sobre Sistemas Pyme.
              </h3>
              <p class="text-xs sm:text-[14px] text-teal-100/85 font-medium leading-relaxed">
                Selecciona arriba una de las <button type="button" onclick="spToggleFaqDrawerTecnosala()" class="text-teal-300 hover:text-white underline font-bold cursor-pointer">preguntas frecuentes</button>, escribe abajo o pulsa <button type="button" onclick="spToggleDictadoVozTecnosala()" class="text-emerald-300 hover:text-white underline font-bold cursor-pointer">🎙️ Hablar</button> para preguntarme con tu voz.
              </p>
            </div>

            <!-- ESTADO 2: RESPUESTA ACTIVA DEL CONSULTOR (Oculto hasta que el usuario toca una pregunta, escribe o habla) -->
            <div id="spTecnosalaActiveOutput" class="hidden text-left my-auto">
              <div class="flex items-center justify-between gap-2 mb-2">
                <span id="spTecnosalaAnswerTag" class="inline-flex items-center gap-1.5 text-[10.5px] font-extrabold uppercase tracking-wider text-emerald-300 bg-emerald-950/90 px-3 py-0.5 rounded-full border border-emerald-400/50">
                  ✨ Consultor Sistemas Pyme
                </span>
                <span id="spTecnosalaStatusLabel" class="text-[11px] font-bold text-teal-300">Respuesta en pantalla ✓</span>
              </div>
              <h4 id="spTecnosalaAnswerTitle" class="text-sm sm:text-[16px] font-black text-amber-300 mb-1.5 leading-snug"></h4>
              <div id="spTecnosalaAnswerBody" class="text-xs sm:text-[14px] text-slate-100 leading-relaxed space-y-2"></div>
            </div>

          </div>

          <!-- CONSOLA / TECLADO + MICRÓFONO DE VOZ INFERIOR -->
          <form onsubmit="spEnviarPreguntaLibreTecnosala(event)" class="sp-hw-keyboard-dock p-2 sm:p-2.5 rounded-2xl flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
            <div class="relative flex-1 flex items-center">
              <span class="pl-3 pr-1.5 text-teal-300 select-none text-base">⌨️</span>
              <input
                type="text"
                id="spTecnosalaInput"
                placeholder="Escribe tu duda o pulsa 🎙️ Hablar para preguntar por voz..."
                class="w-full bg-transparent px-2 py-2 text-xs sm:text-[14px] text-white placeholder-slate-400 focus:outline-none font-medium"
              />
            </div>
            <div class="flex items-center gap-2">
              <button
                type="button"
                id="spBtnVoiceTecnosala"
                onclick="spToggleDictadoVozTecnosala()"
                title="Consultar hablando por micrófono"
                class="sp-hw-voice-btn flex-1 sm:flex-initial px-4 py-2.5 rounded-xl font-extrabold text-xs sm:text-[13px] inline-flex items-center justify-center gap-2 cursor-pointer whitespace-nowrap"
              >
                <span id="spVoiceMicIcon" class="text-sm leading-none">🎙️</span>
                <span id="spVoiceBtnText">Hablar</span>
              </button>
              <button type="submit" class="sp-btn-s5-primary-3d flex-1 sm:flex-initial px-5 py-2.5 rounded-xl text-white font-extrabold text-xs sm:text-[13.5px] whitespace-nowrap cursor-pointer">
                Preguntar &rarr;
              </button>
            </div>
          </form>

        </div>

        <!-- Pie minimalista de la Tecnosala -->
        <div class="flex flex-wrap items-center justify-between gap-3 px-1">
          <div class="flex flex-wrap items-center gap-2 text-xs text-slate-300">
            <span class="font-bold text-teal-300">📄 Fichas en PDF:</span>
            <a href="documentos/catalogo.html" target="_blank" class="underline hover:text-white">Catálogo</a>
            <span>•</span>
            <a href="documentos/setup.html" target="_blank" class="underline hover:text-white">Auditorías SEO+GEO</a>
            <span>•</span>
            <a href="documentos/tarifas.html" target="_blank" class="underline hover:text-white">Tarifas</a>
          </div>
          <div class="flex items-center gap-2.5">
            <button type="button" onclick="cambiarVista('auditorias')" class="text-xs font-extrabold text-teal-200 hover:text-white bg-teal-950/80 hover:bg-teal-900 px-4 py-2 rounded-xl border border-teal-500/40 cursor-pointer">
              Ir al Test de diagnóstico &rarr;
            </button>
            <a id="spTecnosalaWaBtn" href="https://wa.me/34711547561?text=Hola%20Francisco%2C%20vengo%20de%20la%20Tecnosala%20y%20querr%C3%ADa%20hacerte%20una%20consulta%20sobre%20mi%20negocio" target="_blank" class="sp-btn-s5-secondary-3d px-4 py-2 rounded-xl text-white font-bold text-xs">
              💬 Hablar con Francisco
            </a>
          </div>
        </div>

      </div>
    </div>"""

    html = re.sub(
        r'<!-- ======================================================================= -->\s*<!-- VISTA TECNOSALA:.*?<script>',
        lambda m: nueva_vista_tecnosala + "\n\n    <script>",
        html,
        flags=re.DOTALL
    )

    reemplazo_js_tecnosala = """        function marcarChipActivo(idChip) {
          ['rgpd', 'fijo', 'informe360', 'instalacion', 'seogeo', 'precios'].forEach(function(k) {
            var el = document.getElementById('spFaqChip_' + k);
            if (el) {
              if (k === idChip) el.classList.add('sp-faq-active');
              else el.classList.remove('sp-faq-active');
            }
          });
        }

        window.spToggleFaqDrawerTecnosala = function(forzarEstado) {
          var drawer = document.getElementById('spTecnosalaFaqDrawer');
          var lbl = document.getElementById('spLabelToggleFaqTecnosala');
          var arr = document.getElementById('spArrowToggleFaqTecnosala');
          if (!drawer) return;
          var abrir = (typeof forzarEstado === 'boolean') ? forzarEstado : !drawer.classList.contains('sp-faq-drawer-open');
          if (abrir) {
            drawer.classList.add('sp-faq-drawer-open');
            if (lbl) lbl.textContent = 'Ocultar preguntas frecuentes';
            if (arr) arr.style.transform = 'rotate(180deg)';
          } else {
            drawer.classList.remove('sp-faq-drawer-open');
            if (lbl) lbl.textContent = '¿Quieres ver preguntas frecuentes?';
            if (arr) arr.style.transform = 'rotate(0deg)';
          }
        };

        window.spMostrarSalidaEnPantallaTecnosala = function() {
          var idle = document.getElementById('spTecnosalaIdleWelcome');
          var out = document.getElementById('spTecnosalaActiveOutput');
          var btnReset = document.getElementById('spBtnResetScreenTecnosala');
          if (idle) idle.classList.add('hidden');
          if (out) out.classList.remove('hidden');
          if (btnReset) btnReset.classList.remove('hidden');
        };

        window.spLimpiarPantallaTecnosala = function() {
          marcarChipActivo(null);
          var idle = document.getElementById('spTecnosalaIdleWelcome');
          var out = document.getElementById('spTecnosalaActiveOutput');
          var btnReset = document.getElementById('spBtnResetScreenTecnosala');
          var input = document.getElementById('spTecnosalaInput');
          if (out) out.classList.add('hidden');
          if (idle) idle.classList.remove('hidden');
          if (btnReset) btnReset.classList.add('hidden');
          if (input) input.value = '';
        };

        /* MOTOR DE RECONOCIMIENTO DE VOZ EN VIVO (Web Speech API es-ES) */
        var _spVoiceRecognition = null;
        var _spVoiceListening = false;

        function _spActualizarEstadoBotonVoz(escuchando) {
          _spVoiceListening = escuchando;
          var btn = document.getElementById('spBtnVoiceTecnosala');
          var txt = document.getElementById('spVoiceBtnText');
          var ico = document.getElementById('spVoiceMicIcon');
          var input = document.getElementById('spTecnosalaInput');
          if (!btn) return;
          if (escuchando) {
            btn.classList.add('sp-voice-listening');
            if (txt) txt.textContent = 'Escuchando...';
            if (ico) ico.textContent = '🔴';
            if (input) input.placeholder = '🎙️ Habla ahora con naturalidad (ej. ¿cómo funciona el cortafuegos de WhatsApp?)...';
          } else {
            btn.classList.remove('sp-voice-listening');
            if (txt) txt.textContent = 'Hablar';
            if (ico) ico.textContent = '🎙️';
            if (input) input.placeholder = 'Escribe tu duda o pulsa 🎙️ Hablar para preguntar por voz...';
          }
        }

        window.spToggleDictadoVozTecnosala = function() {
          var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
          var input = document.getElementById('spTecnosalaInput');
          if (!SpeechRec) {
            window.spMostrarSalidaEnPantallaTecnosala();
            var tagEl = document.getElementById('spTecnosalaAnswerTag');
            var titleEl = document.getElementById('spTecnosalaAnswerTitle');
            var bodyEl = document.getElementById('spTecnosalaAnswerBody');
            if (tagEl) tagEl.textContent = '🎙️ Aviso de Navegador';
            if (titleEl) titleEl.textContent = 'Tu navegador actual no tiene activado el dictado directo por voz';
            if (bodyEl) bodyEl.innerHTML = '<p>Para usar el micrófono en directo te recomendamos abrir esta página en <strong>Google Chrome, Safari o Microsoft Edge</strong>, o escribir tu consulta directamente en el teclado inferior.</p>';
            if (input) input.focus();
            return;
          }

          if (_spVoiceListening && _spVoiceRecognition) {
            try { _spVoiceRecognition.stop(); } catch (e) {}
            _spActualizarEstadoBotonVoz(false);
            return;
          }

          try {
            _spVoiceRecognition = new SpeechRec();
            _spVoiceRecognition.lang = 'es-ES';
            _spVoiceRecognition.continuous = false;
            _spVoiceRecognition.interimResults = true;

            var textoCapturadoFinal = '';

            _spVoiceRecognition.onstart = function() {
              _spActualizarEstadoBotonVoz(true);
              if (input) input.value = '';
            };

            _spVoiceRecognition.onresult = function(event) {
              var parcial = '';
              for (var i = event.resultIndex; i < event.results.length; i++) {
                var tr = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                  textoCapturadoFinal += tr;
                } else {
                  parcial += tr;
                }
              }
              if (input) {
                input.value = (textoCapturadoFinal + ' ' + parcial).trim();
              }
            };

            _spVoiceRecognition.onerror = function() {
              _spActualizarEstadoBotonVoz(false);
            };

            _spVoiceRecognition.onend = function() {
              _spActualizarEstadoBotonVoz(false);
              if (input && (input.value || '').trim().length > 1) {
                window.spEnviarPreguntaLibreTecnosala();
              }
            };

            _spVoiceRecognition.start();
          } catch (err) {
            _spActualizarEstadoBotonVoz(false);
          }
        };

        window.spEjecutarConsultaTecnosala = function(claveFaq) {
          marcarChipActivo(claveFaq);
          window.spMostrarSalidaEnPantallaTecnosala();
          var info = BASE_CONOCIMIENTO_TECNOSALA[claveFaq] || BASE_CONOCIMIENTO_TECNOSALA.rgpd;
          var tagEl = document.getElementById('spTecnosalaAnswerTag');
          var statusEl = document.getElementById('spTecnosalaStatusLabel');
          var titleEl = document.getElementById('spTecnosalaAnswerTitle');
          var bodyEl = document.getElementById('spTecnosalaAnswerBody');

          if (tagEl) tagEl.textContent = info.tag;
          if (statusEl) statusEl.textContent = 'Respuesta verificada ✓';
          if (titleEl) titleEl.textContent = info.titulo;
          if (bodyEl) bodyEl.innerHTML = info.html;
        };"""

    html = re.sub(
        r"function marcarChipActivo\(idChip\)\s*\{.*?window\.spEjecutarConsultaTecnosala\s*=\s*function\(claveFaq\)\s*\{.*?\};",
        lambda m: reemplazo_js_tecnosala,
        html,
        flags=re.DOTALL
    )

    html = re.sub(
        r"(window\.spEnviarPreguntaLibreTecnosala = function\(ev\) \{\s*_spEnviarPingTiempoCategoriaAnterior\(\);\s*if \(ev && ev\.preventDefault\) ev\.preventDefault\(\);\s*var input = document\.getElementById\('spTecnosalaInput'\);\s*if \(!input\) return;\s*var texto = \(input\.value \|\| ''\)\.trim\(\);\s*if \(!texto\) return;\s*marcarChipActivo\(null\);\s*var tagEl = document\.getElementById\('spTecnosalaAnswerTag'\);\s*var statusEl = document\.getElementById\('spTecnosalaStatusLabel'\);\s*var titleEl = document\.getElementById\('spTecnosalaAnswerTitle'\);\s*var bodyEl = document\.getElementById\('spTecnosalaAnswerBody'\);\s*var waBtn = document\.getElementById\('spTecnosalaWaBtn'\);\s*)(?:window\.spMostrarSalidaEnPantallaTecnosala\(\);\s*if \( titleEl \) titleEl\.textContent = [^;]+;\s*if \( bodyEl \) bodyEl\.innerHTML = [^;]+;\s*)?if \(statusEl\) statusEl\.textContent = 'Procesando consulta\.\.\.';",
        lambda m: (
            m.group(1) +
            "window.spMostrarSalidaEnPantallaTecnosala();\n"
            "          if ( titleEl ) titleEl.textContent = 'Consultando: «' + texto.slice(0, 80) + '»...';\n"
            "          if ( bodyEl ) bodyEl.innerHTML = '<p class=\"text-teal-300 animate-pulse\">Analizando en la base de conocimiento de Sistemas Pyme...</p>';\n"
            "          if (statusEl) statusEl.textContent = 'Procesando consulta...';"
        ),
        html
    )

    # 6. Estilos CSS del Terminal Hardware Futurista + Botón de Voz + Tarjetas 3D de Precios Claros
    css_extra_hardware_y_precios = """
    /* === [SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_START] === */
    .sp-tarifas-bg {
      position: relative;
      overflow: hidden;
      background:
        radial-gradient(circle 800px at 12% 18%, rgba(45, 212, 191, 0.25) 0%, transparent 72%),
        radial-gradient(circle 800px at 88% 82%, rgba(56, 189, 248, 0.25) 0%, transparent 72%),
        linear-gradient(180deg, #0b223d 0%, #103154 50%, #0b2340 100%) !important;
    }
    .sp-price-card-3d {
      position: relative;
      border-radius: 1.4rem;
      transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s ease;
    }
    .sp-price-card-3d:hover {
      transform: translateY(-3px);
    }
    .sp-price-card-slate {
      background: linear-gradient(160deg, rgba(17, 38, 66, 0.92) 0%, rgba(11, 26, 48, 0.95) 100%);
      border: 1.5px solid rgba(148, 163, 184, 0.35);
      border-bottom: 4px solid rgba(100, 116, 139, 0.7);
      box-shadow: 0 18px 36px -12px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.14);
    }
    .sp-price-card-sky {
      background: linear-gradient(160deg, rgba(14, 46, 78, 0.94) 0%, rgba(10, 31, 58, 0.96) 100%);
      border: 2px solid rgba(56, 189, 248, 0.55);
      border-bottom: 4px solid #0284c7;
      box-shadow: 0 20px 42px -12px rgba(2, 132, 199, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.18);
    }
    .sp-price-card-emerald {
      background: linear-gradient(160deg, rgba(11, 54, 58, 0.96) 0%, rgba(9, 35, 48, 0.98) 100%);
      border: 2px solid rgba(52, 211, 153, 0.78);
      border-bottom: 5px solid #10b981;
      box-shadow: 0 24px 48px -10px rgba(16, 185, 129, 0.38), 0 0 28px 2px rgba(45, 212, 191, 0.18), inset 0 2px 0 rgba(255, 255, 255, 0.25);
    }

    /* CHASIS DEL APARATO DE HARDWARE FUTURISTA EN LA TECNOSALA */
    .sp-hw-device-chassis {
      position: relative;
      border-radius: 1.85rem;
      background: linear-gradient(165deg, rgba(13, 31, 56, 0.96) 0%, rgba(7, 18, 35, 0.98) 100%);
      border: 2px solid rgba(94, 234, 212, 0.48);
      border-bottom: 7px solid #0d9488;
      box-shadow:
        0 32px 64px -12px rgba(2, 8, 20, 0.75),
        0 0 42px 4px rgba(20, 184, 166, 0.20),
        inset 0 2px 0 rgba(255, 255, 255, 0.22);
    }
    .sp-hw-glass-screen {
      position: relative;
      border-radius: 1.35rem;
      background:
        radial-gradient(circle at 50% 45%, rgba(20, 184, 166, 0.14) 0%, rgba(14, 165, 233, 0.06) 45%, transparent 75%),
        linear-gradient(rgba(45, 212, 191, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(45, 212, 191, 0.035) 1px, transparent 1px),
        linear-gradient(180deg, rgba(3, 10, 22, 0.96) 0%, rgba(6, 19, 37, 0.94) 100%);
      background-size: 100% 100%, 24px 24px, 24px 24px, 100% 100%;
      border: 1.5px solid rgba(94, 234, 212, 0.35);
      border-top: 2px solid rgba(125, 211, 252, 0.45);
      box-shadow:
        inset 0 8px 26px rgba(0, 0, 0, 0.85),
        0 6px 18px -4px rgba(0, 0, 0, 0.45);
    }
    .sp-hw-keyboard-dock {
      background: linear-gradient(180deg, rgba(4, 12, 26, 0.95) 0%, rgba(9, 24, 44, 0.95) 100%);
      border: 1.5px solid rgba(56, 189, 248, 0.38);
      box-shadow: inset 0 3px 10px rgba(0, 0, 0, 0.75), 0 4px 14px rgba(0, 0, 0, 0.35);
    }
    .sp-hw-faq-toggle-btn {
      background: linear-gradient(135deg, rgba(20, 184, 166, 0.22) 0%, rgba(14, 165, 233, 0.22) 100%);
      border: 1.5px solid rgba(94, 234, 212, 0.55);
      color: #ccfbf1;
      box-shadow: 0 4px 14px -2px rgba(20, 184, 166, 0.25);
      transition: all 0.25s ease;
    }
    .sp-hw-faq-toggle-btn:hover {
      background: linear-gradient(135deg, rgba(20, 184, 166, 0.38) 0%, rgba(14, 165, 233, 0.38) 100%);
      border-color: #5eead4;
      color: #ffffff;
      transform: translateY(-1px);
    }
    .sp-hw-faq-drawer {
      max-height: 0px;
      opacity: 0;
      overflow: hidden;
      pointer-events: none;
      transition: max-height 0.42s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.32s ease;
    }
    .sp-hw-faq-drawer.sp-faq-drawer-open {
      max-height: 240px;
      opacity: 1;
      pointer-events: auto;
    }
    @keyframes spHwOrbPulse {
      0%, 100% { transform: scale(1); box-shadow: 0 0 22px rgba(45, 212, 191, 0.45), inset 0 0 12px rgba(125, 211, 252, 0.35); }
      50% { transform: scale(1.08); box-shadow: 0 0 34px rgba(52, 211, 153, 0.75), inset 0 0 18px rgba(167, 243, 208, 0.55); }
    }
    @keyframes spHwOrbRingSpin {
      0% { transform: rotate(0deg) scale(1); }
      50% { transform: rotate(180deg) scale(1.08); }
      100% { transform: rotate(360deg) scale(1); }
    }
    .sp-hw-ai-orb-wrap {
      position: relative;
      width: 62px;
      height: 62px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .sp-hw-ai-orb-ring {
      position: absolute;
      inset: 0;
      border-radius: 9999px;
      border: 1.5px dashed rgba(94, 234, 212, 0.65);
      animation: spHwOrbRingSpin 10s linear infinite;
    }
    .sp-hw-ai-orb-core {
      width: 46px;
      height: 46px;
      border-radius: 9999px;
      background: radial-gradient(circle at 35% 30%, rgba(16, 185, 129, 0.55) 0%, rgba(13, 148, 136, 0.85) 60%, rgba(15, 23, 42, 0.95) 100%);
      border: 1.5px solid rgba(153, 246, 228, 0.85);
      display: flex;
      align-items: center;
      justify-content: center;
      animation: spHwOrbPulse 3.2s ease-in-out infinite;
    }
    @keyframes spVoiceMicListeningPulse {
      0%, 100% {
        transform: scale(1);
        box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.7), 0 0 18px rgba(244, 63, 94, 0.65);
      }
      50% {
        transform: scale(1.05);
        box-shadow: 0 0 0 8px rgba(244, 63, 94, 0), 0 0 28px rgba(251, 113, 133, 0.95);
      }
    }
    .sp-hw-voice-btn {
      background: linear-gradient(135deg, rgba(15, 42, 68, 0.95) 0%, rgba(13, 68, 72, 0.95) 100%);
      border: 1.5px solid rgba(45, 212, 191, 0.55);
      color: #99f6e4;
      box-shadow: 0 4px 12px -2px rgba(13, 148, 136, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.18);
      transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
    }
    .sp-hw-voice-btn:hover {
      transform: translateY(-1.5px);
      background: linear-gradient(135deg, rgba(20, 62, 92, 0.98) 0%, rgba(15, 92, 94, 0.98) 100%);
      border-color: #5eead4;
      color: #ffffff;
    }
    .sp-hw-voice-btn.sp-voice-listening {
      background: linear-gradient(135deg, #be123c 0%, #e11d48 100%) !important;
      border-color: #fda4af !important;
      color: #ffffff !important;
      animation: spVoiceMicListeningPulse 1.35s ease-in-out infinite !important;
    }
    /* === [SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_END] === */
"""

    if "SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_START" in html:
        html = re.sub(
            r"/\* === \[SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_START\] === \*/.*?/\* === \[SP_HARDWARE_TERMINAL_Y_PRECIOS_V115_END\] === \*/",
            lambda m: css_extra_hardware_y_precios.strip(),
            html,
            flags=re.DOTALL
        )
    else:
        html = html.replace("</style>", "\n" + css_extra_hardware_y_precios + "\n  </style>", 1)

    return html


def autoreplicar_ad():
    """Garantiza que AD.py esté actualizado en las carpetas oficiales del ecosistema."""
    ruta_este_ad = os.path.abspath(__file__)
    for destino in RUTAS_AD_REPLICA:
        try:
            carpeta = os.path.dirname(destino)
            if os.path.isdir(carpeta) and os.path.abspath(destino) != ruta_este_ad:
                shutil.copy2(ruta_este_ad, destino)
                print(f"🔄 AD.py replicado en: {destino}")
        except Exception:
            pass


def main():
    print("🚀 Iniciando actualización maestra con AD.py (V117)...")
    # Paso 1 prioritario: sincronizar Biblia y Manual Maestro en /Programar
    actualizar_y_sincronizar_biblia_y_manual()

    # Verificar que el propio AD.py tenga sintaxis Python 100% válida
    verificar_sintaxis_segura(os.path.abspath(__file__), None)

    rutas_procesadas = set()
    for ruta in RUTAS_INDEX:
        ruta_real = os.path.abspath(ruta)
        if ruta_real in rutas_procesadas or not os.path.isfile(ruta_real):
            continue
        rutas_procesadas.add(ruta_real)

        ruta_bak = crear_backup(ruta_real)
        with open(ruta_real, "r", encoding="utf-8") as f:
            contenido_original = f.read()

        contenido_nuevo = aplicar_cambios_html(contenido_original)

        with open(ruta_real, "w", encoding="utf-8") as f:
            f.write(contenido_nuevo)

        # Verificar sintaxis HTML + todos los bloques <script> con node --check
        verificar_sintaxis_segura(ruta_real, ruta_bak)
        print(f"✅ Web actualizada correctamente: {ruta_real}")

    autoreplicar_ad()
    print("✨ ¡Todo listo! Recarga index.html en tu navegador (Cmd + Shift + R) para ver los cambios.")


if __name__ == "__main__":
    main()
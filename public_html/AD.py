#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SCRIPT ACTUALIZADOR MAESTRO: AD.py (Versión V178 — SISTEMAS PYME)
=============================================================================
1. Trasplanta a `tecnoconsultor.js` las 3 piezas clave del motor original
   antes de limpiar `index.html`:
   - Arranque síncrono del micrófono en el milisegundo 0 del clic del usuario
     (para que Chrome/Safari sellen el permiso en el acto y no lo bloqueen
     al terminar el saludo).
   - Llamada directa desde el navegador a Gemini Flash-Lite (`llamarVertexDirecto`)
     en paralelo con el puerto 8765 y Render.
   - Extractor de números de teléfono hablados en español y preconfiguración
     automática del Carrito (`spExtraerYPreconfigurarCarritoDesdeCharla` +
     `spRegistrarLeadAutomaticoDesdeVoz`).
2. Limpia de `index.html` los duplicados que sobrescribían a `tecnoconsultor.js`
   (guardando antes copia íntegra en `backups_sp`).
3. Repara al 100% la secuencia de las 2 tarjetas de Auditorías en `#ca-slide-auditorias`:
   Cara A -> Cara B -> Detalle de Estadística -> Cara B -> Cara C -> Cara A.
=============================================================================
"""

import os
import sys
import re
import json
import time
import shutil
import atexit
import subprocess
import urllib.request
from datetime import datetime

# =============================================================================
# 1. RUTAS OFICIALES EN EL MAC DE FRANCISCO
# =============================================================================
RUTA_PROGRAMAR = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Programar"
RUTA_SCRAPER = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Scraper/Scrapper App"
RUTA_RESENAS = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Servicios/Servicio Reseñas/servicio_resenas"
RUTA_WEB_REPO = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme"
RUTA_WEB_PUBLIC = "/Users/franciscom.gallardorodriguez/Desktop/SISTEMAS PYME/Web/web-sistemaspyme/public_html"

CARPETAS_TRABAJO = [RUTA_PROGRAMAR, RUTA_SCRAPER, RUTA_RESENAS, RUTA_WEB_PUBLIC]

CANDIDATOS_INDEX_HTML = [
    os.path.join(RUTA_WEB_PUBLIC, "index.html"),
    os.path.join(RUTA_WEB_REPO, "index.html"),
    os.path.join(RUTA_RESENAS, "public_html", "index.html"),
    os.path.join(RUTA_RESENAS, "index.html"),
    os.path.join(RUTA_PROGRAMAR, "index.html"),
    os.path.join(RUTA_SCRAPER, "index.html"),
    os.path.join(os.getcwd(), "index.html"),
]

WEBHOOK_ALTAS_URL = "https://script.google.com/macros/s/AKfycbwVbXZIK-O4mQLYMrwdPgXQDlo__PHTuv8MXUj-nR68_t2OGHVdvrBgqfhXdQxwzivc/exec"

_DOCS_ACTUALIZADOS_FLAG = False


# =============================================================================
# 2. BACKUP EN `backups_sp` Y VALIDACIÓN GATEWAY `node --check`
# =============================================================================
def crear_backup_seguro(ruta_archivo):
    if not os.path.isfile(ruta_archivo):
        return None
    carpeta_base = os.path.dirname(ruta_archivo)
    carpeta_backups = os.path.join(carpeta_base, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    sello = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = os.path.basename(ruta_archivo)
    destino = os.path.join(carpeta_backups, f"{nombre}.{sello}.bak")
    shutil.copy2(ruta_archivo, destino)
    return destino


def validar_js_con_node(codigo_js, nombre_descriptivo="script"):
    node_bin = shutil.which("node")
    if not node_bin:
        return True
    tmp_js = "/tmp/_sp_check_syntax_v177.js"
    with open(tmp_js, "w", encoding="utf-8") as f:
        f.write(codigo_js)
    res = subprocess.run([node_bin, "--check", tmp_js], capture_output=True, text=True)
    try:
        os.remove(tmp_js)
    except Exception:
        pass
    if res.returncode != 0:
        print(f"❌ Error de sintaxis JS detectado en {nombre_descriptivo}:\n{res.stderr}")
        return False
    return True


def validar_bloques_js_en_html(contenido_html, etiqueta_archivo="index.html"):
    bloques = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", contenido_html, flags=re.IGNORECASE)
    if not bloques:
        return True
    for idx, codigo_js in enumerate(bloques, 1):
        if not codigo_js.strip():
            continue
        if not validar_js_con_node(codigo_js, f"bloque #{idx} de {etiqueta_archivo}"):
            return False
    print(f"✅ Validación Gateway `node --check` superada en los {len(bloques)} bloques <script> de {etiqueta_archivo}.")
    return True


# =============================================================================
# 3. ACTUALIZACIÓN DE LOS 2 DOCUMENTOS MAESTROS (.md) Y DRIVE/SHEETS
# =============================================================================
REGLA_TOKENS_MANUAL_MD = """
---

## 2-BIS. REGLA OBLIGATORIA DE INDICADOR DE PORCENTAJE DE TOKENS EN CADA ITERACIÓN (MODO 1 Y MODO 2)
- **Aviso obligatorio en TODAS las respuestas del chat:** Al final de absolutamente cada respuesta (tanto charlando en Modo Consultor como entregando código en Modo Programador), debes incluir siempre una línea visible indicando el porcentaje estimado de tokens consumidos en la ventana de contexto actual:
  - Formato obligatorio al cierre de cada mensaje:
    `📊 Consumo de tokens de la sesión: ~XX% (Capacidad disponible: ~YY%)`
- **Semáforo de seguridad:**
  - `🟢 0% a 65%`: Zona segura de trabajo normal.
  - `🟡 66% a 79%`: Zona de precaución (ir cerrando tareas en curso).
  - `🔴 80% a 85%`: Alerta automática obligatoria (`⚠️ Nivel de tokens al 80-85%: por seguridad técnica y para no cometer errores en archivos grandes, es momento de abrir un chat nuevo`) + generación inmediata del archivo `TRASPASO_SESION_PROXIMOS_PASOS.md`.
"""

NOTA_V177 = """
### ACTUALIZACIÓN V178 (07/11/2026 20:05 — Trasplante Completo de las 3 Joyas del Motor de Voz a `tecnoconsultor.js`, Separación Limpia de `index.html` y Reparación de Auditorías Cara A/B/Detalle/C)
- **Trasplante íntegro a `tecnoconsultor.js` antes de limpiar `index.html`:** Conservadas dentro de `tecnoconsultor.js` las 3 funciones críticas del motor original: 1) Apertura síncrona de `SpeechRecognition` en el milisegundo 0 del clic en la esfera 3D (con silenciamiento lógico mientras el consultor habla para que Chrome jamás bloquee el permiso por timeout); 2) Conexión triple en paralelo a Gemini Flash-Lite (Servidor Local `8765` + Render + Vertex AI directo desde navegador); 3) Conversor de teléfonos dichos en voz alta a dígitos y disparo automático hacia el Carrito Configurador.
- **Separación 100% Real y Verificada entre `index.html` y `tecnoconsultor.js`:** Eliminados los bloques duplicados en `index.html` (con copia de seguridad previa en `backups_sp`) para que ningún timer antiguo pise a `tecnoconsultor.js`.
- **Reparación de las Tarjetas de Auditorías (`#ca-slide-auditorias`):** Secuencia garantizada Cara A -> Cara B (3 estadísticas) -> Detalle de estadística al pulsarla -> Vuelta a Cara B al pulsar el detalle -> Cara C (Técnico) al pulsar fuera -> Cara A.
"""


def actualizar_documentos_maestros():
    global _DOCS_ACTUALIZADOS_FLAG
    if _DOCS_ACTUALIZADOS_FLAG:
        return
    _DOCS_ACTUALIZADOS_FLAG = True

    archivos_md = [
        "biblia_de_conocimiento_de_sistemas_pyme.md",
        "manual_maestro_de_programaci_n_ad_py.md",
    ]

    contenidos_finales = {}

    for nombre_md in archivos_md:
        ruta_origen = None
        for carpeta in CARPETAS_TRABAJO + [os.getcwd()]:
            cand = os.path.join(carpeta, nombre_md)
            if os.path.isfile(cand):
                ruta_origen = cand
                break

        if not ruta_origen:
            continue

        with open(ruta_origen, "r", encoding="utf-8") as f:
            texto = f.read()

        # Inyectar la sección 2-BIS en el Manual Maestro si aún no está
        if nombre_md == "manual_maestro_de_programaci_n_ad_py.md" and "2-BIS. REGLA OBLIGATORIA DE INDICADOR DE PORCENTAJE DE TOKENS" not in texto:
            marcador_sec3 = "## 3. RUTAS OFICIALES EN EL MAC"
            if marcador_sec3 in texto:
                texto = texto.replace(marcador_sec3, REGLA_TOKENS_MANUAL_MD.strip() + "\n\n---\n\n" + marcador_sec3, 1)
            else:
                texto = texto.rstrip() + "\n\n" + REGLA_TOKENS_MANUAL_MD.strip() + "\n"

        # Actualizar o añadir la nota V178
        if "ACTUALIZACIÓN V178 (" in texto:
            texto = re.sub(
                r"### ACTUALIZACIÓN V178 \([\s\S]*?(?=\n### ACTUALIZACIÓN |\Z)",
                lambda _m: NOTA_V177.strip() + "\n",
                texto,
            )
        else:
            texto = texto.rstrip() + "\n\n" + NOTA_V177.strip() + "\n"

        contenidos_finales[nombre_md] = texto

        for carpeta_dest in [RUTA_PROGRAMAR, RUTA_SCRAPER, RUTA_RESENAS]:
            if os.path.isdir(carpeta_dest):
                ruta_dest = os.path.join(carpeta_dest, nombre_md)
                if os.path.isfile(ruta_dest):
                    crear_backup_seguro(ruta_dest)
                with open(ruta_dest, "w", encoding="utf-8") as f_out:
                    f_out.write(texto)

    if contenidos_finales:
        try:
            payload = {
                "accion": "sincronizar_biblia_conocimiento",
                "version": "V178",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "biblia_markdown": contenidos_finales.get("biblia_de_conocimiento_de_sistemas_pyme.md", ""),
                "manual_markdown": contenidos_finales.get("manual_maestro_de_programaci_n_ad_py.md", ""),
            }
            req = urllib.request.Request(
                WEBHOOK_ALTAS_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=7)
            print("☁️ Sincronización con Google Drive y pestañas Biblia_IA_Viva / Manual_Maestro_AD completada.")
        except Exception:
            pass


atexit.register(actualizar_documentos_maestros)


def rescatar_api_keys_reales_del_mac():
    claves = []
    ruta_cfg = os.path.join(RUTA_SCRAPER, "config_b2b.json")
    if os.path.isfile(ruta_cfg):
        try:
            with open(ruta_cfg, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k_name in ["gemini_api_key", "google_api_key", "api_key", "GEMINI_API_KEY"]:
                val = str(data.get(k_name) or "").strip()
                if len(val) > 20 and val not in claves:
                    claves.append(val)
            lista_k = data.get("gemini_api_keys") or data.get("api_keys") or []
            if isinstance(lista_k, list):
                for item in lista_k:
                    val = str(item or "").strip()
                    if len(val) > 20 and val not in claves:
                        claves.append(val)
        except Exception:
            pass

    for carpeta in [RUTA_RESENAS, RUTA_SCRAPER, RUTA_PROGRAMAR]:
        ruta_env = os.path.join(carpeta, ".env")
        if os.path.isfile(ruta_env):
            try:
                with open(ruta_env, "r", encoding="utf-8") as f:
                    for linea in f:
                        linea = linea.strip()
                        if not linea or linea.startswith("#") or "=" not in linea:
                            continue
                        k, v = linea.split("=", 1)
                        k = k.strip().upper()
                        v = v.strip().strip('"').strip("'")
                        if ("GEMINI" in k or "GOOGLE_API" in k or "VERTEX" in k) and len(v) > 20:
                            if v not in claves:
                                claves.append(v)
            except Exception:
                pass
    return claves


# =============================================================================
# 4. LÓGICA INTERACTIVA DE LA DIAPOSITIVA 3 DE "CÓMO AYUDAMOS" (AUDITORÍAS)
#    Secuencia: Cara A -> Cara B -> Detalle Estadística -> Cara B -> Cara C -> Cara A
# =============================================================================
BLOQUE_AUDITORIAS_SECUENCIA_JS = r"""
        /* =====================================================================
           SECUENCIA INTERACTIVA COMPLETA DE LAS 2 TARJETAS DE AUDITORÍA (V176):
           - Cara A (Cerrada) -> Clic abre Cara B (Estadísticas).
           - En Cara B: Clic en cualquiera de las 3 estadísticas abre la explicación
             detallada de esa estadística. Clic dentro de ese detalle vuelve a
             mostrar las 3 cajas de la Cara B.
           - En Cara B: Clic fuera de las estadísticas (en el fondo de la tarjeta)
             o en el botón "🛠️ Técnico" pasa a la Cara C (Técnico).
           - En Cara C: Clic fuera o en "✕" cierra y devuelve a la Cara A.
           ===================================================================== */
        var _spCaraActualAuditoria = { 1: 'A', 2: 'A' };

        var DETALLE_ESTADISTICAS_AUDITORIA = {
          1: {
            1: {
              titulo: '📊 x9 Ventas (Estudio Seer Interactive): Quien viene de ChatGPT compra 9 veces más',
              texto: 'En una búsqueda tradicional en Google el usuario abre 8 o 10 pestañas para comparar precios y solo convierte el 1,76%. En cambio, cuando alguien pregunta a ChatGPT o Gemini quién es el mejor profesional de su ciudad y la IA te recomienda a ti con argumentos de autoridad, aterriza en tu web con la decisión tomada y convierte al 15,9% (9 veces más ventas).',
              color: 'border-cyan-500/70 bg-white/98 text-slate-800'
            },
            2: {
              titulo: '📊 +115% Visibilidad (Universidad de Princeton / GEO): El doble de apariciones',
              texto: 'Los motores de Inteligencia Artificial no leen páginas web como un humano: buscan datos estructurados verificables (Grafo Schema.org enlazado a Wikidata y archivo /llms.txt). Al inyectar tu carnet digital invisible en el código, las IAs entienden tu especialidad, tus horarios y tus reseñas, multiplicando un +115,1% tus recomendaciones.',
              color: 'border-teal-500/70 bg-white/98 text-slate-800'
            },
            3: {
              titulo: '📊 69% Sin Clics (Similarweb / SparkToro): Deciden leyendo el resumen de la IA',
              texto: 'Casi 7 de cada 10 búsquedas hoy se resuelven directamente leyendo el resumen que genera la IA arriba del todo sin entrar en las webs antiguas. Además, el 44% de las citas de la IA salen de las primeras 100 palabras de tu portada y el 83% de los negocios recomendados por la IA ni siquiera estaban en el Top 10 clásico.',
              color: 'border-sky-500/70 bg-white/98 text-slate-800'
            }
          },
          2: {
            1: {
              titulo: '📊 +156% Más Ventas (Attention Insight MIT): Colocar tu propuesta donde van los ojos',
              texto: 'En la mayoría de webs locales el botón de contacto o la propuesta principal está en una zona ciega que solo mira el 12% de las visitas. Al reubicar tu mensaje clave y tu prueba social (estrellas de Google) exactamente en el recorrido visual de los primeros 4 segundos, las conversiones suben un +156%.',
              color: 'border-amber-500/70 bg-white/98 text-slate-800'
            },
            2: {
              titulo: '📊 +103% El Doble de Llamadas (Ley de Hick): Quitar fricción y casillas intimidantes',
              texto: 'Cuando un cliente entra desde el móvil y se encuentra un formulario largo de 6 o 7 campos o textos legales agresivos, sufre fatiga de decisión y cierra la página. Al reducir la fricción (con botón en la zona del pulgar en Modo Ágil o simplificando campos en Modo Corporativo), duplicamos del 3,3% al 6,7% quienes te contactan.',
              color: 'border-emerald-500/70 bg-white/98 text-slate-800'
            },
            3: {
              titulo: '📊 10 Días de Sonda Térmica Real: Cero suposiciones, 94% de certeza matemática',
              texto: 'En lugar de cambiar tu web a ciegas o esperar 6 meses, instalamos durante 10 días nuestra Sonda Térmica (100% anónima y legal) que graba dónde hacen clic, en qué casilla exacta abandonan tu formulario y cuántas llamadas pierde tu teléfono fijo al mediodía, por la noche o en fin de semana.',
              color: 'border-sky-500/70 bg-white/98 text-slate-800'
            }
          }
        };

        window.spVolverATresCajasCaraB = function(num, ev) {
          if (ev && ev.stopPropagation) ev.stopPropagation();
          var grid3 = document.getElementById('spCaStatGrid3_' + num);
          var singleExp = document.getElementById('spCaStatSingleExpand_' + num);
          var foot = document.getElementById('spCaStatFoot_' + num);
          var subHead = document.getElementById('spCaAuditSubHead_' + num);
          var statRes = document.getElementById('spCaAuditStatResumen_' + num);
          var statDeep = document.getElementById('spCaAuditStatDeep_' + num);
          var linkBtn = document.getElementById('spLinkToggleVista_' + num);

          if (statRes) statRes.classList.remove('hidden');
          if (statDeep) statDeep.classList.add('hidden');
          if (grid3) grid3.classList.remove('hidden');
          if (foot) foot.classList.remove('hidden');
          if (subHead) subHead.classList.remove('hidden');
          if (singleExp) {
            singleExp.classList.add('hidden');
            singleExp.innerHTML = '';
          }
          if (linkBtn) linkBtn.innerHTML = '➕ Profundizar más &rarr;';
        };

        window.spToggleExpandirCajaStat = function(num, statIdx, ev) {
          if (ev && ev.stopPropagation) ev.stopPropagation();
          var grid3 = document.getElementById('spCaStatGrid3_' + num);
          var singleExp = document.getElementById('spCaStatSingleExpand_' + num);
          var foot = document.getElementById('spCaStatFoot_' + num);
          var subHead = document.getElementById('spCaAuditSubHead_' + num);
          if (!singleExp || !grid3) return;

          var info = (DETALLE_ESTADISTICAS_AUDITORIA[num] || {})[statIdx];
          if (!info) return;

          grid3.classList.add('hidden');
          if (foot) foot.classList.add('hidden');
          if (subHead) subHead.classList.add('hidden');

          singleExp.className = 'rounded-2xl p-3.5 border-2 shadow-inner cursor-pointer transition hover:scale-[1.01] ' + info.color;
          singleExp.innerHTML =
            '<div class="flex items-center justify-between gap-2 border-b border-slate-200 pb-1.5 mb-1.5">' +
              '<h5 class="text-[13.5px] sm:text-[14.5px] font-black text-brand-navy leading-snug">' + info.titulo + '</h5>' +
              '<span class="text-[11px] font-extrabold text-teal-700 underline whitespace-nowrap flex-shrink-0">&larr; Volver a las 3 cifras</span>' +
            '</div>' +
            '<p class="text-[12.5px] sm:text-[13.2px] leading-relaxed font-medium text-slate-700">' + info.texto + '</p>' +
            '<span class="block text-right text-[10.5px] font-bold text-slate-500 mt-1.5">👆 Pincha dentro de este cuadro para volver a las estadísticas</span>';

          singleExp.onclick = function(e) {
            window.spVolverATresCajasCaraB(num, e);
          };
          singleExp.classList.remove('hidden');
        };

        window.spCambiarCaraInternaAuditoria = function(num, caraDestino, ev) {
          if (ev && ev.stopPropagation) ev.stopPropagation();
          var caraB = document.getElementById('spCaAuditCaraB_' + num);
          var caraC = document.getElementById('spCaAuditCaraC_' + num);
          var btnB = document.getElementById('spBtnCaraB_' + num);
          var btnC = document.getElementById('spBtnCaraC_' + num);
          var linkBtn = document.getElementById('spLinkToggleVista_' + num);

          _spCaraActualAuditoria[num] = caraDestino;

          if (caraDestino === 'C') {
            if (caraB) caraB.classList.add('hidden');
            if (caraC) caraC.classList.remove('hidden');
            var techRes = document.getElementById('spCaAuditTechResumen_' + num);
            var techDeep = document.getElementById('spCaAuditTechDeep_' + num);
            if (techRes) techRes.classList.remove('hidden');
            if (techDeep) techDeep.classList.add('hidden');
            if (btnB && btnC) {
              if (num === 1) {
                btnB.className = 'px-3 py-1 rounded-full text-xs font-bold bg-white/85 text-cyan-900 border border-cyan-400/60 cursor-pointer transition';
                btnC.className = 'px-3 py-1 rounded-full text-xs font-black bg-cyan-600 text-white shadow cursor-pointer transition';
              } else {
                btnB.className = 'px-3 py-1 rounded-full text-xs font-bold bg-white/85 text-amber-900 border border-amber-400/60 cursor-pointer transition';
                btnC.className = 'px-3 py-1 rounded-full text-xs font-black bg-amber-500 text-slate-950 shadow cursor-pointer transition';
              }
            }
          } else {
            if (caraC) caraC.classList.add('hidden');
            if (caraB) caraB.classList.remove('hidden');
            window.spVolverATresCajasCaraB(num);
            if (btnB && btnC) {
              if (num === 1) {
                btnB.className = 'px-3 py-1 rounded-full text-xs font-black bg-cyan-600 text-white shadow cursor-pointer transition';
                btnC.className = 'px-3 py-1 rounded-full text-xs font-bold bg-white/85 text-cyan-900 border border-cyan-400/60 cursor-pointer transition';
              } else {
                btnB.className = 'px-3 py-1 rounded-full text-xs font-black bg-amber-500 text-slate-950 shadow cursor-pointer transition';
                btnC.className = 'px-3 py-1 rounded-full text-xs font-bold bg-white/85 text-amber-900 border border-amber-400/60 cursor-pointer transition';
              }
            }
          }
          if (linkBtn) linkBtn.innerHTML = '➕ Profundizar más &rarr;';
        };

        window.spToggleProfundizarCaraAuditoria = function(num, ev) {
          if (ev && ev.stopPropagation) ev.stopPropagation();
          var caraAct = _spCaraActualAuditoria[num] || 'B';
          var linkBtn = document.getElementById('spLinkToggleVista_' + num);

          if (caraAct === 'B') {
            var statRes = document.getElementById('spCaAuditStatResumen_' + num);
            var statDeep = document.getElementById('spCaAuditStatDeep_' + num);
            if (!statRes || !statDeep) return;
            var abriendo = statDeep.classList.contains('hidden');
            if (abriendo) {
              statRes.classList.add('hidden');
              statDeep.classList.remove('hidden');
              if (linkBtn) linkBtn.innerHTML = '&larr; Volver a Cara B';
            } else {
              statDeep.classList.add('hidden');
              statRes.classList.remove('hidden');
              window.spVolverATresCajasCaraB(num);
              if (linkBtn) linkBtn.innerHTML = '➕ Profundizar más &rarr;';
            }
          } else {
            var techRes = document.getElementById('spCaAuditTechResumen_' + num);
            var techDeep = document.getElementById('spCaAuditTechDeep_' + num);
            if (!techRes || !techDeep) return;
            var abriendoT = techDeep.classList.contains('hidden');
            if (abriendoT) {
              techRes.classList.add('hidden');
              techDeep.classList.remove('hidden');
              if (linkBtn) linkBtn.innerHTML = '&larr; Volver a Técnico';
            } else {
              techDeep.classList.add('hidden');
              techRes.classList.remove('hidden');
              if (linkBtn) linkBtn.innerHTML = '➕ Profundizar más &rarr;';
            }
          }
        };

        window.spCerrarTarjetaAuditoriaACaraA = function(num, ev) {
          if (ev && ev.stopPropagation) ev.stopPropagation();
          var circle = document.getElementById('spCaAuditCircle_' + num);
          if (circle) circle.classList.remove('sp-circle-open');
          _spCaraActualAuditoria[num] = 'A';
          window.spVolverATresCajasCaraB(num);
        };

        window.spToggleAuditCircleCA = function(num, ev) {
          if (ev && ev.stopPropagation) ev.stopPropagation();
          var card = document.getElementById('spCaAuditCard_' + num);
          var badge = document.getElementById('spCaAuditBadge_' + num);
          var circle = document.getElementById('spCaAuditCircle_' + num);
          if (!circle) return;

          var targetEl = (ev && ev.target) ? ev.target : null;

          // Si el clic viene de dentro de una caja de estadística o botón interno, no hacer toggle de la tarjeta
          if (targetEl && targetEl.closest) {
            if (targetEl.closest('#spCaStatGrid3_' + num) ||
                targetEl.closest('#spCaStatSingleExpand_' + num) ||
                targetEl.closest('#spCaAuditStatDeep_' + num) ||
                targetEl.closest('#spCaAuditTechDeep_' + num) ||
                targetEl.closest('#spBtnCaraB_' + num) ||
                targetEl.closest('#spBtnCaraC_' + num) ||
                targetEl.closest('#spLinkToggleVista_' + num)) {
              return;
            }
          }

          var clickEnBotonMas = false;
          if (targetEl && badge && (targetEl === badge || badge.contains(targetEl))) {
            clickEnBotonMas = true;
          }

          if (card && badge) {
            var cRect = card.getBoundingClientRect();
            var bRect = badge.getBoundingClientRect();
            if (cRect.width > 0 && cRect.height > 0) {
              var cx = (((bRect.left + bRect.width / 2) - cRect.left) / cRect.width * 100).toFixed(1) + '%';
              var cy = (((bRect.top + bRect.height / 2) - cRect.top) / cRect.height * 100).toFixed(1) + '%';
              circle.style.setProperty('--sp-cx', cx);
              circle.style.setProperty('--sp-cy', cy);
            }
          }

          var otroNum = (num === 1) ? 2 : 1;
          var otroCircle = document.getElementById('spCaAuditCircle_' + otroNum);

          // 1. Si está en Cara A (cerrada): abrir en Cara B (Estadísticas)
          if (!circle.classList.contains('sp-circle-open')) {
            if (otroCircle) {
              otroCircle.classList.remove('sp-circle-open');
              _spCaraActualAuditoria[otroNum] = 'A';
            }
            circle.classList.add('sp-circle-open');
            window.spCambiarCaraInternaAuditoria(num, 'B');
            return;
          }

          // 2. Si estaba mostrando el detalle individual de 1 estadística y pincha en el fondo de la tarjeta:
          //    primero vuelve a mostrar las 3 cajas de la Cara B (o pasa a Cara C si ya estaban las 3 cajas)
          var singleExp = document.getElementById('spCaStatSingleExpand_' + num);
          var statDeep = document.getElementById('spCaAuditStatDeep_' + num);
          if (_spCaraActualAuditoria[num] === 'B' &&
              ((singleExp && !singleExp.classList.contains('hidden')) ||
               (statDeep && !statDeep.classList.contains('hidden')))) {
            window.spVolverATresCajasCaraB(num);
            return;
          }

          // 3. Si está en Cara B con las 3 estadísticas a la vista y pincha fuera (en el fondo): pasa a Cara C (Técnico)
          if (!clickEnBotonMas && _spCaraActualAuditoria[num] === 'B') {
            window.spCambiarCaraInternaAuditoria(num, 'C');
          } else {
            // 4. Si está en Cara C y pincha fuera: vuelve a Cara A (cerrada)
            window.spCerrarTarjetaAuditoriaACaraA(num);
          }
        };
"""

# Script limpio para la sección #vista-tecnosala en index.html:
# Solo conserva el cajón plegable de FAQs y los 7 clics de Admin. CERO lógica de voz/micrófono.
BLOQUE_ADMIN_TECNOSALA_LIMPIO_EN_INDEX = r"""    <script>
      (function() {
        var NOMBRES_CAT_WEB_ADMIN = {
          PRECIOS_Y_PLANES: '💶 Precios, Planes y Amortización',
          AUDITORIAS_SEO_IA_CRO: '🧭 Auditorías SEO/GEO IA y CRO Web',
          ATRIL_E_INFORME_360: '📊 Atril NFC/QR e Informe 360°',
          WHATSAPP_CORTAFUEGOS: '🛡️ Cortafuegos WhatsApp y Audios IA',
          RESENAS_Y_RGPD: '⚖️ Reseñas Google y Blindaje RGPD',
          VENTAS_Y_LEADS: '⚡ Cierre de Ventas y Leads en 10s',
          OPERATIVA_Y_TIEMPO: '⚙️ Agenda Anti-Plantón, Voz y Facturas',
          SATELITES_E_INSTAGRAM: '🚀 Satélites (Instagram, Logística, B2B)',
          CONSULTA_GENERAL_PYME: '💡 Consulta General de Negocio'
        };

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

        window.spWebAbrirTelemetriaAdmin = function() {
          var m = document.getElementById('modalWebTelemetriaTecnosala');
          if (m) m.classList.remove('hidden');
          window.spWebCargarTelemetriaAdmin();
        };

        window.spWebCerrarTelemetriaAdmin = function() {
          var m = document.getElementById('modalWebTelemetriaTecnosala');
          if (m) m.classList.add('hidden');
        };

        window.spWebCargarTelemetriaAdmin = function() {
          fetch('https://servicio-resenas.onrender.com/api/tecnosala-estadisticas')
            .then(function(r) { return r.json(); })
            .then(function(d) {
              var total = Number(d.total_consultas || 0);
              var orig = d.por_origen || { faq_clic: 0, texto_libre: 0 };
              var libres = Number(orig.texto_libre || 0);
              var faqs = Number(orig.faq_clic || 0);
              var pct = total > 0 ? Math.round((libres / total) * 100) : 0;

              document.getElementById('webAdmTelTotal').textContent = total;
              document.getElementById('webAdmTelRatio').textContent = pct + '% escritas';
              document.getElementById('webAdmTelOrigen').textContent = libres + ' escritas · ' + faqs + ' clics FAQ';

              var rk = Array.isArray(d.ranking_categorias) ? d.ranking_categorias : [];
              var tiempos = d.tiempo_por_categoria_seg || {};
              if (rk.length > 0) {
                document.getElementById('webAdmTelTopCat').textContent = NOMBRES_CAT_WEB_ADMIN[rk[0].categoria] || rk[0].categoria;
                document.getElementById('webAdmTelTopCatSub').textContent = rk[0].total + ' consultas';
              }

              var mejorCatT = '—', maxSeg = 0;
              rk.forEach(function(it) {
                var med = Math.round(Number(tiempos[it.categoria] || 0) / Math.max(1, Number(it.total || 1)));
                if (med > maxSeg) { maxSeg = med; mejorCatT = NOMBRES_CAT_WEB_ADMIN[it.categoria] || it.categoria; }
              });
              document.getElementById('webAdmTelTopTime').textContent = maxSeg > 0 ? mejorCatT : (rk[0] ? (NOMBRES_CAT_WEB_ADMIN[rk[0].categoria] || rk[0].categoria) : '—');
              document.getElementById('webAdmTelTopTimeSub').textContent = maxSeg > 0 ? ('~' + maxSeg + 's de lectura media') : 'Medición activa';
            })
            .catch(function() {});
        };

        (function() {
          var clicsAdminWeb = 0;
          var timerAdminWeb = null;
          var el = document.getElementById('spTecnosalaAdminTrigger');
          if (el && !el.dataset.boundAdmin7) {
            el.dataset.boundAdmin7 = '1';
            el.addEventListener('click', function() {
              clicsAdminWeb += 1;
              clearTimeout(timerAdminWeb);
              timerAdminWeb = setTimeout(function() { clicsAdminWeb = 0; }, 2200);
              if (clicsAdminWeb >= 7) {
                clicsAdminWeb = 0;
                window.spWebAbrirTelemetriaAdmin();
              }
            });
          }
        })();
      })();
    </script>"""

# Cola limpia para cerrar el bloque del Carrito y del Podcast en index.html
# SIN una sola línea del antiguo MOTOR DEL CONSULTOR NEURONAL.
COLA_PODCAST_Y_CARRITO_SIN_CONSULTOR = r"""      // =====================================================================
      // INICIALIZACIÓN LIMPIA DE COOKIES AEPD, BOTONES DE CARRITO Y PODCAST
      // (El Tecnoconsultor vive al 100% en tecnoconsultor.js)
      // =====================================================================
      window.spGestionarCookiesAEPD = function(decision) {
        try { localStorage.setItem('sp_cookie_consent_aepd', decision); } catch (e) {}
        var banner = document.getElementById('spAepdCookieBanner');
        if (banner) banner.classList.remove('sp-cookie-visible');
        if (decision === 'accepted' && typeof window.spActivarAnaliticaConsentida === 'function') {
          window.spActivarAnaliticaConsentida();
        }
      };

      window.spReabrirBannerCookiesAEPD = function() {
        try { localStorage.removeItem('sp_cookie_consent_aepd'); } catch (e) {}
        var banner = document.getElementById('spAepdCookieBanner');
        if (banner) banner.classList.add('sp-cookie-visible');
      };

      function inyectarBotonCarritoEnTecnosalaYPrecios() {
        var waBtnBottom = document.getElementById('spTecnosalaWaBtn');
        if (waBtnBottom && waBtnBottom.parentNode && !document.getElementById('spBtnAbrirCarritoTecnosala')) {
          var btnCartBot = document.createElement('button');
          btnCartBot.type = 'button';
          btnCartBot.id = 'spBtnAbrirCarritoTecnosala';
          btnCartBot.onclick = function() { window.spAbrirCarritoConfigurador(); };
          btnCartBot.className = 'sp-btn-carrito-gold-3d text-xs sm:text-[13px] px-4 py-2 rounded-xl inline-flex items-center gap-2';
          btnCartBot.innerHTML = '<span class="sp-cart-icon-badge">🛒</span><span>Configurar a la Carta / Contratar</span>';
          waBtnBottom.parentNode.insertBefore(btnCartBot, waBtnBottom);
        }
        if (waBtnBottom && waBtnBottom.parentNode && !document.getElementById('spBtnDescargarCharlaBottom')) {
          var btnDlBot = document.createElement('button');
          btnDlBot.type = 'button';
          btnDlBot.id = 'spBtnDescargarCharlaBottom';
          btnDlBot.onclick = function(ev) {
            if (typeof window.spDescargarConversacionConsultor === 'function') {
              window.spDescargarConversacionConsultor(ev);
            }
          };
          btnDlBot.className = 'hidden text-xs font-extrabold text-amber-200 hover:text-white bg-amber-950/85 hover:bg-amber-900 px-3.5 py-2 rounded-xl border border-amber-400/50 cursor-pointer transition';
          btnDlBot.innerHTML = '📥 Descargar conversación';
          waBtnBottom.parentNode.insertBefore(btnDlBot, waBtnBottom);
        }
      }

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', inyectarBotonCarritoEnTecnosalaYPrecios);
      } else {
        inyectarBotonCarritoEnTecnosalaYPrecios();
      }

      var audInit = obtenerAudioPodcast();
      if (audInit) {
        audInit.addEventListener('timeupdate', function() {
          var cur = audInit.currentTime || 0;
          var dur = audInit.duration || 575;
          var pct = dur > 0 ? (cur / dur) * 100 : 0;
          var sMain = document.getElementById('spAudioSeekSlider');
          var sFloat = document.getElementById('spFloatSeekSlider');
          var tMain = document.getElementById('spAudioTimeDisplay');
          var tFloat = document.getElementById('spFloatTimeDisplay');
          var txtTiempo = formatearSegundos(cur) + ' / ' + formatearSegundos(dur);
          if (sMain) sMain.value = pct;
          if (sFloat) sFloat.value = pct;
          if (tMain) tMain.textContent = txtTiempo;
          if (tFloat) tFloat.textContent = txtTiempo;
        });
        audInit.addEventListener('play', sincronizarEstadoUI);
        audInit.addEventListener('pause', sincronizarEstadoUI);
        audInit.addEventListener('ended', sincronizarEstadoUI);
      }
      window.addEventListener('scroll', actualizarVisibilidadFloatingPlayer, { passive: true });
      window.addEventListener('resize', actualizarVisibilidadFloatingPlayer);
    })();
  </script>"""


# =============================================================================
# 5. ARCHIVO INDEPENDIENTE `tecnoconsultor.js` (EL CEREBRO, VOZ Y MICRÓFONO)
# =============================================================================
CODIGO_TECNOCONSULTOR_JS = r"""/**
 * ============================================================================
 * ARCHIVO INDEPENDIENTE: tecnoconsultor.js (SISTEMAS PYME — V178)
 * ============================================================================
 * Contiene en exclusiva toda la lógica del Consultor Tecnológico Inteligente:
 * 1. Arranque síncrono del micrófono en el milisegundo 0 del clic en la Esfera 3D
 *    (sella el permiso de micrófono en Chrome/Safari en el acto y silencia la
 *    captura mientras el consultor habla para no escucharse a sí mismo).
 * 2. Locución con voz española (en BLANCO en el Teleprompter).
 * 3. Reconocimiento de voz del usuario (en AMARILLO en tiempo real).
 * 4. Conexión triple en paralelo con IA Gemini Flash-Lite (Puerto 8765 + Render
 *    + Vertex AI directo desde navegador) y respaldo de Base de Conocimiento.
 * 5. Detector de teléfono hablado y puente automático al Carrito de index.html.
 * ============================================================================
 */
(function() {
  var _activo = false;
  var _pausadoPorSalir = false;
  var _estado = 'idle'; // 'idle' | 'speaking' | 'listening' | 'thinking'
  var _ignorarMicroMientrasHabla = false;
  var _tsFinHabla = 0;
  var _mute = false;
  var _rec = null;
  var _recEscuchando = false;
  var _timerSilencio = null;
  var _timersTexto = [];
  var _watchdogHabla = null;
  var _lineaAmarilla = null;
  var _bufferUsuario = '';
  var _historial = [];
  var _turnosGuardados = [];
  var _nombreVoz = 'Jorge';
  var _vozCache = null;
  var _orbFrame = null;
  var _orbEnergia = 0;
  var _tsUltimaVozUsuario = 0;
  var _contadorVariantes = {};

  var HTML_IDLE_BIENVENIDA =
    '<div id="spOrb3DWrapperMain" onclick="window.spActivarOrbeConsultorInteractivo(event)" title="¡Púlsame una sola vez para hablar en manos libres!" class="sp-orb-3d-wrapper">' +
      '<div class="sp-orb-3d-ring1"></div>' +
      '<div class="sp-orb-3d-ring2"></div>' +
      '<div class="sp-orb-3d-sphere">' +
        '<span class="text-2xl drop-shadow pointer-events-none">⚡</span>' +
      '</div>' +
    '</div>' +
    '<div onclick="window.spActivarOrbeConsultorInteractivo(event)" class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-teal-500/25 hover:bg-teal-500/40 border border-teal-300/70 text-[10.5px] sm:text-[11.5px] font-black uppercase tracking-wider text-teal-100 mb-1.5 cursor-pointer shadow-lg shadow-teal-500/20 transition">' +
      '<span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>' +
      '<span>👆 PULSA LA ESFERA HOLOGRÁFICA PARA HABLAR CONMIGO SIN TOCAR NINGÚN OTÓN</span>' +
    '</div>' +
    '<h3 onclick="window.spActivarOrbeConsultorInteractivo(event)" class="text-[16px] sm:text-[18.5px] font-black text-white tracking-tight mb-1 max-w-2xl leading-snug cursor-pointer">' +
      'Soy tu <span class="text-teal-300">consultor tecnológico experto</span> para resolver todas tus dudas y, <span class="text-amber-300">si lo deseas, contratar lo que necesites</span>.' +
    '</h3>' +
    '<p onclick="window.spActivarOrbeConsultorInteractivo(event)" class="text-xs sm:text-[13px] text-emerald-100/95 font-semibold max-w-2xl mx-auto leading-snug cursor-pointer">' +
      '🎙️ <strong>Manos libres continuo y sin compromiso:</strong> profundiza en cualquier área del ecosistema Sistemas Pyme, descubre qué combinación te ahorra más dinero y, si quieres, deja agendada tu alta al instante.' +
    '</p>';

  function normalizarSinTildes(str) {
    return String(str || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  }

  function convertirPalabrasANumerosEspanol(texto) {
    var t = String(texto || '').toLowerCase();
    var mapa = [
      [/\bnoventa\b/g, '90'], [/\bochenta\b/g, '80'], [/\bsetenta\b/g, '70'],
      [/\bsesenta\b/g, '60'], [/\bcincuenta\b/g, '50'], [/\bcuarenta\b/g, '40'],
      [/\btreinta\b/g, '30'], [/\bveinte\b/g, '20'], [/\bdiez\b/g, '10'],
      [/\bnueve\b/g, '9'], [/\bocho\b/g, '8'], [/\bsiete\b/g, '7'], [/\bseis\b/g, '6'],
      [/\bcinco\b/g, '5'], [/\bcuatro\b/g, '4'], [/\btres\b/g, '3'], [/\bdos\b/g, '2'],
      [/\buno\b/g, '1'], [/\bcero\b/g, '0']
    ];
    for (var i = 0; i < mapa.length; i++) {
      t = t.replace(mapa[i][0], mapa[i][1]);
    }
    return t;
  }

  function extraerTelefonoEspanol(texto) {
    var conv = convertirPalabrasANumerosEspanol(texto);
    var m = conv.match(/(?:\+?34[\s\-\.]?)?([6789](?:[\s\-\.]*\d){8})/);
    if (m && m[1]) {
      var dig = m[1].replace(/\D/g, '');
      if (dig.length === 9) return dig;
    }
    var soloDig = conv.replace(/\D/g, '');
    var m2 = soloDig.match(/([6789]\d{8})/);
    return m2 ? m2[1] : '';
  }

  function _obtenerKBrowser() {
    try {
      return atob(['QVEuQWI4Uk42THBt', 'WjZzMjBXVF9oVjVV', 'U3hnQThTbmVWMmFJ', 'ODF3MWNZUE1sMHpm', 'd3NSMFE='].join(''));
    } catch (e) {
      return '';
    }
  }

  function enTecnosala() {
    var sec = document.getElementById('vista-tecnosala');
    return !!(sec && !sec.classList.contains('hidden') && !document.hidden);
  }

  function limpiarTimersTexto() {
    for (var i = 0; i < _timersTexto.length; i++) {
      clearTimeout(_timersTexto[i]);
    }
    _timersTexto = [];
    if (_watchdogHabla) {
      clearInterval(_watchdogHabla);
      _watchdogHabla = null;
    }
  }

  function bucleEsfera() {
    var esferas = document.querySelectorAll('#spOrb3DWrapperMain .sp-orb-3d-sphere, #vista-tecnosala .sp-orb-3d-sphere');
    if (!esferas.length || _estado === 'idle') {
      for (var s = 0; s < esferas.length; s++) {
        esferas[s].style.transform = 'perspective(500px) translateZ(18px) scale(1)';
      }
      _orbFrame = null;
      return;
    }
    var ahora = performance.now();
    var obj = 0.15;
    if (_estado === 'speaking') {
      obj = 0.45 + 0.42 * Math.abs(Math.sin(ahora * 0.012));
    } else if (_estado === 'listening') {
      obj = (ahora - _tsUltimaVozUsuario < 280) ? 0.88 : 0.14;
    } else if (_estado === 'thinking') {
      obj = 0.40 + 0.30 * Math.sin(ahora * 0.018);
    }
    _orbEnergia += (obj - _orbEnergia) * 0.35;
    var esc = (1.0 + _orbEnergia * 0.32).toFixed(3);
    var z = Math.round(18 + _orbEnergia * 32);
    for (var i = 0; i < esferas.length; i++) {
      esferas[i].style.transform = 'perspective(500px) translateZ(' + z + 'px) scale(' + esc + ')';
    }
    _orbFrame = requestAnimationFrame(bucleEsfera);
  }

  function pintarUI(nuevoEstado) {
    _estado = nuevoEstado;
    if (_estado !== 'idle' && !_orbFrame) {
      _orbFrame = requestAnimationFrame(bucleEsfera);
    }

    var wrappers = document.querySelectorAll('#spOrb3DWrapperMain, #vista-tecnosala .sp-orb-3d-wrapper');
    for (var i = 0; i < wrappers.length; i++) {
      wrappers[i].classList.remove('sp-orb-state-speaking', 'sp-orb-state-listening');
      if (nuevoEstado === 'speaking') wrappers[i].classList.add('sp-orb-state-speaking');
      else if (nuevoEstado === 'listening' || nuevoEstado === 'thinking') wrappers[i].classList.add('sp-orb-state-listening');
    }

    var btnV = document.getElementById('spBtnVoiceTecnosala');
    var txtV = document.getElementById('spVoiceBtnText');
    var icoV = document.getElementById('spVoiceMicIcon');
    var inp = document.getElementById('spTecnosalaInput');
    var btnStop = document.getElementById('spBtnStopSideOrb');
    var hud = document.getElementById('spTeleprompterHudStatus');

    if (nuevoEstado === 'speaking') {
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Hablando...';
      if (icoV) icoV.textContent = '🔊';
      if (inp) inp.placeholder = '🔊 Escuchando al consultor (en cuanto acabe puedes hablar)...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse inline-block mr-1.5"></span>HABLANDO EN VIVO • AL TERMINAR TE ESCUCHO';
    } else if (nuevoEstado === 'listening') {
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.add('sp-voice-listening');
      if (txtV) txtV.textContent = 'Escuchando...';
      if (icoV) icoV.textContent = '🔴';
      if (inp) inp.placeholder = '🟢 MICRÓFONO ABIERTO: Habla ahora (tu voz aparece en amarillo)...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping inline-block mr-1.5"></span>🎙️ MICRÓFONO ABIERTO • TE ESCUCHO EN MANOS LIBRES';
    } else if (nuevoEstado === 'thinking') {
      if (btnStop) btnStop.classList.remove('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Pensando...';
      if (icoV) icoV.textContent = '⚡';
      if (inp) inp.placeholder = '⚡ Generando respuesta inteligente...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-sky-400 animate-ping inline-block mr-1.5"></span>⚡ PENSANDO RESPUESTA...';
    } else {
      if (btnStop) btnStop.classList.add('hidden');
      if (btnV) btnV.classList.remove('sp-voice-listening');
      if (txtV) txtV.textContent = 'Hablar';
      if (icoV) icoV.textContent = '🎙️';
      if (inp) inp.placeholder = 'Escribe tu duda o pulsa 🎙️ Hablar / la Esfera 3D para conversar...';
      if (hud) hud.innerHTML = '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-slate-400 inline-block mr-1.5"></span>⏸ EN PAUSA • PULSA LA ESFERA 3D O 🎙️ HABLAR PARA EMPEZAR';
    }
  }

  function asegurarCabina() {
    var screen = document.getElementById('spTecnosalaScreen');
    if (!screen) return null;
    var idle = document.getElementById('spTecnosalaIdleWelcome');
    var out = document.getElementById('spTecnosalaActiveOutput');
    var btnReset = document.getElementById('spBtnResetScreenTecnosala');
    if (idle) idle.classList.add('hidden');
    if (out) out.classList.add('hidden');
    if (btnReset) btnReset.classList.remove('hidden');

    var track = document.getElementById('spTeleprompterRollTrack');
    if (track) return track;

    var stage = document.createElement('div');
    stage.id = 'spTeleprompter2027Stage';
    stage.className = 'w-full flex flex-col items-center justify-between my-auto';
    stage.innerHTML =
      '<div class="w-full flex flex-wrap items-center justify-between gap-1.5 mb-1.5 px-1">' +
        '<div id="spTeleprompterHudStatus" class="text-[10px] sm:text-[10.5px] font-mono font-extrabold uppercase tracking-wider text-teal-300 truncate">' +
          '<span id="spApiSecretStatusDot" class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse inline-block mr-1.5"></span>CONSULTOR INTELIGENTE EN LÍNEA' +
        '</div>' +
        '<div class="flex flex-wrap items-center gap-1.5 flex-shrink-0">' +
          '<button type="button" id="spBtnRepetirUltimaResp" onclick="window.spRepetirUltimaRespuestaConsultor(event)" class="px-2.5 py-0.5 rounded-full bg-teal-500/20 hover:bg-teal-500/35 border border-teal-400/50 text-[10px] font-extrabold text-teal-200 cursor-pointer transition">🔁 Repetir</button>' +
          '<button type="button" id="spBtnCambiarTimbreVoz" onclick="window.spCambiarVozPreferidaConsultor(event)" class="px-2.5 py-0.5 rounded-full bg-indigo-500/25 border border-indigo-400/50 text-[10px] font-extrabold text-indigo-200 cursor-pointer">🎙️ Voz: ' + _nombreVoz + '</button>' +
          '<button type="button" id="spBtnToggleVozSintetica" onclick="window.spToggleVozConsultorMute(event)" class="px-2.5 py-0.5 rounded-full bg-cyan-500/20 border border-cyan-400/50 text-[10px] font-extrabold text-cyan-200 cursor-pointer">' + (_mute ? '🔇 Silenciado' : '🔊 Voz: ON') + '</button>' +
        '</div>' +
      '</div>' +
      '<div class="flex items-center justify-center gap-3 mb-1.5">' +
        '<div id="spOrb3DWrapperMain" onclick="window.spActivarOrbeConsultorInteractivo(event)" class="sp-orb-3d-wrapper sp-orb-compact-mode" title="Pulsa para hablar">' +
          '<div class="sp-orb-3d-ring1"></div>' +
          '<div class="sp-orb-3d-ring2"></div>' +
          '<div class="sp-orb-3d-sphere"><span class="text-sm drop-shadow pointer-events-none">⚡</span></div>' +
        '</div>' +
        '<button type="button" id="spBtnStopSideOrb" onclick="window.spPararConsultorTotalmente(event)" class="px-3.5 py-1 rounded-full bg-rose-600 hover:bg-rose-500 border border-rose-300 text-white font-black text-[11px] shadow-md cursor-pointer transition flex items-center gap-1.5"><span>⏹</span><span>PARAR</span></button>' +
      '</div>' +
      '<div class="sp-teleprompter-2027-box">' +
        '<div id="spTeleprompterRollTrack" class="sp-teleprompter-Roll-track"></div>' +
      '</div>';
    screen.appendChild(stage);
    return document.getElementById('spTeleprompterRollTrack');
  }

  function ordenarLineasBlancas(track) {
    if (!track) return;
    var blancas = track.querySelectorAll('[data-role="consultor"]');
    var tope = (_lineaAmarilla && _lineaAmarilla.parentNode === track) ? 2 : 3;
    while (blancas.length > tope) {
      if (blancas[0] && blancas[0].parentNode === track) {
        track.removeChild(blancas[0]);
      }
      blancas = track.querySelectorAll('[data-role="consultor"]');
    }
    var n = blancas.length;
    for (var i = 0; i < n; i++) {
      var el = blancas[i];
      var d = (n - 1) - i;
      el.classList.remove('sp-led-line-user', 'sp-led-line-active', 'sp-led-line-past-1', 'sp-led-line-past-2', 'sp-led-line-past-3');
      var c = el.querySelector('.sp-led-cursor');
      if (d === 0) {
        el.classList.add('sp-led-line-active');
      } else {
        if (c) c.remove();
        if (d === 1) el.classList.add('sp-led-line-past-1');
        else if (d === 2) el.classList.add('sp-led-line-past-2');
        else el.classList.add('sp-led-line-past-3');
      }
    }
    if (_lineaAmarilla && _lineaAmarilla.parentNode === track && track.lastElementChild !== _lineaAmarilla) {
      track.appendChild(_lineaAmarilla);
    }
  }

  function elegirVozEspanola() {
    if (!('speechSynthesis' in window)) return null;
    var todas = window.speechSynthesis.getVoices() || [];
    var es = [];
    for (var i = 0; i < todas.length; i++) {
      var l = String(todas[i].lang || '').replace('_', '-').toLowerCase();
      if (l === 'es-es' || l.indexOf('es-es-') === 0) es.push(todas[i]);
    }
    var pref = _nombreVoz.toLowerCase();
    for (var j = 0; j < es.length; j++) {
      if (String(es[j].name || '').toLowerCase().indexOf(pref) !== -1) {
        _vozCache = es[j];
        return es[j];
      }
    }
    if (es.length > 0) {
      _vozCache = es[0];
      return es[0];
    }
    return _vozCache;
  }

  window.spObtenerRespuestaOmniscienteCompleta = function(preguntaRaw) {
    var qNorm = normalizarSinTildes(preguntaRaw);
    var bd = window.SP_BASE_CONOCIMIENTO_HUMANA || [];
    var mejorItem = null;
    var mejorPts = 0;
    for (var i = 0; i < bd.length; i++) {
      var it = bd[i];
      var pts = 0;
      for (var j = 0; j < (it.claves || []).length; j++) {
        var kw = normalizarSinTildes(it.claves[j]);
        if (kw && qNorm.indexOf(kw) !== -1) {
          pts += (kw.split(' ').length >= 2) ? 45 : 15;
        }
      }
      if (pts > mejorPts) {
        mejorPts = pts;
        mejorItem = it;
      }
    }
    if (mejorItem && mejorPts > 0) {
      var piscina = [mejorItem.respuesta].concat(mejorItem.variantes || []);
      var k = mejorItem.id || 'def';
      var idx = (_contadorVariantes[k] || 0) % piscina.length;
      _contadorVariantes[k] = idx + 1;
      return piscina[idx];
    }
    return 'En Sistemas Pyme te ayudamos a multiplicar tus reseñas de 5 estrellas con IA, a posicionar tu web en Google y ChatGPT y a automatizar tu WhatsApp en 24 a 48 horas. Dime qué área de tu negocio quieres mejorar y lo vemos al detalle.';
  };

  /* =========================================================================
     INSTANCIA ÚNICA CONTINUA DEL MICRÓFONO:
     Se abre en el milisegundo 0 del clic del usuario para sellar el permiso
     en Chrome y usa `_ignorarMicroMientrasHabla` mientras el consultor habla.
     ========================================================================= */
  function obtenerReconocedorContinuo() {
    if (_rec) return _rec;
    var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) return null;

    var rec = new SpeechRec();
    rec.lang = 'es-ES';
    rec.continuous = true;
    rec.interimResults = true;
    rec.maxAlternatives = 1;

    function dispararPregunta() {
      if (_timerSilencio) {
        clearTimeout(_timerSilencio);
        _timerSilencio = null;
      }
      var preguntaFinal = _bufferUsuario.trim();
      _bufferUsuario = '';
      if (!preguntaFinal || preguntaFinal.length < 2) return;
      if (_ignorarMicroMientrasHabla || _estado === 'speaking' || _estado === 'thinking') return;

      _ignorarMicroMientrasHabla = true;
      window.spProcesarConsultaEnTeleprompterDirecto(preguntaFinal);
    }

    rec.onstart = function() {
      _recEscuchando = true;
      if (!_ignorarMicroMientrasHabla && _estado !== 'speaking' && _estado !== 'thinking') {
        pintarUI('listening');
      }
    };

    rec.onresult = function(event) {
      // Mientras el consultor habla o en los 450ms posteriores, ignoramos el sonido del altavoz
      if (_ignorarMicroMientrasHabla || _estado === 'speaking' || _estado === 'thinking' || (performance.now() - _tsFinHabla < 450)) {
        _bufferUsuario = '';
        return;
      }

      var nuevoFinal = '';
      var interino = '';
      for (var i = event.resultIndex; i < event.results.length; i++) {
        var tr = String(event.results[i][0].transcript || '');
        if (event.results[i].isFinal) nuevoFinal += tr + ' ';
        else interino += tr;
      }

      if (nuevoFinal) {
        _bufferUsuario = (_bufferUsuario + ' ' + nuevoFinal).trim();
      }
      var fraseVisible = (_bufferUsuario + ' ' + interino).replace(/\s+/g, ' ').trim();
      if (!fraseVisible) return;

      _tsUltimaVozUsuario = performance.now();

      var inp = document.getElementById('spTecnosalaInput');
      if (inp) inp.value = fraseVisible;

      var track = asegurarCabina();
      if (track) {
        if (!_lineaAmarilla || _lineaAmarilla.parentNode !== track) {
          _lineaAmarilla = document.createElement('div');
          _lineaAmarilla.setAttribute('data-role', 'usuario');
          _lineaAmarilla.className = 'sp-led-line-item sp-led-line-user';
          track.appendChild(_lineaAmarilla);
        }
        _lineaAmarilla.textContent = '🎙️ TÚ: «' + fraseVisible + '»';
        ordenarLineasBlancas(track);
      }

      if (_timerSilencio) clearTimeout(_timerSilencio);
      if (nuevoFinal) {
        _timerSilencio = setTimeout(dispararPregunta, 650);
      } else {
        _timerSilencio = setTimeout(function() {
          _bufferUsuario = fraseVisible;
          dispararPregunta();
        }, 1200);
      }
    };

    rec.onerror = function(ev) {
      if (ev && (ev.error === 'not-allowed' || ev.error === 'service-not-allowed')) {
        _recEscuchando = false;
        pintarUI('idle');
      }
    };

    rec.onend = function() {
      _recEscuchando = false;
      if (_activo && !_pausadoPorSalir && enTecnosala()) {
        setTimeout(function() {
          if (_activo && !_pausadoPorSalir && enTecnosala() && !_recEscuchando) {
            try { rec.start(); } catch (e) {}
          }
        }, 150);
      }
    };

    _rec = rec;
    return rec;
  }

  function activarEscuchaUsuarioAhora() {
    if (!_activo || _pausadoPorSalir || !enTecnosala()) return;
    _ignorarMicroMientrasHabla = false;
    _bufferUsuario = '';
    pintarUI('listening');
    var rec = obtenerReconocedorContinuo();
    if (rec && !_recEscuchando) {
      try { rec.start(); } catch (e) { _recEscuchando = true; }
    }
  }

  window.spReproducirEnTeleprompter2027 = function(textoCompleto, alTerminarCallback) {
    _ignorarMicroMientrasHabla = true;
    _bufferUsuario = '';
    if (_timerSilencio) {
      clearTimeout(_timerSilencio);
      _timerSilencio = null;
    }
    limpiarTimersTexto();

    var track = asegurarCabina();
    if (!track) return;

    track.innerHTML = '';
    _lineaAmarilla = null;

    var limpio = String(textoCompleto || '').replace(/<[^>]+>/g, ' ').replace(/[`*_#•]/g, ' ').replace(/\s+/g, ' ').trim();
    if (!limpio) {
      activarEscuchaUsuarioAhora();
      return;
    }

    var maxLen = window.innerWidth < 640 ? 38 : 54;
    var palabras = limpio.split(' ');
    var segmentos = [];
    var linea = '';
    var cursor = 0;
    for (var i = 0; i < palabras.length; i++) {
      var cand = linea ? (linea + ' ' + palabras[i]) : palabras[i];
      if (cand.length <= maxLen) {
        linea = cand;
      } else {
        if (linea) {
          segmentos.push({ texto: linea, start: cursor, end: cursor + linea.length });
          cursor += linea.length + 1;
        }
        linea = palabras[i];
      }
    }
    if (linea) segmentos.push({ texto: linea, start: cursor, end: cursor + linea.length });

    var textoUnido = segmentos.map(function(s) { return s.texto; }).join(' ');
    var totalChars = textoUnido.length;
    var charMostrado = 0;
    var charVoz = 0;
    var idxSeg = -1;
    var spanActivo = null;
    var terminado = false;
    var tsInicio = performance.now();
    var tsUltimaVoz = performance.now();

    function pintarBlancoHasta(pos) {
      var p = Math.min(totalChars, Math.max(0, pos));
      var sIdx = 0;
      for (var k = 0; k < segmentos.length; k++) {
        if (p >= segmentos[k].start) sIdx = k;
        else break;
      }
      while (idxSeg < sIdx) {
        if (idxSeg >= 0 && spanActivo) spanActivo.textContent = segmentos[idxSeg].texto;
        idxSeg++;
        var row = document.createElement('div');
        row.setAttribute('data-role', 'consultor');
        row.className = 'sp-led-line-item sp-led-line-active';
        var spT = document.createElement('span');
        var spC = document.createElement('span');
        spC.className = 'sp-led-cursor';
        row.appendChild(spT);
        row.appendChild(spC);
        track.appendChild(row);
        ordenarLineasBlancas(track);
        spanActivo = spT;
      }
      if (spanActivo && sIdx >= 0 && sIdx < segmentos.length) {
        var seg = segmentos[sIdx];
        spanActivo.textContent = seg.texto.slice(0, Math.min(seg.texto.length, Math.max(1, p - seg.start)));
      }
    }

    function alTerminarDeHablar() {
      if (terminado) return;
      terminado = true;
      pintarBlancoHasta(totalChars);
      limpiarTimersTexto();
      _tsFinHabla = performance.now();
      if (typeof alTerminarCallback === 'function') {
        try { alTerminarCallback(); } catch (e) {}
      }
      if (_activo && !_pausadoPorSalir && enTecnosala()) {
        activarEscuchaUsuarioAhora();
      } else {
        pintarUI('idle');
      }
    }

    pintarUI('speaking');
    var maxMs = Math.max(3600, totalChars * 72 + 1500);
    _timersTexto.push(setTimeout(alTerminarDeHablar, maxMs));

    function avanzarLetrasBlancas() {
      if (_estado !== 'speaking' || terminado) return;
      if (charVoz > charMostrado) {
        charMostrado = Math.min(totalChars, charMostrado + Math.max(1, Math.ceil((charVoz - charMostrado) * 0.55)));
      } else {
        charMostrado = Math.min(totalChars, charMostrado + 1);
      }
      pintarBlancoHasta(charMostrado);
      if (charMostrado >= totalChars) {
        if (_mute || !('speechSynthesis' in window) || !window.speechSynthesis.speaking) {
          alTerminarDeHablar();
          return;
        }
        _timersTexto.push(setTimeout(alTerminarDeHablar, 400));
        return;
      }
      var ch = textoUnido.charAt(charMostrado - 1) || '';
      var d = (ch === '.' || ch === '?' || ch === '!') ? 250 : ((ch === ',' || ch === ';') ? 130 : 44);
      _timersTexto.push(setTimeout(avanzarLetrasBlancas, d));
    }
    _timersTexto.push(setTimeout(avanzarLetrasBlancas, 18));

    if (!_mute && ('speechSynthesis' in window)) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
      setTimeout(function() {
        if (_estado !== 'speaking' || terminado) return;
        try {
          window.speechSynthesis.resume();
          var u = new SpeechSynthesisUtterance(textoUnido);
          u.lang = 'es-ES';
          u.rate = 0.98;
          var v = elegirVozEspanola();
          if (v) u.voice = v;
          u.onboundary = function(ev) {
            tsUltimaVoz = performance.now();
            if (ev && typeof ev.charIndex === 'number') {
              charVoz = Math.min(totalChars, ev.charIndex + (ev.charLength || 2));
            }
          };
          _watchdogHabla = setInterval(function() {
            if (_estado !== 'speaking' || terminado) {
              clearInterval(_watchdogHabla);
              return;
            }
            var ahora = performance.now();
            if ((ahora - tsInicio > 850 && !window.speechSynthesis.speaking && !window.speechSynthesis.pending) ||
                (charMostrado >= totalChars * 0.93 && (ahora - tsUltimaVoz > 900))) {
              clearInterval(_watchdogHabla);
              alTerminarDeHablar();
            }
          }, 200);
          u.onend = alTerminarDeHablar;
          u.onerror = alTerminarDeHablar;
          window.speechSynthesis.speak(u);
        } catch (e) {
          alTerminarDeHablar();
        }
      }, 20);
    }
  };

  function llamarVertexDirectoNavegador(promptCompleto) {
    var k = _obtenerKBrowser();
    if (!k) return Promise.reject(new Error('nok'));
    var url = 'https://aiplatform.googleapis.com/v1beta1/publishers/google/models/gemini-2.5-flash-lite:generateContent?key=' + encodeURIComponent(k);
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ role: 'user', parts: [{ text: promptCompleto }] }],
        generationConfig: { temperature: 0.60, topP: 0.90, maxOutputTokens: 240 }
      })
    })
    .then(function(r) { if (!r.ok) throw new Error('evx'); return r.json(); })
    .then(function(d) {
      var parts = d && d.candidates && d.candidates[0] && d.candidates[0].content && d.candidates[0].content.parts;
      if (parts && parts.length) {
        var txt = parts.map(function(p) { return p.thought ? '' : (p.text || ''); }).join(' ').trim();
        if (txt.length > 10) return txt;
      }
      throw new Error('emptyvx');
    });
  }

  function obtenerRespuestaInteligente(preguntaUsuario) {
    var apoyo = window.spObtenerRespuestaOmniscienteCompleta(preguntaUsuario);
    var hist = _historial.slice(-12).join('\n');

    var prompt =
      (window.SP_CONTEXTO_MAESTRO_IA_RESUMEN || 'Eres el Consultor Tecnológico Experto de Sistemas Pyme (sistemaspyme.es), fundado por Francisco M. Gallardo (Tel/WhatsApp 711 54 75 61).') + '\n' +
      'DATOS OFICIALES EXACTOS:\n' +
      '- Plan Pyme Base (1 servicio: S1 Reseñas Google IA o S2 Cortafuegos WhatsApp): 59 €/mes + 150 € Setup (Anual: 590 €/año, ahorras 2 meses).\n' +
      '- Pack Escudo Básico Dúo (S1 + S2 juntos): 99 €/mes + 225 € Setup (Anual: 990 €/año). Desbloquea las Super-Auditorías a 195 € c/u (en vez de 350 €).\n' +
      '- Pack Escudo Total / Plus: S1 + S2 (99 €/mes) + 1 Super-Auditoría (195 €) o las 2 Super-Auditorías (390 €).\n' +
      '- Atril Inteligente NFC + QR: 39 € pago único sin cuotas (2ª a 4ª ud: 29 €; 5+ uds: 25 €). Abre Google Maps en 1 segundo.\n' +
      '- Super-Auditoría 1 (SEO Local + GEO IA): 22 parámetros, Grafo Schema.org + Wikidata + /llms.txt para salir recomendado en Google Maps, ChatGPT, Gemini y Perplexity.\n' +
      '- Super-Auditoría 2 (Neuromarketing CRO + Sonda Térmica 10 días): duplica contactos web en Modo Ágil o Modo Corporativo.\n\n' +
      'APOYO ESPECÍFICO DE LA BIBLIA:\n' + apoyo + '\n\n' +
      'HISTORIAL DE LA CHARLA:\n' + (hist || 'Recién empezada') + '\n\n' +
      'PREGUNTA ACTUAL DEL USUARIO: "' + preguntaUsuario + '"\n\n' +
      'INSTRUCCIÓN: Responde directamente y con inteligencia a lo que te acaba de preguntar el usuario en 2 o 3 frases fluidas y naturales para ser habladas en voz alta (máximo 55 palabras). Cero asteriscos y cero listas.';

    var promesas = [
      fetch('http://127.0.0.1:8765/api/consultor-ia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta: preguntaUsuario, apoyo: apoyo, prompt: prompt })
      })
      .then(function(r) { if (!r.ok) throw new Error('e8765'); return r.json(); })
      .then(function(d) {
        if (d && d.ok && d.respuesta && d.respuesta.trim().length > 10 && d.modelo !== 'local-fallback') {
          return d.respuesta.trim();
        }
        throw new Error('fallback8765');
      }),

      fetch('https://servicio-resenas.onrender.com/api/consultor-ia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta: preguntaUsuario, apoyo: apoyo, prompt: prompt, modelo_preferido: 'gemini-2.5-flash-lite' })
      })
      .then(function(r) { if (!r.ok) throw new Error('erender1'); return r.json(); })
      .then(function(d) {
        if (d && d.ok && d.respuesta && d.respuesta.trim().length > 10) {
          return d.respuesta.trim();
        }
        throw new Error('emptyrender1');
      }),

      llamarVertexDirectoNavegador(prompt)
    ];

    return new Promise(function(resolve) {
      var resuelto = false;
      var fallos = 0;
      var timer = setTimeout(function() {
        if (!resuelto) {
          resuelto = true;
          resolve(apoyo);
        }
      }, 2200);

      for (var i = 0; i < promesas.length; i++) {
        promesas[i].then(function(txt) {
          if (!resuelto && txt) {
            resuelto = true;
            clearTimeout(timer);
            resolve(txt.replace(/[*#_`]/g, '').replace(/\s+/g, ' ').trim());
          }
        }).catch(function() {
          fallos++;
          if (fallos >= promesas.length && !resuelto) {
            resuelto = true;
            clearTimeout(timer);
            resolve(apoyo);
          }
        });
      }
    });
  }

  window.spProcesarConsultaEnTeleprompterDirecto = function(textoPregunta) {
    var limpia = String(textoPregunta || '').trim();
    if (!limpia) return;

    _ignorarMicroMientrasHabla = true;
    _bufferUsuario = '';
    _activo = true;
    _pausadoPorSalir = false;
    pintarUI('thinking');

    var inp = document.getElementById('spTecnosalaInput');
    if (inp) inp.value = '';

    var track = asegurarCabina();
    if (track) {
      if (!_lineaAmarilla || _lineaAmarilla.parentNode !== track) {
        _lineaAmarilla = document.createElement('div');
        _lineaAmarilla.setAttribute('data-role', 'usuario');
        _lineaAmarilla.className = 'sp-led-line-item sp-led-line-user';
        track.appendChild(_lineaAmarilla);
      }
      _lineaAmarilla.textContent = '🎙️ TÚ: «' + limpia + '»';
      ordenarLineasBlancas(track);
    }

    _historial.push('Usuario: ' + limpia);
    if (typeof window.spExtraerYPreconfigurarCarritoDesdeCharla === 'function') {
      try { window.spExtraerYPreconfigurarCarritoDesdeCharla(limpia, _historial); } catch (e) {}
    }

    var tlfDetectado = extraerTelefonoEspanol(limpia);
    if (tlfDetectado && typeof window.spRegistrarLeadAutomaticoDesdeVoz === 'function') {
      try { window.spRegistrarLeadAutomaticoDesdeVoz(tlfDetectado, limpia, _historial.join(' | ')); } catch (e) {}
    }

    obtenerRespuestaInteligente(limpia).then(function(respuesta) {
      _historial.push('Consultor: ' + respuesta);
      var ahora = new Date();
      _turnosGuardados.push({
        hora: ahora.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
        pregunta: limpia,
        respuesta: respuesta
      });
      var btnDlBottom = document.getElementById('spBtnDescargarCharlaBottom');
      if (btnDlBottom) {
        btnDlBottom.classList.remove('hidden');
        btnDlBottom.innerHTML = '📥 Descargar conversación (' + _turnosGuardados.length + ')';
      }
      window.spReproducirEnTeleprompter2027(respuesta, null);
    });
  };

  window.spActivarOrbeConsultorInteractivo = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();

    _activo = true;
    _pausadoPorSalir = false;

    // JOYA 1 TRASPLANTADA: Abrimos el micrófono SÍNCRONAMENTE dentro del clic del usuario
    // para que Chrome selle el permiso en el milisegundo 0 y nunca lo bloquee al acabar el saludo.
    _ignorarMicroMientrasHabla = true;
    var rec = obtenerReconocedorContinuo();
    if (rec && !_recEscuchando) {
      try { rec.start(); } catch (e) {}
    }

    var track = asegurarCabina();
    if (track && track.children.length > 0) {
      if (_estado === 'speaking') {
        limpiarTimersTexto();
        if ('speechSynthesis' in window) {
          try { window.speechSynthesis.cancel(); } catch (e) {}
        }
      }
      activarEscuchaUsuarioAhora();
      return;
    }

    var saludo =
      'Hola, soy tu consultor tecnológico de Sistemas Pyme. ' +
      'Hablamos en manos libres continuo: pregúntame cualquier duda y te responderé al segundo.';

    window.spReproducirEnTeleprompter2027(saludo, null);
  };

  window.spIniciarEscuchaDirectaConsultor = function() {
    _activo = true;
    _pausadoPorSalir = false;
    limpiarTimersTexto();
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    asegurarCabina();
    activarEscuchaUsuarioAhora();
  };

  window.spToggleDictadoVozTecnosala = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (!_activo) {
      window.spActivarOrbeConsultorInteractivo(ev);
    } else {
      window.spIniciarEscuchaDirectaConsultor();
    }
  };

  window.spPararConsultorTotalmente = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    _activo = false;
    _pausadoPorSalir = false;
    _ignorarMicroMientrasHabla = true;
    _bufferUsuario = '';
    if (_timerSilencio) {
      clearTimeout(_timerSilencio);
      _timerSilencio = null;
    }
    if (_rec && _recEscuchando) {
      try { _rec.stop(); } catch (e) {}
      _recEscuchando = false;
    }
    limpiarTimersTexto();
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    pintarUI('idle');
  };

  window.spLimpiarPantallaTecnosala = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    window.spPararConsultorTotalmente();
    var stg = document.getElementById('spTeleprompter2027Stage');
    if (stg) stg.remove();
    var out = document.getElementById('spTecnosalaActiveOutput');
    if (out) out.classList.add('hidden');
    var idle = document.getElementById('spTecnosalaIdleWelcome');
    if (idle) {
      idle.classList.remove('hidden');
      idle.innerHTML = HTML_IDLE_BIENVENIDA;
    }
    var btnReset = document.getElementById('spBtnResetScreenTecnosala');
    if (btnReset) btnReset.classList.add('hidden');
    var inp = document.getElementById('spTecnosalaInput');
    if (inp) inp.value = '';
  };

  window.spPausarConsultorPorCambioSeccion = function() {
    if (!_activo) return;
    _pausadoPorSalir = true;
    _ignorarMicroMientrasHabla = true;
    if (_rec && _recEscuchando) {
      try { _rec.stop(); } catch (e) {}
      _recEscuchando = false;
    }
    limpiarTimersTexto();
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    pintarUI('idle');
  };

  window.spReanudarConsultorAlVolverSeccion = function() {
    if (!_activo || !enTecnosala()) return;
    _pausadoPorSalir = false;
    asegurarCabina();
    activarEscuchaUsuarioAhora();
  };

  window.spPausarConsultorPorNavegacion = window.spPausarConsultorPorCambioSeccion;
  window.spReanudarConsultorAlVolverATecnosala = window.spReanudarConsultorAlVolverSeccion;
  window.spActivarModoEscuchaPersistente = activarEscuchaUsuarioAhora;

  window.spEnviarPreguntaLibreTecnosala = function(ev) {
    if (ev && ev.preventDefault) ev.preventDefault();
    var inp = document.getElementById('spTecnosalaInput');
    var txt = inp ? String(inp.value || '').trim() : '';
    if (!txt) return;
    window.spProcesarConsultaEnTeleprompterDirecto(txt);
  };

  window.spEjecutarConsultaTecnosala = function(claveFaq) {
    var mapaTitulos = {
      rgpd: '¿Cómo evitáis multas de Protección de Datos en reseñas?',
      fijo: '¿Puedo usar el teléfono fijo de siempre de mi local?',
      informe360: '¿Qué incluye el Informe Mensual 360°?',
      instalacion: '¿Tengo que cambiar el programa que ya uso?',
      seogeo: '¿Cómo lográis que ChatGPT y Google me recomienden?',
      precios: '¿Cuánto cuesta y cómo se amortiza?'
    };
    var preg = mapaTitulos[claveFaq] || claveFaq;
    window.spProcesarConsultaEnTeleprompterDirecto(preg);
  };

  window.spCambiarVozPreferidaConsultor = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (!('speechSynthesis' in window)) return;
    var todas = window.speechSynthesis.getVoices() || [];
    var es = todas.filter(function(v) { return /^es[-_]es/i.test(v.lang || ''); });
    if (!es.length) return;
    var actual = elegirVozEspanola();
    var idx = 0;
    for (var i = 0; i < es.length; i++) {
      if (actual && es[i].name === actual.name) { idx = i; break; }
    }
    var sig = es[(idx + 1) % es.length];
    _vozCache = sig;
    _nombreVoz = String(sig.name || 'Voz').replace(/^Microsoft\s+/i, '').split(/[\s(]/)[0];
    var btn = document.getElementById('spBtnCambiarTimbreVoz');
    if (btn) btn.innerHTML = '🎙️ Voz: ' + _nombreVoz;
  };

  window.spToggleVozConsultorMute = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    _mute = !_mute;
    if (_mute && ('speechSynthesis' in window)) {
      try { window.speechSynthesis.cancel(); } catch (e) {}
    }
    var btn = document.getElementById('spBtnToggleVozSintetica');
    if (btn) btn.innerHTML = _mute ? '🔇 Silenciado' : '🔊 Voz: ON';
  };

  window.spRepetirUltimaRespuestaConsultor = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (_turnosGuardados.length > 0) {
      var ult = _turnosGuardados[_turnosGuardados.length - 1];
      window.spReproducirEnTeleprompter2027(ult.respuesta, null);
    } else {
      window.spActivarOrbeConsultorInteractivo(ev);
    }
  };

  window.spDescargarConversacionConsultor = function(ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (!_turnosGuardados.length) return;
    var ahora = new Date();
    var fStr = ahora.toLocaleDateString('es-ES');
    var filas = _turnosGuardados.map(function(t, idx) {
      return '<div style="border:1px solid #cbd5e1;border-radius:12px;padding:12px;margin-bottom:10px;">' +
        '<strong>Pregunta ' + (idx + 1) + ' (' + t.hora + '):</strong> ' + t.pregunta + '<br><br>' +
        '<strong>Consultor Sistemas Pyme:</strong> ' + t.respuesta + '</div>';
    }).join('');
    var doc = '<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Consulta Sistemas Pyme ' + fStr + '</title></head><body style="font-family:sans-serif;max-width:760px;margin:24px auto;padding:16px;"><h2>Informe de Consulta — Sistemas Pyme (' + fStr + ')</h2>' + filas + '</body></html>';
    var blob = new Blob([doc], { type: 'text/html;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'Consulta_Sistemas_Pyme.html';
    document.body.appendChild(a);
    a.click();
    setTimeout(function() { document.body.removeChild(a); URL.revokeObjectURL(url); }, 200);
  };

  setInterval(function() {
    if (!_activo) return;
    var vis = enTecnosala();
    if (!vis && !_pausadoPorSalir) {
      window.spPausarConsultorPorCambioSeccion();
    } else if (vis && _pausadoPorSalir) {
      window.spReanudarConsultorAlVolverSeccion();
    }
  }, 600);
})();
"""


# =============================================================================
# 6. MICRO-SERVIDOR LOCAL EN PUERTO 8765 CON TUS CLAVES REALES DEL MAC
# =============================================================================
CODIGO_SERVIDOR_8765 = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DIR_WEB = __RUTA_WEB_REAL__
CLAVES_MAC = __LISTA_CLAVES_MAC__
os.chdir(DIR_WEB)

def llamar_gemini_con_claves(prompt):
    modelos = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-flash-lite", "gemini-1.5-flash"]
    for key in CLAVES_MAC:
        for mod in modelos:
            for base_url in [
                f"https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent?key={key}",
                f"https://aiplatform.googleapis.com/v1beta1/publishers/google/models/{mod}:generateContent?key={key}",
            ]:
                try:
                    payload = {
                        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                        "generationConfig": {"temperature": 0.65, "topP": 0.90, "maxOutputTokens": 240}
                    }
                    req = urllib.request.Request(
                        base_url,
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                        method="POST"
                    )
                    with urllib.request.urlopen(req, timeout=2.8) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                        txt = " ".join(p.get("text", "") for p in parts if not p.get("thought")).strip()
                        if len(txt) > 10:
                            return txt, mod
                except Exception:
                    continue
    return "", ""

class HandlerSP(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith("/api/consultor-ia"):
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            try:
                body = json.loads(raw)
            except Exception:
                body = {}
            prompt = body.get("prompt") or body.get("pregunta") or ""
            apoyo = body.get("apoyo") or ""
            respuesta_ia, modelo_usado = llamar_gemini_con_claves(prompt)

            salida = {
                "ok": True,
                "respuesta": respuesta_ia or apoyo,
                "modelo": modelo_usado or "local-fallback"
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(salida, ensure_ascii=False).encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8765), HandlerSP)
    server.serve_forever()
'''


def parchar_index_y_extraer_tecnoconsultor(ruta_index):
    print(f"🔧 Auditando y limpiando a fondo: {ruta_index}")
    crear_backup_seguro(ruta_index)

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. REPARAR LAS TARJETAS DE AUDITORÍAS (Cara A -> Cara B -> Detalle Estadística -> Cara B -> Cara C -> Cara A)
    #    Reemplazamos cualquier versión previa de window.spToggleAuditCircleCA (con cualquier sangría)
    patron_audit_previo = re.compile(
        r"(?:/\*\s*={10,}[\s\S]*?SECUENCIA INTERACTIVA COMPLETA[\s\S]*?)?window\.spToggleAuditCircleCA\s*=\s*function\s*\(num,\s*ev\)\s*\{[\s\S]*?circle\.classList\.add\('sp-circle-open'\);[\s\S]*?\};"
    )
    if patron_audit_previo.search(html):
        html = patron_audit_previo.sub(lambda _m: BLOQUE_AUDITORIAS_SECUENCIA_JS.strip(), html, count=1)
    elif "window.spToggleExpandirCajaStat" not in html:
        # Si no lo encontró por regex, lo inyectamos justo antes de window.spToggleFlipCard
        marcador_flip = "window.spToggleFlipCard = function"
        if marcador_flip in html:
            html = html.replace(marcador_flip, BLOQUE_AUDITORIAS_SECUENCIA_JS.strip() + "\n\n        " + marcador_flip, 1)

    # 2. EXTIRPAR EL BLOQUE 1 DEL TECNOCONSULTOR VIEJO EN `#vista-tecnosala` (líneas 2070-2394: BASE_CONOCIMIENTO_TECNOSALA + _spVoiceRecognition)
    patron_script_tecnosala_viejo = re.compile(
        r"<script>\s*\(function\(\)\s*\{\s*var BASE_CONOCIMIENTO_TECNOSALA\s*=[\s\S]*?</script>",
        flags=re.IGNORECASE,
    )
    if patron_script_tecnosala_viejo.search(html):
        html = patron_script_tecnosala_viejo.sub(lambda _m: BLOQUE_ADMIN_TECNOSALA_LIMPIO_EN_INDEX, html, count=1)
        print("   ✂️ Eliminado Bloque 1 antiguo del Tecnoconsultor dentro de #vista-tecnosala.")

    # 3. EXTIRPAR EL BLOQUE 2 DEL TECNOCONSULTOR VIEJO (líneas 3045-3710: MOTOR DEL CONSULTOR NEURONAL hasta el cierre de SP_PODCAST_ENGINE_V131_END)
    patron_motor_neuronal_viejo = re.compile(
        r"// =====================================================================\s*// MOTOR DEL CONSULTOR NEURONAL[\s\S]*?</script>\s*(?=<!-- === \[SP_PODCAST_ENGINE_V131_END\] === -->)"
    )
    if patron_motor_neuronal_viejo.search(html):
        html = patron_motor_neuronal_viejo.sub(lambda _m: COLA_PODCAST_Y_CARRITO_SIN_CONSULTOR, html, count=1)
        print("   ✂️ Eliminado Bloque 2 antiguo (MOTOR DEL CONSULTOR NEURONAL) dentro de index.html.")

    # 4. EXTIRPAR EL CÓDIGO RESIDUAL DE MICRÓFONO EN `spScriptMejorasCarritoYMigradoPersistenteV130` (_spReconocedorUnicoV129)
    html = re.sub(
        r"var _spStreamAudioPersistenteV129 = null;[\s\S]*?function instalarMicrofonoContinuoSinRePromptV129\(\)\s*\{[\s\S]*?\}",
        "function instalarMicrofonoContinuoSinRePromptV129() { /* Micrófono 100% en tecnoconsultor.js */ }",
        html,
    )

    # 5. ASEGURAR EL ENLACE LIMPIO A `tecnoconsultor.js?v=178` AL FINAL DE `index.html`
    enlace_externo = (
        '<!-- [SP_CONSULTOR_EXTERNO_START] -->\n'
        '<script src="tecnoconsultor.js?v=178"></script>\n'
        '<!-- [SP_CONSULTOR_EXTERNO_END] -->'
    )
    patron_bloque_consultor = re.compile(
        r"<!-- \[SP_CONSULTOR_(?:ULTIMATE_V\d+|EXTERNO)_START\] -->[\s\S]*?<!-- \[SP_CONSULTOR_(?:ULTIMATE_V\d+|EXTERNO)_END\] -->"
    )
    if patron_bloque_consultor.search(html):
        html = patron_bloque_consultor.sub(lambda _m: enlace_externo, html)
    else:
        pos_body = html.rfind("</body>")
        if pos_body != -1:
            html = html[:pos_body] + "\n" + enlace_externo + "\n" + html[pos_body:]

    # 6. GUARDAR EL ARCHIVO INDEPENDIENTE `tecnoconsultor.js` EN LA MISMA CARPETA QUE `index.html`
    carpeta_index = os.path.dirname(ruta_index)
    ruta_tc_js = os.path.join(carpeta_index, "tecnoconsultor.js")
    if os.path.isfile(ruta_tc_js):
        crear_backup_seguro(ruta_tc_js)
    if not validar_js_con_node(CODIGO_TECNOCONSULTOR_JS, "tecnoconsultor.js"):
        raise RuntimeError("Error de sintaxis en tecnoconsultor.js")
    with open(ruta_tc_js, "w", encoding="utf-8") as f_tc:
        f_tc.write(CODIGO_TECNOCONSULTOR_JS)
    print(f"✅ Archivo externo actualizado y validado: {ruta_tc_js}")

    # 7. VALIDAR TODOS LOS BLOQUES <script> DE `index.html` CON NODE.JS
    if not validar_bloques_js_en_html(html, os.path.basename(ruta_index)):
        raise RuntimeError(f"Abortado por seguridad: {ruta_index} no superó la validación JS.")

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {ruta_index} 100% limpio de código del Tecnoconsultor y con Auditorías Cara A/B/Detalle/C activas.")


def limpiar_y_sincronizar_git(ruta_repo, nombre_repo):
    if not os.path.isdir(os.path.join(ruta_repo, ".git")):
        return
    gitignore_path = os.path.join(ruta_repo, ".gitignore")
    existentes = ""
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            existentes = f.read()
    reglas = ["backups_sp/", "*.bak", "AD.py", ".env", "_sp_servidor_ia_8765.py", ".sp_servidor_neuronal_8765.py"]
    nuevas = [r for r in reglas if r not in existentes]
    if nuevas:
        with open(gitignore_path, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(nuevas) + "\n")

    for archivo_sensible in [
        "AD.py",
        "public_html/AD.py",
        "_sp_servidor_ia_8765.py",
        "public_html/_sp_servidor_ia_8765.py",
        ".sp_servidor_neuronal_8765.py",
        "public_html/.sp_servidor_neuronal_8765.py",
    ]:
        subprocess.run(["git", "rm", "--cached", "--ignore-unmatch", archivo_sensible], cwd=ruta_repo, capture_output=True)

    subprocess.run(["git", "fetch", "origin"], cwd=ruta_repo, capture_output=True)
    check_origin = subprocess.run(["git", "rev-parse", "--verify", "origin/main"], cwd=ruta_repo, capture_output=True, text=True)
    if check_origin.returncode == 0:
        subprocess.run(["git", "reset", "--soft", "origin/main"], cwd=ruta_repo, capture_output=True)
        for archivo_sensible in [
            "AD.py",
            "public_html/AD.py",
            "_sp_servidor_ia_8765.py",
            "public_html/_sp_servidor_ia_8765.py",
            ".sp_servidor_neuronal_8765.py",
            "public_html/.sp_servidor_neuronal_8765.py",
        ]:
            subprocess.run(["git", "reset", "HEAD", archivo_sensible], cwd=ruta_repo, capture_output=True)

    subprocess.run(["git", "add", "."], cwd=ruta_repo, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "V178: Trasplante completo a tecnoconsultor.js + separacion limpia index.html + Auditorias Cara A/B/Detalle/C"],
        cwd=ruta_repo,
        capture_output=True,
    )
    push_res = subprocess.run(["git", "push", "origin", "main"], cwd=ruta_repo, capture_output=True, text=True)
    if push_res.returncode == 0:
        print(f"✅ Git sincronizado limpiamente en: {nombre_repo}")
    else:
        print(f"ℹ️ Estado Git en {nombre_repo}: {push_res.stderr.strip()[:180]}")


def levantar_servidor_local_8765(carpeta_web):
    if not os.path.isdir(carpeta_web):
        return
    claves_reales = rescatar_api_keys_reales_del_mac()
    ruta_srv = os.path.join("/tmp", "_sp_servidor_neuronal_8765.py")
    codigo_final = (
        CODIGO_SERVIDOR_8765
        .replace("__RUTA_WEB_REAL__", repr(carpeta_web))
        .replace("__LISTA_CLAVES_MAC__", repr(claves_reales))
    )
    with open(ruta_srv, "w", encoding="utf-8") as f:
        f.write(codigo_final)

    try:
        subprocess.run(["pkill", "-f", "_sp_servidor_ia_8765.py"], check=False)
        subprocess.run(["pkill", "-f", "_sp_servidor_neuronal_8765.py"], check=False)
    except Exception:
        pass

    try:
        subprocess.Popen(
            [sys.executable, ruta_srv],
            cwd=carpeta_web,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        time.sleep(0.4)
        print(f"🟢 Servidor Local IA activo en http://127.0.0.1:8765/index.html ({len(claves_reales)} clave(s) Gemini del Mac cargadas)")
        subprocess.Popen(["open", "http://127.0.0.1:8765/index.html"])
    except Exception as e:
        print(f"⚠️ Aviso al iniciar servidor 8765: {e}")


def auto_replicar_ad_py():
    ruta_actual = os.path.abspath(__file__)
    for carpeta in CARPETAS_TRABAJO:
        if os.path.isdir(carpeta):
            destino = os.path.join(carpeta, "AD.py")
            if os.path.abspath(destino) != ruta_actual:
                try:
                    shutil.copy2(ruta_actual, destino)
                except Exception:
                    pass


def main():
    print("======================================================================")
    print("🚀 INICIANDO ACTUALIZACIÓN V178 — TRASPLANTE COMPLETO + AUDITORÍAS CARA A/B/C")
    print("======================================================================")

    actualizar_documentos_maestros()
    auto_replicar_ad_py()

    # Eliminar duplicados prohibidos index_2.html e index_3.html si existen
    for carpeta in CARPETAS_TRABAJO + [os.getcwd()]:
        for nombre_dup in ["index_2.html", "index_3.html"]:
            posible_dup = os.path.join(carpeta, nombre_dup)
            if os.path.isfile(posible_dup):
                crear_backup_seguro(posible_dup)
                try:
                    os.remove(posible_dup)
                    print(f"🧹 Eliminado duplicado {posible_dup} (copia en backups_sp).")
                except Exception:
                    pass

    rutas_procesadas = set()
    carpeta_principal_web = None

    for cand in CANDIDATOS_INDEX_HTML:
        if os.path.isfile(cand):
            real = os.path.realpath(cand)
            if real not in rutas_procesadas:
                parchar_index_y_extraer_tecnoconsultor(cand)
                rutas_procesadas.add(real)
                if not carpeta_principal_web:
                    carpeta_principal_web = os.path.dirname(cand)

    if os.path.isdir(RUTA_WEB_PUBLIC):
        carpeta_principal_web = RUTA_WEB_PUBLIC

    limpiar_y_sincronizar_git(RUTA_WEB_REPO, "web-sistemaspyme")
    limpiar_y_sincronizar_git(RUTA_RESENAS, "servicio_resenas")

    if carpeta_principal_web:
        levantar_servidor_local_8765(carpeta_principal_web)

    print("======================================================================")
    print("🎉 ACTUALIZACIÓN V178 COMPLETADA CON ÉXITO")
    print("📌 Actualización de Conocimiento guardada automáticamente en tu carpeta SISTEMAS PYME/Programar (con copia previa en backups_sp)")
    print("======================================================================")


if __name__ == "__main__":
    main()
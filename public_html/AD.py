import os
import shutil
import re
from datetime import datetime


def localizar_directorio_public_html():
    """
    Localiza la carpeta raíz public_html en el Escritorio de Francisco.
    """
    home = os.path.expanduser("~")
    rutas_directas = [
        os.path.join(home, "Desktop", "SISTEMAS PYME", "Web", "web-sistemaspyme", "public_html"),
        os.path.join(home, "Escritorio", "SISTEMAS PYME", "Web", "web-sistemaspyme", "public_html"),
        os.path.abspath("."),
        os.path.abspath("public_html")
    ]
    for r in rutas_directas:
        if os.path.isdir(r) and os.path.isfile(os.path.join(r, "index.html")):
            return r

    rutas_escritorio = [
        os.path.join(home, "Desktop"),
        os.path.join(home, "Escritorio")
    ]
    carpetas_ignorar = {"backups_sp", "Backups", "backups", ".git", "node_modules", "__pycache__", ".venv", "venv"}

    for escritorio in rutas_escritorio:
        if not os.path.isdir(escritorio):
            continue
        for raiz, dirs, archivos in os.walk(escritorio):
            dirs[:] = [d for d in dirs if d not in carpetas_ignorar]
            if "index.html" in archivos and "public_html" in raiz:
                return raiz

    return None


def obtener_backup_mas_antiguo_limpio(carpeta_backups, rel_path):
    """
    Busca el primer backup creado en backups_sp para ese documento (antes de las pruebas de hoy)
    para partir de un HTML 100% limpio y sin deformaciones previas.
    """
    if not os.path.isdir(carpeta_backups):
        return None
    prefijo = f"{rel_path}.backup_"
    candidatos = []
    for nombre in os.listdir(carpeta_backups):
        if nombre.startswith(prefijo):
            ruta_b = os.path.join(carpeta_backups, nombre)
            if os.path.isfile(ruta_b):
                candidatos.append(ruta_b)
    if not candidatos:
        return None
    candidatos.sort()  # El más antiguo por timestamp YYYYMMDD_HHMMSS
    return candidatos[0]


BLOQUE_AUTOENCUADRE_TABLAS_INTACTAS = """<!-- [SP_AUTO_FIT_MOBILE_START] Autoencuadre Directo + Tablas Completas sin Recortes -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes, maximum-scale=5.0" id="sp-dynamic-viewport">
<style id="sp-direct-autofit-css">
  @media screen {
    html, body {
      margin: 0 !important;
      padding: 8px 0 24px 0 !important;
      overflow-x: visible !important;
      -webkit-text-size-adjust: 100% !important;
    }
    /* Evitar que ningún contenedor recorte trozos de tablas o de la Vía 2 */
    .sheet, .page, .a4-page, .a5-page, .dossier-page, .magazine-page {
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      overflow: visible !important;
      margin-left: auto !important;
      margin-right: auto !important;
    }
    .pricing-table-box, .table-box, .table-container, .via-card, .modalidad-box, section, article, div {
      overflow: visible !important;
      max-height: none !important;
    }
    table {
      width: 100% !important;
      max-width: 100% !important;
      border-collapse: collapse !important;
      table-layout: auto !important;
    }
    th, td {
      word-break: normal !important;
      overflow-wrap: break-word !important;
    }
  }
</style>
<script id="sp-auto-fit-mobile">
(function() {
  function ajustarDocumentoYTablas() {
    var hojas = document.querySelectorAll('.sheet, .page, .a4-page, .a5-page, .dossier-page, .magazine-page');
    var contenedorPrincipal = hojas.length ? hojas[0] : document.body.firstElementChild;
    if (!contenedorPrincipal) return;

    /* 1. Aumentar de forma segura la letra de los textos generales (+22%), pero en tablas densas (+8%) para que no rompan ni desborden ninguna columna */
    if (!document.body.dataset.spFontAdjusted) {
      document.body.dataset.spFontAdjusted = '1';
      var contenedores = hojas.length ? hojas : [document.body];
      contenedores.forEach(function(hoja) {
        var elementos = hoja.querySelectorAll('*');
        var cambios = [];
        elementos.forEach(function(el) {
          if (el.children.length === 0 || el.tagName === 'P' || el.tagName === 'TD' || el.tagName === 'TH' || el.tagName === 'LI' || el.tagName === 'SPAN' || el.tagName === 'STRONG') {
            var cs = window.getComputedStyle(el);
            var fs = parseFloat(cs.fontSize);
            if (fs && fs > 0 && fs < 14) {
              var dentroDeTabla = !!el.closest('table');
              var factor = dentroDeTabla ? 1.08 : 1.20;
              var tope = dentroDeTabla ? 11.5 : 15.0;
              var nuevoFs = Math.min(tope, Math.round(fs * factor * 10) / 10);
              cambios.push({ el: el, size: nuevoFs, enTabla: dentroDeTabla });
            }
          }
        });
        cambios.forEach(function(item) {
          item.el.style.fontSize = item.size + 'px';
          if (!item.enTabla) {
            item.el.style.lineHeight = '1.26';
          }
        });
      });
    }

    /* 2. Calcular el ancho real máximo (incluyendo cualquier tabla ancha como la de desembolso.html o Cara B de tarifas.html) */
    var maxAncho = contenedorPrincipal.scrollWidth || contenedorPrincipal.offsetWidth || 600;
    hojas.forEach(function(h) {
      if (h.scrollWidth > maxAncho) maxAncho = h.scrollWidth;
      if (h.offsetWidth > maxAncho) maxAncho = h.offsetWidth;
    });
    document.querySelectorAll('table').forEach(function(t) {
      if (t.scrollWidth + 24 > maxAncho) maxAncho = t.scrollWidth + 24;
    });

    /* 3. Fijar el viewport del móvil al ancho real del documento + 24px de margen para que se autoencuadre entero sin cortar ningún borde */
    var vp = document.getElementById('sp-dynamic-viewport') || document.querySelector('meta[name="viewport"]');
    if (vp) {
      var anchoViewport = Math.max(580, maxAncho + 24);
      vp.setAttribute('content', 'width=' + anchoViewport + ', user-scalable=yes, maximum-scale=5.0');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ajustarDocumentoYTablas);
  } else {
    ajustarDocumentoYTablas();
  }
  window.addEventListener('load', ajustarDocumentoYTablas);
})();
</script>
<!-- [SP_AUTO_FIT_MOBILE_END] -->"""


def es_documento_tarjeton_o_dossier(ruta_archivo, contenido):
    nombre = os.path.basename(ruta_archivo).lower()
    if nombre in ("index.html", "tarjeta.html"):
        return False
    indicadores = (
        'class="sheet"',
        "class='sheet'",
        'class="page"',
        'class="a4-page"',
        "size: A5",
        "size: A4",
        "148mm",
        "210mm",
        "297mm",
        "tarjeton",
        "catalogo",
        "tarifas",
        "setup",
        "desembolso",
        "magazine"
    )
    contenido_low = contenido.lower()
    return (
        any(ind.lower() in contenido_low for ind in indicadores)
        or ("documentos" in ruta_archivo.lower())
        or ("articulos" in ruta_archivo.lower())
    )


def ejecutar_actualizador():
    print("=" * 80)
    print("🔎 ACTUALIZADOR INTERACTIVO SISTEMAS PYME (AD.py — Reparación Tablas Tarifas y Desembolso)")
    print("=" * 80)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ ERROR: No se encontró la carpeta 'public_html' en el Escritorio.")
        return

    print(f"📂 Carpeta raíz localizada en: {dir_raiz}")

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

    carpetas_ignorar = {"backups_sp", "Backups", "backups", ".git", "node_modules", "__pycache__"}
    archivos_actualizados = []

    for raiz, dirs, archivos in os.walk(dir_raiz):
        dirs[:] = [d for d in dirs if d not in carpetas_ignorar]
        for arch in archivos:
            if not arch.lower().endswith(".html"):
                continue
            ruta_completa = os.path.join(raiz, arch)
            try:
                with open(ruta_completa, "r", encoding="utf-8", errors="ignore") as f:
                    contenido_actual = f.read()
            except Exception as e:
                print(f"⚠️ No se pudo leer {ruta_completa}: {e}")
                continue

            if not es_documento_tarjeton_o_dossier(ruta_completa, contenido_actual):
                continue

            rel_path = os.path.relpath(ruta_completa, dir_raiz).replace(os.sep, "_")

            # Si existe el primer backup limpio en backups_sp, restauramos su base para eliminar cualquier residuo de pruebas anteriores
            primer_backup = obtener_backup_mas_antiguo_limpio(carpeta_backups, rel_path)
            if primer_backup:
                try:
                    with open(primer_backup, "r", encoding="utf-8", errors="ignore") as fb:
                        contenido_base = fb.read()
                except Exception:
                    contenido_base = contenido_actual
            else:
                contenido_base = contenido_actual

            # Guardar backup del estado actual
            nombre_backup = f"{rel_path}.backup_{marca_tiempo}"
            ruta_backup = os.path.join(carpeta_backups, nombre_backup)
            shutil.copy2(ruta_completa, ruta_backup)

            # 1. Limpiar cualquier bloque o clase inyectada anteriormente
            contenido_nuevo = re.sub(
                r'<!-- \[SP_AUTO_FIT_MOBILE_START\][\s\S]*?<!-- \[SP_AUTO_FIT_MOBILE_END\] -->',
                '',
                contenido_base
            )
            contenido_nuevo = contenido_nuevo.replace("sp-reading-mode", "").replace("sp-reading-xl", "").replace("sp-print-preview", "")

            # 2. Quitar meta viewport previo para poner el dinámico que mide también el ancho real de las tablas
            contenido_nuevo = re.sub(
                r'<meta\s+name=["\']viewport["\'][^>]*>\s*',
                '',
                contenido_nuevo,
                flags=re.IGNORECASE
            )

            # 3. Inyectar el nuevo autoencuadre con protección de tablas
            if "</head>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</head>", BLOQUE_AUTOENCUADRE_TABLAS_INTACTAS + "\n</head>", 1)
            elif "</body>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</body>", BLOQUE_AUTOENCUADRE_TABLAS_INTACTAS + "\n</body>", 1)
            else:
                contenido_nuevo += "\n" + BLOQUE_AUTOENCUADRE_TABLAS_INTACTAS

            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(contenido_nuevo)

            archivos_actualizados.append(os.path.relpath(ruta_completa, dir_raiz))
            print(f"   ✔ Restaurada base original + Autoencuadre de tablas completas en: {os.path.relpath(ruta_completa, dir_raiz)}")

    print("\n" + "=" * 80)
    print(f"🎉 PROCESO COMPLETADO: {len(archivos_actualizados)} documentos reparados y autoencuadrados.")
    print(f"📦 Copias de seguridad en: {carpeta_backups}")
    print("=" * 80)


if __name__ == "__main__":
    ejecutar_actualizador()
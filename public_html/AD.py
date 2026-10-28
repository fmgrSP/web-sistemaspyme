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


BLOQUE_AUTOENCUADRE_DIRECTO = """<!-- [SP_AUTO_FIT_MOBILE_START] Autoencuadre Directo + Letra Más Grande -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes" id="sp-dynamic-viewport">
<style id="sp-direct-autofit-css">
  @media screen {
    html, body {
      margin: 0 !important;
      padding: 0 !important;
      width: 100% !important;
      overflow-x: hidden !important;
      -webkit-text-size-adjust: 100% !important;
    }
    /* Permitir que cada hoja crezca en altura en pantalla para albergar la letra más grande sin cortar nada */
    .sheet, .page, .a4-page, .a5-page, .dossier-page, .magazine-page {
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      overflow: visible !important;
      margin-left: auto !important;
      margin-right: auto !important;
    }
  }
</style>
<script id="sp-auto-fit-mobile">
(function() {
  function aplicarAutoencuadreYLetraGrande() {
    var hojas = document.querySelectorAll('.sheet, .page, .a4-page, .a5-page, .dossier-page, .magazine-page');
    if (!hojas.length) return;

    /* 1. Agrandar proporcionalmente todas las letras del documento en pantalla (+35%) una sola vez */
    if (!document.body.dataset.spFontBoosted) {
      document.body.dataset.spFontBoosted = '1';
      hojas.forEach(function(hoja) {
        var elementos = hoja.querySelectorAll('*');
        var cambios = [];
        elementos.forEach(function(el) {
          if (el.children.length === 0 || el.tagName === 'P' || el.tagName === 'TD' || el.tagName === 'TH' || el.tagName === 'LI' || el.tagName === 'SPAN' || el.tagName === 'STRONG' || /^H[1-6]$/.test(el.tagName)) {
            var cs = window.getComputedStyle(el);
            var fs = parseFloat(cs.fontSize);
            if (fs && fs > 0 && fs < 17) {
              var nuevoFs = Math.min(18, Math.round(fs * 1.32 * 10) / 10);
              cambios.push({ el: el, size: nuevoFs });
            }
          }
        });
        cambios.forEach(function(item) {
          item.el.style.fontSize = item.size + 'px';
          item.el.style.lineHeight = '1.28';
        });
      });
    }

    /* 2. Autoencuadrar el documento exactamente al ancho de la pantalla del móvil */
    var primeraHoja = hojas[0];
    var anchoHoja = primeraHoja.offsetWidth || 560;
    var vp = document.getElementById('sp-dynamic-viewport') || document.querySelector('meta[name="viewport"]');

    if (vp && window.screen && window.screen.width < 820) {
      var anchoObjetivo = anchoHoja + 16;
      vp.setAttribute('content', 'width=' + anchoObjetivo + ', user-scalable=yes, maximum-scale=5.0');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', aplicarAutoencuadreYLetraGrande);
  } else {
    aplicarAutoencuadreYLetraGrande();
  }
  window.addEventListener('load', aplicarAutoencuadreYLetraGrande);
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
    print("🔎 ACTUALIZADOR INTERACTIVO SISTEMAS PYME (AD.py — Autoencuadre Directo + Letra Más Grande)")
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
                    contenido = f.read()
            except Exception as e:
                print(f"⚠️ No se pudo leer {ruta_completa}: {e}")
                continue

            if not es_documento_tarjeton_o_dossier(ruta_completa, contenido):
                continue

            rel_path = os.path.relpath(ruta_completa, dir_raiz).replace(os.sep, "_")
            nombre_backup = f"{rel_path}.backup_{marca_tiempo}"
            ruta_backup = os.path.join(carpeta_backups, nombre_backup)
            shutil.copy2(ruta_completa, ruta_backup)

            # 1. Eliminar cualquier bloque anterior inyectado
            contenido_nuevo = re.sub(
                r'<!-- \[SP_AUTO_FIT_MOBILE_START\][\s\S]*?<!-- \[SP_AUTO_FIT_MOBILE_END\] -->',
                '',
                contenido
            )

            # 2. Eliminar cualquier meta viewport previo para que no interfiera con el autoencuadre
            contenido_nuevo = re.sub(
                r'<meta\s+name=["\']viewport["\'][^>]*>\s*',
                '',
                contenido_nuevo,
                flags=re.IGNORECASE
            )

            # 3. Insertar el autoencuadre directo + aumento de letra
            if "</head>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</head>", BLOQUE_AUTOENCUADRE_DIRECTO + "\n</head>", 1)
            elif "</body>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</body>", BLOQUE_AUTOENCUADRE_DIRECTO + "\n</body>", 1)
            else:
                contenido_nuevo += "\n" + BLOQUE_AUTOENCUADRE_DIRECTO

            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(contenido_nuevo)

            archivos_actualizados.append(os.path.relpath(ruta_completa, dir_raiz))
            print(f"   ✔ Autoencuadre directo + letra más grande aplicado en: {os.path.relpath(ruta_completa, dir_raiz)}")

    print("\n" + "=" * 80)
    print(f"🎉 PROCESO COMPLETADO: {len(archivos_actualizados)} documentos actualizados.")
    print(f"📦 Copias de seguridad guardadas en: {carpeta_backups}")
    print("=" * 80)


if __name__ == "__main__":
    ejecutar_actualizador()
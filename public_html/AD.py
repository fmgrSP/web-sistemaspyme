import os
import shutil
import re
import glob
from datetime import datetime


def localizar_directorio_public_html():
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

    for esc in [os.path.join(home, "Desktop"), os.path.join(home, "Escritorio")]:
        if not os.path.isdir(esc):
            continue
        for raiz, dirs, archivos in os.walk(esc):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("backups_sp", "Backups", "node_modules")]
            if "index.html" in archivos and os.path.basename(raiz) == "public_html":
                return raiz
    return None


def obtener_magazine_original_limpio(ruta_magazine, carpeta_backups):
    """
    Recupera el contenido original íntegro de Pyme_Magazine_N1.html desde el primer backup
    o limpia cualquier script de redirección móvil que se le haya inyectado.
    """
    patron_bk = os.path.join(carpeta_backups, "Pyme_Magazine_N1.html.backup_*")
    lista_bks = sorted(glob.glob(patron_bk))

    if lista_bks:
        ruta_primer_bk = lista_bks[0]
        with open(ruta_primer_bk, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"   ✔ Restaurada base original íntegra desde: {os.path.basename(ruta_primer_bk)}")
    else:
        with open(ruta_magazine, "r", encoding="utf-8") as f:
            html = f.read()

    # Limpiamos cualquier bloque previo de redirección o parches experimentales
    html = re.sub(
        r"<!-- \[SP_AUTO_REDIRECT_MOVIL_START\] -->.*?<!-- \[SP_AUTO_REDIRECT_MOVIL_END\] -->\s*",
        "",
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r"<!-- \[SP_DESKTOP_ZOOM_READABILITY_START\] -->.*?<!-- \[SP_DESKTOP_ZOOM_READABILITY_END\] -->\s*",
        "",
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r"<!-- \[SP_MAGAZINE_AUTOFIT_START\] -->.*?<!-- \[SP_MAGAZINE_AUTOFIT_END\] -->\s*",
        "",
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r"<!-- \[SP_CLEAN_AUTOFIT_\w+_START\] -->.*?<!-- \[SP_CLEAN_AUTOFIT_\w+_END\] -->\s*",
        "",
        html,
        flags=re.DOTALL
    )
    return html


def construir_bloque_autoencuadre_y_letra_grande_magazine():
    """
    Inyecta en el artículo original Pyme_Magazine_N1.html:
    1) Autoencuadre exacto en pantallas móviles (calcula el ancho real de la hoja A4 y ajusta el viewport
       para que encaje de borde a borde sin cortarse ni requerir botones).
    2) Aumento generoso y equilibrado de la tipografía del artículo (títulos, párrafos, listas y cajas)
       liberando la altura de la hoja en pantalla para que el texto grande respire completo sin cortarse jamás.
    3) Conservación intacta del formato A4 al imprimir.
    """
    return """  <!-- [SP_MAGAZINE_AUTOFIT_START] -->
  <style id="sp-magazine-autofit-bigfont">
    @media screen {
      html, body {
        margin: 0 !important;
        padding: 12px 0 36px 0 !important;
        background-color: #0b1528 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
      }

      /* Liberamos la altura fija de las hojas A4 en pantalla para que al agrandar la letra
         se vea el 100% del artículo completo sin recortar ni ocultar una sola línea */
      .sheet, .page, .a4-page, .magazine-page, main, article.sheet {
        height: auto !important;
        min-height: 297mm !important;
        max-height: none !important;
        overflow: visible !important;
        margin-left: auto !important;
        margin-right: auto !important;
      }

      /* Aumento real y nítido de la letra sobre el diseño original del artículo */
      .sheet p, .page p, main p,
      .sheet li, .page li, main li {
        font-size: 13.8px !important;
        line-height: 1.52 !important;
      }

      .sheet h1, .page h1, main h1 {
        font-size: 26px !important;
        line-height: 1.18 !important;
      }

      .sheet h2, .page h2, main h2 {
        font-size: 18.5px !important;
        line-height: 1.25 !important;
      }

      .sheet h3, .page h3, main h3 {
        font-size: 15.5px !important;
        line-height: 1.28 !important;
      }

      .sheet h4, .page h4, main h4 {
        font-size: 14px !important;
        line-height: 1.28 !important;
      }

      /* En pantallas grandes de ordenador también ampliamos el conjunto para lectura cómoda */
      @media (min-width: 900px) {
        body {
          zoom: 1.22;
        }
      }
    }

    @media print {
      body {
        zoom: 1 !important;
        background: none !important;
        padding: 0 !important;
      }
    }
  </style>
  <script>
    (function() {
      function autoencuadrarMagazineOriginal() {
        var esMovil = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.screen.width <= 860;
        if (!esMovil) return;

        // Buscamos la hoja del artículo para medir su ancho exacto (A4 ~ 794px)
        var hoja = document.querySelector('.sheet, .page, .a4-page, .magazine-page, main') || document.body.firstElementChild;
        var anchoHoja = 815;
        if (hoja && hoja.offsetWidth > 320) {
          anchoHoja = Math.max(hoja.offsetWidth, hoja.scrollWidth) + 20;
        }

        var metaVp = document.querySelector('meta[name="viewport"]');
        if (!metaVp) {
          metaVp = document.createElement('meta');
          metaVp.name = 'viewport';
          document.head.appendChild(metaVp);
        }
        // Fija el viewport al ancho exacto del documento original para que el móvil lo autoencuadre de borde a borde
        metaVp.setAttribute('content', 'width=' + anchoHoja + ', user-scalable=yes, minimum-scale=0.25, maximum-scale=5.0');
      }

      autoencuadrarMagazineOriginal();
      window.addEventListener('DOMContentLoaded', autoencuadrarMagazineOriginal);
      window.addEventListener('load', autoencuadrarMagazineOriginal);
    })();
  </script>
  <!-- [SP_MAGAZINE_AUTOFIT_END] -->"""


def actualizar_index_para_abrir_magazine_original(ruta_index, carpeta_backups, marca):
    """
    Asegura que en index.html al pulsar en Pyme Magazine se abra SIEMPRE el artículo original
    (articulos/Pyme_Magazine_N1.html) en pestaña nueva, tanto en móvil como en ordenador,
    sin redirigir a Pyme_Magazine_N1_movil.html.
    """
    ruta_bk_idx = os.path.join(carpeta_backups, f"index.html.backup_{marca}")
    shutil.copy2(ruta_index, ruta_bk_idx)

    with open(ruta_index, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. En el enrutador de documentos de index.html, quitamos Pyme_Magazine_N1.html del mapa móvil
    html = re.sub(
        r"'articulos/Pyme_Magazine_N1\.html'\s*:\s*'articulos/Pyme_Magazine_N1_movil\.html'\s*,?",
        "",
        html
    )

    # 2. En la función abrirArticuloMagazine, abrimos siempre el original en pestaña nueva
    patron_fn_mag = re.compile(
        r"async function abrirArticuloMagazine\(e,\s*defaultHref\)\s*\{.*?\n    \}",
        re.DOTALL
    )
    nueva_fn_mag = """async function abrirArticuloMagazine(e, defaultHref) {
      if (e) e.preventDefault();
      const destino = defaultHref || 'articulos/Pyme_Magazine_N1.html';
      window.open(destino, '_blank', 'noopener');
    }"""

    if patron_fn_mag.search(html):
        html = patron_fn_mag.sub(nueva_fn_mag, html, count=1)

    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html)
    print("   ✔ 'index.html' configurado para abrir siempre el artículo original completo de Pyme Magazine.")


def ejecutar_actualizacion():
    print("=" * 86)
    print("🚀 RESTAURANDO PYME MAGAZINE N1 ORIGINAL CON AUTOENCUADRE Y LETRA GRANDE")
    print("=" * 86)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ No se encontró el directorio 'public_html' con 'index.html'.")
        return

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")

    ruta_magazine = os.path.join(dir_raiz, "articulos", "Pyme_Magazine_N1.html")
    if not os.path.isfile(ruta_magazine):
        print(f"❌ No se encontró '{ruta_magazine}'.")
        return

    # 1. Backup automático del artículo
    ruta_bk_mag = os.path.join(carpeta_backups, f"Pyme_Magazine_N1.html.backup_{marca}")
    shutil.copy2(ruta_magazine, ruta_bk_mag)
    print(f"📦 Backup creado en: {ruta_bk_mag}")

    # 2. Obtener el artículo original íntegro y sin redirecciones móviles
    html_mag = obtener_magazine_original_limpio(ruta_magazine, carpeta_backups)

    # 3. Eliminar cualquier <meta name="viewport"> viejo para que mande el autoencuadre exacto
    html_mag = re.sub(r'<meta\s+name=["\']viewport["\'][^>]*>\s*', '', html_mag, flags=re.IGNORECASE)

    # 4. Inyectar el autoencuadre + letra grande sobre el diseño original
    bloque_autofit = construir_bloque_autoencuadre_y_letra_grande_magazine()
    if "</head>" in html_mag:
        html_mag = html_mag.replace("</head>", f"{bloque_autofit}\n</head>", 1)
    else:
        html_mag = bloque_autofit + "\n" + html_mag

    with open(ruta_magazine, "w", encoding="utf-8") as f:
        f.write(html_mag)
    print("   ✔ 'articulos/Pyme_Magazine_N1.html' restaurado al diseño original íntegro con autoencuadre y letra grande.")

    # 5. Actualizar index.html para que nunca desvíe Pyme Magazine a la versión recortada
    ruta_index = os.path.join(dir_raiz, "index.html")
    actualizar_index_para_abrir_magazine_original(ruta_index, carpeta_backups, marca)

    print("=" * 86)
    print("🎉 PROCESO COMPLETADO: Pyme Magazine Nº 1 restaurado al original completo con letra grande y autoencuadre.")
    print("=" * 86)


if __name__ == "__main__":
    ejecutar_actualizacion()
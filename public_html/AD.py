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


BLOQUE_AUTOENCUADRE_MOVIL = """<!-- [SP_AUTO_FIT_MOBILE_START] Motor de Autoencuadre Inteligente en Móvil para Tarjetones A5 y Dossiers A4 -->
<script id="sp-auto-fit-mobile">
(function() {
  function ajustarViewportYEscalaTarjetones() {
    if (window.matchMedia && window.matchMedia('print').matches) return;

    var hojas = document.querySelectorAll('.sheet, .page, .a4-page, .a5-page, main.sheet, .hoja-a4, .hoja-a5');
    if (!hojas.length) return;

    // Medir el ancho real en píxeles de la primera hoja visible
    var hojaRef = null;
    for (var i = 0; i < hojas.length; i++) {
      if (hojas[i].offsetWidth > 0) {
        hojaRef = hojas[i];
        break;
      }
    }
    if (!hojaRef) hojaRef = hojas[0];

    // Ancho natural de diseño: ~560px para A5 (148mm) o ~794px para A4 (210mm)
    var anchoNatural = hojaRef.offsetWidth || 560;
    var esA4 = anchoNatural > 680;
    var anchoObjetivoViewport = esA4 ? 830 : 585;

    // 1. Configurar el meta viewport dinámico para que el navegador móvil encuadre la hoja completa de lado a lado sin cortar
    var metaVp = document.querySelector('meta[name="viewport"]');
    if (!metaVp) {
      metaVp = document.createElement('meta');
      metaVp.name = 'viewport';
      document.head.appendChild(metaVp);
    }

    var anchoPantallaFisica = Math.min(window.screen.width || 9999, window.innerWidth || 9999);
    if (anchoPantallaFisica < anchoObjetivoViewport) {
      metaVp.setAttribute('content', 'width=' + anchoObjetivoViewport + ', initial-scale=' + (anchoPantallaFisica / anchoObjetivoViewport).toFixed(4) + ', minimum-scale=0.25, maximum-scale=5.0, user-scalable=yes');
    } else {
      metaVp.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
    }

    // 2. Asegurar centrado perfecto y sin desbordamiento lateral en móvil
    document.documentElement.style.overflowX = 'hidden';
    document.body.style.overflowX = 'hidden';
    document.body.style.margin = '0 auto';
  }

  window.addEventListener('DOMContentLoaded', ajustarViewportYEscalaTarjetones);
  window.addEventListener('load', ajustarViewportYEscalaTarjetones);
  window.addEventListener('resize', ajustarViewportYEscalaTarjetones);
  window.addEventListener('orientationchange', function() {
    setTimeout(ajustarViewportYEscalaTarjetones, 150);
  });

  // Re-ajustar también si el usuario cambia de pestaña dentro de una suite de tarjetones
  document.addEventListener('click', function(e) {
    if (e.target && e.target.closest && e.target.closest('.tab-btn, button')) {
      setTimeout(ajustarViewportYEscalaTarjetones, 60);
    }
  });
})();
</script>
<style id="sp-auto-fit-mobile-css">
  @media screen and (max-width: 900px) {
    html, body {
      max-width: 100% !important;
      overflow-x: hidden !important;
      -webkit-text-size-adjust: 100%;
    }
    body {
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: flex-start !important;
      padding-left: 8px !important;
      padding-right: 8px !important;
    }
    .sheet, .page, .a4-page, .a5-page {
      margin-left: auto !important;
      margin-right: auto !important;
      flex-shrink: 0 !important;
    }
  }
</style>
<!-- [SP_AUTO_FIT_MOBILE_END] -->"""


def es_documento_tarjeton_o_dossier(ruta_archivo, contenido):
    nombre = os.path.basename(ruta_archivo).lower()
    if nombre in ("index.html", "tarjeta.html"):
        return False
    indicadores = (
        'class="sheet"',
        "class='sheet'",
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
    return any(ind.lower() in contenido_low for ind in indicadores) or ("documentos" in ruta_archivo.lower()) or ("articulos" in ruta_archivo.lower())


def ejecutar_actualizador():
    print("=" * 78)
    print("📱 ACTUALIZADOR INTERACTIVO SISTEMAS PYME (AD.py — Autoencuadre Móvil en Tarjetones)")
    print("=" * 78)

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

            # 1. Crear Backup automático en backups_sp
            rel_path = os.path.relpath(ruta_completa, dir_raiz).replace(os.sep, "_")
            nombre_backup = f"{rel_path}.backup_{marca_tiempo}"
            ruta_backup = os.path.join(carpeta_backups, nombre_backup)
            shutil.copy2(ruta_completa, ruta_backup)

            # 2. Limpiar bloque previo si ya existía
            contenido_nuevo = re.sub(
                r'<!-- \[SP_AUTO_FIT_MOBILE_START\] -->[\s\S]*?<!-- \[SP_AUTO_FIT_MOBILE_END\] -->',
                '',
                contenido
            )
            contenido_nuevo = re.sub(
                r'<!-- \[SP_AUTO_FIT_MOBILE_START\][\s\S]*?<!-- \[SP_AUTO_FIT_MOBILE_END\] -->',
                '',
                contenido_nuevo
            )

            # 3. Asegurar viewport base encuadrante según sea A4 (830) o A5 (585)
            es_a4 = ("297mm" in contenido_nuevo) or ("size: A4" in contenido_nuevo) or ("catalogo.html" in arch.lower()) or ("magazine" in arch.lower())
            ancho_vp = "830" if es_a4 else "585"

            if re.search(r'<meta\s+name=["\']viewport["\'][^>]*>', contenido_nuevo, flags=re.IGNORECASE):
                contenido_nuevo = re.sub(
                    r'<meta\s+name=["\']viewport["\'][^>]*>',
                    f'<meta name="viewport" content="width={ancho_vp}, user-scalable=yes">',
                    contenido_nuevo,
                    count=1,
                    flags=re.IGNORECASE
                )
            elif "</head>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace(
                    "</head>",
                    f'  <meta name="viewport" content="width={ancho_vp}, user-scalable=yes">\n</head>',
                    1
                )

            # 4. Inyectar motor de autoencuadre inteligente antes de </head> o </body>
            if "</head>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</head>", BLOQUE_AUTOENCUADRE_MOVIL + "\n</head>", 1)
            elif "</body>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</body>", BLOQUE_AUTOENCUADRE_MOVIL + "\n</body>", 1)
            else:
                contenido_nuevo += "\n" + BLOQUE_AUTOENCUADRE_MOVIL

            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(contenido_nuevo)

            archivos_actualizados.append((os.path.relpath(ruta_completa, dir_raiz), ruta_backup))
            print(f"   ✔ Autoencuadre móvil aplicado en: {os.path.relpath(ruta_completa, dir_raiz)}")

    print("\n" + "=" * 78)
    print(f"🎉 PROCESO COMPLETADO: {len(archivos_actualizados)} tarjetones/dossiers actualizados con autoencuadre móvil.")
    print(f"📦 Copias de seguridad guardadas en: {carpeta_backups}")
    print("=" * 78)


if __name__ == "__main__":
    ejecutar_actualizador()
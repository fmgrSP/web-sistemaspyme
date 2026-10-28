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


BLOQUE_LECTURA_COMODA_SENIOR_V2 = """<!-- [SP_AUTO_FIT_MOBILE_START] Motor v2 de Lectura Cómoda Sin Cortes + Vista A5/A4 Encuadrada -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<style id="sp-easy-read-css">
  /* ==========================================================================
     BARRA SUPERIOR INTERACTIVA DE ACCESIBILIDAD Y LECTURA
     ========================================================================== */
  @media screen {
    .sp-reader-toolbar {
      position: sticky !important;
      top: 6px !important;
      z-index: 999999 !important;
      background: rgba(11, 37, 69, 0.98) !important;
      backdrop-filter: blur(10px) !important;
      color: #ffffff !important;
      border: 2px solid #14b8a6 !important;
      border-radius: 14px !important;
      padding: 10px 14px !important;
      margin: 6px auto 14px auto !important;
      width: 96% !important;
      max-width: 860px !important;
      display: flex !important;
      flex-wrap: wrap !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 10px !important;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.55) !important;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
      box-sizing: border-box !important;
    }
    .sp-reader-toolbar-left {
      display: flex !important;
      align-items: center !important;
      gap: 8px !important;
      font-size: 13.5px !important;
      font-weight: 800 !important;
      color: #5eead4 !important;
      line-height: 1.3 !important;
    }
    .sp-reader-toolbar-btns {
      display: flex !important;
      flex-wrap: wrap !important;
      align-items: center !important;
      gap: 7px !important;
    }
    .sp-reader-btn {
      background: #0f766e !important;
      color: #ffffff !important;
      border: 1.5px solid #2dd4bf !important;
      padding: 8px 12px !important;
      border-radius: 10px !important;
      font-size: 13px !important;
      font-weight: 800 !important;
      cursor: pointer !important;
      transition: all 0.2s ease !important;
      text-decoration: none !important;
      display: inline-flex !important;
      align-items: center !important;
      gap: 5px !important;
      line-height: 1.2 !important;
    }
    .sp-reader-btn:hover {
      background: #115e59 !important;
    }
    .sp-reader-btn.active {
      background: #10b981 !important;
      color: #052e16 !important;
      border-color: #a7f3d0 !important;
      box-shadow: 0 0 14px rgba(16, 185, 129, 0.6) !important;
    }
    .sp-reader-btn.secondary {
      background: #1e293b !important;
      color: #e2e8f0 !important;
      border-color: #475569 !important;
    }
    .sp-reader-btn.print-action {
      background: #d97706 !important;
      color: #ffffff !important;
      border-color: #fbbf24 !important;
    }

    /* ==========================================================================
       MODO 1 Y 2: LECTURA CÓMODA (LETRA GRANDE Y EXTRA GRANDE SIN CORTES)
       Desbloquea todas las alturas/anchuras fijas de imprenta (mm/px) para que
       el documento fluya al 100% del ancho de la pantalla sin cortar jamás nada.
       ========================================================================== */
    html.sp-html-lectura,
    body.sp-modo-lectura {
      width: 100% !important;
      max-width: 100vw !important;
      min-width: 0 !important;
      overflow-x: hidden !important;
      margin: 0 !important;
      padding: 6px 4px 48px 4px !important;
      box-sizing: border-box !important;
    }

    /* Desbloquear cualquier contenedor de página A4/A5 */
    body.sp-modo-lectura .sheet,
    body.sp-modo-lectura .page,
    body.sp-modo-lectura .a4-page,
    body.sp-modo-lectura .a5-page,
    body.sp-modo-lectura .page-container,
    body.sp-modo-lectura .dossier-page,
    body.sp-modo-lectura .magazine-page,
    body.sp-modo-lectura main,
    body.sp-modo-lectura > div:not(#sp-reader-toolbar):not(.control-bar) {
      width: 96% !important;
      max-width: 820px !important;
      min-width: 0 !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      overflow: visible !important;
      padding: 18px 16px !important;
      margin: 0 auto 20px auto !important;
      border-radius: 14px !important;
      box-sizing: border-box !important;
      transform: none !important;
      zoom: 1 !important;
    }

    /* Evitar que ningún elemento hijo se salga por la derecha o corte texto */
    body.sp-modo-lectura .sheet *,
    body.sp-modo-lectura .page *,
    body.sp-modo-lectura .a4-page *,
    body.sp-modo-lectura main * {
      max-width: 100% !important;
      min-width: 0 !important;
      max-height: none !important;
      overflow-wrap: break-word !important;
      word-wrap: break-word !important;
      box-sizing: border-box !important;
    }

    body.sp-modo-lectura .sheet div,
    body.sp-modo-lectura .page div,
    body.sp-modo-lectura .a4-page div,
    body.sp-modo-lectura main div,
    body.sp-modo-lectura section,
    body.sp-modo-lectura article {
      height: auto !important;
      max-height: none !important;
      overflow: visible !important;
    }

    /* Permitir que las etiquetas con nowrap puedan partir línea en móvil si son largas */
    body.sp-modo-lectura span,
    body.sp-modo-lectura strong,
    body.sp-modo-lectura a,
    body.sp-modo-lectura th,
    body.sp-modo-lectura td {
      white-space: normal !important;
    }

    /* Escalado generoso de tipografía (MODO LETRA GRANDE = 16px base) */
    body.sp-modo-lectura p,
    body.sp-modo-lectura li,
    body.sp-modo-lectura td,
    body.sp-modo-lectura dd,
    body.sp-modo-lectura .prod-desc,
    body.sp-modo-lectura .f2-text,
    body.sp-modo-lectura .service-desc,
    body.sp-modo-lectura .roadmap-item span,
    body.sp-modo-lectura .sat-item span,
    body.sp-modo-lectura .sat-card-bullets li,
    body.sp-modo-lectura .print-qr-text,
    body.sp-modo-lectura .contact-details-box,
    body.sp-modo-lectura .footer-bar {
      font-size: 16px !important;
      line-height: 1.55 !important;
    }

    body.sp-modo-lectura h1,
    body.sp-modo-lectura h2,
    body.sp-modo-lectura h3,
    body.sp-modo-lectura h4,
    body.sp-modo-lectura .prod-title,
    body.sp-modo-lectura .f2-title,
    body.sp-modo-lectura .service-title,
    body.sp-modo-lectura .card-title,
    body.sp-modo-lectura .doc-title,
    body.sp-modo-lectura .roadmap-item strong,
    body.sp-modo-lectura .sat-card-title,
    body.sp-modo-lectura .sat-item strong {
      font-size: 19px !important;
      line-height: 1.35 !important;
      margin-bottom: 6px !important;
    }

    body.sp-modo-lectura .section-banner,
    body.sp-modo-lectura .cat-banner,
    body.sp-modo-lectura .banner-title {
      font-size: 16.5px !important;
      padding: 10px 14px !important;
      border-radius: 8px !important;
      line-height: 1.35 !important;
      flex-wrap: wrap !important;
      gap: 6px !important;
      margin-bottom: 12px !important;
      height: auto !important;
    }
    body.sp-modo-lectura .section-banner .rule,
    body.sp-modo-lectura .cat-banner span {
      font-size: 14px !important;
      padding: 3px 8px !important;
    }

    body.sp-modo-lectura .prod-badge,
    body.sp-modo-lectura .price-tag,
    body.sp-modo-lectura .service-benefit,
    body.sp-modo-lectura th {
      font-size: 15px !important;
      line-height: 1.35 !important;
      padding: 5px 8px !important;
    }

    /* Sobrescribir cualquier font-size diminuto inline (ej. style="font-size: 6px") */
    body.sp-modo-lectura [style*="font-size"]:not(.sp-reader-toolbar *):not(.sp-reader-btn) {
      font-size: 15.5px !important;
      line-height: 1.5 !important;
    }
    body.sp-modo-lectura strong[style*="font-size"],
    body.sp-modo-lectura b[style*="font-size"] {
      font-size: 17px !important;
      line-height: 1.4 !important;
    }

    /* Tarjetas con aire y separación */
    body.sp-modo-lectura .card-lanzamiento,
    body.sp-modo-lectura .f2-item,
    body.sp-modo-lectura .roadmap-item,
    body.sp-modo-lectura .sat-item,
    body.sp-modo-lectura .sat-card-3,
    body.sp-modo-lectura .gift-box,
    body.sp-modo-lectura article {
      padding: 14px !important;
      margin-bottom: 12px !important;
      border-radius: 10px !important;
    }

    /* Apilar columnas estrechas en 1 sola columna amplia para que nunca se corte el texto */
    body.sp-modo-lectura .roadmap-grid,
    body.sp-modo-lectura .satellites-grid-3,
    body.sp-modo-lectura [style*="grid-template-columns"] {
      display: flex !important;
      flex-direction: column !important;
      gap: 12px !important;
      width: 100% !important;
    }

    body.sp-modo-lectura .header,
    body.sp-modo-lectura .prod-head,
    body.sp-modo-lectura .service-title-row,
    body.sp-modo-lectura .print-qr-banner,
    body.sp-modo-lectura .footer-bar {
      display: flex !important;
      flex-wrap: wrap !important;
      gap: 10px !important;
      height: auto !important;
    }

    /* Tablas 100% adaptables y con scroll horizontal limpio si tienen muchas columnas */
    body.sp-modo-lectura .pricing-table-box {
      overflow-x: auto !important;
      -webkit-overflow-scrolling: touch !important;
      width: 100% !important;
      display: block !important;
    }
    body.sp-modo-lectura table {
      width: 100% !important;
      border-collapse: collapse !important;
      display: table !important;
    }
    body.sp-modo-lectura th,
    body.sp-modo-lectura td {
      padding: 10px 8px !important;
      word-break: break-word !important;
    }

    /* ==========================================================================
       MODO LETRA EXTRA GRANDE (A+ = 19px-22px PARA PERSONAS MAYORES)
       ========================================================================== */
    body.sp-modo-lectura.sp-letra-xl p,
    body.sp-modo-lectura.sp-letra-xl li,
    body.sp-modo-lectura.sp-letra-xl td,
    body.sp-modo-lectura.sp-letra-xl .prod-desc,
    body.sp-modo-lectura.sp-letra-xl .f2-text,
    body.sp-modo-lectura.sp-letra-xl .service-desc,
    body.sp-modo-lectura.sp-letra-xl .roadmap-item span,
    body.sp-modo-lectura.sp-letra-xl .sat-item span,
    body.sp-modo-lectura.sp-letra-xl .print-qr-text,
    body.sp-modo-lectura.sp-letra-xl [style*="font-size"]:not(.sp-reader-toolbar *):not(.sp-reader-btn) {
      font-size: 19px !important;
      line-height: 1.6 !important;
    }
    body.sp-modo-lectura.sp-letra-xl h1,
    body.sp-modo-lectura.sp-letra-xl h2,
    body.sp-modo-lectura.sp-letra-xl h3,
    body.sp-modo-lectura.sp-letra-xl .prod-title,
    body.sp-modo-lectura.sp-letra-xl .f2-title,
    body.sp-modo-lectura.sp-letra-xl .service-title,
    body.sp-modo-lectura.sp-letra-xl strong[style*="font-size"] {
      font-size: 22px !important;
      line-height: 1.4 !important;
    }

    /* ==========================================================================
       MODO 3: VISTA A5/A4 IMPRESIÓN (ENCUADRE EXACTO DE FOLIO EN PANTALLA)
       ========================================================================== */
    body.sp-vista-impresion {
      overflow-x: hidden !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
    }
  }

  @media print {
    .sp-reader-toolbar {
      display: none !important;
    }
  }
</style>
<script id="sp-auto-fit-mobile">
(function() {
  function ajustarEscalaVistaImpresion() {
    var hojas = document.querySelectorAll('.sheet, .page, .a4-page, .a5-page, .dossier-page, .magazine-page');
    var enModoImpresion = document.body.classList.contains('sp-vista-impresion');

    if (!enModoImpresion) {
      hojas.forEach(function(h) {
        h.style.zoom = '';
        h.style.transform = '';
        h.style.marginBottom = '';
      });
      return;
    }

    var anchoPantalla = window.innerWidth || document.documentElement.clientWidth;
    hojas.forEach(function(h) {
      h.style.zoom = '';
      h.style.transform = '';
      var anchoHoja = h.offsetWidth || 794;
      if (anchoPantalla < anchoHoja + 24) {
        var factor = (anchoPantalla - 20) / anchoHoja;
        if ('zoom' in document.body.style) {
          h.style.zoom = factor;
        } else {
          h.style.transformOrigin = 'top center';
          h.style.transform = 'scale(' + factor + ')';
        }
      }
    });
  }

  function iniciarModoLecturaAccesible() {
    document.documentElement.classList.add('sp-html-lectura');
    document.body.classList.add('sp-modo-lectura');

    if (document.getElementById('sp-reader-toolbar')) return;

    var barra = document.createElement('div');
    barra.id = 'sp-reader-toolbar';
    barra.className = 'sp-reader-toolbar no-print';
    barra.innerHTML =
      '<div class="sp-reader-toolbar-left">' +
        '<span>📖 Modo Lectura Cómoda (Sin Cortes)</span>' +
      '</div>' +
      '<div class="sp-reader-toolbar-btns">' +
        '<a href="../index.html#documentacion" class="sp-reader-btn secondary" id="sp-btn-volver-web">⬅ Volver a la Web</a>' +
        '<button type="button" class="sp-reader-btn active" id="sp-btn-lectura">🔎 Letra Grande</button>' +
        '<button type="button" class="sp-reader-btn" id="sp-btn-xl">➕ Letra Extra Grande (A+)</button>' +
        '<button type="button" class="sp-reader-btn secondary" id="sp-btn-original">📄 Vista A5/A4 Impresión</button>' +
        '<button type="button" class="sp-reader-btn print-action" id="sp-btn-imprimir" style="display:none;">🖨️ Imprimir / PDF</button>' +
      '</div>';

    document.body.insertBefore(barra, document.body.firstChild);

    var path = window.location.pathname || '';
    var btnVolver = document.getElementById('sp-btn-volver-web');
    if (btnVolver) {
      if (path.indexOf('/articulos/') !== -1) {
        btnVolver.setAttribute('href', '../index.html#magazine');
      } else if (path.indexOf('/documentos/') === -1) {
        btnVolver.setAttribute('href', 'index.html#documentacion');
      }
    }

    var btnLectura = document.getElementById('sp-btn-lectura');
    var btnXL = document.getElementById('sp-btn-xl');
    var btnOriginal = document.getElementById('sp-btn-original');
    var btnImprimir = document.getElementById('sp-btn-imprimir');

    btnLectura.addEventListener('click', function() {
      document.documentElement.classList.add('sp-html-lectura');
      document.body.classList.add('sp-modo-lectura');
      document.body.classList.remove('sp-letra-xl', 'sp-vista-impresion');
      btnLectura.classList.add('active');
      btnXL.classList.remove('active');
      btnOriginal.classList.remove('active');
      if (btnImprimir) btnImprimir.style.display = 'none';
      ajustarEscalaVistaImpresion();
    });

    btnXL.addEventListener('click', function() {
      document.documentElement.classList.add('sp-html-lectura');
      document.body.classList.add('sp-modo-lectura', 'sp-letra-xl');
      document.body.classList.remove('sp-vista-impresion');
      btnXL.classList.add('active');
      btnLectura.classList.remove('active');
      btnOriginal.classList.remove('active');
      if (btnImprimir) btnImprimir.style.display = 'none';
      ajustarEscalaVistaImpresion();
    });

    btnOriginal.addEventListener('click', function() {
      document.documentElement.classList.remove('sp-html-lectura');
      document.body.classList.remove('sp-modo-lectura', 'sp-letra-xl');
      document.body.classList.add('sp-vista-impresion');
      btnOriginal.classList.add('active');
      btnLectura.classList.remove('active');
      btnXL.classList.remove('active');
      if (btnImprimir) btnImprimir.style.display = 'inline-flex';
      setTimeout(ajustarEscalaVistaImpresion, 50);
    });

    if (btnImprimir) {
      btnImprimir.addEventListener('click', function() {
        window.print();
      });
    }

    window.addEventListener('resize', ajustarEscalaVistaImpresion);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciarModoLecturaAccesible);
  } else {
    iniciarModoLecturaAccesible();
  }
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


def actualizar_index_con_categoria_documentacion(dir_raiz, carpeta_backups, marca_tiempo):
    ruta_index = os.path.join(dir_raiz, "index.html")
    if not os.path.isfile(ruta_index):
        return False

    shutil.copy2(ruta_index, os.path.join(carpeta_backups, f"index.html.backup_{marca_tiempo}"))
    with open(ruta_index, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    modificado = False

    # 1. Poner id="documentacion" y scroll-mt-24 en la sección de Documentación Oficial y Dossier en Detalle
    patron_sec_doc = re.compile(
        r'<section\s+class="py-16\s+bg-slate-950\s+border-t\s+border-white/5\s+relative\s+overflow-hidden"\s*>',
        re.IGNORECASE
    )
    if 'id="documentacion"' not in html and patron_sec_doc.search(html):
        html = patron_sec_doc.sub(
            '<section id="documentacion" class="scroll-mt-24 py-16 bg-slate-950 border-t border-white/5 relative overflow-hidden">',
            html,
            count=1
        )
        modificado = True
    elif 'id="documentacion"' not in html and "Documentación Oficial y Dossier en Detalle" in html:
        html = html.replace(
            '<section class="py-16 bg-slate-950 border-t border-white/5 relative overflow-hidden">',
            '<section id="documentacion" class="scroll-mt-24 py-16 bg-slate-950 border-t border-white/5 relative overflow-hidden">',
            1
        )
        modificado = True

    # 2. Añadir entrada "Documentación Oficial" en el menú desplegable móvil (arriba a la izquierda / hamburguesa)
    enlace_movil_doc = (
        '      <a href="#documentacion" onclick="toggleMobileMenu()" class="flex items-center gap-3.5 text-teal-200 hover:text-teal-300 transition-colors">\n'
        '        <span class="text-2xl w-8 text-center flex-shrink-0">📄</span>\n'
        '        <span>Documentación Oficial</span>\n'
        '      </a>\n'
    )
    if 'href="#documentacion"' not in html:
        objetivo_movil = '<a href="#contacto" onclick="toggleMobileMenu()"'
        if objetivo_movil in html:
            html = html.replace(objetivo_movil, enlace_movil_doc + "      " + objetivo_movil, 1)
            modificado = True

    # 3. Añadir entrada "Documentación" en la barra de navegación principal de escritorio
    enlace_desktop_doc = '<a href="#documentacion" class="hover:text-teal-400 transition-colors px-1.5 py-1 rounded-md hover:bg-white/5">Documentación</a>\n        '
    objetivo_desktop = '<a href="#contacto" class="hover:text-teal-400 transition-colors px-1.5 py-1 rounded-md hover:bg-white/5">Contacto</a>'
    if objetivo_desktop in html and 'href="#documentacion" class="hover:text-teal-400' not in html:
        html = html.replace(objetivo_desktop, enlace_desktop_doc + objetivo_desktop, 1)
        modificado = True

    if modificado:
        with open(ruta_index, "w", encoding="utf-8") as f:
            f.write(html)
        print("   ✔ 'index.html' actualizado con la entrada directa '📄 Documentación Oficial' en el menú y ancla #documentacion.")
    return modificado


def ejecutar_actualizador():
    print("=" * 80)
    print("🔎 ACTUALIZADOR INTERACTIVO SISTEMAS PYME (AD.py — Modo Lectura v2 Sin Cortes + Menú Documentación)")
    print("=" * 80)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ ERROR: No se encontró la carpeta 'public_html' en el Escritorio.")
        return

    print(f"📂 Carpeta raíz localizada en: {dir_raiz}")

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. Actualizar index.html con la entrada de Documentación Oficial en el menú
    actualizar_index_con_categoria_documentacion(dir_raiz, carpeta_backups, marca_tiempo)

    # 2. Actualizar todos los documentos y tarjetones con el Motor v2 de Lectura Cómoda sin cortes
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

            # Eliminar versión previa del bloque
            contenido_nuevo = re.sub(
                r'<!-- \[SP_AUTO_FIT_MOBILE_START\][\s\S]*?<!-- \[SP_AUTO_FIT_MOBILE_END\] -->',
                '',
                contenido
            )

            # Asegurar meta viewport estándar
            if re.search(r'<meta\s+name=["\']viewport["\'][^>]*>', contenido_nuevo, flags=re.IGNORECASE):
                contenido_nuevo = re.sub(
                    r'<meta\s+name=["\']viewport["\'][^>]*>',
                    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">',
                    contenido_nuevo,
                    count=1,
                    flags=re.IGNORECASE
                )

            if "</head>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</head>", BLOQUE_LECTURA_COMODA_SENIOR_V2 + "\n</head>", 1)
            elif "</body>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</body>", BLOQUE_LECTURA_COMODA_SENIOR_V2 + "\n</body>", 1)
            else:
                contenido_nuevo += "\n" + BLOQUE_LECTURA_COMODA_SENIOR_V2

            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(contenido_nuevo)

            archivos_actualizados.append(os.path.relpath(ruta_completa, dir_raiz))
            print(f"   ✔ Lectura sin cortes + Vista A5/A4 aplicada en: {os.path.relpath(ruta_completa, dir_raiz)}")

    print("\n" + "=" * 80)
    print(f"🎉 PROCESO COMPLETADO: 'index.html' y {len(archivos_actualizados)} documentos actualizados.")
    print(f"📦 Copias de seguridad guardadas en: {carpeta_backups}")
    print("=" * 80)


if __name__ == "__main__":
    ejecutar_actualizador()
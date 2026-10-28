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


BLOQUE_LECTURA_COMODA_SENIOR = """<!-- [SP_AUTO_FIT_MOBILE_START] Motor de Lectura Cómoda (Letra Grande) en Pantalla + Formato Exacto A5/A4 al Imprimir -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<style id="sp-easy-read-css">
  /* ==========================================================================
     MODO LECTURA CÓMODA EN PANTALLA (MÓVIL, TABLET Y ORDENADOR)
     Convierte los tarjetones A5 y dossiers A4 a letra grande (15px-18px)
     cuando está activo 'sp-modo-lectura', manteniendo intacto @media print.
     ========================================================================== */
  @media screen {
    .sp-reader-toolbar {
      position: sticky;
      top: 8px;
      z-index: 99999;
      background: rgba(11, 37, 69, 0.97);
      backdrop-filter: blur(10px);
      color: #ffffff;
      border: 2px solid #14b8a6;
      border-radius: 14px;
      padding: 10px 14px;
      margin: 8px auto 14px auto;
      width: 96%;
      max-width: 820px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .sp-reader-toolbar-left {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      font-weight: 800;
      color: #5eead4;
    }
    .sp-reader-toolbar-btns {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }
    .sp-reader-btn {
      background: #0f766e;
      color: #ffffff;
      border: 1.5px solid #2dd4bf;
      padding: 8px 13px;
      border-radius: 10px;
      font-size: 13.5px;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.2s ease;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .sp-reader-btn:hover {
      background: #115e59;
    }
    .sp-reader-btn.active {
      background: #10b981;
      color: #052e16;
      border-color: #6ee7b7;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.5);
    }
    .sp-reader-btn.secondary {
      background: #1e293b;
      color: #e2e8f0;
      border-color: #475569;
    }

    /* REGLAS DE AMPLIACIÓN DE LETRA Y FLUIDEZ CUANDO ESTÁ EN MODO LECTURA */
    body.sp-modo-lectura {
      padding: 8px 6px 40px 6px !important;
      overflow-x: hidden !important;
      -- f-scale: 1;
    }
    body.sp-modo-lectura .sheet,
    body.sp-modo-lectura .page,
    body.sp-modo-lectura .a4-page,
    body.sp-modo-lectura .a5-page,
    body.sp-modo-lectura main.sheet {
      width: 96% !important;
      max-width: 780px !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      overflow: visible !important;
      padding: 20px 18px !important;
      margin: 0 auto 22px auto !important;
      border-radius: 14px !important;
      gap: 14px !important;
    }

    /* Escalado generoso de toda la tipografía para personas mayores */
    body.sp-modo-lectura .header {
      flex-wrap: wrap !important;
      gap: 10px !important;
      padding-bottom: 12px !important;
      margin-bottom: 14px !important;
    }
    body.sp-modo-lectura .brand-logo-img {
      max-height: 54px !important;
      max-width: 220px !important;
    }
    body.sp-modo-lectura .header-tagline,
    body.sp-modo-lectura .doc-type {
      font-size: 14px !important;
      line-height: 1.4 !important;
      text-align: left !important;
    }
    body.sp-modo-lectura .header-tagline strong,
    body.sp-modo-lectura .doc-title {
      font-size: 16px !important;
    }

    body.sp-modo-lectura .section-banner,
    body.sp-modo-lectura .cat-banner,
    body.sp-modo-lectura .banner-title {
      font-size: 16px !important;
      padding: 10px 14px !important;
      border-radius: 8px !important;
      line-height: 1.35 !important;
      flex-wrap: wrap !important;
      gap: 6px !important;
      margin-bottom: 10px !important;
    }
    body.sp-modo-lectura .section-banner .rule,
    body.sp-modo-lectura .cat-banner span {
      font-size: 13.5px !important;
      padding: 3px 8px !important;
    }

    /* Títulos de servicios y tarjetas */
    body.sp-modo-lectura .prod-title,
    body.sp-modo-lectura .f2-title,
    body.sp-modo-lectura .service-title,
    body.sp-modo-lectura .card-title,
    body.sp-modo-lectura h1,
    body.sp-modo-lectura h2,
    body.sp-modo-lectura h3,
    body.sp-modo-lectura .roadmap-item strong,
    body.sp-modo-lectura .sat-card-title,
    body.sp-modo-lectura .sat-item strong {
      font-size: 18px !important;
      line-height: 1.35 !important;
      margin-bottom: 4px !important;
    }

    /* Precios y etiquetas destacadas */
    body.sp-modo-lectura .prod-badge,
    body.sp-modo-lectura .price-tag,
    body.sp-modo-lectura .service-benefit {
      font-size: 15px !important;
      padding: 3px 8px !important;
    }

    /* Textos descriptivos, párrafos y listas: 15.5px con interlineado holgado */
    body.sp-modo-lectura p,
    body.sp-modo-lectura li,
    body.sp-modo-lectura .prod-desc,
    body.sp-modo-lectura .f2-text,
    body.sp-modo-lectura .service-desc,
    body.sp-modo-lectura .roadmap-item span,
    body.sp-modo-lectura .sat-item span,
    body.sp-modo-lectura .sat-card-bullets,
    body.sp-modo-lectura .sat-card-bullets li,
    body.sp-modo-lectura .print-qr-text,
    body.sp-modo-lectura .contact-details-box,
    body.sp-modo-lectura .footer-bar,
    body.sp-modo-lectura .gift-box div {
      font-size: 15.5px !important;
      line-height: 1.55 !important;
    }

    /* Sobrescribir cualquier font-size diminuto inline (ej. style="font-size: 6px") */
    body.sp-modo-lectura .sheet [style*="font-size"],
    body.sp-modo-lectura .page [style*="font-size"],
    body.sp-modo-lectura .a4-page [style*="font-size"] {
      font-size: 15px !important;
      line-height: 1.5 !important;
    }
    body.sp-modo-lectura .sheet strong[style*="font-size"],
    body.sp-modo-lectura .page strong[style*="font-size"] {
      font-size: 16.5px !important;
    }

    /* Tarjetas con más aire interior */
    body.sp-modo-lectura .card-lanzamiento,
    body.sp-modo-lectura .f2-item,
    body.sp-modo-lectura .roadmap-item,
    body.sp-modo-lectura .sat-item,
    body.sp-modo-lectura .sat-card-3,
    body.sp-modo-lectura .gift-box,
    body.sp-modo-lectura article {
      padding: 12px 14px !important;
      margin-bottom: 10px !important;
      border-radius: 10px !important;
    }
    body.sp-modo-lectura .service-num,
    body.sp-modo-lectura .service-num-badge {
      width: 28px !important;
      height: 28px !important;
      font-size: 15px !important;
      border-radius: 7px !important;
    }

    /* En móvil, apilar rejillas de 2 o 3 columnas en 1 sola columna ancha para que el texto sea grande */
    @media screen and (max-width: 700px) {
      body.sp-modo-lectura .roadmap-grid,
      body.sp-modo-lectura .satellites-grid-3,
      body.sp-modo-lectura [style*="grid-template-columns"] {
        grid-template-columns: 1fr !important;
        gap: 10px !important;
      }
      body.sp-modo-lectura .prod-head,
      body.sp-modo-lectura .service-title-row,
      body.sp-modo-lectura .print-qr-banner {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 8px !important;
      }
      body.sp-modo-lectura .contact-details-box {
        border-left: none !important;
        border-top: 1px solid #99f6e4 !important;
        padding-left: 0 !important;
        padding-top: 8px !important;
        text-align: left !important;
        width: 100% !important;
      }
    }

    /* Tablas de precios mucho más legibles y con scroll suave si la pantalla es muy estrecha */
    body.sp-modo-lectura .pricing-table-box,
    body.sp-modo-lectura table {
      overflow-x: auto !important;
      display: block !important;
      width: 100% !important;
    }
    body.sp-modo-lectura .pricing-table th,
    body.sp-modo-lectura table th {
      font-size: 13.5px !important;
      padding: 9px 10px !important;
    }
    body.sp-modo-lectura .pricing-table td,
    body.sp-modo-lectura table td {
      font-size: 14.5px !important;
      padding: 10px !important;
      line-height: 1.45 !important;
    }

    /* MODO LETRA EXTRA GRANDE (A+) PARA PERSONAS MAYORES */
    body.sp-modo-lectura.sp-letra-xl p,
    body.sp-modo-lectura.sp-letra-xl li,
    body.sp-modo-lectura.sp-letra-xl .prod-desc,
    body.sp-modo-lectura.sp-letra-xl .f2-text,
    body.sp-modo-lectura.sp-letra-xl .sheet [style*="font-size"],
    body.sp-modo-lectura.sp-letra-xl .page [style*="font-size"],
    body.sp-modo-lectura.sp-letra-xl table td {
      font-size: 18px !important;
      line-height: 1.6 !important;
    }
    body.sp-modo-lectura.sp-letra-xl .prod-title,
    body.sp-modo-lectura.sp-letra-xl .f2-title,
    body.sp-modo-lectura.sp-letra-xl h2,
    body.sp-modo-lectura.sp-letra-xl h3 {
      font-size: 21px !important;
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
  function iniciarModoLecturaAccesible() {
    // Activar por defecto el Modo Lectura Cómoda en pantalla
    document.body.classList.add('sp-modo-lectura');

    if (document.getElementById('sp-reader-toolbar')) return;

    var barra = document.createElement('div');
    barra.id = 'sp-reader-toolbar';
    barra.className = 'sp-reader-toolbar no-print';
    barra.innerHTML =
      '<div class="sp-reader-toolbar-left">' +
        '<span>📖 Modo Lectura Cómoda (Letra Grande)</span>' +
      '</div>' +
      '<div class="sp-reader-toolbar-btns">' +
        '<a href="../index.html" class="sp-reader-btn secondary" id="sp-btn-volver-web">⬅ Volver a la Web</a>' +
        '<button type="button" class="sp-reader-btn active" id="sp-btn-lectura">🔎 Letra Grande</button>' +
        '<button type="button" class="sp-reader-btn" id="sp-btn-xl">➕ Letra Extra Grande (A+)</button>' +
        '<button type="button" class="sp-reader-btn secondary" id="sp-btn-original">📄 Vista A5/A4 Impresión</button>' +
      '</div>';

    document.body.insertBefore(barra, document.body.firstChild);

    // Ajustar enlace de retorno si el documento está en la raíz
    var path = window.location.pathname || '';
    if (path.indexOf('/documentos/') === -1 && path.indexOf('/articulos/') === -1) {
      var btnVolver = document.getElementById('sp-btn-volver-web');
      if (btnVolver) btnVolver.setAttribute('href', 'index.html');
    }

    var btnLectura = document.getElementById('sp-btn-lectura');
    var btnXL = document.getElementById('sp-btn-xl');
    var btnOriginal = document.getElementById('sp-btn-original');

    btnLectura.addEventListener('click', function() {
      document.body.classList.add('sp-modo-lectura');
      document.body.classList.remove('sp-letra-xl');
      btnLectura.classList.add('active');
      btnXL.classList.remove('active');
      btnOriginal.classList.remove('active');
    });

    btnXL.addEventListener('click', function() {
      document.body.classList.add('sp-modo-lectura', 'sp-letra-xl');
      btnXL.classList.add('active');
      btnLectura.classList.remove('active');
      btnOriginal.classList.remove('active');
    });

    btnOriginal.addEventListener('click', function() {
      document.body.classList.remove('sp-modo-lectura', 'sp-letra-xl');
      btnOriginal.classList.add('active');
      btnLectura.classList.remove('active');
      btnXL.classList.remove('active');
    });
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


def ejecutar_actualizador():
    print("=" * 78)
    print("🔎 ACTUALIZADOR INTERACTIVO SISTEMAS PYME (AD.py — Modo Lectura Letra Grande en Documentos)")
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
                r'<!-- \[SP_AUTO_FIT_MOBILE_START\][\s\S]*?<!-- \[SP_AUTO_FIT_MOBILE_END\] -->',
                '',
                contenido
            )

            # 3. Poner el meta viewport estándar (width=device-width, initial-scale=1.0) para que la letra NO se encoja en móvil
            if re.search(r'<meta\s+name=["\']viewport["\'][^>]*>', contenido_nuevo, flags=re.IGNORECASE):
                contenido_nuevo = re.sub(
                    r'<meta\s+name=["\']viewport["\'][^>]*>',
                    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">',
                    contenido_nuevo,
                    count=1,
                    flags=re.IGNORECASE
                )

            # 4. Inyectar el motor de Lectura Cómoda (Letra Grande) antes de </head>
            if "</head>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</head>", BLOQUE_LECTURA_COMODA_SENIOR + "\n</head>", 1)
            elif "</body>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</body>", BLOQUE_LECTURA_COMODA_SENIOR + "\n</body>", 1)
            else:
                contenido_nuevo += "\n" + BLOQUE_LECTURA_COMODA_SENIOR

            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(contenido_nuevo)

            archivos_actualizados.append((os.path.relpath(ruta_completa, dir_raiz), ruta_backup))
            print(f"   ✔ Modo Lectura Letra Grande aplicado en: {os.path.relpath(ruta_completa, dir_raiz)}")

    print("\n" + "=" * 78)
    print(f"🎉 PROCESO COMPLETADO: {len(archivos_actualizados)} documentos actualizados con Letra Grande en pantalla.")
    print(f"📦 Copias de seguridad guardadas en: {carpeta_backups}")
    print("=" * 78)


if __name__ == "__main__":
    ejecutar_actualizador()
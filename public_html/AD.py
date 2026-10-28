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


BLOQUE_ADAPTADOR_ESTRUCTURAL_MOVIL_V3 = """<!-- [SP_AUTO_FIT_MOBILE_START] Motor v3 de Adaptación Estructural Mobile-First + Vista Original A5/A4 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<style id="sp-easy-read-css">
  @media screen {
    /* ==========================================================================
       BARRA SUPERIOR DE CONTROL (COMPACTA Y SIEMPRE ACCESIBLE)
       ========================================================================== */
    .sp-reader-toolbar {
      position: sticky !important;
      top: 6px !important;
      z-index: 999999 !important;
      background: rgba(11, 37, 69, 0.97) !important;
      backdrop-filter: blur(12px) !important;
      color: #ffffff !important;
      border: 1.5px solid #14b8a6 !important;
      border-radius: 14px !important;
      padding: 8px 12px !important;
      margin: 6px auto 12px auto !important;
      width: 96% !important;
      max-width: 780px !important;
      display: flex !important;
      flex-wrap: wrap !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 8px !important;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.5) !important;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
      box-sizing: border-box !important;
    }
    .sp-reader-toolbar-btns {
      display: flex !important;
      flex-wrap: wrap !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 6px !important;
      width: 100% !important;
    }
    .sp-reader-btn {
      background: #1e293b !important;
      color: #e2e8f0 !important;
      border: 1px solid #475569 !important;
      padding: 7px 11px !important;
      border-radius: 9px !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      cursor: pointer !important;
      transition: all 0.18s ease !important;
      text-decoration: none !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 4px !important;
      line-height: 1.2 !important;
      flex: 1 1 auto !important;
      text-align: center !important;
    }
    .sp-reader-btn.active {
      background: #10b981 !important;
      color: #052e16 !important;
      border-color: #6ee7b7 !important;
      font-weight: 800 !important;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.45) !important;
    }
    .sp-reader-btn.back-btn {
      background: #0f172a !important;
      color: #5eead4 !important;
      border-color: #0d9488 !important;
    }
    .sp-reader-btn.print-action {
      background: #d97706 !important;
      color: #ffffff !important;
      border-color: #fbbf24 !important;
    }

    /* ==========================================================================
       REESTRUCTURACIÓN MÓVIL (MODO LECTURA SIN DEFORMACIONES)
       ========================================================================== */
    html.sp-html-lectura,
    body.sp-modo-lectura {
      width: 100% !important;
      max-width: 100vw !important;
      overflow-x: hidden !important;
      margin: 0 !important;
      padding: 4px 0 40px 0 !important;
      background-color: #0f172a !important;
      display: block !important;
    }

    /* Cada hoja A4/A5 se convierte en una tarjeta móvil continua y limpia */
    body.sp-modo-lectura .sheet,
    body.sp-modo-lectura .page,
    body.sp-modo-lectura .a4-page,
    body.sp-modo-lectura .a5-page,
    body.sp-modo-lectura .dossier-page,
    body.sp-modo-lectura .magazine-page {
      width: 95% !important;
      max-width: 680px !important;
      height: auto !important;
      min-height: 0 !important;
      max-height: none !important;
      margin: 0 auto 18px auto !important;
      padding: 16px 14px !important;
      border-radius: 14px !important;
      overflow: visible !important;
      box-sizing: border-box !important;
      display: flex !important;
      flex-direction: column !important;
      gap: 12px !important;
      transform: none !important;
      zoom: 1 !important;
    }

    /* Cabecera del documento limpia en móvil */
    body.sp-modo-lectura .header,
    body.sp-modo-lectura header {
      display: flex !important;
      flex-direction: column !important;
      align-items: flex-start !important;
      gap: 6px !important;
      padding-bottom: 10px !important;
      margin-bottom: 8px !important;
      height: auto !important;
    }
    body.sp-modo-lectura .brand-logo-img {
      max-height: 42px !important;
      max-width: 210px !important;
      width: auto !important;
    }
    body.sp-modo-lectura .header-tagline {
      text-align: left !important;
      font-size: 13px !important;
      line-height: 1.35 !important;
    }
    body.sp-modo-lectura .header-tagline strong {
      font-size: 14px !important;
    }

    /* Banners de categoría */
    body.sp-modo-lectura .section-banner,
    body.sp-modo-lectura .cat-banner {
      display: flex !important;
      flex-direction: column !important;
      align-items: flex-start !important;
      gap: 4px !important;
      padding: 10px 12px !important;
      border-radius: 10px !important;
      font-size: 14.5px !important;
      line-height: 1.3 !important;
      margin-bottom: 10px !important;
      height: auto !important;
    }
    body.sp-modo-lectura .section-banner .rule {
      font-size: 12.5px !important;
      padding: 2px 8px !important;
    }

    /* Tarjetas de servicio (conservando el número/icono a la izquierda o arriba limpiamente) */
    body.sp-modo-lectura .card-lanzamiento,
    body.sp-modo-lectura .f2-item,
    body.sp-modo-lectura .roadmap-item,
    body.sp-modo-lectura .sat-card-3,
    body.sp-modo-lectura .sat-item,
    body.sp-modo-lectura .gift-box,
    body.sp-modo-lectura article {
      padding: 12px 14px !important;
      margin-bottom: 10px !important;
      border-radius: 10px !important;
      height: auto !important;
      max-height: none !important;
      width: 100% !important;
      box-sizing: border-box !important;
    }

    /* Icono numérico de cada servicio */
    body.sp-modo-lectura .service-num,
    body.sp-modo-lectura .service-num-badge {
      width: 26px !important;
      height: 26px !important;
      min-width: 26px !important;
      font-size: 13px !important;
      border-radius: 7px !important;
      margin-top: 2px !important;
    }

    /* Cabecera de cada servicio (Título + Precio/Etiqueta) */
    body.sp-modo-lectura .prod-head,
    body.sp-modo-lectura .service-title-row {
      display: flex !important;
      flex-wrap: wrap !important;
      justify-content: space-between !important;
      align-items: baseline !important;
      gap: 6px !important;
      margin-bottom: 6px !important;
    }

    /* Títulos de servicio */
    body.sp-modo-lectura .prod-title,
    body.sp-modo-lectura .f2-title,
    body.sp-modo-lectura .service-title,
    body.sp-modo-lectura .sat-card-title,
    body.sp-modo-lectura .roadmap-item strong,
    body.sp-modo-lectura .sat-item strong {
      font-size: 16px !important;
      line-height: 1.3 !important;
      font-weight: 800 !important;
    }

    /* Etiquetas de precio o beneficio */
    body.sp-modo-lectura .prod-badge,
    body.sp-modo-lectura .service-benefit {
      font-size: 13.5px !important;
      padding: 3px 8px !important;
      border-radius: 6px !important;
    }

    /* Textos descriptivos */
    body.sp-modo-lectura .prod-desc,
    body.sp-modo-lectura .f2-text,
    body.sp-modo-lectura .service-desc,
    body.sp-modo-lectura .roadmap-item span,
    body.sp-modo-lectura .sat-item span,
    body.sp-modo-lectura .sat-card-bullets li,
    body.sp-modo-lectura p,
    body.sp-modo-lectura li {
      font-size: 14.5px !important;
      line-height: 1.5 !important;
    }

    body.sp-modo-lectura .sat-card-tag {
      font-size: 12px !important;
      margin-bottom: 6px !important;
    }

    /* Clases aplicadas por JS a rejillas multi-columna para apilarlas sin deformar */
    body.sp-modo-lectura .sp-stack-mobile {
      display: flex !important;
      flex-direction: column !important;
      gap: 10px !important;
      width: 100% !important;
      height: auto !important;
    }
    body.sp-modo-lectura .sp-stack-mobile > * {
      width: 100% !important;
      max-width: 100% !important;
      margin-left: 0 !important;
      margin-right: 0 !important;
      box-sizing: border-box !important;
    }

    /* ==========================================================================
       TRANSFORMACIÓN DE TABLAS EN TARJETAS VERTICALES PARA MÓVIL (CERO DEFORMACIÓN)
       ========================================================================== */
    body.sp-modo-lectura .pricing-table-box {
      border: none !important;
      background: transparent !important;
      overflow: visible !important;
      width: 100% !important;
    }
    body.sp-modo-lectura table,
    body.sp-modo-lectura tbody {
      display: block !important;
      width: 100% !important;
    }
    body.sp-modo-lectura thead {
      display: none !important;
    }
    body.sp-modo-lectura tr {
      display: flex !important;
      flex-direction: column !important;
      gap: 6px !important;
      background: #f8fafc !important;
      border: 1.5px solid #cbd5e1 !important;
      border-radius: 10px !important;
      padding: 12px !important;
      margin-bottom: 10px !important;
      width: 100% !important;
      box-sizing: border-box !important;
    }
    body.sp-modo-lectura tr.highlight {
      background: #f0fdf4 !important;
      border: 2px solid #16a34a !important;
    }
    body.sp-modo-lectura td {
      display: flex !important;
      flex-direction: column !important;
      width: 100% !important;
      padding: 4px 0 !important;
      border: none !important;
      border-bottom: 1px dashed #e2e8f0 !important;
      font-size: 14.5px !important;
      line-height: 1.4 !important;
      text-align: left !important;
    }
    body.sp-modo-lectura td:last-child {
      border-bottom: none !important;
      padding-bottom: 0 !important;
    }
    body.sp-modo-lectura td[data-label]::before {
      content: attr(data-label);
      font-size: 11px !important;
      font-weight: 800 !important;
      text-transform: uppercase !important;
      color: #0f766e !important;
      letter-spacing: 0.3px !important;
      margin-bottom: 2px !important;
      display: block !important;
    }

    /* Caja QR y Contacto al pie */
    body.sp-modo-lectura .print-qr-banner {
      display: flex !important;
      flex-direction: column !important;
      align-items: flex-start !important;
      gap: 12px !important;
      padding: 14px !important;
      border-radius: 12px !important;
      margin-top: 8px !important;
    }
    body.sp-modo-lectura .print-qr-left {
      display: flex !important;
      align-items: center !important;
      gap: 12px !important;
      width: 100% !important;
    }
    body.sp-modo-lectura .print-qr-img {
      width: 60px !important;
      height: 60px !important;
    }
    body.sp-modo-lectura .print-qr-text {
      font-size: 13.5px !important;
      line-height: 1.4 !important;
    }
    body.sp-modo-lectura .print-qr-text strong {
      font-size: 15px !important;
      margin-bottom: 3px !important;
    }
    body.sp-modo-lectura .contact-details-box {
      border-left: none !important;
      border-top: 1.5px solid #99f6e4 !important;
      padding-left: 0 !important;
      padding-top: 10px !important;
      width: 100% !important;
      text-align: left !important;
      font-size: 14px !important;
      line-height: 1.45 !important;
    }
    body.sp-modo-lectura .contact-details-box .name {
      font-size: 16px !important;
    }
    body.sp-modo-lectura .contact-details-box .role {
      font-size: 12px !important;
      margin-bottom: 2px !important;
    }
    body.sp-modo-lectura .footer-bar {
      display: flex !important;
      flex-wrap: wrap !important;
      justify-content: space-between !important;
      gap: 6px !important;
      font-size: 12px !important;
      padding-top: 8px !important;
    }

    /* ==========================================================================
       MODO LETRA EXTRA GRANDE (A+ = 17px-20px CON LA MISMA ESTRUCTURA LIMPIA)
       ========================================================================== */
    body.sp-modo-lectura.sp-letra-xl .prod-desc,
    body.sp-modo-lectura.sp-letra-xl .f2-text,
    body.sp-modo-lectura.sp-letra-xl .service-desc,
    body.sp-modo-lectura.sp-letra-xl .roadmap-item span,
    body.sp-modo-lectura.sp-letra-xl .sat-item span,
    body.sp-modo-lectura.sp-letra-xl .sat-card-bullets li,
    body.sp-modo-lectura.sp-letra-xl p,
    body.sp-modo-lectura.sp-letra-xl li,
    body.sp-modo-lectura.sp-letra-xl td,
    body.sp-modo-lectura.sp-letra-xl .print-qr-text {
      font-size: 17.5px !important;
      line-height: 1.55 !important;
    }
    body.sp-modo-lectura.sp-letra-xl .prod-title,
    body.sp-modo-lectura.sp-letra-xl .f2-title,
    body.sp-modo-lectura.sp-letra-xl .service-title,
    body.sp-modo-lectura.sp-letra-xl .sat-card-title,
    body.sp-modo-lectura.sp-letra-xl .roadmap-item strong,
    body.sp-modo-lectura.sp-letra-xl h1,
    body.sp-modo-lectura.sp-letra-xl h2,
    body.sp-modo-lectura.sp-letra-xl h3 {
      font-size: 20px !important;
      line-height: 1.35 !important;
    }

    /* ==========================================================================
       MODO 3: VISTA TARJETÓN ORIGINAL (A5/A4 ENCUADRADO AL ANCHO DEL MÓVIL)
       ========================================================================== */
    body.sp-vista-impresion {
      overflow-x: hidden !important;
      margin: 0 !important;
      padding: 6px 0 30px 0 !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
    }
    .sp-scale-wrapper {
      width: 100% !important;
      display: flex !important;
      justify-content: center !important;
      overflow: hidden !important;
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
  /* Prepara las tablas y rejillas inline para que en modo móvil se apilen sin deformarse */
  function prepararEstructuraAdaptativaMovil() {
    var contenedores = document.querySelectorAll('.sheet, .page, .a4-page, .a5-page, .dossier-page, .magazine-page, main');

    contenedores.forEach(function(cont) {
      /* 1. Etiquetar celdas de tablas con el nombre de su columna (data-label) para las tarjetas móviles */
      var tablas = cont.querySelectorAll('table');
      tablas.forEach(function(tabla) {
        var ths = Array.from(tabla.querySelectorAll('thead th')).map(function(th) {
          return (th.textContent || '').trim();
        });
        var filas = tabla.querySelectorAll('tbody tr');
        filas.forEach(function(tr) {
          var tds = tr.querySelectorAll('td');
          tds.forEach(function(td, idx) {
            if (ths[idx] && !td.getAttribute('data-label')) {
              td.setAttribute('data-label', ths[idx]);
            }
          });
        });
      });

      /* 2. Detectar rejillas multi-columna inline y añadirles la clase .sp-stack-mobile */
      var elementos = cont.querySelectorAll('div, section, article');
      elementos.forEach(function(el) {
        var st = (el.getAttribute('style') || '').toLowerCase();
        if (
          st.indexOf('grid-template-columns') !== -1 ||
          el.classList.contains('roadmap-grid') ||
          el.classList.contains('satellites-grid-3')
        ) {
          el.classList.add('sp-stack-mobile');
        }
        /* Cajas flex con justify-content: space-between que tienen 2 bloques grandes (ej. cabecera Auditoría GEO) */
        if (st.indexOf('justify-content: space-between') !== -1 && el.children.length === 2) {
          var textoHijo2 = (el.children[1].textContent || '').trim();
          if (textoHijo2.length > 35) {
            el.classList.add('sp-stack-mobile');
          }
        }
      });

      /* 3. Enmodo lectura móvil, agrandar ligeramente los textos con font-size inline diminuto (5px-8px) de forma proporcional */
      var todosConStyle = cont.querySelectorAll('[style*="font-size"]');
      todosConStyle.forEach(function(el) {
        if (!el.getAttribute('data-orig-style')) {
          el.setAttribute('data-orig-style', el.getAttribute('style'));
        }
      });
    });
  }

  function aplicarEstilosInlineSegunModo(enModoLectura, esXL) {
    var elementos = document.querySelectorAll('[data-orig-style]');
    var baseSize = esXL ? '16.5px' : '14px';
    var titleSize = esXL ? '19px' : '16px';

    elementos.forEach(function(el) {
      var orig = el.getAttribute('data-orig-style') || '';
      if (!enModoLectura) {
        el.setAttribute('style', orig);
      } else {
        /* Reemplazar font-size pequeños (5px..11px) por tamaño legible y line-height holgado */
        var adaptado = orig
          .replace(/font-size\s*:\s*[0-9.]+(?:px|pt|mm)\s*;?/gi, 'font-size: ' + (el.tagName === 'STRONG' ? titleSize : baseSize) + '; ')
          .replace(/line-height\s*:\s*[0-9.]+\s*;?/gi, 'line-height: 1.45; ')
          .replace(/white-space\s*:\s*nowrap\s*;?/gi, 'white-space: normal; ');
        el.setAttribute('style', adaptado);
      }
    });
  }

  /* Escala con transform: scale() real cuando el usuario elige "📄 Vista Original A5/A4" */
  function ajustarEscalaVistaOriginal() {
    var hojas = document.querySelectorAll('.sheet, .page, .a4-page, .a5-page, .dossier-page, .magazine-page');
    var enModoImpresion = document.body.classList.contains('sp-vista-impresion');

    hojas.forEach(function(h) {
      h.style.transform = '';
      h.style.transformOrigin = '';
      h.style.marginBottom = '';
    });

    if (!enModoImpresion) return;

    var anchoVentana = window.innerWidth || document.documentElement.clientWidth;
    hojas.forEach(function(h) {
      var rect = h.getBoundingClientRect();
      var anchoReal = h.offsetWidth || rect.width || 560;
      if (anchoVentana < anchoReal + 16) {
        var factor = (anchoVentana - 16) / anchoReal;
        h.style.transformOrigin = 'top center';
        h.style.transform = 'scale(' + factor + ')';
        var altoOriginal = h.offsetHeight || 790;
        var recorteInferior = altoOriginal * (1 - factor);
        h.style.marginBottom = (-recorteInferior + 14) + 'px';
      }
    });
  }

  function iniciarAdaptadorMovil() {
    prepararEstructuraAdaptativaMovil();

    document.documentElement.classList.add('sp-html-lectura');
    document.body.classList.add('sp-modo-lectura');
    aplicarEstilosInlineSegunModo(true, false);

    if (document.getElementById('sp-reader-toolbar')) return;

    var barra = document.createElement('div');
    barra.id = 'sp-reader-toolbar';
    barra.className = 'sp-reader-toolbar no-print';
    barra.innerHTML =
      '<div class="sp-reader-toolbar-btns">' +
        '<a href="../index.html#documentacion" class="sp-reader-btn back-btn" id="sp-btn-volver-web">⬅ Web</a>' +
        '<button type="button" class="sp-reader-btn active" id="sp-btn-lectura">📱 Vista Móvil</button>' +
        '<button type="button" class="sp-reader-btn" id="sp-btn-xl">➕ Letra A+</button>' +
        '<button type="button" class="sp-reader-btn" id="sp-btn-original">📄 Folleto A5/A4</button>' +
        '<button type="button" class="sp-reader-btn print-action" id="sp-btn-imprimir" style="display:none;">🖨️ PDF</button>' +
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
      aplicarEstilosInlineSegunModo(true, false);
      ajustarEscalaVistaOriginal();
    });

    btnXL.addEventListener('click', function() {
      document.documentElement.classList.add('sp-html-lectura');
      document.body.classList.add('sp-modo-lectura', 'sp-letra-xl');
      document.body.classList.remove('sp-vista-impresion');
      btnXL.classList.add('active');
      btnLectura.classList.remove('active');
      btnOriginal.classList.remove('active');
      if (btnImprimir) btnImprimir.style.display = 'none';
      aplicarEstilosInlineSegunModo(true, true);
      ajustarEscalaVistaOriginal();
    });

    btnOriginal.addEventListener('click', function() {
      document.documentElement.classList.remove('sp-html-lectura');
      document.body.classList.remove('sp-modo-lectura', 'sp-letra-xl');
      document.body.classList.add('sp-vista-impresion');
      btnOriginal.classList.add('active');
      btnLectura.classList.remove('active');
      btnXL.classList.remove('active');
      if (btnImprimir) btnImprimir.style.display = 'inline-flex';
      aplicarEstilosInlineSegunModo(false, false);
      setTimeout(ajustarEscalaVistaOriginal, 40);
    });

    if (btnImprimir) {
      btnImprimir.addEventListener('click', function() {
        window.print();
      });
    }

    window.addEventListener('resize', ajustarEscalaVistaOriginal);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciarAdaptadorMovil);
  } else {
    iniciarAdaptadorMovil();
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
    print("=" * 80)
    print("🔎 ACTUALIZADOR INTERACTIVO SISTEMAS PYME (AD.py — Motor v3 Estructura Móvil Sin Deformación)")
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

            contenido_nuevo = re.sub(
                r'<!-- \[SP_AUTO_FIT_MOBILE_START\][\s\S]*?<!-- \[SP_AUTO_FIT_MOBILE_END\] -->',
                '',
                contenido
            )

            if re.search(r'<meta\s+name=["\']viewport["\'][^>]*>', contenido_nuevo, flags=re.IGNORECASE):
                contenido_nuevo = re.sub(
                    r'<meta\s+name=["\']viewport["\'][^>]*>',
                    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">',
                    contenido_nuevo,
                    count=1,
                    flags=re.IGNORECASE
                )

            if "</head>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</head>", BLOQUE_ADAPTADOR_ESTRUCTURAL_MOVIL_V3 + "\n</head>", 1)
            elif "</body>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</body>", BLOQUE_ADAPTADOR_ESTRUCTURAL_MOVIL_V3 + "\n</body>", 1)
            else:
                contenido_nuevo += "\n" + BLOQUE_ADAPTADOR_ESTRUCTURAL_MOVIL_V3

            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(contenido_nuevo)

            archivos_actualizados.append(os.path.relpath(ruta_completa, dir_raiz))
            print(f"   ✔ Estructura móvil v3 aplicada en: {os.path.relpath(ruta_completa, dir_raiz)}")

    print("\n" + "=" * 80)
    print(f"🎉 PROCESO COMPLETADO: {len(archivos_actualizados)} documentos adaptados estructuralmente para móvil.")
    print(f"📦 Copias de seguridad guardadas en: {carpeta_backups}")
    print("=" * 80)


if __name__ == "__main__":
    ejecutar_actualizador()
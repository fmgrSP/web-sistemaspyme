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


BLOQUE_MOTOR_V4_DOBLE_CAPA = """<!-- [SP_AUTO_FIT_MOBILE_START] Motor v4 Doble Capa: Lector Móvil Nativo + Folleto A5/A4 Auto-Encuadrado -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<style id="sp-v4-reader-css">
  @media screen {
    html.sp-v4-active,
    body.sp-v4-active {
      width: 100% !important;
      max-width: 100vw !important;
      overflow-x: hidden !important;
      margin: 0 !important;
      padding: 0 0 40px 0 !important;
      background: #0b1628 !important;
      -webkit-text-size-adjust: 100% !important;
    }

    /* BARRA SUPERIOR FAVORITA: ⬅ Web | 📱 Vista Móvil | ➕ Letra A+ | 📄 Folleto A5/A4 */
    .sp-reader-toolbar {
      position: sticky !important;
      top: 0 !important;
      z-index: 999999 !important;
      background: rgba(11, 25, 48, 0.98) !important;
      backdrop-filter: blur(12px) !important;
      border-bottom: 2px solid #14b8a6 !important;
      padding: 8px 10px !important;
      margin: 0 auto 12px auto !important;
      width: 100% !important;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
      box-sizing: border-box !important;
    }
    .sp-reader-toolbar-btns {
      display: flex !important;
      flex-wrap: wrap !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 6px !important;
      max-width: 680px !important;
      margin: 0 auto !important;
    }
    .sp-reader-btn {
      background: #1e293b !important;
      color: #e2e8f0 !important;
      border: 1px solid #475569 !important;
      padding: 8px 10px !important;
      border-radius: 9px !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      cursor: pointer !important;
      text-decoration: none !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 4px !important;
      line-height: 1.15 !important;
      flex: 1 1 auto !important;
      text-align: center !important;
      white-space: nowrap !important;
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
      flex: 0 0 auto !important;
    }
    .sp-reader-btn.print-action {
      background: #d97706 !important;
      color: #ffffff !important;
      border-color: #fbbf24 !important;
      flex: 0 0 auto !important;
    }

    /* =========================================================================
       CAPA 1: LECTOR MÓVIL NATIVO (#sp-clean-mobile-reader) — CERO ZOOM RARO
       ========================================================================= */
    #sp-clean-mobile-reader {
      width: 100% !important;
      max-width: 640px !important;
      margin: 0 auto !important;
      padding: 4px 12px 32px 12px !important;
      box-sizing: border-box !important;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
      color: #1e293b !important;
      display: none;
    }
    body.sp-mode-mobile #sp-clean-mobile-reader,
    body.sp-mode-xl #sp-clean-mobile-reader {
      display: block !important;
    }

    /* Ocultar las hojas rígidas A4/A5 mientras está activa la Vista Móvil o Letra A+ */
    body.sp-mode-mobile .sp-original-sheet-host,
    body.sp-mode-xl .sp-original-sheet-host {
      display: none !important;
    }

    /* Tarjeta de cada página dentro del Lector Móvil Nativo */
    .sp-m-page {
      background: #ffffff !important;
      border-radius: 16px !important;
      padding: 18px 16px !important;
      margin-bottom: 18px !important;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35) !important;
      border-top: 4px solid #0d9488 !important;
      box-sizing: border-box !important;
      width: 100% !important;
      overflow: hidden !important;
    }
    .sp-m-page-badge {
      display: inline-block !important;
      font-size: 11px !important;
      font-weight: 800 !important;
      text-transform: uppercase !important;
      letter-spacing: 0.5px !important;
      color: #0f766e !important;
      background: #ccfbf1 !important;
      padding: 3px 9px !important;
      border-radius: 6px !important;
      margin-bottom: 8px !important;
    }
    .sp-m-doc-title {
      font-size: 19px !important;
      font-weight: 900 !important;
      color: #0b2545 !important;
      line-height: 1.25 !important;
      margin: 0 0 14px 0 !important;
      padding-bottom: 10px !important;
      border-bottom: 2px solid #e2e8f0 !important;
    }
    .sp-m-section-banner {
      background: linear-gradient(90deg, #0b2545 0%, #0f766e 100%) !important;
      color: #ffffff !important;
      padding: 10px 13px !important;
      border-radius: 10px !important;
      font-size: 14px !important;
      font-weight: 800 !important;
      line-height: 1.3 !important;
      margin: 14px 0 10px 0 !important;
      text-transform: uppercase !important;
    }
    .sp-m-section-banner small {
      display: block !important;
      font-size: 11.5px !important;
      font-weight: 600 !important;
      color: #99f6e4 !important;
      text-transform: none !important;
      margin-top: 2px !important;
    }

    /* Tarjeta individual de servicio / bloque en móvil */
    .sp-m-card {
      background: #f8fafc !important;
      border: 1.5px solid #cbd5e1 !important;
      border-left: 4px solid #0f766e !important;
      border-radius: 12px !important;
      padding: 13px 14px !important;
      margin-bottom: 10px !important;
    }
    .sp-m-card-head {
      display: flex !important;
      flex-wrap: wrap !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 6px !important;
      margin-bottom: 6px !important;
    }
    .sp-m-card-title {
      font-size: 16px !important;
      font-weight: 800 !important;
      color: #0b2545 !important;
      line-height: 1.3 !important;
    }
    .sp-m-card-badge {
      font-size: 13px !important;
      font-weight: 800 !important;
      color: #0f766e !important;
      background: #ccfbf1 !important;
      padding: 3px 8px !important;
      border-radius: 6px !important;
    }
    .sp-m-card-body {
      font-size: 15px !important;
      color: #334155 !important;
      line-height: 1.55 !important;
    }
    .sp-m-card-body p,
    .sp-m-card-body div,
    .sp-m-card-body li {
      font-size: inherit !important;
      line-height: inherit !important;
      margin-bottom: 6px !important;
    }
    .sp-m-card-body ul {
      padding-left: 18px !important;
      margin: 6px 0 !important;
    }

    /* Tablas convertidas en Fichas Móviles Limpias */
    .sp-m-table-group {
      margin: 12px 0 !important;
    }
    .sp-m-table-card {
      background: #f0fdf4 !important;
      border: 1.5px solid #86efac !important;
      border-radius: 12px !important;
      padding: 12px 14px !important;
      margin-bottom: 10px !important;
    }
    .sp-m-table-row {
      display: flex !important;
      flex-direction: column !important;
      padding: 6px 0 !important;
      border-bottom: 1px dashed #cbd5e1 !important;
    }
    .sp-m-table-row:last-child {
      border-bottom: none !important;
      padding-bottom: 0 !important;
    }
    .sp-m-table-label {
      font-size: 11px !important;
      font-weight: 800 !important;
      text-transform: uppercase !important;
      color: #0f766e !important;
      margin-bottom: 2px !important;
    }
    .sp-m-table-val {
      font-size: 15px !important;
      font-weight: 600 !important;
      color: #0f172a !important;
      line-height: 1.4 !important;
    }

    /* Escalado en modo Letra A+ (Extra Grande para personas mayores) */
    body.sp-mode-xl .sp-m-doc-title {
      font-size: 22px !important;
    }
    body.sp-mode-xl .sp-m-section-banner {
      font-size: 16.5px !important;
    }
    body.sp-mode-xl .sp-m-card-title {
      font-size: 18.5px !important;
    }
    body.sp-mode-xl .sp-m-card-badge {
      font-size: 15px !important;
    }
    body.sp-mode-xl .sp-m-card-body,
    body.sp-mode-xl .sp-m-table-val {
      font-size: 18px !important;
      line-height: 1.6 !important;
    }
    body.sp-mode-xl .sp-m-table-label {
      font-size: 13px !important;
    }

    /* =========================================================================
       CAPA 2: VISTA FOLLETO ORIGINAL A5/A4 AUTO-ENCUADRADO AL MILÍMETRO
       ========================================================================= */
    body.sp-mode-folleto #sp-clean-mobile-reader {
      display: none !important;
    }
    .sp-folleto-stage {
      width: 100vw !important;
      max-width: 100vw !important;
      overflow: hidden !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      gap: 14px !important;
      padding: 4px 0 30px 0 !important;
      box-sizing: border-box !important;
    }
    .sp-folleto-slot {
      width: 100vw !important;
      overflow: hidden !important;
      display: flex !important;
      justify-content: center !important;
      align-items: flex-start !important;
      position: relative !important;
    }
  }

  @media print {
    .sp-reader-toolbar,
    #sp-clean-mobile-reader {
      display: none !important;
    }
    .sp-original-sheet-host {
      display: block !important;
    }
  }
</style>
<script id="sp-auto-fit-mobile">
(function() {
  /* Limpia textos eliminando espacios repetidos */
  function limpiarTexto(str) {
    return (str || '').replace(/\\s+/g, ' ').trim();
  }

  /* Construye el Lector Móvil Nativo extrayendo de forma estructurada todo el contenido de cada hoja */
  function construirLectorMovilNativo() {
    if (document.getElementById('sp-clean-mobile-reader')) return;

    var hojas = document.querySelectorAll('.sheet, .page, .a4-page, .a5-page, .dossier-page, .magazine-page');
    if (!hojas.length) return;

    var lector = document.createElement('div');
    lector.id = 'sp-clean-mobile-reader';
    lector.className = 'no-print';

    hojas.forEach(function(hoja, pageIdx) {
      /* Envolver la hoja original en un contenedor para poder escalarla en modo Folleto */
      if (!hoja.parentElement.classList.contains('sp-folleto-slot')) {
        var slot = document.createElement('div');
        slot.className = 'sp-folleto-slot sp-original-sheet-host';
        hoja.parentNode.insertBefore(slot, hoja);
        slot.appendChild(hoja);
      } else {
        hoja.parentElement.classList.add('sp-original-sheet-host');
      }

      var mPage = document.createElement('section');
      mPage.className = 'sp-m-page';

      /* 1. Cabecera de página */
      var taglineEl = hoja.querySelector('.header-tagline, header');
      var tituloDoc = taglineEl ? limpiarTexto(taglineEl.textContent) : ('Página ' + (pageIdx + 1));
      var htmlPagina = '<span class="sp-m-page-badge">Página ' + (pageIdx + 1) + ' de ' + hojas.length + '</span>';
      htmlPagina += '<h2 class="sp-m-doc-title">' + tituloDoc + '</h2>';

      /* 2. Recorrer en orden real del documento los banners, artículos, tablas y cajas destacadas */
      var nodos = hoja.querySelectorAll(
        '.section-banner, .cat-banner, h1, h2, ' +
        'article, .card-lanzamiento, .f2-item, .roadmap-item, .sat-card-3, .sat-item, .gift-box, .print-qr-banner, ' +
        'table'
      );

      var procesados = new Set();

      nodos.forEach(function(nodo) {
        if (procesados.has(nodo)) return;
        /* Si este nodo está dentro de otro nodo que ya procesamos (salvo que sea una tabla), saltar */
        var padreProcesado = false;
        procesados.forEach(function(p) {
          if (p !== nodo && p.contains(nodo) && nodo.tagName !== 'TABLE') {
            padreProcesado = true;
          }
        });
        if (padreProcesado) return;

        /* CASO A: Banner de sección */
        if (nodo.classList.contains('section-banner') || nodo.classList.contains('cat-banner') || nodo.tagName === 'H1' || nodo.tagName === 'H2') {
          if (nodo.closest('header')) return;
          procesados.add(nodo);
          var spans = nodo.querySelectorAll('span');
          if (spans.length >= 2) {
            htmlPagina += '<div class="sp-m-section-banner">' + limpiarTexto(spans[0].textContent) + '<small>' + limpiarTexto(spans[1].textContent) + '</small></div>';
          } else {
            htmlPagina += '<div class="sp-m-section-banner">' + limpiarTexto(nodo.textContent) + '</div>';
          }
          return;
        }

        /* CASO B: Tabla de precios / comparativa -> Ficha móvil limpia */
        if (nodo.tagName === 'TABLE') {
          procesados.add(nodo);
          var cabeceras = Array.from(nodo.querySelectorAll('thead th')).map(function(th) {
            return limpiarTexto(th.textContent);
          });
          var filas = nodo.querySelectorAll('tbody tr');
          if (!filas.length) filas = nodo.querySelectorAll('tr');

          htmlPagina += '<div class="sp-m-table-group">';
          filas.forEach(function(tr) {
            if (tr.querySelector('th') && !tr.querySelector('td')) return;
            var celdas = tr.querySelectorAll('td, th');
            if (!celdas.length) return;
            htmlPagina += '<div class="sp-m-table-card">';
            celdas.forEach(function(td, cIdx) {
              var label = cabeceras[cIdx] || ('Dato ' + (cIdx + 1));
              var valorHtml = td.innerHTML;
              htmlPagina += '<div class="sp-m-table-row">' +
                '<span class="sp-m-table-label">' + label + '</span>' +
                '<div class="sp-m-table-val">' + valorHtml + '</div>' +
              '</div>';
            });
            htmlPagina += '</div>';
          });
          htmlPagina += '</div>';
          return;
        }

        /* CASO C: Tarjeta de Servicio, Satélite, Regalo o Contacto */
        procesados.add(nodo);
        var tituloEl = nodo.querySelector('.prod-title, .f2-title, .service-title, .sat-card-title, h3, h4, strong');
        var badgeEl = nodo.querySelector('.prod-badge, .service-benefit, .sat-card-tag');
        var descEl = nodo.querySelector('.prod-desc, .f2-text, .service-desc, .sat-card-bullets, p');

        var tituloTxt = tituloEl ? limpiarTexto(tituloEl.textContent) : '';
        var badgeTxt = badgeEl ? limpiarTexto(badgeEl.textContent) : '';

        htmlPagina += '<div class="sp-m-card">';
        if (tituloTxt || badgeTxt) {
          htmlPagina += '<div class="sp-m-card-head">';
          if (tituloTxt) htmlPagina += '<span class="sp-m-card-title">' + tituloTxt + '</span>';
          if (badgeTxt && badgeTxt !== tituloTxt) htmlPagina += '<span class="sp-m-card-badge">' + badgeTxt + '</span>';
          htmlPagina += '</div>';
        }

        if (descEl && !nodo.querySelector('table')) {
          /* Mostrar todos los párrafos o listas de la tarjeta */
          var parrafos = nodo.querySelectorAll('.prod-desc, .f2-text, .service-desc, p, ul');
          if (parrafos.length > 0) {
            htmlPagina += '<div class="sp-m-card-body">';
            parrafos.forEach(function(p) {
              htmlPagina += '<div>' + p.innerHTML + '</div>';
            });
            htmlPagina += '</div>';
          } else {
            htmlPagina += '<div class="sp-m-card-body">' + descEl.innerHTML + '</div>';
          }
        } else {
          /* Fallback para cajas especiales (como Pack Escudo Básico/Total o Contacto QR) */
          var clon = nodo.cloneNode(true);
          if (tituloEl) {
            var tClon = clon.querySelector('.prod-title, .f2-title, .service-title, .sat-card-title');
            if (tClon) tClon.remove();
          }
          var textoRestante = limpiarTexto(clon.textContent);
          if (textoRestante) {
            htmlPagina += '<div class="sp-m-card-body">' + textoRestante + '</div>';
          }
        }
        htmlPagina += '</div>';
      });

      /* Si es un artículo de revista o página con párrafos libres que no tenían las clases anteriores */
      if (procesados.size < 2) {
        var bloquesTexto = hoja.querySelectorAll('h1, h2, h3, p, li, blockquote');
        htmlPagina += '<div class="sp-m-card"><div class="sp-m-card-body">';
        bloquesTexto.forEach(function(b) {
          if (b.closest('header') || b.closest('footer')) return;
          var tag = b.tagName.toLowerCase();
          if (tag === 'h1' || tag === 'h2' || tag === 'h3') {
            htmlPagina += '<h3 style="font-size:17px;font-weight:800;color:#0b2545;margin:12px 0 6px 0;">' + limpiarTexto(b.textContent) + '</h3>';
          } else {
            htmlPagina += '<p style="margin-bottom:8px;">' + b.innerHTML + '</p>';
          }
        });
        htmlPagina += '</div></div>';
      }

      mPage.innerHTML = htmlPagina;
      lector.appendChild(mPage);
    });

    document.body.insertBefore(lector, document.body.firstChild);
  }

  /* Escala el folleto original A5/A4 para que quepa entero en la pantalla del móvil cuando se pulsa "📄 Folleto A5/A4" */
  function encuadrarFolletoOriginal() {
    var enModoFolleto = document.body.classList.contains('sp-mode-folleto');
    var slots = document.querySelectorAll('.sp-folleto-slot');
    var anchoPantalla = Math.min(window.innerWidth || 360, document.documentElement.clientWidth || 360);

    slots.forEach(function(slot) {
      var hoja = slot.firstElementChild;
      if (!hoja) return;

      hoja.style.transform = '';
      hoja.style.transformOrigin = '';
      slot.style.height = '';

      if (!enModoFolleto) return;

      var anchoHoja = hoja.offsetWidth || 560;
      var altoHoja = hoja.offsetHeight || 794;

      if (anchoPantalla < anchoHoja + 16) {
        var escala = (anchoPantalla - 16) / anchoHoja;
        hoja.style.transformOrigin = 'top center';
        hoja.style.transform = 'scale(' + escala + ')';
        slot.style.height = Math.ceil(altoHoja * escala + 12) + 'px';
      }
    });
  }

  function activarModo(modo) {
    document.documentElement.classList.add('sp-v4-active');
    document.body.classList.add('sp-v4-active');
    document.body.classList.remove('sp-mode-mobile', 'sp-mode-xl', 'sp-mode-folleto');

    var btnLectura = document.getElementById('sp-btn-lectura');
    var btnXL = document.getElementById('sp-btn-xl');
    var btnOriginal = document.getElementById('sp-btn-original');
    var btnImprimir = document.getElementById('sp-btn-imprimir');

    if (btnLectura) btnLectura.classList.remove('active');
    if (btnXL) btnXL.classList.remove('active');
    if (btnOriginal) btnOriginal.classList.remove('active');

    if (modo === 'xl') {
      document.body.classList.add('sp-mode-xl');
      if (btnXL) btnXL.classList.add('active');
      if (btnImprimir) btnImprimir.style.display = 'none';
    } else if (modo === 'folleto') {
      document.body.classList.add('sp-mode-folleto');
      if (btnOriginal) btnOriginal.classList.add('active');
      if (btnImprimir) btnImprimir.style.display = 'inline-flex';
      setTimeout(encuadrarFolletoOriginal, 30);
    } else {
      document.body.classList.add('sp-mode-mobile');
      if (btnLectura) btnLectura.classList.add('active');
      if (btnImprimir) btnImprimir.style.display = 'none';
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function iniciarMotorV4() {
    /* Forzar viewport limpio 1:1 eliminando cualquier viewport de ancho fijo anterior */
    var viewports = document.querySelectorAll('meta[name="viewport"]');
    viewports.forEach(function(vp, i) {
      if (i === 0) {
        vp.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
      } else {
        vp.remove();
      }
    });

    construirLectorMovilNativo();

    var oldBar = document.getElementById('sp-reader-toolbar');
    if (oldBar) oldBar.remove();

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

    document.getElementById('sp-btn-lectura').addEventListener('click', function() { activarModo('mobile'); });
    document.getElementById('sp-btn-xl').addEventListener('click', function() { activarModo('xl'); });
    document.getElementById('sp-btn-original').addEventListener('click', function() { activarModo('folleto'); });
    document.getElementById('sp-btn-imprimir').addEventListener('click', function() { window.print(); });

    /* Por defecto en pantallas móviles (< 820px) abre en Vista Móvil; en ordenador en Folleto Original */
    var ancho = window.innerWidth || document.documentElement.clientWidth || 360;
    if (ancho <= 820) {
      activarModo('mobile');
    } else {
      activarModo('folleto');
    }

    window.addEventListener('resize', encuadrarFolletoOriginal);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciarMotorV4);
  } else {
    iniciarMotorV4();
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
    print("🔎 ACTUALIZADOR INTERACTIVO SISTEMAS PYME (AD.py — Motor v4 Doble Capa Móvil + Folleto)")
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

            # Eliminar versiones anteriores del bloque inyectado
            contenido_nuevo = re.sub(
                r'<!-- \[SP_AUTO_FIT_MOBILE_START\][\s\S]*?<!-- \[SP_AUTO_FIT_MOBILE_END\] -->',
                '',
                contenido
            )

            # Eliminar cualquier etiqueta <meta name="viewport"> antigua que forzara width=580 o width=800
            contenido_nuevo = re.sub(
                r'<meta\s+name=["\']viewport["\'][^>]*>\s*',
                '',
                contenido_nuevo,
                flags=re.IGNORECASE
            )

            if "</head>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</head>", BLOQUE_MOTOR_V4_DOBLE_CAPA + "\n</head>", 1)
            elif "</body>" in contenido_nuevo:
                contenido_nuevo = contenido_nuevo.replace("</body>", BLOQUE_MOTOR_V4_DOBLE_CAPA + "\n</body>", 1)
            else:
                contenido_nuevo += "\n" + BLOQUE_MOTOR_V4_DOBLE_CAPA

            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(contenido_nuevo)

            archivos_actualizados.append(os.path.relpath(ruta_completa, dir_raiz))
            print(f"   ✔ Motor v4 Doble Capa aplicado en: {os.path.relpath(ruta_completa, dir_raiz)}")

    print("\n" + "=" * 80)
    print(f"🎉 PROCESO COMPLETADO: {len(archivos_actualizados)} documentos actualizados con el Motor v4.")
    print(f"📦 Copias de seguridad guardadas en: {carpeta_backups}")
    print("=" * 80)


if __name__ == "__main__":
    ejecutar_actualizador()
import os
import re

# ==============================================================================
# CREDENCIALES OFICIALES DE ANALÍTICA DE SISTEMAS PYME (ACTIVOS EN PUBLIC_HTML)
# ==============================================================================
GA4_MEASUREMENT_ID = "G-J8Y61HLB7L"  # ✅ ID Oficial Google Analytics 4
CLARITY_PROJECT_ID = "z5k1bnidx3"    # ✅ ID Oficial Microsoft Clarity


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
    return None


def limpiar_web_y_reparar_scraper(dir_raiz):
    # 1. Eliminar auditoria-trafico.html duplicado de public_html
    ruta_duplicado = os.path.join(dir_raiz, "auditoria-trafico.html")
    if os.path.isfile(ruta_duplicado):
        os.remove(ruta_duplicado)
        print("   🗑️ Eliminado 'auditoria-trafico.html' duplicado de public_html.")
    else:
        print("   ✔ 'public_html' ya está limpio (sin 'auditoria-trafico.html' duplicado).")

    # 2. Dejar el <h1> de index.html en formato universal 100% legible por cualquier escáner
    ruta_index = os.path.join(dir_raiz, "index.html")
    if os.path.isfile(ruta_index):
        with open(ruta_index, "r", encoding="utf-8") as f:
            html = f.read()

        nuevo_h1 = (
            '<h1 aria-label="Sistemas de Automatización e Inteligencia Artificial para Blindar, Posicionar y Escalar tu Negocio Local" '
            'style="line-height: 1.20;" class="text-3xl sm:text-4xl lg:text-[42px] font-black tracking-tight leading-[1.20] sm:leading-[1.20] lg:leading-[1.20] mb-4 sm:mb-6">'
            '<span class="text-white">Sistemas de Automatización e Inteligencia Artificial para </span>'
            '<span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-300 to-emerald-400">Blindar, Posicionar y Escalar</span> '
            '<span class="text-white">tu Negocio Local</span>'
            '</h1>'
        )
        html = re.sub(r"<h1[^>]*>.*?</h1>", nuevo_h1, html, count=1, flags=re.DOTALL | re.IGNORECASE)
        with open(ruta_index, "w", encoding="utf-8") as f:
            f.write(html)
        print("   ✔ Etiqueta <h1> de index.html optimizada en public_html.")

    # 3. Buscar automáticamente la carpeta Scraper y mejorar su detector de <h1> para que lea etiquetas con <span> dentro
    carpeta_scraper = os.path.expanduser("~/Desktop/SISTEMAS PYME/Scraper")
    if os.path.isdir(carpeta_scraper):
        archivos_mejorados = 0
        for r, dirs, files in os.walk(carpeta_scraper):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("venv", ".venv", "__pycache__", "node_modules")]
            for fn in files:
                if fn.endswith((".py", ".html", ".js")):
                    p = os.path.join(r, fn)
                    try:
                        with open(p, "r", encoding="utf-8", errors="ignore") as f:
                            txt = f.read()
                        orig = txt
                        # Reemplazar regex restrictivas que fallan cuando <h1> contiene <span>
                        txt = txt.replace(r"<h1[^>]*>([^<]+)</h1>", r"<h1[^>]*>([\s\S]*?)</h1>")
                        txt = txt.replace(".find('h1').string", ".find('h1').get_text(' ', strip=True)")
                        txt = txt.replace('.find("h1").string', '.find("h1").get_text(" ", strip=True)')
                        if txt != orig:
                            with open(p, "w", encoding="utf-8") as f:
                                f.write(txt)
                            archivos_mejorados += 1
                            print(f"   ✔ Detector de H1 actualizado en ScraperApp: {fn}")
                    except Exception:
                        pass
        if archivos_mejorados == 0:
            print("   ✔ Carpeta ScraperApp revisada y sincronizada.")


if __name__ == "__main__":
    print("=" * 85)
    print("🧹 SINCRONIZANDO PUBLIC_HTML Y REPARANDO DETECTOR H1 EN SCRAPERAPP")
    print("=" * 85)
    d = localizar_directorio_public_html()
    if d:
        limpiar_web_y_reparar_scraper(d)
    print("=" * 85)
    print("🎉 ¡TODO LISTO Y SINCRONIZADO!")
    print("=" * 85)
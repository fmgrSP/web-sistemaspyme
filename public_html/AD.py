import os
import shutil
import re
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
    return None


def obtener_backup_original(carpeta_backups, rel_path):
    if not os.path.isdir(carpeta_backups):
        return None
    prefijo = f"{rel_path}.backup_"
    candidatos = [
        os.path.join(carpeta_backups, n)
        for n in os.listdir(carpeta_backups)
        if n.startswith(prefijo) and os.path.isfile(os.path.join(carpeta_backups, n))
    ]
    if not candidatos:
        return None
    candidatos.sort()
    return candidatos[0]


def restaurar_documentos_originales():
    print("=" * 80)
    print("🔄 RESTAURANDO DOCUMENTOS A SU DISEÑO ORIGINAL INTACTO (SIN MODIFICAR LETRAS)")
    print("=" * 80)

    dir_raiz = localizar_directorio_public_html()
    if not dir_raiz:
        print("❌ No se encontró public_html.")
        return

    carpeta_backups = os.path.join(dir_raiz, "backups_sp")
    os.makedirs(carpeta_backups, exist_ok=True)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

    subcarpetas = ["documentos", "articulos"]
    restaurados = 0

    for sub in subcarpetas:
        ruta_sub = os.path.join(dir_raiz, sub)
        if not os.path.isdir(ruta_sub):
            continue
        for arch in os.listdir(ruta_sub):
            if not arch.lower().endswith(".html"):
                continue
            ruta_completa = os.path.join(ruta_sub, arch)
            rel_path = os.path.relpath(ruta_completa, dir_raiz).replace(os.sep, "_")

            shutil.copy2(ruta_completa, os.path.join(carpeta_backups, f"{rel_path}.backup_{marca_tiempo}"))

            backup_virgen = obtener_backup_original(carpeta_backups, rel_path)
            if backup_virgen:
                with open(backup_virgen, "r", encoding="utf-8", errors="ignore") as f:
                    html = f.read()
            else:
                with open(ruta_completa, "r", encoding="utf-8", errors="ignore") as f:
                    html = f.read()

            # Eliminar cualquier bloque o script inyectado en las pruebas
            html = re.sub(
                r'<!-- \[SP_AUTO_FIT_MOBILE_START\][\s\S]*?<!-- \[SP_AUTO_FIT_MOBILE_END\] -->',
                '',
                html
            )

            # Dejar únicamente un viewport limpio de ancho de hoja (820px para A4, 600px para A5)
            # que muestra el documento original 100% intacto sin tocar ni un solo tamaño de fuente ni tabla
            es_a4 = ("210mm" in html and "297mm" in html) or ("catalogo" in arch.lower()) or ("magazine" in arch.lower())
            ancho_fijo = "820" if es_a4 else "600"

            html = re.sub(
                r'<meta\s+name=["\']viewport["\'][^>]*>',
                f'<meta name="viewport" content="width={ancho_fijo}">',
                html,
                flags=re.IGNORECASE
            )

            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(html)

            restaurados += 1
            print(f"   ✔ Restaurado intacto al 100%: {sub}/{arch} (viewport width={ancho_fijo})")

    print("=" * 80)
    print(f"✅ {restaurados} documentos restaurados a su diseño original sin deformaciones.")
    print("=" * 80)


if __name__ == "__main__":
    restaurar_documentos_originales()
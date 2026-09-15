"""
RO: Utilitar de import care preia meniul Restaurantului Elite de pe Glovo,
descarcă imaginile produselor și generează un fișier CSV, o pagină HTML de
verificare și informații despre sursă în directorul de ieșire specificat.
Scriptul nu este necesar pentru rularea site-ului și poate necesita actualizare
dacă Glovo își modifică structura paginii.
Utilizare: `python scripts/import_glovo_menu.py OUTPUT_DIRECTORY`.
URL-ul de intrare nu este transmis ca argument; este adresa publică definită
în constanta `SOURCE_URL` din acest fișier. OUTPUT_DIRECTORY este calea către
directorul care va fi creat sau reutilizat. Rezultatele așteptate sunt
`glovo-menu.csv`, `glovo-menu.html`, `SOURCE.txt` și subdirectorul `images/`,
care conține imaginile descărcate. Este necesară o conexiune la internet.

EN: Import utility that retrieves the Hotel Restaurant Elite menu from Glovo,
downloads product images, and generates a CSV file, an HTML preview, and source
information in the specified output directory. The script is not required for
the website to run and may need updating if Glovo changes its page structure.
Usage: `python scripts/import_glovo_menu.py OUTPUT_DIRECTORY`.
The input URL is not supplied as an argument; it is the public address defined
by the `SOURCE_URL` constant in this file. OUTPUT_DIRECTORY is the path to a
directory that will be created or reused. Expected outputs are `glovo-menu.csv`,
`glovo-menu.html`, `SOURCE.txt`, and an `images/` subdirectory containing the
downloaded images. An internet connection is required.
"""

import csv
import html
import re
import sys
import unicodedata
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


SOURCE_URL = "https://glovoapp.com/ro/ro/drobeta-turnu-severin/stores/hotel-restaurant-elite-dts"


def class_contains(attrs, fragment):
    classes = dict(attrs).get("class", "")
    return fragment in classes


class MenuParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.category = ""
        self.items = []
        self.in_product = 0
        self.capture = None
        self.buffer = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "h3" and not self.in_product:
            self.capture = "category"
            self.buffer = []
        if tag == "div" and data.get("data-testid") == "product-row":
            self.in_product = 1
            self.current = {"category": self.category, "name": "", "description": "", "price": "", "image_url": ""}
            return
        if self.in_product and tag == "div":
            self.in_product += 1
        if not self.in_product:
            return
        if tag == "img" and not self.current["image_url"]:
            self.current["image_url"] = data.get("src", "")
        elif tag == "p" and class_contains(attrs, "pintxo-typography-body1"):
            self.capture = "name"
            self.buffer = []
        elif tag == "p" and class_contains(attrs, "ItemRow_description"):
            self.capture = "description"
            self.buffer = []
        elif tag == "span" and class_contains(attrs, "pintxo-typography-body2") and not self.current["price"]:
            self.capture = "price"
            self.buffer = []

    def handle_endtag(self, tag):
        if self.capture == "category" and tag == "h3":
            value = " ".join("".join(self.buffer).split())
            if value:
                self.category = value
            self.capture = None
        elif self.in_product and self.capture == "name" and tag == "p":
            self.current["name"] = " ".join("".join(self.buffer).split())
            self.capture = None
        elif self.in_product and self.capture == "description" and tag == "p":
            self.current["description"] = " ".join("".join(self.buffer).split())
            self.capture = None
        elif self.in_product and self.capture == "price" and tag == "span":
            self.current["price"] = " ".join("".join(self.buffer).split())
            self.capture = None
        if self.in_product and tag == "div":
            self.in_product -= 1
            if self.in_product == 0:
                if self.current and self.current["name"]:
                    self.items.append(self.current)
                self.current = None
                self.capture = None

    def handle_data(self, data):
        if self.capture:
            self.buffer.append(data)


def safe_name(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value[:80] or "produs"


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: import_glovo_menu.py OUTPUT_DIRECTORY")
    output = Path(sys.argv[1])
    images = output / "images"
    output.mkdir(parents=True, exist_ok=True)
    images.mkdir(parents=True, exist_ok=True)

    page = fetch(SOURCE_URL).decode("utf-8", errors="replace")
    parser = MenuParser()
    parser.feed(page)
    items = parser.items
    if not items:
        raise RuntimeError("No menu products were found in the Glovo page.")

    used_names = {}
    for item in items:
        item["local_image"] = ""
        if not item["image_url"]:
            continue
        stem = safe_name(item["name"])
        used_names[stem] = used_names.get(stem, 0) + 1
        suffix = "" if used_names[stem] == 1 else f"-{used_names[stem]}"
        extension = Path(urlparse(item["image_url"]).path).suffix.lower()
        if extension not in {".jpg", ".jpeg", ".png", ".webp", ".avif"}:
            extension = ".jpg"
        filename = f"{stem}{suffix}{extension}"
        try:
            (images / filename).write_bytes(fetch(item["image_url"]))
            item["local_image"] = f"images/{filename}"
        except Exception as exc:
            item["local_image"] = f"DOWNLOAD_ERROR: {exc}"

    with (output / "glovo-menu.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["category", "name", "description", "price", "local_image", "image_url"])
        writer.writeheader()
        writer.writerows(items)

    categories = []
    for item in items:
        if not categories or categories[-1][0] != item["category"]:
            categories.append((item["category"], []))
        categories[-1][1].append(item)
    sections = []
    for category, category_items in categories:
        cards = []
        for item in category_items:
            image_markup = ""
            if item["local_image"] and not item["local_image"].startswith("DOWNLOAD_ERROR"):
                image_markup = f'<img src="{html.escape(item["local_image"])}" alt="{html.escape(item["name"])}">'
            cards.append(
                '<article class="item">'
                f'{image_markup}<div><h3>{html.escape(item["name"])}</h3>'
                f'<strong>{html.escape(item["price"])}</strong>'
                f'<p>{html.escape(item["description"])}</p></div></article>'
            )
        sections.append(f'<section><h2>{html.escape(category)}</h2>{"".join(cards)}</section>')
    imported_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    document = f'''<!doctype html>
<html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Meniu Hotel Restaurant Elite — Glovo snapshot</title>
<style>body{{max-width:1100px;margin:40px auto;padding:0 20px;font:16px/1.5 Arial;color:#222}}h1,h2{{font-family:Georgia,serif}}section{{margin:40px 0}}.item{{display:grid;grid-template-columns:120px 1fr;gap:18px;padding:18px 0;border-bottom:1px solid #ddd}}.item img{{width:120px;height:120px;object-fit:cover;border-radius:8px}}.item h3{{margin:0 0 6px}}.item p{{margin:8px 0;color:#555}}@media(max-width:600px){{.item{{grid-template-columns:80px 1fr}}.item img{{width:80px;height:80px}}}}</style></head>
<body><h1>Meniu Hotel Restaurant Elite</h1><p>Snapshot importat de pe <a href="{html.escape(SOURCE_URL)}">Glovo</a> la {html.escape(imported_at)}. Prețurile și disponibilitatea se pot modifica.</p>{''.join(sections)}</body></html>'''
    (output / "glovo-menu.html").write_text(document, encoding="utf-8")
    (output / "SOURCE.txt").write_text(
        f"Source: {SOURCE_URL}\nImported: {imported_at}\nProducts: {len(items)}\n",
        encoding="utf-8",
    )
    print(f"Exported {len(items)} product rows to {output}")


if __name__ == "__main__":
    main()

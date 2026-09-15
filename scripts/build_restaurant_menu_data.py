"""
RO: Utilitar de administrare care transformă un fișier CSV cu preparatele
restaurantului în `js/restaurant-menu-data.js`, fișierul de date folosit de
pagina Meniu. Scriptul nu este necesar pentru rularea site-ului. Atenție:
rularea lui suprascrie fișierul JS de destinație cu datele din CSV.
Utilizare: `python scripts/build_restaurant_menu_data.py INPUT_CSV OUTPUT_JS`.
INPUT_CSV este calea către un fișier CSV UTF-8 cu antetele obligatorii
`category`, `name`, `description`, `price` și `local_image`. OUTPUT_JS este
calea fișierului JavaScript care va fi creat sau suprascris; pentru site-ul
actual, rezultatul așteptat este `js/restaurant-menu-data.js`. Imaginile nu
sunt copiate: numele din `local_image` trebuie să corespundă unor fișiere
existente în `images/Menu/Restaurant/`.

EN: Maintenance utility that converts a CSV file containing the restaurant
menu into `js/restaurant-menu-data.js`, the data file used by the Menu page.
The script is not required for the website to run. Warning: running it
overwrites the destination JS file with the data from the CSV source.
Usage: `python scripts/build_restaurant_menu_data.py INPUT_CSV OUTPUT_JS`.
INPUT_CSV is the path to a UTF-8 CSV file with the required headers `category`,
`name`, `description`, `price`, and `local_image`. OUTPUT_JS is the path of the
JavaScript file to create or overwrite; for the current website, the expected
output is `js/restaurant-menu-data.js`. Images are not copied: filenames from
`local_image` must match existing files in `images/Menu/Restaurant/`.
"""

import csv
import json
import sys
from pathlib import Path


if len(sys.argv) != 3:
    raise SystemExit("Usage: build_restaurant_menu_data.py INPUT_CSV OUTPUT_JS")

source = Path(sys.argv[1])
destination = Path(sys.argv[2])
with source.open(encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

items = [
    {
        "category": row["category"],
        "name": row["name"],
        "description": row["description"],
        "price": row["price"],
        "image": "images/Menu/Restaurant/" + Path(row["local_image"]).name,
    }
    for row in rows
]

destination.write_text(
    "window.restaurantMenuData = " + json.dumps(items, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)
print(f"Generated {len(items)} menu items in {destination}")

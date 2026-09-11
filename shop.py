import os
import io
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageOps

API_KEY = os.environ["FORTNITE_API_KEY"]

url = "https://fortnite-api.com/v2/shop"
headers = {"Authorization": API_KEY}

response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()
data = response.json()

entries = data.get("data", {}).get("entries", [])

today = datetime.now(ZoneInfo("Europe/Madrid")).strftime("%Y-%m-%d")

skins = []
seen = set()

for item in entries:
    in_date = item.get("inDate", "")

    if not in_date.startswith(today):
        continue

    price = item.get("finalPrice") or item.get("regularPrice") or 0

    for cosmetic in item.get("brItems", []):
        if cosmetic.get("type", {}).get("value") != "outfit":
            continue

        skin_id = cosmetic.get("id")

        if not skin_id or skin_id in seen:
            continue

        seen.add(skin_id)

        skins.append({
            "name": cosmetic.get("name", "Sin nombre"),
            "price": price,
            "icon": cosmetic.get("images", {}).get("icon")
        })

skins = skins[:7]

if not skins:
    raise Exception("No se encontraron outfits para hoy.")

# ---------- IMAGEN ----------

W, H = 1920, 1080

img = Image.new("RGB", (W, H), "#0B0D10")
draw = ImageDraw.Draw(img)

font_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

title_font = ImageFont.truetype(font_bold, 58)
subtitle_font = ImageFont.truetype(font_bold, 32)
name_font = ImageFont.truetype(font_bold, 25)
price_font = ImageFont.truetype(font_bold, 24)
footer_font = ImageFont.truetype(font_bold, 30)

cyan = "#00D9FF"
white = "#FFFFFF"
card_bg = "#181818"

def centered_text(text, y, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    width = box[2] - box[0]
    draw.text(((W - width) / 2, y), text, font=font, fill=fill)

centered_text("TIENDA DE FORTNITE", 45, title_font, white)
centered_text("NUEVAS SKINS DE HOY", 115, subtitle_font, cyan)

draw.line((70, 190, 1850, 190), fill=cyan, width=3)

# ---------- TARJETAS ----------

positions = [
    (70, 230),
    (530, 230),
    (990, 230),
    (1450, 230),
    (300, 590),
    (760, 590),
    (1220, 590)
]

for skin, (x, y) in zip(skins, positions):

    draw.rounded_rectangle(
        (x, y, x + 420, y + 310),
        radius=24,
        fill=card_bg,
        outline=cyan,
        width=3
    )

    icon_url = skin.get("icon")

    if icon_url:
        try:
            icon_response = requests.get(icon_url, timeout=20)
            icon_response.raise_for_status()

            icon = Image.open(
                io.BytesIO(icon_response.content)
            ).convert("RGBA")

            icon = ImageOps.contain(icon, (180, 220))

            icon_x = x + 20 + (180 - icon.width) // 2
            icon_y = y + 20 + (220 - icon.height) // 2

            img.paste(icon, (icon_x, icon_y), icon)

        except Exception:
            pass

    name = skin["name"]

    # Cortar nombres demasiado largos
    if len(name) > 18:
        name = name[:17] + "…"

    draw.text(
        (x + 220, y + 80),
        name,
        font=name_font,
        fill=white
    )

    draw.text(
        (x + 220, y + 140),
        f'{skin["price"]} V-BUCKS',
        font=price_font,
        fill=cyan
    )

centered_text("TANROX", 1015, footer_font, cyan)

img.save("tienda-fortnite.png", "PNG")

print("Imagen creada correctamente.")

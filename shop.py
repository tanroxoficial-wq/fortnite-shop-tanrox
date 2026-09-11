img.save("tienda-fortnite.png", "PNG")

print("Imagen creada correctamente.")


# ---------- ENVIAR A DISCORD ----------

webhook = os.environ.get("DISCORD_WEBHOOK_URL")

if webhook:
    mensaje = (
        "🔥 NUEVA TIENDA DE FORTNITE 🔥\n\n"
        "🛒 Mejores skins de la tienda de hoy\n"
        "⭐ Apoya a un creador: TANROX\n"
        "🎮 Usa mi código TANROX en la tienda de Fortnite"
    )

    with open("tienda-fortnite.png", "rb") as image:
        response = requests.post(
            webhook,
            files={
                "file": (
                    "tienda-fortnite.png",
                    image,
                    "image/png"
                )
            },
            data={
                "content": mensaje
            },
            timeout=30
        )

    response.raise_for_status()
    print("Imagen enviada a Discord correctamente.")

else:
    print("ERROR: No existe DISCORD_WEBHOOK_URL")

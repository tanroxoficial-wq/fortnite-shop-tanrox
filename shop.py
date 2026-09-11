# ---------- TEST DISCORD ----------

webhook = os.environ.get("DISCORD_WEBHOOK_URL")

print("Webhook encontrado:", bool(webhook))

if webhook:
    r = requests.post(
        webhook,
        json={
            "content": "🔥 Prueba automática TANROX funcionando"
        },
        timeout=30
    )

    print("Discord respuesta:", r.status_code)
    print(r.text)

else:
    print("NO HAY WEBHOOK")

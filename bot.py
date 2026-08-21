import os
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

FISIER_CONTOR = "contor_bilet.txt"
VALOARE_INITIALA_BILET = 38780885

def citeste_numar_bilet() -> int:
    if os.path.exists(FISIER_CONTOR):
        try:
            with open(FISIER_CONTOR, "r") as f:
                return int(f.read().strip())
        except ValueError:
            pass
    return VALOARE_INITIALA_BILET

def salveaza_numar_bilet(numar: int):
    with open(FISIER_CONTOR, "w") as f:
        f.write(str(numar))

async def genereaza_bilet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numar_bord = update.message.text.strip()

    if not (numar_bord.isdigit() and len(numar_bord) == 4):
        await update.message.reply_text("Te rog să trimiți un număr de bord valid din 4 cifre (ex: 3898).")
        return

    await update.message.reply_text("Solicitarea este in curs de procesare.")

    numar_bilet_curent = citeste_numar_bilet()

    # Ora Moldovei (UTC+3)
    acum_moldova = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3)
    data_str = acum_moldova.strftime("%d.%m.%Y")
    ora_str = acum_moldova.strftime("%H:%M")

    mesaj_bilet = (
        f"Bilet electronic nr.\n"
        f"{numar_bilet_curent}\n"
        f"Data {data_str} ora {ora_str}\n"
        f"Valabil 1 ora\n"
        f"Pret 7 MDL\n"
        f"Numar de bord {numar_bord}"
    )

    salveaza_numar_bilet(numar_bilet_curent + 1)
    await update.message.reply_text(mesaj_bilet)

if __name__ == "__main__":
    TOKEN = "8973901312:AAF0jq2rfuqHe1ltkgVR7fsdoqlvhs6aw-c"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, genereaza_bilet))
    print("--- BOT 1 ACTIV ---")
    app.run_polling()
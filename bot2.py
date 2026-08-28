import logging
import random
from datetime import datetime, timedelta, timezone
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8617433370:AAEPxL8kPhTFpkMhI1ohu9K8FIGvzJaF1c8"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Dicționar pentru a păstra ultimele 4 cifre pentru fiecare număr de bord în parte
borde_memorate = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global borde_memorate
    text = update.message.text.strip()
    
    if text.isdigit() and len(text) == 4:
        # Dacă numărul de bord a mai fost trimis, adăugăm +1
        if text in borde_memorate:
            borde_memorate[text] += 1
            if borde_memorate[text] > 9999:
                borde_memorate[text] = 1000
        else:
            # Dacă e prima dată când îl trimiți, generăm un număr random din 4 cifre
            borde_memorate[text] = random.randint(1000, 9900)
            
        ultimele_cifre = borde_memorate[text]
        bilet_nr = f"{text}{ultimele_cifre:04d}"
        
        # Ora curentă Moldovei minus 5 minute (UTC+3)
        acum_minus_5 = (datetime.now(timezone.utc) + timedelta(hours=3)) - timedelta(minutes=5)
        data_str = acum_minus_5.strftime("%d.%m.%Y")
        ora_str = acum_minus_5.strftime("%H:%M")
        
        # Formatare exactă cu spații înainte de linii
        mesaj_raspuns = (
            f"Bilet electronic nr. \n"
            f" {bilet_nr} \n"
            f" Data {data_str} ora {ora_str} \n"
            f" Valabil 1 ora \n"
            f" Pret 7 MDL \n"
            f" Numar de bord {text}"
        )
        await update.message.reply_text(mesaj_raspuns)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
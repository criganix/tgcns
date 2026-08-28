import logging
import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Token-ul tău pentru Bot 1
TOKEN = "8973901312:AAF0jq2rfuqHe1ltkgVR7fsdoqlvhs6aw-c"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Număr de pornire pentru ultimele 4 cifre (yyyy)
last_yyyy_seq = random.randint(1000, 3000)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_yyyy_seq
    text = update.message.text.strip()
    
    # Verificăm dacă mesajul conține exact 4 cifre
    if text.isdigit() and len(text) == 4:
        # Incrementăm haotic ultimele 4 cifre (ex: cu o valoare aleatorie între 15 și 120)
        last_yyyy_seq += random.randint(15, 120)
        if last_yyyy_seq > 9999:
            last_yyyy_seq = random.randint(1000, 2000)
            
        # Formăm numărul biletului: primele 4 cifre sunt numărul introduse, ultimele 4 sunt cele haotice
        bilet_nr = f"{text}{last_yyyy_seq:04d}"
        
        # Bot 1: Ora curentă în EEST (UTC+3)
        acum = datetime.utcnow() + timedelta(hours=3)
        data_str = acum.strftime("%d.%m.%Y")
        ora_str = acum.strftime("%H:%M")
        
        mesaj_raspuns = (
            f"Bilet electronic nr. {bilet_nr}\n"
            f"Data {data_str} ora {ora_str}\n"
            f"Valabil 1 ora\n"
            f"Pret 7 MDL\n"
            f"Numar de bord {text}"
        )
        await update.message.reply_text(mesaj_raspuns)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
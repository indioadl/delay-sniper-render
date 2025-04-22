
from flask import Flask, request, render_template
import os
import telegram
from telegram.ext import Dispatcher, CommandHandler
from comandos_telegram import start, help_command, esportes_command, ultimos, status, parar, oddsatual
from delay_sniper_odds import iniciar_sniper
from threading import Thread

TOKEN = os.getenv("TOKEN_TELEGRAM")
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

# Handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("esportes", esportes_command))
dispatcher.add_handler(CommandHandler("ultimos", ultimos))
dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(CommandHandler("parar", parar))
dispatcher.add_handler(CommandHandler("oddsatual", oddsatual))

@app.route("/")
def home():
    return render_template("painel.html")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    Thread(target=iniciar_sniper).start()
    app.run(host="0.0.0.0", port=10000)

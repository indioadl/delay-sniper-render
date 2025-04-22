
import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from comandos_telegram import iniciar_comandos_telegram

TOKEN = os.getenv("TOKEN_TELEGRAM")
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return "Delay Sniper Bot com Webhook ativo!"

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp = Dispatcher(bot, None, use_context=True)
    iniciar_comandos_telegram(dp)
    dp.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

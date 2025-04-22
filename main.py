from flask import Flask, request
import telegram
import os
from delay_sniper_odds import buscar_eventos, detectar_oportunidade

TOKEN = os.environ.get("TOKEN_TELEGRAM")
CHAT_ID = os.environ.get("CHAT_ID")
ODDS_API_KEY = os.environ.get("ODDS_API_KEY")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Delay Sniper via Webhook rodando!"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        text = update.message.text

        if text == "/start":
            bot.send_message(chat_id=chat_id, text="Bot Webhook Delay Sniper ativo!")
        return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
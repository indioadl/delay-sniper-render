
import os
from flask import Flask, request
import telegram

TOKEN = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")
BOT = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Delay Sniper Rodando com Webhook!"

@app.route(f"/{TOKEN}", methods=['POST'])
def receive_update():
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    chat_id = update.message.chat_id
    text = update.message.text
    if text == "/start":
        BOT.send_message(chat_id=chat_id, text="🤖 Delay Sniper Bot ativado com Webhook!")
    return "ok"

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)

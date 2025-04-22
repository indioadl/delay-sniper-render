
import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher
from comandos_telegram import iniciar_comandos_telegram
from delay_sniper_odds import buscar_eventos, detectar_oportunidade
from threading import Thread
import time

# Carrega variáveis de ambiente
TOKEN = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Delay Sniper Webhook ativo!"

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp = Dispatcher(bot, None, use_context=True)
    iniciar_comandos_telegram(dp)
    dp.process_update(update)
    return 'ok'

def monitorar_sniper():
    ESPORTES = ["soccer", "tennis", "basketball", "table_tennis", "csgo", "volleyball", "cricket", "ufc"]
    INTERVALO = 60  # segundos
    while True:
        try:
            for esporte in ESPORTES:
                eventos = buscar_eventos(esporte)
                if eventos:
                    detectar_oportunidade(eventos, esporte)
            time.sleep(INTERVALO)
        except Exception as e:
            print(f"[ERRO GERAL]: {e}")
            time.sleep(5)

if __name__ == '__main__':
    Thread(target=monitorar_sniper).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))


from flask import Flask, request
import telegram
import os
from threading import Thread
import time

from comandos_telegam import iniciar_comandos_telegram
from delay_sniper_odds import buscar_eventos, detectar_oportunidade

TOKEN = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
CHECK_INTERVAL = 5  # segundos
ESPORTES = ["soccer", "tennis", "basketball", "volleyball"]

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    bot.process_new_updates([update])
    return 'ok'

@app.route('/')
def home():
    return "Delay Sniper com Webhook Rodando!"

def delay_sniper_loop():
    print("BOT DELAY SNIPER INICIADO COM WEBHOOK...")
    while True:
        try:
            for esporte in ESPORTES:
                dados = buscar_eventos(esporte)
                if dados:
                    detectar_oportunidade(dados, esporte)
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"[ERRO GERAL] {e}")
            time.sleep(5)

if __name__ == "__main__":
    Thread(target=iniciar_comandos_telegram).start()
    Thread(target=delay_sniper_loop).start()
    app.run(host='0.0.0.0', port=8080)

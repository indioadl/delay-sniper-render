
import os
import time
from flask import Flask, request, render_template
from telegram import Bot, Update
from telegram.ext import Dispatcher
from comandos_telegram import iniciar_comandos_telegram
from delay_sniper_odds import buscar_eventos, detectar_oportunidade
from threading import Thread

# Inicializações
TOKEN = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)
app = Flask(__name__, template_folder="templates")

# Variáveis globais para painel
ULTIMOS_ALERTAS = []
ODDS_MINIMA = 1.80
ESPORTES_MONITORADOS = [
    "soccer", "tennis", "basketball", "table_tennis", "csgo", "volleyball", "cricket", "ufc"
]

@app.route("/")
def home():
    return "🤖 Webhook Delay Sniper ativo!"

@app.route("/painel")
def painel():
    return render_template("painel.html",
        esportes=", ".join([e.replace("_", " ").title() for e in ESPORTES_MONITORADOS]),
        odds=ODDS_MINIMA,
        total=len(ULTIMOS_ALERTAS),
        alertas=ULTIMOS_ALERTAS[-10:][::-1]
    )

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp = Dispatcher(bot, None, use_context=True)
    iniciar_comandos_telegram(dp)
    dp.process_update(update)
    return "ok"

def monitorar_sniper():
    while True:
        try:
            for esporte in ESPORTES_MONITORADOS:
                eventos = buscar_eventos(esporte)
                if eventos:
                    for evento in eventos:
                        alerta = detectar_oportunidade(evento, esporte)
                        if alerta:
                            ULTIMOS_ALERTAS.append({
                                "evento": alerta.get("evento"),
                                "esporte": alerta.get("esporte"),
                                "odds": alerta.get("odds"),
                                "horario": alerta.get("horario")
                            })
            time.sleep(60)
        except Exception as e:
            print(f"Erro no monitoramento: {e}")
            time.sleep(5)

if __name__ == '__main__':
    Thread(target=monitorar_sniper).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

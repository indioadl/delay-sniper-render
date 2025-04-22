from flask import Flask
from threading import Thread
from comandos_telegram import iniciar_comandos_telegram
from delay_sniper_odds import iniciar_sniper

app = Flask(__name__)

@app.route("/")
def home():
    return "Delay Sniper Rodando com sucesso!"

if __name__ == "__main__":
    Thread(target=iniciar_comandos_telegram).start()
    Thread(target=iniciar_sniper).start()
    app.run(host="0.0.0.0", port=8080)

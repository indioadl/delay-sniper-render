
import os
import requests
from telegram import Bot

TOKEN = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
bot = Bot(token=TOKEN)

# Esportes com maior volume de eventos ao vivo + UFC
ESPORTES = ["soccer", "tennis", "basketball", "table_tennis", "csgo", "volleyball", "cricket", "ufc"]
CHECK_INTERVAL = 60  # segundos

def buscar_eventos(esporte):
    url = f"https://api.the-odds-api.com/v4/sports/{esporte}/odds/?regions=eu&markets=h2h&oddsFormat=decimal&apiKey={ODDS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar odds de {esporte}: {response.text}")
        return []

def detectar_oportunidade(eventos, esporte):
    for evento in eventos:
        time_casa = evento.get("home_team", "Time Casa")
        time_fora = evento.get("away_team", "Time Visitante")
        site = next((b for b in evento.get("bookmakers", []) if b.get("title") == "Bet365"), None)

        if site and site.get("markets"):
            odds = site["markets"][0]["outcomes"]
            if len(odds) >= 2:
                odd_casa = odds[0].get("price")
                odd_fora = odds[1].get("price")

                if odd_casa >= 1.80 and odd_fora >= 1.80:
                    mensagem = (
                        f"⚠️ *ALERTA DELAY SNIPER* ⚠️\n"
                        f"*{time_casa}* x *{time_fora}*\n"
                        f"🏅 Esporte: *{esporte.upper()}*\n"
                        f"📊 Odds: {odd_casa} x {odd_fora}"
                    )
                    bot.send_message(
                        chat_id=CHAT_ID,
                        text=mensagem,
                        parse_mode='Markdown',
                        reply_markup={
                            "inline_keyboard": [
                                [{"text": "🔗 Apostar Agora!", "url": "https://www.bet365.com/#/IP/B1"}]
                            ]
                        }
                    )

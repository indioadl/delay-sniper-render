
import requests, os, time
import telegram
from comandos_telegram import salvar_alerta, bot_ativo

TOKEN = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
bot = telegram.Bot(token=TOKEN)

ESPORTES = ["soccer", "tennis", "basketball", "mma", "boxing", "volleyball", "baseball", "icehockey", "rugby", "tabletennis"]
ODDS_MIN = 1.70
ODDS_MAX = 3.50
URL_BASE = "https://api.the-odds-api.com/v4/sports/{}/odds/?apiKey={}&regions=eu&markets=h2h&oddsFormat=decimal"

def iniciar_sniper():
    while True:
        try:
            if not bot_ativo():
                time.sleep(10)
                continue
            for esporte in ESPORTES:
                url = URL_BASE.format(esporte, ODDS_API_KEY)
                r = requests.get(url)
                if r.status_code == 200:
                    for jogo in r.json():
                        teams = jogo.get("teams", ["Time A", "Time B"])
                        site = next((s for s in jogo.get("bookmakers", []) if s["title"] == "Bet365"), None)
                        if not site: continue
                        mercados = site["markets"][0]["outcomes"]
                        for outcome in mercados:
                            if ODDS_MIN <= outcome["price"] <= ODDS_MAX:
                                mensagem = (
                                    f"⚠️ *Alerta de ODD Real*\n"
                                    f"🏆 Esporte: {esporte.capitalize()}\n"
                                    f"🆚 Jogo: {teams[0]} x {teams[1]}\n"
                                    f"📈 Aposta: {outcome['name']}\n"
                                    f"💸 Odd: *{outcome['price']}*"
                                )
                                bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode="Markdown", reply_markup=telegram.InlineKeyboardMarkup(
                                    [[telegram.InlineKeyboardButton("🔗 Apostar na Bet365", url="https://www.bet365.com/#/IP/B1")]]
                                ))
                                salvar_alerta(mensagem)
                time.sleep(1)
            time.sleep(60)
        except Exception as e:
            print("[Erro sniper]", e)
            time.sleep(10)

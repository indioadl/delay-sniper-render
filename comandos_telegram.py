
from telegram import Update
from telegram.ext import CallbackContext
import time
import os

# Variáveis globais de estado do bot
ULTIMOS_ALERTAS = []
STATUS_BOT = {"ativo": True, "ultimo_alerta": "Nenhum alerta ainda"}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 Bem-vindo ao Delay Sniper Bot! Use /help para ver os comandos disponíveis.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("""📌 Comandos disponíveis:
/start – Inicia o bot
/help – Mostra os comandos
/esportes – Lista os esportes monitorados
/ultimos – Mostra os últimos alertas enviados
/status – Mostra o status atual do bot
/parar – Pausa temporariamente o sniper
/oddsatual – Retorna a odd atual de um jogo (em construção)
""")

def esportes_command(update: Update, context: CallbackContext):
    esportes = [
        "⚽ Soccer", "🎾 Tennis", "🏀 Basketball", "🥊 MMA", "🥋 Boxing",
        "🏐 Volleyball", "⚾ Baseball", "🏒 Ice Hockey", "🏉 Rugby", "🏓 Table Tennis"
    ]
    update.message.reply_text("📊 Esportes monitorados:
" + "\n".join(esportes))

def ultimos(update: Update, context: CallbackContext):
    if ULTIMOS_ALERTAS:
        mensagens = "\n\n".join(ULTIMOS_ALERTAS[-5:])
        update.message.reply_text(f"📩 Últimos alertas:\n\n{mensagens}")
    else:
        update.message.reply_text("⛔ Ainda não houve alertas.")

def status(update: Update, context: CallbackContext):
    estado = "🟢 Ativo" if STATUS_BOT["ativo"] else "🔴 Pausado"
    ultimo = STATUS_BOT["ultimo_alerta"]
    update.message.reply_text(f"📡 Status do Bot: {estado}\n⏱️ Último alerta: {ultimo}")

def parar(update: Update, context: CallbackContext):
    STATUS_BOT["ativo"] = False
    update.message.reply_text("⛔ Delay Sniper pausado temporariamente.")

def oddsatual(update: Update, context: CallbackContext):
    update.message.reply_text("🔎 Esse comando ainda está em construção. Em breve você poderá consultar odds específicas!")

# Funções para serem usadas no delay_sniper_odds.py
def salvar_alerta(mensagem):
    ULTIMOS_ALERTAS.append(mensagem)
    STATUS_BOT["ultimo_alerta"] = time.strftime('%H:%M:%S')
    if len(ULTIMOS_ALERTAS) > 20:
        ULTIMOS_ALERTAS.pop(0)

def bot_ativo():
    return STATUS_BOT["ativo"]


from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackContext
import os

TOKEN = os.getenv("TOKEN_TELEGRAM")

# Valores fixos (podem ser importados de config no futuro)
ESPORTES = ["soccer", "tennis", "basketball"]
ODDS_MINIMA = 1.80

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🤖 Bot Delay Sniper via Webhook ativo!")

def status(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Status: Online e monitorando oportunidades!")

def ajuda(update: Update, context: CallbackContext):
    comandos = (
        "*Comandos disponíveis:*
"
        "/start - Inicia o bot
"
        "/status - Verifica se o sniper está ativo
"
        "/ajuda - Mostra os comandos disponíveis
"
        "/esportes - Esportes monitorados
"
        "/odds - Odds mínimas configuradas"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=comandos, parse_mode='Markdown')

def esportes(update: Update, context: CallbackContext):
    lista = "\n".join([f"• {e.capitalize()}" for e in ESPORTES])
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"🎯 Esportes monitorados:
{lista}")

def odds(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"📊 Odds mínimas configuradas: {ODDS_MINIMA}")

def iniciar_comandos_telegram(dp):
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("ajuda", ajuda))
    dp.add_handler(CommandHandler("esportes", esportes))
    dp.add_handler(CommandHandler("odds", odds))

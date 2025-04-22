
from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackContext
import os

TOKEN = os.getenv("TOKEN_TELEGRAM")

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🤖 Bot Delay Sniper via Webhook ativo!")

def status(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Status: Online e monitorando oportunidades!")

def ajuda(update: Update, context: CallbackContext):
    comandos = (
        "/start - Inicia o bot\n"
        "/status - Verifica se o sniper está ativo\n"
        "/ajuda - Mostra os comandos disponíveis"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=comandos)

def iniciar_comandos_telegram(dp):
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("ajuda", ajuda))

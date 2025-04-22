from telegram.ext import Updater, CommandHandler
import os

TOKEN = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Delay Sniper está online!")

def iniciar_comandos_telegram():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()

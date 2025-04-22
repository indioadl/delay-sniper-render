
from telegram import Update, Bot
from telegram.ext import CommandHandler, Dispatcher, CallbackContext
import os

TOKEN = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot Delay Sniper ativo!")

def iniciar_comandos_telegram():
    dispatcher.add_handler(CommandHandler("start", start))

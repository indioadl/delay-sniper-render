
from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 Bem-vindo ao Delay Sniper Bot! Use /help para ver os comandos disponíveis.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("""📌 Comandos disponíveis:
/start – Inicia o bot
/help – Mostra os comandos
/esportes – Lista os esportes monitorados
""")

def esportes_command(update: Update, context: CallbackContext):
    esportes = [
        "⚽ Soccer", "🎾 Tennis", "🏀 Basketball", "🥊 MMA", "🥋 Boxing",
        "🏐 Volleyball", "⚾ Baseball", "🏒 Ice Hockey", "🏉 Rugby", "🏓 Table Tennis"
    ]
    update.message.reply_text("📊 Esportes monitorados:
" + "\n".join(esportes))

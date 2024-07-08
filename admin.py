from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from tel import bot

async def handle_admin_text(update:Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    
    await update.message.reply_text('This button is handled.')
    
bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_text))
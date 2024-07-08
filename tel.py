import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from django.conf import settings
import django
import os
import sys
from asgiref.sync import sync_to_async

TOKEN = "6800524763:AAFOLsyu0ZTDvPruWhNNdtoU1yTcbvKI_KY"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import TelegramUser, Products

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
        user_id=user_id,
        defaults={'chat_id': chat_id}
    )
    
    keyboard = [
        ["Categories", "Button 2"],
        ["Button 3", "Button 4"],
        ["Button 5", "Button 6"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)
        
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text

    if text == "Categories":
        inline_keyboard = [
            [InlineKeyboardButton(f"Platform: {platform}", callback_data=f"platform_{platform.lower()}")]
            for platform in ['INSTAGRAM', 'TELEGRAM', 'RUBICA']
        ]
        inline_reply_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_text('Choose one of the inline options:', reply_markup=inline_reply_markup)
        
    else:
        await update.message.reply_text('This button is not handled yet.')

async def platform_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    platform = query.data.split('_')[1].upper()
    
    products = await sync_to_async(list)(Products.objects.filter(Platform=platform))
    if products:
        inline_keyboard = [
            [InlineKeyboardButton(product.Name, callback_data=f"product_{product.id}")] 
            for product in products            
        ]
        inline_keyboard.append( [InlineKeyboardButton("back", callback_data="category"),
             InlineKeyboardButton("close", callback_data="close")])
    else:
        inline_keyboard = [
            [InlineKeyboardButton("There is no product.", callback_data=" ")],
            [InlineKeyboardButton("back", callback_data="category"),
             InlineKeyboardButton("close", callback_data="close")]
        ]
        
    inline_reply_markup = InlineKeyboardMarkup(inline_keyboard)
    
    await query.edit_message_text(text=f"Products for {platform}:", reply_markup=inline_reply_markup)

async def product_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    product_id = int(query.data.split('_')[1])
    product = await sync_to_async(Products.objects.get)(id=product_id)
    
    await query.answer(text=f"Product: {product.Name}\nPrice: {product.Price}", show_alert=True)
    
    

async def close_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("closed.")
    
async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    inline_keyboard = [
            [InlineKeyboardButton(f"Platform: {platform}", callback_data=f"platform_{platform.lower()}")]
            for platform in ['INSTAGRAM', 'TELEGRAM', 'RUBICA']
        ]
    inline_reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await query.edit_message_text('Choose one of the inline options:', reply_markup=inline_reply_markup)



async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        user = await sync_to_async(TelegramUser.objects.get)(user_id=user_id)
        await sync_to_async(user.delete)()
        await update.message.reply_text('Your account has been deleted.')
    except TelegramUser.DoesNotExist:
        await update.message.reply_text('User does not exist.')


bot = bot = Application.builder().token(TOKEN).build()
bot.add_handler(CommandHandler('start', start))
bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
bot.add_handler(CallbackQueryHandler(platform_handler, pattern='^platform_'))
bot.add_handler(CallbackQueryHandler(category, pattern='^category'))
bot.add_handler(CallbackQueryHandler(close_handler, pattern="^close"))
bot.add_handler(CallbackQueryHandler(product_handler, pattern='^product_')) 
bot.add_handler(CommandHandler('delete', delete_user))
bot.run_polling()
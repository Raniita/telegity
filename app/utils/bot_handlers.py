from telegram import Update
from telegram.ext import CallbackContext

def reply_handler(update: Update, context: CallbackContext):
    """Reply message."""
    text = update.message.text
    update.message.reply_text(text)

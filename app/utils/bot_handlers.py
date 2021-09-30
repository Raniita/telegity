def reply_handler(bot, update):
    """Reply message."""
    text = update.message.text
    update.message.reply_text(text)

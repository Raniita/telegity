from telegram import Update, ForceReply
from telegram.ext import CallbackContext

from flask import current_app as app

def reply_handler(update: Update, context: CallbackContext):
    """Reply message."""
    text = update.message.text
    update.message.reply_text(text)


def start_handler(update: Update, context: CallbackContext):
    """ Send a message when the command /start is issued. """
    user = update.effective_user
    app.logger.info("user: {}".format(user.username))
    update.message.reply_markdown_v2(fr'Hi {user.mention_markdown_v2()}\!',
                                     reply_markup=ForceReply(selective=True))
#!/usr/bin/python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, dice
from telegram.ext import MessageHandler, Filters, CallbackContext, Updater, CommandHandler, CallbackQueryHandler

import config
from Main import *


def start(bot, update):
    bot.message.reply_text(main_menu_message(), reply_markup=main_menu_message())


def main_menu(bot, update):
    bot.callback_query.message.edit_text(main_menu_message(), reply_markup=main_menu_message())


def error(update, context):
    print(f'Update {update} caused error {context.error}')


def main_menu_message():
    return config.MESSAGE['START']


def main_handler(update, context):
    html_post = get_course()
    if html_post:
        update.message.reply_text(html_post, parse_mode=ParseMode.HTML, disable_web_page_preview=False)


############################# Handlers #########################################
updater = Updater(config.TELEGRAM_BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, main_handler))

updater.dispatcher.add_error_handler(error)

updater.start_polling()
################################################################################

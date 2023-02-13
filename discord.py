#!/usr/bin/python
import sys
import time

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, Job, Defaults
from Main import *

article = get_random_article()

telegram_channels = match_channel_by_categories(article['id'])

if telegram_channels and telegram_channels['id']:

    data_discord = render_html_post_for_discord(article)

    post_to_discord(data_discord['html'])

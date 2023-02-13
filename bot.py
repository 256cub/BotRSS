import sys
import time

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, Job, Defaults
from Main import *

if len(sys.argv) > 1:
    if sys.argv[1] == 'scrape_articles':
        scrape_articles(1, 100)
        exit()
    elif sys.argv[1] == 'post':
        manual_post()
        exit()
    elif sys.argv[1] == 'post_nft_news':
        manual_post_nft_news()
        exit()

def start(bot, context):
    if bot.message.from_user.id not in config.RESTRICTED_IDS:
        save_restricted_user(bot.message.from_user)
        bot.message.reply_text(config.MESSAGE['REDIRECT_BLOCKED_USERS'], parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        return

    limit = 1
    if len(context.args) > 0:
        limit = int(context.args[0])

    delay_time = 1
    if len(context.args) > 1:
        delay_time = int(context.args[1])

    bot.message.reply_text('SCRAPING {} ARTICLE PER EACH SOURCES | DELAY {} SECONDS'.format(limit, delay_time))
    scrape_articles(delay_time, limit)
    bot.message.reply_text('END SCRAPED')


def error(update, context):
    print(f'Update {update} caused error {context.error}')


def main_handler(update, context):
    if update.message.from_user.id not in config.RESTRICTED_IDS:
        save_restricted_user(update.message.from_user)
        update.message.reply_text(config.MESSAGE['REDIRECT_BLOCKED_USERS'], parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        return


def post(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id not in config.RESTRICTED_IDS:
        save_restricted_user(update.message.from_user)
        update.message.reply_text(config.MESSAGE['REDIRECT_BLOCKED_USERS'], parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        return

    limit = 1
    if len(context.args) > 0:
        limit = int(context.args[0])

    delay_time = 1
    if len(context.args) > 1:
        delay_time = int(context.args[1])

    for cycle in range(0, limit):

        article = get_random_article()

        if not article:
            print('NO ARTICLES')
            exit()

        telegram_channels = match_channel_by_categories(article['id'])
        if telegram_channels and telegram_channels['id']:
            article_short_link = save_short_link(article['id'])
            if article_short_link and is_url_valid(article_short_link):
                article['shorter_url'] = article_short_link
                html_post = render_html_post(article)
                telegram_post = context.bot.send_message(chat_id='@' + telegram_channels['username'], text=html_post, parse_mode='HTML')
                save_telegram_post(telegram_channels['id'], article['id'], telegram_post['message_id'])
                update_article_status(article['id'], 'POSTED')
                increment_total_posts(telegram_channels['id'])
                update.message.reply_text(' ' + str(cycle + 1) + ' | NEW POST: https://t.me/{}/{}'.format(telegram_channels['username'], telegram_post['message_id']), parse_mode='HTML', disable_web_page_preview=True)
            else:
                update.message.reply_text(' ' + str(cycle + 1) + ' | Error generating short link ' + article['id'], disable_web_page_preview=True)

        else:
            update_article_status(article['id'], 'NO_TAG_MATCH')
            tags = get_tags(article['id'])
            tag_html = ''
            for tag in tags:
                tag_html += '\n' + tag['name']

            update.message.reply_text(' ' + str(cycle + 1) + ' | No Channel Match by Tags\n' + tag_html + '\n\n' + article['url'], disable_web_page_preview=True)

        time.sleep(delay_time)


def main():
    updater = Updater(config.TELEGRAM_BOT_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start, pass_job_queue=True))
    updater.dispatcher.add_handler(CommandHandler('post', post))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, main_handler))

    updater.dispatcher.add_error_handler(error)

    # updater.dispatcher.add_handler(MessageHandler(Filters.text, time))
    # updater.job_queue.run_repeating(post, interval=60, first=1, context='1239093494')
    # updater.job_queue.run_repeating(post, 10, context='1239093494')

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

# mysql -u root -ptesttest
# SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

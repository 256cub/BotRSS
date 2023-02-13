import re
import time
import random
import config
import json

import mysql.connector
import requests

from datetime import datetime

from slugify import slugify

from discord_webhook import DiscordWebhook

from bs4 import BeautifulSoup

from telegram.ext import Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, dice
from telegram.ext import MessageHandler, Filters, CallbackContext, Updater, CommandHandler, CallbackQueryHandler


class MySQL:
    def __init__(self, host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWORD, database=config.DB_DATABASE):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database,
            auth_plugin="mysql_native_password"
        )

    def select(self, query):
        sql_cursor = self.connection.cursor(dictionary=True)
        sql_cursor.execute(query)
        sql_result = sql_cursor.fetchall()
        self.connection.close()
        return sql_result

    def select_single(self, query):
        sql_cursor = self.connection.cursor(dictionary=True)
        sql_cursor.execute(query)
        sql_result = sql_cursor.fetchone()
        self.connection.close()
        return sql_result

    def update(self, query):
        sql_cursor = self.connection.cursor()
        sql_cursor.execute(query)
        self.connection.commit()
        sql_cursor.close()
        return sql_cursor.lastrowid

    def close(self):
        self.connection.close()


def render_html_post(data):
    if data:
        post = ' 💥 <strong>' + data['title'].strip() + '</strong> 💥 '
        post += '\n\n'

        tags = get_tags(data['id'], 10)

        for tag in tags:
            post += ' #' + tag['name'].replace(' ', '')

        if len(tags) > 0:
            post += '\n\n'

        post += '<i>' + data['detail'].strip() + '</i>'
        post += '<a href="' + data['url'] + '"> </a>'

        post += '\n\n'
        post += ' <a href="' + data['shorter_url'] + '">' + config.MESSAGE['SOURCE_LINK'] + '</a>'

        post += '\n ➖➖➖➖➖➖➖➖ \n'

        result = dict()
        result['html'] = post
        result['title'] = data['title']
        result['detail'] = data['detail']

        result['name'] = data['name']
        result['shorter_url'] = data['shorter_url']
        result['tags'] = tags

        return result

    return False


def render_html_post_for_discord(data):
    if data:
        post = '**' + data['title'].strip() + '**'
        post += '\n\n'

        # post += '[](' + data['url'] + ')'

        post += '[Read full article here ...](' + data['shorter_url'] + ')'
        post += '\n ➖➖➖➖➖➖➖➖ \n'

        post += '*' + data['detail'].strip() + '*'
        post += '\n\n'

        post += '\n ➖➖➖➖➖➖➖➖ \n'

        result = dict()
        result['html'] = post
        result['title'] = data['title']
        result['name'] = data['name']
        result['shorter_url'] = data['shorter_url']

        return result

    return False


def get_tags(article_id, limit=False):
    query = "SELECT tags.name FROM `articles` LEFT JOIN articles_has_tags ON articles_has_tags.articles_id = articles.id LEFT JOIN tags ON tags.id = articles_has_tags.tags_id WHERE articles.id = {} AND articles.`status` = 'PROCESSED' AND tags.`status` = 'ACTIVE' ORDER BY rand()".format(article_id)
    if limit:
        query = query + ' LIMIT {}'.format(limit)

    return MySQL().select(query)


def get_categories(article_id, limit=False):
    query = "SELECT categories.name FROM `articles` LEFT JOIN articles_has_categories ON articles_has_categories.articles_id = articles.id LEFT JOIN categories ON categories.id = articles_has_categories.categories_id WHERE articles.id = {} AND articles.`status` = 'PROCESSED' AND categories.`status` = 'ACTIVE' ORDER BY rand()".format(article_id)
    if limit:
        query = query + ' LIMIT {}'.format(limit)

    return MySQL().select(query)


def get_sources(source_id=False, limit=False):
    if source_id:
        query = "SELECT * FROM `sources` WHERE `id` = '{}' AND `status` = 'ACTIVE'".format(source_id)
    else:
        query = "SELECT * FROM `sources` WHERE `status` = 'ACTIVE'"

    if limit:
        query = query + ' LIMIT {}'.format(limit)

    return MySQL().select(query)


def save_article(data):
    try:
        query = "SELECT * FROM `articles` WHERE `url` = '{}'".format(data['url'])
        found = MySQL().select_single(query)

        if not found:
            query = "INSERT INTO `articles` (sources_id, url, date_published) VALUES (\"{}\", \"{}\", \"{}\")".format(data['sources_id'], data['url'], data['date_published'])
            articles_id = MySQL().update(query)

            return articles_id
        else:
            # return found['id']
            return False

    except Exception as exception:
        print(exception)


def get_articles(article_id=False, limit=False):
    query = "SELECT DISTINCT articles.id, articles.title, articles.detail, articles.shorter_url, articles.url, articles.date_published, articles.status, categories.`name`, telegram_channels.total_posts FROM `articles` " \
            "LEFT JOIN articles_has_categories ON articles_has_categories.articles_id = articles.id " \
            "LEFT JOIN categories ON categories.id = articles_has_categories.categories_id " \
            "LEFT JOIN telegram_channels_has_categories ON telegram_channels_has_categories.categories_id = categories.id " \
            "LEFT JOIN telegram_channels ON telegram_channels.id = telegram_channels_has_categories.telegram_channels_id " \
            "WHERE articles.status = 'PROCESSED' AND CHAR_LENGTH (articles.title) > 5 AND CHAR_LENGTH (articles.detail) > 5  "

    if article_id:
        query = query + " AND articles.id = '{}'".format(article_id)

    query = query + ' ORDER BY telegram_channels.total_posts ASC, articles.date_published DESC '

    if limit:
        query = query + ' LIMIT {}'.format(limit)

    return MySQL().select(query)


def get_random_article():
    query = "SELECT DISTINCT articles.id, articles.title, articles.detail, articles.shorter_url, articles.url, articles.date_published, articles.status, categories.`name`, telegram_channels.total_posts FROM `articles` " \
            "LEFT JOIN articles_has_categories ON articles_has_categories.articles_id = articles.id " \
            "LEFT JOIN categories ON categories.id = articles_has_categories.categories_id " \
            "LEFT JOIN telegram_channels_has_categories ON telegram_channels_has_categories.categories_id = categories.id " \
            "LEFT JOIN telegram_channels ON telegram_channels.id = telegram_channels_has_categories.telegram_channels_id " \
            "WHERE articles.status = 'PROCESSED' AND CHAR_LENGTH (articles.title) > 5 AND CHAR_LENGTH (articles.detail) > 5 " \
            "ORDER BY telegram_channels.total_posts ASC, articles.date_published ASC LIMIT 5"

    found_articles = MySQL().select(query)

    if found_articles:
        random.shuffle(found_articles)
        return found_articles[0]

    return False


def get_random_nft_article():
    query = "SELECT *, '' AS name FROM `articles` WHERE articles.status = 'PROCESSED' AND CHAR_LENGTH (articles.title) > 5 AND CHAR_LENGTH (articles.detail) > 5 AND (articles.title LIKE '%NFT%' OR articles.detail LIKE '%NFT%') ORDER BY articles.date_published ASC LIMIT 1"
    return MySQL().select_single(query)


def scrape_meta(articles_id):
    article = get_article_by_id(articles_id)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'referer': 'https://google.com/'
    }

    tags = sections = []

    response = requests.get(article['url'], headers=headers)

    soup = BeautifulSoup(response.content, features="lxml")

    section = soup.find("meta", property="article:section")

    if section:
        sections = section.attrs['content'].split(',')

    tag = soup.find("meta", property="article:tag")

    if tag:
        tags = tag.attrs['content'].split(',')

    try:
        title = soup.find("meta", property="og:title").attrs['content'].replace("'", "\\'")
        for word in config.BAN_TITLE_WORDS:
            title = title.replace(word, '')


    except Exception as exception:
        title = ''

    try:
        detail = soup.find("meta", property="og:description").attrs['content'].replace("'", "\\'")
        detail = detail.replace('The latest NFT News, NFT & Web3 Insights and more. ', '').replace(' | NFT News', '')
    except Exception as exception:
        detail = ''

    try:
        image_url = soup.find("meta", property="og:image").attrs['content']
    except Exception as exception:
        image_url = ''

    if 'podcasts' in article['url']:
        update_article_status(articles_id, 'ERROR')
        return

    update_article(articles_id, title.strip(), detail.strip(), image_url)

    save_tags(articles_id, tags)
    save_tags(articles_id, sections)


def save_tags(articles_id, tags):
    try:
        for tag in tags:

            tag = tag.strip().replace(' ', '')
            tag = re.sub("[^0-9a-zA-Z]+", '', tag)

            query = "SELECT * FROM `tags` WHERE `name` = '{}'".format(tag)
            found_tag = MySQL().select_single(query)

            if not found_tag:
                query = "INSERT INTO `tags` (name) VALUES (\"{}\")".format(tag)
                tags_id = MySQL().update(query)
            else:
                tags_id = found_tag['id']

            query = "SELECT * FROM `articles_has_tags` WHERE articles_id = '{}' AND `tags_id` = '{}'".format(articles_id, tags_id)
            articles_has_tags = MySQL().select_single(query)

            if not articles_has_tags:
                query = "INSERT INTO `articles_has_tags` (articles_id, tags_id) VALUES (\"{}\", \"{}\")".format(articles_id, tags_id)
                articles_has_tags_id = MySQL().update(query)
            else:
                articles_has_tags_id = articles_has_tags['id']

    except Exception as exception:
        print(exception)


def save_categories(articles_id):
    try:

        query = "SELECT * FROM `articles` WHERE id = '{}'".format(articles_id)
        articles = MySQL().select_single(query)

        if articles and articles['title'] and articles['detail']:
            categories = re.split(' ', articles['title'].lower()) + re.split(' ', articles['detail'].lower())

            query = "SELECT * FROM `categories` WHERE 1=2 "

            for nr, category in enumerate(categories):
                category = category.replace(',', '').replace('.', '')
                if category.isalpha():
                    query += " OR categories.name = '" + category + "'"

            found_categories = MySQL().select(query)

            if found_categories:
                for found_category in found_categories:
                    categories_id = found_category['id']

                    query = "SELECT * FROM `articles_has_categories` WHERE articles_id = '{}' AND `categories_id` = '{}'".format(articles['id'], categories_id)
                    articles_has_categories = MySQL().select_single(query)

                    if not articles_has_categories:
                        query = "INSERT INTO `articles_has_categories` (articles_id, categories_id) VALUES (\"{}\", \"{}\")".format(articles['id'], categories_id)
                        articles_has_categories_id = MySQL().update(query)
                    else:
                        articles_has_categories_id = articles_has_categories['id']

                return True

            return False
    except Exception as exception:
        print(exception)


def save_telegram_post(telegram_channels_id, articles_id, message_id):
    try:
        query = "INSERT INTO `telegram_posts` (telegram_channels_id, articles_id, message_id) VALUES (\"{}\", \"{}\", \"{}\")".format(telegram_channels_id, articles_id, message_id)
        return MySQL().update(query)
    except Exception as exception:
        print(exception)


def update_article_status(articles_id, status):
    try:
        query = "UPDATE `articles` SET status = '{}' WHERE id = {}".format(status, articles_id)
        return MySQL().update(query)
    except Exception as exception:
        print(exception)


def increment_total_posts(telegram_channels_id):
    try:

        query = "SELECT * FROM `telegram_channels` WHERE id = '{}'".format(telegram_channels_id)
        telegram_channels = MySQL().select_single(query)

        if telegram_channels:
            total_posts = telegram_channels['total_posts']
            if total_posts:
                total_posts = total_posts + 1
            else:
                total_posts = 1

            query = "UPDATE `telegram_channels` SET total_posts = '{}' WHERE id = '{}'".format(total_posts, telegram_channels_id)
            telegram_channels_id = MySQL().update(query)

    except Exception as exception:
        print(exception)


def update_article(articles_id, title, detail, image_url):
    try:
        query = "UPDATE `articles` SET title = '{}', detail = '{}', image_url = '{}', status = 'PROCESSED' WHERE id = {}".format(title, detail, image_url, articles_id)
        return MySQL().update(query)
    except Exception as exception:
        print(exception)


def get_article_by_id(articles_id):
    query = "SELECT * FROM `articles` WHERE id = '{}'".format(articles_id)
    return MySQL().select_single(query)


def match_channel_by_tags(article):
    tags = get_tags(article['id'])

    try:
        query = "SELECT telegram_channels.id, telegram_channels.username, COUNT(*) FROM telegram_channels LEFT JOIN telegram_channels_has_tags ON telegram_channels_has_tags.telegram_channels_id = telegram_channels.id LEFT JOIN tags ON tags.id = telegram_channels_has_tags.tags_id WHERE "
        for nr, tag in enumerate(tags):
            if nr == 0:
                query += " tags.name LIKE '%" + tag['name'] + "%'"
            else:
                query += " OR tags.name LIKE '%" + tag['name'] + "%'"

        query += ' GROUP BY telegram_channels.username ORDER BY COUNT(*) DESC LIMIT 1'

        return MySQL().select_single(query)
    except Exception as exception:
        print(exception)


def match_channel_by_categories(articles_id):
    try:

        query = "SELECT telegram_channels.id, telegram_channels.username, COUNT(*) FROM articles " \
                "LEFT JOIN articles_has_categories ON articles_has_categories.articles_id = articles.id " \
                "LEFT JOIN categories ON categories.id = articles_has_categories.categories_id " \
                "LEFT JOIN telegram_channels_has_categories ON telegram_channels_has_categories.categories_id = categories.id " \
                "LEFT JOIN telegram_channels ON telegram_channels.id = telegram_channels_has_categories.telegram_channels_id " \
                "WHERE articles.id = '{}' " \
                "GROUP BY telegram_channels.id ORDER BY telegram_channels.date_updated ASC, telegram_channels.total_posts ASC, COUNT(*) DESC LIMIT 1".format(articles_id)

        return MySQL().select_single(query)
    except Exception as exception:
        print(exception)


def scrape_articles(delay_time, limit=False):
    sources = get_sources()

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'referer': 'https://google.com/'
    }

    for source in sources:
        resp = requests.get(source['rss_url'], headers=headers)

        soup = BeautifulSoup(resp.content, features="xml")

        items = soup.findAll('item')

        tags = []

        for nr, item in enumerate(items):
            categories = item.findAll('category')
            for category in categories:
                tag = category.text.title().replace(' ', '').replace('-', '').replace('@', '').replace('.', '').replace(',', '')
                if '_' not in tag:
                    tags.append(tag)

            news_item = {
                'sources_id': source['id']
            }

            try:
                news_item['url'] = item.link.text
            except Exception as exception:
                news_item['url'] = ''

            # try:
            #     news_item['shorter_url'] = item.link.text
            # except Exception as exception:
            #     news_item['shorter_url'] = ''

            try:
                news_item['date_published'] = datetime.strptime(item.pubDate.text, '%a, %d %b %Y %H:%M:%S +%f')
            except Exception as exception:
                try:
                    news_item['date_published'] = datetime.strptime(item.pubDate.text, '%a, %d %b %Y %H:%M:%S GMT')
                except Exception as exception:
                    news_item['date_published'] = '1970-01-01 01:01:01'

            articles_id = save_article(news_item)

            if articles_id:
                save_tags(articles_id, tags)
                scrape_meta(articles_id)

                if not save_categories(articles_id):
                    update_article_status(articles_id, 'NO_TAG_MATCH')

                if limit and nr >= limit:
                    break

                time.sleep(delay_time)


def save_restricted_user(data):
    try:
        query = "INSERT INTO `security` (username, first_name, last_name, user_id, language_code, is_bot) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(data.username, data.first_name, data.last_name, data.id, data.language_code, int(data.is_bot))
        return MySQL().update(query)
    except Exception as exception:
        print(exception)


def generate_short_link(url_to_short, title, url_custom=False):
    return url_to_short

    # TODO
    post_data = dict()
    post_data['url'] = url_to_short
    # post_data['type'] = 'splash'

    if url_custom:
        post_data['custom'] = slugify(title)

    urls = [
        'https://ads.moneycoma.com/api/url/add'
    ]

    random.shuffle(urls)

    url = urls[0]

    headers = {"Authorization": "Bearer tttttt"}

    x = requests.post(url, data=json.dumps(post_data), headers=headers).json()
    print(url_to_short)
    print(x)
    if x['shorturl']:
        return x['shorturl']

    return False


def save_short_link(articles_id):
    try:
        article = get_article_by_id(articles_id)
        shorter_url = generate_short_link(article['url'], article['title'], True)

        if shorter_url:
            query = "UPDATE `articles` SET shorter_url = '{}' WHERE id = {}".format(shorter_url, articles_id)
            MySQL().update(query)

            query = "SELECT shorter_url FROM `articles` WHERE `id` = '{}'".format(articles_id)
            result = MySQL().select_single(query)
            return result['shorter_url']
        else:
            update_article_status(articles_id, 'ERROR')

    except Exception as exception:
        print(exception)


def is_url_valid(url):
    try:
        response = requests.get(url)
        return True
    except requests.ConnectionError as exception:
        print(exception)
        return False


def post_to_discord(html):
    embed = [
        {
            "author": {
                "name": "Birdie♫",
                "url": "https://www.reddit.com/r/cats/",
                "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
            },
            "title": "Title",
            "url": "https://google.com/",
            "description": "Text message. You can use Markdown here. *Italic* **bold** __underline__ ~~strikeout~~ [hyperlink](https://google.com) `code`",
            "color": 15258703,
            "fields": [
                {
                    "name": "Text",
                    "value": "More text",
                    "inline": True
                },
                {
                    "name": "Even more text",
                    "value": "Yup",
                    "inline": True
                },
                {
                    "name": "Use `\"inline\": true` parameter, if you want to display fields in the same line.",
                    "value": "okay..."
                },
                {
                    "name": "Thanks!",
                    "value": "You're welcome :wink:"
                }
            ],
            "thumbnail": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/4-Nature-Wallpapers-2014-1_ukaavUI.jpg"
            },
            "image": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/A_picture_from_China_every_day_108.jpg"
            },
            "footer": {
                "text": "Woah! So cool! :smirk:",
                "icon_url": "https://i.imgur.com/fKL31aD.jpg"
            }
        }
    ]
    webhook = DiscordWebhook(
        url=random.choice(config.DISCORD_WEBHOOKS),
        content=html,
        username='TODO',
        avatar_url='TODO',
        # embeds=embed
    )
    response = webhook.execute()


def manual_post():
    article = get_random_article()

    if not article:
        print('NO ARTICLES')
        # print('SCRAPING ...')
        # scrape_articles(10)
        exit()

    telegram_channels = match_channel_by_categories(article['id'])

    if telegram_channels and telegram_channels['id']:
        article_short_link = save_short_link(article['id'])
        if article_short_link and is_url_valid(article_short_link):
            article['shorter_url'] = article_short_link

            data = render_html_post(article)

            updater = Updater(config.TELEGRAM_BOT_TOKEN, use_context=True)

            keyboard = []

            if True:
                affiliates = get_affiliates(article['title'], data['detail'], data['tags'], limit=3)

                keyboard3 = []
                for affiliate in affiliates:
                    keyboard3.append(InlineKeyboardButton(text=affiliate['name'], url=affiliate['url_short']))

                keyboard.append(keyboard3)

            if random.randint(1, 5) >= 2:
                keyboard = []

            reply_markup = InlineKeyboardMarkup(keyboard)

            telegram_post = updater.bot.send_message(chat_id='@' + telegram_channels['username'], text=data['html'], parse_mode=ParseMode.HTML, reply_markup=reply_markup)

            if telegram_channels['username'] == 'TODO':
                data_discord = render_html_post_for_discord(article)
                post_to_discord(data_discord['html'])

            save_telegram_post(telegram_channels['id'], article['id'], telegram_post['message_id'])
            update_article_status(article['id'], 'POSTED')
            increment_total_posts(telegram_channels['id'])

        else:
            update_article_status(article['id'], 'ERROR')


def manual_post_nft_news():
    article = get_random_nft_article()
    if not article:
        return False

    telegram_channels = match_channel_by_categories(article['id'])

    if telegram_channels and telegram_channels['id']:
        article_short_link = save_short_link(article['id'])
        if article_short_link and is_url_valid(article_short_link):
            article['shorter_url'] = article_short_link

            data = render_html_post(article)

            updater = Updater(config.TELEGRAM_BOT_TOKEN, use_context=True)

            keyboard = []

            if True:
                affiliates = get_affiliates(article['title'], data['detail'], data['tags'], limit=3)

                keyboard3 = []
                for affiliate in affiliates:
                    keyboard3.append(InlineKeyboardButton(text=affiliate['name'], url=affiliate['url_short']))

                keyboard.append(keyboard3)

            if random.randint(1, 3) >= 2:
                keyboard = []

            reply_markup = InlineKeyboardMarkup(keyboard)

            telegram_post = updater.bot.send_message(chat_id='@' + telegram_channels['username'], text=data['html'], parse_mode=ParseMode.HTML, reply_markup=reply_markup)

            if telegram_channels['username'] == 'TODO':
                data_discord = render_html_post_for_discord(article)
                post_to_discord(data_discord['html'])

            save_telegram_post(telegram_channels['id'], article['id'], telegram_post['message_id'])
            update_article_status(article['id'], 'POSTED')
            increment_total_posts(telegram_channels['id'])

        else:
            update_article_status(article['id'], 'ERROR')


def get_affiliates(title, details, categories, limit=10):
    try:
        query = "SELECT * FROM `affiliates` WHERE `status` = 'ACTIVE' ORDER BY rand() LIMIT {}".format(limit)
        return MySQL(database=config.DB_DATABASE_AFFILIATE).select(query)
    except Exception as exception:
        print(exception)

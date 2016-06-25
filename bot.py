# -*- coding: utf-8 -*-
import os
from uuid import uuid4

import re

from places.places import get_places
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, ChosenInlineResultHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def escape_markdown(text):
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def format_response(response_object):
    response = ('*{name}* \n'
                'Адрес: {address} \n'
                'Рейтинг: {rating}').format(name=response_object.get('name'),
                                            address=response_object.get('formatted_address'),
                                            rating=response_object.get('rating'))
    return response


def inlinequery(bot, update):
    query_object = update.inline_query
    query = query_object.query
    results = []

    places = get_places(query, lat=query_object.location.latitude, lng=query_object.location.longitude)
    for place in places:
        google_map_url = InlineKeyboardButton(text='На карте', url=place['url'])
        if place.get('website'):
            website = InlineKeyboardButton(text='Сайт', url=place['website'])
            keyboard = [[google_map_url, website]]
        else:
            keyboard = [[google_map_url, ]]
        results.append(InlineQueryResultArticle(id=uuid4(),
                                                title=place.get('name'),
                                                description=place.get('formatted_address'),
                                                input_message_content=InputTextMessageContent(
                                                    format_response(place),
                                                    parse_mode=ParseMode.MARKDOWN),
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                                                thumb_url=place.get('icon')
                                                ))
    bot.answerInlineQuery(update.inline_query.id, results=results)


def appendimage(bot, update):
    inline_message_id = update.chosen_inline_result.inline_message_id


def find(bot, update):
    pass


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv('TELEGRAM_TOKEN'))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(ChosenInlineResultHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

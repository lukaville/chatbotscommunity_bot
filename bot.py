# -*- coding: utf-8 -*-
import os
from uuid import uuid4

import re

import image_handler
from places.places import get_places
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, ChosenInlineResultHandler
from imgurpython import ImgurClient
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def escape_markdown(text):
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def format_response(response_object, image):
    response = ('*{name}* \n'
                'Адрес: {address} \n'
                'Рейтинг: {rating} \n').format(name=response_object.get('name'),
                                               address=response_object.get('formatted_address'),
                                               rating=response_object.get('rating'))
    opening_hours = response_object.get('opening_hours')
    is_opened = ''
    if opening_hours:
        is_opened = 'Открыто \n' if opening_hours.get('open_now') else 'Закрыто \n'
    link = image.get('link')
    return response + is_opened + link


def inlinequery(bot, update):
    query_object = update.inline_query
    query = query_object.query
    results = []
    if not query_object.location:
        return []
    places = get_places(query, lat=query_object.location.latitude, lng=query_object.location.longitude)
    for place in places:
        keyboard = [[], []]
        if place.get('website'):
            website = InlineKeyboardButton(text='Сайт', url=place['website'])
            keyboard[0].append(website)
        if place.get('url'):
            google_map_url = InlineKeyboardButton(text='На карте', url=place['url'])
            keyboard[0].append(google_map_url)
        opening_hours = place.get('opening_hours')
        is_opened = True
        if opening_hours:
            is_opened = opening_hours.get('open_now')

        image_handler.handle_image(
            title=place.get('name'),
            location=place.get('formatted_address'),
            phone=place.get('formatted_phone'),
            is_active=is_opened,
            rating=place.get('rating')
        )
        client = ImgurClient(
            os.getenv('IMGUR_CLIENT_ID'),
            os.getenv('IMGUR_CLIENT_SECRET')
        )
        resp = client.upload_from_path('resources/output/temp.png')

        if keyboard[0]:
            results.append(InlineQueryResultArticle(id=uuid4(),
                                                    title=place.get('name'),
                                                    description=place.get('formatted_address'),
                                                    input_message_content=InputTextMessageContent(
                                                        format_response(place, resp),
                                                        parse_mode=ParseMode.MARKDOWN),
                                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                                                    thumb_url=place.get('icon')
                                                    ))
    bot.answerInlineQuery(update.inline_query.id, results=results)


def appendimage(bot, update):
    inline_message_id = update.chosen_inline_result.inline_message_id
    print(inline_message_id)


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
    dp.add_handler(ChosenInlineResultHandler(appendimage))

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

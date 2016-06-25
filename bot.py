# -*- coding: utf-8 -*-

from uuid import uuid4

import re

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
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
    response = ('Название: {name} \n'
                'Адрес: {address} \n'
                'Рейтинг: {rating}').format(name=response_object.get('name'),
                                            address=response_object.get('formatted_adress'),
                                            rating=response_object.get('rating'))
    return response


def inlinequery(bot, update):
    query_object = update.inline_query
    query = query_object.query
    print(query_object.location)
    results = []

    # places = []
    # for place in places:
    place = {
         "formatted_address" : "ТЦ «Охотный ряд», Manege Sq, 1, стр. 2, Moscow, Russia",
         "geometry" : {
            "location" : {
               "lat" : 55.7555761,
               "lng" : 37.6152563
            }
         },
         "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png",
         "id" : "a70d7282178fedb683206a247a413f29eb8c9528",
         "name" : "McDonalds",
         "opening_hours" : {
            "open_now" : True,
            "weekday_text" : []
         },
         "photos" : [
            {
               "height" : 2322,
               "html_attributions" : [
                  "\u003ca href=\"https://maps.google.com/maps/contrib/104856352017638145108/photos\"\u003ePiter Ju\u003c/a\u003e"
               ],
               "photo_reference" : "CoQBdwAAAFFOJVdCIF8SM8n0P0AWXfHq7660uBt6cwyFWariEc8N0qx7T1m8faadbgL0PtdK7daUO0dq1qfWW9INJLc8WQBpxKWY-fz8vTAqI-UBnPQXjnvM0KtWDCBNMRdzQx13pDPEzjz_lDXLxt43Zx6K2_rwAlnh6_NCSBo7gvLI874pEhA_SBAPJOk1emElfk2inXo9GhSin6NGjzZ3-dD4YVyc55llib8Xtg",
               "width" : 4128
            }
         ],
         "place_id" : "ChIJh8a6d1BKtUYRACDWujPchsI",
         "price_level" : 1,
         "rating" : 4,
         "reference" : "CmRdAAAA_K0BSAAy9cSCsiDCtGNRDflhsnS1y093cly9rVX6-E7cWR0m2EXz9ZIRNFno5ao2i-Lcajnu49e077ww5jdJdqTF6K0gtKpoKfEIWeYsEG0b2U_owuFhnpYAWWPZjM2UEhApjq8eMw_Fqd3rned9UWfEGhRuFlxrDeBCW9g_zFE3epes1rajLg",
         "types" : [ "restaurant", "food", "point_of_interest", "establishment" ]
      }
    keyboard = [[InlineKeyboardButton(text='Test', url='google.com'), InlineKeyboardButton(text='No', url='ya.ru')]]
    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title=place.get('name'),
                                            description=place.get('formatted_address'),
                                            input_message_content=InputTextMessageContent(
                                                format_response(place),
                                                parse_mode=ParseMode.MARKDOWN),
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
                                            ))

    bot.answerInlineQuery(update.inline_query.id, results=results)


def find(bot, update):
    pass


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('231410719:AAGyoNSHPnKCm3PZfLtB1MyxypXbgcF0xXQ')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("find", find))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

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

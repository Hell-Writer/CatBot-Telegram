import logging
import os

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import settings

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

TOKEN = os.getenv('TOKEN')

updater = Updater(token=TOKEN)


def get_image_url():
    try:
        response = requests.get(settings.RAND_CAT_URL)
        return response.json()[0]["url"]
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(settings.RAND_DOG_URL)
        return response.json()[0]["url"]


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я KittyBot!')


def kitty_photo(update, context):
    url = get_image_url()
    chat = update.effective_chat
    context.bot.send_photo(chat.id, url)


def wake_up(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что включили меня, {chat.first_name}!',
        reply_markup=button)
    kitty_photo(update, context)


def main():
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', kitty_photo))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

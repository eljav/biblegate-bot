import re
import requests
import logging
from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)
from books import BIBLE_BOOKS

BOT_TOKEN = "secret_token"
TRANSLATION = "kjv"
API_URL = "https://bible-api.com/"
MAX_MESSAGE_LENGTH = 4096


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot in progress, please be patient.\n"
             "I will try to reply with a bible verse whenever one is mentioned like *'John 3:16'*.\n"
             "Get a range of verses with *'John 1:1-5'*.\n"
             "Get a full chapter with *'John 1'*.\n"
             "For a list of books type */books*",
        parse_mode="markdown"
    )


def send_verse(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    for book in BIBLE_BOOKS:
        if book.lower() in text:
            quoted_book = book
            list_text = text.split()
            quoted_verse = list_text[list_text.index(quoted_book.lower()) + 1]
            if re.match("\d{1,2}\:?\d{0,2}\-?\d{0,2}", quoted_verse):
                result = get_verse(quoted_book, quoted_verse)
                result_verse = [result[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(result), MAX_MESSAGE_LENGTH)]
                for r in result_verse:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=r,
                        parse_mode='markdown'
                    )


def send_books(update: Update, context: CallbackContext):
    list_books = ""
    for book in BIBLE_BOOKS:
        list_books += book + "\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="List of books you can quote:\n" + list_books
    )


def get_verse(book, verse):
    response = requests.get(API_URL + book + verse + "?translation=" + TRANSLATION)
    response_data = response.json()
    verse_text = response_data['text']
    result = "*" + book + " " + verse + ", " + TRANSLATION.upper() + "*\n" + verse_text
    return result


updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

books_handler = CommandHandler('books', send_books)
dispatcher.add_handler(books_handler)

verse_handler = MessageHandler(Filters.text, send_verse)
dispatcher.add_handler(verse_handler)

updater.start_polling()

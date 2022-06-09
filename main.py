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


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot in progress, please be patient.\n"
             "I will try to reply with a bible verse whenever one is mentioned like 'Ephesians 6:11'.\n"
             "For books with numbers like '2 Kings' type '2Kings'."
             "For a list of books type */books*",
        parse_mode="markdown"
    )


def send_verse(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    for book in BIBLE_BOOKS:
        if book.lower() in text:
            quoted_book = book
            list_text = text.split()
            quoted_chapter = list_text[list_text.index(quoted_book.lower()) + 1]
            if re.match("\d{1,2}[\-\:][\d-]{1,2}", quoted_chapter):
                quoted_chapter = quoted_chapter.replace('-', ':')
                result_verse = get_verse(quoted_book, quoted_chapter)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=result_verse,
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


def get_verse(book, chapter):
    response = requests.get(API_URL + book + chapter + "?translation=" + TRANSLATION)
    response_data = response.json()
    verse_text = response_data['verses'][0]['text']
    result = "*" + book + " " + chapter + ", " + TRANSLATION.upper() + "*\n" + verse_text
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

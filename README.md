# Biblegate bot
[Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot/) for automatically quoting Bible verses in telegram groups. The bot consumes the public domain [bible-api](https://github.com/seven1m/bible_api) API for content. 

## How to use  
---
Talk to the bot on Telegram @biblegate_bot or add it to your group. Whenever someone quotes a Bible verse in the form 'John 3:16' the bot will reply with the verse, like this:
>  **John 3:16, KJV**  
> For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.

It also will quote whole chapters in the form 'John 1' and ranges of verses in the form 'John 1:1-5'.

## Available commands  
---
`/start`  
Gives a small introduction to the bot.

`/books`  
Returns a list with the names of all the books of the Bible the bot can quote.

## To-do ✅  
---
- [x] Add support for ranges of verses (like John 1:1-5)  
- [ ] Add inline buttons to save a verse as favorite  
- [ ] Add translations of the Bible  
- [ ] Add more to-dos  

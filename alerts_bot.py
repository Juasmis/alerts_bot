import asyncio
import json
import logging
import argparse

# Telegram bot
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from telegram.constants import ParseMode

# Test alerts
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-f","--conf_file", help="Configuration file name",
                    required=False, type=str, default='config_alerts_bot.json', )
args = parser.parse_args()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

global config

with open(args.conf_file, mode="r", encoding='utf-8') as file: 
    config = json.loads(file.read())

# Telegram API
application = ApplicationBuilder().token(config['token']).build()

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global config
    
    # Remove the chat id from configuration
    config['chat_ids'].remove(update.effective_chat.id)
    
    # Update configuration file
    with open(args.conf_file, mode="w", encoding='utf-8') as file: 
        json.dump(config, file, indent=4, ensure_ascii=False)  
        logging.info(f'Chat id {update.effective_chat.id} removed from configuration file')
        
    # Send goodbye confirmation message
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=config['goodbye_message']['media'],
                                 caption="You were removed from the alerts list, but not from my heart ♥")
        

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global config
    
    welcome_message = """Hi\! I'm the alerts bot\. I will send you alerts when something related to webSCADA happens, \
also you can ask me about different parts of the system and I will answer you with some \(hopefully\) useful information
    
webSCADA web interface: [http://webscada:8052](http://webscada:8052)
Source code: [Gitlab](http://gitlab/jmserrano/webscada)
"""
    
#     welcome_message = """*bold \*text*
# _italic \*text_
# __underline__
# ~strikethrough~
# ||spoiler||
# *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
#  [inline URL](http://www.example.com/)
#  [inline mention of a user](tg://user?id=123456789)
# `inline fixed-width code`
# ```
# pre-formatted fixed-width code block
# ```
# ```python
# pre-formatted fixed-width code block written in the Python programming language
# ```"""
    
    await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=config['welcome_message']['media'])
    # await context.bot.send_animation(chat_id=update.effective_chat.id, animation=config['welcome_message']['media'],
                                    #  caption=welcome_message, parse_mode="MarkdownV2")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message, parse_mode="MarkdownV2")
    
    # Add the new chat id to configuration
    config['chat_ids'].append(update.effective_chat.id)
    
    # Update configuration file with chat_id
    if update.effective_chat.id not in config['chat_ids']:
        with open(args.conf_file, mode="w", encoding='utf-8') as file:
            json.dump(config, file, indent=4, ensure_ascii=False)  
            logging.info(f'Chat id {update.effective_chat.id} added to configuration file')

async def error_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Raise an error to trigger the error handler."""
    
    alert_data = {
        "level": "error",
        "title": "Test error alert, be aware!",
        "message": "Test alert of level Error to see if everything is working as expected",
        "source": "telegram_bot",
    }
    
    requests.post(config['API_url'], json=alert_data)

async def danger_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Raise an error to trigger the danger handler."""
    
    alert_data = {
        "level": "danger",
        "title": "Test danger alert, luckily it's not real!",
        "message": "Test alert of level danger to see if everything is working as expected",
        "source": "telegram_bot",
    }
    
    requests.post(config['API_url'], json=alert_data)
    
async def warning_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Raise a warning to trigger the warning alert."""
    
    alert_data = {
        "level": "warning",
        "title": "Test warning alert, still works? Then life is good",
        "message": "Test alert of level warning to see if everything is working as expected",
        "source": "telegram_bot",
    }
    
    requests.post(config['API_url'], json=alert_data)
    
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Raise an info alert to trigger the info alert message."""
    
    alert_data = {
        "level": "info",
        "title": "Test info alert, you look beautiful today",
        "message": "Test alert of level info to see if everything is working as expected",
        "source": "telegram_bot",
    }
    requests.post(config['API_url'], json=alert_data)

    
# async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(CommandHandler("error_command", error_command))
    application.add_handler(CommandHandler("danger_command", danger_command))
    application.add_handler(CommandHandler("warning_command", warning_command))
    application.add_handler(CommandHandler("info_command", info_command))
    
    # unknown_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), unknown)
    # application.add_handler(unknown_handler)

    asyncio.run(application.run_polling())
    
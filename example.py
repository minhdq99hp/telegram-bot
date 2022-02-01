'''
Echo Bot Example

Author: minhdq99hp@gmail.com
Updated: 01/02/2022
'''

import datetime
import json
import os
from pathlib import Path
import filecmp
import shutil
import traceback
from enum import Enum
from time import sleep

from app.settings import TIMEZONE, CONFIG
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      constants, BotCommand)
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from app.bot.constants import *
from app.bot.decorators import *
from app.bot.helpers import ThrowingArgumentParser, truncate_caption, truncate_text
from app.bot.logic import *
from app.bot.models import *

class EchoBot(TelegramBot):
    """Echo Bot Example"""

    def __init__(self, *args, **kwargs):
        super().__init__('echo_bot', *args, **kwargs)

        command_handlers = [
            CommandHandler('start', self.start),
            CommandHandler('help', self.help),
        ]
        
        message_handler = MessageHandler(Filters.all, self.response)
        
        # ADD HANDLER
        for handler in command_handlers:
            self.dispatcher.add_handler(handler)
        self.dispatcher.add_handler(message_handler)

    def help(self, update, context):
        update.message.reply_text('HELP')

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='HI')

    @message_handler(restricted=False)
    def response(self, update, context):
        message = update.message.text 
        sleep(1)
        update.message.reply_text(message)

    def _run_telegram_listener(self):
        self.updater.start_polling()

    def run(self):
        self._run_telegram_listener()


if __name__ == '__main__':
    echobot = EchoBot()
    echobot.run()

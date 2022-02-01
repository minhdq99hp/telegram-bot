import os
import shlex
from enum import Enum
import logging
from app.settings import DATA_DIR, CONFIG

from telegram.ext import Updater
from telegram import (KeyboardButton, ReplyKeyboardMarkup)

yes_no_keyboard_markup = ReplyKeyboardMarkup([[KeyboardButton("Yes"), KeyboardButton("No"),]]) 


class TelegramBot:
    """Telegram Chatbot"""

    class STATES(Enum):
        READY = 0

    def __init__(self, name, logger=None, auth_logger=None):
        if not logger:
            self.logger = logging.getLogger(f'{name}_telegram_bot')
            self.logger.setLevel(logging.DEBUG)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
            self.logger.addHandler(stream_handler)
        else:
            self.logger = logger
        
        if not auth_logger:
            self.auth_logger = logging.getLogger(f'{name}_telegram_bot_auth')
            self.auth_logger.setLevel(logging.DEBUG)
            file_handler = logging.FileHandler(os.path.join(DATA_DIR, "unauthorized_accesses.log"), mode='a', encoding='utf-8')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
            self.auth_logger.addHandler(file_handler)
        
        self.state = {} # contain the current state of bot, key is chat_id
        self.data = {} # contain the data of a conversation, key is chat_id

        self.master_id = CONFIG['master_id']
        self.authorized_ids = [self.master_id]

        self.updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'], use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

    def _is_authorized(self, chat_id):
        return chat_id in self.authorized_ids

    def _get_command_args(self, message):
        message = message.replace('”', '"').replace('“', '"').replace("’", "'")

        message = shlex.split(message)
        return [] if not message[0].startswith('/') else message[1:]
    
    def _get_state(self, chat_id):
        return self.state.setdefault(chat_id, self.STATES.READY)
    
    def _set_state(self, chat_id, new_state):
        self.state[chat_id] = new_state

    
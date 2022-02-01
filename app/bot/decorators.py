import datetime
import traceback
from functools import wraps

from pytz import utc
from telegram import ChatAction
from telegram.error import BadRequest


def serializer_user(user):
    return f"{user.id} - {user.username} - {user.full_name if user.full_name else None}" + f" - {user.link} - {user.is_bot} - {user.language_code}"


def restricted(func):
    """Restrict usage of func to allowed users only and replies if necessary"""

    @wraps(func)
    def wrapped(self, update, context, *args, **kwargs):
        user_id = update.effective_user.id
        username = update.effective_user.username

        if user_id not in self.authorized_ids:
            self.logger.warn(f"Handler {func.__name__}: Unauthorized access denied for {user_id} - {username}.")
            self.auth_logger.warn(f"Unauthorized access denied - {serializer_user(update.effective_user)} - {update.message.text if update.message.text else ''} - {func.__name__}")

            try:
                update.message.reply_text('Unauthorized access denied')
            except BadRequest as e:
                self.logger.warn(e.message)
            return  # quit function
        else:
            self.logger.debug(f"Received message from authorized user {user_id} - {username}.")
        
        return func(self, update, context, *args, **kwargs)
    return wrapped


def has_typing_action(func):
    """Send typing action before running message handler"""

    @wraps(func)
    def wrapped(self, update, context, *args, **kwargs):
        try:
            update.message.reply_chat_action(action=ChatAction.TYPING)
        except Exception:
            self.logger.warn("Unable to send typing action")
        return func(self, update, context, *args, **kwargs)
    return wrapped


def ignore_empty_message(func):
    """Ignore empty message"""

    @wraps(func)
    def wrapped(self, update, context, *args, **kwargs):
        if not update.message.text:
            return
        return func(self, update, context, *args, **kwargs)
    return wrapped


def ignore_outdated_message(delta=datetime.timedelta(minutes=5)):
    def decorator(func):
        @wraps(func)
        def wrapper(self, update, context, *args, **kwargs):
            if utc.localize(datetime.datetime.utcnow()) - update.message.date > delta:
                self.logger.warn(f"Ignore outdated message from {update.effective_user.username}")
                return
            return func(self, update, context, *args, **kwargs)
        return wrapper
    return decorator


def message_handler(name='', restricted=True, has_typing_action=True, ignore_empty=True, ignore_outdated=True, timeout=datetime.timedelta(minutes=5), handle_exception=True):
    """An universal decorator for message handler

    :param name: name of the message handler, defaults to empty string
    :type name: str, optional
    :param restricted: only reply authorized user, defaults to True
    :type restricted: bool, optional
    :param has_typing_action: send typing action before running message handler, defaults to True
    :type has_typing_action: bool, optional
    :param ignore_empty: ignore empty message, defaults to True
    :type ignore_empty: bool, optional
    :param ignore_outdated: ignore outdated message, defaults to True
    :type ignore_outdated: bool, optional
    :param delta: set message timeout, defaults to datetime.timedelta(minutes=5)
    :type delta: [type], optional
    :param handle_exception: auto catch exception and response to sender, defaults to True
    :type handle_exception: bool, optional
    """

    def decorator(func):
        @wraps(func)
        def wrapped(self, update, context, *args, **kwargs):
            if not name:
                func_name = func.__name__

            user_id = update.effective_user.id
            username = update.effective_user.username

            if restricted:
                if user_id not in self.authorized_ids:
                    self.logger.warn(f"Handler {func_name}: Unauthorized access denied for {user_id} - {username}.")
                    self.auth_logger.warn(f"Unauthorized access denied - {serializer_user(update.effective_user)} - {update.message.text if update.message.text else ''} - {func_name}")

                    try:
                        update.message.reply_text('Unauthorized access denied')
                    except BadRequest as e:
                        self.logger.warn(e.message)
                    return  # quit function
                else:
                    self.logger.debug(f"Received message from authorized user {user_id} - {username}.")
            
            if ignore_outdated:
                if utc.localize(datetime.datetime.utcnow()) - update.message.date > timeout:
                    self.logger.warn(f"Ignore outdated message from {update.effective_user.username}")
                    return

            if ignore_empty:
                if not update.message.text:
                    return
            
            if has_typing_action:
                try:
                    update.message.reply_chat_action(action=ChatAction.TYPING)
                except Exception:
                    self.logger.warn("Unable to send typing action")

            if handle_exception:
                try:
                    return func(self, update, context, *args, **kwargs)
                except Exception:
                    traceback.print_exc()
                    try:
                        update.message.reply_text('')
                    except Exception:
                        pass
                    return

        return wrapped
    
    return decorator

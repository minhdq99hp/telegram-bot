import random
import logging

def has_a_chance(rate=1, success_log_message='', fail_log_message=''):
        if random.uniform(0, 1) >= rate:
            if fail_log_message:
                logging.info(fail_log_message)
            return False
        if success_log_message:
            logging.info(success_log_message)
        return True
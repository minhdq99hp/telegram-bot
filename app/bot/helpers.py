import argparse

class ArgumentParserError(Exception): pass

class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def truncate_caption(caption):
    if len(caption) <= 1024:
        return caption
    else:
        return caption[:1024] + '...'


def truncate_text(text):
    if len(text) <= 4096:
        return text
    else:
        return text[:4093] + '...'
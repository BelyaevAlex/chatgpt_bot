import os


def get_tokens():
    return os.environ['OPENAI_TOKEN'], os.environ['TELEGRAM_TOKEN']
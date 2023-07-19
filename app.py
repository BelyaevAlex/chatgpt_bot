from main import TELEGRAM_BOT
from os import path
from database import create_connection, execute_query, execute_read_query, add_row
from Tokens import get_tokens


def who_start_chat(connection):
    select_users = f"SELECT id_tg from chat"
    is_chat_starts = {}
    chat_users = {}
    users_id = execute_read_query(connection, select_users)
    users_id_new = []
    for user_id in list(users_id):
        users_id_new.append(user_id[0])
    for user_id in sorted(users_id_new):
        if users_id_new.count(user_id) > 1:
            chat_users.update({user_id: 'Yes'})
            is_chat_starts.update({user_id: 'Yes'})
        else:
            is_chat_starts.update({user_id: 'Yes'})
    return is_chat_starts, chat_users

def run_bot():
    abs_path = path.abspath(__file__)  # полный путь к файлу скрипта
    path_rep = path.dirname(abs_path)
    is_chat_starts, chat_users = who_start_chat(create_connection(path_rep + path.sep + 'input.sqlite'))
    openai_token, telegram_token = get_tokens()
    telegram_bot = TELEGRAM_BOT(
        path_rep=path_rep,
        openai_token=openai_token,
        telegram_token=telegram_token,
        is_chat_starts = is_chat_starts,
        chat_users = chat_users
    )
    telegram_bot.run()

run_bot()
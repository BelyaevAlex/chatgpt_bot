from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import messages as mg
from database import create_connection, execute_query, execute_read_query
import openai
import messages as mg
from database import create_connection, execute_query, execute_read_query
import os
import json
from os import path

def get_script_dir():
    abs_path = path.abspath(__file__) # полный путь к файлу скрипта
    return path.dirname(abs_path)


DB_NAME = 'input.sqlite'
DB_FILE = get_script_dir() + path.sep + DB_NAME

openai.organization = "org-lH8tlTiviZMLomLzQ5iSJqMz"
connection = create_connection(DB_FILE)
openai.api_key = "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"
openai.Model.list()

bot = Bot(token="6050756412:AAHVxNAxl_w1fMtn87GO9tWfac4RVd0CM5c")
dp = Dispatcher(bot)


chat_users = {}
is_chat_starts = {}

keyboard_main = mg.keyboard_main
keyboard_chat = mg.keyboard_chat

keyboard_start1 = mg.keyboard_start1
keyboard_start2 = mg.keyboard_start2
keyboard_start3 = mg.keyboard_start3

def in_users_db(id_tg):
    create_input = f"SELECT * from users WHERE id_tg = {id_tg}"
    a = execute_read_query(connection, create_input)
    if not a:
        create_input = f"""
                            INSERT INTO
                              users (num_of_requests, id_tg)
                            VALUES
                              (0, {id_tg});
                            """
        execute_query(connection, create_input)


@dp.message_handler(commands = 'file')
async def send_file(message: types.Document):
    if message.from_user.id == 905410819:
        await message.reply_document(open(DB_FILE, 'rb'))



@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    in_users_db(msg.from_user.id)
    if msg.from_user.id == 905410819:
        create_input = f"SELECT id_tg from users"
        a = execute_read_query(connection, create_input)
        await bot.send_message(msg.from_user.id, f"Поздравляю у бота уже {len(set(a))} пользователей")
        create_input = f"SELECT num_of_requests from users"
        a = execute_read_query(connection, create_input)
        b = []
        for i in a:
            b.append(int(i[0]))
        await bot.send_message(msg.from_user.id, f"Поздравляю у бота уже {sum(b)} запросов")
    await bot.send_message(msg.from_user.id, mg.start0, reply_markup=keyboard_start1)


@dp.message_handler(text=mg.button1_start1_text)
async def process_help_command(msg: types.Message):
    await bot.send_message(msg.from_user.id, mg.start1, reply_markup=keyboard_start2)


@dp.message_handler(text=mg.button1_start2_text)
async def process_help_command(msg: types.Message):
    await bot.send_message(msg.from_user.id, mg.start2, reply_markup=keyboard_start3)


@dp.message_handler(text=mg.button1_start3_text)
async def process_help_command(msg: types.Message):
    await bot.send_message(msg.from_user.id, mg.start3, reply_markup=keyboard_main)


@dp.message_handler(commands=['help'])
@dp.message_handler(text=mg.button2_main_text)
async def process_help_command(msg: types.Message):
    global keyboard_main
    in_users_db(msg.from_user.id)
    await bot.send_message(msg.from_user.id, mg.help, reply_markup=keyboard_main)


@dp.message_handler(commands=['chat_start'])
@dp.message_handler(text=mg.button3_main_text)
async def process_help_command(msg: types.Message):
    global keyboard_main, is_chat_starts
    in_users_db(msg.from_user.id)
    if msg.from_user.id in is_chat_starts:
        await bot.send_message(msg.from_user.id, mg.chat_is_already_open, reply_markup=keyboard_chat)
    else:
        is_chat_starts.update({msg.from_user.id : 'Yes'})
        await bot.send_message(msg.from_user.id, mg.chat_start, reply_markup=keyboard_chat)


@dp.message_handler(commands=['chat_end'])
@dp.message_handler(text=mg.button1_chat_text)
async def process_help_command(msg: types.Message):
    global is_chat_starts, keyboard_main, chat_users
    in_users_db(msg.from_user.id)
    if msg.from_user.id in is_chat_starts:
        is_chat_starts.pop(msg.from_user.id)
        if msg.from_user.id in chat_users:
            chat_users.pop(msg.from_user.id)
        await bot.send_message(msg.from_user.id, mg.chat_end, reply_markup=keyboard_main)
    else:
        await bot.send_message(msg.from_user.id, mg.chat_is_not_open, reply_markup=keyboard_main)


@dp.message_handler(commands=['donate'])
@dp.message_handler(text=mg.button1_main_text)
async def process_help_command(msg: types.Message):
    await bot.send_message(msg.from_user.id, mg.pozh, reply_markup=keyboard_main)


@dp.message_handler()
async def main_messages(msg: types.Message):
    global is_chat_starts, chat_users

    if msg.from_user.id in is_chat_starts:
        #select_users = f"SELECT text from chat_history WHERE id_tg = {msg.from_user.id}"
        #inputing = execute_read_query(connection, select_users)
        #print(len(inputing))
        if msg.from_user.id in chat_users:
            text = msg.text
            chat_present = {"role": "user", "content": text}
            chat_past = chat_users.pop(msg.from_user.id)
            chat_past.append(chat_present)
            chat_present = chat_past

            select_users = f"SELECT num_of_requests from users WHERE id_tg = {msg.from_user.id}"
            num_of_requests = execute_read_query(connection, select_users)[0][0]
            plus_requests = f"UPDATE users SET num_of_requests = {num_of_requests + 1} WHERE id_tg = {msg.from_user.id}"
            execute_query(connection, plus_requests)
            print(0)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chat_present
            )
            await bot.send_message(msg.from_user.id, response["choices"][0]["message"]["content"], reply_markup=keyboard_chat)
            #request = f"""INSERT INTO
            #                      chat_history (id_tg, text)
            #                    VALUES
            #                      ({msg.from_user.id}, {json.dumps(chat_present)});
            #                    """
            #execute_query(connection, request)
        else:
            text = msg.text
            chat_present = [{"role": "user", "content": text}]
            select_users = f"SELECT num_of_requests from users WHERE id_tg = {msg.from_user.id}"
            num_of_requests = execute_read_query(connection, select_users)[0][0]
            plus_requests = f"UPDATE users SET num_of_requests = {num_of_requests + 1} WHERE id_tg = {msg.from_user.id}"
            execute_query(connection, plus_requests)
            print(0)

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=chat_present
                )
                await bot.send_message(msg.from_user.id, response["choices"][0]["message"]["content"],
                                       reply_markup=keyboard_chat)
            except Error:
                await bot.send_message(msg.from_user.id, mg.chat_is_overloaded,
                                       reply_markup=keyboard_chat)
            #request = f"""INSERT INTO
            #                                  chat_history (id_tg, text)
            #                                VALUES
            #                                  ({msg.from_user.id}, {json.dumps(chat_present)});
            #                                """

            #execute_query(connection, request)

        chat_users.update({msg.from_user.id: chat_present})
        #create_input = f"""
        #                            INSERT INTO
        #                              chat (text, tg_id)
        #                            VALUES
        #                              ('{chat_present}', '{msg.from_user.id}');
        #                            """
        #execute_query(connection, create_input)
    else:
        await bot.send_message(msg.from_user.id, mg.error_write_corectly, reply_markup=keyboard_main)

if __name__ == '__main__':
    executor.start_polling(dp)
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ContentType
import messages as mg
from database import create_connection, execute_query, execute_read_query
import openai
from database import create_connection, execute_query, execute_read_query, add_row, add_row_chat, update_add_row_chat
import os
import json
from os import path
import asyncio
import time
import asyncgpt


class TELEGRAM_BOT:
    def __init__(self, path_rep, openai_token, telegram_token, is_chat_starts, chat_users):
        self._path = path_rep
        self._openai = openai
        self._openai.api_key = openai_token
        self._openai_token = openai_token
        self._telegram_token = telegram_token
        self._bot = Bot(token=telegram_token)
        self._dp = Dispatcher(self._bot)
        self._chat_users = chat_users
        self._is_chat_starts = is_chat_starts
        self._keyboard_main = mg.keyboard_main
        self._keyboard_chat = mg.keyboard_chat
        self._keyboard_start1 = mg.keyboard_start1
        self._keyboard_start2 = mg.keyboard_start2
        self._keyboard_start3 = mg.keyboard_start3
        self._DB_NAME = 'input.sqlite'
        self._DB_FILE = path_rep + path.sep + self._DB_NAME
        self._connection = create_connection(self._DB_FILE)
        self._register_handlers()
        self._sendmta = 0


    def run(self):
        executor.start_polling(self._dp)


    def _register_handlers(self):
        self._dp.message_handler(commands='file')(self.send_db_file)
        self._dp.message_handler(commands=['start'])(self.start_command)
        self._dp.message_handler(text=mg.button1_start1_text)(self.start_command_2)
        self._dp.message_handler(text=mg.button1_start2_text)(self.start_command_3)
        self._dp.message_handler(text=mg.button1_start3_text)(self.start_command_4)
        self._dp.message_handler(commands=['help'])(self.help_command)
        self._dp.message_handler(text=mg.button2_main_text)(self.help_command)
        self._dp.message_handler(commands=['chat_start'])(self.start_chat)
        self._dp.message_handler(text=mg.button3_main_text)(self.start_chat)
        self._dp.message_handler(commands=['chat_end'])(self.end_chat)
        self._dp.message_handler(text=mg.button1_chat_text)(self.end_chat)
        self._dp.message_handler(commands=['donate'])(self.donate_command)
        self._dp.message_handler(text=mg.button1_main_text)(self.donate_command)
        self._dp.message_handler(commands=['sendmta'])(self.send_message_to_all)
        self._dp.message_handler()(self.main_messages)
        self._dp.message_handler(content_types=ContentType.PHOTO)(self.process_photo)
        self._dp.message_handler(content_types=[ContentType.VOICE])(self.process_audio)


    async def process_photo(self, msg: types.Message):
        if msg.from_user.id in self._is_chat_starts:
            await self._bot.send_message(msg.from_user.id, 'Извините, этот бот не умеет обрабатывать изображения', reply_markup=self._keyboard_chat)
        else:
            await self._bot.send_message(msg.from_user.id, 'Извините, этот бот не умеет обрабатывать изображения', reply_markup=self._keyboard_main)


    async def process_audio(self, msg: types.Message):
        if msg.from_user.id in self._is_chat_starts:
            await self._bot.send_message(msg.from_user.id, 'Извините, этот бот не умеет обрабатывать аудио файлы', reply_markup=self._keyboard_chat)
        else:
            await self._bot.send_message(msg.from_user.id, 'Извините, этот бот не умеет обрабатывать аудио файлы', reply_markup=self._keyboard_main)

    #смена переменной для отправки сообщения всем пользователям
    async def send_message_to_all(self, msg: types.Message):
        if msg.from_user.id == 905410819:
            await self._bot.send_message(msg.from_user.id, "Напиши сообщение, которое отправиться всем", reply_markup=self._keyboard_main)
            self._sendmta = 1


    async def requests_gpt(self, history, id):
        try:
            bot = asyncgpt.GPT(apikey=self._openai_token)
            #запрос chatgpt
            completion = await bot.chat_complete(history)
            #сохраниение результата chatgpt
            update_add_row_chat(self._connection, "chat", id, completion)
            #отправка сообщения пользователю
            await self._bot.send_message(id, completion, reply_markup=self._keyboard_chat)
        except:
            await self._bot.send_message(id, mg.chat_is_overloaded, reply_markup=self._keyboard_chat)

    #проверка есть ли пользователь в базе данных
    def in_users_db(self, id_tg):
        create_input = f"SELECT * from users WHERE id_tg = {id_tg}"
        a = execute_read_query(self._connection, create_input)
        if not a:
            create_input = f"""
                                    INSERT INTO
                                      users (num_of_requests, id_tg)
                                    VALUES
                                      (0, {id_tg});
                                    """
            execute_query(self._connection, create_input)


    #отправка бд
    async def send_db_file(self, message: types.Document):
        if message.from_user.id == 905410819:
            await message.reply_document(open(self._DB_FILE, 'rb'))


    async def start_command(self, msg: types.Message):
        self.in_users_db(msg.from_user.id)
        if msg.from_user.id == 905410819:
            create_input = f"SELECT id_tg from users"
            a = execute_read_query(self._connection, create_input)
            await self._bot.send_message(msg.from_user.id, f"Поздравляю у бота уже {len(set(a))} пользователей")
            create_input = f"SELECT num_of_requests from users"
            a = execute_read_query(self._connection, create_input)
            b = []
            for i in a:
                b.append(int(i[0]))
            await self._bot.send_message(msg.from_user.id, f"Поздравляю у бота уже {sum(b)} запросов")
        await self._bot.send_message(msg.from_user.id, mg.start0, reply_markup=self._keyboard_start1)


    async def start_command_2(self, msg: types.Message):
        await self._bot.send_message(msg.from_user.id, mg.start1, reply_markup=self._keyboard_start2)


    async def start_command_3(self, msg: types.Message):
        await self._bot.send_message(msg.from_user.id, mg.start2, reply_markup=self._keyboard_start3)


    async def start_command_4(self, msg: types.Message):
        await self._bot.send_message(msg.from_user.id, mg.start3, reply_markup=self._keyboard_main)


    async def help_command(self, msg: types.Message):
        self.in_users_db(msg.from_user.id)
        await self._bot.send_message(msg.from_user.id, mg.help, reply_markup=self._keyboard_main)


    async def start_chat(self, msg: types.Message):
        self.in_users_db(msg.from_user.id)
        if msg.from_user.id in self._is_chat_starts:
            await self._bot.send_message(msg.from_user.id, mg.chat_is_already_open, reply_markup=self._keyboard_chat)
        else:
            self._is_chat_starts.update({msg.from_user.id: 'Yes'})
            await self._bot.send_message(msg.from_user.id, mg.chat_start, reply_markup=self._keyboard_chat)


    async def end_chat(self, msg: types.Message):
        self.in_users_db(msg.from_user.id)
        delete_comment = f"DELETE FROM input WHERE id_tg = {msg.from_user.id}"
        execute_query(self._connection, delete_comment)
        delete_comment = f"DELETE FROM chat WHERE id_tg = {msg.from_user.id}"
        execute_query(self._connection, delete_comment)
        delete_comment = f"DELETE FROM finish WHERE id_tg = {msg.from_user.id}"
        execute_query(self._connection, delete_comment)
        if msg.from_user.id in self._is_chat_starts:
            self._is_chat_starts.pop(msg.from_user.id)
            if msg.from_user.id in self._chat_users:
                self._chat_users.pop(msg.from_user.id)
            await self._bot.send_message(msg.from_user.id, mg.chat_end, reply_markup=self._keyboard_main)
        else:
            await self._bot.send_message(msg.from_user.id, mg.chat_is_not_open, reply_markup=self._keyboard_main)


    async def donate_command(self, msg: types.Message):
        await self._bot.send_message(msg.from_user.id, mg.pozh, reply_markup=self._keyboard_main)


    async def main_messages(self, msg: types.Message):
        #проверка сообщения, является ли это сообщение для всех
        if msg.from_user.id == 905410819 and self._sendmta == 1 and msg.text != '/sendmta':
            self._sendmta = 0
            select_users = f"SELECT id_tg from users"
            users_id = execute_read_query(self._connection, select_users)
            #отправка всем пользователям сообщение
            for id in users_id:
                try:
                    await self._bot.send_message(id[0], msg.text,
                                                reply_markup=self._keyboard_main)
                except:
                    pass
            self._is_chat_starts = {}
            self._chat_users = {}
        #проверка начато ли общение с пользователем
        elif msg.from_user.id in self._is_chat_starts:
            #добавка сообщения в историю чата
            add_row_chat(self._connection, "chat", msg.text, msg.from_user.id)
            if msg.from_user.id in self._chat_users:
                pass
            else:
                self._chat_users.update({msg.from_user.id: 'Yes'})
            select_users = f"SELECT num_of_requests from users WHERE id_tg = {msg.from_user.id}"
            num_of_requests = execute_read_query(self._connection, select_users)[0][0]
            #добавление запроса к счётчику запросов
            plus_requests = f"UPDATE users SET num_of_requests = {num_of_requests + 1} WHERE id_tg = {msg.from_user.id}"
            execute_query(self._connection, plus_requests)
            #предупреждение пользователя, что его сообщение получено
            await self._bot.send_message(msg.from_user.id, 'Думаю над ответом, пожалуйста подождите...',
                                         reply_markup=self._keyboard_chat)
            #чтение базы данных на историю сообщений
            select_users = f"SELECT text, answer FROM chat WHERE id_tg = {msg.from_user.id}"
            d_history_chat = execute_read_query(self._connection, select_users)
            history_chat = []
            #преобразование текста в правильную форму для отправки chatgpt
            for i in d_history_chat:
                print(i)
                history_chat.append({"role": "user", "content": str(i[0])})
                if str(i[1]) != "no_answer":
                    history_chat.append({"role": "assistant", "content": str(i[1])})
            print(history_chat)
            #отправка запроса chatgpt
            await asyncio.create_task(self.requests_gpt(history_chat, msg.from_user.id))
        #предупреждение человека, что он начал писать не начав разгоор с ботом
        else:
            await self._bot.send_message(msg.from_user.id, mg.error_write_corectly, reply_markup=self._keyboard_main)
            #на случай бага, если человек уже начал разговор
            if msg.from_user.id in self._is_chat_starts:
                self._is_chat_starts.pop(msg.from_user.id)
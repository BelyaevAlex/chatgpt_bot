import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlite3 import Error



bot = Bot(token="6050756412:AAHVxNAxl_w1fMtn87GO9tWfac4RVd0CM5c")
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()


def add_row(connection, name, text, id):
  cursor = connection.cursor()
  try:
    cursor.execute(f"INSERT INTO {name} (text, id_tg) VALUES (?, ?);", (text, id))
    connection.commit()
    print("Query executed successfully")
  except Error as e:
      print(f"The error '{e}' occurred")


def add_row_chat(connection, name, text, id):
  cursor = connection.cursor()
  try:
    cursor.execute(f"INSERT INTO {name} (text, id_tg, answer) VALUES (?, ?, ?);", (text, id, 'no_answer'))
    connection.commit()
    print("Query executed successfully")
  except Error as e:
      print(f"The error '{e}' occurred")


def update_add_row_chat(connection, name, id, answer):
  cursor = connection.cursor()
  try:
    cursor.execute(f'UPDATE {name} SET answer = (?) WHERE id_tg = {id} AND answer = (?)', (str(answer), 'no_answer'))
    connection.commit()
    print("Query executed successfully")
  except Error as e:
      print(f"The error '{e}' occurred")



def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred post")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
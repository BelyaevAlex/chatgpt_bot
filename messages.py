from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button1_start1_text = "✅Да"

button1_start2_text = "➡️Далее"

button1_start3_text = "🚀Старт"

button1_main_text = "💳Донат автору"

button2_main_text = "✅Помощь"

button3_main_text = "💬Начать разговор"

button1_chat_text = "🛑Завершить разговор"


keyboard_start1 = ReplyKeyboardMarkup(resize_keyboard=True)

button1_start1 = KeyboardButton(button1_start1_text)

keyboard_start1.add(button1_start1)


keyboard_start2 = ReplyKeyboardMarkup(resize_keyboard=True)

button1_start2 = KeyboardButton(button1_start2_text)

keyboard_start2.add(button1_start2)


keyboard_start3 = ReplyKeyboardMarkup(resize_keyboard=True)

button1_start3 = KeyboardButton(button1_start3_text)

keyboard_start3.add(button1_start3)


keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)

button1_main = KeyboardButton(button1_main_text)
button2_main = KeyboardButton(button2_main_text)
button3_main = KeyboardButton(button3_main_text)

keyboard_main.add(button1_main, button2_main).add(button3_main)


keyboard_chat = ReplyKeyboardMarkup(resize_keyboard=True)

button1_chat = KeyboardButton(button1_chat_text)

keyboard_chat.add(button1_chat)

start0 = "Привет, я полностью бесплатный бот, который может как и просто разговаривать с тобой, так и отвечать на твои запрос ). Сейчас я проведу тебе маленькую экскурсию, если ты готов, то нажми кнопку Да внизу экрана"

start1 = "Я умею отвечать на вопросы, рассуждать, писать сочинения и ещё много чего."

start2 = """У меня есть команды: 
/start  пройти обучение заново
/help  помощь и рекомендации
/donate  Донат автору
/chat_start  начать разговор со мной
/chat_end  закончить разговор со мной
Также ты можешь со мной комуницировать и через кнопки которые есть у тебя внизу экрана. Ну что начнём? """


start3 = "Это главное меню, тут есть всё что тебе нужно. Ну что, удачи."

help = """⚠️Помощь: 


1️⃣Если я тебе ответил каким-то странным сообщением, значит на сервере что-то пошло не так, просто подожди немного и всё исправится.

2️⃣Если я долго не отвечаю, попробуй завершить разговор и начать его заново.

3️⃣Если будут какие-то замечания, вопросы или предложения пиши сюда: @bbe_lyaev


✅Рекомендации:


1️⃣Помни, что я не умею читать мысли, поэтому чем точнее вопрос, тем точнее ответ.

2️⃣При смене темы разговора завершай разговор и начинай новый, чтобы я не путался о чём мы сейчас говорим.

3️⃣Когда, во время разговора, я ответил на все твои вопросы, пожалуйста завершай разговор."""


error_write_corectly = "⚠️Чтобы начать со мной общаться - нажми ' 💬Начать разговор ' или введи команду /chat_start"

chat_start = "Какой вопрос ты мне бы хотел задать?"

chat_end = "Если появятся ещё какие-нибудь вопрос, то пиши - буду рад с тобой общаться👋"

chat_is_not_open = 'Вы ещё даже не начали общаться, а ты уже хочешь завершить разговор😢'


chat_is_already_open = 'Мы уже с тобой общаемся'


pozh = """Спасибо, что хочешь помочь автору, который является школьником) Вот ссылка на донат: 
https://www.donationalerts.com/r/bbe_lyaev"""

chat_is_overloaded = 'К сожелению, так как этот бот бесплатный, у него есть ограниения связанные с количеством запросов в минуту. Вы можете поддержать автора, чтобы он смог улучшить этого бота'
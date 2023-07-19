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

start0 = "Привет, это полностью бесплатный бот, который может как и просто разговаривать с вами, так и отвечать на ваши запрос ). Сейчас будет проведена маленькая экскурсия по боту, если вы готовы, то нажмите кнопку Да внизу экрана"

start1 = "Бот умеет отвечать на вопросы, рассуждать, писать сочинения и ещё много чего."

start2 = """У него есть команды: 
/start  пройти обучение заново
/help  помощь и рекомендации
/donate  Донат автору
/chat_start  начать разговор с ботом
/chat_end  закончить разговор с ботом
Также вы можете комуницировать с ботом и через кнопки которые есть у вас внизу экрана. Ну что начнём? """


start3 = "Это главное меню, тут есть всё что вам нужно. Ну что, удачи. P.S. первоначально советую ознакомиться со вкладкой Помощь"

help = """⚠️Помощь: 


1️⃣Если бот вам ответил каким-то странным сообщением, значит на сервере что-то пошло не так, просто подождите немного и всё исправится.

2️⃣Если бот долго не отвечает, попробуйте завершить разговор и начать его заново.

3️⃣Если будут какие-то замечания, вопросы или предложения пишите сюда: @bbe_lyaev


✅Рекомендации:


1️⃣Помните, что бот не умеет читать мысли, поэтому чем точнее вопрос, тем точнее ответ.

2️⃣При смене темы разговора завершайте разговор и начинайте новый, чтобы бот не путался о чём вы сейчас говорите.

3️⃣Когда, во время разговора, бот ответил на все ваши вопросы, пожалуйста завершайте разговор.

⚠️Ограничения:

1️⃣Бот не умеет принимать аудио, фото и видео файлы, даже если он пишет, что может

2️⃣Бот содержит данные только до 2021 года, что было после, он не знает"""


error_write_corectly = "⚠️Чтобы начать со мной общаться - нажмите ' 💬Начать разговор ' или введи команду /chat_start"

chat_start = "Какой вопрос вы хотели бы мне задать?"

chat_end = "Если появятся ещё какие-нибудь вопросы, то пишите - буду рад с вами пообщаться👋"

chat_is_not_open = 'Мы ещё даже не начали общаться, а вы уже хотите завершить разговор😢'


chat_is_already_open = 'Мы уже с вами общаемся'


pozh = """Спасибо, что хотите помочь автору, который является школьником) Вот ссылка на донат: 
https://www.donationalerts.com/r/bbe_lyaev"""

chat_is_overloaded = 'К сожелению, так как этот бот бесплатный, у него есть ограниения связанные с количеством запросов в минуту. Вы можете поддержать автора, чтобы он смог улучшить этого бота'
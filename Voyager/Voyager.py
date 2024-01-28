import sqlite3 as sl
from datetime import datetime as dt, timedelta
import FonProcess
from threading import Thread
from multiprocessing import Process
import asyncio
import gid as gid
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
loop = asyncio.get_event_loop()
#import TableManager
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Dispatcher
#from aiogram.fsm.context import FSMContext
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, date
import TableManager as tm
import GraphManager as gm
from math import radians
#загрузка необходимых библиотек

#индетефикатор бота
TOKEN_API="6443091891:AAEn1CmfGMhe0QpgsTf7mmrNZTvclHr-KFI"

#клавиатуры используемые в боте
kb = ReplyKeyboardMarkup()
b1=KeyboardButton('Создать новый запрос')
b2=KeyboardButton('Посмотреть предыдущий запрос')
b3=KeyboardButton('Убрать ежедневные уведомления')
kb.add(b1)
kb.add(b2)
kb.add(b3)

kblocation = ReplyKeyboardMarkup()
bl1=KeyboardButton('РФ')
bl2=KeyboardButton('США')
bl3=KeyboardButton('МИР')
kblocation.add(bl1)
kblocation.add(bl2)
kblocation.add(bl3)

kbweb = ReplyKeyboardMarkup()
bweb1=KeyboardButton('Web-поиск')
bweb2=KeyboardButton('Ютуб')
kbweb.add(bweb1)
kbweb.add(bweb2)


kbtime = ReplyKeyboardMarkup()
btime1=KeyboardButton('год')
btime2=KeyboardButton('три_месяца')
btime3=KeyboardButton('один_месяц')
kbtime.add(btime1)
kbtime.add(btime2)
kbtime.add(btime3)

kbdeltatime = ReplyKeyboardMarkup()
bdeltatime1=KeyboardButton('три дня')
bdeltatime2=KeyboardButton('неделя')
bdeltatime3=KeyboardButton('две недели')
kbdeltatime.add(bdeltatime1)
kbdeltatime.add(bdeltatime2)
kbdeltatime.add(bdeltatime3)

kbcategory = ReplyKeyboardMarkup()
bcategory1=KeyboardButton('Игры')
bcategory2=KeyboardButton('Развлечения')
bcategory3=KeyboardButton('Все_запросы')
kbcategory.add(bcategory1)
kbcategory.add(bcategory2)
kbcategory.add(bcategory3)

kba = ReplyKeyboardMarkup()
ba1=KeyboardButton('Да')
ba2=KeyboardButton('Нет')
kba.add(ba1)
kba.add(ba2)

kbdatazapros = ReplyKeyboardMarkup()
bdatazapros1=KeyboardButton('в 8 часов по МСК')
bdatazapros2=KeyboardButton('в 12 часов по МСК')
bdatazapros3=KeyboardButton('в 18 часов по МСК')
bdatazapros4=KeyboardButton('в 21 час по МСК')
kbdatazapros.add(bdatazapros1)
kbdatazapros.add(bdatazapros2)
kbdatazapros.add(bdatazapros3)
kbdatazapros.add(bdatazapros4)

kbtypeTop = ReplyKeyboardMarkup()
btypeTop1=KeyboardButton('Лидеры в скорости роста популярности')
btypeTop2=KeyboardButton('Лидеры по количеству запросов')
kbtypeTop.add(btypeTop1)
kbtypeTop.add(btypeTop2)

kbrequest_type = ReplyKeyboardMarkup()
brequest_type1=KeyboardButton('Темы поиска')
brequest_type2=KeyboardButton('Поисковые запросы')
kbrequest_type.add(brequest_type1)
kbrequest_type.add(brequest_type2)


#подключение к базе данных
con = sl.connect('data_trends.db')
cursor = con.cursor()

#Содание объектов бота
bot = Bot(token=TOKEN_API, parse_mode="HTML")
dp=Dispatcher(bot, loop=loop, storage=MemoryStorage())


class RequestState(StatesGroup):
    zapros = State()
class link_time(StatesGroup):
    Hour = State()


#Установка часового пояса отправки уведомления
scheduler =AsyncIOScheduler(timezone="Europe/Moscow")

#Функции запуска в определённое файла FonProcess отвечающий за отправку уведомлений
scheduler.add_job(FonProcess.send_message_time21, trigger='cron', hour=21, minute = 0, start_date=datetime.now(), kwargs={'bot': bot})
scheduler.add_job(FonProcess.send_message_time18, trigger='cron', hour=18, minute = 0, start_date=datetime.now(), kwargs={'bot': bot})
scheduler.add_job(FonProcess.send_message_time12, trigger='cron', hour=12, minute = 5, start_date=datetime.now(), kwargs={'bot': bot})
scheduler.add_job(FonProcess.send_message_time8, trigger='cron', hour=9, minute = 24, start_date=datetime.now(), kwargs={'bot': bot})
scheduler.start()

#Дальше будут написаны обработчики сообщений телеграм
#Команда запуска бота и отправки краткого описания
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=f"""Привет {message.from_user.first_name}! Ты открыл BotTrendsVoyager \n Главная цель бота - предостовлять информацию по изменению текущих трендов в интернете\nЧтобы узнать изменения нужно: \n1 создать запрос \n2 выбрать страну
3 выбрать платформу для анализа 
и тд
Что такое время анализа динамики роста?
Это период, за который анализируется изменение популярности
Что такое темы и поисковые запросы?
Пример 'как приготовить блины' - это запрос, а Еда, приготовление еды - это уже темы
Данные в таблице:
(номер в рейтинге)(название)()
(относительный рост популярности)""", reply_markup=kb)

#Команда убирающая ежедневную отправку
@dp.message_handler(lambda message: message.text == 'Убрать ежедневные уведомления')
async def new_command(message: types.Message):
    con = sl.connect('analysis.db')
    cursor = con.cursor()
    cursor.execute('DELETE FROM Users WHERE idU = (?)', (message.from_user.id,)) #Удаление пользователя из базы данных запросов
    con.commit()

#Команда создания нового запроса и запуска RequestState
@dp.message_handler(lambda message: message.text == 'Создать новый запрос')
async def new_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Готовим новый запрос', reply_markup=kblocation)
    await RequestState.zapros.set()
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    user = message.from_user.id
    
    cursor.execute('INSERT INTO Users (idU, numbeer) VALUES (?, ?)', 
                       (user, 2))  #Добавление запроса пользователя к базе данных отправки уведомлений
    
    con.commit()

#Команда просмотра сохранёного запроса
@dp.message_handler(lambda message: message.text == 'Посмотреть предыдущий запрос')
async def old_command(message: types.Message):
    text=""
    
    #загрузка запроса пользователя из базы данных
    with con:
        data = con.execute(f"SELECT * FROM Users WHERE idU={message.from_user.id}")
        print(data)
        for row in data:
            Time = row[1]
            country = row[2]
            search = row[3]
            category = row[4]
            MTime = row[5]
            deltatime = row[7]
            Type = row[9]
            TypeSearch = row[8]

    #объявление переменых для использования их структурировании даных
    current_time = dt.now() 
    sorter = tm.SorterElement()       
    sorter.State = country
    sorter.Category = category
    sorter.PeriodDays = Time
    sorter.RequestSearch = search
    sorter.RequestType = Type
    sorter.TypeSearch = TypeSearch
    sorter.DateFinish = date.today()
    sorter.DateStart = date.today() - timedelta(days=deltatime)      
        

    #???
    result = tm.Get_result_sorter("C:\\Programming\\pythonProject\\Voyager\\data_trends.db",sorter,'data_trends.db')
    border_day = tm.Get_border_date(result)
    last_day = tm.Get_list_day_with_place(result,border_day[1])
    start_day = tm.Get_list_day_with_place(result,border_day[0])
    list_chage_place = tm.Get_list_change_place(last_day,start_day)      
    list_change_data = tm.Get_last_chage_place_data(last_day, result)        
    #drop_out = tm.Get_drop_out(result, last_day)
    list_row_table_output = tm.Get_print_table_top(list_change_data)        
    print(list_row_table_output)
    sorter_change_day = tm.Sorter_request_list(list_change_data)
    path_to_image = "C:\\Users\\thepr\\Desktop\\Sputnik\\image"
    full_path = gm.PrintGraph(sorter_change_day, 0, 10, sorter,path_to_image)


    text=""
    for i in range(len(list_row_table_output)):
        text+=list_row_table_output[i]
        text+="\n"
    #отправка таблицы
    await bot.send_message(chat_id=message.from_user.id, text=text,
                           parse_mode="HTML", reply_markup=kb)

    #Отправка фото
    await bot.send_photo(chat_id=message.from_user.id, photo=open(full_path, 'rb'))


#3 команды для выбора страны
#1 команда выбор страны России
@dp.message_handler(lambda message: message.text == 'РФ', state=RequestState.zapros)# handler для обработки сообщений
async def RF_command(message: types.Message, state: FSMContext):
    country = 'ru'#присвоение переменной country значение ru
    await bot.send_message(chat_id=message.from_user.id, text="Выбрана страна - Россия", parse_mode="HTML", reply_markup=kbweb) # отправка ответного сообщения и установка клавиатуры для ответа на следующий запрос
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите анализируемую платформу</b>",parse_mode="HTML", reply_markup=kbweb)
    await message.delete()
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET country = ? WHERE idU = ? AND numbeer = 2',
                   (country, message.from_user.id)) #загрузка переменной в базу запросов
    con.commit() #обновление BD

#2 команда выбор страны США
@dp.message_handler(lambda message: message.text == 'США', state=RequestState.zapros)
async def USA_command(message: types.Message, state: FSMContext):
    
    country = 'us'
    await bot.send_message(chat_id=message.from_user.id, text="Выбрана страна - США", parse_mode="HTML", reply_markup=kbweb)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите анализируемую платформу</b>", parse_mode="HTML", reply_markup=kbweb)
    await message.delete()
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET country = ? WHERE idU = ?',
                   (country, message.from_user.id))
    con.commit()

#3 команда выбор всего мира
@dp.message_handler(lambda message: message.text == 'МИР', state=RequestState.zapros)
async def WOrld_command(message: types.Message, state: FSMContext):
    country = 'world'
    await bot.send_message(chat_id=message.from_user.id, text="Выбран весь мир", parse_mode="HTML", reply_markup=kbweb)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите анализируемую платформу</b>", parse_mode="HTML", reply_markup=kbweb)
    await message.delete()
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET country = ? WHERE idU = ?',
                   (country, message.from_user.id))
    con.commit()


#2 команды выбора анализируемой площадки площадки
#1 команда выбор Web-запросов как платформы
@dp.message_handler(lambda message: message.text == 'Web-поиск', state=RequestState.zapros)
async def WebSearch_command(message: types.Message, state: FSMContext):
    search = 'web'
    await bot.send_message(chat_id=message.from_user.id, text="Выбран тип поиска - Web-поиск", parse_mode="HTML", reply_markup=kbtime)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите период анализа</b>", parse_mode="HTML", reply_markup=kbtime)
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET search = ? WHERE idU = ?',
                   (search, message.from_user.id))
    con.commit()
#2 команда выбор ютуб платформы
@dp.message_handler(lambda message: message.text == 'Ютуб', state=RequestState.zapros)
async def YouTubeSearch_command(message: types.Message, state: FSMContext):
    search = 'youtube'
    await bot.send_message(chat_id=message.from_user.id, text="Выбран тип поиска - Ютуб", parse_mode="HTML", reply_markup=kbtime)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите период анализа</b>", parse_mode="HTML", reply_markup=kbtime)
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET search = ? WHERE idU = ?',
                   (search, message.from_user.id))
    con.commit()


#3 команды выбора анализируемого периода 
@dp.message_handler(lambda message: message.text == 'год', state=RequestState.zapros)
async def Year_command(message: types.Message, state: FSMContext):
    Time = '365'
    await bot.send_message(chat_id=message.from_user.id, text="Выбран период анализа - 1 год", parse_mode="HTML", reply_markup=kbdeltatime)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите период анализа динамики роста</b>", parse_mode="HTML", reply_markup=kbdeltatime)
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET Time = ? WHERE idU = ?',
                   (Time, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'три_месяца', state=RequestState.zapros)
async def Month3_command(message: types.Message, state: FSMContext):
    Time = "90"
    await bot.send_message(chat_id=message.from_user.id, text="Выбран период анализа - 3 месяца", parse_mode="HTML", reply_markup=kbdeltatime)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите период анализа динамики роста</b>", parse_mode="HTML", reply_markup=kbdeltatime)
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET Time = ? WHERE idU = ?',
                   (Time, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'один_месяц', state=RequestState.zapros)
async def Month_command(message: types.Message, state: FSMContext):
    Time = '30'
    await bot.send_message(chat_id=message.from_user.id, text="Выбран период анализа - 1 месяц", parse_mode="HTML", reply_markup=kbdeltatime)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите период анализа динамики роста</b>", parse_mode="HTML", reply_markup=kbdeltatime)
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET Time = ? WHERE idU = ?',
                   (Time, message.from_user.id))
    con.commit()

#3 команды выбора анализируемого периода для оценки динамики роста
@dp.message_handler(lambda message: message.text == 'три дня', state=RequestState.zapros)
async def Year_command(message: types.Message, state: FSMContext):
    
    deltatime = 3
    await bot.send_message(chat_id=message.from_user.id, text="Выбран период анализа динамики роста - 3 дня", parse_mode="HTML", reply_markup=kbtypeTop)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите - лидеров по популярности запросов или лидеров по росту популярности?</b>", parse_mode="HTML", reply_markup=kbtypeTop)
    
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET deltatime = ? WHERE idU = ?',
                   (deltatime, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'неделя', state=RequestState.zapros)
async def Month3_command(message: types.Message, state: FSMContext):
    
    deltatime = 7
    await bot.send_message(chat_id=message.from_user.id, text="Выбран период анализа - 7 дней", parse_mode="HTML", reply_markup=kbtypeTop)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите - лидеров по популярности запросов или лидеров по росту популярности?</b>", parse_mode="HTML", reply_markup=kbtypeTop)
    
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET deltatime = ? WHERE idU = ?',
                   (deltatime, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'две недели', state=RequestState.zapros)
async def Month_command(message: types.Message, state: FSMContext):
    
    deltatime = 14
    await bot.send_message(chat_id=message.from_user.id, text="Выбран период анализа - 14 дней", parse_mode="HTML", reply_markup=kbtypeTop)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите - лидеров по популярности запросов или лидеров по росту популярности?</b>", parse_mode="HTML", reply_markup=kbtypeTop)
    
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET deltatime = ? WHERE idU = ?',
                   (deltatime, message.from_user.id))
    con.commit()


@dp.message_handler(lambda message: message.text == 'Лидеры в скорости роста популярности', state=RequestState.zapros)
async def Rising_command(message: types.Message, state: FSMContext):
    
    type_search="rising"
    await bot.send_message(chat_id=message.from_user.id, text="Выбраны лидеры в скорости роста популярности", parse_mode="HTML", reply_markup=kbrequest_type)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите запросы или популярные темы</b>", parse_mode="HTML", reply_markup=kbrequest_type)
    
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET type_search = ? WHERE idU = ? AND numbeer = 2',
                   (type_search, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'Лидеры по количеству запросов', state=RequestState.zapros)
async def Top_command(message: types.Message, state: FSMContext):
    
    type_search="top"
    await bot.send_message(chat_id=message.from_user.id, text="Выбраны лидеры по количеству запросов.", parse_mode="HTML", reply_markup=kbrequest_type)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите запросы или популярные темы</b>", parse_mode="HTML", reply_markup=kbrequest_type)
    
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET type_search = ? WHERE idU = ? AND numbeer = 2',
                   (type_search, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'Темы поиска', state=RequestState.zapros)
async def request_entities_command(message: types.Message, state: FSMContext):
    
    request_type="entities"
    await bot.send_message(chat_id=message.from_user.id, text="Выбраны темы поиска", parse_mode="HTML", reply_markup=kbcategory)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите категорию поиска</b>", parse_mode="HTML", reply_markup=kbcategory)
    
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET request_type = ? WHERE idU = ? AND numbeer = 2',
                   (request_type, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'Поисковые запросы', state=RequestState.zapros)
async def request_queries_command(message: types.Message, state: FSMContext):
    
    request_type="queries"
    await bot.send_message(chat_id=message.from_user.id, text="Выбраны поисковые запросы", parse_mode="HTML", reply_markup=kbcategory)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Выберите категорию поиска</b>", parse_mode="HTML", reply_markup=kbcategory)
    
    await message.delete()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await RequestState.zapros.set()
    cursor.execute('UPDATE Users SET request_type = ? WHERE idU = ? AND numbeer = 2',
                   (request_type, message.from_user.id))
    con.commit()

#3 команды выбора категории поиска
@dp.message_handler(lambda message: message.text == 'Игры', state=RequestState.zapros)
async def Game_command(message: types.Message, state: FSMContext):
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    text=""
    global category
    category = 'game'
    cursor.execute('UPDATE Users SET category = ? WHERE idU = ?',
                   (category, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Процесс регестрации запроса закончен.",
                           parse_mode="HTML")
    await message.delete()
    await bot.send_message(chat_id=message.from_user.id, text="Скоро выведем ответ на ваш запрос. Подождите, пожалуйста",
                           parse_mode="HTML")
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    #загрузка запроса
    text = ""
    user = message.from_user.id
    data = con.execute(f"SELECT * FROM Users WHERE idU={user} AND numbeer=2")
    print(data)
    for row in data:
        Time = row[1]
        country = row[2]
        search = row[3]
        category = row[4]
        MTime = row[5]
        deltatime = row[7]
        Type = row[9]
        TypeSearch = row[8]

    
    
    
    #присвоение переменной
    current_time = dt.now()
    sorter = tm.SorterElement()       
    sorter.State = country
    sorter.Category = category
    sorter.PeriodDays = Time
    sorter.RequestSearch = search
    sorter.RequestType = Type
    sorter.TypeSearch = TypeSearch
    sorter.DateFinish = date.today()
    sorter.DateStart = date.today() - timedelta(days=deltatime)      
        
    #присвоение переменной
    result = tm.Get_result_sorter("C:\\Programming\\pythonProject\\Voyager\\data_trends.db",sorter,'data_trends.db')
    border_day = tm.Get_border_date(result)
    last_day = tm.Get_list_day_with_place(result,border_day[1])
    start_day = tm.Get_list_day_with_place(result,border_day[0])
    list_chage_place = tm.Get_list_change_place(last_day,start_day)      
    list_change_data = tm.Get_last_chage_place_data(last_day, result)        
    #drop_out = tm.Get_drop_out(result, last_day)
    list_row_table_output = tm.Get_print_table_top(list_change_data)        
    print(list_row_table_output)
    sorter_change_day = tm.Sorter_request_list(list_change_data)
    path_to_image = "C:\\Users\\thepr\\Desktop\\Sputnik\\image"
    full_path = gm.PrintGraph(sorter_change_day, 0, 10, sorter,path_to_image)
    text=""
    for i in range(len(list_row_table_output)):
        text+=list_row_table_output[i]
        text+="\n"
    
    await bot.send_message(chat_id=message.from_user.id, text=text,
                           parse_mode="HTML", reply_markup=kb)


    await bot.send_photo(chat_id=message.from_user.id, photo=open(full_path, 'rb'))
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вам присылать обновения по данному запросу?",
                           parse_mode="HTML", reply_markup=kba)

    


@dp.message_handler(lambda message: message.text == 'Развлечения', state=RequestState.zapros)
async def Razvlech_command(message: types.Message, state: FSMContext):
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    text = ""
    global category
    category = 'entertainment'
    cursor.execute('UPDATE Users SET category = ? WHERE idU = ?',
                   (category, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Процесс регестрации запроса закончен",
                           parse_mode="HTML")
    await message.delete()
    await bot.send_message(chat_id=message.from_user.id, text="Скоро выведем ответ на ваш запрос. Подождите, пожалуйста",
                           parse_mode="HTML")
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    #загрузка запроса
    text = ""
    
    user = message.from_user.id
    data = con.execute(f"SELECT * FROM Users WHERE idU={user} AND numbeer=2")
    print(data)
    for row in data:
        Time = row[1]
        country = row[2]
        search = row[3]
        category = row[4]
        MTime = row[5]
        deltatime = row[7]
        Type = row[9]
        TypeSearch = row[8]

    
    
    
    #присвоение переменной
    current_time = dt.now()
    sorter = tm.SorterElement()       
    sorter.State = country
    sorter.Category = category
    sorter.PeriodDays = Time
    sorter.RequestSearch = search
    sorter.RequestType = Type
    sorter.TypeSearch = TypeSearch
    sorter.DateFinish = date.today()
    sorter.DateStart = date.today() - timedelta(days=deltatime)      
        
    #присвоение переменной
    result = tm.Get_result_sorter("C:\\Programming\\pythonProject\\Voyager\\data_trends.db",sorter,'data_trends.db')
    border_day = tm.Get_border_date(result)
    last_day = tm.Get_list_day_with_place(result,border_day[1])
    start_day = tm.Get_list_day_with_place(result,border_day[0])
    list_chage_place = tm.Get_list_change_place(last_day,start_day)      
    list_change_data = tm.Get_last_chage_place_data(last_day, result)        
    #drop_out = tm.Get_drop_out(result, last_day)
    list_row_table_output = tm.Get_print_table_top(list_change_data)        
    print(list_row_table_output)
    sorter_change_day = tm.Sorter_request_list(list_change_data)
    path_to_image = "C:\\Users\\thepr\\Desktop\\Sputnik\\image"
    full_path = gm.PrintGraph(sorter_change_day, 0, 10, sorter,path_to_image)
    text=""
    for i in range(len(list_row_table_output)):
        text+=list_row_table_output[i]
        text+="\n"
    
    await bot.send_message(chat_id=message.from_user.id, text=text,
                           parse_mode="HTML", reply_markup=kb)


    await bot.send_photo(chat_id=message.from_user.id, photo=open(full_path, 'rb'))
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вам присылать обновения по данному запросу?",
                           parse_mode="HTML", reply_markup=kba)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)


@dp.message_handler(lambda message: message.text == 'Все_запросы', state=RequestState.zapros)
async def EveryCateg_command(message: types.Message, state: FSMContext):
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    text = ""
    category = 'all'
    cursor.execute('UPDATE Users SET category = ? WHERE idU = ?',
                   (category, message.from_user.id))
    con.commit()
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Процесс регестрации запроса закончен.",
                           parse_mode="HTML")
    await message.delete()
    await bot.send_message(chat_id=message.from_user.id, text="Скоро выведем ответ на ваш запрос. Подождите, пожалуйста",
                           parse_mode="HTML")
    bot.delete_message(message.from_user.id,message_id=message.message_id - 2)
    bot.delete_message(message.from_user.id,message_id=message.message_id - 3)
    await bot.send_message(chat_id=message.from_user.id, text="Скоро выведем ответ на ваш запрос. Подождите, пожалуйста",
                           parse_mode="HTML")
    
    #загрузка запроса
    text = ""
    user = message.from_user.id
    data = con.execute(f"SELECT * FROM Users WHERE idU={user} AND numbeer=2")
    print(data)
    for row in data:
        Time = row[1]
        country = row[2]
        search = row[3]
        category = row[4]
        MTime = row[5]
        deltatime = row[7]
        Type = row[9]
        TypeSearch = row[8]

    
    
    
    #присвоение переменной
    current_time = dt.now()
    sorter = tm.SorterElement()       
    sorter.State = country
    sorter.Category = category
    sorter.PeriodDays = Time
    sorter.RequestSearch = search
    sorter.RequestType = Type
    sorter.TypeSearch = TypeSearch
    sorter.DateFinish = date.today()
    sorter.DateStart = date.today() - timedelta(days=deltatime)      
        
    #присвоение переменной
    result = tm.Get_result_sorter("C:\\Programming\\pythonProject\\Voyager\\data_trends.db",sorter,'data_trends.db')
    border_day = tm.Get_border_date(result)
    last_day = tm.Get_list_day_with_place(result,border_day[1])
    start_day = tm.Get_list_day_with_place(result,border_day[0])
    list_chage_place = tm.Get_list_change_place(last_day,start_day)      
    list_change_data = tm.Get_last_chage_place_data(last_day, result)        
    #drop_out = tm.Get_drop_out(result, last_day)
    list_row_table_output = tm.Get_print_table_top(list_change_data)        
    print(list_row_table_output)
    sorter_change_day = tm.Sorter_request_list(list_change_data)
    path_to_image = "C:\\Users\\thepr\\Desktop\\Sputnik\\image"
    full_path = gm.PrintGraph(sorter_change_day, 0, 10, sorter,path_to_image)
    text=""
    for i in range(len(list_row_table_output)):
        text+=list_row_table_output[i]
        text+="\n"
    
    await bot.send_message(chat_id=message.from_user.id, text=text,
                           parse_mode="HTML", reply_markup=kb)


    await bot.send_photo(chat_id=message.from_user.id, photo=open(full_path, 'rb'))
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вам присылать обновения по данному запросу?",
                           parse_mode="HTML", reply_markup=kba)
    





#2 команды ответ на вопрос присылать ли уведомления по данному запросу м отправка его результатов
@dp.message_handler(lambda message: message.text == 'Да', state=RequestState.zapros)
async def Yes_command(message: types.Message, state: FSMContext):

    #удаление старого запроса
    
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    user = message.from_user.id
    data = con.execute(f"SELECT * FROM Users WHERE idU={user} AND numbeer=2")
    print(data)
    for row in data:
        Time = row[1]
        country = row[2]
        search = row[3]
        category = row[4]
        MTime = row[5]
        deltatime = row[7]
        Type = row[9]
        TypeSearch = row[8]
    cursor.execute('DELETE FROM Users WHERE idU = (?)', (message.from_user.id,))
    #сохранение нового
    data_link_user = 8
    user_id = message.from_user.id
    cursor.execute('INSERT INTO Users (idU, Time, country, search, category, MTime, deltatime, numbeer, request_type, Type_search) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (user_id, Time, country, search, category, MTime, deltatime, 1, Type, TypeSearch))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id, text="В какое время вам отправлять обновления по вашему запросу?",
                           parse_mode="HTML", reply_markup=kbdatazapros)

    

@dp.message_handler(lambda message: message.text == 'Нет', state=RequestState.zapros)
async def NO_command(message: types.Message, state: FSMContext):
    text = ""
    global category
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    user = message.from_user.id
    data = con.execute(f"SELECT * FROM Users WHERE idU={user} AND numbeer=2")
    print(data)
    for row in data:
        Time = row[1]
        country = row[2]
        search = row[3]
        category = row[4]
        MTime = row[5]
        deltatime = row[7]
        Type = row[9]
        TypeSearch = row[8]

    sorter = tm.SorterElement()       
    sorter.State = country
    sorter.Category = category
    sorter.PeriodDays = Time
    sorter.RequestSearch = search
    sorter.RequestType = Type
    sorter.TypeSearch = TypeSearch
    sorter.DateFinish = date.today()
    sorter.DateStart = date.today() - timedelta(days=deltatime)      
        

    result = tm.Get_result_sorter("C:\\Programming\\pythonProject\\Voyager\\data_trends.db",sorter,'data_trends.db')
    border_day = tm.Get_border_date(result)
    last_day = tm.Get_list_day_with_place(result,border_day[1])
    start_day = tm.Get_list_day_with_place(result,border_day[0])
    list_chage_place = tm.Get_list_change_place(last_day,start_day)      
    list_change_data = tm.Get_last_chage_place_data(last_day, result)        
    #drop_out = tm.Get_drop_out(result, last_day)
    list_row_table_output = tm.Get_print_table_top(list_change_data)        
    print(list_row_table_output)
    sorter_change_day = tm.Sorter_request_list(list_change_data)
    path_to_image = "C:\\Users\\thepr\\Desktop\\Sputnik\\image"
    full_path = gm.PrintGraph(sorter_change_day, 0, 10, sorter,path_to_image)
    text=""
    for i in range(len(list_row_table_output)):
        text+=list_row_table_output[i]
        text+="\n"
    

    await bot.send_message(chat_id=message.from_user.id, text=text,
                           parse_mode="HTML", reply_markup=kb)


    await bot.send_photo(chat_id=message.from_user.id, photo=open(full_path, 'rb'))

    await state.finish()



@dp.message_handler(lambda message: message.text == 'в 8 часов по МСК', state=RequestState.zapros)
async def Eighthourcomand(message: types.Message, state: FSMContext):
    data_link_user=8
    cursor.execute('UPDATE Users SET Mtime = ? WHERE idU = ?',
                   (data_link_user, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id, text="Время отправки установлено",
                           parse_mode="HTML", reply_markup=kb)
    await state.finish()

@dp.message_handler(lambda message: message.text == 'в 12 часов по МСК', state=RequestState.zapros)
async def Twelvehourcomand(message: types.Message, state: FSMContext):
    print("RequestStateRequestStateAA")
    data_link_user=12
    cursor.execute('UPDATE Users SET Mtime = ? WHERE idU = ?',
                   (data_link_user, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id, text="Время отправки установлено",
                           parse_mode="HTML", reply_markup=kb)
    await state.finish()

@dp.message_handler(lambda message: message.text == 'в 18 часов по МСК', state=RequestState.zapros)
async def Eightinhourcomand(message: types.Message, state: FSMContext):
    print("RequestStateRequestStateAA")
    data_link_user=18
    cursor.execute('UPDATE Users SET Mtime = ? WHERE idU = ?',
                   (data_link_user, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id, text="Время отправки установлено",
                           parse_mode="HTML", reply_markup=kb)
    await state.finish()

@dp.message_handler(lambda message: message.text == 'в 21 час по МСК', state=RequestState.zapros)
async def TwentyOnehourcomand(message: types.Message, state: FSMContext):
    print("RequestStateRequestStateAA")
    data_link_user=21
    cursor.execute('UPDATE Users SET Mtime = ? WHERE idU = ?',
                   (data_link_user, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id, text="Время отправки установлено",
                           parse_mode="HTML", reply_markup=kb)

    await state.finish()
    
    

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)









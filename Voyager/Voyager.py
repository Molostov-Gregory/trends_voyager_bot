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
bdatazapros1=KeyboardButton('в восемь часов')
bdatazapros2=KeyboardButton('в двенадцать часов')
bdatazapros3=KeyboardButton('в восемнадцать часов')
bdatazapros4=KeyboardButton('в двадцать первый час')
kbdatazapros.add(bdatazapros1)
kbdatazapros.add(bdatazapros2)
kbdatazapros.add(bdatazapros3)
kbdatazapros.add(bdatazapros4)



con = sl.connect('data_trends.db')
cursor = con.cursor()

bot = Bot(token=TOKEN_API, parse_mode="HTML")
dp=Dispatcher(bot, loop=loop, storage=MemoryStorage())
data_link_user=''
link_flag=0

class aaaa(StatesGroup):
    zapros = State()
class link_time(StatesGroup):
    Hour = State()

scheduler =AsyncIOScheduler(timezone="Europe/Moscow")
scheduler.add_job(FonProcess.send_message_time21, trigger='cron', hour=17, minute = 27, start_date=datetime.now(), kwargs={'bot': bot})
scheduler.add_job(FonProcess.send_message_time18, trigger='cron', hour=17, minute = 30, start_date=datetime.now(), kwargs={'bot': bot})
scheduler.add_job(FonProcess.send_message_time12, trigger='cron', hour=12, minute = 0, start_date=datetime.now(), kwargs={'bot': bot})
scheduler.add_job(FonProcess.send_message_time8, trigger='cron', hour=8, minute = 0, start_date=datetime.now(), kwargs={'bot': bot})
scheduler.start()



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Добро пожаловать в бот!", reply_markup=kb)

@dp.message_handler(lambda message: message.text == 'Убрать ежедневные уведомления')
async def new_command(message: types.Message):
    con = sl.connect('analysis.db')
    cursor = con.cursor()
    cursor.execute('DELETE FROM Users WHERE idU = (?)', (message.from_user.id,))
    con.commit()



@dp.message_handler(lambda message: message.text == 'Создать новый запрос')
async def new_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Готовим новый запрос', parse_mode="HTML", reply_markup=kblocation)
    await aaaa.zapros.set()
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    user = message.from_user.id
    
    cursor.execute('INSERT INTO Users (idU, numbeer) VALUES (?, ?)',
                       (user, 2))
    
    con.commit()


@dp.message_handler(lambda message: message.text == 'Посмотреть предыдущий запрос')
async def old_command(message: types.Message):
    text=""
    global Time
    global country
    global search
    global category

    with con:
        data = con.execute(f"SELECT * FROM Users WHERE idU={message.from_user.id}")
        print(data)
        for row in data:
            Time = row[1]
            country = row[2]
            search = row[3]
            category = row[4]
        
    current_time = dt.now()

    sorter = tm.SorterElement()       
    sorter.State = country
    sorter.Category = category
    sorter.PeriodDays = Time
    sorter.RequestSearch = search
    sorter.RequestType = "queries"
    sorter.TypeSearch = "rising"
    sorter.DateFinish = date.today()
    sorter.DateStart = date.today() - timedelta(days=14)      
        

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


@dp.message_handler(lambda message: message.text == 'РФ', state=aaaa.zapros)
async def RF_command(message: types.Message, state: FSMContext):
    country = 'ru'
    await bot.send_message(chat_id=message.from_user.id, text="Выбрана страна - Россия. Выберите тип поиска", parse_mode="HTML", reply_markup=kbweb)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET country = ? WHERE idU = ? AND numbeer = 2',
                   (country, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'США', state=aaaa.zapros)
async def USA_command(message: types.Message, state: FSMContext):
    
    country = 'us'
    await bot.send_message(chat_id=message.from_user.id, text="Выбрана страна - США. Выберите тип поиска", parse_mode="HTML", reply_markup=kbweb)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET country = ? WHERE idU = ?',
                   (country, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'МИР', state=aaaa.zapros)
async def WOrld_command(message: types.Message, state: FSMContext):
    country = 'world'
    await bot.send_message(chat_id=message.from_user.id, text="Выбран весь мир. Выберите тип поиска", parse_mode="HTML", reply_markup=kbweb)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET country = ? WHERE idU = ?',
                   (country, message.from_user.id))
    con.commit()



@dp.message_handler(lambda message: message.text == 'Web-поиск', state=aaaa.zapros)
async def WebSearch_command(message: types.Message, state: FSMContext):
    search = 'web'
    await bot.send_message(chat_id=message.from_user.id, text="Выбран тип поиска - Web-поиск. Выберите период анализа", parse_mode="HTML", reply_markup=kbtime)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET search = ? WHERE idU = ?',
                   (search, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'Ютуб', state=aaaa.zapros)
async def YouTubeSearch_command(message: types.Message, state: FSMContext):
    search = 'youtube'
    await bot.send_message(chat_id=message.from_user.id, text="Выбран тип поиска - Ютуб. Выберите период анализа", parse_mode="HTML", reply_markup=kbtime)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET search = ? WHERE idU = ?',
                   (search, message.from_user.id))
    con.commit()



@dp.message_handler(lambda message: message.text == 'год', state=aaaa.zapros)
async def Year_command(message: types.Message, state: FSMContext):
    Time = '365'
    await bot.send_message(chat_id=message.from_user.id, text="Выбран период анализа - 1 год. Выберите период анализа динамики роста", parse_mode="HTML", reply_markup=kbdeltatime)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET Time = ? WHERE idU = ?',
                   (Time, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'три_месяца', state=aaaa.zapros)
async def Month3_command(message: types.Message, state: FSMContext):
    Time = "90"
    await bot.send_message(chat_id=message.from_user.id, text="Выбрано период анализа - 3 месяца. Выберите период анализа динамики роста", parse_mode="HTML", reply_markup=kbdeltatime)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET Time = ? WHERE idU = ?',
                   (Time, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'один_месяц', state=aaaa.zapros)
async def Month_command(message: types.Message, state: FSMContext):
    Time = '30'
    await bot.send_message(chat_id=message.from_user.id, text="Выбрано период анализа - 1 месяц. Выберите период анализа динамики роста", parse_mode="HTML", reply_markup=kbdeltatime)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET Time = ? WHERE idU = ?',
                   (Time, message.from_user.id))
    con.commit()
import time
@dp.message_handler(lambda message: message.text == 'три дня', state=aaaa.zapros)
async def Year_command(message: types.Message, state: FSMContext):
    
    deltatime = 3
    await bot.send_message(chat_id=message.from_user.id, text="Выбран период анализа динамики роста - 3 дня. Выберите категорию поиска", parse_mode="HTML", reply_markup=kbcategory)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET deltatime = ? WHERE idU = ?',
                   (deltatime, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'неделя', state=aaaa.zapros)
async def Month3_command(message: types.Message, state: FSMContext):
    
    deltatime = 7
    await bot.send_message(chat_id=message.from_user.id, text="Выбрано период анализа - 7 дней. Выберите категорию поиска", parse_mode="HTML", reply_markup=kbcategory)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET deltatime = ? WHERE idU = ?',
                   (deltatime, message.from_user.id))
    con.commit()

@dp.message_handler(lambda message: message.text == 'две недели', state=aaaa.zapros)
async def Month_command(message: types.Message, state: FSMContext):
    
    deltatime = 14
    await bot.send_message(chat_id=message.from_user.id, text="Выбрано период анализа - 14 дней. Выберите категорию поиска", parse_mode="HTML", reply_markup=kbcategory)
    await message.delete()
    await aaaa.zapros.set()
    cursor.execute('UPDATE Users SET deltatime = ? WHERE idU = ?',
                   (deltatime, message.from_user.id))
    con.commit()


@dp.message_handler(lambda message: message.text == 'Игры', state=aaaa.zapros)
async def Game_command(message: types.Message, state: FSMContext):
    
    text=""
    global category
    category = 'game'
    cursor.execute('UPDATE Users SET category = ? WHERE idU = ?',
                   (category, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Процесс регестрации закончен. Ваш запрос {country}, {search}, {Time}, {category}",
                           parse_mode="HTML")
    await message.delete()
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вам присылать обновения по данному запросу?",
                           parse_mode="HTML", reply_markup=kba)








@dp.message_handler(lambda message: message.text == 'Развлечения', state=aaaa.zapros)
async def Razvlech_command(message: types.Message, state: FSMContext):
    
    text = ""
    global category
    category = 'entertainment'
    cursor.execute('UPDATE Users SET category = ? WHERE idU = ?',
                   (category, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Процесс регестрации закончен. Ваш запрос {country}, {search}, {Time}, {category}",
                           parse_mode="HTML")
    await message.delete()
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вам присылать обновения по данному запросу?",
                           parse_mode="HTML", reply_markup=kba)


@dp.message_handler(lambda message: message.text == 'Все_запросы', state=aaaa.zapros)
async def EveryCateg_command(message: types.Message, state: FSMContext):
    
    text = ""
    category = 'all'
    cursor.execute('UPDATE Users SET category = ? WHERE idU = ?',
                   (category, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Процесс регестрации закончен. Ваш запрос {country}, {search}, {Time}, {category}",
                           parse_mode="HTML")
    await message.delete()
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Вам присылать обновения по данному запросу?",
                           parse_mode="HTML", reply_markup=kba)


@dp.message_handler(lambda message: message.text == 'Да', state=aaaa.zapros)
async def YesNO_command(message: types.Message, state: FSMContext):
    
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

    
    cursor.execute('DELETE FROM Users WHERE idU = (?)', (message.from_user.id,))
    UserSet.add(int(message.from_user.id))
    data_link_user = 8
    user_id = message.from_user.id
    cursor.execute('INSERT INTO Users (idU, Time, country, search, category, MTime, deltatime, numbeer) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (user_id, Time, country, search, category, MTime, deltatime, 1))
    con.commit()
    
    

    current_time = dt.now()

    sorter = tm.SorterElement()       
    sorter.State = country
    sorter.Category = category
    sorter.PeriodDays = Time
    sorter.RequestSearch = search
    sorter.RequestType = "queries"
    sorter.TypeSearch = "rising"
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


    await bot.send_message(chat_id=message.from_user.id, text="В какое время вам отправлять обновления по вашему запросу?",
                           parse_mode="HTML", reply_markup=kbdatazapros)


@dp.message_handler(lambda message: message.text == 'в восемь часов', state=aaaa.zapros)
async def Eighthourcomand(message: types.Message, state: FSMContext):
    data_link_user=8
    cursor.execute('UPDATE Users SET Mtime = ? WHERE idU = ?',
                   (data_link_user, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id, text="Время отправки установлено",
                           parse_mode="HTML", reply_markup=kb)

@dp.message_handler(lambda message: message.text == 'в двенадцать часов', state=aaaa.zapros)
async def Twelvehourcomand(message: types.Message, state: FSMContext):
    print("AAAAAAAAAA")
    data_link_user=12
    cursor.execute('UPDATE Users SET Mtime = ? WHERE idU = ?',
                   (data_link_user, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id, text="Время отправки установлено",
                           parse_mode="HTML", reply_markup=kb)

@dp.message_handler(lambda message: message.text == 'в восемнадцать часов', state=aaaa.zapros)
async def Eightinhourcomand(message: types.Message, state: FSMContext):
    print("AAAAAAAAAA")
    data_link_user=18
    cursor.execute('UPDATE Users SET Mtime = ? WHERE idU = ?',
                   (data_link_user, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id, text="Время отправки установлено",
                           parse_mode="HTML", reply_markup=kb)

@dp.message_handler(lambda message: message.text == 'в двадцать первый час', state=aaaa.zapros)
async def TwentyOnehourcomand(message: types.Message, state: FSMContext):
    print("AAAAAAAAAA")
    data_link_user=21
    cursor.execute('UPDATE Users SET Mtime = ? WHERE idU = ?',
                   (data_link_user, message.from_user.id))
    con.commit()
    await bot.send_message(chat_id=message.from_user.id, text="Время отправки установлено",
                           parse_mode="HTML", reply_markup=kb)

@dp.message_handler(lambda message: message.text == 'Нет', state=aaaa.zapros)
async def NO_command(message: types.Message, state: FSMContext):
    global category
    global Time
    global country
    global search
    global func_category
    global data_link_user
    global UserSet
    text = ""
    global category
    con = sl.connect('analysis.db')
    cursor = con.cursor()

    with con:
        data = con.execute(
            f"SELECT id, request, value FROM data_trends WHERE categories = \'{category}\' AND period_days = {Time} AND state = \'{country}\' AND request_search = \'{search}\'")
        for row in data:
            text += str(row)
            text += "\n"
    await bot.send_message(chat_id=message.from_user.id, text=text,
                           parse_mode="HTML", reply_markup=kb)

    await state.finish()










if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
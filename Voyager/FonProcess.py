
import TableManager as tm
import GraphManager as gm
from datetime import datetime as dt, timedelta
from datetime import datetime, date

import sqlite3 as sl
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
"""kb = ReplyKeyboardMarkup()
b1=KeyboardButton('Создать новый запрос')
b2=KeyboardButton('Посмотреть предыдущий запрос')
b3=KeyboardButton('Убрать ежедневные уведомления')
kb.add(b1)
kb.add(b2)
kb.add(b3)"""
async def send_message_time8(bot: Bot):
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    text=''
    data = cursor.execute('SELECT idU FROM Users')
    users = []
    for row in data:
        users.append(row[0])
    
    list(users)
    print(users)

    for user in users:
        text=""
        n = 1

        with con:
            str1 = f"SELECT * FROM Users WHERE idU = {user} AND numbeer = {n} "
            data = con.execute(str1)
            print(data)
            MTime = 0
            for row in data:
                Time = row[1]
                country = row[2] 
                search = row[3]
                category = row[4]
                MTime = row[5]
                deltatime = row[7]
            if MTime == 8:
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

                await bot.send_message(chat_id=user, text=text,
                                       parse_mode="HTML")


                await bot.send_photo(chat_id=user, photo=open(full_path, 'rb'))



async def send_message_time12(bot: Bot):
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    text=''
    data = cursor.execute('SELECT idU FROM Users')
    users = []
    for row in data:
        users.append(row[0])
    
    list(users)
    print(users)

    for user in users:
        text=""
        n = 1

        with con:
            str1 = f"SELECT * FROM Users WHERE idU = {user} AND numbeer = {n} "
            data = con.execute(str1)
            print(data)
            MTime = 0
            for row in data:
                Time = row[1]
                country = row[2] 
                search = row[3]
                category = row[4]
                MTime = row[5]
                deltatime = row[7]
            if MTime == 12:
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

                await bot.send_message(chat_id=user, text=text,
                                       parse_mode="HTML")


                await bot.send_photo(chat_id=user, photo=open(full_path, 'rb'))

async def send_message_time18(bot: Bot):
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    text=''
    data = cursor.execute('SELECT idU FROM Users')
    users = []
    for row in data:
        users.append(row[0])
    
    list(users)
    print(users)

    for user in users:
        text=""
        n = 1

        with con:
            str1 = f"SELECT * FROM Users WHERE idU = {user} AND numbeer = {n} "
            data = con.execute(str1)
            print(data)
            MTime = 0
            for row in data:
                Time = row[1]
                country = row[2] 
                search = row[3]
                category = row[4]
                MTime = row[5]
                deltatime = row[7]
            if MTime == 18:
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

                await bot.send_message(chat_id=user, text=text,
                                       parse_mode="HTML")


                await bot.send_photo(chat_id=user, photo=open(full_path, 'rb'))


async def send_message_time21(bot: Bot):
    con = sl.connect('data_trends.db')
    cursor = con.cursor()
    text=''
    data = cursor.execute('SELECT idU FROM Users')
    users = []
    for row in data:
        users.append(row[0])
    
    list(users)
    print(users)

    for user in users:
        text=""
        n = 1

        with con:
            str1 = f"SELECT * FROM Users WHERE idU = {user} AND numbeer = {n} "
            data = con.execute(str1)
            print(data)
            MTime = 0
            for row in data:
                Time = row[1]
                country = row[2] 
                search = row[3]
                category = row[4]
                MTime = row[5]
                deltatime = row[7]
            if MTime == 21:
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

                await bot.send_message(chat_id=user, text=text,
                                       parse_mode="HTML")


                await bot.send_photo(chat_id=user, photo=open(full_path, 'rb'))
import datetime
import sqlite3 as sl
import copy

class ValueElement:
    Date = datetime.timedelta.min
    Request = ""
    Value = 0
    Place = 0
    PlaceChange = ""
    PlaceTrendChange =""
    
class SorterElement:
    DateFinish = datetime.date.today()
    DateStart = DateFinish - datetime.timedelta(days=7)
    State = ""
    PeriodDays = 0
    Category = ""
    RequestType = ""
    TypeSearch = ""
    RequestSearch = ""
    
def Get_result_sorter(dbName,sorter, dbnormalname):

    currentDate = sorter.DateStart
    finishDate = sorter.DateFinish
    values = []
    
    while(currentDate <= finishDate):
        dateStr = currentDate.strftime("%d-%m-%Y")
        date = f"date = '{dateStr}'"
        state = f" AND state = '{sorter.State}'" if sorter.State!="" else ""
        category = f" AND categories = '{sorter.Category}'" if sorter.Category!="" else ""
        period_days = f" AND period_days = {sorter.PeriodDays}" if sorter.PeriodDays!="" else ""
        request_search = f" AND request_search = '{sorter.RequestSearch}'" if sorter.RequestSearch != "" else ""
        request_type = f" AND request_type = '{sorter.RequestType}'" if sorter.RequestType != "" else ""
        type_search = f" AND type_search = '{sorter.TypeSearch}'" if sorter.TypeSearch != "" else ""
        conD = sl.connect(dbnormalname)
        cursorD = conD.cursor()
        listD = ""
        request = f"SELECT date, request, value FROM google_trends WHERE {date}{state}{category}{period_days}{request_search}{request_type}{type_search} ORDER BY value DESC"
        with conD:
            data = conD.execute(request)
            for row in data:
                value = []
                date_str = row[0].split("-")
                date_0 = datetime.date(int(date_str[2]),int(date_str[1]),int(date_str[0]))
                value.append(date_0)
                value.append(row[1])
                value.append(row[2])
                value.append(0)
                value.append("")
                value.append(0)
                values.append(value)               

        
        currentDate += datetime.timedelta(days=1)
    return values

def Extract_unique_queries(values):
    unique_list = []
    if type(values) is list:
        for value in values:
            if type(value) is list:
                if not value[1] in unique_list:
                    unique_list.append(value[1])
                    
    return(unique_list)

def Extract_unique_queries_in_sorter_list(values):
    unique_list = []
    if type(values) is list:
        for value in values:
            if type(value) is list:
                if not value[1] in unique_list:
                    unique_list.append(value[1])
                    
    return(unique_list)
                    
           
            
def Sorter_request_list(old_list):
    new_list = copy.deepcopy(old_list)
    string_list = Extract_unique_queries(new_list)
    sorter_list = []
    queries_row = []
    for query in string_list:
        for index, value in reversed(list(enumerate(new_list))):
            verification_query = new_list[index][1]
            if query == verification_query:
                queries_row.append(copy.deepcopy(new_list[index]))
                new_list.pop(index)
        queries_row = sorted(queries_row, key=lambda l1: l1[0])
        sorter_list.append(copy.deepcopy(queries_row))
        queries_row = []
    return sorter_list

def Get_border_date(input_list):
    min_date = datetime.date(2100,1,1)
    max_date = datetime.date(2000,1,1)
    for row in input_list:
        date_0 = row[0]
        if date_0 < min_date:
            min_date = date_0
        if date_0 > max_date:
            max_date = date_0
    return min_date, max_date
    
def Get_list_day_with_place(input_list, day):
    border_day = Get_border_date(input_list)
    list_day = []
    for item in input_list:
        date_0 = item[0]
        if date_0 == day:
            list_day.append(item)
    list_day = sorted(list_day, key=lambda last_day_item: last_day_item[2], reverse=True)
    for i in range(len(list_day)):
        list_day[i][3] = i+1
    return list_day

def Get_drop_out(input_list, last_day_data):
    drop_out = []
    name_data = Extract_unique_queries(last_day_data)
    for item in input_list:        
        if not item[1] in name_data:
            item[4] = "drop out"
            item[5] = -1
            drop_out.append(item)
    drop_out = sorted(drop_out, key=lambda drop_out_1: drop_out_1[2], reverse=True)
    return drop_out

def Get_list_change_place(last_day_list,start_day_list):
    
    for last_item in last_day_list:
        query_last_item = last_item[1]
        for start_item in start_day_list:
            query_start_item = start_item[1]
            if query_last_item in query_start_item:
                change = start_item[3] - last_item[3]
                if change > 0:
                    last_item[4] = "+"+str(change)
                    last_item[5] = 1
                    break
                elif change < 0:
                    last_item[4] = str(change)
                    last_item[5] = -1
                    break
                else: 
                    last_item[4] = str(change)
                    last_item[5] = 0
                    break
            else:
                last_item[4] = "new"
                last_item[5] = 1
    return last_day_list

def Get_string_row_table_place(table_list):
    table_string_row_list = []
    #for item in table_list:
        

def Get_last_chage_place_data(last_day, request_list):
    extract_last_day = copy.deepcopy(last_day)
    for item in last_day:
        for request in request_list:
            itm1 = request[1]
            itm0 = item[1]
            if itm1 == itm0:   
                dt1 = request[0]
                dt0 = item[0]
                if dt1 != dt0:
                    extract_last_day.append(request)
    list1 = sorted(extract_last_day, key=lambda l1: l1[2], reverse=True)
    return list1
                

def Get_print_table_top(list_input):
        sorter_change_day = Sorter_request_list(list_input)
        list_str = []
        for i in range(len(sorter_change_day)):
            item_list = sorter_change_day[i]
            str0 = []
            str1 = ""
            l0 = sorted(item_list, key=lambda l1: l1[0], reverse=True)
            row = l0[0]
            str1 = str(i+1) + ". " + row[1] + " (" + row[4]  + ")\n ("
            str0.append(str1)
            str1 = " => " + str(row[2]) + "%)" 
            str0.append(str1)                   

            l0 = sorted(item_list, key=lambda l1: l1[0])
            str1 = str(l0[0][2])+"%"
            str2 = str0[0]+str1 + str0[1]
            list_str.append(str2)
            print(str2)
        return list_str
            
def Get_print_table_drop(list_drop_out):
        sorter_change_day = Sorter_request_list(list_drop_out)
        list_str = []
        for i in range(len(sorter_change_day)):
            item_list = sorter_change_day[i]
            str0 = []
            str1 = ""
            l0 = sorted(item_list, key=lambda l1: l1[2], reverse=True)
            row = l0[0]
            str1 = row[1] + " (" + row[4]  + ")\n ("
            str0.append(str1)
            str1 = " => " + str(row[2]) + "%)" 
            str0.append(str1)                   

            l0 = sorted(item_list, key=lambda l1: l1[2])
            str1 = str(l0[0][2])+"%"
            str2 = str0[0]+str1 + str0[1]
            list_str.append(str2)
            print(str2)
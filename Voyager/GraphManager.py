import copy
import datetime as dt
from datetime import datetime

import numpy as np # installed with matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import (YEARLY,WEEKLY, DateFormatter, RRuleLocator, drange,
                              rrulewrapper)
import matplotlib.colors as mcolors
from matplotlib.ticker import NullFormatter

def Get_list_colors():
    colors = []
    colors.append("fuchsia")
    colors.append("r")
    colors.append("lightcoral")
    colors.append("sandybrown")
    #colors.append("darkorange")
    colors.append("gold")
    colors.append("y")
    colors.append("yellowgreen")
    colors.append("lawngreen")
    colors.append("limegreen")
    colors.append("seagreen")
    colors.append("mediumturquoise")
    colors.append("aqua")
    colors.append("royalblue")
    colors.append("blue")
    return colors
    
def Get_markers_line():
    markers = ["o","v","^","<",">","1","2","3","4","s","p","*","h","H","+","x","x","D","d","|","_"]
    return markers
    

def Get_border_date(input_list):
    min_date = dt.date(2100,1,1)
    max_date = dt.date(2000,1,1)
    for item in input_list:
        for row in item:
            date_0 = row[0]
            if date_0 < min_date:
                min_date = date_0
            if date_0 > max_date:
                max_date = date_0
    return min_date, max_date
      

def Get_line_axix(input_list):
    border_dates = Get_border_date(input_list)
    current_date = copy.deepcopy(border_dates[0])
    end_date = border_dates[1]
    line_axix = []
    while current_date<=end_date:
        line_axix.append(current_date)
        current_date += dt.timedelta(days=1)
    return line_axix


def PrintGraph(sorter_list, start_point, size_count_lines, sorter,path_to_image):


        
    graphs = []
    
    colors = Get_list_colors()
    markers = Get_markers_line()
    if size_count_lines > len(colors):
        size_count_lines = len(colors)
    if size_count_lines > len(markers):
        size_count_lines = len(markers)

    rule = rrulewrapper(WEEKLY)
    #loc = RRuleLocator(rule)
    fig, ax = plt.subplots(1, 1, layout='constrained', figsize=(10, 8))
    max_value = 0
    min_value = 10000
    for i in range(size_count_lines): 
        query_value = sorter_list[i+start_point]
        graph = []        
        grqph_x = []
        grqph_y = []
        for row in query_value:
            grqph_y.append(row[0])
            grqph_x.append(row[2])
            if max_value < row[2]:
                max_value = row[2]
            if min_value > row[2]:
                min_value = row[2]
        graph.append((grqph_x,grqph_y))
        graphs.append(copy.deepcopy(graph))
        legend = query_value[0][1] + " "
        plt.plot(grqph_y, grqph_x, color=colors[i],marker=markers[i], label=str(i+start_point+1) +". "+legend)   
    
    plt.legend(bbox_to_anchor=(1, -0.1))  
    step0 = max_value // 10
    x_step = np.arange(start = (min_value-1)//10*10, stop = ((max_value+5)//10+1)*10, step = (step0//10)*10)
        
        
    months = mdates.MonthLocator()
    days = mdates.DayLocator()
    timeFmt = mdates.DateFormatter('%d')
    
    now_date = datetime.now()
    border_date = Get_border_date(sorter_list)

    plt.title(f'Changing trends ({sorter.State}-{sorter.Category}-{sorter.PeriodDays}-{sorter.RequestSearch}-{sorter.RequestType}) {now_date.strftime("%Y-%m-%d")}')
    locator = mdates.AutoDateLocator(minticks=1, maxticks=5)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_formatter(NullFormatter())
    line_axix = Get_line_axix(sorter_list)
    ax.set_xticks(line_axix)
    ax.set_yticks(x_step)

    
    
    
    name_tible1 = now_date.strftime("%Y-%m-%d_%H-%M-%S_%f")
    name_tible2 = str(sorter.State[0])+sorter.Category[0]+str(sorter.PeriodDays)+sorter.RequestSearch[0]+sorter.RequestType[0]+sorter.TypeSearch[0]
    name_tible = name_tible1 +"_"+ name_tible2
    
    full_name_image = f'{path_to_image}\\{name_tible}.png'
    plt.savefig(full_name_image)
    print(full_name_image)
    #plt.show()
    return full_name_image


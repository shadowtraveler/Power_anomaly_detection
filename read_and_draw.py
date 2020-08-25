# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 20:13:04 2020

@author: steve
"""

import numpy as np
from dateutil.parser import parse
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

def read(start_day,end_day,type_key,my_path='D:/document/NCTU_sec1/Powermeter/'):
    try:
        print("Loading...")
        if(start_day>end_day):
            print("Error")
        key=0
        dt=pd.DataFrame()
        Path_dictionary=['Consumption-O','Current1','Current2','Power1','Power2','Volt1','Volt2',]
        my_path=my_path+str(Path_dictionary[type_key])
        my_List=os.listdir(my_path)
        for file in my_List:
            if(key==0):
                key=1
                if(end_day<parse(file[:10])):
                    print("end day out of range.")
                    break
                elif(start_day<parse(file[:10])):
                    print("The data is start from "+str(parse(file[:10]))+"\nstart day changed to "+str(parse(file[:10]))+".")
                    start_day=parse(file[:10])
            if(start_day<=parse(file[:10]) and end_day>=parse(file[:10])):
                dt_tmp=pd.read_csv(os.path.join(my_path,file))
                dt=dt.append(dt_tmp,ignore_index=True)
        return start_day,dt
    except:
        raise ValueError("There is an error in read_and_save function\nPlease check your path.")
        
def start_end():
    while(1):
        input_day=input("input start day(eg.2018-09-18 12:20:13):")
        try:
            start_day=parse(input_day)
            break
        except:
            print("error,wrong data format or range.")
    while(1):
        input_day=input("input end time(eg.2020-10-18 12:20:13):")
        try:
            end_day=parse(input_day)
            break
        except:
            print("error,wrong data format or range.")
    return start_day,end_day

def draw_six(data):
    #dateFormatter = "%A, %B %d, %Y %H:%M:%S"
    data=data.drop_duplicates()
    timest=data.pop('datetime')
    timest=pd.to_datetime(timest)
    #timest=timest.drop_duplicates()
    data=data.set_index(timest)
    #data=data.interpolate(freq='1H',method='time')
    #print(data.value_counts())
    #data=data.index.drop_duplicates()
    #data=data.date_range(data.first(),data.last(),'1H')
    data_min=data.resample('1min').mean()
    data_hour=data.resample('1H').mean()
    data_day=data.resample('1D').mean()
    data_week=data.resample('7D').mean()
    data_month=data.resample('1M').mean()

    fig = plt.figure(figsize=(36,12))
    ax1=fig.add_subplot(231)
    ax1.plot(np.array(data.index),np.array(data['value']))
    ax1.set_title("sec")
    ax2=fig.add_subplot(232)
    ax2.plot(np.array(data_min.index),np.array(data_min['value']))
    ax2.set_title("min")
    ax3=fig.add_subplot(233)
    ax3.plot(np.array(data_hour.index),np.array(data_hour['value']))
    ax3.set_title("hour")
    ax4=fig.add_subplot(234)
    ax4.plot(np.array(data_day.index),np.array(data_day['value']))
    ax4.set_title("day")
    ax5=fig.add_subplot(235)
    ax5.plot(np.array(data_week.index),np.array(data_week['value']))
    ax5.set_title("week")
    ax6=fig.add_subplot(236)
    ax6.plot(np.array(data_month.index),np.array(data_month['value']))
    ax6.set_title("month")
    print("close picture to the next step.")
    plt.show()
    return data
if __name__ == '__main__':
    my_path='D:/document/NCTU_sec1/Powermeter/' #input the path you put the data where named Powermeter in default.
    Path_dictionary=['Consumption-O','Current1','Current2','Power1','Power2','Volt1','Volt2','Default(Current2)']
    key=1
    type_key=7
    start_day=parse('20190930')
    end_day=parse('20191001')
    print(type(start_day))
    start_day,my_dt=read(start_day,end_day,2,my_path)
    while(key):
        try:
            key=int(input("exit input 0\nset day range input 1\nsee describe for data in between range input 2\ndraw picture input 3\ndraw detail picture input 4\nkey:"))
        except:
            key=1
            continue
        if(key==0):
            break
        elif(key==1):
            type_key=int(input("Current1 information input 1\nCurrent2 information input 2\nPower1 information input 3\nPower2 information input 4\nVolt1 information input 5\nVolt2 information input 6\nChoose data:"))
            if(type_key>7):
                continue
            start_day,end_day=start_end()
            start_day,my_dt=read(start_day,end_day,type_key,my_path)
        elif(key==2):
            try:
                print(my_dt.describe())
            except:
                print("input key =1 to set day range.")
        elif(key==3):
            try:
                my_dt.plot()
                print("Close picture to the next step.")
                plt.show()
            except:
                print("input key =1 to set day range.")
        elif(key==4):
            try:
                tmp=my_dt.copy()
                tmp=draw_six(tmp)
            except:
                print("input key =1 to set day range.")
        if(type_key==7):
            print("Now is "+str(datetime.datetime.date(start_day))+" to "+str(datetime.datetime.date(end_day))+" with "+str(Path_dictionary[type_key])+" data.\nPlease input key==1 to set your data range.")
        else:
            print("Now is "+str(datetime.datetime.date(start_day))+" to "+str(datetime.datetime.date(end_day))+" with "+str(Path_dictionary[type_key])+" data.")
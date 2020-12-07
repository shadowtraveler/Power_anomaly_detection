# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 13:00:10 2020

@author: steve
"""

import pandas as pd
import os

def draw_six(data,start_day='2018-09-25'):
    data['value']=data['value'].interpolate()
    data['datetime']=data['datetime'].drop_duplicates()
    timest=data.pop('datetime')
    timest=pd.to_datetime(timest)
    data=data.set_index(timest)
    #data_min=data.resample('1min',origin=start_day).mean()
    data_min=data.resample('1min',convention='start').mean()
    data_min['value']=data_min['value'].interpolate()
    return data_min


def read_and_save(my_path='D:/document/NCTU_sec1/Powermeter/20201024data/data/smartMeter/'):
    if(not os.path.isdir(my_path+"/output")):
        os.mkdir(my_path+"/output")
    try:
        Path_o=my_path
        Path_dictionary=['Consumption-O','Current1','Current2','Power1','Power2','Volt1','Volt2',]
        #Path_dictionary=['Consumption-O']
        dt=pd.DataFrame()
        for p_d in Path_dictionary:
            dt=pd.DataFrame()
            Path_tmp = Path_o+p_d
            My_List = os.listdir(Path_tmp)
            print("Loading...")
            for file in My_List:
                df=pd.read_csv(os.path.join(Path_tmp,file))
                dt=dt.append(df,ignore_index=True)
            dt=draw_six(dt)
            dt=dt.rename(columns={'value':'value_'+p_d})
            dt.to_csv('output/output_new_'+p_d+".csv")
            print(p_d+" finished.")
    except:
        raise ValueError("There is an error in read_and_save function\nPlease check your path.")

if __name__ == '__main__':
    #my_path='D:/document/NCTU_sec1/Powermeter/' #input the path you put the data where named Powermeter in default.
    #Path_dictionary=['Consumption-O','Current1','Current2','Power1','Power2','Volt1','Volt2','Default(Current2)']
    #my_dt=read_and_save(my_path)
    read_and_save()
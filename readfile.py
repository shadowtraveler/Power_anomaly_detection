# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 19:19:32 2020

@author: steve
"""

import pickle
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


def read_and_save(my_path='D:/document/NCTU_sec1/Powermeter/'):
    if(os.path.isfile('out.npy')):
        print("file out.npy existed.\nLoading...\n")
        out=np.load('./out.npy',allow_pickle=True)
        return out
    try:
        Path_o=my_path
        Path_dictionary=['Consumption-O','Current1','Current2','Power1','Power2','Volt1','Volt2',]
        num=0
        total=[]
        total_d=[]
        total_total=[]
        for p_d in Path_dictionary:
            Path_tmp = Path_o+p_d
            My_List = os.listdir(Path_tmp)
            if(num==0):
                for file in My_List:
                    df=pd.read_csv(os.path.join(Path_tmp,file))
                    tmp=[]
                    tmp.extend(df['value'])
                    total.append(tmp)
                    tmp_d=[]
                    tmp_d.extend(df['datetime'])
                    total_d.append(tmp_d)
                    num+=1
                    print(num)
                total_total.append(total_d)
                total_total.append(total)
            else:
                total=[]
                for file in My_List:
                    df=pd.read_csv(os.path.join(Path_tmp,file))
                    tmp=[]
                    tmp.extend(df['value'])
                    total.append(tmp)
                    num+=1
                    print(num)
                total_total.append(total)
                
        out=np.array(total_total)
        print(out[0][100][2])
        np.save('out.npy',out)
        return out
    except:
        raise ValueError("There is an error in read_and_save function\nPlease check your path.")

def draw(my_path='D:/document/NCTU_sec1/Powermeter/',filename='Current1/2018-09-27.csv'):
    try:
        Path_o=my_path
        df=pd.read_csv(os.path.join(Path_o,filename))
        df.plot(title=filename)
    except:
        raise ValueError("There is an error in draw function\nPlease check your filename or path.")
    
def s_max(start_date,end_date):
    #find max
    print("max")
    
"""
Path_o='D:/document/NCTU_sec1/Powermeter/Current1/'
df=pd.read_csv(os.path.join(Path_o,'2018-09-27.csv'))
tmp=[]
tmp.extend(df['value'])
print(type(tmp))
df.plot()
"""

if __name__ == '__main__':
    my_path='D:/document/NCTU_sec1/Powermeter/' #input the path you put the data where named Powermeter in default.
    filename='Current1/2018-09-27.csv'
    output=read_and_save(my_path)
    draw(my_path,filename)

# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 19:19:32 2020

@author: steve

#####################################################################################
#   Data Structure:                                                                 #
#   data:                                                                           #
#   L-1:                                                                            #
#       [0]:Consumption-O timestamp                                                 #
#       [1]:Consumption-O data                                                      #
#       [2]:Current1-timestamp                                                      #
#       [3]:Current1 data                                                           #
#       [4]:Current2-timestamp                                                      #
#       [5]:Current2 data                                                           #
#       [6]:Power1-timestamp                                                        #
#       [7]:Power1 data                                                             #
#       [8]:Power2-timestamp                                                        #
#       [9]:Power2 data                                                             #
#       [10]:Volt1-timestamp                                                        #
#       [11]:Volt1 data                                                             #
#       [12]:Volt2-timestamp                                                        #
#       [13]:Volt2 data                                                             #
#   L-2:                                                                            #
#       [][0:]:data for 20xx-xx-xx(one day)                                         #
#   L-3:                                                                            #
#       [(if odd) ][][0]:filename                                                   #
#       [(if even)][][0]:0                                                          #
#       [(if odd) ][][1:]:timestamp                                                 #
#       [(if even)][][1:]:Value                                                     #
#   Function:                                                                       #
#       start_day:      find data start_day and finish_day                          #
#       read_and_save:  read raw data and save as out.npy                           #
#       draw:           Test whether path and filename are correct.                 #
#       custom_max:     show data between range                                     #
#       my_max:         show data between range by years or months                  #
#       input_day:      input day range                                             #
#       my_darw:        draw six pictures for input range                           #
#       all_save:       save all data for days                                      #
#####################################################################################
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

def start_day(data):
    long=len(data[0])-1
    s_year=int(data[0][0][0][:4])
    s_month=int(data[0][0][0][5:7])
    s_day=int(data[0][0][0][8:10])
    start=[s_year,s_month,s_day]
    f_year=int(data[0][long][0][:4])
    f_month=int(data[0][long][0][5:7])
    f_day=int(data[0][long][0][8:10])
    finish=[f_year,f_month,f_day]
    return start,finish

def read_and_save(my_path='D:/document/NCTU_sec1/Powermeter/'):
    if(os.path.isfile('output.npy')):
        print("file output.npy existed.\nLoading...\n")
        out=np.load('./output.npy',allow_pickle=True)
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
            total=[]
            total_d=[]
            for file in My_List:
                df=pd.read_csv(os.path.join(Path_tmp,file))
                tmp=[0]                 #用來對齊
                tmp.extend(df['value'])
                total.append(tmp)
                tmp_d=[file]            #與這個對齊
                tmp_d.extend(df['datetime'])
                total_d.append(tmp_d)
                num+=1
                print(num)
            total_total.append(total_d)
            total_total.append(total)
        out=np.array(total_total)
        print(out[0][100][2])
        np.save('output.npy',out)
        return out
    except:
        raise ValueError("There is an error in read_and_save function\nPlease check your path.")

def draw(my_path='D:/document/NCTU_sec1/Powermeter/',filename='Current1/2018-09-27.csv'):
    try:
        Path_o=my_path
        df=pd.read_csv(os.path.join(Path_o,filename))
        df.plot(title=filename)
        print("File loaded.\nClose picture to start.")
        plt.show()
    except:
        raise ValueError("There is an error in draw function\nPlease check your filename or path.")

def custom_max(data,start_day,end_day,type_key):
    def check_range(start_day,end_day):
        key=0
        if(start_day[0]!=end_day[0]):
            key=1
        elif(start_day[1]!=end_day[1]):
            key=2
        elif(start_day[2]!=end_day[2]):
            key=3
        else:
            key=4
        return key
    #key=check_range(start_day,end_day)
    type_key_d=type_key-1
    ans=0
    num=0
    tmp=0
    sum_ans=0
    s_day=0
    e_day=0
    index=[0,0]
    stdev_arr=[]
    for i in range(len(data[type_key_d])):
        if(start_day[0]==int(data[type_key_d][i][0][:4]) and start_day[1]==int(data[type_key_d][i][0][5:7]) and start_day[2]==int(data[type_key_d][i][0][8:10])):
            s_day=i
        if(end_day[0]==int(data[type_key_d][i][0][:4]) and end_day[1]==int(data[type_key_d][i][0][5:7]) and end_day[2]==int(data[type_key_d][i][0][8:10])):
            e_day=i+1
            break
    my_draw(data,s_day,e_day,check_range(start_day,end_day),type_key)
    for i in range(s_day,e_day):
        if(len(data[type_key][i])!=1):
            num+=len(data[type_key][i])-1
            stdev_arr.extend(data[type_key][i][1:])
            sum_ans+=sum(data[type_key][i])
            tmp=max(data[type_key][i])
            if(ans<tmp):
                for x in range(len(data[type_key][i])):
                    if(tmp==data[type_key][i][x]):
                        tmp_index=x
                        break
                ans=tmp
                index=[i,tmp_index]
    print("Var:    \t"+str(np.var(stdev_arr)))
    print("Stdev:  \t"+str(np.std(stdev_arr)))
    print("Average:\t"+str(sum_ans/num))
    print("Count:  \t"+str(num))
    print("Max day: "+str(data[type_key_d][index[0]][index[1]]))
    print("The max from "+str(start_day[0])+"y "+str(start_day[1])+"m "+str(start_day[2])+"d to "+str(end_day[0])+"y "+str(end_day[1])+"m "+str(end_day[2])+"d "+" is "+str(ans))

def my_max(data,year=2018,month=1,key=0,type_key=3):
    if(key==0):
        ans=0
        num=0
        sum_ans=0
        flag=0
        s_day=0
        e_day=0
        type_key_d=type_key-1
        for i in range(len(data[type_key_d])) :
            if(year>int(data[type_key_d][i][0][:4])):
                continue
            elif(year<int(data[type_key_d][i][0][:4])):
                e_day=i
                break
            if(flag==0):
                s_day=i
                flag=1
            num+=len(data[type_key][i])-1
            if(data[type_key][i]!=[]):
                sum_ans+=sum(data[type_key][i])
                tmp=max(data[type_key][i])
                ans=max(tmp,ans)
            else:
                continue
        stdev_arr=[]
        for x in  range(s_day,e_day):
            if(len(data[type_key][x])!=1):
                stdev_arr.extend(data[type_key][x][1:])
        print("Var:    \t"+str(np.var(stdev_arr)))
        print("Stdev:  \t"+str(np.std(stdev_arr)))
        print("Average:\t"+str(sum_ans/num))
        print("Count:  \t"+str(num))
        print("The max in "+str(year)+" is "+str(ans))
    elif(key==1):
        ans=0
        num=0
        sum_ans=0
        s_day=0
        e_day=0
        type_key_d=type_key-1
        index=[0,0]
        flag=0
        for i in range(len(data[type_key_d])) :
            if(year>int(data[type_key_d][i][0][:4])):
                continue
            for j in range(i,len(data[type_key_d])):
                if(month!=int(data[type_key_d][j][0][5:7]) and flag==1):
                    e_day=j
                    break
                if(month>int(data[type_key_d][j][0][5:7])):
                    continue
                if(flag==0):
                    s_day=j
                    flag=1
                if(data[type_key][j]!=[]):
                    num+=len(data[type_key][j])-1
                    sum_ans+=sum(data[type_key][j])
                    tmp=max(data[type_key][j])
                    if(ans<tmp):
                        for x in range(len(data[type_key][j])):
                            if(tmp==data[type_key][j][x]):
                                tmp_index=x
                                break
                        ans=tmp
                        index=[j,tmp_index]#找到最大的index在哪
                else:
                    continue
            break
        stdev_arr=[]
        for x in  range(s_day,e_day):
            if(len(data[type_key][x])!=1):
                stdev_arr.extend(data[type_key][x][1:])
        print("Var     \t"+str(np.var(stdev_arr)))
        print("Stdev:  \t"+str(np.std(stdev_arr)))
        print("Average:\t"+str(sum_ans/num))
        print("Count:  \t"+str(num))
        print("Max day: "+str(data[type_key_d][index[0]][index[1]]))
        print("The max in "+str(year)+"y "+str(month)+"m is "+str(ans))
    #print("max")

def input_day(start_day,finish_day,key):
    def check_day(year,month,day):
        m_d={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        if(month>12):
            return False
        elif(month==2):
            if(year%4==0 and day==29):
                return True
        else:
            if(day>m_d[month] or day<1):
                return False
        return True
    
    def error_msg(error_key=0):
        if(error_key):
            print("Something is wrong for input month and day.")
        else:
            print("Error!!The data is out of range!\nRange is from")
            print(str(start_day[0])+"y "+str(start_day[1])+"m "+str(start_day[2])+"d")
            print("to\n"+str(finish_day[0])+"y "+str(finish_day[1])+"m "+str(finish_day[2])+"d")
    while(1):
        if(key==0):
            print("input your start day:")
        elif(key==1):
            print("input your finish day:")
        year=int(input("year:"))
        if(year==0):
            return [0,0,0]
        month=int(input("month:"))
        day=int(input("day:"))
        if(year<start_day[0] or (year==start_day[0] and month<start_day[1]) or (year==start_day[0] and month==start_day[1] and day<start_day[2])):
            error_msg()
        elif(year>finish_day[0] or (year==finish_day[0] and month>finish_day[1]) or (year==finish_day[0] and month==finish_day[1] and day>finish_day[2])):
            error_msg()
        else:
            if(check_day(year,month,day)):
                return [year,month,day]
            else:
                error_msg(error_key=1)

def my_draw(data,start_day,end_day,key,type_key):
    type_key_d=type_key-1
    sum_ans=0
    num=0
    month_data=[]   
    month_data_time=[]
    week_data=[]    
    week_data_time=[]
    day_data=[]     
    hour_data=[]    
    min_data=[]     
    sec_data=[]     
    month_flag=[-1,0]    #1
    week_flag=[-1,0]     #2
    hour_flag=[-1,0]     #3
    min_flag=[-1,0]      #4
    for i in range(start_day,end_day):
        
        #month cal
        if(month_flag[0]==-1):
            month_flag[0]=int(data[type_key_d][i][0][5:7])
            month_flag[1]=i
        elif(month_flag[0]!=int(data[type_key_d][i][0][5:7])):
            sum_ans=0
            num=0
            for j in range(month_flag[1],i):
                sum_ans+=sum(data[type_key][j])
                num+=len(data[type_key][j])-1
            if(num==0):
                month_data.extend([0])
                month_data_time.extend([data[type_key_d][month_flag[1]][0][:7]])
            else:
                month_data.extend([sum_ans/num])
                month_data_time.extend([data[type_key_d][month_flag[1]][0][:7]])
            month_flag[0]=int(data[type_key_d][i][0][5:7])
            month_flag[1]=i
        
        #week cal
        if(week_flag[0]==-1):
            week_flag[0]=1
            week_flag[1]=i
        elif(week_flag[0]<7):
            week_flag[0]+=1
        else:
            sum_ans=0
            num=0
            for j in range(week_flag[1],i):
                sum_ans+=sum(data[type_key][j])
                num+=len(data[type_key][j])-1
            if(num==0):
                week_data.extend([0])
                week_data_time.extend([data[type_key_d][week_flag[1]][0][:10]])
            else:
                week_data.extend([sum_ans/num])
                week_data_time.extend([data[type_key_d][week_flag[1]][0][:10]])
            week_flag[0]=1
            week_flag[1]=i
        if(len(data[type_key][i])!=1):
            sec_data.extend(data[type_key][i][1:])
            day_data.extend([sum(data[type_key][i])/(len(data[type_key][i])-1)])
            
            for k in range(1,len(data[type_key][i])):
                tmp=data[type_key_d][i][k].split()
                if(hour_flag[0]==-1):
                    hour_flag[0]=int(tmp[1][:2])
                    hour_flag[1]=k
                elif(hour_flag[0]!=int(tmp[1][:2])):
                    sum_ans=0
                    num=k-hour_flag[1]
                    for j in range(hour_flag[1],k):
                        sum_ans+=data[type_key][i][j]
                    if(num==0):
                        hour_data.extend([0])
                    else:
                        hour_data.extend([sum_ans/num])
                    hour_flag[0]=int(tmp[1][:2])
                    hour_flag[1]=k
                    
                    
                if(min_flag[0]==-1):
                    min_flag[0]=int(tmp[1][3:5])
                    min_flag[1]=k
                elif(min_flag[0]!=int(tmp[1][3:5])):
                    sum_ans=0
                    num=k-min_flag[1]
                    for j in range(min_flag[1],k):
                        sum_ans+=data[type_key][i][j]
                    if(num==0):
                        min_data.extend([0])
                    else:
                        min_data.extend([sum_ans/num])
                    min_flag[0]=int(tmp[1][3:5])
                    min_flag[1]=k
                    
                    
            #hour cal
            num=len(data[type_key][i])-hour_flag[1]
            for j in range(hour_flag[1],len(data[type_key][i])):
                sum_ans+=data[type_key][i][j]
            if(num==0):
                hour_data.extend([0])
            else:
                hour_data.extend([sum_ans/num])    
            
            
            #min cal
            num=len(data[type_key][i])-min_flag[1]
            for j in range(min_flag[1],len(data[type_key][i])):
                sum_ans+=data[type_key][i][j]
            if(num==0):
                min_data.extend([0])
            else:
                min_data.extend([sum_ans/num])    
    #month cal
    for j in range(month_flag[1],end_day):
        sum_ans+=sum(data[type_key][j])
        num+=len(data[type_key][j])-1
    if(num==0):
        month_data.extend([0])
        month_data_time.extend([data[type_key_d][month_flag[1]][0][:7]])
    else:
        month_data.extend([sum_ans/num])
        month_data_time.extend([data[type_key_d][month_flag[1]][0][:7]])
    
    #week cal
    for j in range(week_flag[1],end_day):
        sum_ans+=sum(data[type_key][j])
        num+=len(data[type_key][j])-1
    if(num==0):
        week_data.extend([0])
        week_data_time.extend([data[type_key_d][week_flag[1]][0][:10]])
    else:
        week_data.extend([sum_ans/num])
        week_data_time.extend([data[type_key_d][week_flag[1]][0][:10]])
        
    #繪圖
    fig = plt.figure(figsize=(36,12))
    ax1=fig.add_subplot(231)
    ax2=fig.add_subplot(232)
    ax3=fig.add_subplot(233)
    ax4=fig.add_subplot(234)
    ax5=fig.add_subplot(235)
    ax6=fig.add_subplot(236)
    fig.subplots_adjust(top=0.85)
    fig.suptitle('test', color='red', fontsize=20)
    ax1.plot(np.array(sec_data))
    ax1.set_title("sec")
    ax2.plot(np.array(min_data))
    ax2.set_title("min")
    ax3.plot(np.array(hour_data))
    ax3.set_title("hour")    
    ax4.plot(np.array(day_data))
    ax4.set_title("day")
    if(len(week_data_time)<10):
        ax5.plot(np.array(week_data_time),np.array(week_data))
    else:
        ax5.plot(np.array(week_data))
    ax5.set_title("week")
    ax6.plot(np.array(month_data_time),np.array(month_data))
    ax6.set_title("month")
    print("Close Picture to the next step")
    plt.show()

def all_save(data,my_path,type_key,key=0):
    if(os.path.isdir(my_path+"/output")):
        print("Now Loading...")
    else:
        os.mkdir(my_path+"/output")
        print("Now Loading...")
    Path_dictionary=['Consumption-O','Current1','Current2','Power1','Power2','Volt1','Volt2',]
    tmp_Time=[]
    tmp_Var=[]
    tmp_Std=[]
    tmp_Aver=[]
    tmp_Count=[]
    tmp_Max=[]
    tmp_Max_day=[]
    i=type_key
    for j in range(len(data[i])):
        if(len(data[i][j])==1):
            tmp_Time.extend([str(data[i-1][j][0][:10])])
            tmp_Var.extend([0])
            tmp_Std.extend([0])
            tmp_Aver.extend([0])
            tmp_Count.extend([0])
            tmp_Max.extend([0])
            tmp_Max_day.extend([" "])
        else:
            if(j%100==0):
                print("Now:"+str(j)+"/"+str(len(data[i])))
            tmp_Time.extend([str(data[i-1][j][0][:10])])
            tmp_Var.extend([np.var(data[i][j])])
            tmp_Std.extend([np.std(data[i][j])])
            tmp_Aver.extend([np.sum(data[i][j])/(len(data[i][j])-1)])
            tmp_Count.extend([len(data[i][j])-1])
            tmp_Max.extend([max(data[i][j])])
            for k in range(len(data[i][j])):
                if(max(data[i][j])==data[i][j][k]):
                    tmp_Max_day.extend([str(data[i-1][j][k])])
                    break
                
    data_output=pd.DataFrame({'Day':tmp_Time,'Var':tmp_Var,'Std':tmp_Std,'Aver':tmp_Aver,'Max':tmp_Max,'Max_day':tmp_Max_day})
    data_output.to_csv(my_path+"output/"+Path_dictionary[int((i-1)/2)]+".csv",index=False,sep=",")


if __name__ == '__main__':
    my_path='D:/document/NCTU_sec1/Powermeter/' #input the path you put the data where named Powermeter in default.
    filename='Current1/2018-09-26.csv'
    data=read_and_save(my_path)
    start_day,finish_day=start_day(data)
    my_start_day=[0,0,0]
    my_finish_day=[0,0,0]
    draw(my_path,filename)
    key=1
    while(key):
        key=input("input 0 to exit\ninput 1 to show data status\ninput 2 to set range\ninput 3 to save all data\nEnter:")
        if(key==""):
            key=1
            continue
        key=int(key)
        if(key==0):
            print("bye~")
            break
        elif(key==1):
            type_key=2*int(input("Current1 information input 1\nCurrent2 information input 2\nPower1 information input 3\nPower2 information input 4\nVolt1 information input 5\nVolt2 information input 6\nChoose data:"))+1
            if(type_key>13):
                continue
            year=int(input("year:"))
            month=int(input("(if you want to see year data,input 0)\nmonth:"))
            if(month==0):
                my_max(data,year,month,0,type_key)
            else:
                my_max(data,year,month,1,type_key)
        elif(key==2):
            type_key=2*int(input("Current1 information input 1\nCurrent2 information input 2\nPower1 information input 3\nPower2 information input 4\nVolt1 information input 5\nVolt2 information input 6\nChoose data:"))+1
            if(type_key>13 ):
                continue
            my_start_day=input_day(start_day,finish_day,0)
            if(my_start_day[0]==0):
                continue
            my_finish_day=input_day(start_day,finish_day,1)
            if(my_finish_day[0]==0):
                continue
            custom_max(data,my_start_day,my_finish_day,type_key)
        elif(key==3):
            type_key=2*int(input("Current1 information input 1\nCurrent2 information input 2\nPower1 information input 3\nPower2 information input 4\nVolt1 information input 5\nVolt2 information input 6\nChoose data:"))+1
            if(type_key>13 ):
                continue
            all_save(data,my_path,type_key)
            print("file saved.")
        input("Press Enter...")
        

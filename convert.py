#!/bin/python

import fnmatch
import sys
import os
import argparse
from pprint import pprint, pformat
from collections import OrderedDict

import numpy as np
import pandas as pd

#Possible bugs: no such file is a relative file

#預言家: -p, prophet
#女巫: -w, witch
#獵人: -h, hunter
#白神: -i, idiot
#狼王: -wk, king of wolves
#守衛: -g, guard

def file_extension_error():
    print("Error:")
    print("Your file extension is not \'.csv\' .")
    print("It should be \'.csv\'.")

def no_such_file_error(file):
    print("Error:")
    print("%s does not exist"%file)

def name_revision(df,i):
    #bool protection = True
    name = input("編號%s號的人名字為:"%str(i+1))
    df["Name"][i] = name
    return df

def PWHI():#預女獵白
    voting_status = np.array([-1,-1,-1,-1,-1,-1, -1])     #0 for 該輪平票PK, 1 for 有進行到該輪 [警長, 第一輪, ......]
    data_play = []
    wolf_camp = []
    good_camp = []
    witch = 0
    prophet = 0
    hunter = 0
    idiot = 0
    print("版子為：預女獵白")
    print("配置為：")
    print("$好人：預言家、女巫、獵人、白痴神")
    print("$狼人：四隻小狼")
    print("請依照座位號碼輸入其編號和其身分:")
    print("身份輸入請輸入相對應的數字:\'狼人\':1, \'預言家\':2, \'女巫\':3, \'獵人\':4, \'白痴神\':5, \'平民\':6")
    for i in range(12):
        temp_no = input("坐%s號位的玩家編號為:"%str(i+1))
        temp_id = input("%s號位的玩家身份為:"%str(i+1))
        temp_id = int(temp_id)
        temp_identification = None
        if temp_id == 1:
            temp_identification = "狼人"
            wolf_camp.append(i+1)
        elif temp_id == 2:
            temp_identification = "預言家"
            good_camp.append(i+1)
            prophet = i+1
        elif temp_id == 3:
            temp_identification = "女巫"
            good_camp.append(i+1)
            witch = i+1
        elif temp_id == 4:
            temp_identification = "獵人"
            good_camp.append(i+1)
            hunter = i+1
        elif temp_id == 5:
            temp_identification = "白痴神"
            good_camp.append(i+1)
            witch = i+1
        elif temp_id == 6:
            temp_identification = "平民"
            good_camp.append(i+1)
        else:
            print("Unknown Commands!")
            sys.exit()
        data_play.append({'Seat':i+1, 'No':temp_no, 'Identification': temp_identification, 'Identifiaction(id in number)': temp_id,
                          "警長投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "First Round Vote (0 for 棄票, -1 for 無法投票)": -1,
                          "Second Round Vote (0 for 棄票, -1 for 無法投票)": -1,
                          "Third Round Vote (0 for 棄票, -1 for 無法投票)": -1,
                          "Fourth Round Vote (0 for 棄票, -1 for 無法投票)": -1,
                          "Fixth Round Vote (0 for 棄票, -1 for 無法投票)": -1,
                          "Sixth Round Vote (0 for 棄票, -1 for 無法投票)": -1,
                          "警長PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第一輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第二輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第三輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第四輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第五輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第六輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "特殊功能加分": 0})
    df_play = pd.DataFrame(data_play, columns=['Seat', 'No', 'Identification', 'Identifiaction(id in number)',
                                               '警長投票 (0 for 棄票, -1 for 無法投票)',
                                               'First Round Vote (0 for 棄票, -1 for 無法投票)',
                                               'Second Round Vote (0 for 棄票, -1 for 無法投票)',
                                               'Third Round Vote (0 for 棄票, -1 for 無法投票)',
                                               'Fourth Round Vote (0 for 棄票, -1 for 無法投票)',
                                               'Fixth Round Vote (0 for 棄票, -1 for 無法投票)',
                                               "Sixth Round Vote (0 for 棄票, -1 for 無法投票)",
                                               "警長PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第一輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第二輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第三輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第四輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第五輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第六輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "特殊功能加分"])
    print("這場身份如下：")
    print(df_play[['Seat', 'No', 'Identification']])

    print("狼人陣營:",wolf_camp)
    print("好人陣營:",good_camp)

    already_death = []
    wolf_action = -1  #Kill whom  Not killing: 0
    witch_action = -1 #Status: -1, can save and poison; -2, can only poison, -3, can only save; -5: nothing
    gun_action = -1   #Cannot kill:0, kill:Seat Number
    prophet_action = "None"
    print("-------------------------------")
    print("第一晚:")
    wolf_temp = input("請輸入狼人擊殺對象 (0:空刀):")
    witch_temp = input("請輸入女巫是否發動技能（-1:空, 0:救人, 座位號碼:毒人):")
    prophet_temp = input("請輸入預言家查驗對象:")
    for wolf in wolf_camp:
        if wolf == int(prophet_temp):
            prophet_action = "狼人"
            break
    if prophet_action == -1:
        prophet_action = "好人"

    print("預言家查驗的玩家%s為好人"%prophet_temp)
    #Witch
    if (int(witch_temp)==0 and (witch_action==-1 or witch_action==-3)):
        if witch_action==-1:
            witch_action = -2
        else:
            witch_action = -5
    elif (int(witch_temp)>0 and (witch_action==-1 or witch_action==-2)):
        if witch_action==-1:
            witch_action = -3
        else:
            witch_action = -5
    else:
        witch_temp = -1
    witch_temp = int(witch_temp)


    #女巫毒狼有加分
    if int(witch_temp) > 0:
        a = 0
        for wolf in wolf_camp:
            if wolf == int(witch_temp):
                df_play["特殊功能加分"][witch-1] += 0.5
                a = 1
                break
        if a==0:
            df_play["特殊功能加分"][witch-1] -= 0.5


    print("---------------------------------")
    print("警長競選環節")


    if witch_temp == 0:
        print("平安夜!")
    elif int(wolf_temp)==0 and witch_temp==-1:
        print("平安夜")
    elif int(wolf_temp)==0 and witch_temp>0:
        print("今晚%s倒牌"%str(witch_temp))
    elif witch_temp==-1:
        print("今晚%s倒牌"%str(wolf_temp))
    else:
        print("今晚倒牌的玩家有兩名", wolf_temp, str(witch_temp))






def main():
    """
    __main__
    """

    parser = argparse.ArgumentParser(description="請依照您想要的功能輸入相對應的\'flag\'")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p1', '--pwhi', dest='pwhi', default=False, help='預女獵白')
    group.add_argument('-p2', '--wkg', dest='wkg', default=False, help='狼王守衛')
    group.add_argument('-c', '--create', default=False, help='創造一個新的資料檔', dest="create")
    args = parser.parse_args()

    file_base = None
    data = None
    if args.pwhi:
        file_base = str(args.pwhi)
        if file_base[-3:] != "csv":
            file_extension_error()
            return
        if not os.path.isfile("%s"%file_base):
            no_such_file_error(file_base)
            return
        print("進行的版子為:預女獵白")
        print("使用:%s作為記錄的檔案。"%file_base)
        PWHI()
        data = pd.read_csv(file_base)
    elif args.wkg:
        file_base = str(args.wkg)
        if file_base[-3:] != "csv":
            file_extension_error(file_base)
            return
        if not os.path.isfile("%s"%file_base):
            no_such_file_error()
            return
        print("進行的版子為:狼王守衛")
        print("使用:%s作為記錄的檔案。"%file_base)
        data = pd.read_csv(file_base)
    elif args.create:
        file, num = args.create.split(':')
        num = int(num)
        file_base = str(file)

        #Protection of file_existence
        if os.path.isfile("%s"%file_base):
            print("%s原本就存在喔！將覆寫該檔案!"%file_base)
            temp = input("是否同意覆寫?[y/n]")
            if temp[0] == 'y' or temp[0]=='Y':
                print("將覆寫該檔案！")
            elif temp[0] != 'n' and temp[0]!='N':
                print("非\'y\'亦非\'n\'，將假設您不同意覆寫！")
                return
            else:
                print("不同意覆寫!")
                return
        ############################

        if file_base[-3:] != "csv":
            file_extension_error()
            return
        print("創造", file_base)
        data = []
        for i in range(num):
            data.append({'No': i+1, 'Name': '', 'Score': 0, 'Win': 0, 'Lose':0, 'Remark':''})
        df = pd.DataFrame(data, columns=['No', 'Name', 'Score', 'Win', 'Lose', 'Remark'])
        temp = input("您想要現在直接輸入每個人的名字嗎?[y/n]")
        if temp[0] == 'y' or temp[0]=='Y':
            for i in range(num):
                df = name_revision(df, i)
        elif temp[0] != 'n' and temp[0]!='N':
            print("非\'y\'亦非\'n\'，將直接假設您不需要！")

        df.to_csv(file_base, index=False)
        print("成功創造檔案%s"%file_base)




if __name__ == "__main__":
    sys.exit(main())


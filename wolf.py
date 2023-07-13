#!/bin/python

import fnmatch
import sys
import os
import argparse
from pprint import pprint, pformat
from collections import OrderedDict

import numpy as np
import pandas as pd

from board import pwhi, wkg
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




def main():
    """
    __main__
    """

    parser = argparse.ArgumentParser(description="請依照您想要的功能輸入相對應的\'flag\'")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p1', '--pwhi', dest='pwhi', default=False, help='預女獵白')
    group.add_argument('-p2', '--wkg', dest='wkg', default=False, help='狼王守衛')
    group.add_argument('-p3', '--ng', dest='ng', default=False, help='夢魘守衛')
    group.add_argument('-p4', '--bhe', dest='bhe', default=False, help='血月獵魔')
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
        scores = pwhi.main()
        data = pd.read_csv(file_base)
        for i in range(12):
            data['Score'][scores[i,0]-1] += scores[i,1]
            data['Win'][scores[i,0]-1] += scores[i,2]
            data['Lose'][scores[i,0]-1] += scores[i,3]

        data.to_csv(file_base, index=False)

    elif args.wkg:
        file_base = str(args.wkg)
        if file_base[-3:] != "csv":
            file_extension_error()
            return
        if not os.path.isfile("%s"%file_base):
            no_such_file_error(file_base)
            return
        print("進行的版子為:狼槍守衛")
        print("使用:%s作為記錄的檔案。"%file_base)
        scores = wkg.main()
        data = pd.read_csv(file_base)
        for i in range(12):
            data['Score'][scores[i,0]-1] += scores[i,1]
            data['Win'][scores[i,0]-1] += scores[i,2]
            data['Lose'][scores[i,0]-1] += scores[i,3]

        data.to_csv(file_base, index=False)
    elif args.ng:
        print("進行的版子為:夢魘守衛")
        print("Sorry~夢魘守衛還不能玩喔~~~")
        return
        file_base = str(args.ng)
        if file_base[-3:] != "csv":
            file_extension_error()
            return
        print("進行的版子為:夢魘守衛")
        print("使用:%s作為記錄的檔案。"%file_base)
    elif args.bhe:
        print("進行的版子為:血月獵魔")
        print("Sorry~血月獵魔還不能玩喔~~~")
        return
        file_base = str(args.bhe)
        if file_base[-3:] != "csv":
            file_extension_error()
            return
        print("進行的版子為:血月獵魔")
        print("使用:%s作為記錄的檔案。"%file_base)
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


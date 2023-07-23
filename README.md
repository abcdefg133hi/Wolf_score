## Instruction
狼人殺是一款大小朋友都可以同樂的桌遊，邏輯的碰撞以及情感直覺的堆疊造就了一群熱愛狼人殺的玩家，你也是其中之一嗎？如果是的話，可以試試看此套件，此套件程式可以用以長期紀錄各玩家的長期狼人殺競賽得分，利用場上做對事的成效、勝敗方、以及MVP票選來創造一個公平公正的計分模式，可用於狼人殺競賽上，亦可以用於日常紀錄。

## Shell Commands to activate the code:

```
git clone https://github.com/abcdefg133hi/Wolf_score.git
cd Wolf_score
python3 ./wolf.py -h
```

## The commands
```
python3 ./wolf.py -c  [YourFile.csv:Num of People]   #For creating the recording file.
python3 ./wolf.py -p1 [YourFile.csv]                 #For playing 預女獵白.
python3 ./wolf.py -p2 [YourFile.csv]                 #For playing 狼王守衛.
python3 ./wolf.py -p3 [YourFile.csv]                 #For playing 夢魘守衛.
python3 ./wolf.py -p4 [YourFile.csv]                 #For playing 血月獵魔.
```

## Quick Start
### 預女獵白
```
git clone https://github.com/abcdefg133hi/Wolf_score.git
cd Wolf_score
python3 ./wolf.py -c record.csv:12
python3 ./wolf.py -p1 record.csv
open record.csv
```
### 狼王守衛
```
git clone https://github.com/abcdefg133hi/Wolf_score.git
cd Wolf_score
python3 ./wolf.py -c record.csv:12
python3 ./wolf.py -p2 record.csv
```
Notice: Make sure that your computer contains "numpy" and "pandas" or you should first install them by
```
pip install numpy
pip install pandas
```
Or if you use "conda"
```
conda install numpy
conda install pandas
```


## Notice
- It is under developed.
- In current status, only 預女獵白, 狼王守衛 will work.

## Rules for Scoring
### 預女獵白
- 獲勝方基礎分: 3 分
- 失敗方基礎分: -3 分
- 女巫毒狼人: +0.5 分
- 女巫毒好人: -0.5 分
- 獵人開槍帶走狼人: +0.5 分
- 獵人開槍帶走好人: -0.5 分
- 放逐公投時,好人投票投狼: +0.5 分
- 放逐公投時,好人投票投好人: -0.5 分
- 好人MVP票選第一名: +5分
- 好人MVP票選第二名: +3分
- 狼人MVP票選第一名: +5分
### 狼王守衛
- 獲勝方基礎分: 3 分
- 失敗方基礎分: -3 分
- 女巫毒狼人: +0.5 分
- 女巫毒好人: -0.5 分
- 獵人開槍帶走狼人: +0.5 分
- 獵人開槍帶走好人: -0.5 分
- 狼王開槍帶走非女巫或守衛（含狼同伴）: +0.5 分
- 狼王開槍帶走女巫（非第一天自刀）: +1 分
- 狼王開槍帶走守衛（非第一天自刀）: +2 分
- 狼王於第一天自刀帶走守衛或女巫: +0.5 分 
- 放逐公投時,好人投票投狼: +0.5 分
- 放逐公投時,好人投票投好人: -0.5 分
- 好人MVP票選第一名: +5分
- 好人MVP票選第二名: +3分
- 狼人MVP票選第一名: +5分
### More rules are still under developed and will be announced soon ~~~ (Have Fun ^-^)




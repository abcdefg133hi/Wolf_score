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
- In current status, recording for 狼王守衛 is not completed.

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
### 狼王守衛
- 獲勝方基礎分: 3 分
- 失敗方基礎分: -3 分
- 女巫毒狼人: +0.5 分
- 女巫毒好人: -0.5 分
- 放逐公投時,好人投票投狼: +0.5 分
- 放逐公投時,好人投票投好人: -0.5 分
### More rules are still under developed and will be announced soon ~~~ (Have Fun ^-^)




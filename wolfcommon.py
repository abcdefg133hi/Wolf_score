import numpy as np
import pandas as pd

def order_initialize(array):
    n = len(array)
    for i in range(n):
        array[i] = i+1
    return array


def daily(player_survive, wolf_camp, hunter, sergeant):
    death = np.array([])
    tickets = np.zeros(12)      #Initialize
    vote_array = np.zeros((2,12))-1.  #(vote, pk vote), 0:棄票, -1:不能投票
    hunter_status = 0           #獵人是否帶到狼, 0:無開槍, -1:無, 1:有
    no_one_dead_today = False

    print("發言完畢時請按Enter以繼續")
    input()
    temp = input("發言完畢警長歸票:(若多名成員PK請用空格分開, 若不歸請輸入0)")
    temp = [int(player) for player in temp.split()]
    if len(temp) > 1:
        print("警長票降為1票!")
        temp = 1
    else:
        print("警歸%s!"%str(temp[0]))
        temp = 1.5


    voter = np.copy(player_survive)
    for player in voter:
        vote = input("%s號玩家投的是:（棄票請打0）"%str(int(player)))
        vote = int(vote)
        if vote not in player_survive:
            vote = 0       #亂投票=棄票
        vote_array[0][int(player-1)] = vote
        if vote == 0:
            continue
        if player == sergeant:
            tickets[vote-1] += temp
        else:
            tickets[vote-1]+=1
    #print("投票結果如下：")
    #print(df_play[['Seat', 'No', 'First Round Vote (0 for 棄票, -1 for 無法投票)']])
    max_tickets = np.max(tickets)
    max_candidate = np.where(tickets == max_tickets)[0]+1
    if len(max_candidate) > 1:
        tickets = np.zeros(12)      #Initialize
        all_players = np.copy(player_survive)
        voter = np.setdiff1d(all_players,max_candidate)
        print("因為超過一人得最高票，進行PK的為:", max_candidate)
        print("發言完畢時請按Enter以繼續")
        input()
        for player in voter:
            vote = input("%s號玩家投的是:（棄票請打0）"%str(int(player)))
            vote = int(vote)
            if vote not in max_candidate:
                vote = 0       #亂投票=棄票
            vote_array[1][int(player-1)] = vote
            if vote == 0:
                continue
            tickets[vote-1] += 1
        max_tickets = np.max(tickets)
        max_candidate = tickets[tickets==max_tickets]
        #print("投票結果如下：")
        #print(df_play[['Seat', 'No', '第一輪PK投票 (0 for 棄票, -1 for 無法投票)']])
        if len(max_candidate) > 1:
            print("平票，平安日!")
            no_one_dead_today = True

    if not no_one_dead_today:
        death = np.append(death, tickets.argmax()+1)
        print("%s玩家出局，請留遺言!"%str(tickets.argmax()+1))
        if(tickets.argmax()+1==hunter):
            hunt = input("公投出局的玩家是否要開槍:(0 for 不開槍)")
            if hunt!=0:
                death = np.append(death, hunt)
                if hunt in wolf_camp:
                    hunter_status = 1
                else:
                    hunter_status = -1
                print("%s玩家出局，請留遺言!"%hunt)

        death = death.astype('float')
        death = death.astype('int')
        player_survive = np.setdiff1d(player_survive, death)

    if sergeant in death:
        temp = input("%s移交警徽給(撕掉請輸入0):"%str(sergeant))
        sergeant = int(temp)

    return player_survive, vote_array, hunter_status, sergeant

def if_end(player_survive, wolf_camp, god_camp, villager_camp,sergeant):
    winner = -1
    good_camp_survive = np.setdiff1d(player_survive, wolf_camp)
    god_camp_survive = np.setdiff1d(good_camp_survive, villager_camp)
    villager_camp_survive = np.setdiff1d(good_camp_survive, god_camp)
    num_of_survive = len(player_survive)
    num_of_good_survive = len(good_camp_survive)
    num_of_wolf_survive = len(player_survive) - num_of_good_survive
    num_of_god_survive = len(god_camp_survive)
    num_of_villager_survive = len(villager_camp_survive)

    if num_of_good_survive <= num_of_wolf_survive:
        print("狼人綁票!")
        winner = 1
        return False, winner

    god_camp_survive = np.setdiff1d(player_survive, wolf_camp)
    if num_of_god_survive == 0 or num_of_villager_survive == 0:
        print("狼隊獲勝!")
        winner = 1
        return False, winner

    if num_of_wolf_survive == 0:
        print("好人獲勝!")
        winner = 0
        return False, winner

    print("遊戲繼續,天黑請閉眼!")
    return True, winner



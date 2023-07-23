import numpy as np
import pandas as pd

def order_initialize(array):
    n = len(array)
    for i in range(n):
        array[i] = i+1
    return array

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

    print("遊戲繼續!")
    return True, winner


def night(player_survive, wolf_camp, god_camp, villager_camp, witch_action, witch, prophet, hunter, sergeant):
    wolf_temp = input("請輸入狼人擊殺對象 (0:空刀):")
    witch_temp = input("請輸入女巫是否發動技能（-1:空, 0:救人, 座位號碼:毒人):")
    prophet_temp = input("請輸入預言家查驗對象:")
    prophet_action = -1  #-1:好人, 0:狼人
    death = np.array([])
    witch_status = 0
    hunter_status = 0
    if prophet not in player_survive:
        pass
    else:
        for wolf in wolf_camp:
            if wolf == int(prophet_temp):
                prophet_action = 0
                print("預言家查驗的玩家%s為狼人"%prophet_temp)
                break
        if prophet_action == -1:
            prophet_action = "好人"
            print("預言家查驗的玩家%s為好人"%prophet_temp)

    #Witch
    if witch not in player_survive:
        #witch_action = -5
        witch_temp = -1
        pass
    elif (int(witch_temp)==0 and (witch_action==-1 or witch_action==-3)):
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
                witch_status += 0.5
                a = 1
                break
        if a==0:
            witch_status -= 0.5


    if witch_temp == 0:
        print("昨晚為平安夜!")
    elif int(wolf_temp)==0 and witch_temp==-1:
        print("昨晚為平安夜!")
    elif int(wolf_temp)==0 and witch_temp>0:
        print("昨晚%s倒牌"%str(witch_temp))
        death = np.append(death, witch_temp)
    elif witch_temp==-1:
        print("昨晚%s倒牌"%str(wolf_temp))
        death = np.append(death, int(wolf_temp))
        if int(wolf_temp)==hunter:
            player_survive = np.setdiff1d(player_survive, death)
            game_status, winner = if_end(player_survive, wolf_camp, god_camp, villager_camp, sergeant)
            if(game_status):
                hunt = input("公投出局的玩家是否要開槍:(0 for 不開槍)")
                if hunt!=0:
                    death = np.append(death, hunt)
                    if hunt in wolf_camp:
                        hunter_status = 0.5
                    else:
                        hunter_status = -0.5
                print("%s玩家出局，請留遺言!"%hunt)
    elif witch_temp==int(wolf_temp):
        print("昨晚%s倒牌"%str(wolf_temp))
        death = np.append(death, int(wolf_temp))
    else:
        print("昨晚倒牌的玩家有兩名", wolf_temp, str(witch_temp))
        death = np.append(death, int(wolf_temp))
        death = np.append(death, witch_temp)
        if int(wolf_temp)==hunter:
            player_survive = np.setdiff1d(player_survive, death)
            game_status, winner = if_end(player_survive, wolf_camp, god_camp, villager_camp, sergeant)
            if(game_status):
                hunt = input("公投出局的玩家是否要開槍:(0 for 不開槍)")
                if hunt!=0:
                    death = np.append(death, hunt)
                    if hunt in wolf_camp:
                        hunter_status = 0.5
                    else:
                        hunter_status = -0.5
                print("%s玩家出局，請留遺言!"%hunt)

    death = death.astype('float')
    death = death.astype('int')
    player_survive = np.setdiff1d(player_survive, death)
    if sergeant in death:
        temp = input("%s移交警徽給(撕掉請輸入0):"%str(sergeant))
        sergeant = int(temp)

    return player_survive, witch_action, witch_status, hunter_status, sergeant

def daily(player_survive, wolf_camp, god_camp, villager_camp, hunter, sergeant):
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
            player_survive = np.setdiff1d(player_survive, death)
            game_status, winner = if_end(player_survive, wolf_camp, god_camp, villager_camp, sergeant)
            if(game_status):
                hunt = input("公投出局的玩家是否要開槍:(0 for 不開槍)")
                if hunt!=0:
                    death = np.append(death, hunt)
                    if hunt in wolf_camp:
                        hunter_status = 0.5
                    else:
                        hunter_status = -0.5
                print("%s玩家出局，請留遺言!"%hunt)

        death = death.astype('float')
        death = death.astype('int')
        player_survive = np.setdiff1d(player_survive, death)

    if sergeant in death:
        temp = input("%s移交警徽給(撕掉請輸入0):"%str(sergeant))
        sergeant = int(temp)

    return player_survive, vote_array, hunter_status, sergeant

def main():#
    pd.set_option('mode.chained_assignment', None)
    voting_status = np.array([-1,-1,-1,-1,-1,-1, -1])     #0 for 該輪平票PK, 1 for 有進行到該輪 [警長, 第一輪, ......]
    data_play = []
    wolf_camp = []
    villager_camp = []
    god_camp = []
    witch = 0
    prophet = 0
    hunter = 0
    idiot = 0
    sergeant = 0  #警長
    tickets = np.zeros(12)
    player_survive = order_initialize(np.zeros(12))
    game_status = True
    game_day = 0
    winner = -1   #wolf:1, good:0
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
            god_camp.append(i+1)
            prophet = i+1
        elif temp_id == 3:
            temp_identification = "女巫"
            god_camp.append(i+1)
            witch = i+1
        elif temp_id == 4:
            temp_identification = "獵人"
            god_camp.append(i+1)
            hunter = i+1
        elif temp_id == 5:
            temp_identification = "白痴神"
            god_camp.append(i+1)
            idiot = i+1
        elif temp_id == 6:
            temp_identification = "平民"
            villager_camp.append(i+1)
        else:
            print("Unknown Commands!")
            sys.exit()
        data_play.append({'Seat':i+1, 'No':temp_no, 'Identification': temp_identification, 'Identifiaction(id in number)': temp_id,
                          "警長投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第1輪投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第2輪投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第3輪投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第4輪投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第5輪投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第6輪投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "警長PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第1輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第2輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第3輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第4輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第5輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "第6輪PK投票 (0 for 棄票, -1 for 無法投票)": -1,
                          "特殊功能加分": 0})
    df_play = pd.DataFrame(data_play, columns=['Seat', 'No', 'Identification', 'Identifiaction(id in number)',
                                               '警長投票 (0 for 棄票, -1 for 無法投票)',
                                               '第1輪投票 (0 for 棄票, -1 for 無法投票)',
                                               '第2輪投票 (0 for 棄票, -1 for 無法投票)',
                                               '第3輪投票 (0 for 棄票, -1 for 無法投票)',
                                               '第4輪投票 (0 for 棄票, -1 for 無法投票)',
                                               '第5輪投票 (0 for 棄票, -1 for 無法投票)',
                                               "第6輪投票 (0 for 棄票, -1 for 無法投票)",
                                               "警長PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第1輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第2輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第3輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第4輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第5輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "第6輪PK投票 (0 for 棄票, -1 for 無法投票)",
                                               "特殊功能加分"])
    print("這場身份如下：")
    print(df_play[['Seat', 'No', 'Identification']])

    print("狼人陣營:",wolf_camp)
    print("神職陣營:",god_camp)
    print("平民陣營:",villager_camp)

    already_death = []
    wolf_action = -1  #Kill whom  Not killing: 0
    witch_action = -1 #Status: -1, can save and poison; -2, can only poison, -3, can only save; -5: nothing
    gun_action = -1   #Cannot kill:0, kill:Seat Number
    prophet_action = -1
    print("-------------------------------")
    print("第一晚:")
    wolf_temp = input("請輸入狼人擊殺對象 (0:空刀):")
    witch_temp = input("請輸入女巫是否發動技能（-1:空, 0:救人, 座位號碼:毒人):")
    prophet_temp = input("請輸入預言家查驗對象:")
    if prophet not in player_survive:
        pass
    else:
        for wolf in wolf_camp:
            if wolf == int(prophet_temp):
                prophet_action = 0
                print("預言家查驗的玩家%s為狼人"%prophet_temp)
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

    candidate = input("警上玩家:（若多位玩家上警請以空格隔開）")
    voter = input("警下玩家:（若多位玩家上警請以空格隔開）")

    candidate = [int(player) for player in candidate.split()]
    voter = [int(player) for player in voter.split()]

    print("發言完畢時請按Enter以繼續")
    input()
    print("發言完畢,退水環節")
    true_candidate = input("警上玩家剩餘:（若多位玩家上警請以空格隔開）")
    true_candidate = [int(player) for player in true_candidate.split()]

    if len(true_candidate) == 1:
        sergeant = true_candidate[0]
        print("%s自動當選警長"%str(true_candidate[0]))
    else:
        for player in voter:
            vote = input("%s號玩家投的是:（棄票請打0）"%str(player))
            vote = int(vote)
            if vote not in true_candidate:
                vote = 0       #亂投票=棄票
            df_play['警長投票 (0 for 棄票, -1 for 無法投票)'][player-1] = vote
            if vote == 0:
                continue
            tickets[vote-1] += 1
        print("投票結果如下：")
        print(df_play[['Seat', 'No', '警長投票 (0 for 棄票, -1 for 無法投票)']])
        max_tickets = np.max(tickets)
        max_candidate = np.where(tickets == max_tickets)[0]+1
        if len(max_candidate) > 1:
            tickets = np.zeros(12)      #Initialize
            all_players = order_initialize(np.copy(tickets))
            print("all:", all_players)
            voter = np.setdiff1d(all_players,max_candidate)
            print("v:", voter)
            print("因為超過一人得最高票，能繼續參與PK競選的為:", max_candidate)
            print("發言完畢時請按Enter以繼續")
            input()
            for player in voter:
                vote = input("%s號玩家投的是:（棄票請打0）"%str(int(player)))
                vote = int(vote)
                if vote not in max_candidate:
                    vote = 0       #亂投票=棄票
                df_play['警長PK投票 (0 for 棄票, -1 for 無法投票)'][player-1] = vote
                if vote == 0:
                    continue
                tickets[vote-1] += 1
            max_tickets = np.max(tickets)
            max_candidate = tickets[tickets==max_tickets]
            print("投票結果如下：")
            print(df_play[['Seat', 'No', '警長PK投票 (0 for 棄票, -1 for 無法投票)']])
            if len(max_candidate) > 1:
                print("平票，警徽流失!")
                sergeant = -1

        if sergeant > -1:
            sergeant = tickets.argmax()+1
            print("%s號玩家當選警長"%str(sergeant))


    death = np.array([])
    if witch_temp == 0:
        print("昨晚為平安夜!")
    elif int(wolf_temp)==0 and witch_temp==-1:
        print("昨晚為平安夜!")
    elif int(wolf_temp)==0 and witch_temp>0:
        print("昨晚%s倒牌"%str(witch_temp))
        death = np.append(death, witch_temp)
    elif witch_temp==-1:
        print("昨晚%s倒牌"%str(wolf_temp))
        death = np.append(death, int(wolf_temp))
        if int(wolf_temp)==hunter:
            hunt = input("公投出局的玩家是否要開槍:(0 for 不開槍)")
            if hunt!=0:
                death = np.append(death, hunt)
                if hunt in wolf_camp:
                    df_play['特殊功能加分'][hunter-1] += 0.5
                else:
                    df_play['特殊功能加分'][hunter-1] += -0.5
                print("%s玩家出局，請留遺言!"%hunt)
    elif witch_temp==int(wolf_temp):
        print("昨晚%s倒牌"%str(wolf_temp))
        death = np.append(death, int(wolf_temp))
    else:
        print("昨晚倒牌的玩家有兩名", wolf_temp, str(witch_temp))
        death = np.append(death, int(wolf_temp))
        death = np.append(death, witch_temp)
        if int(wolf_temp)==hunter:
            hunt = input("公投出局的玩家是否要開槍:(0 for 不開槍)")
            if hunt!=0:
                death = np.append(death, hunt)
                if hunt in wolf_camp:
                    df_play['特殊功能加分'][hunter-1] += 0.5
                else:
                    df_play['特殊功能加分'][hunter-1] += -0.5
                print("%s玩家出局，請留遺言!"%hunt)

    if sergeant in death:
        temp = input("%s移交警徽給(撕掉請輸入0):"%str(sergeant))
        sergeant = int(temp)
    death = death.astype('float')
    death = death.astype('int')
    player_survive = np.setdiff1d(player_survive, death)

    while(True):
        game_day += 1
        print("------第%s天白天------"%str(game_day))
        print("剩餘存活玩家為", player_survive)
        player_survive, vote_array, hunter_status, sergeant = daily(player_survive, wolf_camp, god_camp, villager_camp, hunter, sergeant)

        label = "第"+str(game_day)+"輪投票 (0 for 棄票, -1 for 無法投票)"
        label_pk = "第"+str(game_day)+"輪PK投票 (0 for 棄票, -1 for 無法投票)"
        for i in range(12):
            df_play[label][i] = vote_array[0,i]
            df_play[label_pk][i] = vote_array[1,i]
        df_play['特殊功能加分'][hunter-1] += hunter_status
        game_status, winner = if_end(player_survive, wolf_camp, god_camp, villager_camp, sergeant)
        if(not game_status):
            break
        print("剩餘存活玩家為", player_survive)
        print("------第%s天晚上------"%str(game_day+1))
        player_survive, witch_action, witch_status, hunter_status, sergeant = night(player_survive, wolf_camp, god_camp, villager_camp, witch_action,witch, prophet, hunter, sergeant)
        df_play['特殊功能加分'][hunter-1] += hunter_status
        df_play['特殊功能加分'][witch-1] += witch_status
        game_status, winner = if_end(player_survive, wolf_camp, god_camp, villager_camp, sergeant)
        if(not game_status):
            break

    mvp1 = input("請輸入第一位好人陣營 MVP:")
    mvp2 = input("請輸入第二位好人陣營 MVP:")
    mvp3 = input("請輸入一位狼人陣營 MVP:")

    scores = np.zeros((12,4))
    if winner==0:   #好人獲勝
        for player in range(1,13):
            if player in wolf_camp:
                scores[player-1,0] = df_play['No'][player-1]
                scores[player-1,1] = -3
                scores[player-1,2] = 0
                scores[player-1,3] = 1

            else:
                scores[player-1,0] = df_play['No'][player-1]
                scores[player-1,1] = 3
                scores[player-1,2] = 1
                scores[player-1,3] = 0
    else:
        for player in range(1,13):
            if player in wolf_camp:
                scores[player-1,0] = df_play['No'][player-1]
                scores[player-1,1] = 3
                scores[player-1,2] = 1
                scores[player-1,3] = 0

            else:
                scores[player-1,0] = df_play['No'][player-1]
                scores[player-1,1] = -3
                scores[player-1,2] = 0
                scores[player-1,3] = 1

    #MVP
    scores[int(mvp1)-1, 1] += 5
    scores[int(mvp2)-1, 1] += 3
    scores[int(mvp3)-1, 1] += 5
    for player in range(1,13):
        for game_day in range(1,7):
            label = "第"+str(game_day)+"輪投票 (0 for 棄票, -1 for 無法投票)"
            label_pk = "第"+str(game_day)+"輪PK投票 (0 for 棄票, -1 for 無法投票)"
            if df_play[label][player-1] in wolf_camp and player not in wolf_camp:
                scores[player-1,1] += 0.5
            elif df_play[label_pk][player-1] not in wolf_camp and player not in wolf_camp:
                if df_play[label_pk][player-1] == -1:
                    pass
                else:
                    scores[player-1,1] -= 0.5
        scores[player-1,1] += df_play['特殊功能加分'][player-1]

    return scores

import nba_api as nba_api
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import boxscoreadvancedv2, teamgamelogs, teamgamelog, teamestimatedmetrics
from nba_api.live.nba.endpoints import scoreboard, boxscore
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import numpy as np
import statistics
import matplotlib.pyplot as plt
import sklearn
from sklearn.exceptions import DataConversionWarning, ConvergenceWarning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor, MLPClassifier


def predictor(x_train, y_train, x_test):
    num = len(x_train)
    x_test = np.array(x_test).reshape(-1, 1)
    y_test = []
    try:
        regr = LinearRegression()
        regr.fit(x_train, y_train)
        y_pred = regr.predict(x_test)
        print("The predicted linear is:", y_pred)

        regr = MLPRegressor(random_state=1, solver='adam', max_iter=1500, learning_rate='adaptive',
                            batch_size=num)
        regr.fit(x_train, y_train)
        mlpregr = []
        mlp = regr.predict(x_test)
        print("The predicted neural is:", mlp)
        y_test.append(y_pred)
        y_test.append(mlp)
    except DataConversionWarning or ConvergenceWarning:
        pass
    return y_test


intro = "C:\\Users\\lukeh\\PycharmProjects\\MLB_Proj\\"
for j in intro:
    if j == '\\':
        j.replace('\\', '/')

def nba_schedule_former():
    def nba_matchup_finder():
        box = scoreboard.ScoreBoard().get_dict()
        print(box['scoreboard']['games'][0]['homeTeam']['teamId'])
        matchup = []
        match = []
        for k in range(len(box['scoreboard']['games'])):
            match = [box['scoreboard']['games'][k]['homeTeam']['teamId'],
                     box['scoreboard']['games'][k]['homeTeam']['teamTricode'],
                     box['scoreboard']['games'][k]['awayTeam']['teamId'],
                     box['scoreboard']['games'][k]['awayTeam']['teamTricode'],
                     box['scoreboard']['games'][k]['gameId']]
            matchup.append(match)
            match = []
        print(matchup)
        return matchup

    output = {}
    matchups = nba_matchup_finder()
    for i in range(len(matchups)):
        output[matchups[i][-1]] = {'home': matchups[i][1], 'away': matchups[i][3], 'home_score_1': 0, 'away_score_1': 0,
                                   'home_score_2': 0, 'away_score_2': 0, 'h_off_eff': 0, 'h_def_eff': 0, 'a_off_eff': 0,
                                   'a_def_eff': 0, 'homeid': matchups[i][0], 'awayid': matchups[i][2]}
    for t in output.keys():
        print(output[t])
    log = teamgamelogs.TeamGameLogs(season_nullable='2022-23', timeout=300).get_dict()
    result = log['resultSets']

    result = result[0]
    headers = result['headers']
    games = result['rowSet']
    matchup = []
    for i in games:
        matchup.append(i[6])

    row = []
    teams = []
    teamid = []
    for i in games:
        if i[3] in teams:
            continue
        else:
            teams.append(i[3])
    print(headers)
    row.append(headers)
    for i in games:
        row.append(i)
    df = pd.DataFrame(row)

    gameid = []
    Dict = {}
    stat = ['points for', 'points against', 'opp', 'opp_id', 'opp_off_eff', 'opp_def_eff']
    for i in teams:
        Dict[i] = {'gameid':{'points for':'points scored', 'points against':'opponent score','opp':'the opponent',
                   'opp_id':'the opponent id', 'opp_off_eff':'the opponent offensive efficiency' ,
                             'opp_def_eff':'opponent defensive efficiency'}}
    for j in range(len(games)):
        for i in teams:
            if i == games[j][3]:
                Dict[i][games[j][4][2:]] = {stat[0]: 0, stat[1]: 0, stat[2]: 'opp',stat[3]: 0, stat[4]: 0, stat[5]: 0}

    for j in range(len(games)):
        for i in teams:
            if i == games[j][3]:
                Dict[i][games[j][4][2:]][stat[0]] = int(games[j][28])
    for i in Dict.keys():
        for k in Dict[i].keys():
            for j in range(len(games)):
                if (games[j][2] != i) and (k[:2] == games[j][4][:2]):
                    Dict[i][k][stat[1]] = int(games[j][28])
                    Dict[i][k][stat[2]] = games[j][3]
    '''
    metrics = teamestimatedmetrics.TeamEstimatedMetrics(season='2022-23', league_id=00, season_type='Regular Season')
    maybe = teamestimatedmetrics.TeamEstimatedMetrics(season='2022-23', league_id=00, season_type='Regular Season').DataSet
    result = metrics.team_estimated_metrics.data['data']
    maybe = maybe
    #result = metrics.team_estimated_metrics.get_data_frame()
    print(result)
    print(maybe)
    '''
    boxed = []

    for i in Dict.keys():
        for k in Dict[i].keys():
            for j in range(len(games)):
                if Dict[i][k]['opp_id'] == 0:
                    if i == games[j][3]:
                        Dict[i][k]['opp_id'] = games[j][1]
    scores = scoreboard.ScoreBoard().get_dict()
    print(scores)

    def nba_eff_fetcher(url):
        intro = "C:\\Users\\lukeh\\PycharmProjects\\MLB_Proj\\"
        for j in intro:
            if j == '\\':
                j.replace('\\', '/')


        options = Options()
        options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        shitshow = driver.page_source

        h = driver.find_elements(By.CLASS_NAME, "text-right")
        o = driver.find_elements(By.CLASS_NAME, 'odd')
        t = driver.find_elements(By.CLASS_NAME, 'even')
        print('SHITSHOW DONE')
        odd = []
        even = []
        team = []
        eff_off = []
        for b in h:
            eff_off.append(b.get_attribute('innerHTML'))
        for p in t:
            p = p.get_attribute('innerHTML')
            p = p.split('</a>')[0]
            p = p.split('a href')[1]
            p = p.split('\">')[1]
            even.append(p)
        for u in o:
            u = u.get_attribute('innerHTML')
            u = u.split('</a>')[0]
            u = u.split('a href')[1]
            u = u.split('\">')[1]
            odd.append(u)
        for w in range(29):
            if w == 0:
                team.append(odd[int(w)])
            if w%2 == 0:
                team.append(even[int(w/2)])
            if w%2 != 0:
                team.append(odd[int((w+1) / 2)])
        key = []
        for a in range(0, len(eff_off), 6):
            key.append(eff_off[a:a+6])
        key = key[1:]
        # i.get_attribute('innerHTML'))
        driver.quit()
        my_dict = {}
        head = ['2022', 'Last 3', 'Last 1', 'Home', 'Away', '2021']
        for c in team:
            my_dict[c] = {}
        for c in team:
            for r in head:
                my_dict[c][r] = 0
        for c in range(len(team)):
            for r in range(len(head)):
                if my_dict[team[c]][head[r]] == 0:
                    my_dict[team[c]][head[r]] = key[c][r]
        return my_dict
        # trial = [class="text-right", class="text-left nowrap"]

    url1 = 'https://www.teamrankings.com/nba/stat/offensive-efficiency'
    url2 = 'https://www.teamrankings.com/nba/stat/defensive-efficiency'
    o_eff = nba_eff_fetcher(url1)
    d_eff = nba_eff_fetcher(url2)
    print(o_eff)
    head = ['2022', 'Last 3', 'Last 1', 'Home', 'Away', '2021']
    for i in Dict.keys():
        for k in Dict[i].keys():
            for q in o_eff.keys():
                if Dict[i][k]['opp_off_eff'] == 0:
                    if q[:2] == Dict[i][k]['opp'][:2]:
                        Dict[i][k]['opp_off_eff'] = str(float((float(o_eff[q]['Last 3']))))
    for i in Dict.keys():
        for k in Dict[i].keys():
            for q in d_eff.keys():
                if Dict[i][k]['opp_def_eff'] == 0:
                    if q[:2] == Dict[i][k]['opp'][:2]:
                        Dict[i][k]['opp_def_eff'] = str(float((float(d_eff[q]['Last 3']))))
    teaming = {}
    for t in Dict.keys():
        for r in Dict[t].keys():
            print(Dict[t][r])
    for i in output.keys():
        for k in Dict.keys():
            for l in Dict[k].keys():
                if output[i]['homeid'] == Dict[k][l]['opp_id']:
                    if len(output[i]['home']) == 3:
                        if output[i]['home'] == Dict[k][l]['opp'][:1]:
                            output[i]['home'] = Dict[k][l]['opp']
                if output[i]['awayid'] == Dict[k][l]['opp_id']:
                    if len(output[i]['away']) == 3:
                        if output[i]['away'] == Dict[k][l]['opp'][:1]:
                            output[i]['away'] = Dict[k][l]['opp']
    for k in output.keys():
        print(output[k])
    for i in output.keys():
        for q in o_eff.keys():
            if output[i]['h_off_eff'] == 0:
                if q[:4] == output[i]['home'][:4]:
                    output[i]['h_off_eff'] = str(float((float(o_eff[q]['Last 3']))))
    for i in output.keys():
        for q in o_eff.keys():
            if output[i]['a_off_eff'] == 0:
                if q[:4] in output[i]['away'][:4]:
                    output[i]['a_off_eff'] = str(float((float(o_eff[q]['Last 3']))))
    for i in output.keys():
        for q in d_eff.keys():
            if output[i]['h_def_eff'] == 0:
                if q[:4] in output[i]['home'][:4]:
                    output[i]['h_def_eff'] = str(float((float(d_eff[q]['Last 3']))))
    for i in output.keys():
        for q in d_eff.keys():
            if output[i]['a_def_eff'] == 0:
                if q[:4] in output[i]['away'][:4]:
                    output[i]['a_def_eff'] = str(float((float(d_eff[q]['Last 3']))))

    for k in output.keys():
        print(output[k])

    def team_predictor(team, a_dict, matches):
        keyglock = ['points for', 'points against', 'opp', 'opp_id', 'opp_off_eff', 'opp_def_eff']
        slatt = a_dict
        l = team
        points = []
        opp = []
        matched = matches
        team_off_eff = []
        team_def_eff = []
        for n in slatt[l].keys():
            if n == 'gameid':
                continue
            else:
                points.append(float(slatt[l][n][keyglock[0]]))
                opp.append(float(slatt[l][n][keyglock[1]]))
                team_off_eff.append(float(slatt[l][n][keyglock[-2]]))
                team_def_eff.append(float(slatt[l][n][keyglock[-1]]))
        for o in matched.keys():
            print(o, '\n')
            print(matched[o], '\n\n')
        points = np.array(points).reshape(-1, 1)
        opp = np.array(opp).reshape(-1, 1)
        team_off_eff = np.array(team_off_eff).reshape(-1, 1)
        team_def_eff = np.array(team_def_eff).reshape(-1, 1)
        '''print(points, '\n')
        print(opp, '\n')
        print(team_off_eff, '\n')
        print(team_def_eff, '\n')'''
        for p in matched.keys():
            if matched[p]['home'][:3] == l[:3]:
                print('done')
                opp_off_eff = float(matched[p]['a_off_eff'])
                opp_def_eff = float(matched[p]['a_def_eff'])
                print(predictor(team_off_eff, opp, opp_off_eff), '\n')
                print(predictor(team_def_eff, points, opp_def_eff), '\n')
                matched[p]['home_score_1'] = predictor(team_def_eff, points, opp_def_eff)
                matched[p]['away_score_1'] = predictor(team_off_eff, opp, opp_def_eff)
            if matched[p]['away'][:3] == l[:3]:
                print('done')
                opp_off_eff = float(matched[p]['h_off_eff'])
                opp_def_eff = float(matched[p]['h_def_eff'])
                print(predictor(team_off_eff, opp, opp_off_eff), '\n')
                print(predictor(team_def_eff, points, opp_def_eff), '\n')
                matched[p]['away_score_2'] = predictor(team_def_eff, points, opp_def_eff)
                matched[p]['home_score_2'] = predictor(team_off_eff, opp, opp_off_eff)
        return matched
    for i in output.keys():
        team_predictor(output[i]['home'], Dict, output)
    for i in output.keys():
        team_predictor(output[i]['away'], Dict, output)
    print(output)
    wet = []
    for u in output.keys():
        wet.append(pd.DataFrame([output[u]['home'], output[u]['home_score_1'][0],output[u]['home_score_1'][1],
                                 output[u]['home_score_2'][0],output[u]['home_score_2'][1],
                                output[u]['away'], output[u]['away_score_1'][0],output[u]['away_score_1'][1],
                                output[u]['away_score_2'][0],output[u]['away_score_2'][1]]))
    for h in wet:
        h.to_csv(intro + '3-22-23-recent_nba.csv', mode='a+')
    '''
    print('Expect the Magic to score as primary team:')
    team_predictor('Orlando Magic', Dict, output)
    print('\n\n\rExpect the Hornets to score as primary team:')
    team_predictor('Charlotte Hornets', Dict, output)
    
    for i in Dict.keys():
        for k in Dict[i].keys():
            for l in output.keys():
                if Dict[i][k]['opp_id'] == output[l]['home']:
                    
                if Dict[i][k]['opp_id'] == output[l]['away']:
    '''

    # df.to_csv(intro+'test1.0_nba.csv', mode='a+')

nba_schedule_former()
import csv
import bs4
import os
import sys

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from urllib.request import urlopen
from bs4 import BeautifulSoup

import json
def form_nba_today():
    html = 'https://www.nbastuffer.com/2022-2023-nba-team-stats/'
    url = 'https://www.fantasypros.com/nba/offense-vs-defense.php'
    matched = 'https://www.rotowire.com/betting/nba/odds'
    # Importing the required modules
    ## get number of matchups in day

    ## file prep
    count = 4
    file_names = ['regular', 'last5', 'road', 'home']
    # create file preparation, stripping \ for info file
    fixed_file_names = []
    intro = "C:\\Users\\lukeh\\PycharmProjects\\MLB_Proj\\"
    for j in intro:
        if j == '\\':
            j.replace('\\', '/')
    file_path = 'mlb_end_of_reg_szn_hitting_'
    file_name = intro + 'nba_stats_today'
    write_to = 'nba_today'
    ### scrub sites for data
    data = []
    red = pd.read_html(html, index_col='TEAM')
    matchups = pd.read_html(url, index_col='Team')

    ### write to the distinct files the scrubbed data
    ### create list with 4 elements, being the file names, with elements of the set of data in dataframe
    ### create dict with data as value and key as file_names[iterator]
    Dict = {'Team':{'stat':{'category': 'stat value'}}}
    ### creates dict and list with each element being a dict conglomerating the list
    regular = {}
    recent = {}
    road = {}
    home = {}
    sheet = [0, 0, 0, 0]
    matchup = []
    for i in range(len(matchups)):
        matchup.append(matchups[i])
    for i in range(len(red)):
        red[i].to_csv(file_name + file_names[i] + '.csv')
        data.append(red[i])

    ### read empty csv file into dataframe then write matchups to csv
    writing = pd.read_csv(intro + write_to + '.csv', skipinitialspace=True)
    writing_to = intro + write_to + '.csv'
    written = pd.DataFrame(matchups[0])

    written.to_csv(writing_to, mode='a+')
    written.to_html()

    ### read in csv into dataframe, will be matchups in unfilled table
    writing = pd.DataFrame(pd.read_csv(intro + write_to + '.csv' , header=None, skipinitialspace=False, low_memory=False))
    total_teams = []
    for i in data[-1].index:
        total_teams.append(i)
    ### reshape data
    for k in data:
        k = pd.DataFrame(k).reset_index()
        k = k[1:]
    ### create list where elements are dicts with value being a dict, key being the stat category
    ### nested dict has team as key and value as stat nested for
    for k in range(len(data)):
        sheet[k] = data[k].to_dict()
    keyglock = []

    for i in data:
        for j in i.keys():
            keyglock.append(j)

    for l in sheet:
        print(l['OEFFOffensive EfficiencyPoints scored per 100 possessions.']['Boston'])

    ### create data frame with matchup table is
    todays = pd.DataFrame(matchup[:][:][0])
    teams = []
    for i in todays[:][:]['FG%'].keys():
        teams.append(i)
    fatcat = []
    key1 = []
    key2 = []
    key3 = []
    key4 = []
    for i in sheet[0].keys():
        key1.append(i)
    for i in sheet[1].keys():
        key2.append(i)
    for i in sheet[2].keys():
        key3.append(i)
    for i in sheet[3].keys():
        key4.append(i)
    kat=[]
    kat.append(key1)
    kat.append(key2)
    kat.append(key3)
    kat.append(key4)
    print(kat)
    print(sheet[0]['GP']['Boston'])
    print(sheet[1]['GP']['Boston'])
    print(sheet[2]['GP']['Boston'])
    print(sheet[0]['SOSStrength of the ScheduleOpponent efficiency differential average for all games played so far (venue of the games also taken into account) is used as an indicator of strength of the schedule. The higher the SoS rating, the tougher the schedule; where zero is average.']['Boston'])
    that = todays[:][:]['FG%']
    cat = []

    count = 0
    for i in total_teams:
        Dict[i] = {}
        for key in kat:
            for glock in key:
                Dict[i][glock] = {}
                r = range(0, 4, 1)
                for x in r:
                    Dict[i][glock][file_names[x]] = str('nan')
    for i in total_teams:
        for key in kat:
            for glock in key:
                r = range(0, 4, 1)
                for x in r:
                    Dict[i][glock].update({file_names[x]:sheet[x][kat[x][key.index(glock)]][i]})
    add = []
    playing = []
    additions = []
    for i in Dict.keys():
        for j in teams:
            if i[0:3] == j[0:3]:
                playing.append(i)
                continue

    '''
    for i in playing:
        add.append([])
        for j in Dict[i].keys():
            add[playing.index(i)].append([])
    '''
    for j in teams:
        if j == 'Los Angeles Lakers':
            playing.append('LA Lakers')
        if j == 'Los Angeles Clippers':
            playing.append('LA Clippers')
    print(playing)
    louis = []
    for i in Dict.keys():
        if i not in playing:
            continue
        else:
            add.append(pd.DataFrame(Dict[i]))
            louis.append([i, Dict[i]])

    for i in add:
        del i['RANK']
        del i['CONF']
        del i['DIVISION']

    file_name = intro + 'nba_today_filled'

    for j in louis:
        j[1]['Team'] = j[0]
        additions.append(pd.DataFrame(j[1]))

    for i in additions:
        i.to_csv(file_name+'.csv', mode='a+')


    '''
    for i in add:
        for j in i.values():
            written = written.from_dict(j)
            print(written)
            for k in written.keys():
                pd.concat( written, df)
    print(df)
    
    for key in kat:
        for glock in key:
            for l in file_names:
                for k in total_teams:
                    Dict[k][glock][l].replace(str(np.NAN),str(sheet[kat.index(key)][glock][k]))
    print(Dict)
    
    write_to = write_to + '_filled'
    written = pd.DataFrame(Dict)
    written.to_csv(writing_to, mode='a+')
    

   
    for l in file_names:
        for glock in keyglock:
            for k in total_teams:
                Dict[k][glock][l].update(sheet[file_names.index(l)][glock][k])
    
               
    print(len(data))
    for i in todays.keys():
        cat.append(i)
    for z in range(len(keyglock)):
        for m in range(len(total_teams)):
            for h in range(len(data)):
                fatcat.append(sheet[int(h)][str(keyglock[z])][total_teams[m]])
    for l in file_names:
        for k in range(len(total_teams)):
            for j in range(len(sheet)):
                for i in range(len(teams)):
                    if str(teams[i][0:2]) == str(total_teams[k][0:2]):
                        dict[total_teams[k]][keyglock[j]][l] = sheet[j][keyglock[j]][total_teams[k]]
    print(keyglock)
    print(dict)
    print(fatcat)

    ### write data, a list of df, to csv. element by element
    for i in data:
        i.to_csv(writing_to, mode='a+')
    
    ### read in filled data
    
    
    writing_to = intro + write_to + '.csv'
    df = pd.read_csv(writing_to, skipinitialspace=True)
    lists = []
    write_that = []
    write_that.append(add[3].keys())
    for key in kat:
        for glock in key:
            for j in additions[3:]:
                for i in additions[3].keys():
                    adding = []
                    for l in file_names:
                        if j[kat[file_names.index(l)][key.index(glock)]][l] == np.NAN:
                            del j[kat[file_names.index(l)][key.index(glock)]][l]

                        keys, values = j[kat[file_names.index(l)][key.index(glock)]][l].keys(), j[kat[file_names.index(l)][key.index(glock)]][l].values()

                        for h in values:
                            adding.append(h)
                    add_to = []
                    add_to.append(adding)
            write_that.append(add_to)

    print(write_that)
    write_that[0] = write_that[0].transpose()
    for k in write_that[1:]:
        k=pd.DataFrame(k)

    write_that = pd.DataFrame(write_that)
    print(write_that)
    #
    file_name = intro + 'nba_stats_today'
    write_that.to_csv(file_name+'_filled.csv', mode='w')

    
    for x in additions:
        for key in kat:
            for glock in key:
                for i in playing:
                    for l in file_names:
                        play = []
                        y = x[glock][l]
                        play.append(y)
                        lists.append(play)
    #print(lists)
    '''

    print(written)


form_nba_today()


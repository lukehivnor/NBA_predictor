import csv
import bs4
import os
import sys

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import xarray as xr
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = 'https://www.nbastuffer.com/2022-2023-nba-team-stats/'
url = 'https://www.fantasypros.com/nba/offense-vs-defense.php'
# Importing the required modules
'''
count = int(input('Enter the number of files for info stripping: \n'))
file_names = []
for i in range(count-1):
    info_file_name = input('Enter abbreviated file name for data filling here: \n')
    file_names.append(info_file_name)

'''
num_matchups = 13
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

data = []
red = pd.read_html(html, index_col='TEAM')
matchups = pd.read_html(url, index_col='Team')
dict = {}

for i in range(len(red)):
    red[i].to_csv(file_name + file_names[i] + '.csv')
    data.append(red[i])
    dict[file_names[i]] = red[i]

field_names = []


writing = pd.read_csv(intro + write_to + '.csv', skipinitialspace=True)
writing_to = intro + write_to + '.csv'
written = pd.DataFrame(matchups[0])
written.to_csv(writing_to,mode='a+')

writing = pd.DataFrame(pd.read_csv(intro + write_to + '.csv' , skipinitialspace=False, low_memory=False))
header = writing[0:3]

teams = writing[1:2][:]
rows = []
###
count = 0
while count < 103:
    rows.append(writing[:][count:count+1])
    count += 1

print('count = ', count)



def updater(files, new):
    writing_dict = {}
    writings = files
    for i in range(len(writings)):
        writing_dict[writings[i,0]] = writings[i,1]
    ## create looped boolean that will replace value from info_reader to value in writing_reader if key matches ##
    for i in range(len(writings)-1):
        if writings[i][0] in writing_dict:
            writing_dict[writings[i,0]] = writings[i,1]
    print(writing_dict)
    exit()




'''
## UPDATING CHUNK ##
for j in range(2,count):
    for i in range(2, count):
        if rows[j].columns.intersection(data[j][i].columns) != np.NAN:
            (rows[j]).update(data[j])
print(teams)


###



'''
for k in data:
    k = pd.DataFrame(k).reset_index()


for i in data:
    i.to_csv(writing_to, mode='a+')


write_to = write_to + '_filled'
writing = pd.read_csv(intro + write_to + '.csv' , skipinitialspace=True, dtype=object, low_memory=False).to_dict()

regular = {}
recent = {}
road = {}
home = {}
sheet = [regular, recent, road, home]
for i in writing:
    i = i[24:28][:]

for i in writing:
    print('i=', i, ',', '\n',
          'writing[i]=', writing[i], '\n')



'''
for i in sheet:
    for j in writing[:][:]:
        i[writing[][j]] = writing[-1:-5][j]
    print(i)

'''

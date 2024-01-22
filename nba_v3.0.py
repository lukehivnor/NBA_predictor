

import csv
import bs4
import os
import sys
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

def nba_matcher():
    options = Options()

    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.betonline.ag/sportsbook/basketball/nba")
    shitshow = driver.page_source

    print('SHITSHOW DONE')
    odds = []
    h = driver.find_elements(By.CLASS_NAME, "lines-row__money")
    str1= 'bet-pick__wager-point ng-star-inserted'
    str2 ='bet-pick__wager ng-star-inserted'
    str3= 'bet-pick ng-star-inserted'
    str4 = 'lines-row__spread'
    for i in h:
        odds.append(i.get_attribute('innerHTML').split(sep="----><!---->"))
    print('Thats all of the stripped mL')
    odding = []
    for i in odds:
        try:
            odding.append(i[4].split(sep=' <!')[0])
        except IndexError:
            pass
    teaming = []
    teams = []
    f = driver.find_elements(By.CLASS_NAME, 'lines-row__team-row')
    for i in f:

        teaming.append(i.get_attribute('innerHTML').split(sep='"">')[1])
    for i in teaming:
        teams.append(i.split(sep='</span')[0])

    print('That is all of the teams')
    f = driver.find_elements(By.XPATH, './/span[@class = "lines-row__team-name"]')

    driver.quit()
    count = 0
    counter = 0
    for i in range(0, int(len(teams))-1, 2):
        for j in range(0, int(len(odding))-1, 2):
            if count == i:
                if counter == j:
                    print('Today the %s, at odds %s, visit the %s, at odds %s.'%(str(teams[i]), odding[j], teams[i+1], odding[j+1]))
                    counter += 2
                    count += 2
    print(len(teams), '\n')
    print(len(odding))
    print(teams)
    print(odding)
    #### Need to change teams[:4] so its only teams playing today not tmo too
    return teams, odding


teams = []
odds = []
total = []
g=1
'''while g==1:
    nba_matcher()
    odds.append(nba_matcher()[1])
    time.sleep(300)
    print(odds)'''
intro = "C:\\Users\\lukeh\\PycharmProjects\\MLB_Proj\\"
for j in intro:
    if j == '\\':
        j.replace('\\', '/')

while 1:
    nba_matcher()
    teams.append(nba_matcher()[0])
    odds.append(nba_matcher()[1])
    for i in range(len(teams)):
        df = pd.DataFrame(teams[i], odds[i])
        total.append(df)
    for i in total:
        i.to_csv(intro + 'test_2-24-23_odds_collection.csv', mode='a+')
    time.sleep(600)





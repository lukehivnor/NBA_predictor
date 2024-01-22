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
from sklearn.exceptions import DataConversionWarning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor, MLPClassifier
intro = "C:\\Users\\lukeh\\PycharmProjects\\MLB_Proj\\"
for j in intro:
    if j == '\\':
        j.replace('\\', '/')

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
                     box['scoreboard']['games'][k]['gameId'] ]
        matchup.append(match)
        match = []
    print(matchup)
    return matchup

nba_matchup_finder()
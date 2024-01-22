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
        mean = statistics.mean(y_test)
    except DataConversionWarning or ConvergenceWarning:
        pass
    return y_test


intro = "C:\\Users\\lukeh\\PycharmProjects\\MLB_Proj\\"
for j in intro:
    if j == '\\':
        j.replace('\\', '/')

def nba_matchup_finder():
    box = scoreboard.ScoreBoard().get_dict()
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


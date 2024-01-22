import csv
import bs4
import os
import sys
import pandas as pd
import statistics
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import pybettor
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor, MLPClassifier

def odds_predictor(num):
    intro = "C:\\Users\\lukeh\\PycharmProjects\\MLB_Proj\\"
    for j in intro:
        if j == '\\':
            j.replace('\\', '/')
    odds = []
    timing = []
    odding = []
    df = pd.read_csv(intro+'test_odds_collection.csv')
    for i in df.keys():
        for j in range(num):
            odds.append(df['Odds'][j])
            timing.append(df['Time'][j])
    print(timing)
    print(len(odds))

    for i in odds:
        if i <= int(-100):
            k = 1 / (1 - 100 / (i))
            odding.append(k)
        else:
            k = 1 / (1 + i / 100)
            odding.append(k)
    print(odding)
    odding = np.array(odding).reshape(-1, 1)
    timing = np.array(timing).reshape(-1, 1)
    x_train = timing
    y_train = odding
    x_test = np.array([240,250,260,270,280]).reshape(-1, 1)
    y_test = []
    regr = LinearRegression()
    regr.fit(x_train, y_train)
    y_pred = regr.predict(x_test)
    print("The predicted probabilities are:", y_pred)
    x_test = np.array([240,250,260,270,280]).reshape(-1, 1)
    '''
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)'''
    regr = MLPRegressor(random_state=1, solver='lbfgs', max_iter=500)
    regr.fit(x_train, y_train)
    mlpregr = []
    mlp = regr.predict(x_test)
    for i in range(len(mlp)-1):
        calc = mlp[i+1] - mlp[i]
        mlpregr.append(calc)
    print("The average calculus for lbfgs while approaching game time leads to: ")
    print(statistics.mean(mlpregr))
    regr = MLPRegressor(random_state=1, solver='adam', max_iter=200, learning_rate='adaptive', batch_size=num)
    regr.fit(x_train, y_train)
    mlpregr = []
    mlp = regr.predict(x_test)
    print("The predicted probabilities are:",mlp)
    for i in range(len(mlp) - 1):
        calc = mlp[i + 1] - mlp[i]
        mlpregr.append(calc)
    print("The average calculus using ADAM approaching game time leads to: ")
    print(statistics.mean(mlpregr))


odds_predictor(24)
# PriceEstimator class and auxiliary functions
# Train and test data source: http://archive.ics.uci.edu/ml/machine-learning-databases/00312/
import math
import pandas as pd
import numpy as np
import operator

import datetime

from sklearn.preprocessing import Normalizer

from errors import InvalidDataError

import collections

# Indexes values - values for the dimensions of the Knn Algorithm:
    # date - 0
    # open - 1
    # high - 2
    # low - 3
    # close - 4
    # volume - 5
    # percent_change_price - 6
    # percent_change_volume_over_last_wk - 7
    # previous_weeks_volume - 8
    # next_weeks_open - 9 
    # next_weeks_close - 10
    # percent_change_next_weeks_price - 11
    # days_to_next_dividend - 12 
    # percent_return_next_dividend - 13

class PriceEstimator:
    def __init__(self, request = None):                                  
        if request != None:
            if request.form.get("year") != '':
                self.date = datetime.date(year = int(request.form.get("year")),
                                            month = int(request.form.get("month")),
                                            day = int(request.form.get("day")))
                self.date = get_last_friday(date)
                self.stock = request.form.get("stock")
        else:
            self.stock = 'AA'
        self.indexes = [5, 6, 12, 13] # the dimensions for the Knn algorithm
        self.train_data, self.test_data = preprocess(self.stock, self.indexes)


    def make_prediction(self):
        train_data, test_data = self.train_data, self.test_data
        predicted_prices = []
        for test in test_data:                                              # prediction is made for the week coming after the test week
            predicted_price = knn(train_data, test, self.indexes)
            predicted_prices.append(predicted_price)
        return predicted_prices

def preprocess(stock, indexes):
    df = pd.read_csv("data/dow_jones_index.data")                           # reading from the file
    data = df.to_dict('records')         
    # Splitting the data based on stock value
    result = collections.defaultdict(list)
    for d in data:
        result[d['stock']].append(d)
    split_data = list(result.values())
    # Searching the requested stock name for prediction
    
    for d in split_data:
        if d[0]['stock'] == stock:
            train_test_data = d

    #splitting the train_test data into train and test data
    train_data, test_data = [], []
    for d in train_test_data:
        if (d['quarter'] == 1):
            train_data.append(list(d.values()))
        else:
            test_data.append(list(d.values()))

    # converting all the values to float type
    for d in train_data:
        for i in range (3, len(d) - 1):
            if isinstance(d[i], str):
                if (d[i][0] == '$'):
                    d[i] = d[i][1:]
                d[i] = float(d[i])
    for d in test_data:
        for i in range (3, len(d) - 1):
            if isinstance(d[i], str):
                if (d[i][0] == '$'):
                    d[i] = d[i][1:]
                d[i] = float(d[i])
    
    
    norm_train_data = normalize(train_data, indexes)
    norm_test_data = normalize(test_data, indexes)
    return norm_train_data, norm_test_data

def normalize_array(array):
    minim = min(array)
    maxim = max(array)
    for i in range(len(array)):
        
        array[i] = (array[i] - minim) / (maxim - minim)
    
    return array


def euclidian_distance(x, y, indexes):
    distance = 0
    for i in indexes:
        distance += pow (x[i] - y[i], 2)
    return math.sqrt(distance)

def get_last_friday(date):
    temp = date - datetime.timedelta(days=date.weekday()) + datetime.timedelta(days=4, weeks=-1)
    one_week = datetime.timedelta(weeks=1)
    if (date - temp > one_week):
        date = temp + one_week
    print(date)
    return date

def normalize(data, indexes):
    transposed_data=[ list(d) for d in zip(*data)]
    transposed_data = transposed_data[2:]
    
    for i in indexes:
        transposed_data[i] = normalize_array(transposed_data[i])

    normalized_data = [ list(d) for d in zip(*transposed_data)]
    return normalized_data
def comp_avg_price(week):
    return (week[9] + week[10]) / 2

def knn(train_data, test, indexes, k = 2):
    distance = []
    for i in range(len(train_data)):
        dist = euclidian_distance(train_data[i], test, indexes)
        distance.append((train_data[i], dist))
    distance.sort(key=operator.itemgetter(1))
    # calculating the avg.
    price_sum = 0
    for i in range(k):
        price_sum += comp_avg_price(distance[i][0])
    
    return price_sum / k
get_last_friday(datetime.date(year =2011, month = 4, day = 4))

p = PriceEstimator()
p.make_prediction()
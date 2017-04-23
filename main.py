import sys
import pandas as pd
import csv


def hdi_history(filename):
    df = pd.read_csv(filename)
    avg = [0] * 7   # init list of avg HDI values for all countries.
    count = [0] * 7
    years = []

    for year in df.keys()[2:]:
        years.append(year.split(" ")[-1:][0])

    for i in range(0, len(df)):
        for j in range(0, 7):
            try:
                avg[j] += float(df.ix[i][j+2])
                count[j] += 1
            except ValueError:
                continue    # skipping junk values

    for i in range(0, 7):
        avg[i] /= count[i]

    print years
    print avg

    new_df = pd.DataFrame(columns=years)
    new_df.loc[0] = avg

    print new_df
    new_df.to_csv('history.csv')

if __name__ == '__main__':
    '''HDI over the years'''
    hdi_history('historical_index.csv')

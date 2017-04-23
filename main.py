import sys
import pandas as pd
import csv


def hdi_history(filename):
    df = pd.read_csv(filename)
    avg = [0] * 7   # init list of avg HDI values for all countries.
    count = [0] * 7
    years = []
    usa_hdi = []

    for year in df.keys()[2:]:
        years.append(year.split(" ")[-1:][0])

    for i in range(0, len(df)):
        # save row for usa.
        if df.ix[i][1] == 'United States':
            usa_hdi = df.ix[i].tolist()[2:]
        for j in range(0, 7):
            try:
                avg[j] += float(df.ix[i][j+2])
                count[j] += 1
            except ValueError:
                continue    # skipping junk values

    # calculating avg HDI for each year.
    for i in range(0, 7):
        avg[i] /= count[i]
        avg[i] = str(avg[i])

    # converting years to integer values
    for i in range(0, len(years)):
        years[i] = years[i][1:-1]
        print years[i]

    for i in range(0, len(usa_hdi)):
        usa_hdi[i] = str(usa_hdi[i])
    print usa_hdi
    print avg


    # converting values to float
    #usa_hdi = map(float, usa_hdi)
    print years



    columns = ['symbol', 'date', 'hdi']
    symbols = ['world', 'usa']

    new_df = pd.DataFrame(columns=columns)

    # fill the new data frame with values
    count = 0
    for i in range(0, len(avg)):
        new_df.loc[count] = ['World', years[i], avg[i]]
        count += 1
    for i in range(0, len(avg)):
        new_df.loc[count] = ['USA', years[i], usa_hdi[i]]
        count += 1

    print new_df
    new_df.to_csv('history.csv', float_format='%.0f')

if __name__ == '__main__':
    '''HDI over the years'''
    hdi_history('historical_index.csv')

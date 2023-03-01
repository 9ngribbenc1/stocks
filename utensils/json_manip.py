# This script contains functions for converting json to Pandas DataFrames as
# doing other useful manipulations of the information.


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def fundamental_to_df(json_fundamental):
    """
    This function converts json data structures to Pandas DataFrames.
    """

    #print(json_fundamental)
    #print(json_income['symbol'])
    #print(json_income['annualReports'][0].keys())
    #print(json_income['quarterlyReports'][0].keys())

    fin_nums = json_fundamental['quarterlyReports'][0].keys()

    #quarter_reports = json_income['quarterlyReports']
    #quarter_dates = [quarter_reports[i]['fiscalDateEnding']
    #                        for i in range(len(quarter_reports))]

    # Create dictionary of lists of individual metric values
    quarter_reports = json_fundamental['quarterlyReports']
    num_vals = {}
    for num in fin_nums:
        num_vals[num] = [quarter_reports[i][num]
                                for i in range(len(quarter_reports))]

    values_df = pd.DataFrame(num_vals)
    #values_df['grossProfit'] = values_df['grossProfit'].astype('float')

    # Convert from objects to datetime and floats
    df_cols = values_df.columns
    #print("Columns", df_cols)
    values_df.replace("None", "0", inplace=True)
    values_df[df_cols[0]] = pd.to_datetime(values_df[df_cols[0]]) 
    for col in df_cols[2:]:
        values_df[col] = values_df[col].astype('float')

    return values_df
    

def balance_to_df(json_income):
    """
    This function converts json data structures to Pandas DataFrames.
    """

    #print(json_income.keys())
    #print(json_income['symbol'])
    #print(json_income['annualReports'][0].keys())
    #print(json_income['quarterlyReports'][0].keys())

    fin_nums = json_income['quarterlyReports'][0].keys()

    #quarter_reports = json_income['quarterlyReports']
    #quarter_dates = [quarter_reports[i]['fiscalDateEnding']
    #                        for i in range(len(quarter_reports))]

    # Create dictionary of lists of individual metric values
    quarter_reports = json_income['quarterlyReports']
    num_vals = {}
    for num in fin_nums:
        num_vals[num] = [quarter_reports[i][num]
                                for i in range(len(quarter_reports))]

    values_df = pd.DataFrame(num_vals)
    #values_df['grossProfit'] = values_df['grossProfit'].astype('float')

    # Convert from objects to datetime and floats
    df_cols = values_df.columns
    print("Columns", df_cols)
    values_df.replace("None", "0", inplace=True)
    values_df[df_cols[0]] = pd.to_datetime(values_df[df_cols[0]]) 
    for col in df_cols[2:]:
        values_df[col] = values_df[col].astype('float')

    return values_df




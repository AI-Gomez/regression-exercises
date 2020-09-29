from sklearn.model_selection import train_test_split
import sklearn.preprocessing
import pandas as pd
import numpy as np
import wrangle
from env import host, user, password
import seaborn as sns
import matplotlib.pyplot as plt

def plot_variable_pairs():
    df = wrangle.get_data_from_sql()
    train_and_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_and_validate, test_size=.2, random_state=123)
    fig = sns.regplot(x='tenure', y='monthly_charges', data=train)
    return fig

def months_to_years():
    df = wrangle.get_data_from_sql()
    df['tenure_years'] = (df.tenure / 12).round(0)
    
    return df

def plot_categorical_and_continuous_vars():
    df = wrangle.get_data_from_sql()
    df['tenure_years'] = (df.tenure / 12).round(0)
    train_and_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_and_validate, test_size=.2, random_state=123)
    
    plt.subplot(321)
    f1 = sns.boxplot(y='monthly_charges', x='tenure_years', data=train)
    plt.subplot(322)
    f2 = train.tenure_years.value_counts().sort_index().plot.bar()
    plt.subplot(323)
    f3 = sns.swarmplot(data=train, y='monthly_charges', x='tenure_years')
    plt.subplot(324)
    f4 = sns.violinplot(data=train, y='monthly_charges', x='tenure_years')

    
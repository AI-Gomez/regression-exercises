import sklearn.preprocessing
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from env import host, user, password

# function to get the url


def get_db_url(db_name):
    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"


def get_data_from_sql():
    query = """
    SELECT customer_id, monthly_charges, tenure, total_charges
    FROM customers
    WHERE contract_type_id = 3;
    """
    df = pd.read_sql(query, get_db_url("telco_churn"))
    return df

def add_scaled_columns(train, validate, test, scaler, columns_to_scale):
    new_column_names = [c + '_scaled' for c in columns_to_scale]
    scaler.fit(train[columns_to_scale])

    train = pd.concat([
        train,
        pd.DataFrame(scaler.transform(train[columns_to_scale]), columns=new_column_names, index=train.index),
    ], axis=1)
    validate = pd.concat([
        validate,
        pd.DataFrame(scaler.transform(validate[columns_to_scale]), columns=new_column_names, index=validate.index),
    ], axis=1)
    test = pd.concat([
        test,
        pd.DataFrame(scaler.transform(test[columns_to_scale]), columns=new_column_names, index=test.index),
    ], axis=1)

    return train, validate, test

def scale_telco_data(train, test, validate):
    train, validate, test = add_scaled_columns(
        train,
        test,
        validate,
        scaler=sklearn.preprocessing.MinMaxScaler(),
        columns_to_scale=['total_charges', 'monthly_charges', 'tenure'],
    )
    return train, validate, test


def wrangle_telco():
    # Gets a df from sql that replaces blanks with nan then changes the dtype to float
    #Also returns the supplied data already split into train-test-validate
    df = get_data_from_sql()
    df.tenure.replace(0, 1, inplace=True)
    df.total_charges = df.total_charges.replace(" ", np.nan)
    df.total_charges = df.total_charges.fillna(df.monthly_charges)
    df.total_charges = df.total_charges.astype(float)

    train_and_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_and_validate, test_size=.2, random_state=123)

    return scale_telco_data(train, test, validate)



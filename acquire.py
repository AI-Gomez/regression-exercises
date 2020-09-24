### Make a new python module, acquire.py to hold the following 
#data aquisition functions:

import pandas as pd
import os
from env import host, password, user 

def get_connection(db, user=user, host=host, password=password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

################ Acquire mall customers #################
def get_connection(db, user=user, host=host, password=password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def new_mall_data():
    '''
    this function reads the mall customer data from the codeup db into a df,
    write it to a csv file, and returns the df.
    '''
    sql_query = 'Select * from customers'
    df = pd.read_sql(sql_query, get_connection('mall_customers'))
    df.to_csv('mall_customers_df.csv')
    return df

def get_mall_data(cached=False):
    '''
    ths function reads in mall customer data from codeup database if cached==False
    or if cached == True reads in mall customer df from a csv file, returns df
    '''
    if cached or os.path.isfile('mall_customers_df.csv') == False:
        df = new_mall_data()
    else:
        df = pd.read_csv('mall_customers_df.csv', index_col=0)
        return df

    

# 1. get_titanic_data: returns the titanic data from the codeup data science database as a pandas data frame.
def get_titanic_data():
    filename = 'titanic.csv'
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=0)
        return df
    else:
        df = pd.read_sql('SELECT * FROM passengers', get_connection('titanic_db'))
        df.to_csv(filename)
        return df
    
# 2. get_iris_data: returns the data from the iris_db on the codeup data science database as a pandas data frame. 
# The returned data frame should include the actual name of the species in addition to the species_ids.
def get_iris_data():
    filename = 'iris.csv'
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=0)
        return df
    else:
        df = pd.read_sql('select * from measurements join species using (species_id);', get_connection('iris_db'))
        df.to_csv(filename)
        return df

def telco_cust():
    sql_query = '''
    select * from customers as c
join internet_service_types as ist on ist.internet_service_type_id = c.internet_service_type_id
join contract_types as cs on cs.contract_type_id = c.contract_type_id
join payment_types as pt on pt.payment_type_id = c.payment_type_id
    '''
    df = pd.read_sql(sql_query, get_connection('telco_churn'))
    return df 

def telco_cust1():
    df1 = pd.read_sql(get_connection('telco_churn'))
    return df1 

####### Regression Exercises Acquire ########
def wrangle_telco():
    sql_query = '''
    select * from customers as c
join internet_service_types as ist on ist.internet_service_type_id = c.internet_service_type_id
join contract_types as cs on cs.contract_type_id = c.contract_type_id
join payment_types as pt on pt.payment_type_id = c.payment_type_id
where contract_type = 'Two year'
    '''
    df = pd.read_sql(sql_query, get_connection('telco_churn'))
    df = df.drop(columns=['internet_service_type_id','contract_type_id', 'payment_type_id', 'gender','senior_citizen', 'partner','dependents','phone_service','multiple_lines','online_security','online_backup','device_protection', 'tech_support','streaming_tv','streaming_movies','paperless_billing','churn', 'internet_service_type','contract_type','payment_type'])
    return df 


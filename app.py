import pandas as pd
import streamlit as st
import requests
from urllib.request import urlretrieve
from sklearn.linear_model import LinearRegression

api_key = 'V0D76XY4UM8F2714'

# Linear Regression Model for predicting closing price
def predictor(company,test):
    csv_link=f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={company}&apikey={api_key}&datatype=csv'
    filename = f"dataset/{company}.csv"
    urlretrieve(csv_link, filename)
    historical_data = pd.read_csv(filename)
    historical_data = historical_data.drop(columns=['timestamp','volume'])
    features = ['open', 'high', 'low']
    X,y=historical_data[features],historical_data['close']
    model=LinearRegression()
    model.fit(X,y)
    return model.predict(test)

# Getting all companies with their symbol
def getAllCompany():
    company = pd.read_csv('dataset/allCompanies.csv')
    company_abbr=list(company['symbol'])
    company_name=list(company['name'])
    companies=[]
    for i in range(len(company)):
        companies.append((company_abbr[i],company_name[i]))
    return companies


# format for displaying in select box
def format(options):
    return f"{options[1]} ({options[0]})"
    


allCompany=getAllCompany()


# selectbox for selecting company
option = st.selectbox('Company Name',options=allCompany,format_func=format,placeholder='Select a Company',index=None)

# If selected
if(option!=None):
    company_symbol=option[0]
    st.write("<h4>Current values for selected company</h4>",unsafe_allow_html=True)
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={company_symbol}&apikey={api_key}'
    response=requests.get(url)
    data=response.json()['Global Quote']  #getting current info
    open=float(data['02. open'])
    high=float(data['03. high'])
    low=float(data['04. low'])
    test = pd.DataFrame({
    'open': [open],
    'high': [high],
    'low': [low]
    })
    

    display_open=f'<p style="color:white;font-size:20px;display:inline">open: {open}</p>'
    display_high=f'<p style="color:green;font-size:20px;display:inline">high: {high}</p>'
    display_low=f'<p style="color:red;font-size:20px;display:inline">low: {low}</p>'
    width_space='<div style="width:100px;display:inline-block"></div>'
    height_space='<div style="height:50px;display:inline-block"></div>'
    st.write(display_open+width_space+display_high+width_space+display_low,unsafe_allow_html=True)  #diplaying current info
    st.write(height_space,unsafe_allow_html=True)

    #prediction button
    btn=st.button("Predict Today's closing price")
    if btn:
        with st.spinner():
            result=predictor(company_symbol,test)[0]
            st.success(f'Prediction for Today;s closing price: {result}')
            



        
    



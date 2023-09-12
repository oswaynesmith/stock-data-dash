import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title("Stock Data Dashboard")

st.sidebar.header("User Input")

stock_symbol = st.sidebar.text_input("Enter Stock Ticker Symbol", value='AAPL')

start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2022-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2023-01-01'))

def load_stock_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data

data = load_stock_data(stock_symbol, start_date, end_date)


st.subheader("Interactive Stock Price Chart")
fig = px.line(data, x=data.index, y='Adj Close', title=f'{stock_symbol} Stock Price')
st.plotly_chart(fig)



pricing, fundamentals, news = st.tabs(["Pricing Data", "Fundamentals", "Stock News"])

from alpha_vantage.fundamentaldata import FundamentalData

with pricing:
    st.header("Stock Price Movements")
    data2 = data
    data2["%Change"]= data["Adj Close"]/ data["Adj Close"].shift(1) -1
    data2.dropna(inplace=True)
    st.write(data)
    annual_return = data["%Change"].mean()*252*100
    st.write("Annual return is", annual_return, "%")

with fundamentals:
    key = "JUA80ZM1M3F2VD3F"
    fd = FundamentalData(key, output_format = "pandas")
    st.subheader("Balance Sheet")
    balance_sheet = fd.get_balance_sheet_annual(stock_symbol)[0]
    bs = balance_sheet.T[2:]
    bs.columns= list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader("Income Statement")
    income_statement = fd.get_income_statement_annual(stock_symbol)[0]
    is1 = income_statement.T[2:]
    is1.columns= list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader("Cash Flow Statement")
    cash_flow = fd.get_cash_flow_annual(stock_symbol)[0]
    cf = cash_flow.T[2:]
    cf.columns= list(cash_flow.T.iloc[0])
    st.write(cf)

from stocknews import StockNews
with news:
    st.header(f"News of {stock_symbol}")
    sn = StockNews(stock_symbol, save_news=False)
    snews = sn.read_rss()
    for i in range(10):
        st.subheader(f"Story {i+1}")
        st.write(snews['published'][i])
        st.write(snews['title'][i])
        st.write(snews['summary'][i])

import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time
import re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/98.0.4758.102 Safari/537.36", "Referer": "https://finance.sina.com.cn/"}
stock_ids = ["sh600010", "sh600519", "sh601318", "sh601857", "sh600036", "sz000792", "sz002432", "sz002594",
             "sz000723", "sz002104"]
url = "https://hq.sinajs.cn/?format=text&list={}".format(','.join(stock_ids))


def pd_form():
    response = requests.get(url, headers=headers)
    stock_info = response.text.strip().split("\n")
    stock_name = []
    stock_id = []
    for stock in stock_info:
        temp = stock.strip().split(",")
        ans = re.findall(r's.(.*)=(.*)', temp[0])
        Id = ans[0][0]
        name = ans[0][1]
        stock_id.append(Id)
        stock_name.append(name)
    Stock_data = {'Stock_Id': stock_id, 'Stock_Name': stock_name}
    data = pd.DataFrame(Stock_data)
    return data


def get_url(i, dataframe):
    while i <= 320:
        response = requests.get(url, headers=headers)
        dataframe = pd.concat([dataframe, info_process(response)], axis=1)
        i += 1
        time.sleep(3)
    return dataframe


def info_process(response):
    stock_info = response.text.strip().split("\n")
    cur_price = []
    Time = []
    for stock in stock_info:
        temp = stock.strip().split(",")
        cur_price.append(temp[3])
        date = temp[30] + ' ' + temp[31]
        Time.append(date)
    data = {Time[1]: cur_price}
    return pd.DataFrame(data)


def main():
    final = pd.read_excel("data.xlsx", header=None)
    final = pd.DataFrame(final.values.T, columns=final.index)
    final.drop(final.head(3).index, inplace=True)
    final[0] = pd.to_datetime(final[0])  # date转为时间格式
    minute_final = pd_form()
    begin = []
    end = []
    for i in range(1, 16):
        price = []
        Time = "Minute" + ' ' + str(i)
        temp = final[(final[0].dt.minute == 4 + i)]
        if i == 1:
            value = temp.iloc[0, 1:11]
            begin = value.values.tolist()
        elif i == 15:
            value = temp.iloc[-1, 1:11]
            end = value.values.tolist()
        for j in range(1, 11):
            value = temp[j].astype('float').mean()
            price.append(value)
        new_column = {Time: price}
        new_column = pd.DataFrame(new_column)
        minute_final = pd.concat([minute_final, new_column], axis=1)
    rate = []
    for i in range(1, 11):
        rate.append(format(round((float(end[i - 1]) - float(begin[i - 1])) / float(begin[i - 1]), 6), '.4%'))
    new_column = {"Rate": rate}
    new_column = pd.DataFrame(new_column)
    minute_final = pd.concat([minute_final, new_column], axis=1)
    minute_final.to_excel("minute_data.xlsx", index=None)
    print("ok")


def fun_plot(i):
    final = pd.read_excel("data.xlsx", header=None)
    final = pd.DataFrame(final.values.T, columns=final.index)
    final.drop(final.head(3).index, inplace=True)
    for i in range(1, 11):
        value = final.iloc[:, i].values.tolist()
        plt.plot(value)
        plt.savefig("./{}.png".format(i))
        plt.show()
    return


if __name__ == "__main__":
    df = pd_form()
    final = get_url(0, df)
    final.to_excel("data.xlsx")
    # fun_plot(1)
    main()

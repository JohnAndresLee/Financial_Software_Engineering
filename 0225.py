import requests
from bs4 import BeautifulSoup

res = requests.get(url="https://finance.sina.com.cn/china/gncj/2022-02-23/doc-imcwiwss2403820.shtml")
res.encoding = "utf-8"
# print(res)
# print(res.headers)
# print(res.status_code)
# print(res.text)

soup = BeautifulSoup(res.text, features="html.parser")
# print(soup)
# print(type(soup))

# 打印文章标题
title = soup.head.title.string
print(title)

# find & find_all函数
artibody = soup.find(name="div")
artibody2 = soup.find(name="div", attrs={"id": "artibody"})

content = artibody2.find_all(name="p")
print(content)

print("ok")


from email.mime import image
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import img2pdf

#取得集跟頁數

driver = webdriver.Chrome('C:/Users/shitb/OneDrive/Desktop/chromedriver_win32/chromedriver.exe')
url = 'https://www.cartoonmad.com/comic/2504.html'
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'lxml')
table = soup.find('table', {"align":"center","width":"800"})
t = str(table.text).strip().replace(')','').replace('(','').replace(' ','').replace('‧','')
ep = []
pagenum = []
carry = ''

#整理資料，去掉話卷頁
for i in t:
    carry += i
    if i == '話' or i == '卷':
        ep.append(carry)
        carry = ''
    elif i == '頁':
        pagenum.append(carry)
        carry = ''
        
ep_res = []
pagenum_res = []
for j in ep:
    ep_res.append(j.strip().replace('第','').replace('話','').replace('卷',''))
for k in pagenum:
    k = k.strip().replace('頁','')
    if len(k) == 3:
        pagenum_res.append(k)
    else:
        k = '0'+k
        pagenum_res.append(k)

#下載IMG
imgurl = 'https://www.cartoonmad.com/5e585/2504/{}/{}.jpg'
for x in range(len(ep_res)):
    li = []
    for y in range(1,int(pagenum_res[x])+1):
        if len(str(y)) == 3:
            pass
        elif len(str(y)) == 2:
            y = '0'+str(y)
        else:
            y = '00'+str(y)
        res_url = imgurl.format(ep_res[x],y)
        res = requests.get(res_url)
        with open('{}-{}.jpg'.format(ep_res[x],y), 'wb') as f:
            f.write(res.content)
        li.append('{}-{}.jpg'.format(ep_res[x],y))
        
    #迴圈結束打包成PDF
    pdf_obj = img2pdf.convert(li)
    with open('{}.pdf'.format(ep_res[x]), 'wb') as f:
        f.write(pdf_obj)
    
    

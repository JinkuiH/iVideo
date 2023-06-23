'''
Descripttion:
version: 
Author: Kevin
Date: 2023-06-20 21:57:23
LastEditors: Kevin
LastEditTime: 2023-06-23 15:20:07
'''

# 引入必要的库
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import re
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import os
def get_driver():
    return webdriver.Chrome(executable_path='chromedriver')


# 得到登录的cookie
def login_cookie():
    driver = get_driver()    
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)   
    LOGIN_URL = 'https://www.zhihu.com/'
    driver.get(LOGIN_URL)
    time.sleep(5)
    input("请登录后按 Enter")
    cookies = driver.get_cookies()
    jsonCookies = json.dumps(cookies)
    #下面的文件位置需要自己改
    with open('zhihu.txt','w') as f:
        f.write(jsonCookies)
    driver.quit()

# 再次登录
def login():    
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    LOGIN_URL = 'https://www.zhihu.com/'
    driver.get(LOGIN_URL)
    time.sleep(5)
    #下面的文件位置需要自己改，与上面的改动一致
    f = open('zhihu.txt')
    cookies = f.read()
    jsonCookies = json.loads(cookies)
    for co in jsonCookies:
        driver.add_cookie(co)
    driver.refresh()
    time.sleep(5)

# 爬取某问题下的所有答案
def get_answers(question_url):
    driver.get(question_url)
    # number_text = driver.find_element_by_partial_link_text('查看全部').text
    number_text = driver.find_element(By.PARTIAL_LINK_TEXT, '查看全部').text

    number = int(re.search('[0-9]+',number_text).group())
    # driver.find_element_by_partial_link_text('查看全部').click()
    driver.find_element(By.PARTIAL_LINK_TEXT, '查看全部').click()
    time.sleep(1)
    pathtitle = '/html/body/div[1]/div/main/div/div/div[1]/div[2]/div/div[1]/div[1]/h1'
    title = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, pathtitle))).text
    print(title)
    if not os.path.exists(os.path.join('answears', title)):
        os.makedirs(os.path.join('answears', title))
    for k in range(number):
        xpath = '/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div/div/div/div/div[2]/div/div[{}]/div/div/div[2]/span[1]/div/div/span'.format(k+2)
        while True:
            try:
                print(k+2)
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
                answer = element.text
                break
            except  StaleElementReferenceException:
                driver.refresh()
                time.sleep(1)
            except  TimeoutException:
                driver.refresh()
                time.sleep(1)
        print(answer)

        #下面的文件位置需要自己改，保存到你想要的位置
        file = open('answears/{}/answer{}.txt'.format(title,k+1),'w',encoding='utf-8')
        file.write(answer)
        file.close()
        print('answer '+ str(k+1) +' collected!')
        time.sleep(1)
        js="window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js)
        time.sleep(1)

if __name__ == "__main__":
    # 设置你想要搜索的问题
    question_url = 'https://www.zhihu.com/question/587982337/answer/3001751047'
    # login_cookie()
    driver = get_driver() 
    login()
    get_answers(question_url)
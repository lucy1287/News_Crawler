#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install selenium


# In[2]:


import pandas as pd


# In[3]:


from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# In[4]:


pip install lxml


# In[5]:


#selenium 속도 향상을 위한 설정
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.headless = True

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"


# In[6]:


from selenium import webdriver


# In[7]:


pip install webdriver_manager


# In[8]:


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# In[9]:


# Beautiful soup로 했을 때 더보기 버튼 못 찾는 문제 발생
# driver = webdriver.Chrome()
# driver.get('https://www.chosun.com/politics/')
#soup = BeautifulSoup(driver.page_source, 'lxml')
#print(soup)


# In[10]:


#selenium 사용 시 더보기 버튼 찾기 가능
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('lang=ko_KR')
driver = webdriver.Chrome(chrome_options=chrome_options)
    
driver.get('https://www.chosun.com/politics/')

btn = driver.find_element(By.XPATH, '//button[text()="기사 더보기"]')
print(btn)
btn.click()


# In[11]:


import time
from time import sleep


# In[12]:


#정치 기사 탭에서 스크롤, 더보기 버튼 클릭 - selenium 사용
def scroll_plus():
#     더보기 버튼 클릭되어야 하므로 headless 옵션 적용하면 안됨
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('headless')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome()
    
    driver.get('https://www.chosun.com/politics/')
    driver.maximize_window()
    for i in range (110):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(1)
        
        btn = driver.find_element(By.XPATH, '//button[text()="기사 더보기"]')
        btn.click()
    return driver
        


# In[13]:


#실패한 코드(Beautiful Soup으로 하면 html이 그대로 가져와지지 않는 문제 발생)

# def get_news():
#     news_df = pd.DataFrame(columns=("title", "article", "news"))
#     idx = 0
#     links = soup.find_all('div', {'class':'story-card-component story-card__headline-container | text--overflow-ellipsis text--left'})

    
#     for link in links:
#         news_url = link.find('a').get('href')
#         news_url = 'https://www.chosun.com' + news_url
#         print(news_url)
#         news_link = urllib.request.urlopen(news_url).read()
#         news_html = BeautifulSoup(news_link, 'html.parser')
        
#         title = news_html.find('h1').get_text()
#         article = news_html.find('section', {'class' : 'article-body'}).get_text()
#         #article = news_html.find('script', {'id' : 'fusion-metadata'}).get('content')
#         publisher = '조선일보'

#         news_df.loc[idx] = [title, article, publisher]
#         idx += 1
#         print("#", end = "")
#     return news_html


# In[14]:


def get_news():
    driver = scroll_plus()
    news_df = pd.DataFrame(columns=("title", "article", "news"))
    idx = 0
    
    #scropp_plus()가 리턴한 driver에서 Beautiful Soup 사용 -> 기사 링크를 담고 있는 'div'들을 links 배열에 저장
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links = soup.find_all('div', {'class':'story-card-component story-card__headline-container | text--overflow-ellipsis text--left'})
    
    
    #selenium 속도 향상을 위해 headless 옵션 적용
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    for link in links:
        news_url = link.find('a').get('href')
        news_url = 'https://www.chosun.com' + news_url
        if(news_url == '#'):
            continue
        else:
            # 각 링크 열어서 제목, 본문 태그의 내용 가져오기
            driver.get(news_url)
            title = driver.find_element(By.TAG_NAME, 'h1').text
            article = driver.find_element(By.CLASS_NAME, 'article-body').text
            publisher = '조선일보'
            
            #데이터 프레임으로 만들기
            news_df.loc[idx] = [title, article, publisher]
            idx += 1
            print("#", end = "")
    return news_df
    


# In[12]:


get_news().to_csv('chsun1000.csv', encoding='utf-8-sig')


# In[ ]:





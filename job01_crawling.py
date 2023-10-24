from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
# options.add_argument("--no-sandbox")

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

titles = []
total_titles = []
reviews = []
df_titles = pd.DataFrame()

for L in range(0, 3):
    for l in range(1,13):
        time.sleep(0.5)
        if(l < 10):
            section_url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=202{}0{}'.format(L,l)
        else:
            section_url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=202{}{}'.format(L, l)
        url = section_url
        driver.get(url)
        for n in range(1,31):
            try:
                time.sleep(0.5)
                title = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(n)).text
            except:
                print(n)
            if title in total_titles:
                print('중복된 영화입니다.')
            else:
                total_titles.append(title)
                print(title)
                try:
                    button = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(n)) # 영화제목 클릭
                    button.click()
                    time.sleep(0.5)
                    button = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span')  # 평점 클릭
                    button.click()
                    time.sleep(0.5)
                except:
                    print(n)
                for I in range(0, 5):
                    try:
                        time.sleep(1)
                        button = driver.find_element('xpath', '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button') # 폄점 더보기 클릭
                        button.click()
                    except:
                        print('no')
                # for k in range(1, pages[l] + 1):
                for k in range(1, 161):
                    try:
                        review = driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(k)).text
                        review = re.compile('[^가-힣]').sub(' ', review)
                        reviews.append(review)
                        titles.append(title)
                    except:
                        # print('error{} {} {}'.format(l,n,k))
                        pass
                try:
                    driver.get(url)
                except:
                    print('뒤로가기 실패')

                    # if k % 10 == 0:
                    #     df_section_title = pd.DataFrame(titles, columns=['titles'])
                    #     df_section_title['category'] = category[l]
                    #     df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
                    #     df_titles.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(l,k), index=False)
                    #     titles = []

                df_section_title = pd.DataFrame(reviews, columns=['reviews'])
                df_section_title['titles'] = titles
                df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
                df_titles.to_csv('./crawling_data/crawling_data_20212223.csv', index=False)
                titles = []
                reviews = []

#for l in range(0, 6):
for l in range(1,10):
    time.sleep(0.5)
    section_url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=20230{}'.format(l)
    url = section_url
    driver.get(url)
    for n in range(1,31):
        try:
            time.sleep(0.5)
            title = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(n)).text
        except:
            print(n)
        if title in total_titles:
            print('중복된 영화입니다.')
        else:
            try:
                total_titles.append(title)
                print(title)
                button = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(n)) # 영화제목 클릭
                button.click()
                time.sleep(0.5)
                button = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span')  # 평점 클릭
                button.click()
                time.sleep(0.5)
            except:
                print(n)
            for I in range(0, 5):
                try:
                    time.sleep(1)
                    button = driver.find_element('xpath', '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button') # 폄점 더보기 클릭
                    button.click()
                except:
                    print('no')
            # for k in range(1, pages[l] + 1):
            for k in range(1, 161):
                try:
                    review = driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(k)).text
                    review = re.compile('[^가-힣]').sub(' ', review)
                    reviews.append(review)
                    titles.append(title)
                except:
                    # print('error{} {} {}'.format(l,n,k))
                    pass
        try:
            driver.get(url)
        except:
            print('뒤로가기 실패')

            # if k % 10 == 0:
            #     df_section_title = pd.DataFrame(titles, columns=['titles'])
            #     df_section_title['category'] = category[l]
            #     df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
            #     df_titles.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(l,k), index=False)
            #     titles = []

        df_section_title = pd.DataFrame(reviews, columns=['reviews'])
        df_section_title['titles'] = titles
        df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
        df_titles.to_csv('./crawling_data/crawling_data_20212223.csv', index=False)
        titles = []
        reviews = []

print(df_titles.head())
df_titles.info()
print(df_titles['titles'].value_counts())
print(df_titles['reviews'].value_counts())
driver.close()


# Xpath 저장 형태
# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[2]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[5]/dl/dt[2]/a
# //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[4]/li[5]/dl/dt[2]/a

# 파일 합치기
# data1 = pd.read_csv('./crawling_data/crawling_data1.csv')
# data2 = pd.read_csv('./crawling_data/crawling_data_20212223.csv')
# data3 = pd.read_csv('./crawling_data/crawling_data3.csv')
#
# crawling_data_last = pd.concat([data1, data2], ignore_index=True)
# crawling_data_last = pd.concat([crawling_data_last, data3], ignore_index=True)
# crawling_data_last.to_csv('./crawling_data/crawling_data_last.csv')







# //*[@id="mainContent"]/div/div[2]/ol/li[1]/div/div[2]/strong/a    영화 제목
# //*[@id="mainContent"]/div/div[2]/ol/li[2]/div/div[2]/strong/a
# //*[@id="mainContent"]/div/div[2]/ol/li[29]/div/div[2]/strong/a

# //*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span  평점
# //*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span

# //*[@id="alex-area"]/div/div/div/div[3]/div[1]/button 평점 더보기
# //*[@id="alex-area"]/div/div/div/div[3]/div[1]/button
# //*[@id="alex-area"]/div/div/div/div[3]/div[1]/button

# //*[@id="comment915803840"]/div/p 리뷰1
# //*[@id="comment912600643"]/div/p
# //*[@id="comment912043079"]/div/p
# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[1]/div/p
# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[2]/div/p
# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[3]/div/p
# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[13]/div/p
# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[10]/div/p

# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[11]/div/p

# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[11]/div/p

# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[160]/div/p

# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[219]/div/p
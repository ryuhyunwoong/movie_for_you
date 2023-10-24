from selenium import webdriver              # 웹사이트(및 웹 애플리케이션)의 유효성 검사에 사용되는 자동화 테스트 프레임워크
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time
import datetime

url = 'https://movie.daum.net/ranking/boxoffice/monthly'
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_argument('lang=ko_KR')

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executble_path=ChromeDriverManager().install())
# 크롬 드라이버
driver = webdriver.Chrome(service=service, options=options)

titles = []
total_titles = []
reviews = []
# year = ['2014', '2015', '2016']
# month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
df_titles = pd.DataFrame()

for L in range(6, 7):
    for l in range(1,13):
        if(l < 10):
            section_url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=201{}0{}'.format(L,l)
        else:
            section_url = ('https://movie.daum.net/ranking/boxoffice/monthly?date=201'
                           ''
                           ''
                           ''
                           '{}{}').format(L, l)
        url = section_url
        driver.get(url)

        for n in range(1, 31):
            try:
                time.sleep(0.1)
                title = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(n)).text
            except:
                print(n)
            if title in total_titles:
                print('중복된 영화입니다.')
            else:
                total_titles.append(title)
                print(title)
                try:
                    button = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(n))  # 영화제목 클릭
                    button.click()
                    time.sleep(0.5)
                    button = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span')  # 평점 클릭
                    button.click()
                    time.sleep(0.5)
                except:
                    print(n)
                for I in range(0, 5):
                    try:
                        time.sleep(1)
                        button = driver.find_element('xpath', '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button')  # 폄점 더보기 클릭
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
                        print('error{} {} {}'.format(l, n, k))
                try:
                    driver.back()
                    time.sleep(0.5)
                    driver.back()
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
                df_titles.to_csv('./crawling_data/crawling_data_{}.csv', index=False)
                df_titles.to_csv('./crawling_data/movie_data_16_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
                titles = []
                reviews = []

    print(df_titles.head())
    df_titles.info()
    print(df_titles['titles'].value_counts())
    print(df_titles['reviews'].value_counts())
    driver.close()

    ############내코드#################
    # for i in range(len(year)):
    #     # 월간차트 연월 변경
    #     section_url = 'https://movie.daum.net/ranking/boxoffice/monthly'
    #
    #     for j in range(len(month)):
    #         url = section_url + '?date={}'.format(year[i] + month[j])  ##2014년-2016년까지 반복'.format(j)  # 페이지 변경 1월-12월까지 반복
    #         driver.get(url)
    #         print('연월변경')
    #         time.sleep(1)
    #     for k in range(1, 31):  ##월순위별 영화클릭 한페이지에 30개
    #         xpath_temp = '/html/body/div[2]/main/article/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(k)
    #         driver.find_element('xpath', xpath_temp).click()  # 클릭 시 사이트로 이동
    #         print('영화페이지')
    #         time.sleep(1)  # 클릭 후 사이트로 이동할 대기 시간 부여
    #
    #         ## 영화제목 크롤링
    #         title = '//*[@id="mainContent"]/div/div[1]/div[2]/div[1]/h3/span[1]'
    #         name = driver.find_element('xpath', title).text
    #         name = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', name)
    #         titles.append(title)
    #         print(name)
    #         time.sleep(0.1)
    #
    #         rating = '/html/body/div[2]/main/article/div/div[2]/div[1]/ul/li[4]/a/span'
    #         driver.find_element('xpath', rating).click()  # 클릭하기
    #         print('평점 버튼')
    #         time.sleep(0.5)
    #
    #
    #         for l in range(5):    ##리뷰더보기 5번클릭
    #             botton = '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button'
    #             driver.find_element('xpath', botton).click()
    #             print('더보기')
    #             time.sleep(0.5)
    #
    #         ## 리뷰 크롤링 부분
    #         for r in range(1, 161):
    #             # title_review = driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(r)).text
    #             # title_review = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', title_review)
    #             # titles.append(title_review)
    #             # print(title_review)
    #             # time.sleep(2)
    #             # try:
    #                 review = driver.find_element('xpath','/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(r)).text
    #                 review = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', review)
    #                 reviews.append(review)
    #                 titles.append(title)
    #
    #             # except:
    #                 print('error{} {}'.format(k, r))
    #
    #
    #
    #         driver.back()
    #         driver.back()
    #
    #
    #
    #     if i % 12 == 0:
    #         df_section_title = pd.DataFrame(reviews, columns=['reviews'])
    #         df_section_title['titles'] = titles
    #         df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
    #         df_titles.to_csv('./crawling_data/movie_data_{}_{}.csv'.format(i, j), index=False)
    #         titles = []
    #
    # df_section_title = pd.DataFrame(reviews, columns=['reviews'])
    # df_section_title['titles'] = titles
    # df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
    # df_titles.to_csv('./crawling_data/movie_data.csv', index=False)
    #

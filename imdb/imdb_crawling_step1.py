# IMDB의 영화 id 값을 수집한다.

import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


def crawling(start_year, last_year, movie_num):
    for k in range(start_year, last_year+1):
        print("year : " + str(k))

        title_list = []
        imdb_movie_id_list = []

        res = requests.get("https://www.imdb.com/search/title/?title_type=feature&year=2020")
        soup = BeautifulSoup(res.content, 'html.parser')

        if movie_num == "all":
            movie_num = soup.find('div', {'class': 'desc'})
            movie_num = movie_num.find("span").text
            movie_num = re.sub('1.*of', '', movie_num)
            movie_num = re.sub('ti.*', '', movie_num)
            movie_num = re.sub(',', '', movie_num)
            movie_num = int(movie_num.strip())

        for i in range(1, movie_num, 50):
            print("movie_num : " + str(i/movie_num))
            res = requests.get('https://www.imdb.com/search/title/?title_type=feature&year='+str(k)+'-01-01,'+str(k)+'-12-31&start='+str(i)+'&ref_=adv_nxt')
            soup = BeautifulSoup(res.content, 'html.parser')

            header_list = soup.find_all('div', {'class': 'lister-item-content'})

            for j in range(0, len(header_list)):
                try:
                    title = header_list[j].find('a').text.strip()
                    imdb_movie_id = header_list[j].find('a')['href'].strip()

                except:
                    continue

                imdb_movie_id = re.sub('/title/', '', imdb_movie_id)
                imdb_movie_id = re.sub('/', '', imdb_movie_id)

                title_list.append(title)
                imdb_movie_id_list.append(imdb_movie_id)

        df_title = pd.DataFrame(title_list)
        df_imdb_movie_id = pd.DataFrame(imdb_movie_id_list)

        total = pd.concat([df_title, df_imdb_movie_id], axis=1)
        total.columns = ["title", "imdb_movie_id"]

        total.to_csv("imdb_list_"+str(k)+".csv", index=False)


def main():
    start_year = 2019
    last_year = 2020
    movie_num = "100"   # 수집하고 싶은 영화의 개수를 입력. 만약 모두 수집하고 싶으면 all로 설정한다.

    crawling(start_year, last_year, movie_num)


if __name__ == '__main__':
    main()



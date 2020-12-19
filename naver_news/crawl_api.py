import pandas as pd
import requests

client_id = "#네이버 검색 API ID 값"
client_secret = "#네이버 검색 API 비밀번호 값"



search_word = '코로나'
encode_type = 'json'
sort = 'date'

for i in range(0, 3):
    start = (100*i) + 1
    end = 100 * (i+1)

    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(100)}&start={str(int(start))}&sort={sort}"

    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

    r = requests.get(url, headers=headers)
    pd_news = pd.DataFrame(r.json()['items'])
    pd_news.to_csv('naver_news_api_'+str(end)+'.csv', index=False)
    print(end)

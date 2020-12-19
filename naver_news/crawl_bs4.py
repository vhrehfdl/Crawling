import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_news(news_url):
    news_detail = []

    innerRaw = requests.get(news_url, headers={'User-Agent': 'Mozilla/5.0'})
    innerSoup = BeautifulSoup(innerRaw.content, 'html.parser')

    date = innerSoup.find('span', {'class': 't11'}).text
    date = date[0:10]

    title = innerSoup.find('h3', {'id': 'articleTitle'}).text

    text = innerSoup.select('#articleBodyContents')[0].get_text().replace('\n', " ")
    text = text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")
    news_detail.append(text.strip())
    news_detail.append(news_url)

    content = " ".join(news_detail)

    return date, title, content


def crawling(keyword, start_year, end_year, start_month, end_month):
    for year in range(start_year, end_year+1):
        for month in range(start_month, end_month+1):
            title_list = []
            press_list = []
            date_list = []
            url_list = []
            content_list = []

            if month < 10:
                month = "0"+str(month)

            seed_url = 'https://search.naver.com/search.naver?&where=news&query=' + keyword + '&sort=0&ds='+str(year)+'.'+str(month)+'.01&de='+str(year)+'.'+str(month)+'.31&docid=&nso=so:da,p:from'+str(year)+''+str(month)+'01to'+str(year)+''+str(month)+'31,a:all'
            for i in range(0, 400):
                print(i, 400)
                url = seed_url + '&start=' + str(i * 10 + 1)

                raw = requests.get(url)
                soup = BeautifulSoup(raw.content, 'html.parser')

                news_list = soup.find_all('div', {'class': 'info_group'})
                for news_element in news_list:
                    info = news_element.find_all('a', {'class': 'info'})
                    if len(info) == 2:
                        press = info[0].text
                        naver_news_url = info[1]["href"]

                        try:
                            date, title, content = get_news(naver_news_url)

                            title_list.append(title)
                            press_list.append(press)
                            url_list.append(naver_news_url)
                            date_list.append(date)
                            content_list.append(content)
                        except:
                            print(naver_news_url)
                            pass

            df_title = pd.DataFrame(title_list)
            df_press = pd.DataFrame(press_list)
            df_date = pd.DataFrame(date_list)
            df_url = pd.DataFrame(url_list)
            df_content = pd.DataFrame(content_list)

            total = pd.concat([df_title, df_press, df_date, df_url, df_content], axis=1)
            total.columns = ["title", "press", "date", "url", "content"]
            total.to_csv("naver_news_bs4_"+str(month)+".csv", index=False)


def main():
    keyword = "트럼프"
    start_year, end_year = 2020, 2020
    start_month, end_month = 1, 2

    crawling(keyword, start_year, end_year, start_month, end_month)


if __name__ == '__main__':
    main()
# step1에서 수집한 imdb 영화 ID갑을 활용해 세부 데이터를 수집한다.

import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


def crawling(input_dir):
    df_total = pd.read_csv(input_dir)

    title_list, imdb_movie_list, release_year_list = df_total["title"].tolist(), df_total["imdb_movie_id"].tolist(),  []
    storyline_list, plot_keyword_list, genre_list, character_list = [], [], [], []
    director_list, actor_list, certificate_list, release_date_list, runtime_list = [], [], [], [], []
    budget_list, opening_weekend_use_list, gross_usa_list, cumulative_gross_list = [], [], [], []
    metascore_list, reviews_list, imdb_popularity_list, imdb_rating_list = [], [], [], []


    for i in range(0, len(imdb_movie_list)):
        print("Pregress : ", i, len(imdb_movie_list))

        res = requests.get('https://www.imdb.com/title/'+str(imdb_movie_list[i]))
        soup = BeautifulSoup(res.content, 'html.parser')

        # Release Year 수집.
        try:
            release_year = soup.find('span', {'id': 'titleYear'})
            release_year = release_year.find('a').text

            release_year_list.append(release_year)

        except:
            release_year_list.append(None)


        # StoryLine 수집.
        try:
            storyline = soup.find('div', {'id': 'titleStoryLine'})
            storyline = storyline.find('p')
            storyline = storyline.find('span').text.strip()

            storyline_list.append(storyline)

        except:
            storyline_list.append(None)


        # Plot Keywords 수집.
        try:
            res_keyword_list = requests.get('https://www.imdb.com/title/' + str(imdb_movie_list[i]) + "/keywords")
            soup_keyword_list = BeautifulSoup(res_keyword_list.content, 'html.parser')

            storyline = soup_keyword_list.find('table', {'class': 'dataTable evenWidthTable2Col'})
            keyword_list = storyline.find_all('div', {'class': 'sodatext'})

            keyword_sentence = ""
            for keyword in keyword_list:
                keyword = keyword.find('a').text
                keyword_sentence += keyword + ","

            plot_keyword_list.append(keyword_sentence[:-1])

        except:
            plot_keyword_list.append(None)


        # Genres 수집.
        try:
            total_list = soup.find_all('div', {'class': 'see-more inline canwrap'})

            genre_sentence = ""
            for element in total_list:
                if "Genres" in str(element):
                    genres_all = element.find_all('a')
                    for genres in genres_all:
                        genres = re.sub('<.+?>', '', str(genres)).strip()
                        genre_sentence += genres + ","

            genre_list.append(genre_sentence[:-1])

        except:
            genre_list.append(None)


        # Character Name 수집.
        try:
            cast_list = soup.find('table', {'class': 'cast_list'})
            cast_list = cast_list.find_all('td', {'class': 'character'})

            character_sentence = ""
            for character in cast_list:
                try:
                    character = re.sub('<.+?>', '', str(character)).strip()
                    character = re.sub('\n', '', str(character)).strip()
                    character_sentence += character + ","
                except:
                    continue

            character_list.append(character_sentence[:-1])

        except:
            character_list.append(None)


        # Director 수집.
        try:
            director = soup.find('div', {'class': 'credit_summary_item'})
            director = director.find('a').text
            director_list.append(director)

        except:
            director_list.append(None)


        # Actor Name 수집.
        try:
            cast_list = soup.find('table', {'class': 'cast_list'})
            cast_list = cast_list.find_all('tr')

            actor_name_sentence = ""
            del cast_list[0]
            for cast in cast_list:
                try:
                    actor = cast.find('a')
                    actor = actor.find('img')["title"]
                    actor_name_sentence += actor + ","

                except:
                    continue

            actor_list.append(actor_name_sentence[:-1])

        except:
            actor_list.append(None)


        # Certificate 수집.
        try:
            total_list = soup.find_all('div', {'class': 'txt-block'})

            for element in total_list:
                if "Certificate" in str(element):
                    certificate = element.find('span').text.strip()

            certificate_list.append(certificate)

        except:
            certificate_list.append(None)


        # Release Date 수집.
        release_date = ""
        try:
            total_box = soup.find('div', {'id': 'titleDetails'})
            total_box = total_box.find_all('div', {'class': 'txt-block'})

            for detail in total_box:
                try:
                    detail_name = detail.find('h4', {'class': 'inline'}).text

                    if detail_name == "Release Date:":
                        detail = re.sub('<.+?>', '', str(detail))
                        release_date = re.sub('Release Date:', '', str(detail)).strip()
                        release_date = re.sub('See more »', '', str(release_date)).strip()

                except:
                    continue

        except:
            release_date = ""

        release_date_list.append(release_date)


        # Runtime 수집.
        runtime = ""
        try:
            total_box = soup.find('div', {'id': 'titleDetails'})
            total_box = total_box.find_all('div', {'class': 'txt-block'})

            for detail in total_box:
                try:
                    detail_name = detail.find('h4', {'class': 'inline'}).text

                    if detail_name == "Runtime:":
                        detail = re.sub('<.+?>', '', str(detail))
                        runtime = re.sub('Runtime:', '', str(detail)).strip()
                        runtime = re.sub('\n', '', str(runtime)).strip()
                        runtime = re.sub(',', '', str(runtime)).strip()
                        runtime = re.sub('\$', '', str(runtime)).strip()

                except:
                    continue

        except:
            runtime = ""

        runtime_list.append(runtime)

        "------------------------------------------------------------------------------------------------------------------"

        # Budget 수집.
        budget = ""
        try:
            total_box = soup.find('div', {'id': 'titleDetails'})
            total_box = total_box.find_all('div', {'class': 'txt-block'})

            for detail in total_box:
                try:
                    detail_name = detail.find('h4', {'class': 'inline'}).text

                    if detail_name == "Budget:":
                        detail = re.sub('<.+?>', '', str(detail))
                        budget = re.sub('Budget:', '', str(detail)).strip()
                        budget = re.sub('\n', '', str(budget)).strip()
                        budget = re.sub(',', '', str(budget)).strip()
                        budget = re.sub('\$', '', str(budget)).strip()

                except:
                    continue

        except:
            budget = ""

        budget_list.append(budget)


        # Opening Weekend USA 수집.
        weekend_usa = ""
        try:
            total_box = soup.find('div', {'id': 'titleDetails'})
            total_box = total_box.find_all('div', {'class': 'txt-block'})

            for detail in total_box:
                try:
                    detail_name = detail.find('h4', {'class': 'inline'}).text

                    if detail_name == "Opening Weekend USA:":
                        detail = re.sub('<.+?>', '', str(detail))
                        weekend_usa = re.sub('Opening Weekend USA:', '', str(detail)).strip()
                        weekend_usa = re.sub('\n', '', str(weekend_usa)).strip()
                        weekend_usa = re.sub(',', '', str(weekend_usa)).strip()
                        weekend_usa = re.sub('\$', '', str(weekend_usa)).strip()

                except:
                    continue

        except:
            weekend_usa = ""

        opening_weekend_use_list.append(weekend_usa)


        # Gross USA 수집.
        gross_usa = ""
        try:
            total_box = soup.find('div', {'id': 'titleDetails'})
            total_box = total_box.find_all('div', {'class': 'txt-block'})

            for detail in total_box:
                try:
                    detail_name = detail.find('h4', {'class': 'inline'}).text

                    if detail_name == "Gross USA:":
                        detail = re.sub('<.+?>', '', str(detail))
                        gross_usa = re.sub('Gross USA:', '', str(detail)).strip()
                        gross_usa = re.sub('\n', '', str(gross_usa)).strip()
                        gross_usa = re.sub(',', '', str(gross_usa)).strip()
                        gross_usa = re.sub('\$', '', str(gross_usa)).strip()

                except:
                    continue

        except:
            gross_usa = ""

        gross_usa_list.append(gross_usa)


        # Cumulative Gross 수집.
        cumulative_gross = ""
        try:
            total_box = soup.find('div', {'id': 'titleDetails'})
            total_box = total_box.find_all('div', {'class': 'txt-block'})

            for detail in total_box:
                try:
                    detail_name = detail.find('h4', {'class': 'inline'}).text

                    if detail_name == "Cumulative Worldwide Gross:":
                        detail = re.sub('<.+?>', '', str(detail))
                        cumulative_gross = re.sub('Cumulative Worldwide Gross:', '', str(detail)).strip()
                        cumulative_gross = re.sub('\n', '', str(cumulative_gross)).strip()
                        cumulative_gross = re.sub(',', '', str(cumulative_gross)).strip()
                        cumulative_gross = re.sub('\$', '', str(cumulative_gross)).strip()

                except:
                    continue

        except:
            cumulative_gross = ""

        cumulative_gross_list.append(cumulative_gross)

        "------------------------------------------------------------------------------------------------------------------"

        # Metascore 수집.
        try:
            metascore = soup.find_all('div', {'class': 'titleReviewBarItem'})[0]
            metascore = metascore.find('span').text.strip()
            metascore_list.append(metascore)

        except:
            metascore_list.append(None)


        # reviews_num 수집.
        try:
            reviews_num = soup.find_all('div', {'class': 'titleReviewBarItem'})[1]
            reviews_num = reviews_num.find('span', {'class': 'subText'}).text.strip()
            reviews_num = re.sub('\n', '', str(reviews_num)).strip()
            reviews_list.append(reviews_num)

        except:
            reviews_list.append(None)


        # imdb_popularity 수집.
        try:
            imdb_popularity = soup.find_all('div', {'class': 'titleReviewBarItem'})[2]
            imdb_popularity = imdb_popularity.find('span', {'class': 'subText'}).text.strip()
            imdb_popularity = re.sub('\n', '', str(imdb_popularity)).strip()
            imdb_popularity_list.append(imdb_popularity)

        except:
            imdb_popularity_list.append(None)


        # imdb_rating 수집.
        try:
            imdb_rating = soup.find('div', {'class': 'ratingValue'})
            imdb_rating = imdb_rating.find('span', {'itemprop': 'ratingValue'}).text.strip()
            imdb_rating_list.append(imdb_rating)

        except:
            imdb_rating_list.append(None)


    df_title, df_imdb_id, df_release_year = pd.DataFrame(title_list), pd.DataFrame(imdb_movie_list), pd.DataFrame(release_year_list)
    df_storyline, df_plot_keyword, df_genre, df_character = pd.DataFrame(storyline_list), pd.DataFrame(plot_keyword_list), pd.DataFrame(genre_list), pd.DataFrame(character_list)
    df_director, df_actor, df_certificate, df_release_date, df_runtime = pd.DataFrame(director_list), pd.DataFrame(actor_list), pd.DataFrame(certificate_list), pd.DataFrame(release_date_list), pd.DataFrame(runtime_list)
    df_budget, df_opening_weekend, df_gross, df_cumulative_gross = pd.DataFrame(budget_list), pd.DataFrame(opening_weekend_use_list), pd.DataFrame(gross_usa_list), pd.DataFrame(cumulative_gross_list)
    df_metascore, df_reviews, df_popularity, df_imdb_rating = pd.DataFrame(metascore_list), pd.DataFrame(reviews_list), pd.DataFrame(imdb_popularity_list), pd.DataFrame(imdb_rating_list)

    total = pd.concat([df_title, df_imdb_id, df_release_year, df_storyline, df_plot_keyword, df_genre, df_character, df_director, df_actor, df_certificate, df_release_date, df_runtime, df_budget, df_opening_weekend, df_gross, df_cumulative_gross, df_metascore, df_reviews, df_popularity, df_imdb_rating], axis=1)
    total.columns = ["title", "IMDB_movie_id", "release_year", "storyline", "plot_keywords", "genre", "character_name", "director", "actor", "certificate", "release_date", "runtime", "budget", "opening_gross", "gross_usa", "cumulative_worldwide_gross", "metascore", "reviews", "IMDB_popularity", "IMDB_rating"]
    total.to_csv("../Data/imdb_total.csv", index=False)


def main():
    input_dir = "imdb_list_2019.csv"
    crawling(input_dir)


if __name__ == '__main__':
    main()



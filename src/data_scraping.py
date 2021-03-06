import json
import os
import urllib.request
from enum import Enum

import requests
from bs4 import BeautifulSoup


class Platform(Enum):
    PC = 'pc'
    Switch = 'switch'
    PS4 = 'playstation-4'
    PS5 = 'playstation-5'
    XboxOne = 'xbox-one'
    XboxSeries = 'xbox-series-x'


class Game(object):
    def __init__(self, score, name, platform, date):
        self.score = score
        self.name = name
        self.platform = platform
        self.date = date
        self.url = ''

    def __str__(self):
        return self.name + ' ' + self.platform + ' ' + self.date + ' ' + self.score

    def get_string_without_platform(self):
        return self.score + ", " + self.name

    def get_string_without_date(self):
        return self.get_string_without_platform() + ", " + self.platform

    def get_string(self):
        return self.get_string_without_date() + ", Date: " + self.date


def get_response(url):
    user_agent = {'User-Agent': 'Chrome/94.0.4606.71'}
    response = requests.get(url, headers=user_agent)
    return response


def get_top_5_by_year(year, text=None):
    if text is None:
        if year < 1916 or year > 2021:
            raise ValueError('Invalid year. Must be between 1916 and 2021. Received year: ' + str(year))
        basic_url = "https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected=%s&distribution=&sort=desc&view=detailed"
        text = get_response(basic_url % str(year)).text
    html_soup = BeautifulSoup(text, 'html.parser')
    games_container = html_soup.find_all('td', class_='clamp-summary-wrap')[:5]
    result = []
    for i in range(len(games_container)):
        score = games_container[i].a.div.text
        name = games_container[i].find('a', class_='title').h3.text
        platform = games_container[i].find('div', class_='platform').find('span', class_='data').text.strip()
        date = games_container[i].find('div', class_='clamp-details').findAll('span')[2].text
        result.append(Game(score, name, platform, date))
    return result


def get_top_50_for_decade(text=None):
    if text is None:
        url = "https://www.metacritic.com/feature/best-videogames-of-the-decade-2010s"
        text = get_response(url).text
    html_soup = BeautifulSoup(text, 'html.parser')
    games_container = html_soup.find('table', class_='bordertable')
    games_container = games_container.table.tbody.find_all('tr')
    result = []
    for i in range(len(games_container)):
        game_number = games_container[i].td.text
        game = games_container[i].text
        year = game[game.rfind(',') + 1:game.rfind(')')].strip()
        score = game[game.rfind(')') + 1:]
        platform = game[game.rfind('(') + 1:game.rfind(',')]
        game = game.replace(game_number, "")
        name = game[:game.rfind('(')].strip()
        result.append(Game(score, name, platform, year))
    return result


def get_top_10_by_platform(platform: Platform, text=None):
    if text is None:
        basic_url = 'https://www.metacritic.com/game/'
        basic_url += platform.value
        text = get_response(basic_url).text
    html_soup = BeautifulSoup(text, 'html.parser')
    games_container = html_soup.find('table', class_='clamp-list')
    games_container = games_container.find_all('td', class_='clamp-summary-wrap')
    result = []
    for i in range(len(games_container)):
        score = games_container[i].a.div.text
        name = games_container[i].h3.text.strip()
        year = games_container[i].find_all('div', class_='clamp-details')[1].span.text
        result.append(Game(score, name, platform.value, year))
    return result


''' Query is a string as it was typed in chat-bot input, with whitespaces, lower/upper cases etc.'''


def get_result_of_query(query: str):
    result = []

    if query == "":
        return result
        # raise ValueError("Empty string")

    if query.startswith('/'):
        return result

    search_url = "https://www.metacritic.com/search/game/{}/results"
    words = query.split()

    query_word_delimiter = "%20"
    query_url_style = ""
    for word in words:
        query_url_style += word + query_word_delimiter
    query_url_style = query_url_style[:-3]
    search_url = search_url.format(query_url_style)
    response = get_response(search_url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    if html_soup.find('div', class_='body').p.text.strip() == 'No search results found.':
        return result
        # raise ValueError("No search results")

    pages_container = html_soup.find('ul', class_='pages')
    games_container = []
    if pages_container is None:
        response = get_response(search_url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        games_container.append(html_soup.find('ul', class_='search_results module'))
    else:
        for i in range(len(pages_container)):
            response = get_response(search_url + '?page=' + str(i))
            html_soup = BeautifulSoup(response.text, 'html.parser')
            games_container.append(html_soup.find('ul', class_='search_results module'))

    for games in games_container:
        games_container_local = games.find_all('li')
        for game in games_container_local:
            name = game.a.text.strip()
            score = game.span.text.strip()
            platform = game.p.span.text.strip()
            year = game.p.text.split()[2:]
            url = game.find('div', class_='main_stats').h3.a
            url = url.attrs['href']
            if len(year) == 1 and year[0] == 'TBA':
                continue

            if len(year) == 2:
                year = year[0] + ' ' + year[1]
            else:
                year = year[0]

            TBA_symbol = game.p.text.split()[-2]
            if TBA_symbol != 'TBA' and year != 'TBA':
                if platform == 'PC':
                    result.append(Game(score, name, 'pc', year))
                    result[-1].url = url
                if platform == 'XONE':
                    result.append(Game(score, name, 'xbox-one', year))
                    result[-1].url = url
                if platform == 'PS4':
                    result.append(Game(score, name, 'playstation-4', year))
                    result[-1].url = url
                if platform == 'PS5':
                    result.append(Game(score, name, 'playstation-5', year))
                    result[-1].url = url
                if platform == 'Switch':
                    result.append(Game(score, name, 'switch', year))
                    result[-1].url = url
                if platform == 'XBSX':
                    result.append(Game(score, name, 'xbox-series-x', year))
                    result[-1].url = url

    return result


def get_description_score_details_by_game(game: Game):
    if game.url == '':
        return ''

    url = 'https://www.metacritic.com' + game.url
    response = get_response(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    res = html_soup.find('div', class_='section product_details')
    res1 = res.find('div', class_='details side_details').ul
    desc_container = res1.text
    desc_container = os.linesep.join([s for s in desc_container.splitlines() if s])
    desc_container = desc_container.splitlines()
    desc_text = ''
    for i in range(len(desc_container) - 1):
        if ':' in desc_container[i]:
            if desc_text != '':
                desc_text += '\n'
            desc_text += " ".join(desc_container[i].split()).strip()
        else:
            desc_text += ' ' + " ".join(desc_container[i].split()).strip()

    temp = html_soup.find('div', class_='userscore_wrap feature_userscore')
    if temp is not None:
        user_score = temp.a.div.text.strip()
        user_reviews = temp.p.a.text.strip().split()[0]
        critic_reviews = html_soup.find('div', class_='score_summary metascore_summary')
        critic_reviews = critic_reviews.find('div', class_='summary').p.a.span.text.strip()
    else:
        user_score = -1
        user_reviews = -1
        critic_reviews = -1

    return desc_text, user_score, user_reviews, critic_reviews


def get_game_image(game: Game):
    if game.url == '':
        return 0

    print(game.name + ' ' + game.platform)
    url = 'https://www.metacritic.com' + game.url
    response = get_response(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    res = html_soup.find('div', class_='product_image large_image must_play')
    all_images = [img["src"] for img in res.find_all('img', {'class': 'product_image large_image'})]
    image_url = all_images[0]
    print('???????????? ???? ???????????????? ?? metacritic: ')
    print(image_url)

    download_image(image_url, 'images/', 'game_metacritic_icon')

    file_path = 'images/game_metacritic_icon.jpg'
    search_url = 'https://yandex.ru/images/search'
    files = {'upfile': ('blob', open(file_path, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(search_url, params=params, files=files)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = search_url + '?' + query_string
    print('???????????? ???? ???????????????? ???????????? ?? Yandex: ')
    print(img_search_url)

    soup = BeautifulSoup(requests.get(img_search_url).text, 'html.parser')
    similar = soup.find_all('div', class_='CbirSimilar-Thumb')
    img_tag = similar[0].find('a').get('href')

    img_url = 'https://yandex.ru' + img_tag
    print('???????????? ???? ???????????? ?? ???????????? ????????????????:')
    print(img_url)

    s = BeautifulSoup(requests.get(img_url).text, 'html.parser')

    try:
        # print('here 1')
        resp2 = s.find('div', class_='serp-item serp-item_type_search serp-item_group_search serp-item_pos_0 '
                                     'serp-item_selected_yes serp-item_scale_yes justifier__item i-bem').get_attribute_list(
            'data-bem')
    except Exception as e:
        # print('here 2')
        resp2 = s.find('div', class_='serp-item serp-item_type_search serp-item_group_search serp-item_pos_0 '
                                     'serp-item_scale_yes justifier__item i-bem').get_attribute_list(
            'data-bem')

    final_url = json.loads(resp2[0])['serp-item']['preview'][0]['url']
    print('???????????????? ???????????? ???? ????????????????: ')
    print(final_url)

    is_downloaded = download_image(final_url, 'images/', 'game_image')

    # ???????? ???????? ?????????????????? ??????????????????, ?????????? ???????????????? ?? metacritic
    if not is_downloaded:
        with open('images/game_metacritic_icon.jpg', 'rb') as image:
            copy = image.read()
        with open('images/game_image.jpg', 'wb') as file:
            file.write(copy)


def download_image(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    try:
        urllib.request.urlretrieve(url, full_path)
        return True
    except Exception as e:
        return False


def get_top_string(year=None):
    if year is not None:
        top___by_year = get_top_5_by_year(year)
        out_text = ''
        for game in top___by_year[:5]:
            out_text += game.get_string_without_date() + "\n"
    else:
        top___by_year_decade = get_top_50_for_decade()
        out_text = ''
        for game in top___by_year_decade[:10]:
            out_text += game.get_string_without_date() + "\n"
    return out_text


def get_top_platform_string(platform: Platform):
    top_by_platform = get_top_10_by_platform(platform)
    out_text = ''
    for game in top_by_platform[:10]:
        out_text += game.get_string_without_platform() + "\n"
    return out_text

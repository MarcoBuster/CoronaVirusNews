from bs4 import BeautifulSoup
import requests
from pprint import pprint


BASE_URL = 'https://www.worldometers.info/coronavirus/'


def _sanitize_text(string: str):
    return int(string.lstrip().rstrip().replace(',', ''))


def scrape():
    print('Getting the URL...')
    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    print('Scraping...')

    res = dict()
    big_counters = soup.findAll('div', {'class': 'maincounter-number'})
    res['total_cases'] = _sanitize_text(big_counters[0].text)
    res['deaths'] = _sanitize_text(big_counters[1].text)
    res['recovered'] = _sanitize_text(big_counters[2].text)

    small_counters = soup.findAll('span', {'class': 'number-table'})
    res['mild_condition'] = _sanitize_text(small_counters[0].text)
    res['critical_condition'] = _sanitize_text(small_counters[1].text)

    res['news'] = list()
    raw_latest_news = soup.findAll('ul')[5].findAll('li')
    for news in raw_latest_news:
        news_text = ''
        for child in news.children:
            if child.name == "strong":
                news_text += f"<b>{child.text}</b>"
            elif child.name in ["i", "u", "code", "pre"]:
                news_text += str(child)
            else:
                try:
                    news_text += child.text
                except AttributeError:
                    news_text += str(child)
        res['news'].append(news_text)
    return res


if __name__ == "__main__":
    pprint(scrape())

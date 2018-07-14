import requests
from bs4 import BeautifulSoup
import json


def google(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=' + q + '&ie=utf-8&oe=utf-8'
    print(url)
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    output = []
    for searchWrapper in soup.find_all('h3'):
        url = searchWrapper.find('a')["href"]
        text = searchWrapper.find('a').text.strip()
        result = {'text': text, 'url': url}
        output.append(result)
    return output


def add_links_to_articles():
    with open("articles_pages.json") as i_file:
        articles_pages = json.load(i_file)
    for i in range(len(articles_pages)):
        with open("ReferencesText/" + articles_pages[i][29:] + ".json") as f:
            bibliography = json.load(f)
        for j in range(1, len(bibliography) + 1):
            print(google(bibliography[str(j)]))


def main():
    add_links_to_articles()


if __name__ == "__main__":
    main()

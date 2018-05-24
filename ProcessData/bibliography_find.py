import requests
from bs4 import BeautifulSoup
import json
import os
import scholarly

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
        new_dict = {}
        with open("ReferencesText/" + articles_pages[i][29:] + ".json") as f:
            bibliography = json.load(f)
        # print(bibliography)
        for j in range(1, len(bibliography) + 1):
            # print(bibliography[str(j)])
            print(google(bibliography[str(j)]))
            # new_dict[j] = (bibliography[j], google(bibliography[j])[0]['url'])
            break
        # print(new_dict)
        break

def main():
    print(google("monkey"))

if __name__ == "__main__":
    main()
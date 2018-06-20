import requests
from bs4 import BeautifulSoup
import json


def google(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.de/search?q=' + q + '&sourceid=chrome&ie=UTF-8'
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    output = []
    cnt = 0
    for searchWrapper in soup.find_all('h3'):
        cnt += 1
        try:
            url = searchWrapper.find('a')["href"]
            text = searchWrapper.find('a').text.strip()
        except:
            break
        result = {'text': text, 'url': url}
        output.append(result)
        if cnt == 2:
            break
    return output


def add_links_to_articles():
    with open("articles_pages.json") as i_file:
        articles_pages = json.load(i_file)
    for i in range(len(articles_pages)):
        try:
            f = open("BibliographySearchResults/" + articles_pages[i][29:] + ".json")
            f.close()
            continue
        except:
            google_bibliography = {}
        with open("ReferencesText/" + articles_pages[i][29:] + ".json") as f:
            bibliography = json.load(f)
        for j in bibliography:
            res = google(bibliography[j])
            print(res)
            google_bibliography[bibliography[j]] = res
        with open("BibliographySearchResults/" + articles_pages[i][29:] + ".json", 'w') as f:
            json.dump(google_bibliography, f)


def main():
    add_links_to_articles()


if __name__ == "__main__":
    main()

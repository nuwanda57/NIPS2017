import requests
from bs4 import BeautifulSoup
import json
import urllib.request


def get_article_refs():
    main_page = requests.get("https://papers.nips.cc/book/advances-in-"
                             "neural-information-processing-systems-30-2017")
    main_page_soup = BeautifulSoup(main_page.text, "html.parser")
    lists = main_page_soup.find_all("li")
    articles_names = [x.find("a", attrs={"class": False}).get("href") for x in lists]
    for r in articles_names:
        if r.find("paper") == -1:
            articles_names.remove(r)
    articles_refs = []
    for i in range(0, len(articles_names)):
        articles_refs.append("https://papers.nips.cc" + articles_names[i] + ".pdf")
    articles_pages = []
    for i in range(0, len(articles_names)):
        articles_pages.append("https://papers.nips.cc" + articles_names[i])
    with open("articles_refs.json", "w") as o_file:
        json.dump(articles_refs, o_file)
    with open("articles_pages.json", "w") as o_file:
        json.dump(articles_pages, o_file)

        
def download_articles():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("Articles/" + ref[29:])
            f.close()
        except:
            urllib.request.urlretrieve(ref, "Articles/" + ref[29:])

            
def download_abstracts():
    with open("articles_pages.json") as i_file:
        articles_pages = json.load(i_file)
    for page_ref in articles_pages:
        try:
            f = open("Abstracts/" + page_ref[29:] + ".txt")
            f.close()
        except:
            page = requests.get(page_ref)
            page_soup = BeautifulSoup(page.text, "html.parser")
            abstract = page_soup.find(attrs={"class": "abstract"})
            with open("Abstracts/" + page_ref[29:] + ".txt", "w") as o_file:
                o_file.write(abstract.text)

                
def download_reviews():
    with open("articles_pages.json") as i_file:
        articles_pages = json.load(i_file)
    for page_ref in articles_pages:
        page = requests.get(page_ref)
        page_soup = BeautifulSoup(page.text, "html.parser")
        refs = page_soup.find_all('a')
        review_page_ref = ""
        for r in refs:
            if r.text == "[Reviews]":
                review_page_ref = r.get('href')
                break
        if review_page_ref == "":
            raise 42
        urllib.request.urlretrieve("https:" + review_page_ref, "Reviews/" + page_ref[29:] + ".html")

        
def main():
    get_article_refs()
    download_articles()
    download_abstracts()
    download_reviews()

    
if __name__ == "__main__":
    main()

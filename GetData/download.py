import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import argparse
import warnings
import os
import shutil


USERNAME = "your linux username"


def resolve_path(path, is_overwrite):
    if os.path.isdir(path):
        if is_overwrite:
            warnings.warn("Overwriting directory " + path)
            shutil.rmtree(path)
        else:
            warnings.warn("The directory " + path + " already exists")
            return False
    os.makedirs(path)
    os.makedirs(path + "Abstracts/")
    os.makedirs(path + "Articles/")
    os.makedirs(path + "Reviews/")
    return True


def get_article_refs(path, webpage):
    print(webpage)
    main_page = requests.get(webpage)
    main_page_soup = BeautifulSoup(main_page.text, "html.parser")
    lists = main_page_soup.find_all("li")
    articles_names = [x.find("a", attrs={"class": False}).get("href") for x in lists]
    for r in articles_names:
        if r.find("paper") == -1:
            articles_names.remove(r)
    articles_refs = []
    for i in range(0, len(articles_names)):
        print(1)
        articles_refs.append("https://papers.nips.cc" + articles_names[i] + ".pdf")
    articles_pages = []
    for i in range(0, len(articles_names)):
        articles_pages.append("https://papers.nips.cc" + articles_names[i])
    with open(path + "articles_refs.json", "w") as o_file:
        json.dump(articles_refs, o_file)
    with open(path + "articles_pages.json", "w") as o_file:
        json.dump(articles_pages, o_file)
    print(55)

        
def download_articles(path):
    with open(path + "articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open(path + "Articles/" + ref[29:])
            f.close()
        except:
            urllib.request.urlretrieve(ref, path + "Articles/" + ref[29:])

            
def download_abstracts(path):
    with open(path + "articles_pages.json") as i_file:
        articles_pages = json.load(i_file)
    for page_ref in articles_pages:
        try:
            f = open("Abstracts/" + page_ref[29:] + ".txt")
            f.close()
        except:
            page = requests.get(page_ref)
            page_soup = BeautifulSoup(page.text, "html.parser")
            abstract = page_soup.find(attrs={"class": "abstract"})
            with open(path + "Abstracts/" + page_ref[29:] + ".txt", "w") as o_file:
                o_file.write(abstract.text)

                
def download_reviews(path):
    with open(path + "articles_pages.json") as i_file:
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
        urllib.request.urlretrieve("https:" + review_page_ref, path + "Reviews/" + page_ref[29:] + ".html")

        
def main(path, is_overwrite, webpage):
    if not resolve_path(path, is_overwrite):
        warnings.warn("Invalid path")
        return
    get_article_refs(path, webpage)
    download_articles(path)
    download_abstracts(path)
    download_reviews(path)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true", required=False,
                        help="if specified and the given directory exists, the directory will be overwritten")
    parser.add_argument(
        "--path", type=str, help="directory where to store the data")
    parser.add_argument("--webpage", type=str, required=False, help="Link to the [year] Nips web page")
    args = parser.parse_args()
    if args.path[0] != "/":
        path = "/home/" + USERNAME + args.path
    else:
        path = "/home/" + USERNAME + args.path
    if path[-1] != "/":
        path += "/"
    webpage = args.webpage
    if webpage is None:
        webpage =  "https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017"
    is_overwrite = args.overwrite
    main(path, is_overwrite, webpage)

from bs4 import BeautifulSoup
import requests
import json


def get_authors():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("Authors1/" + ref[29:-3] + "json")
            f.close()
        except:
            ref1 = ref[:-4]
            r = requests.get(ref1)
            page = BeautifulSoup(r.text, "html.parser")
            authors_page = page.find("ul", attrs={"class": "authors"})
            authors = [i.text for i in authors_page.find_all("li")]
            with open("Authors1/" + ref[29:-3] + "json", "w") as f_out:
                json.dump(authors, f_out)


def main():
    get_authors()


if __name__ == "__main__":
    main()

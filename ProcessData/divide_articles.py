# bad article: 6664 - not readable
import subprocess
from bs4 import BeautifulSoup
import json


# convert pdf document to python string
def get_text(pdf_path):
    subprocess.call(["pdftotext", pdf_path, "temp.txt"])
    f = open("temp.txt", encoding="utf8")
    text = f.read()
    f.close()
    return text


def write_text_to_file(text, path):
    with open(path, 'w') as f_out:
        f_out.write(text)


# go through each pdf article and create txt file based on it
def write_all_texts():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("ArticleText/" + ref[29:-3] + "json")
            f.close()
            continue
        except:
            pdf_path = 'Articles/' + ref[29:]
        text = get_text(pdf_path)
        o_path = "ArticleText/" + ref[29:-3] + "txt"
        write_text_to_file(text, o_path)


# take review html file and create txt file from it
def parse_review_html(path, o_path):
    try:
        f = open(o_path + ".txt")
        f.close()
        return
    except:
        with open(path) as f_in:
            soup = BeautifulSoup(f_in, "html.parser")
    names = soup.find_all("h3")
    reviews = soup.find_all("div", attrs={"style" : "white-space: pre-wrap;"})
    text = ""
    for i in range(len(names)):
        text += names[i].get_text()
        text += "\n\n"
        text += reviews[i].get_text()
        text += "\n\n"
    write_text_to_file(text, o_path + ".txt")


# for each article take it's review html file and create a txt file based on it
def write_all_reviews():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        path = 'Reviews/' + ref[29:-3] + "html"
        o_path = "ReviewText/" + ref[29:-4]
        parse_review_html(path, o_path)


def main():
    write_all_texts()
    write_all_reviews()


if __name__ == "__main__":
    main()

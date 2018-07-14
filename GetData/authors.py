from bs4 import BeautifulSoup
import requests
import json
import argparse
import warnings
import os
import shutil


USERNAME = "your linux username"


def get_authors(path, is_overwrite):
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    if os.path.isdir(path):
        if is_overwrite:
            warnings.warn("Overwriting directory " + path)
            shutil.rmtree(path)
        else:
            warnings.warn("The directory " + path + " already exists")
            return
    if path[-1] != "/":
        path += "/"
    os.makedirs(path + "Authors1/")
    for ref in articles_refs:
        try:
            f = open(path + "Authors1/" + ref[29:-3] + "json")
            f.close()
        except:
            ref1 = ref[:-4]
            r = requests.get(ref1)
            page = BeautifulSoup(r.text, "html.parser")
            authors_page = page.find("ul", attrs={"class": "authors"})
            authors = [i.text for i in authors_page.find_all("li")]
            with open(path + "Authors1/" + ref[29:-3] + "json", "w") as f_out:
                json.dump(authors, f_out)


def main(path, is_overwrite):
    get_authors(path, is_overwrite)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true",
                        help="if specified and the given directory exists, the directory will be overwritten")
    parser.add_argument(
        "--path", type=str, help="directory where to store the data")
    args = parser.parse_args()
    if args.path[0] != "/":
        path = "/home/" + USERNAME + args.path
    else:
        path = "/home/" + USERNAME + args.path
    if path[-1] != "/":
        path += "/"
    is_overwrite = args.overwrite
    main(path, is_overwrite)

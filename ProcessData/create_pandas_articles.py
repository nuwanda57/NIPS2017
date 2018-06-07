import pandas as pd
import json

def main():
    df = pd.DataFrame(columns=["name", "pdf", "ref", "text", "abstract",
                               "intro", "bibliography", "review",
                               "review_html", "acknowledgements", "conclusion", "related"])
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        name = ref[29:-4]
        pdf = "Articles/" + name + ".pdf"
        text = "ArticleText/" + name + ".txt"
        abstract = "Abstracts/" + name + ".txt"
        review = "ReviewText/" + name + ".txt"
        review_html = "Reviews/" + name + ".html"
        try:
            f = open("IntroText/" + ref[29:-4] + ".txt")
            f.close()
            intro = "IntroText/" + name + ".txt"
        except:
            intro = None
        try:
            f = open("ConclusionText/" + ref[29:-4] + ".txt")
            f.close()
            conclusion = "ConclusionText/" + name + ".txt"
        except:
            conclusion = None
        try:
            f = open("RelatedText/" + ref[29:-4] + ".txt")
            f.close()
            related = "RelatedText/" + name + ".txt"
        except:
            related = None
        try:
            f = open("AcknowledgementsText/" + ref[29:-4] + ".txt")
            f.close()
            acknow = "AcknowledgementsText/" + name + ".txt"
        except:
            acknow = None
        references = "ReferencesText" + name + ".json"
        df = df.append({"name" : name, "pdf" : pdf, "ref" : ref, "text" : text, "abstract" : abstract,
                        "intro" : intro, "bibliography" : references, "review" : review,
                        "review_html" : review_html, "acknowledgements" : acknow, "conclusion" : conclusion,
                        "related" : related}, ignore_index=True)
    df.to_csv("articles.csv")

if __name__ == "__main__":
    main()

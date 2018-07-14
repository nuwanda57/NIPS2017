import pandas as pd
import json


def main():
    df = pd.DataFrame(columns=["name", "id", "authors", "ref", "pdf", "text", "abstract", "review_html",
                               "review_text", "bibliography", "processed_text", "intro", "conclusion", "related",
                               "acknowledgements", "only_words", "n_gram",
                               ])
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    cnt = 1
    for ref in articles_refs:
        id = str(cnt)
        name = ref[29:-4]
        articles = "No_Preprocessing/Articles/" + name + ".pdf"
        text = "No_Preprocessing/ArticleText/" + name + ".txt"
        abstract = "No_Preprocessing/Abstracts/" + name + ".txt"
        review = "No_Preprocessing/Reviews/" + name + ".html"
        review_text = "No_Preprocessing/ReviewText/" + name + ".txt"
        try:
            f = open("SectionProcessing/Sections/IntroText/" + ref[29:-4] + ".txt")
            f.close()
            intro = "SectionProcessing/Sections/IntroText/" + name + ".txt"
        except:
            intro = None
        try:
            f = open("SectionProcessing/Sections/ConclusionText/" + ref[29:-4] + ".txt")
            f.close()
            conclusion = "SectionProcessing/Sections/ConclusionText/" + name + ".txt"
        except:
            conclusion = None
        try:
            f = open("SectionProcessing/Sections/RelatedText/" + ref[29:-4] + ".txt")
            f.close()
            related = "SectionProcessing/Sections/RelatedText/" + name + ".txt"
        except:
            related = None
        try:
            f = open("SectionProcessing/Sections/AcknowledgementsText/" + ref[29:-4] + ".txt")
            f.close()
            acknow = "SectionProcessing/Sections/AcknowledgementsText/" + name + ".txt"
        except:
            acknow = None
        references = "No_Preprocessing/ReferencesText/" + name + ".json"
        only_text = "SectionProcessing/OnlyText/" + name + ".txt"
        clean_text = "TextCleaning/CleanText1/" + name + ".txt"
        stat = "TextCleaning/Statistics1/" + name + ".txt"
        with open("No_Preprocessing/Authors1/" + name + ".json") as f_in:
            authors = "\n".join(json.load(f_in))
        df = df.append({
            "name": name, "id": id, "authors": authors, "ref": ref, "pdf": articles, "text": text,
            "abstract": abstract, "review_html": review, "review_text": review_text, "bibliography": references,
            "processed_text": only_text, "intro": intro, "conclusion": conclusion, "related": related,
            "acknowledgements": acknow, "only_words": clean_text, "n_gram": stat
        }, ignore_index=True)
        cnt += 1
    df = df.set_index("name")
    df.to_csv("location_main_table.csv")


if __name__ == "__main__":
    main()

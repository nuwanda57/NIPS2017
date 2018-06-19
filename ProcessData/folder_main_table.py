import pandas as pd
import json


def main():
    df = pd.DataFrame(columns=["name", "id", "authors", "ref", "No_Preprocessing/Articles/", "No_Preprocessing/ArticleText/",
                               "No_Preprocessing/Abstracts/", "No_Preprocessing/Reviews/",
                               "No_Preprocessing/ReviewText/", "No_Preprocessing/ReferencesText/",
                               "SectionProcessing/OnlyText/", "SectionProcessing/Sections/IntroText/",
                               "SectionProcessing/Sections/ConclusionText/", "SectionProcessing/Sections/RelatedText/",
                               "SectionProcessing/Sections/AcknowledgementsText/"
                               "TextCleaning/CleanText1/", "TextCleaning/Statistics1/",
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
            "name" : name, "id" : id, "authors" : authors, "ref" : ref, "No_Preprocessing/Articles/" : articles,
            "No_Preprocessing/ArticleText/" : text,
            "No_Preprocessing/Abstracts/" : abstract, "No_Preprocessing/Reviews/" : review,
            "No_Preprocessing/ReviewText/" : review_text, "No_Preprocessing/ReferencesText/" : references,
            "SectionProcessing/OnlyText/" : only_text, "SectionProcessing/Sections/IntroText/" : intro,
            "SectionProcessing/Sections/ConclusionText/" : conclusion,
            "SectionProcessing/Sections/RelatedText/" : related,
            "SectionProcessing/Sections/AcknowledgementsText/" : acknow,
            "TextCleaning/CleanText1/" : clean_text, "TextCleaning/Statistics1/" : stat
        }, ignore_index=True)
        cnt += 1
    df = df.set_index("name")
    df.to_csv("folder_main_table.csv")

if __name__ == "__main__":
    main()

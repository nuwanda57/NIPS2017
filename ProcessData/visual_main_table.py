import pandas as pd
import json


def main():
    df = pd.DataFrame(columns=["name", "id", "authors", "ref", "text", "abstract", "review_html",
                               "review_text", "bibliography", "processed_text", "intro", "conclusion", "related",
                               "acknowledgements", "only_words", "n_gram",
                               ])
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    cnt = 1
    for ref in articles_refs:
        id = str(cnt)
        name = ref[29:-4]
        with open("No_Preprocessing/ArticleText/" + name + ".txt") as f_in:
            text = f_in.read()
        with open("No_Preprocessing/Abstracts/" + name + ".txt") as f_in:
            abstract = f_in.read()
        with open("No_Preprocessing/ReviewText/" + name + ".txt") as f_in:
            review_text = f_in.read()
        try:
            f = open("SectionProcessing/Sections/IntroText/" + ref[29:-4] + ".txt")
            intro = f.read()
            f.close()
        except:
            intro = None
        try:
            f = open("SectionProcessing/Sections/ConclusionText/" + ref[29:-4] + ".txt")
            conclusion = f.read()
            f.close()
        except:
            conclusion = None
        try:
            f = open("SectionProcessing/Sections/RelatedText/" + ref[29:-4] + ".txt")
            related = f.read()
            f.close()
        except:
            related = None
        try:
            f = open("SectionProcessing/Sections/AcknowledgementsText/" + ref[29:-4] + ".txt")
            acknow = f.read()
            f.close()
        except:
            acknow = None
        references_f = "No_Preprocessing/ReferencesText/" + name + ".json"
        with open(references_f) as f_in:
            refs = json.load(f_in).values()
            references = "\n".join(refs)
        with open("SectionProcessing/OnlyText/" + name + ".txt") as f_in:
            only_text = f_in.read()
        with open("TextCleaning/CleanText1/" + name + ".txt") as f_in:
            clean_text = f_in.read()
        with open("TextCleaning/Statistics1/" + name + ".txt") as f_in:
            stat = f_in.read()
        with open("No_Preprocessing/Authors1/" + name + ".json") as f_in:
            authors = "\n".join(json.load(f_in))
        df = df.append({
            "name": name, "id": id, "authors": authors, "ref": ref, "text": text,
            "abstract": abstract, "review_text": review_text, "bibliography": references,
            "processed_text": only_text, "intro": intro, "conclusion": conclusion, "related": related,
            "acknowledgements": acknow, "only_words": clean_text, "n_gram": stat
        }, ignore_index=True)
        cnt += 1
    df = df.set_index("name")
    df.to_csv("visual_main_table.csv")


if __name__ == "__main__":
    main()

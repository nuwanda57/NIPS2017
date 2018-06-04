import pandas as pd
import json

def main():
    df = pd.DataFrame(columns=["name", "pdf", "ref", "abstract", "intro", "bibliography"])
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        name = ref[29:-4]
        pdf = "Articles/" + name + ".pdf"
        abstract = "Abstracts/" + name + ".txt"
        try:
            f = open("IntroText/" + ref[29:-4] + ".txt")
            f.close()
            intro = "IntroText/" + name + ".txt"
        except:
            intro = None
        references = "ReferencesText" + name + ".json"
        df = df.append({"name" : name, "pdf" : pdf, "ref" : ref, "abstract" : abstract,
                        "intro" : intro, "bibliography" : references}, ignore_index=True)
    df.to_csv("articles.csv")

if __name__ == "__main__":
    main()

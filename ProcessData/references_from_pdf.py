# Bad Articles
# 6664, 7017, 7088, 7131, 7263
import json
import re
import subprocess


def text_from_pdf(pdf_path):
    subprocess.call(["pdftotext", pdf_path, "temp.txt"])
    f = open("temp.txt", encoding="utf8")
    text = f.read()
    f.close()
    return text


def categorize_main():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    s = []
    for ref in articles_refs:
        try:
            f = open("ReferencesText/" + ref[29:-3] + "json")
            f.close()
        except:
            pdf_path = 'Articles/' + ref[29:]
            text = text_from_pdf(pdf_path)
            cut1 = text.rfind("Bibliography")
            cut2 = text.rfind("References")
            if (cut1 == -1):
                text = text[cut2 + 9:]
            elif (cut2 == -1):
                text = text[cut1 + 11:]
            elif (cut2 > cut1):
                text = text[cut2 + 9:]
            else:
                text = text[cut1 + 11:]
            text = text.replace("\n", " ")
            bibliography = re.findall("\[[0-9]+\]", text)
            if (len(bibliography) >= 5):
                s.append(ref[29:-3])
    f = open("ReferencesStaff/CategoryMAIN.json", "w")
    json.dump(s, f)
    f.close()

    
def create_ref_texts_main():
    with open("ReferencesStaff/CategoryMAIN.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("ReferencesText/" + ref + "json")
            f.close()
        except:
            f = open("ReferencesText/" + ref + "json", "w")
            pdf_path = 'Articles/' + ref + "pdf"
            text = text_from_pdf(pdf_path)
            cut1 = text.rfind("Bibliography")
            cut2 = text.rfind("References")
            if (cut1 == -1):
                text = text[cut2 + 9:]
            elif (cut2 == -1):
                text = text[cut1 + 11:]
            elif (cut2 > cut1):
                text = text[cut2 + 9:]
            else:
                text = text[cut1 + 11:]
            text = text.replace("\n", " ")
            bibliography = re.split("\[[0-9]+\]", text)
            bibliography.pop(0)
            bibliography_dict = {}
            for i in range(0, len(bibliography)):
                bibliography_dict[i + 1] = bibliography[i]
            json.dump(bibliography_dict, f)
            f.close()

            
def categorize_rest_PARENTHESIS_YEAR():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    s = []
    for ref in articles_refs:
        try:
            f = open("ReferencesText/" + ref[29:-3] + "json")
            f.close()
        except:
            pdf_path = 'Articles/' + ref[29:]
            text = text_from_pdf(pdf_path)
            cut1 = text.rfind("Bibliography")
            cut2 = text.rfind("References")
            if (cut1 == -1):
                text = text[cut2 + 9:]
            elif (cut2 == -1):
                text = text[cut1 + 11:]
            elif (cut2 > cut1):
                text = text[cut2 + 9:]
            else:
                text = text[cut1 + 11:]
            text = text.replace("\n", " ")
            bibliography = re.findall("\([1-2][0-9][0-9][0-9]\)", text)
            if (len(bibliography) >= 10):
                s.append(ref[29:-3])
    f = open("ReferencesStaff/CategoryBIBLIOGRAPHY(YEAR).json", "w")
    json.dump(s, f)
    f.close()

    
def deal_with_PARENTHESIS_YEAR():
    with open("ReferencesStaff/CategoryBIBLIOGRAPHY(YEAR).json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("ReferencesText/" + ref + "json")
            f.close()
        except:
            f = open("ReferencesText/" + ref + "json", "w")
            pdf_path = 'Articles/' + ref + "pdf"
            text = text_from_pdf(pdf_path)
            cut1 = text.rfind("Bibliography")
            cut2 = text.rfind("References")
            if (cut1 == -1):
                text = text[cut2 + 9:]
            elif (cut2 == -1):
                text = text[cut1 + 11:]
            elif (cut2 > cut1):
                text = text[cut2 + 9:]
            else:
                text = text[cut1 + 11:]
            bibliography = re.split("\n", text)
            new_bibliography = []
            new_bibliography.append(bibliography[0])
            for ind in range(1, len(bibliography)):
                if (len(re.findall("\([1-2][0-9][0-9][0-9]\)", bibliography[ind])) != 0):
                    new_bibliography.append(bibliography[ind])
                    continue
                new_bibliography[-1] += bibliography[ind]
            d_bibl = {}
            for cnt in range(len(new_bibliography)):
                if (len(new_bibliography[cnt]) > 15):
                    new_bibliography[cnt] = new_bibliography[cnt].replace("\n", " ")
                    d_bibl[cnt + 1] = new_bibliography[cnt]
            json.dump(d_bibl, f)
            f.close()

            
def categorize_rest_YEAR_IN_THE_END():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    s = []
    for ref in articles_refs:
        try:
            f = open("ReferencesText/" + ref[29:-3] + "json")
            f.close()
        except:
            pdf_path = 'Articles/' + ref[29:]
            text = text_from_pdf(pdf_path)
            cut1 = text.rfind("Bibliography")
            cut2 = text.rfind("References")
            if (cut1 == -1):
                text = text[cut2 + 9:]
            elif (cut2 == -1):
                text = text[cut1 + 11:]
            elif (cut2 > cut1):
                text = text[cut2 + 9:]
            else:
                text = text[cut1 + 11:]
            bibliography = re.findall("[^0-9][1-2][0-9][0-9][0-9][^0-9]{0,1}[^~]{0,4}\\n", text)
            if (len(bibliography) >= 10):
                s.append(ref[29:-3])
    f = open("ReferencesStaff/CategoryBIBLIOGRAPHY_YEAR_IN_THE_END.json", "w")
    json.dump(s, f)
    f.close()

    
def deal_with_YEAR_IN_THE_END():
    with open("ReferencesStaff/CategoryBIBLIOGRAPHY_YEAR_IN_THE_END.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("ReferencesText/" + ref + "json")
            f.close()
        except:
            f = open("ReferencesText/" + ref + "json", "w")
            pdf_path = 'Articles/' + ref + "pdf"
            text = text_from_pdf(pdf_path)
            cut1 = text.rfind("Bibliography")
            cut2 = text.rfind("References")
            if (cut1 == -1):
                text = text[cut2 + 9:]
            elif (cut2 == -1):
                text = text[cut1 + 11:]
            elif (cut2 > cut1):
                text = text[cut2 + 9:]
            else:
                text = text[cut1 + 11:]
            years = re.findall("[^0-9][1-2][0-9][0-9][0-9][^0-9]{0,1}[^~]{0,4}\\n", text)
            bibliography = re.split("[^0-9][1-2][0-9][0-9][0-9][^0-9]{0,1}[^~]{0,4}\\n", text)
            d_bibl = {}
            for cnt in range(len(bibliography)):
                if (len(bibliography[cnt]) > 15):
                    if (cnt < len(years)):
                        bibliography[cnt] = bibliography[cnt] + years[cnt]
                    bibliography[cnt] = bibliography[cnt].replace("\n", " ")
                    d_bibl[cnt + 1] = bibliography[cnt]
            json.dump(d_bibl, f)
            f.close()

            
def show_rests():
    print("All Done, but:")
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("ReferencesText/" + ref[29:-3] + "json")
            f.close()
        except:
            print(ref, "\n")


def main():
    categorize_main()
    create_ref_texts_main()
    categorize_rest_PARENTHESIS_YEAR()
    deal_with_PARENTHESIS_YEAR()
    categorize_rest_YEAR_IN_THE_END()
    deal_with_YEAR_IN_THE_END()
    show_rests()

    
if __name__ == "__main__":
    main()

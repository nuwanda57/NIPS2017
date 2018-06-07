# bad article: 6664 - not readable
import subprocess
from bs4 import BeautifulSoup
import json
import re

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
        except:
            pdf_path = 'Articles/' + ref[29:]
            text = get_text(pdf_path)
            o_path = "ArticleText/" + ref[29:-3] + "txt"
            write_text_to_file(text, o_path)

# try to get Introduction from text - 1 variant
def get_intro1(text):
    cut = text.find("\n1\n\nIntroduction")
    if (cut == -1):
        return ""
    text = text[cut:]
    end_cut = text.find("\n2")
    text = text[:end_cut]
    return text

# try to get Introduction from text - 2 variant
# if 1 didn't work
def get_intro2(text):
    cut = text.find("\nIntroduction")
    if (cut == -1):
        return ""
    text = text[cut:]
    end_cut = text.find("\n1\n\n")
    text = text[:end_cut]
    return text

# try to get Introduction from text - 3 variant
# if 1,2 didn't work
def get_intro3(text):
    cut = text.find("\n1 Introduction")
    if (cut == -1):
        return ""
    text = text[cut:]
    end_cut1 = text.find("\n2 ")
    end_cut2 = re.search("\n?2 ", text).start()
    if (end_cut1 == -1 and end_cut2 == -1):
        return ""
    if (end_cut1 == -1):
        end_cut = end_cut2
    elif (end_cut2 == None):
        end_cut = end_cut1
    else:
        end_cut = min(end_cut1, end_cut2)
    text = text[:end_cut]
    return text

# for each article create file with Introduction text
# there are some files without Introduction
def write_all_introductions():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("IntroText/" + ref[29:-3] + "txt")
            f.close()
        except:
            pdf_path = 'ArticleText/' + ref[29:-3] + "txt"
            with open(pdf_path) as f_in:
                text = f_in.read()
            intro_text = get_intro1(text)
            if (intro_text == ""):
                intro_text = get_intro2(text)
                if (intro_text == ""):
                    intro_text = get_intro3(text)
                    if (intro_text == ""):
                        print(ref)
                        continue
            o_path = "IntroText/" + ref[29:-3] + "txt"
            write_text_to_file(intro_text, o_path)

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
    reviews = soup.find_all("div", attrs={"style":"white-space: pre-wrap;"})
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

# read article and get headers from it (like Introduction, Related work, etc.)
# detect all headers starting with section single number (ex. "2 Introduction")
def add_headers_from_article(path, headers):
    with open(path) as f_in:
        text = f_in.read()
    new_heads = re.findall("\n[1-9][ \n][A-z ]{5,40}\n", text)
    for j in range(len(new_heads)):
        i = new_heads[j]
        i = i[3:]
        i = i.strip()
        if (i not in headers):
            headers[i] = 1
        else:
            headers[i] += 1

# read article and get headers from it (like Introduction, Related work, etc.)
# detect all headers starting with subsection double number (ex. "2.2 Model")
def add_subheaders_from_article(path, headers):
    with open(path) as f_in:
        text = f_in.read()
    new_heads = re.findall("\n[1-9][\.][1-9][ \n]+[A-z ]{5,40}\n", text)
    for j in range(len(new_heads)):
        i = new_heads[j]
        i = i[5:]
        i = i.strip()
        if (i not in headers):
            headers[i] = 1
        else:
            headers[i] += 1

# Reveal the list of the most common headers in the articles
# with the number of articles where it appears
# (Not all of them because not every header starts with a paragraph number)
def detect_main_headers():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    headers = dict()
    for ref in articles_refs:
        path = "ArticleText/" + ref[29:-3] + "txt"
        add_headers_from_article(path, headers)
        add_subheaders_from_article(path, headers)
    import operator
    sorted_headers = sorted(headers.items(), key=operator.itemgetter(1), reverse=True)
    headers_set = set()
    for i in sorted_headers:
        if i[1] > 2:
            print(i)
            headers_set.add(i[0])
    return headers_set

# acknowledgements are not headers : they do not start with paragraph number
# so they are not in the list above
# Note: there are 4 different versions or how it is written
def get_acknowledgements1(text, headers_set):
    cut = text.find("\n\nAcknowledgement")
    if (cut == -1):
        cut = text.find("\nAcknowledgement")
    if (cut == -1):
        cut = text.find("\nAcknowledgment")
    if (cut == -1):
        cut = text.find("Acknowledgement")
    if (cut == -1):
        cut = text.find("Acknowledgment")
    if (cut == -1):
        return ""
    text = text[cut:]
    end_cut2 = text.find("Reference")
    end_cut3 = text.find("Bibliography")
    if (end_cut2 == -1):
        end_cut = end_cut3
    elif (end_cut3 == -1):
        end_cut = end_cut2
    else:
        end_cut = min(end_cut2, end_cut3)
    for word in headers_set:
        end_cut2 = text.find(word)
        if (end_cut2 != -1):
            if (end_cut == -1 or end_cut > end_cut2):
                end_cut = end_cut2
    if end_cut == -1:
        return ""
    text = text[:end_cut]
    return text

# get acknowledgements from every article and create txt file for each of them
def write_all_acknowledgements(headers_set):
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("AcknowledgementsText/" + ref[29:-3] + "txt")
            f.close()
        except:
            pdf_path = 'ArticleText/' + ref[29:-3] + "txt"
            with open(pdf_path) as f_in:
                text = f_in.read()
            acknowledgements_text = get_acknowledgements1(text, headers_set)
            if (acknowledgements_text == ""):
                continue
            o_path = "AcknowledgementsText/" + ref[29:-3] + "txt"
            write_text_to_file(acknowledgements_text, o_path)

# show which articles do not have acknowledgements
# Do not influence the output
def check_acknowledgements():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("AcknowledgementsText/" + ref[29:-3] + "txt")
            f.close()
        except:
            print(ref)

# proceed one article by finding related materials
# for more information see next function
def get_related(text, headers_set):
    related_best = {
        "\n\D?[1-9][ \n]+Related Work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Related Work[ ]*\n",
        "\n\D?[1-9][ \n]+Related Works[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Related Works[ ]*\n",
        "\n\D?[1-9][ \n]+Related work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Related work[ ]*\n",
        "\n\D?[1-9][ \n]+Related works[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Related works[ ]*\n",
        "\n\D?[1-9][ \n]+Conclusion and Future Work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Conclusion and Future Work[ ]*\n",
        "\n\D?[1-9][ \n]+Conclusions and Future Work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Conclusions and Future Work[ ]*\n",
        "\n\D?[1-9][ \n]+Discussion[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Discussion[ ]*\n",
        "\n\D?[1-9][ \n]+Discussions[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Discussions[ ]*\n",
        "\n\D?[1-9][ \n]+Discussion and Conclusion[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Discussion and Conclusion[ ]*\n",
        "\n\D?[1-9][ \n]+Applications[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Applications[ ]*\n",
        "\n\D?[1-9][ \n]+Conclusion and future work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Conclusion and future work[ ]*\n",
        "\n\D?[1-9][ \n]+Discussion and Future Work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Discussion and Future Work[ ]*\n",
        "\n\D?[1-9][ \n]+Background and Related Work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Background and Related Work[ ]*\n",
        "\n\D?[1-9][ \n]+Background and related work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Background and related work[ ]*\n",
        "\n\D?[1-9][ \n]+Previous Work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Previous Work[ ]*\n",
        "\n\D?[1-9][ \n]+Other Related Works[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Other Related Works[ ]*\n",
        "\n\D?[1-9][ \n]+Conclusions and future work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Conclusions and future work[ ]*\n",
        "\n\D?[1-9][ \n]+Discussion and Conclusions[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Discussion and Conclusions[ ]*\n",
        "\n\D?[1-9][ \n]+Future Work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Future Work[ ]*\n",
        "\n\D?[1-9][ \n]+Conclusions & future work[ ]*\n", "\n\D?[1-9][\.][1-9][ \n]+Conclusions & future work[ ]*\n"
    }
    match_res = []
    ans_text = ""
    for i in related_best:
        match_res += re.findall(i, text)
    if (len(match_res) != 0):
        for match in match_res:
            cut = text.find(match)
            text1 = text[cut + 3:]
            end_cut2 = text1.find("Reference")
            end_cut3 = text1.find("Bibliography")
            end_cut4 = text1.find("Acknowledgment")
            end_cut5 = text1.find("Acknowledgement")
            end_cuts = []
            if (end_cut2 != -1):
                end_cuts.append(end_cut2)
            if (end_cut3 != -1):
                end_cuts.append(end_cut3)
            if (end_cut4 != -1):
                end_cuts.append(end_cut4)
            if (end_cut5 != -1):
                end_cuts.append(end_cut5)
            end_cuts1 = re.findall("\n[1-9][\.][1-9][ \n]+\D{5,40}\n", text1)
            end_cuts2 = re.findall("\n[1-9][ \n]+\D{5,40}\n", text1)
            end_cuts3 = re.findall("\n\D?[1-9][ \n]+\D{5,40}", text1)
            end_cuts4 = re.findall("\n\D?[1-9][\.][1-9][ \n]+\D{5,40}", text1)
            for i in end_cuts1:
                end_cuts.append(text1.find(i))
            for i in end_cuts2:
                end_cuts.append(text1.find(i))
            for i in end_cuts3:
                end_cuts.append(text1.find(i))
            for i in end_cuts4:
                end_cuts.append(text1.find(i))
            end_cuts.sort()
            for i in end_cuts:
                if (i > 30):
                    ans_text += "\n\n"
                    ans_text += text1[:i]
                    break
        return ans_text
    return ""

# Based on List of Headers the following sections form division
# Related Work, Conclusion and Future Work (also refer to the conclusion division),
# Conclusions and Future Work, Discussion and Conclusion, Applications, Discussions,
# Background and related work
def write_related_staff(headers_set):
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("RelatedText/" + ref[29:-3] + "txt")
            f.close()
        except:
            pdf_path = 'ArticleText/' + ref[29:-3] + "txt"
            with open(pdf_path) as f_in:
                text = f_in.read()
            related_text = get_related(text, headers_set)
            if (related_text == ""):
                continue
            o_path = "RelatedText/" + ref[29:-3] + "txt"
            write_text_to_file(related_text, o_path)

# show which articles do not have related materials
# Do not influence the output
def check_related():
    with open("articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        print("RelatedText/" + ref[29:-3] + "txt")
        try:
            f = open("RelatedText/" + ref[29:-3] + "txt")
            f.close()
        except:
            print(ref)

def main():
    # write_all_texts()
    # write_all_abstracts()
    # write_all_reviews()
    # write_all_introductions()
    headers_set = detect_main_headers()
    headers_set.add("Proofs")
    headers_set.add("Technical results")
    headers_set.add("\n\n8\n")
    headers_set.add("\n3\n\n")
    # write_all_acknowledgements(headers_set)
    # check_acknowledgements()
    write_related_staff(headers_set)
    check_related()

if __name__ == "__main__":
    main()
# bad article: 6664
import subprocess
import json
import re

def get_text(pdf_path):
    subprocess.call(["pdftotext", pdf_path, "temp.txt"])
    f = open("temp.txt", encoding="utf8")
    text = f.read()
    f.close()
    return text

def write_text_to_file(text, path):
    with open(path, 'w') as f_out:
        f_out.write(text)

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

def get_intro1(text):
    cut = text.find("\n1\n\nIntroduction")
    if (cut == -1):
        return ""
    text = text[cut:]
    end_cut = text.find("\n2")
    text = text[:end_cut]
    return text

def get_intro2(text):
    cut = text.find("\nIntroduction")
    if (cut == -1):
        return ""
    text = text[cut:]
    end_cut = text.find("\n1\n\n")
    text = text[:end_cut]
    return text

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

def main():
    # write_all_texts()
    # write_all_abstracts()
    write_all_introductions()

if __name__ == "__main__":
    main()
import json


def write_text_to_file(text, path):
    with open(path, 'w') as f_out:
        f_out.write(text)


# Make sure that before each section or subsection number there are at least two line breaks
def process_article1(text1):
    i = 3
    text = text1
    while i < len(text) - 4:
        if text[i].isdigit() and text[i] != "0":
            # "\n\n1"
            if text[i - 1] == "\n" and text[i - 2] == "\n":
                i += 1
            # "\n\n?1\n" --> "\n\n1\n":
            elif (ord(text[i - 1]) >= 128 or ord(text[i - 1]) < 32) and text[i - 2] == "\n" and text[i - 3] == "\n":
                text = text[:i - 1] + text[i:]
            # "\n1\n" --> "\n\n1\n"
            elif (text[i + 1] == "\n" or text[i + 1] == " ") and text[i - 1] == "\n":
                text = text[:i] + "\n" + text[i:]
                if text[i + 2] == " ":
                    text = text[:i + 2] + "\n" + text[i + 3:]
                i += 2
            # "\n?1\n" --> "\n\n1\n"
            elif (text[i + 1] == "\n" or text[i + 1] == " ") and \
                    (ord(text[i - 1]) >= 128 or ord(text[i - 1]) < 32) and text[i - 2] == "\n":
                text = text[:i - 1] + "\n" + text[i:]
                if text[i + 2] == " ":
                    text = text[:i + 1] + "\n" + text[i + 2:]
                i += 1
            # "\n1.1\n" --> "\n\n1.1\n"
            elif text[i - 1] == "\n" and text[i + 1] == "." and text[i + 2].isdigit() \
                    and (text[i + 3] == "\n" or text[i + 3] == " "):
                text = text[:i] + "\n" + text[i:]
                if text[i + 4] == " ":
                    text = text[:i + 4] + "\n" + text[i + 5:]
                i += 2
            # "\n?1.1\n" --> "\n\n1.1\n"
            elif (ord(text[i - 1]) >= 128 or ord(text[i - 1]) < 32) and text[i - 2] == "\n" and text[i + 1] == "." \
                    and text[i + 2].isdigit() and (text[i + 3] == "\n" or text[i + 3] == " "):
                text = text[:i - 1] + "\n" + text[i:]
                if text[i + 3] == " ":
                    text = text[:i + 3] + "\n" + text[i + 4:]
                i += 1
            else:
                i += 1
        else:
            i += 1
    return text


# Make sure that double line breaks are only before possible section or subsection numbers
def process_article2(text):
    sections = text.split("\n\n")
    it = 1
    while it < len(sections):
        par = sections[it]
        if len(par) == 0:
            sections.pop(it)
        elif par[0].isdigit() and par[0] != "0" and (len(par) == 1 or par[1] == "\n" or par[1] == " "):
            it += 1
        elif par[0].isdigit() and par[0] != "0" and par[1] == "." and \
                ((len(par) == 3 and par[2].isdigit()) or (len(par) > 3 and par[2].isdigit()
                                                          and (par[3] == "\n" or par[3] == " "))):
            it += 1
        else:
            if par[0] == "\n":
                sections[it - 1] += sections[it]
            else:
                sections[it - 1] += "\n"
                sections[it - 1] += sections[it]
            sections.pop(it)
    res = "\n\n".join(sections)
    return res


# find some sections which are definitely not sections
# and make them not sections by adding the to the previous paragraph
def process_article3(text):
    sections = text.split("\n\n")
    it = 1
    while it < len(sections):
        sentences = sections[it].split("\n")
        if not sentences[0].isdigit():
            if len(sentences[0]) < 3:
                sections[it - 1] += sections[it]
                sections.pop(it)
                continue
            if not (sentences[0][0].isdigit() and sentences[0][0] != "0"
                    and sentences[0][1] == "." and sentences[0][2].isdigit() and sentences[0][2] != "0"):
                sections[it - 1] += sections[it]
                sections.pop(it)
                continue
        if len(sentences) == 1:
            if not sentences[0].isdigit():
                sections[it - 1] += sections[it]
                sections.pop(it)
                continue
            number = int(sentences[0])
            if it == len(sections) - 1:
                sections[it - 1] += sections[it]
                sections.pop(it)
                continue
            next_sentences = sections[it + 1].split("\n")
            if not (len(next_sentences[0]) >= 3 and next_sentences[0][0] == number and next_sentences[0][1] == "."
                    and next_sentences[0][2].isdigit() and next_sentences[0][2] != "0"):
                sections[it - 1] += sections[it]
                sections.pop(it)
                continue
            else:
                it += 1
                continue
        else:
            it += 1
    text1 = "\n\n".join(sections)
    return text1


# find some sections which are definitely not sections
# and make them not sections by adding the to the previous paragraph
def process_articles4(text):
    sections = text.split("\n\n")
    it = 1
    while it < len(sections):
        sentences = sections[it].split("\n")
        if len(sentences) == 1:
            continue
        if len(sentences[1]) <= 4:
            sections[it - 1] += sections[it]
            sections.pop(it)
            continue
        it += 1
    text1 = "\n\n".join(sections)
    return text1


# find some sections which are definitely not sections
# and make them not sections by adding the to the previous paragraph
# based on irrelevant substrings
def process_articles5(text):
    irrelevant_substrings_for_one_digit = {
        "Figure ", "Table ", "https://", "University", "Laboratory", "Microsoft Research", "School of", "+",
        "=", "Cov", "cov ", "Institute"
    }
    sections = text.split("\n\n")
    it = 1
    while it < len(sections):
        sentences = sections[it].split("\n")
        if len(sentences) == 1:
            continue
        if len(sentences[0]) == 1:
            s = sentences[1]
            for i in irrelevant_substrings_for_one_digit:
                if s[:20].find(i) != -1:
                    sections[it - 1] += sections[it]
                    sections.pop(it)
                    it -= 1
                    break
            it += 1
            continue
        it += 1
    text1 = "\n\n".join(sections)
    return text1


def section_priority(sections):
    for j in range(len(sections)):
        i = sections[j]
        if len(i) == 1:
            sections[j] = "\n" + i
            continue
        if i[1] != ".":
            sections[j] = "\n" + i
    return sections


def section_division(text):
    sections = text.split("\n\n")
    sections = section_priority(sections)
    text = "\n\n".join(sections)
    return text


def add_empty_line_before_numbers():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("OnlyText1/" + ref[29:-3] + "txt")
            f.close()
            continue
        except:
            pdf_path = './../ArticleText/' + ref[29:-3] + "txt"
            with open(pdf_path) as f_in:
                text = f_in.read()
            text = process_article1(text)
            text = process_article2(text)
            text = process_article3(text)
            text = process_articles4(text)
            text = process_articles5(text)
            text = section_division(text)
            o_path = "OnlyText1/" + ref[29:-3] + "txt"
            write_text_to_file(text, o_path)


def main():
    add_empty_line_before_numbers()


if __name__ == "__main__":
    main()

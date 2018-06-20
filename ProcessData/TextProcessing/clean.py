import json
import enchant
from nltk.corpus import words as WORDS


ENGLISH = enchant.Dict("en_US")


def write_text_to_file(text, path):
    with open(path, 'w') as f_out:
        f_out.write(text)


def count_numbers(p):
    res = 0
    for i in p:
        if i.isdigit():
            res += 1
    return res


def count_words(p):
    words = p.split()
    return len(words)


def count_symbols(p):
    res = 0
    for i in p:
        if i != " ":
            res += 1
    return res


def average_word_length(p):
    cnt = count_words(p)
    if cnt == 0:
        return 0
    total = count_symbols(p)
    return total / cnt


def median_word_length(p):
    words = p.split()
    mas = []
    for i in words:
        mas.append(len(i))
    return mas[len(mas) // 2]


def count_letters(p):
    res = 0
    for i in p:
        if i.isalpha():
            res += 1
    return res


def count_special(p):
    res = 0
    for i in p:
        if not i.isalpha() and i != " ":
            res += 1
    return res


def save_only_words(text):
    not_words = {
        "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "i", "J", "j", "K", "k",
        "L", "l", "M" "m", "N", "n", "O", "o", "P", "Q", "q", "R", "r", "S", "s", "T", "t", "U",
        "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "sup", "inf", "xi", "Xi", ".", "km", "tr"
    }
    lines = text.split("\n")
    i = 1
    while i < len(lines):
        new_line = ""
        words = lines[i].split()
        for w in words:
            if w == "":
                continue
            if count_numbers(w) != 0:
                continue
            try:
                if ENGLISH.check(w) and w not in not_words:
                    if new_line != "":
                        new_line += " "
                    new_line += w
                    continue
            except:
                continue
            try:
                if len(w) > 2 and ((ENGLISH.check(w[:-1]) and w[:-1] not in not_words)
                                   or (ENGLISH.check(w[1:]) and w[1:] not in not_words)):
                    if new_line != "":
                        new_line += " "
                    new_line += w
                    continue
            except:
                continue
            try:
                if len(w) > 4 and ENGLISH.check(w[1:-1]) and w[1:-1] not in not_words:
                    if new_line != "":
                        new_line += " "
                    new_line += w
                    continue
            except:
                continue
            if count_special(w) / len(w) >= 0.5:
                continue
            if count_special(w) > 2:
                continue
            if len(w) <= 2:
                continue
            else:
                # if new_line != "":
                #     new_line += " "
                # new_line += w
                continue
        if new_line == "":
            lines.pop(i)
            continue
        lines[i] = new_line
        i += 1
    return "\n".join(lines)


def get_clean(text):
    sections = text.split("\n\n\n")
    for i in range(len(sections)):
        sec = sections[i]
        subsections = sec.split("\n\n")
        for j in range(len(subsections)):
            par = subsections[j]
            subsections[j] = save_only_words(par)
        sections[i] = "\n\n".join(subsections)
    return "\n\n\n".join(sections)


def clean():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("CleanText1/" + ref[29:-3] + "txt")
            f.close()
        except:
            pdf_path = './../TextProcessing/OnlyText/' + ref[29:-3] + "txt"
            with open(pdf_path) as f_in:
                text = f_in.read()
            clean_text = get_clean(text)
            o_path = "CleanText1/" + ref[29:-3] + "txt"
            write_text_to_file(clean_text, o_path)


def main():
    clean()


if __name__ == "__main__":
    main()

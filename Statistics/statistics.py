import spacy
import json
from collections import Counter
from nltk import ngrams


nlp = spacy.load('en')


def write_text_to_file(text, path):
    with open(path, 'w') as f_out:
        f_out.write(text)


def count_letters(p):
    res = 0
    for i in p:
        if i.isalpha():
            res += 1
    return res


def file_statistics(text):
    answer = ""
    tokens = nlp(text)
    words = []
    for t in tokens:
        if count_letters(t.text) != 0:
            words.append(t.text.lower())
    ngram_counts2 = Counter(ngrams(words, 2))
    ngram_counts3 = Counter(ngrams(words, 3))
    ngram_counts4 = Counter(ngrams(words, 4))
    ngram_counts5 = Counter(ngrams(words, 5))
    answer += "TWO WORDS\n"
    for i in ngram_counts2.most_common(20):
        answer += str(i[1])
        answer += "\t"
        var_ans = ""
        for j in i[0]:
            var_ans += j
            var_ans += " "
        answer += var_ans
        answer += "\n"
    answer += "\n\n"
    answer += "THREE WORDS\n"
    for i in ngram_counts3.most_common(20):
        answer += str(i[1])
        answer += "\t"
        var_ans = ""
        for j in i[0]:
            var_ans += j
            var_ans += " "
        answer += var_ans
        answer += "\n"
    answer += "\n\n"
    answer += "FOUR WORDS\n"
    for i in ngram_counts4.most_common(20):
        answer += str(i[1])
        answer += "\t"
        var_ans = ""
        for j in i[0]:
            var_ans += j
            var_ans += " "
        answer += var_ans
        answer += "\n"
    answer += "\n\n"
    answer += "FIVE WORDS\n"
    for i in ngram_counts5.most_common(20):
        answer += str(i[1])
        answer += "\t"
        var_ans = ""
        for j in i[0]:
            var_ans += j
            var_ans += " "
        answer += var_ans
        answer += "\n"
    return answer


def statistics():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("Statistics1/" + ref[29:-3] + "txt")
            f.close()
        except:
            pdf_path = 'CleanText1/' + ref[29:-3] + "txt"
            with open(pdf_path) as f_in:
                text = f_in.read()
            clean_text = file_statistics(text)
            o_path = "Statistics1/" + ref[29:-3] + "txt"
            write_text_to_file(clean_text, o_path)


def main():
    statistics()


if __name__ == '__main__':
    main()

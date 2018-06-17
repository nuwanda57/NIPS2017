import json
import re


def write_text_to_file(text, path):
    with open(path, 'w') as f_out:
        f_out.write(text)


def get_end_cut_section(text, prev_number):
    end_cut1 = text.find("\n\n\n")
    end_cut2 = text.find("\n\n")
    if end_cut1 <= end_cut2 and end_cut1 != -1:
        end_cut = end_cut1
        return end_cut
    else:
        try:
            number = int(text[end_cut2 + 2])
        except:
            number = None
        while number == prev_number:
            end_cut2 = text[end_cut2 + 1:].find("\n\n")
            if end_cut2 == -1:
                break
            if end_cut1 <= end_cut2:
                break
            try:
                number = int(text[end_cut2 + 2])
            except:
                number = None
        if end_cut2 == -1:
            end_cut = end_cut1
        else:
            end_cut = min(end_cut1, end_cut2)
    return end_cut


def get_end_cut_subsection(text):
    return text.find("\n\n")


# try to get Introduction from text - 1 variant
def get_intro1(text):
    cut = text.find("\n\n\n1\nIntroduction")
    if cut == -1:
        cut = text.find("\n\n\nIntroduction")
        if cut == -1:
            cut = text.find("\nIntroduction")
            if cut == -1:
                cut = text.find("\n\n\n1\nMotivation")
                if cut == -1:
                    cut = text.find("\n\n\n1\nOverview")
                    if cut == -1:
                        return ""
            text = text[cut + 1:]
        else:
            text = text[cut + 3:]
    else:
        text = text[cut + 5:]
    end_cut = get_end_cut_section(text, 1)
    text = text[:end_cut]
    return text


# for each article create file with Introduction text
# there are some files without Introduction
def write_all_introductions():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("Sections/IntroText/" + ref[29:-3] + "txt")
            f.close()
            continue
        except:
            pdf_path = 'OnlyText/' + ref[29:-3] + "txt"
            with open(pdf_path) as f_in:
                text = f_in.read()
            intro_text = get_intro1(text)
            if intro_text == "":
                print(ref)
                continue
            o_path = "Sections/IntroText/" + ref[29:-3] + "txt"
            write_text_to_file(intro_text, o_path)


# acknowledgements are not headers : they do not start with paragraph number
# so they are not in the list above
# Note: there are 4 different versions or how it is written
def get_acknowledgements1(text):
    names = {
        "\n\n\nAcknowledgement", "\n\n\nAcknowledgment", "\nAcknowledgement", "\nAcknowledgment",
        "Acknowledgement", "Acknowledgment"
    }
    cut = -1
    for n in names:
        cut = text.find(n)
        if cut != -1:
            break
    if cut == -1:
        return ""
    while text[cut] == "\n":
        cut += 1
    text = text[cut:]
    end_cut = get_end_cut_subsection(text)
    text = text[:end_cut]
    return text


# get acknowledgements from every article and create txt file for each of them
def write_all_acknowledgements():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("Sections/AcknowledgementsText/" + ref[29:-3] + "txt")
            f.close()
        except:
            pdf_path = 'OnlyText/' + ref[29:-3] + "txt"
            with open(pdf_path) as f_in:
                text = f_in.read()
            acknowledgements_text = get_acknowledgements1(text)
            if acknowledgements_text == "":
                print(ref)
                continue
            o_path = "Sections/AcknowledgementsText/" + ref[29:-3] + "txt"
            write_text_to_file(acknowledgements_text, o_path)


# proceed one article by finding related materials
# for more information see next function
def get_related1(text):
    related_best1 = {
        "\n\n\n[1-9]*\n*Related",
        "\n\n\n[1-9]*\n*Conclusion and Future Work",
        "\n\n\n[1-9]*\n*Conclusions and Future Work",
        "\n\n\n[1-9]*\n*Discussion",
        "\n\n\n[1-9]*\n*Applications",
        "\n\n\n[1-9]*\n*Conclusion and future work",
        "\n\n\n[1-9]*\n*Discussion and Future Work",
        "\n\n\n[1-9]*\n*Background",
        "\n\n\n[1-9]*\n*Previous Work",
        "\n\n\n[1-9]*\n*Other Related Works",
        "\n\n\n[1-9]*\n*Conclusions and future work",
        "\n\n\n[1-9]*\n*Discussion and Conclusions",
        "\n\n\n[1-9]*\n*Future Work",
        "\n\n\n[1-9]*\n*Future work",
        "\n\n\n[1-9]*\n*Conclusions & future work",
        "\n\n\n[1-9]*\n*Discussion and Extensions",
        "\n\n\n[1-9]*\n*Discussion and extensions",
        "\n\n\n[1-9]*\n*Conclusion & Future Directions",
        "\n\n\n[1-9]*\n*Generalization and Future Work",
        "\n\n\n[1-9]*\n*Discussion and perspective",
        "\n\n\n[1-9]*\n*Prior work",
    }
    match_res = []
    ans_text = ""
    for i in related_best1:
        match_res += re.findall(i, text)
    if len(match_res) != 0:
        for match in match_res:
            cut = text.find(match)
            try:
                number = int(text[cut + 3])
            except:
                number = None
            text1 = text[cut + 5:]
            if number is None:
                end_cut = get_end_cut_subsection(text1)
            else:
                end_cut = get_end_cut_section(text1, number)
            text1 = text1[:end_cut]
            if ans_text != "":
                ans_text += "\n\n"
            ans_text += text1
    related_best2 = set()
    for q in related_best1:
        k = q[1:]
        k = k[:2] + "[1-9].[1-9]\n" + k[10:]
        related_best2.add(k)
    match_res = []
    for i in related_best2:
        match_res += re.findall(i, text)
    if len(match_res) != 0:
        for match in match_res:
            cut = text.find(match)
            text1 = text[cut + 2:]
            end_cut = get_end_cut_subsection(text1)
            text1 = text1[:end_cut]
            if ans_text != "":
                ans_text += "\n\n"
            ans_text += text1
    return ans_text


# Based on List of Headers the following sections form division
# Related Work, Conclusion and Future Work (also refer to the conclusion division),
# Conclusions and Future Work, Discussion and Conclusion, Applications, Discussions,
# Background and related work
def write_related_staff():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("Sections/RelatedText/" + ref[29:-3] + "txt")
            f.close()
        except:
            pdf_path = 'OnlyText/' + ref[29:-3] + "txt"
            with open(pdf_path) as f_in:
                text = f_in.read()
            related_text = get_related1(text)
            if related_text == "":
                print(ref)
                continue
            o_path = "Sections/RelatedText/" + ref[29:-3] + "txt"
            write_text_to_file(related_text, o_path)


# proceed one article by finding conclusions/analysis
# for more information see next function
def get_conclusions1(text):
    related_best1 = {
        "\n\n\n[1-9]*\n*Conclusion",
        "\n\n\n[1-9]*\n*Results",
        "\n\n\n[1-9]*\n*Experimental Results",
        "\n\n\n[1-9]*\n*Experimental results",
        "\n\n\n[1-9]*\n*Discussion and Conclusion",
        "\n\n\n[1-9]*\n*Analysis",
        "\n\n\n[1-9]*\n*Evaluation",
        "\n\n\n[1-9]*\n*Theoretical Analysis",
        "\n\n\n[1-9]*\n*Inference",
        "\n\n\n[1-9]*\n*Contributions",
        "\n\n\n[1-9]*\n*Summary",
        "\n\n\n[1-9]*\n*Concluding Remarks",
        "\n\n\n[1-9]*\n*Experimental Evaluation",
        "\n\n\n[1-9]*\n*Main results",
        "\n\n\n[1-9]*\n*Convergence Analysis",
        "\n\n\n[1-9]*\n*Generalization and Future Work",
        "\n\n\n[1-9]*\n*Discussion and perspective",
        "\n\n\n[1-9]*\n*Our contributions",
        "\n\n\n[1-9]*\n*Main Result",
        "\n\n\n[1-9]*\n*Empirical Evaluation",
        "\n\n\n[1-9]*\n*Theoretical analysis",
        "\n\n\n[1-9]*\n*Experiments and Results",
        "\n\n\n[1-9]*\n*Theoretical Results",
        "\n\n\n[1-9]*\n*Empirical evaluation",
        "\n\n\n[1-9]*\n*Our Results",
        "\n\n\n[1-9]*\n*Numerical Results",
        "\n\n\n[1-9]*\n*Our Contributions"
    }
    match_res = []
    ans_text = ""
    for i in related_best1:
        match_res += re.findall(i, text)
    if len(match_res) != 0:
        for match in match_res:
            cut = text.find(match)
            try:
                number = int(text[cut + 3])
            except:
                number = None
            text1 = text[cut + 5:]
            if number is None:
                end_cut = get_end_cut_subsection(text1)
            else:
                end_cut = get_end_cut_section(text1, number)
            text1 = text1[:end_cut]
            if ans_text != "":
                ans_text += "\n\n"
            ans_text += text1
    related_best2 = set()
    for q in related_best1:
        k = q[1:]
        k = k[:2] + "[1-9].[1-9]\n" + k[10:]
        related_best2.add(k)
    match_res = []
    for i in related_best2:
        match_res += re.findall(i, text)
    if len(match_res) != 0:
        for match in match_res:
            cut = text.find(match)
            text1 = text[cut + 2:]
            end_cut = get_end_cut_subsection(text1)
            text1 = text1[:end_cut]
            if ans_text != "":
                ans_text += "\n\n"
            ans_text += text1
    return ans_text


# Based on List of Headers the following sections form division
# Conclusions/Analysis
def write_conclusions_staff():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("Sections/ConclusionText/" + ref[29:-3] + "txt")
            f.close()
        except:
            pdf_path = 'OnlyText/' + ref[29:-3] + "txt"
            with open(pdf_path) as f_in:
                text = f_in.read()
            related_text = get_conclusions1(text)
            if related_text == "":
                print(ref)
                continue
            o_path = "Sections/ConclusionText/" + ref[29:-3] + "txt"
            write_text_to_file(related_text, o_path)


def main():
    write_all_introductions()
    write_all_acknowledgements()
    write_related_staff()
    write_conclusions_staff()


if __name__ == "__main__":
    main()

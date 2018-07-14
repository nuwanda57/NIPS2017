import json

SECTION_STATISTICS = []
POPULAR_SECTIONS = set()


def write_text_to_file(text, path):
    with open(path, 'w') as f_out:
        f_out.write(text)


def section_statistics(sections, var_section_statistics):
    for s in sections:
        mas = s.split("\n")
        name = mas[1]
        if name in var_section_statistics.keys():
            var_section_statistics[name] += 1
        else:
            var_section_statistics[name] = 1


def create_statistics():
    var_sections_statistics = {}
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        pdf_path = 'OnlyText1/' + ref[29:-3] + "txt"
        with open(pdf_path) as f_in:
            text = f_in.read()
        sections = text.split("\n\n\n")
        section_statistics(sections, var_sections_statistics)
    for it in var_sections_statistics.keys():
        SECTION_STATISTICS.append((var_sections_statistics[it], it))
    SECTION_STATISTICS.sort(reverse=True)


def show_section_statistics():
    for i in SECTION_STATISTICS:
        print(i)


def update_text_based_on_statistics_1(text):
    sections = text.split("\n\n\n")
    ackno = {
        "\x0cAcknowledgments", "\x0cAcknowledgements",
        "Acknowledgements", "Acknowledgments", "\x0cAcknowledgement",
        "Acknowledgment", "\x0cAcknowledgment"
    }
    for i in range(len(sections)):
        s = sections[i]
        mas = s.split("\n")
        name = mas[1]
        if name == "\x0cReferences":
            mas[1] = "References"
            var = "\n".join(mas)
            sections[i] = var
            continue
        if name in ackno:
            mas[1] = "Acknowledgements"
            var = "\n".join(mas)
            sections[i] = var
            continue
        if name == "\x0cMethod":
            mas[1] = "Method"
            var = "\n".join(mas)
            sections[i] = var
            continue
        if name == "\x0cModel":
            mas[1] = "Model"
            var = "\n".join(mas)
            sections[i] = var
            continue
        if name == "\x0cImages":
            mas[1] = "Images"
            var = "\n".join(mas)
            sections[i] = var
            continue
        if name == "\x0cDataset":
            mas[1] = "Dataset"
            var = "\n".join(mas)
            sections[i] = var
            continue
        if name == "\x0cData":
            mas[1] = "Data"
            var = "\n".join(mas)
            sections[i] = var
            continue
        if name == "\x0cInput":
            mas[1] = "Input"
            var = "\n".join(mas)
            sections[i] = var
            continue
        cnt = 0
        while cnt < len(name):
            if ord(name[cnt]) < 32 or ord(name[cnt]) > 127:
                cnt += 1
            else:
                break
        if cnt != 0:
            mas[1] = mas[1][cnt:]
            var = "\n".join(mas)
            sections[i] = var
        continue
    return "\n\n\n".join(sections)


def update_text_based_on_statistics_2(text):
    sections = text.split("\n\n\n")
    non_sections = {
        "31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA.",
        "log2(k)", "h (0)", "x10 4", "observed load", "log(m)", "Epsilon5", "800 1000 1200 1400 1600",
        "− 1−\x0f", "σAdept", "· 106", "cores", "Time [ms]", "Time (s)", "0.051", "# input triplets",
        "− zi z −1", "to N do", "minimize", "log(τ̂H (2m))", "log n", "X X yc", "O (N )", "Runtime (sec.)",
        "O(n 2 pT )", "O( (1−2η)", "Facebook AI Research", "Alan Turing Institute", "To summarize",
    }
    i = 1
    while i < len(sections):
        s = sections[i]
        mas = s.split("\n")
        name = mas[1]
        if name in non_sections:
            sections[i - 1] += "\n"
            sections[i - 1] += s
            sections.pop(i)
            continue
        i += 1
    return "\n\n\n".join(sections)


def update_text_based_on_statistics_3(text):
    sections = text.split("\n\n\n")
    i = 1
    while i < len(sections):
        s = sections[i]
        mas = s.split("\n")
        name = mas[1]
        if len(name) == 0:
            sections[i - 1] += "\n"
            sections[i - 1] += s
            sections.pop(i)
            continue
        if ord(name[0]) < 65 or ord(name[0]) > 90:
            sections[i - 1] += "\n"
            sections[i - 1] += s
            sections.pop(i)
            continue
        if name[0] == "X":
            sections[i - 1] += "\n"
            sections[i - 1] += s
            sections.pop(i)
            continue
        i += 1
    return "\n\n\n".join(sections)


def update_text_based_on_statistics_4(text):
    bad_start = {
        "Moreover, ", "More precisely, ", "More generally", "More formally", "More efficient algorithms exist",
        "Let ", "It is worth ", "It is also", "It can ", "However, ", "Here we ", "Further, ", "Furthermore, ",
        "For ", "Finally, we", "Due to", "Since ", "T ", "We "
    }
    sections = text.split("\n\n\n")
    i = 1
    while i < len(sections):
        s = sections[i]
        mas = s.split("\n")
        name = mas[1]
        for st in bad_start:
            if name.find(st) == 0:
                sections[i - 1] += "\n"
                sections[i - 1] += s
                sections.pop(i)
                i -= 1
                break
        i += 1
    return "\n\n\n".join(sections)


def update_text_based_on_statistics():
    var_sections_statistics = {}
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        pdf_path = 'OnlyText1/' + ref[29:-3] + "txt"
        with open(pdf_path) as f_in:
            text = f_in.read()
        text = update_text_based_on_statistics_1(text)
        text = update_text_based_on_statistics_2(text)
        text = update_text_based_on_statistics_3(text)
        text = update_text_based_on_statistics_4(text)
        write_text_to_file(text, pdf_path)
    for it in var_sections_statistics.keys():
        SECTION_STATISTICS.append((var_sections_statistics[it], it))
    SECTION_STATISTICS.sort(reverse=True)


def ask(name, number, prev):
    print(name, number, prev)
    print("Is header?")
    print()
    ans = int(input())
    if ans == 1:
        return True
    return False


def count_words(p):
    words = p.split()
    return len(words)


def count_numbers(p):
    res = 0
    for i in p:
        if i.isdigit():
            res += 1
    return res


def count_special(p):
    res = 0
    for i in p:
        if not i.isalpha() and i != " ":
            res += 1
    return res


def average_word_length(p):
    cnt = count_words(p)
    if cnt == 0:
        return 0
    words = p.split()
    total = 0
    for i in words:
        total += len(i)
    return total / cnt


def divide_text(text):
    prev = 0
    sections = text.split("\n\n\n")
    i = 1
    bad_start = {
        "Thus, ", "Throughout", "Though ", "This ", "There ", "Then ", "The following ", "That is, ",
        "Specifically, ", "So ", "See, ", "See ", "Remark ", "R ", "O ", "O(", "N ", "Lemma ", "K ", "It ",
        "In ", "If ", "Here ", "Here,", "Definition 1", "Definition 2", "By ", "C ", "As ", "Or ", "Theorem ",
        "To summarize", "Acc :", "W ( ", "Department of", "Write ", "Code is available at", "MNIST", "Input: ",
        "Hence 0"
    }
    flag = False
    while i < len(sections):
        s = sections[i]
        mas = s.split("\n")
        name = mas[1]
        number = int(mas[0])
        # print(prev)
        # print(number)
        # print(name)
        if number <= prev:
            sections[i - 1] += "\n"
            sections[i - 1] += s
            sections.pop(i)
            continue
        if name in POPULAR_SECTIONS:
            prev = number
            i += 1
            continue
        for b in bad_start:
            if name.find(b) == 0:
                sections[i - 1] += "\n"
                sections[i - 1] += s
                sections.pop(i)
                flag = True
                break
        if flag:
            flag = False
            continue
        if number - prev == 1:
            words = name.split()
            if len(words) <= 8:
                if count_numbers(name) <= 2:
                    if average_word_length(name) > 3:
                        if count_special(name) <= 4:
                            prev = number
                            i += 1
                            continue
        if number - prev <= 2 and sections[i].find(str(number) + "." + "1") != -1 \
                and sections[i].find(str(number) + "." + "2") != -1:
            prev = number
            i += 1
            continue
        if number - prev > 3:
            sections[i - 1] += "\n"
            sections[i - 1] += s
            sections.pop(i)
            continue
        words = name.split()
        if len(words) > 12:
            sections[i - 1] += "\n"
            sections[i - 1] += s
            sections.pop(i)
            continue
        if not ask(name, number, prev):
            sections[i - 1] += "\n"
            sections[i - 1] += s
            sections.pop(i)
            continue
        prev = number
        i += 1
    return "\n\n\n".join(sections)


def divide():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    cnt = 0
    for ref in articles_refs:
        if cnt > 100:
            break
        try:
            f = open("OnlyText2/" + ref[29:-3] + "txt")
            f.close()
            continue
        except:
            pdf_path = 'OnlyText1/' + ref[29:-3] + "txt"
        with open(pdf_path) as f_in:
            text = f_in.read()
        print(ref)
        text = divide_text(text)
        pdf_path = 'OnlyText2/' + ref[29:-3] + "txt"
        write_text_to_file(text, pdf_path)
        cnt += 1


def separate_ref(text):
    sections = text.split("\n\n\n")
    i = len(sections) - 1
    cut1 = sections[i].rfind("Bibliography")
    cut2 = sections[i].rfind("References")
    cut = max(cut1, cut2)
    if cut <= 15:
        return text
    part1 = sections[i][:cut]
    part2 = sections[i][cut:]
    sections.pop()
    sections.append(part1)
    sections.append(part2)
    return "\n\n\n".join(sections)


def separate_references():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("OnlyText3/" + ref[29:-3] + "txt")
            f.close()
            continue
        except:
            pdf_path = 'OnlyText2/' + ref[29:-3] + "txt"
        with open(pdf_path) as f_in:
            text = f_in.read()
        text = separate_ref(text)
        if text is None:
            continue
        pdf_path = 'OnlyText3/' + ref[29:-3] + "txt"
        write_text_to_file(text, pdf_path)


def separate_ack(text, ref):
    cut1 = text.find("\nAcknowledgement")
    if cut1 == -1:
        cut1 = text.find("\nAcknowledgment")
        if cut1 == -1:
            return text
        if text[cut1 + 1:].find("\nAcknowledgment") != -1:
            print(ref)
            return None
    else:
        if text[cut1 + 1:].find("\nAcknowledgment") != -1:
            print(ref)
            return None
        if text[cut1 + 1:].find("\nAcknowledgement") != -1:
            print(ref)
            return None
    sections = text.split("\n\n\n")
    i = 0
    while i < len(sections):
        cut = sections[i].find("\nAcknowledgement")
        if cut == -1:
            cut = sections[i].find("\nAcknowledgment")
            if cut == -1:
                i += 1
                continue
            if cut <= 15:
                return text
            else:
                part1 = sections[i][:cut]
                part2 = sections[i][cut:]
                sections.pop(i)
                sections.insert(i, part1)
                sections.insert(i + 1, part2)
                return "\n\n\n".join(sections)
        if cut <= 15:
            return text
        else:
            part1 = sections[i][cut:]
            part2 = sections[i][:cut]
            sections.pop(i)
            sections.insert(i, part1)
            sections.insert(i + 1, part2)
            return "\n\n\n".join(sections)
    return "\n\n\n".join(sections)


def separate_ackno():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("OnlyText4/" + ref[29:-3] + "txt")
            f.close()
            continue
        except:
            pdf_path = 'OnlyText3/' + ref[29:-3] + "txt"
        with open(pdf_path) as f_in:
            text = f_in.read()
        text = separate_ack(text, ref)
        if text is None:
            continue
        pdf_path = 'OnlyText4/' + ref[29:-3] + "txt"
        write_text_to_file(text, pdf_path)


def separate_intro(text, ref):
    cut = text.find("\nIntroduction")
    if cut == -1:
        return text
    if text[cut + 1:].find("\nIntroduction") != -1:
        print(ref)
        return None
    sections = text.split("\n\n\n")
    i = 0
    while i < len(sections):
        cut = sections[i].find("\nIntroduction")
        if cut == -1:
            i += 1
            continue
        if cut <= 15:
            return text
        else:
            part1 = sections[i][:cut]
            part2 = sections[i][cut:]
            sections.pop(i)
            sections.insert(i, part1)
            sections.insert(i + 1, part2)
            return "\n\n\n".join(sections)
    return "\n\n\n".join(sections)


def separate_introes():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        try:
            f = open("OnlyText5/" + ref[29:-3] + "txt")
            f.close()
            continue
        except:
            pdf_path = 'OnlyText4/' + ref[29:-3] + "txt"
        with open(pdf_path) as f_in:
            text = f_in.read()
        text = separate_ack(text, ref)
        if text is None:
            continue
        pdf_path = 'OnlyText5/' + ref[29:-3] + "txt"
        write_text_to_file(text, pdf_path)


def subsection_div(text):
    sections = text.split("\n\n\n")
    prev2 = 0
    for i in range(0, len(sections)):
        sec = sections[i]
        try:
            number = int(sec[0])
        except:
            number = None
        subsections = sec.split("\n\n")
        j = 1
        while j < len(subsections):
            subsec = subsections[j]
            n1 = int(subsec[0])
            n2 = int(subsec[2])
            if n1 == number:
                prev2 = n2
                j += 1
                continue
            if n2 == prev2 + 1:
                prev2 = n2
                j += 1
                continue
            if number is not None and n2 == 1 and n1 - number <= 2:
                prev2 = n2
                j += 1
                continue
            if n2 - prev2 >= 3:
                subsections[j - 1] += "\n"
                subsections[j - 1] += subsections[j]
                subsections.pop(j)
                continue
            else:
                if ask(subsec, n1, n2):
                    prev2 = n2
                    j += 1
                    continue
                else:
                    subsections[j - 1] += "\n"
                    subsections[j - 1] += subsections[j]
                    subsections.pop(j)
        sections[i] = "\n\n".join(subsections)
    return "\n\n\n".join(sections)


def subsection_division():
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    cnt = 0
    for ref in articles_refs:
        if cnt == 50:
            break
        try:
            f = open("OnlyText6/" + ref[29:-3] + "txt")
            f.close()
            continue
        except:
            pdf_path = 'OnlyText5/' + ref[29:-3] + "txt"
        with open(pdf_path) as f_in:
            text = f_in.read()
        print(ref)
        text = subsection_div(text)
        pdf_path = 'OnlyText6/' + ref[29:-3] + "txt"
        write_text_to_file(text, pdf_path)
        cnt += 1


def separate1(text, ref, header):
    cut = text.find("\n" + header + " ")
    if cut == -1:
        return text
    if text[cut + 1:].find("\n" + header + " ") != -1:
        print("found several", header + " ", ref)
        return text
    sections = text.split("\n\n\n")
    i = 0
    while i < len(sections):
        cut = sections[i].find("\n" + header + " ")
        if cut == -1:
            i += 1
            continue
        if cut <= 15:
            return text
        else:
            if sections[i][cut - 1].isdigit() and sections[i][cut - 2] == "." and sections[i][cut - 3].isdigit():
                print("is subsection", header, ref)
                return text
            if i == len(sections) - 1:
                if not ask(ref, header, sections[i][:30]):
                    return text
            part1 = sections[i][:cut]
            part2 = sections[i][cut + 1:]
            sections.pop(i)
            sections.insert(i, part1)
            sections.insert(i + 1, part2)
            print("partition occured", header, ref)
            return "\n\n\n".join(sections)
    return "\n\n\n".join(sections)


def separate(header):
    with open("./../articles_refs.json") as i_file:
        articles_refs = json.load(i_file)
    for ref in articles_refs:
        pdf_path = 'OnlyText7/' + ref[29:-3] + "txt"
        with open(pdf_path) as f_in:
            text = f_in.read()
        text = separate1(text, ref, header)
        pdf_path = 'OnlyText7/' + ref[29:-3] + "txt"
        write_text_to_file(text, pdf_path)


def section_processing():
    create_statistics()
    # show_section_statistics()
    update_text_based_on_statistics()
    create_statistics()
    show_section_statistics()
    for i in SECTION_STATISTICS:
        if i[0] < 6:
            break
        POPULAR_SECTIONS.add(i[1])
    divide()
    # Now we have OnlyText2
    separate_references()
    separate_ackno()
    separate_introes()
    subsection_division()
    # copy all files from OnlyText6 into OnlyText7
    section_to_div = {
        "Abstract", "Abstracts", "References", "Related Works.", "Related Works\n", "Conclusion.", "Conclusion\n",
        "Conclusions.", "Conclusions\n", "Related Work.", "Related Work\n", "Related work.", "Related work\n"
    }
    for i in section_to_div:
        print(i, "\n\n")
        separate(i)


def main():
    section_processing()


if __name__ == "__main__":
    main()

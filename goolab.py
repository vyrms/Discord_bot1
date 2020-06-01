import os

import requests
from dotenv import load_dotenv
from collections import Counter


def senryu(sentence):
    sentence = sentence.replace("\n", "").replace(" ", "").replace("　", "")

    # get the app id for goolab from .env
    load_dotenv()
    app_id = os.getenv("goolabo_id")

    # request to goo lab API
    r = requests.post("https://labs.goo.ne.jp/api/morph",
                      data={"app_id": app_id,
                            "sentence": sentence})

    # if goo lab API didn't return valid result
    if r.status_code != 200:
        return False, None

    # if we have an actual result from goo lab API
    separated = r.json()["word_list"][0]
    print(separated)

    for j in range(len(separated)):
        line_number = 0  # counts which line of haiku you are on
        syllables = 0
        senryu = ""

        # kinds of words to not begin with
        ignore = ["格助詞", "動詞接尾辞", "終助詞", "接続接尾辞",
                  "形容詞接尾辞", "連用助詞", "名詞接尾辞", "動詞活用語尾", "間投詞", "Kana"]
        punctuations = ["読点", "句点", "Symbol", "Undef"]
        if separated[j][1] in ignore or separated[j][1] in punctuations:
            continue

        # look in list for senryu
        for i in range(j, len(separated)):
            # look at individual words
            word = separated[i]
            length = len(word[2])
            senryu += word[0]

            # remove things that aren't syllables
            not_syllables = ["ァ", "ィ", "ゥ", "ェ", "ォ", "ャ", "ュ", "ョ", "゛", "゜"]
            for letter in not_syllables:
                counter = Counter(word[2])[letter]
                length -= counter
            syllables += length

            # count syllables and see if sentence contains a senryu
            if line_number == 0 and syllables > 5:
                break
            elif line_number == 0 and syllables == 5:
                if i + 1 <= len(separated):
                    if separated[i + 1][1] in ignore:
                        break
                    elif separated[i + 1][1] in punctuations:
                        continue
                line_number += 1
                syllables = 0
                senryu += "\n"

            elif line_number == 1 and syllables == 7 or syllables == 8:
                if i + 1 < len(separated):
                    if separated[i + 1][1] in ignore:
                        break
                    elif separated[i + 1][1] in punctuations:
                        continue
                line_number += 1
                syllables = 0
                senryu += "\n"

            elif line_number == 2 and syllables == 5:
                if i + 1 < len(separated):
                    if separated[i + 1][1] in ignore:
                        break
                print("haiku detected!")

                # save on mysql


                return True, senryu
    return False, None

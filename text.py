from pyknp import KNP
sentence = KNP(option='-tab').parse('ポット内の温度が１００℃より低い場合、水が沸騰しない。')
print([m.midasi for m in sentence.mrph_list()])
print(len(sentence.mrph_list()[0].midasi))
print(ord(sentence.mrph_list()[0].midasi[0]))
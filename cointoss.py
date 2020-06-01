import random


def cointoss(n=1):
    # for one toss
    if n == 1:
        toss = bool(random.getrandbits(1))
        if toss:
            return "表"
        return "裏"

    # for multiple tosses
    results = ""
    heads = 0
    tails = 0
    for i in range(n):
        toss = bool(random.getrandbits(1))
        if toss:
            results += "表 "
            heads += 1
        else:
            results += "裏 "
            tails += 1
    results += "\n表" + str(heads) + "\t裏" + str(tails)
    return results

# command for .dice


import random


def dice(n=1):
    # for one die
    if n == 1:
        return random.randint(1, 6)

    # for multiple dice rolls
    results = ""
    counts = [0, 0, 0, 0, 0, 0]
    for i in range(n):
        die = random.randint(1, 6)
        results += str(die) + " "
        counts[die - 1] += 1

    for i in range(len(counts)):
        results += "\n" + str(i + 1) + ": " + str(counts[i])

    return results

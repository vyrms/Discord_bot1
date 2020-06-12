# bot chooses from choices given


import random


# syntax = .choose choice1;choice2
def choose(command=""):
    # tidy the command
    command = command.strip(".choose ")
    choices = command.split(";")
    print(choices)

    if choices[0] == "":
        print("error")
        return "入力ミスした？こんな感じで入力してね！\n" \
               ".choose 選択肢1;選択肢2"

    # choose one
    idx = random.randint(0, len(choices) - 1)

    return choices[idx]

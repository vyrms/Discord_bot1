# command for .teach and speaking


import re
import random

from sql_connect import DBcon


# .teach
def learn(command="", guild_id=0):
    # try to connect to the database
    dbcon = DBcon(guild_id)

    try:
        # tidy the command
        command = command.strip(".teach").strip(" ").strip("　").strip("\"")
        command = re.split("\"", command, 1)
        command[0] = command[0].strip(" ").strip("　")

        # see if the trigger is a duplicate
        sql = f"select * from vocab where trig = \'{command[0]}\'"
        dbcon.cur.execute(sql)
        orig = dbcon.cur.fetchall()
        if len(orig) != 0:
            # see if there are the same responses already, and keep non-dupes in nondupes
            orig = orig[0][2]
            new = [word for word in command[1].split(";") if word not in orig]
            nondupes = ";".join(new) + ";" + orig
            nondupes = nondupes.strip(";")

            # if all the new responses are already there
            if len(new) == 0:
                return "その返事はもう覚えたよ！"

            # save to database
            sql = f"update vocab set resp = \'{nondupes}\' where trig = \'{command[0]}\'"
            dbcon.cur.execute(sql)
            dbcon.cnx.commit()

            # response to discord
            output = f"その言葉の返事はもうあったけど、がんばって追加で覚えたよ！\n" \
                     f"言葉：「{command[0]}」返事：「{nondupes}」\nを覚えました！"
            return output

        # save to database
        sql = f"insert into vocab (trig, resp) values (\'{command[0]}\', \'{command[1]}\')"
        dbcon.cur.execute(sql)
        dbcon.cnx.commit()

        # response
        output = f"言葉：「{command[0]}」返事：「{command[1]}」\nを覚えました！"
        return output

    # if the command input was in some weird form
    except IndexError:
        return "入力ミスした？\n" \
               "↓こんな感じで入力してね！\n" \
               ".teach えらい \"えへへへ;ありがと！\""


# finds trigger words
def speak(message="", guild_id=0):
    # try to connect to the database
    dbcon = DBcon(guild_id)

    # look in database for the trig word
    sql = f"select * from vocab"
    dbcon.cur.execute(sql)
    speak_data = dbcon.cur.fetchall()

    # find matching trigger
    keep = []
    for line in speak_data:
        if line[1] in message:
            keep.append(line)

    # if no words match
    if len(keep) == 0:
        return

    # find which trigger is longest
    chosen = max(keep, key=lambda i: len(i[1]))

    # pick randomly if there are choices
    resp = chosen[2].split(";")
    idx = random.randint(0, len(resp) - 1)
    return resp[idx]


# .forget 言葉
def forget(command="", guild_id=0):
    # try to connect to the database
    dbcon = DBcon(guild_id)

    # tidy the command
    word = command.strip(".forget").strip(" ").strip("　")

    # see if the word is not in database
    sql = f"select trig from vocab"
    dbcon.cur.execute(sql)
    triggers = dbcon.cur.fetchall()
    triggers = [tup[0] for tup in triggers]
    if word not in triggers:
        return f"{word}？知らない子ですね…"

    # delete from database
    sql = f"delete from vocab where trig = \'{word}\'"
    dbcon.cur.execute(sql)
    dbcon.cnx.commit()

    return f"321ポカン！\n言葉：{word}を忘れたよ！"


# .vocab
def see_vocab(guild_id=0):
    # try to connect to the database
    dbcon = DBcon(guild_id)

    # get index, trigger, and response from database
    sql = "select * from vocab"
    dbcon.cur.execute(sql)
    data = dbcon.cur.fetchall()
    print(data)

    if len(data) == 0:
        return "うへぇ！なんも覚えてねぇや！"

    output = "\n".join(list("\t".join(map(str, tup)) for tup in data))
    return output

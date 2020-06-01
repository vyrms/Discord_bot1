import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

# import my own functions from other .py files
from cointoss import cointoss
from senryu import *
from dice import dice
from sql_connect import *


# make a .env file with the tokens and IDs needed

# botのトークン
load_dotenv()
token = os.getenv('discord_token')

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    guilds = client.guilds
    # creates mysql database and tables for all servers (if necessary)
    for guild in guilds:
        dbcon = DBcon(guild.id)
        dbcon.table_maker()

    # 起動したらターミナルにログイン通知が表示される
    channel = client.get_channel(712433049845104690)
    print('Logged on as', client.user)
    await channel.send("オン")


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # if they want cointoss
    elif message.content.startswith(".coin"):
        n = message.content.replace(".coin", "").strip(" ")
        if n == "":
            await message.channel.send(cointoss())
        else:
            try:
                await message.channel.send(cointoss(int(n)))
            except ValueError:
                errormsg = "入力ミスした？\n" \
                           "こんな感じで入力してね！→ .coin 5"
                await message.channel.send(errormsg)
        return

    # if they want dice
    elif message.content.startswith(".dice"):
        n = message.content.replace(".dice", "").strip(" ")
        if n == "":
            await message.channel.send(dice())
        else:
            try:
                await message.channel.send(dice(int(n)))
            except ValueError:
                errormsg = "入力ミスした？\n" \
                           "こんな感じで入力してね！→ .dice 5"
                await message.channel.send(errormsg)
        return

    # 「/neko」と発言したら「にゃーん」が返る処理
    elif message.content == '/neko':
        await message.channel.send('にゃーん')
        return

    # test if it's a senryu
    result = senryu_detect(message.content, message.author, message.guild.id)
    if result is not None:
        await message.channel.send(result)

    # reads a senryu
    triggers = ["詠め", "ハイク", "俳句", "川柳"]
    for trigger in triggers:
        if trigger in message.content:
            senryu = senryu_say(message.guild.id)
            await message.channel.send(senryu)
            break


# リアクション追加時に実行されるイベントハンドラ
@client.event
async def on_reaction_add(reaction, user):
    pass


"""新規メンバー参加時に実行されるイベントハンドラ"""
@client.event
async def on_member_join(member):
    pass


# Botの起動とDiscordサーバーへの接続
client.run(token)
import os

import discord
from dotenv import load_dotenv

from cointoss import cointoss
from goolab import senryu


# botのトークン
load_dotenv()
token = os.getenv('discord_token')

# 接続に必要なオブジェクトを生成
client = discord.Client()


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    channel = client.get_channel(712433049845104690)
    print("オン")
    await channel.send("オン")


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # if they want cointoss
    elif message.content.startswith(".coin"):
        await message.channel.send(cointoss(message.content))

    # 「/neko」と発言したら「にゃーん」が返る処理
    elif message.content == '/neko':
        await message.channel.send('にゃーん')

    # test if it's a senryu
    result = senryu(message.content)
    if result[0]:
        await message.channel.send(result[1])


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
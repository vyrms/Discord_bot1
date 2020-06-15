import discord
import discord.errors

# import my own functions from other .py files
from functions.cointoss import cointoss
from functions.APIs.senryu import *
from functions.dice import dice
from functions.sql_connect import DBcon
from functions.help import help_message
from functions.learn_speak import learn, speak, forget, see_vocab
from functions.uranai import unsei
from functions.APIs.wiki import wiki_suggest, wiki_search
from functions.choose import choose
from functions.calculator import integral, derivative, calc


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
        dbcon.db_maker()
        dbcon.table_maker()
        dbcon.close()

    # 起動したらターミナルにログイン通知が表示される
    channel = client.get_channel(712433049845104690)
    print('Logged on as', client.user)
    await channel.send("オン")


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    try:
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return

        # if they want help
        elif message.content.startswith(".help"):
            await message.channel.send(help_message())

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

        # 「.neko」と発言したら「にゃーん」が返る処理
        elif message.content == '.neko':
            await message.channel.send('にゃーん')
            return

        # make suggestions about what they want to search
        elif message.content.startswith(".wikisuggest"):
            await message.channel.send(wiki_suggest(message.content))
            return

        # search wikipedia for top hit
        elif message.content.startswith(".wikisearch"):
            await message.channel.send(wiki_search(message.content))
            return

        # integrate
        elif message.content.startswith(".integrate"):
            await message.channel.send(integral(message.content))
            return

        # derive
        elif message.content.startswith(".derive"):
            await message.channel.send(derivative(message.content))
            return

        # calculate
        elif message.content.startswith(".calc"):
            await message.channel.send(calc(message.content))
            return

        # if they want to teach
        elif message.content.startswith(".teach"):
            await message.channel.send(learn(message.content, message.guild.id))
            return

        # if they want bot to forget a word
        elif message.content.startswith(".forget"):
            await message.channel.send(forget(message.content, message.guild.id))
            return

        # if they want to see the bot vocab
        elif message.content.startswith(".vocab"):
            await message.channel.send(see_vocab(message.guild.id))
            return

        # respond to 今日の運勢
        elif "今日の運勢" in message.content:
            await message.channel.send(unsei())
            return

        # .choose function
        elif message.content.startswith(".choose"):
            await message.channel.send(choose(message.content))
            return

        # respond to certain words that are taught
        result = speak(message.content, message.guild.id)
        if result is not None:
            await message.channel.send(result)
            return

        # test if it's a senryu
        result = senryu_detect(message.content, message.author, message.guild.id)
        if result is not None:
            await message.channel.send(result)
            return

        # read a senryu
        triggers = ["詠め", "ハイク", "俳句", "川柳"]
        for trigger in triggers:
            if trigger in message.content:
                senryu = senryu_say(message.guild.id)
                await message.channel.send(senryu)
                return

    except discord.errors.HTTPException as err:
        await message.channel.send("エラーだよ！お返事の文字数が多すぎてディスコくんに怒られちゃった！")
        return


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
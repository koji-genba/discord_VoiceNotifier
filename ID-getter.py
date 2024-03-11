import discord

client = discord.Client(intents=discord.Intents.all())

# 起動時処理
@client.event
async def on_ready():
    for channel in client.get_all_channels():
        print("----------")
        print("チャンネル名:" + str(channel.name))
        print("チャンネルID:" + str(channel.id))
        print("----------")
# Botのトークンを指定（デベロッパーサイトで確認可能）
client.run("TOKEN")
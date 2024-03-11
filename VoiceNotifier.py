import discord
from discord.ext import commands
from discord import app_commands
import json

# ボットの設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# チャンネルの設定を保存するファイル名
CONFIG_FILE = 'channel_config.json'

# チャンネル設定を読み込む関数
def load_channel_config():
    try:
        with open(CONFIG_FILE, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return {}

# チャンネル設定を保存する関数
def save_channel_config(config):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file, indent=4)

# ボイスチャンネルの入退室を監視するイベント
@bot.event
async def on_voice_state_update(member, before, after):
    config = load_channel_config()
    guild_id = str(member.guild.id)
    if guild_id in config:
        # 退室通知
        if before.channel is not None and before.channel.id in config[guild_id]['voice_channels'] :
            text_channel = bot.get_channel(config[guild_id]['text_channel'])
            if member.nick != None:
                await text_channel.send("["+ before.channel.name +"]:red_circle:" + member.nick)
            elif member.display_name != None:
                await text_channel.send("["+ before.channel.name +"]:red_circle:" + member.display_name)
            else:
                await text_channel.send("["+ before.channel.name +"]:red_circle:" + member.name)
        
        # 入室通知
        if after.channel is not None and after.channel.id in config[guild_id]['voice_channels']:
            text_channel = bot.get_channel(config[guild_id]['text_channel'])
            if member.nick != None:
                await text_channel.send("["+ after.channel.name +"]:green_circle:" + member.nick)
            elif member.display_name != None:
                await text_channel.send("["+ after.channel.name +"]:green_circle:" + member.display_name)
            else:
                await text_channel.send("["+ after.channel.name +"]:green_circle:" + member.name)
        
# スラッシュコマンドを使用して監視するボイスチャンネルを追加するコマンド
@bot.tree.command()
@app_commands.describe(voice_channel='監視するボイスチャンネル')
async def add_voice_channel(interaction: discord.Interaction, voice_channel: discord.VoiceChannel):
    config = load_channel_config()
    guild_id = str(interaction.guild_id)
    if guild_id not in config:
        config[guild_id] = {'voice_channels': [], 'text_channel': None}
    config[guild_id]['voice_channels'].append(voice_channel.id)
    save_channel_config(config)
    await interaction.response.send_message(f'ボイスチャンネル{voice_channel.name}を監視リストに追加しました。')
    print(config)

# スラッシュコマンドを使用して通知を送信するテキストチャンネルを設定するコマンド
@bot.tree.command()
@app_commands.describe(text_channel='通知を送信するテキストチャンネル')
async def set_text_channel(interaction: discord.Interaction, text_channel: discord.TextChannel):
    config = load_channel_config()
    guild_id = str(interaction.guild_id)
    
    # ギルドIDに対応する設定がなければ新しく作成
    if guild_id not in config:
        config[guild_id] = {'voice_channels': [], 'text_channel': None}
    
    # 以前に設定されたテキストチャンネルがあれば通知
    old_text_channel_id = config[guild_id].get('text_channel')
    if old_text_channel_id is not None:
        old_text_channel = bot.get_channel(old_text_channel_id)
        if old_text_channel:
            await old_text_channel.send(f'通知チャンネルが{text_channel.name}に変更されました。')
    
    # 新しいテキストチャンネルを設定
    config[guild_id]['text_channel'] = text_channel.id
    save_channel_config(config)
    await interaction.response.send_message(f'通知を送信するテキストチャンネルを{text_channel.name}に設定しました。')

# ヘルプコマンド
# スラッシュコマンドを使用してコマンドの使い方を表示するコマンド
@bot.tree.command()
@app_commands.describe(command='説明を表示するコマンド')
async def man(interaction: discord.Interaction, command: str):
    # コマンドの説明を格納する辞書
    command_descriptions = {
        'add_voice_channel': 'ボイスチャンネルを監視リストに追加します。使用方法: /add_voice_channel [ボイスチャンネル]',
        'set_text_channel': '通知を送信するテキストチャンネルを設定します。既に指定されている場合は置き換えられます。使用方法: /set_text_channel [テキストチャンネル]',
        'remove_voice_channel': '監視リストからボイスチャンネルを削除します。使用方法: /remove_voice_channel [ボイスチャンネル]',
    }
    
    # 指定されたコマンドの説明を取得
    description = command_descriptions.get(command)
    
    # 説明が見つかった場合は表示、見つからない場合はエラーメッセージを表示
    if description:
        await interaction.response.send_message(description)
    else:
        await interaction.response.send_message(f'コマンド"{command}"の説明が見つかりません。')


# スラッシュコマンドを使用して監視するボイスチャンネルを削除するコマンド
@bot.tree.command()
@app_commands.describe(voice_channel='削除するボイスチャンネル')
async def remove_voice_channel(interaction: discord.Interaction, voice_channel: discord.VoiceChannel):
    config = load_channel_config()
    guild_id = str(interaction.guild_id)
    if guild_id in config and voice_channel.id in config[guild_id]['voice_channels']:
        config[guild_id]['voice_channels'].remove(voice_channel.id)
        save_channel_config(config)
        await interaction.response.send_message(f'ボイスチャンネル{voice_channel.name}を監視リストから削除しました。')
    else:
        await interaction.response.send_message(f'ボイスチャンネル{voice_channel.name}は監視リストに存在しません。')
    print(config)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    new_activity = f"スラッシュコマンド実装中……" 
    await bot.change_presence(activity=discord.Game(new_activity)) 
    # スラッシュコマンドを同期 
    await bot.tree.sync()

# サーバに招待された時のやつ
@bot.event
async def on_guild_join(guild):
    # デフォルトのテキストチャンネルを見つける
    default_channel = next((channel for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages), None)
    
    # 歓迎メッセージを送信
    if default_channel:
        await default_channel.send(f'こんにちは！{guild.name}サーバーに招待していただきありがとうございます！コマンドの使い方については、`/man [コマンド名]` を使用してください。\nコマンドは次の3つです。\n`/set_text_channel`\n`/add_voice_channel`\n`/remove_voice_channel`')


# ボットのトークンを設定
bot.run("Here TOKEN")

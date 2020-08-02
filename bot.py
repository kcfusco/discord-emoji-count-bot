# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    servers = discord.utils.get(client.guilds)
    print(
        f'{client.user.name} has connected to Discord!\n'
        f'Connected servers:\n {servers}'
    )


@client.command(name='total', help='Returns how many times each emoji has been used, in descending order.')
async def emojitotal(ctx):
    # api reads emojis as '<:boombalul:662342993084153856>'
    emoji_count = {}
    emoji_list = []
    # ctx.guild returns [<Guild id=638479828089307207 name='Testing' shard_id=None chunked=True member_count=3>]
    for emoji in ctx.guild.emojis:
        emoji_count.setdefault(str(emoji), 0)
    if isinstance(ctx.channel, discord.TextChannel):
        async for message in ctx.channel.history(limit=50000):
            if message.author != client.user:
                emoji_iter = re.finditer("<:[^:]+:([0-9]+)>", message.content)
                emoji_list.append([str(emoji_id.group(0)) for emoji_id in emoji_iter])

            for reaction in message.reactions:
                if str(reaction.emoji) in emoji_count:
                    emoji_count[str(reaction.emoji)] += reaction.count

    new_emoji_list = list(filter(None, emoji_list))
    flat_list = [item for sublist in new_emoji_list for item in sublist]
    for f in flat_list:
        for k in emoji_count.keys():
            if f == k:
                emoji_count[k] += 1
    # anonymous func applied to each element in emoji_count list as criteria for sorting
    sorted_emoji_count = {k: v for k, v in sorted(emoji_count.items(), key=lambda item: item[1], reverse=True)}
    emojis_list = list(sorted_emoji_count.items())
    await ctx.send(emojis_list[0:5])


@client.command(name='remove', help='Returns the least used emoji in the server (Excludes animated emojis)')
async def emojiremove(ctx):
    # api reads emojis as '<:boombalul:662342993084153856>'
    emoji_count = {}
    emoji_list = []
    # ctx.guild returns [<Guild id=638479828089307207 name='Testing' shard_id=None chunked=True member_count=3>]
    for emoji in ctx.guild.emojis:
        emoji_count.setdefault(str(emoji), 0)
    if isinstance(ctx.channel, discord.TextChannel):
        async for message in ctx.channel.history(limit=50000):
            if message.author != client.user:
                emoji_iter = re.finditer("<:[^:]+:([0-9]+)>", message.content)
                emoji_list.append([str(emoji_id.group(0)) for emoji_id in emoji_iter])

            for reaction in message.reactions:
                if str(reaction.emoji) in emoji_count:
                    emoji_count[str(reaction.emoji)] += reaction.count

    new_emoji_list = list(filter(None, emoji_list))
    flat_list = [item for sublist in new_emoji_list for item in sublist]
    for f in flat_list:
        for k in emoji_count.keys():
            if f == k:
                emoji_count[k] += 1
    # anonymous func applied to each element in emoji_count list as criteria for sorting
    sorted_emoji_count = {k: v for k, v in sorted(emoji_count.items(), key=lambda item: item[1], reverse=True)}
    emojis_list = list(sorted_emoji_count.items())
    await ctx.send(emojis_list[-14:-8])
# may not work properly with animated emojis, not being picked up when searching channel history

# TODO: implement command for choosing ideal emoji for removal based on usage and emoji usage by user
@client.command(name='user', help="WIP - Returns each user's most used emoji, in descending order. - WIP")
async def emojiuser(ctx):
    response = 'Most used emojis by USER'
    await ctx.send(response)


client.run(TOKEN)

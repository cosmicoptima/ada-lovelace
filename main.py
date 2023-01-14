from cequesting import interpret_quest_command
from common import *

import discord

table = db['points']


@client.event
async def on_ready():
    channel = client.get_channel(SPECIFIC_CHANNEL)
    await channel.send('I am ready!')


@client.event
async def on_message(message):
    if message.content.startswith('ada give '):
        if message.author.id == CELESTE:
            user = message.mentions[0]
            amount = int(message.content.split(' ')[-1])

            await give_points(user, amount)
            await poast(message.channel, f'gave {user.mention} {amount}CP. current CP: {get_points(user)}')
        else:
            await poast(message.channel, 'you are not celeste <:threat:1058682393956978688>')

    elif message.content.startswith('ada get '):
       user = message.mentions[0]
        points = get_points(user)
        if points < 0:
            await poast(message.channel, f'{user.mention} has {points}CP <:owned:1062177746723278929>')
        else:
            await poast(message.channel, f'{user.mention} has {points}CP')

    elif message.content == "ada help":
        await poast(message.channel, "there is no he;lp for you")

    elif message.content.startswith('ada quest '):
        await interpret_quest_command(message)

    elif message.content.startswith('ada '):
        await poast(message.channel, f'What')

    # +1 for petting celeste
    elif message.content == "!celeste pet":
        if message.author.id == CELESTE:
            await poast(message.channel, "that is pathetic")
        elif message.channel.type != discord.ChannelType.private:
            await give_points(message.author, 1)
            await poast(message.channel, f':3  {message.author.mention} has {get_points(message.author)}CP')


def get_points(user):
    current = table.find_one(user_id=user.id)
    current = 0 if current is None else current['points']

    return current


client.run(DISCORD_BOT_TOKEN)

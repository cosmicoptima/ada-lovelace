from common import *

import discord

table = db['points']
quests_table = db['quests___x3']


@client.event
async def on_ready():
    channel = client.get_channel(SPECIFIC_CHANNEL)
    await channel.send('I am ready!')


@client.event
async def on_message(message):
    if message.author.id == IAN:
        return

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

    elif message.content.startswith('ada quest add '):
        # ada quest add "<name>" <points>
        if message.author.id == CELESTE:
            name = message.content.split('"')[1]
            points = int(message.content.split(' ')[-1])

            quests_table.insert(dict(name=name, points=points))
            await poast(message.channel, f'added quest "{name}" worth {points}CP')
        else:
            await poast(message.channel, 'you are not celeste :threat:1058682393956978688>')

        await render_questlog()
    elif message.content.startswith('ada quest fulfill '):
        # ada quest fulfill "<name>" <user>
        if message.author.id == CELESTE:
            name = message.content.split('"')[1]
            user = message.mentions[0]

            quest = quests_table.find_one(name=name)
            if quest is None:
                await poast(message.channel, f'What!?!? There is no quest called "{name}"')
            else:
                await give_points(user, quest['points'])
                await poast(message.channel, f'gave {user.mention} {quest["points"]}CP for completing "{name}"')
                quests_table.delete(name=name)
        else:
            await poast(message.channel, 'you are not celeste <:threat:1058682393956978688>')

        await render_questlog()
    elif message.content.startswith('ada quest remove '):
        # ada quest remove "<name>"
        if message.author.id == CELESTE:
            name = message.content.split('"')[1]

            quest = quests_table.find_one(name=name)
            if quest is None:
                await poast(message.channel, f'What!?!?????!I')
            else:
                quests_table.delete(name=name)
                await poast(message.channel, f'removed quest "{name}"')
        else:
            await poast(message.channel, 'you are not celeste <:threat:1058682393956978688>')

        await render_questlog()

    elif message.content.startswith('ada '):
        await poast(message.channel, f'What')

    # +1 for petting celeste
    elif message.content == "!celeste pet":
        if message.author.id == CELESTE:
            await poast(message.channel, "that is pathetic")
        elif message.channel.type != discord.ChannelType.private:
            await give_points(message.author, 1)
            await poast(message.channel, f':3  {message.author.mention} has {get_points(message.author)}CP')

    # -1 for petting ian
    elif message.content == "!ian pet":
        if message.author.id == IAN:
            await poast(message.channel, "wow based")
        elif message.channel.type != discord.ChannelType.private:
            await give_points(message.author, -1)
            await poast(message.channel, f'no!  {message.author.mention} has {get_points(message.author)}CP')


async def render_questlog():
    # set QUESTLOG_POST in LEADERBOARD_CHANNEL to questlog
    channel = client.get_channel(LEADERBOARD_CHANNEL)
    post = await channel.fetch_message(QUESTLOG_POST)

    quests = quests_table.all()
    quests = sorted(quests, key=lambda x: x['points'], reverse=True)

    # in a code block
    text = '```\n'
    for quest in quests:
        text += f'{quest["name"]} - {quest["points"]}CP\n'
    text += '```'

    await post.edit(content=text)


def get_points(user):
    current = table.find_one(user_id=user.id)
    current = 0 if current is None else current['points']

    return current


client.run(DISCORD_BOT_TOKEN)

import discord
from common import CELESTE, DISCORD_BOT_TOKEN, SPECIFIC_CHANNEL, LEADERBOARD_CHANNEL, LEADERBOARD_POST, db, client
table = db['points']


@client.event
async def on_ready():
    channel = client.get_channel(SPECIFIC_CHANNEL)
    await channel.send('I am ready!')


@client.event
async def on_message(message):
    if message.content.startswith('!cp give '):
        if message.author.id == CELESTE:
            user = message.mentions[0]
            amount = int(message.content.split(' ')[-1])

            await give_points(user, amount)
            await message.channel.send(f'gave {user.mention} {amount} CELESTE POINTS. current CELESRE POINTS: {get_points(user)}.')
        else:
            await message.channel.send('You are not Celeste <:threat:1058682393956978688>')
    elif message.content.startswith('!cp get '):
        user = message.mentions[0]
        points = get_points(user)
        if points < 0:
            await message.channel.send(f'{user.mention} has {points} CELESTE POINTS <:owned:1062177746723278929>')
        else:
            await message.channel.send(f'{user.mention} has {points} CELESTE POINTS')
    elif message.content == "!cp help":
        await message.channel.send("There is no he;lp for you")
    elif message.content.startswith('!cp quest'):
        from cequests import interpret_queste_command
        await interpret_queste_command(message)
    elif message.content.startswith('!cp '):
        await message.channel.send(f'What')

    # +1 for petting celeste
    elif message.content == "!celeste pet":
        if message.author.id == CELESTE:
            await message.channel.send("that is pathetic")
        elif message.channel.type != discord.ChannelType.private:
            await give_points(message.author, 1)
            await message.channel.send(f':3  {message.author.mention} has {get_points(message.author)} CEGKESTE POINTS')


async def render_leaderboard():
    sorted_points = sorted(table, key=lambda x: x['points'], reverse=True)
    # returns a code block with two columns, points and user; padded
    return '```\n' + '\n'.join([f'{row["points"]:>8} {client.get_user(row["user_id"]).name}' for row in sorted_points]) + '```'


async def give_points(user, amount):
    current = table.find_one(user_id=user.id)
    if current is None:
        current = 0
    else:
        current = current['points']

    table.upsert({'user_id': user.id, 'points': current + amount}, ['user_id'])

    channel = client.get_channel(LEADERBOARD_CHANNEL)
    post = await channel.fetch_message(LEADERBOARD_POST)
    await post.edit(content=await render_leaderboard())


def get_points(user):
    current = table.find_one(user_id=user.id)
    if current is None:
        current = 0
    else:
        current = current['points']

    return current


client.run(DISCORD_BOT_TOKEN)

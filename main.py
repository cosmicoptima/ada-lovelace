import dataset
import discord
from dotenv import load_dotenv
from os import environ

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

db = dataset.connect('sqlite:///data.db')
table = db['points']

CELESTE = 140541286498304000
LEADERBOARD_CHANNEL = 1062244958477750344
LEADERBOARD_POST = 1062245394152685618
SPECIFIC_CHANNEL = 1039267300412493856


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
            await message.channel.send(f'Gave {user.mention} {amount} points. Current points: {get_points(user)}.')
        else:
            await message.channel.send('You are not Celeste <:threat:1058682393956978688>')
    elif message.content.startswith('!cp get '):
        user = message.mentions[0]
        await message.channel.send(f'{user.mention} has {get_points(user)} points.')
    elif message.content.startswith('!cp '):
        await message.channel.send(f'What')


async def render_leaderboard():
    # returns code block with leaderboard
    sorted_points = sorted(table, key=lambda x: x['points'], reverse=True)
    body = '\n'.join([f'{client.get_user(row["user_id"]).name}: {row["points"]}' for row in sorted_points])
    return f'```\n{body}```'


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
    current = table.find_one(user_id=user.id)['points']
    if current is None:
        current = 0

    return current



client.run(environ['DISCORD_BOT_TOKEN'])

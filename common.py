import dataset
import discord
from os import environ
from dotenv import load_dotenv
db = dataset.connect('sqlite:///data.db')

load_dotenv()

DISCORD_BOT_TOKEN = environ['DISCORD_BOT_TOKEN']
CELESTE = int(environ['CELESTE'])
LEADERBOARD_CHANNEL = int(environ['LEADERBOARD_CHANNEL'])
LEADERBOARD_POST = int(environ['LEADERBOARD_POST'])
SPECIFIC_CHANNEL = int(environ['SPECIFIC_CHANNEL'])
QUESTLOG_POST = int(environ['QUESTLOG_POST'])

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)


async def give_points(user, amount):
    current = db['points'].find_one(user_id=user.id)
    if current is None:
        current = 0
    else:
        current = current['points']

    db['points'].upsert(
        {'user_id': user.id, 'points': current + amount}, ['user_id'])

    channel = client.get_channel(LEADERBOARD_CHANNEL)
    post = await channel.fetch_message(LEADERBOARD_POST)
    await post.edit(content=await render_leaderboard())


async def render_leaderboard():
    sorted_points = sorted(
        db['points'], key=lambda x: x['points'], reverse=True)
    # returns a code block with two columns, points and user; padded
    return '```\n' + '\n'.join([f'{row["points"]:>8} {client.get_user(row["user_id"]).name}' for row in sorted_points]) + '```'

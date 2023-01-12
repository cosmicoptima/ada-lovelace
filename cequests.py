from common import db, give_points, client, LEADERBOARD_CHANNEL, QUESTLOG_POST
from random import random

table = db['quests']
points = db['points']


async def interpret_queste_command(message) -> None:
    if message.content.startswith('!cp quest add'):
        await add_queste(message)
    elif message.content.startswith('!cp quest remove'):
        await remove_queste(message)
    elif message.content.startswith('!cp quest fulfill'):
        await fulfill_queste(message)
    await update_questelog()


async def add_queste(message) -> None:
    args = message.content.split()[3:]
    if len(args) == 2:
        table.insert(
            dict(title=args[0], description=None, bounty=float(args[1])))
        await message.channel.send(f'CEQUESTE ESTABLIMSHED: {args[0]}')
    elif len(args) == 3:
        table.insert(
            dict(title=args[0], description=args[1], bounty=float(args[2])))
        await message.channel.send(f'CEQUESTE ESTABLIMSHED: {args[0]}')
    else:
        # random chance to be helpful
        if random() > 0.5:
            await message.channel.send(f'Usage: !cp quest add "<title>" "[description]" <amount>')
            await message.channel.send(f'Don\'t forget the quotes!')
        else:
            await message.channel.send(f'dumbass')


async def remove_queste(message) -> None:
    args = message.content.split()[3:]
    if len(args) != 1:
        if random() > 0.5:
            await message.channel.send(f'Usage: !cp quest remove "<title>"')
            await message.channels.send(f'Don\'t forget the quotes!')
        else:
            await message.channel.send(f'idiiot')
    else:
        title = args[0]
        quest = table.find_one(title)
        if quest == None:
            await message.channel.send(f'Removed nonexistend cequeste "{title}"')
        else:
            table.delete(title=title)
            await message.channel.send(f'Removed cequeste "{title}"')


async def fulfill_queste(message) -> None:
    args = message.content.split()[3:]
    if len(args) != 2:
        if random() > 0.5:
            await message.channel.send(f'Usage: !cp quest fulfill "<title>" "<user>"')
            await message.channels.send(f'Don\'t forget the quotes!')
        else:
            await message.channel.send(f'why did you thnk that would work')
    else:
        title = args[0]
        user = message.mentions[0]
        quest = table.find_one(title=title)
        if quest == None:
            await message.channel.send(f'Fulfilled fake cequetse "{title}"')
        else:
            user_row = points.find_one(user_id=user.id)
            if user_row == None:
                await message.channel.send(f'That user dosent even exist lol')
            else:
                bounty = quest['bounty']
                table.delete(title=title)
                await give_points(user, float(quest['bounty']))
                await message.channel.send(f'Rewarded {user.name} {bounty} CESTESLER POINTS for completing quest "{title}"')


def stringify_queste(quest) -> str:
    title = quest['title']
    description = quest['description'] or 'A mysterious quest'
    bounty = quest['bounty']
    return f'{title}\n{description}\nBounty: {bounty} Clsetere Points'


async def update_questelog() -> None:
    quests = table.all()
    quest_lines = [stringify_queste(quest) for quest in quests]
    message = '```\n' + 'Cequeste Log\n' + '\n'.join(quest_lines) + '\n```'
    channel = client.get_channel(LEADERBOARD_CHANNEL)
    post = await channel.fetch_message(QUESTLOG_POST)
    await post.edit(content=message)

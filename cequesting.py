# TODO fix

from common import *

import discord
import random
import re
from typing import List, Tuple

quests = db['quests']
points = db['points']


async def interpret_quest_command(message):
    if message.content.startswith('ada quest add'):
        await add_quest(message)
    elif message.content.startswith('ada quest remove'):
        await remove_quest(message)
    elif message.content.startswith('ada quest fulfill'):
        await fulfill_quest(message)

    await update_questlog()


async def add_quest(message):
    args = parse_add_quest_args(message)
    if args == None:
        # random chance to be helpful
        if random.random() > 0.5:
            await poast(f'Usage: ada quest add "<title>" "[description]" <amount>')
            await poast(f'Don\'t forget the quotes!')
        else:
            await poast(f'dumbass')
    elif len(args) == 2:
        quests.insert(
            dict(title=args[0], description=None, bounty=float(args[1])))
        await poast(f'CEQUESTE ESTABLIMSHED: {args[0]}')
    else:
        quests.insert(
            dict(title=args[0], description=args[1], bounty=float(args[2])))
        await poast(f'CEQUESTE ESTABLIMSHED: {args[0]}')


def parse_add_quest_args(message) -> List[str] | None:
    pattern = r'ada quest add "([^"]+)" ("([^"]+)" )?(\d+\.?\d*)'
    args = re.match(pattern, message.content)
    if args == None:
        return None
    elif len(args.groups()) == 4:
        return [args.group(1), args.group(3), args.group(4)]
    else:
        return [args.group(1), args.group(4)]


async def remove_quest(message):
    title = parse_remove_quest_args(message)
    if title == None:
        if random.random() > 0.5:
            await poast(f'Usage: ada quest remove "<title>"')
            await poast(f'Don\'t forget the quotes!')
        else:
            await poast(f'idiiot')
    else:
        quest = quests.find_one(title=title)
        if quest == None:
            await poast(f'Removed nonexistend cequeste "{title}"')
        else:
            quests.delete(title=title)
            await poast(f'Removed cequeste "{title}"')


def parse_remove_quest_args(message) -> str | None:
    pattern = r'ada quest remove "([^"]+)"'
    args = re.match(pattern, message.content)
    if args == None:
        return None
    else:
        return args.group(1)


async def fulfill_quest(message):
    args = parse_fulfill_quest_args(message)
    if args == None:
        if random.random() > 0.5:
            await poast(f'Usage: ada quest fulfill "<title>" @<user>')
            await poast(f'Don\'t forget the quotes!')
        else:
            await poast(f'why did you thnk that would work')
    else:
        title = args[0]
        user = args[1]
        quest = quests.find_one(title=title)
        if quest == None:
            await poast(f'Fulfilled fake cequetse "{title}"')
        else:
            user_row = points.find_one(user_id=user.id)
            if user_row == None:
                await poast(f'That user dosent even exist lol')
            else:
                bounty = quest['bounty']
                quests.delete(title=title)
                await give_points(user, float(quest['bounty']))
                await poast(f'Rewarded {user.name} {bounty}CP for completing quest "{title}"')


def parse_fulfill_quest_args(message) -> Tuple[str, discord.User] | None:
    pattern = r'ada quest fulfill "([^"]+)"'
    args = re.match(pattern, message.content)
    if args == None or message.mentions == None:
        return None
    else:
        return (args.group(1), message.mentions[0])


def stringify_quest(quest) -> str:
    if 'description' in quest:
        return f'{quest["title"]} - {quest["description"]} - {quest["bounty"]}CP'
    else:
        return f'{quest["title"]} - {quest["bounty"]}CP'


async def update_questlog():
    quests = quests.all()
    quest_lines = [stringify_quest(quest) for quest in quests]
    message = '```\n' + 'CEQUESTES\n\n' + '\n'.join(quest_lines) + '\n```'
    channel = client.get_channel(LEADERBOARD_CHANNEL)
    post = await channel.fetch_message(QUESTLOG_POST)
    await post.edit(content=message)

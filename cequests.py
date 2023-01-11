from main import client, db, LEADERBOARD_CHANNEL
from random import random

table = db['quests']

QUESTLOG_POST = 1062555665505202216


class Quest():
    def __init__(self, title, description, bounty) -> None:
        self.title = title
        self.description = description
        self.bounty = bounty

    def __str__(self) -> str:
        return f'{self.title}\n{self.description}\nBounty: {self.bounty} Clsetere Points'

    def serialize(self) -> dict:
        return dict(title=self.title, description=self.description, bounty=self.bounty)


async def interpret_queste_command(message) -> None:
    if message.content.startswith('!cp quest add'):
        await add_queste(message)
    elif message.content.startswith('!cp quest remove'):
        await remove_queste(message)
    elif message.content.startswith('!cp quest fulfill'):
        # todo


async def add_queste(message) -> None:
    args = message.content.split()[2:]
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
            await message.channel.send(f'Expected 2 or 3 arguments, recieved {len(args)}')
            await message.channel.send(f'Usage: !cp quest add <title> [description] <amount>')
        else:
            await message.channel.send(f'dumbass')


async def remove_queste(message) -> None:
    if len(message.content.split() != 4):
        if random() > 0.5:
            await message.channel.send(f'Expected 1 argument, recieved {len(message.content.split())}')
            await message.channel.send(f'Usage: !cp quest remove <title>')
        else:
            await message.channel.send(f'idiiot')
    else:
        title = message.content.split()[3]
        quest = table.find_one(title)
        if quest == None:
            await message.channel.send(f'Removed nonexistend cequeste "{title}"')
        else:
            table.delete(title=title)
            await message.channel.send(f'Removed cequeste "{title}"')


async def fulfill_queste(message) -> None:
    # todo

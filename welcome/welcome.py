import json
import logging
import time

import discord
import asyncio

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
console.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
logger.addHandler(console)

client = discord.Client()


def get_token():
    with open(".token", "r") as f:
        token = f.read()
    return token


async def run(token):
    await client.login(token.strip())
    await client.connect()


@client.event
async def on_ready():
    logger.info("on_ready")


def replace_macros(mention):
    msg = conf["message"]
    for key, value in conf["macros"].items():
        msg = msg.replace("{" + key + "}", value)
    return msg.replace("{mention}", mention)


def replace_channel_mention(msg):
    i = 1
    for channel in conf["channel_mentions"]:
        key = "channel_mention" + str(i)
        msg = msg.replace("{" + key + "}", client.get_channel(int(channel)).mention)
    return msg


@client.event
async def on_member_join(member):
    logger.info("Welcoming {0}".format(member.name))
    mention = member.mention
    channel = client.get_channel(int(conf["channel"]))
    time.sleep(60)
    await channel.send(replace_channel_mention(replace_macros(mention)))


def read_config():
    global conf
    with open('config.json', 'r') as f:
        conf = json.load(f)


if __name__ == '__main__':
    token = get_token()
    if token is not None:
        loop = asyncio.get_event_loop()
        read_config()
        loop.run_until_complete(asyncio.gather(run(token)))

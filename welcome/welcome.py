import json
import logging

import discord
import asyncio

logging.basicConfig(level=logging.INFO)
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
    logging.info("on_ready")


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
    mention = member.mention
    channel = client.get_channel(int(conf["channel"]))
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

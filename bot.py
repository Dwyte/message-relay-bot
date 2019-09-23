import discord
import asyncio
import configparser as cfg
import re
import glob
import os

client = discord.Client()
loop = asyncio.get_event_loop()


def parse_config(section, field):
    parser = cfg.ConfigParser()
    parser.read("config.cfg")
    return parser.get(section, field)

def parse_settings():
    modeStr = parse_config('settings', 'mode')
    mode = False if modeStr == "False" else True

    listStr = parse_config('settings', 'list').replace(" ", "")
    listArr = listStr.split(',')
    
    for counter,_id in enumerate(listArr):
        listArr[counter] = int(_id)

    return (mode, listArr)

settings = parse_settings()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for counter, attachment in enumerate(message.attachments):
        file_path = os.getcwd() + "/file{}.png".format(counter)

        await attachment.save(file_path)

    channel_mentions = message.channel_mentions

    if len(channel_mentions):
        output = "**User: {}**\n".format(message.author)
        output += message.content
        output = output.replace("@everyone", "")

        # For every channel mentioned
        for channel in channel_mentions:
            condition = channel.id in settings[1] if settings[0] else channel.id not in settings[1]
            print(condition)


            if condition:
                files = []
                for _file in glob.glob("file*.png"):
                    files.append(discord.File(_file))

                await channel.send(content=output, files=files)

        # Clean the Files
        for _file in glob.glob("file*.png"):
            os.remove(_file)

@client.event
async def on_ready():
    ''' Called when bot is ready.'''

    print('Logged in as', client.user.name)
    print('------')


def main():
    # Start Asyncio loop of the client starting.
    try:
        loop.run_until_complete(client.start(
            parse_config("token_ids", "bot_token")))
    finally:
        loop.close()


if __name__ == '__main__':
    main()

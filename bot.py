import discord
import asyncio
import configparser as cfg
import re
import glob,os

client = discord.Client()
loop = asyncio.get_event_loop()


def parse_config(section, field):
    parser = cfg.ConfigParser()
    parser.read("config.cfg")
    return parser.get(section, field)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    files = []
    for counter, attachment in enumerate(message.attachments):
        file_path = os.getcwd() + "/file{}.png".format(counter)

        await attachment.save(file_path)

        files.append(discord.File(file_path))

    # x = await message.attachments[0].save()

    # y = discord.File(os.getcwd() + "/file.png")

    channel_mentions = message.channel_mentions

    if len(channel_mentions):
        output = "**User: {}**\n".format(message.author)
        output += message.content

        for channel in channel_mentions:
            await channel.send(content=output, files=files)
        
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

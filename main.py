# IMPORTS
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from table2ascii import table2ascii as t2a, PresetStyle

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
# load client and environment

client = discord.Client(intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

# set commands to start with '!'
bot = commands.Bot(intents=discord.Intents.default(), command_prefix='!')


# on ready send confirmation of bot login
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# when a message is sent
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # if the command starts with !alliance_chat
    if message.content.startswith('!alliance_chat'):
        # creates array [!alliance_chat, input_1, input_2...]
        command_contents = message.content.split()
        # throw error if fewer than 3 inputs
        if len(command_contents) < 3:
            await message.channel.send('Alliance chats need at least two players!')
        else:
            # remove '!alliance_chat' from array of names
            command_contents.pop(0)
            # keep the channel secret by default
            overwrites = {
                message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                message.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            # loops through inputs and create string in form 'name-' while opening channel to roles
            names = ''
            name_dupes = []
            duplicates = False
            for name in command_contents:
                # checks for duplicate names
                for dup_name in name_dupes:
                    if name == dup_name:
                        duplicates = True
                        await message.channel.send('Alliance chat cannot be created because there are duplicate names!')
                name_dupes.append(name)
                # find the role associated with the player name
                role = discord.utils.get(message.guild.roles, name=name)
                # opens the channel to the player
                overwrites[role] = discord.PermissionOverwrite(read_messages=True)
                names = names + name + '-'
            # remove the last '-'
            chat_name = names[:-1]

            # find the host role
            host = discord.utils.get(message.guild.roles, name="Host")
            # open the channel to the host
            overwrites[host] = discord.PermissionOverwrite(read_messages=True)

            # finds members with the head of logistics role
            hol = discord.utils.get(message.guild.roles, name="Head of Logistics")
            # open the channel to head of logistics
            overwrites[hol] = discord.PermissionOverwrite(read_messages=True)

            # finds members with the head of filming role
            hof = discord.utils.get(message.guild.roles, name="Head of Filming")
            # open the channel to head of filming
            overwrites[hof] = discord.PermissionOverwrite(read_messages=True)

            # Finds the 'Alliance Chats' category
            category = discord.utils.get(message.guild.categories, name="Alliance Chats")

            # If there were no duplicate names
            if duplicates == False:
                try:
                    # create channel with assembled name, overwrites and category
                    await message.guild.create_text_channel(chat_name, overwrites=overwrites, category=category)
                    # send confirmation message
                    await message.channel.send('Chat ' + chat_name + ' created!')
                # error if it fails
                except:
                    # send error message
                    await message.channel.send('Error creating chat! Make sure player names are spelled correctly!')
    if message.content.startswith('!request_filmer'):
        inputs = message.content.split(' ')


    # If the message starts with '!devs'
    if message.content.startswith('!devs'):
        # Output the new amsterdam message.
        await message.channel.send(
            "This bot was developed by Harrison Jumper and Gabe Holmes with additional programming by Juliana Sica")

    # If the message starts with '!help'
    if message.content.startswith('!help'):
        # send the documentation
        await message.channel.send(
            "https://docs.google.com/document/d/1mRM8xl5f2_zhOgsapYVhOHUXql13RGacO_wCArEuyuU/edit?usp=sharing")

    # If the message starts with '!test'
    if message.content.startswith('!test'):
        # Output the new amsterdam message.
        await message.channel.send(
            "Woooo the bot is back!!")

    # If the message starts with '!MVP'
    if message.content.startswith('!MVP'):
        # Output the MVPPPPP
        with open('tatum.jpg', 'rb') as f:
            picture = discord.File(f)
        await message.channel.send(file=picture)

    # If the message starts with '!never_stop_gambling'
    if message.content.startswith('!stick_season'):
        # Output the new amsterdam message.
        with open('lyrics.txt') as f:
            lines = f.readlines()
        print(''.join(lines))
        await message.channel.send(
            (''.join(lines))[:1999])

# run bot
client.run(TOKEN)
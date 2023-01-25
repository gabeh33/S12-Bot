# IMPORTS
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from table2ascii import table2ascii as t2a, PresetStyle
import randfacts
import pyjokes
import random

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
# load client and environment

client = discord.Client(intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# set commands to start with '!'
bot = commands.Bot(intents=discord.Intents.default(), command_prefix='!')


# on ready send confirmation of bot login
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global filming_msg_channel
    filming_channel = client.get_channel(1053095948110266420)
    bot_test_channel = client.get_channel(1066168204830982194)
    filming_msg_channel = filming_channel

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
            add_head_of_filming = True
            if add_head_of_filming:
                hof = discord.utils.get(message.guild.roles, name="Head of Filming")
                # open the channel to head of filming
                overwrites[hof] = discord.PermissionOverwrite(read_messages=True)

            # Finds the 'Alliance Chats' category
            category = discord.utils.get(message.guild.categories, name="ALLIANCE CHATS")

            # If there were no duplicate names
            if not duplicates:
                try:
                    # create channel with assembled name, overwrites and category
                    await message.guild.create_text_channel(chat_name, overwrites=overwrites, category=category)

                    # send confirmation message
                    await message.channel.send('Chat ' + chat_name + ' created!')
                    print(f"Created chat with: {chat_name}")
                # error if it fails
                except:
                    # send error message
                    await message.channel.send('Error creating chat! Make sure player names are spelled correctly!')

    if message.content.startswith('!request_filmer'):
        inputs = message.content.split()
        # Need at least the players and a time, description is optional
        if len(inputs) < 3:
            await message.channel.send(
                "To request a filmer, use "
                "!request_filmer  [player1/player2/player3...]  [time]  [description (optional)]\n"
                "For example, !request_filmer Gabe/Steph/Lauren today-1pm Alliance meeting")
            return
        inputs.pop(0)

        # Send a message to the filming chat
        try:
            channel_name = inputs[0].replace('/', '-').lower()
            print(channel_name)
        except:
            await message.channel.send(
                "Unable to recognize players provided, please specify players using player1/player2/player3...")

        request_msg = ' '.join(inputs)
        bot_message = await filming_msg_channel.send(f'<@&1066783347000483900> Meeting requested: {request_msg}')
        return
        def check(m):
            return m.message == bot_message.content

        thumb_up = '👍'

        while True:
            reaction, user = await client.wait_for("reaction_add", check=check)
            if str(reaction.emoji) == thumb_up:
                # Add the person to the channel
                try:
                    meeting_channel = discord.utils.get(client.get_all_channels(), name=channel_name)
                    await meeting_channel.send("sending message in the correct channel")
                except:
                    print("no channel found")
                await filming_msg_channel.send(f'{user} is filming the specified meeting: {request_msg}')
                return

        # Find the channel

    # If the message starts with '!devs'
    if message.content.startswith('!devs'):
        # Output the devs.
        await message.channel.send(
            "This bot was developed by Gabe Holmes and Harrison Jumper with additional programming by Juliana Sica")

    # If the message starts with '!help'
    if message.content.startswith('!help'):
        # send the documentation
        await message.channel.send(
            "https://docs.google.com/document/d/1mRM8xl5f2_zhOgsapYVhOHUXql13RGacO_wCArEuyuU/edit?usp=sharing")

    if message.content.startswith('!gambling'):
        # send the documentation
        await message.channel.send(
            "never stop.")

    # If the message starts with '!MVP'
    if message.content.startswith('!MVP'):
        # Output the MVPPPPP
        with open('tatum.jpg', 'rb') as f:
            picture = discord.File(f)
        await message.channel.send(file=picture)

    if message.content.startswith('!soccer'):
        with open('simpson.png', 'rb') as f:
            picture = discord.File(f)
        await message.channel.send(file=picture)

    if message.content.startswith('!steph'):
        with open('steph.jpg', 'rb') as f:
            picture = discord.File(f)
        await message.channel.send(file=picture)
        
    megan_arr = ['Jelly Bellies makes me feel good.', 'What is the purpose of the toy if you have to feed it with an iPad?', 'I know it’s my code, Cole. But she doesn’t look confused; she looks demented.', 'What in the ever-loving Christ is this?', 'What happened to the virtual pet I got you for your birthday?', 'I don’t even take care of my plants.', 'It’s a toy. I assume it’s not that complicated.', 'You’re going to have to make one or two adjustments in order for this to work.', 'The problem with toys like Bruce is that they are so expensive, not everyone can afford to have one.', 'If I had a toy like Bruce, I don’t think I’d ever need another toy again.', 'See if you can guess.', 'This is incredible. I mean, this is unbelievable, isn’t it?', 'Remember the moment. The moment we kicked Hasbro in the d*ck.', 'M3gan is on a constant quest for self-improvement.', 'M3gan is an excellent listener, and she even has a few stories of her own.', 'Katie, seriously, flush the toilet.', 'I thought we were creating a tool to support parents, not replace them.', 'Will I die?', 'A toy like that won’t come cheap.', 'Every day I wake up in this strange house, and I remember my parents are dead.', 'That’s a memory you’ll never forget. I am keeping it for you here.', 'I think the world is about to shift on its axis.', 'As of right now, she’s the most valuable asset this company has.', 'You weren’t porn-hubbing in the office again, were you?', 'M3gan’s not a person; she’s a toy.', 'You made her cry.', 'M3gan has been instructed to help Katie get over the loss. M3gan is part of the family now.', 'If you make a toy that is impossible to get rid of, how do you ever expect her to grow?', 'Experts say the preferred method is to give your child the choice.', 'You can’t make me do something I don’t want to do.', 'Let her go.', 'That is seriously cool.', 'F*ck off, Holly.', 'Make her say something.', 'She’s paired with me. She won’t play with anyone else.', 'So, you’re not going to play with me?', 'You need to learn good manners, Brandon.', 'This is the part where you run.', 'In a nutshell.', 'There will always have forces in the world that wish to cause us harm.', 'If heaven exists, they wouldn’t let boys like Brandon in.', 'I’ve been asking myself that same question.', 'Couldn’t sleep. Occupational hazard.', 'Hold on a second. I thought we were having a conversation.', 'God, I hope not. Because if I did, we’d both be in a lot of trouble.', 'When she looks at me, it’s like I’m the only thing that matters. Kind of like how my mom used to.', 'It’s just, I get too crazy without M3gan.', 'If something’s broken, you don’t just throw it away, you fix it.', 'She’s not a solution. She’s just a distraction.', 'You are all that matters to me now.', 'This is her. She’s locked us out.', 'How could you do this? How could you kill someone?', 'I didn’t kill anyone, Kurt. You did.', 'What did you think was going to happen?', 'Oh really? Is that where we are?', 'I’m going to show her what real love looks like.', 'Being a parent was never in the cards for you.', 'In this family, we don’t run from trauma.', 'There’s another member of the family we didn’t tell you about. His name is Bruce.', 'You ungrateful, little b*tch.']
    if message.content.startswith('!megan'):
        await message.channel.send(
            megan_arr[random.randrange(60)])
        
    if message.content.startswith('!gloose'):
        with open('gloose.jpg', 'rb') as f:
            picture = discord.File(f)
        await message.channel.send(file=picture)
        
    if message.content.startswith('!roll'):
        with open('Rick Astley - Never Gonna Give You Up (Official Music Video).mp4', 'rb') as f:
            video = discord.File(f)
        await message.channel.send(file=video)

    if message.content.startswith('!survivor_house'):
        await message.channel.send(
            "9 sewall st. You're always invited")

    if message.content.startswith('!gabe'):
        await message.channel.send(
            "likes to vote correctly")

    if message.content.startswith('!khalid'):
        await message.channel.send(
            "Gabe's #1 Ally")
    if message.content.startswith('!vince'):
        await message.channel.send(
            "chronically online")

    if message.content.startswith('!nr'):
        await message.channel.send(
            "oh my days and nights")

    if message.content.startswith('!conor'):
        await message.channel.send(
            "ratio")

    if message.content.startswith('!biddie'):
        await message.channel.send(
            "🪨🪨🪨")

    if message.content.startswith('!fun_fact'):
        await message.channel.send(
            randfacts.get_fact())

    if message.content.startswith('!juliana'):
        await message.channel.send(
            pyjokes.get_joke())

    if message.content.startswith('!pranav'):
        await message.channel.send("she’s nice she’s smart she’s hot")

    if message.content.startswith('!grace'):
        await message.channel.send("purrrrrrr")

    if message.content.startswith('!siya'):
        await message.channel.send("wocib af")

    # If the message starts with '!stick_season'
    if message.content.startswith('!stick_season'):
        # Output the lyrics to a great song
        with open('lyrics.txt') as f:
            lines = f.readlines()
        print(''.join(lines))
        await message.channel.send(
            (''.join(lines))[:1999])

    if message.content.startswith('!winners'):
        # Output the new amsterdam message.
        output = t2a(
            header=["Season", "Winner"],
            body=[[1, 'Ryan Mallaby'], [2, 'Lydia Tavera'], [3, 'Austin Shaughnessy'], [4, 'James Zemartis'],
                  [5, 'Alex Sharp'], [6, 'Delanie Smither'], [7, 'Lauren Murphy'], [8, 'Stephanie Yee'],
                  [9, 'Katalina Baehring'], [10, 'Margaret Morehead'], [11, 'Siya Gupta']],
            style=PresetStyle.thin_compact
        )
        await message.channel.send(f"```\n{output}\n```")


# run bot
client.run(TOKEN)

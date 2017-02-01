# coding: UTF-8
# knovabot v0.1
# this is python 3
# basically just expanding on the example bot from disord.py's readme file

import discord
import asyncio
import json
import datetime
import atexit
from msgfunc import redditfetch, helpmsg, roll

client = discord.Client()
botdata = json.load(open('botinfo.json', 'r'))


@client.event
async def on_ready():
    print ('Connected to Discord as: ' + client.user.name + '\n')


@client.event
async def on_message(message):
    if str(client.user.name) in str(message.author):
        return

    if message.content.startswith('!help'):
        print ("Received !help command")
        for h in helpmsg():
            await client.send_message(message.channel, h)

    elif message.content.startswith('!location'):
        print("Received !location command")
        await client.send_message(message.channel, 'My location is '+str(botdata['location']))

    elif message.content.startswith('!name'):
        print("Received !name command")
        await client.send_message(message.channel, 'My name is '+str(client.user.name)+', but you can call me '+str(botdata['botname']))

    elif message.content.startswith('!reddit'):
        print("Received !reddit command")
        rfetch = redditfetch(message.content)
        for r in rfetch:
            await client.send_message(message.channel, r)

    elif message.content.startswith('!roll'):
        print("Received !roll command")
        num = roll(message.content)
        if num > 0:
            await client.send_message(message.channel, "You rolled a " + str(num))
        else:
            await client.send_message(message.channel, "You suck at rolling dice. Try !roll <size of dice here>")

    elif message.mentions:
        for m in message.mentions:
            if str(client.user.name) in str(m):
                print (str(client.user.name) + " was mentioned, responding to " + str(message.author))
                await client.send_message(message.channel, 'Hi ' + str(message.author.mention) + '! I am awake and listening, use !help for more info.')


# this next part is pretty sinister, it reposts a comment if a user deletes it
# you may want to disable this
@client.event
async def on_message_delete(message):
    print(message.author.name + " deleted a message, asking if users want to have it reposted.")
    await client.send_message(message.channel, "Like a true loser, " + message.author.mention + " has deleted a message!")
    await client.send_message(message.channel, "Does anyone want me to repost it? Type !repostnow within 10 seconds if so!")
    msg = await client.wait_for_message(timeout=10.0, channel = message.channel, content="!repostnow")
    if msg == None:
        print ("Repost request timed out.")
    else:
        await client.send_message(message.channel,
                    "REPOSTING: [originally posted " + message.timestamp.strftime("%x %X %Z") + ", by " + message.author.name + "]: " + message.content)


# the actual process that runs the bot. pulls the token from botinfo.json, so place your token there
client.run(botdata['token'])


# what to do if the program exits?
@atexit.register
def quitbot():
    print ("Bot was terminated for an unknown reason.")


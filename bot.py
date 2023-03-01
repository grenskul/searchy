import discord
from discord.ext import commands
import json
import re
import asyncio
import os

Intents = discord.Intents.all()



channels = []
attach_name = []
attach_link = []

def read (filename):
   try:
        with open(filename, 'r') as json_file:
            return json.loads(json_file.read())
   except FileNotFoundError:
        return []

def write(filename , save_object):
    with open(filename, 'w') as json_file:
        json_file.write(json.dumps(save_object))

if os.path.getsize('/config/channels.json') == 0:
	channels = []
else:
	channels = read('/config/channels.json')
	

if os.path.getsize('/config/attach_name.json') == 0:
	attach_name = []
else:
	attach_name = read('/config/attach_name.json')


if os.path.getsize('/config/attach_link.json')== 0:
	attach_link = []
else:
	attach_link = read('/config/attach_link.json')	

	
bot = commands.Bot(command_prefix='&', description="This is a search bot",intents=Intents)


@bot.command()
async def Scan(ctx):
    if str(ctx.channel.id) not in channels:
        channels.append(str(ctx.channel.id))
        write('/config/channels.json', channels)
        async for message in ctx.history(limit=1000000):
            if message.attachments:
                attach_name.append(message.attachments[0].filename)
                attach_link.append(message.jump_url) 
                write('/config/attach_name.json',  attach_name)
                write('/config/attach_link.json',  attach_link)



@bot.command()
async def Search(ctx, query):
    if str(ctx.channel.id) not in channels:
        await ctx.channel.send("Channel not scanned yet")
    else:
        found =[]
        for attachment in attach_name:
            if query in str(attachment):
                ind = attach_name.index(attachment)
                found.append(attach_link[ind])
        deduper= set(found)
        deduped=list(deduper)
        for i in range(len(deduped)):
                ind = deduped[i]
                await ctx.channel.send(deduped[i] + "    " + attach_name[attach_link.index(deduped[i])])
		



# Events
@bot.event
async def on_message(message):

    if (message.attachments and (str(message.channel.id) in channels) and (message.attachments[0].url.endswith('epub')or message.attachments[0].url.endswith('txt') or message.attachments[0].url.endswith('TXT') or message.attachments[0].url.endswith('EPUB') or message.attachments[0].url.endswith('docx') or message.attachments[0].url.endswith('DOCX') or message.attachments[0].url.endswith('pdf') or message.attachments[0].url.endswith('PDF'))):
        attach_link.append(message.jump_url) 
        attach_name.append(message.attachments[0].filename)
        write('/config/attach_name.json',  attach_name)
        write('/config/attach_link.json',  attach_link)
    await bot.process_commands(message)

	

@bot.event
async def on_ready():
    game = discord.Game("with attachments")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print('Bot has started')



bot.run(os.getenv('discord_token'))

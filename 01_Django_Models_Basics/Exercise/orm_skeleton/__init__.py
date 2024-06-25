import discord
from discord.ext import commands, tasks
import time
from python_mcstatus import JavaStatusResponse, statusJava
import os

intents = discord.Intents.default()
intents.message_content = (True)

bot = commands.Bot(commands.when_mentioned_or("s!"), intents=intents)

#@bot.event
#async def on_member_join(member: discord.Member):
    #channel = bot.get_channel(1187561310729273408)
    #await channel.send(f"Welcome {member.mention} to Back 2 Basics!")

@bot.event
async def on_ready():
    print('Bot is ready')
    channel= bot.get_channel(1174379650634481804)
    g = ''
    for guild in bot.guilds:
        g = guild.name + '\n'
    await channel.send(f'{bot.user} is now online \nguilds = \n{g}')
# The above sends a message to my test server letting me know when the bot has come back online it also tells me what guilds/servers it is in

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.guild.id != 1029379459649912833 or message.guild.id != 1187561310729273405: # returns if the message isn't in my testing server or the B2B discord
        return
    if message.content.startswith('!ip'):
        await message.channel.send('The server ip is `play.back2basics.gg`\nwe recommend joining on 1.20.4') #if it reeds !ip at the start of a message it responds with the text on the next line
    if message.content.startswith('!status'): #idk whether to keep this or not but it just sends a message telling you how many people are online
        host = 'play.back2basics.gg'
        port = 25565
        query = True
        JavaStatusResponse = statusJava(host, port, query)
        await message.channel.send(f'There is currently `{JavaStatusResponse.players.online}` players online')
    if message.content.startswith('!ping'): #simple ping command it returns 'Pong!'
        await message.channel.send('Pong!')

@tasks.loop(seconds = 30) #loops every 30seconds
async def myLoop():
    print('im online')
    await bot.wait_until_ready()
    host = 'play.back2basics.gg'
    port = 25565
    query = True
    try:
        JavaStatusResponse = statusJava(host, port, query)
        channel = bot.get_channel(1212340514930561096)
        message = await channel.fetch_message(1212369016530804766)
        unix = time.time()
        unix = round(unix)
        await message.edit(content = f'current online players: `{JavaStatusResponse.players.online}`\n last updated at:<t:{unix}:R>') #edits a message in my test server to show when it last ran and how many palyers are online
        players = JavaStatusResponse.players.online
        await bot.change_presence(status=discord.Status.online , activity=discord.Game(f"with {players} other players on play.back2basics.gg!"))  #changes the status to display the current online people
    except: #if something goes wrong in the above it will let me know this usually happens when it doesn't get a response from the server
        print('server is offline')
        botlogg = bot.get_channel(1174326100684460144)
        await botlogg.send('Minecraft server is offline')


myLoop.start()
token = 'BOT_TOKEN'
bot.run(token)

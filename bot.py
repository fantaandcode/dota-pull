import discord
from discord.ext import commands
import logging
import datetime

from calls import matchinfo as mi

TOKEN = 'INSERT_HERE'

client = commands.Bot(command_prefix = '.')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

output = ''

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='Testing'))

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['lm'])
async def lastmatch(ctx, p_id):
    try:
        p_id = int(p_id)
        await ctx.send(f'Parsing {p_id}\'s last match.')
        output = mi.lastmatch(p_id)
        embed = discord.Embed(
            title = output[0],
            colour = discord.Colour.orange()
        )

        embed.set_footer(text = f'Completed {datetime.datetime.now().strftime("%x")}')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name=output[1], value=output[2], inline=False)
        embed.add_field(name=output[3], value=output[4], inline=False)
        embed.add_field(name=output[5], value=output[6], inline=False)

        await ctx.send(embed=embed)
    except ValueError:
        await ctx.send('Please enter a valid player ID.')

@client.command(aliases=['mi'])
async def matchinfo(ctx, m_id):
    try:
        p_id = int(p_id)
        await ctx.send(f'Parsing match {m_id}.')
        output = mi.matchinfo(m_id)
        await ctx.send(output)
    except ValueError:
        await ctx.send('Please enter a valid match ID.')

@client.command(aliases=['reg'])
async def register(ctx, p_url):
    # Eventually put all of this in external script in calls
    # Dotabuff or OpenDota
    if ('dotabuff.com/players' in p_url or 'opendota.com/players' in p_url):
        p_id = p_url.split('/')[-1]
        print(p_id)

        # check if PID is an int
        try:
            p_id = int(p_id)
            await ctx.send(f'{p_id} is registered to {ctx.author}')
        except ValueError:
            await ctx.send('The URL might be incorrect, please use OpenDota or Dotabuff.')
    else:
        await ctx.send('The URL might be incorrect, please use OpenDota or Dotabuff.')

    # add later for registration
    # p_id for SteamID
    # ctx.author.id for Discord ID

@commands.command()
async def command_name(self, ctx):
    channel = self.bot.get_channel(channelid)
    await channel.send('Text')

client.run(TOKEN)

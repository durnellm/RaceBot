import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import datetime
import time
import random

Client = discord.Client()
bot_prefix= "."
client = commands.Bot(command_prefix=bot_prefix)

class Timer(object):
    """A simple timer class"""
    
    def __init__(self):
        pass
    
    def start(self):
        """Starts the timer"""
        self.start = datetime.datetime.now()
        return self.start
    
    def elapsed(self):
        """Time elapsed since start was called"""
        return str(datetime.datetime.now() - self.start)

class Race(object):
    def __init__(self, ra = 0, bi =0, e = [], r = [], ru = [], d = [], f  = []):
        self.rain = ra
        self.bing = bi
        self.en = e
        self.re = r
        self.ru = ru
        self.do = d
        self.fo = f
        
    def initrace(self):
        self.rain = 1

    def go(self):
        self.rain = 2

    def start(self):
        self.rain = 0
        self.bing = 0

    def startrace(self):
        if self.rain == 0:
            self.en = []
            self.re = []
            self.ru = []
            self.do = []
            self.fo = []
            self.initrace()
            return 'A race has been started, type .enter to join!'
        else:
            return 'A race has already been started, wait for the first one to end'
    
    def bingo(self):
        self.bing = 1

    def enter(self, runner):
        if self.rain == 0:
            return 'A race has not been started, type .startrace to begin.'
        elif self.rain == 2:
            return 'A race has already started, please wait for this one to end before starting another.'
        elif (runner not in self.en) and (runner not in self.re) and (runner not in self.ru) and (runner not in self.do) and (runner not in self.fo):
            self.en.append(runner)
            if len(self.en) > 1:
                e = 's.'
            else:
                e = '.'
            return ' has entered the race! ' + str(len(self.en)) + ' entrant' + e
        else:
            return 'You are already in the race, type .quit to leave or .forfeit to forfeit'

    def ready(self, runner):
        if self.rain == 0:
            return 'A race has not been started, type .startrace to begin.'
        elif self.rain == 2:
            return 'A race has already started, please wait for this one to end before starting another.'
        elif (runner in self.en):
            self.re.append(runner)
            self.en.remove(runner)
            if len(self.re) >= 1 and len(self.en) == 0:
                self.ru.extend(self.re)
                self.re = []
                return 'The race is about to begin. Starting in 10'                    
            return ' is ready! ' + str(len(self.en) + len(self.re)) + ' remaining.'
        elif (runner not in self.en) and (runner not in self.re) and (runner not in self.ru) and (runner not in self.do) and (runner not in self.fo):
            return 'You are not in the race, type .enter to join'
        elif (runner in self.re):
            return 'You are already ready, type .unready to undo'
        else:
            return 'You are already in the race, type .quit to leave or .forfeit to forfeit'

    def unready(self, runner):
        if self.rain == 0:
            return 'A race has not been started, type .startrace to begin.'
        elif self.rain == 2:
            return 'A race has already started, please wait for this one to end before starting another.'
        elif (runner in self.re):
            self.re.remove(runner)
            self.en.append(runner)
            return """ isn't ready! """ + str(len(self.en)) + ' remaining.'
        elif (runner in self.en):
            return """ isn't ready! """ + str(len(self.en)) + ' remaining.'
        elif (runner in self.ru) or (runner in self.do) or (runner in self.fo):
            return 'You are already in the race, type .forfeit to quit'

    def done(self, runner):
        if self.rain == 0:
            return 'A race has not been started, type .startrace to begin.'
        elif self.rain == 1:
            return 'The race has not started yet, wait until everyone has readied up.'
        elif (runner in self.ru):
            self.do.append(runner)
            self.ru.remove(runner)
            t2 = t.elapsed()
            t2 = t2[:-7]
            s = ""
            p = str(len(self.do))
            if p[len(p)-1] == '1':
                p += 'st'
            elif p[len(p)-1] == '2':
                p += 'nd'
            elif p[len(p)-1] == '3':
                p += 'rd'
            else:
                p += 'th'
            if len(self.ru) == 0:
                s = "1"
                self.start()
                self.do = []
                self.fo = []
                self.ru = []
            return s + ' has finished in ' + p + ' place with a time of: ' + str(t2)
        else:
            return 'You are currently not in the race.'

    def undone(self, runner):
        if self.rain == 0:
            return 'A race has not been started, type .startrace to begin.'
        elif self.rain == 1:
            return 'The race has not started yet, wait until everyone has readied up.'
        elif (runner in self.do):
            self.do.remove(runner)
            self.ru.append(runner)
            return + """ isn't done. """
        elif (runner in self.fo):
            self.fo.remove(runner)
            self.ru.append(runner)
            return + """ isn't done. """
        elif (runner in self.ru):
            return + """ isn't done. """
        else:
            return 'You are currently not in the race.'

    def forfeit(self, runner):
        if self.rain == 0:
            return 'A race has not been started, type .startrace to begin.'
        elif (runner in self.en):
            self.en.remove(runner)
            return ' has quit'
        elif (runner in self.re):
            self.re.remove(runner)
            return ' has quit'
        elif self.rain == 1:
            return 'The race has not started yet, type .enter to join.'
        elif (runner in self.ru):
            self.fo.append(runner)
            self.ru.remove(runner)
            s = ''
            if len(self.ru) == 0:
                s = "1"
                self.start()
                self.do = []
                self.fo = []
                self.ru = []
            return s + ' has forfeit.'
        else:
            return 'You are currently not in the race.'
        
@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    global race
    race = Race()
    print("ready")

@client.command(pass_context=True)
async def startup(ctx):
    global race
    race = Race()
    print("ready")

@client.command(pass_context=True)
async def startrace(ctx):
    out = race.startrace()
    await ctx.channel.send(out)
    
@client.command(pass_context=True)
async def forcequit(ctx):
    race.start()
    await ctx.channel.send('Race Cancelled')
    
@client.command(pass_context=True)
async def commands(ctx):
    out = discord.Embed(title="RaceBot Commands")
    out.add_field(name='.startrace',value='starts a new race if there isnt already one running',inline=False)
    out.add_field(name='.bingo',value='generates a bingo board when the race starts',inline=False)
    out.add_field(name='.enter',value='joins the race',inline=False)
    out.add_field(name='.ready',value='readies for the race, race starts when everyone is ready',inline=False)
    out.add_field(name='.unready',value='unreadies for the race',inline=False)
    out.add_field(name='.done',value='to mark your completion of race requirements, race ends when everyone is done or forfeits',inline=False)
    out.add_field(name='.forfeit',value='quits the race',inline=False)
    out.add_field(name='.undone',value='reneters the race if you have finished or forfeited',inline=False)
    await ctx.channel.send(embed=out)
    
@client.command(pass_context=True)
async def bingo(ctx):
    out = race.bingo()
    await ctx.channel.send('A seed will be generated when the race starts')

@client.command(pass_context=True)
async def enter(ctx):
    out = race.enter(ctx.message.author)
    if out[0] == " ":
        await ctx.channel.send(ctx.message.author.mention + out)
    else:
        await ctx.channel.send(out)

@client.command(pass_context=True)
async def ready(ctx):
    out = race.ready(ctx.message.author)
    if out[0] == "T":
        global t
        t = Timer()
        await ctx.channel.send(out)
        time.sleep(5)
        await ctx.channel.send('5')
        time.sleep(1)
        await ctx.channel.send('4')
        time.sleep(1)
        await ctx.channel.send('3')
        time.sleep(1)
        await ctx.channel.send('2')
        time.sleep(1)
        await ctx.channel.send('1')
        time.sleep(1)
        await ctx.channel.send('GO!')
        if race.bing == 1:
            await ctx.channel.send('https://hpbingo.github.io/HP2%20v4.1/bingo.html?mode=normal&seed=' + "%06d" % random.randint(0,999999))
        race.go()
        t.start()
    else:
        await ctx.channel.send(out)

@client.command(pass_context=True)
async def unready(ctx):
    out = race.unready(ctx.message.author)
    if out[0] == " ":
        await ctx.channel.send(ctx.message.author.mention + out)
    else:
        await ctx.channel.send(out)

@client.command(pass_context=True)
async def done(ctx):
    out = race.done(ctx.message.author)
    if out[0] == "1":
        out =out[1:] 
        await ctx.channel.send(ctx.message.author.mention + out)
        await ctx.channel.send('The race has ended.')
    elif out[0] == " ":
        await ctx.channel.send(ctx.message.author.mention + out)
    else:
        await ctx.channel.send(out)

@client.command(pass_context=True)
async def undone(ctx):
    out = race.undone(ctx.message.author)
    if out[0] == " ":
        await ctx.channel.send(ctx.message.author.mention + out)
    else:
        await ctx.channel.send(out)

@client.command(pass_context=True)
async def forfeit(ctx):
    out = race.forfeit(ctx.message.author)
    if out[0] == "1":
        out = out[1:]
        await ctx.channel.send(ctx.message.author.mention + out)
        await ctx.channel.send('The race has ended.')
    elif out[0] == " ":
        await ctx.channel.send(ctx.message.author.mention + out)
    else:
        await ctx.channel.send(out)

@client.command()
async def shame():
        await ctx.channel.send('Shame on those that havent readied up!')

client.run("XXXX") #Replace with client key

import math, re, requests, discord, asyncio, io, aiohttp, random, emoji, os
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from textwrap import wrap

bot = commands.Bot(command_prefix=']')
slash = SlashCommand(bot, sync_commands=True)

guild_ids = [int(i) for i in os.environ.get("GUILD_IDS").split(".")]

@bot.event
async def on_ready():
    DiscordComponents(bot)
    print('Logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(bot.command_prefix + "help"))

# @bot.command(brief="Change command prefix")
# async def prefix(ctx, arg):
#     # bot.command_prefix = arg
#     # await ctx.send("Prefix is now " + arg)
#     # await bot.change_presence(status=discord.Status.online, activity=discord.Game(arg + "help"))
#     await ctx.send("I'm not changing the prefix, deal with it")

# @bot.command(brief="Very simple ping pong")
# async def ping(ctx):
#     await ctx.send('pong')

# @bot.command(brief="Ôø´ ıˆ∂´˜")
# async def button(ctx):
#     await ctx.send(
#         "Click one",
#         components = [[Button(label = str(i+1)) for i in range(j,j+5)] for j in range(0,25,5)]
#     )

    # interaction = await bot.wait_for("button_click")

'''
@bot.event
async def on_message(message):
    print(message.content)

    content = message.content + ' ' +  ' '.join([name(i) for i in message.mentions + message.channel_mentions + message.role_mentions])
    for i in re.findall("(?a?:<?:[\\w\\(\\)]+:(?:\\d+>)?)|(?:[🇦-🇿])", emoji.demojize(content)):
        if len(i) == 1 and ord(i[0]) >= 127462 and ord(i[0]) <= 127487:
            await message.add_reaction(i)
        elif i.startswith(":"):
            await message.add_reaction(emoji.emojize(i))
        else:
            await message.add_reaction(i[1:-1])
'''

# @bot.event
# async def on_message(message):
#     try:
#         n = message.author.nick
#     except:
#         n = message.author.name
#     if n is None:
#         n = message.author.name
#     for i in re.findall("(?:<?:[\\w\\(\\)]+:(?:\\d+>)?)|(?:[🇦-🇿])", emoji.demojize(message.content)): # n + " " + 
#         if len(i) == 1 and ord(i[0]) >= 127462 and ord(i[0]) <= 127487:
#             await message.add_reaction(i)
#         elif i.startswith(":"):
#             await message.add_reaction(emoji.emojize(i))
#         else:
#             await message.add_reaction(i[1:-1])
# #🇦 🇿
# @bot.event
# async def on_reaction_add(reaction, user):
#     await reaction.message.add_reaction(reaction.emoji)

@bot.event
async def on_button_click(res):
    await res.message.channel.send("{0.user} clicked {0.component.label}".format(res), delete_after=5.0, allowed_mentions=discord.AllowedMentions.none())
    #await res.respond(content = "Thanks for pressing!")
    if res.message.content == "```\nError\n```":
        await res.message.edit("```\n \n```")
    if res.component.label in "0123456789+-*/.()\%ej":
        if res.message.content == "```\nError\n```":
            await res.message.edit("```\n{0.component.label}\n```".format(res))
        else:
            await res.message.edit("```\n" + res.message.content[3:-3].strip() + "{0.component.label}\n```".format(res))
    else:
        if res.component.label == "π":
            await res.message.edit("```\n" + res.message.content[3:-3].strip() + f"{math.pi}\n```")
        elif res.component.label == "𝑒":
            await res.message.edit("```\n" + res.message.content[3:-3].strip() + f"{math.e}\n```")
        elif res.component.label == "AC":
            await res.message.edit("```\n \n```")
        elif res.component.label == "DEL":
            if not re.match(r'^[0-9+\-*\/.\(\)%ej]+$', res.message.content[3:-3].strip()):
                await res.message.edit("```\n \n```")
            else:
                await res.message.edit("```\n" + res.message.content[3:-3].strip()[:-1] + "\n```")
        elif res.component.label == "=":
            try:
                m = res.message.content[3:-3].strip()
                if m != "" and re.match(r'^[0-9+\-*\/.\(\)%ej]+$', res.message.content[3:-3].strip()):
                    await res.message.edit("```\n" + str(eval(m)) + "\n```")
                    await res.message.channel.send("```\n" + m + " = " + str(eval(m)) + "\n```")
            except:
                await res.message.edit("```\nError\n```")
    

@slash.slash(name="joe", guild_ids=guild_ids)
async def _joe(ctx): # Defines a new "context" (ctx) command called "ping."
    await ctx.send("Slash command test!")

@slash.slash(name="calc", description = "Calculator with buttons (doesn't work)", guild_ids=guild_ids, options=[
               create_option(
                 name="eqn",
                 description="Equation to load on the calculator (optional)",
                 option_type=3,
                 required=False
               )
             ])
async def _calc(ctx, eqn=''):
    try:
        await calc(ctx, eqn=eqn)
    except:
        await ctx.send("This doesn't work, use `" + bot.command_prefix + "calc` instead, because the modules I used for buttons and slash commands are incompatible with one another.")

@bot.command(brief="Calculator with buttons")
async def calc(ctx, *, eqn=''):
    l1 = [Button(label = i) for i in ["7","8","9"]]
    l2 = [Button(label = i, style=ButtonStyle.red) for i in ["DEL","AC"]]
    l3 = [Button(label = i) for i in ["4","5","6"]]
    l4 = [Button(label = i, style=ButtonStyle.blue) for i in ["*","/"]]
    l5 = [Button(label = i) for i in ["1","2","3"]]
    l6 = [Button(label = i, style=ButtonStyle.blue) for i in ["+","-"]]
    l7 = [Button(label = i) for i in ["0",".","(",")"]]
    l8 = [Button(label = '%', style=ButtonStyle.blue)]
    l9 = [Button(label = i, style=ButtonStyle.blue) for i in ["π","𝑒"]]
    l10 = [Button(label = i) for i in ["e","j"]]
    l11 = [Button(label = '=', style=ButtonStyle.green)]
    message = await ctx.send("Loading...", components = [ [*l1,*l2], [*l3,*l4], [*l5, *l6], [*l7, *l8], [*l9, *l10, *l11] ] )
    s = "```\n \n```"
    if re.match(r'^[0-9+\-*\/.\(\)%ej]+$', eqn):
        s = "```\n" + eqn + "\n```"
    await message.edit(s)

@slash.slash(name="wikitext", description = "Plain text from Wikipedia", guild_ids=guild_ids, options=[create_option(name="name", description="Name of article", option_type=3, required=True), create_option(name="lang", description="Language (default: en)", option_type=3, required=False)])
async def _wiki(ctx, name, lang="en"):
    url = requests.head("https://"+lang+".wikipedia.org/wiki/"+name, allow_redirects=True).url
    await ctx.send(url)
    nname = url.split("/", 4)[4].split('#')[0]
    r = requests.get("https://" + lang + ".wikipedia.org/w/api.php?action=query&format=json&titles=" + nname + "&prop=extracts&explaintext").json()["query"]["pages"]
    for i in wrap(r[list(r)[0]]["extract"], 2000):
        await ctx.channel.send(i)

def egyptify(x,y):
    import math
    if x == 1:
        return [y]
    if x == 0:
        return []
    return [math.ceil(y/x)] + egyptify((-y)%x,y*math.ceil(y/x))

def formatdn(denoms):
    return ('1/' + ' + 1/'.join([str(i) for i in denoms])).replace('1/1 ','1 ')

@slash.slash(name="frac", description = "Convert fraction to Egyptian fractions", guild_ids=guild_ids, options=[
               create_option(
                 name="numerator",
                 description="Numerator",
                 option_type=4,
                 required=True
               ), create_option(
                 name="denominator",
                 description="Denominator",
                 option_type=4,
                 required=True
               )
             ])
async def _frac(ctx, numerator, denominator):
    await ctx.send(str(numerator) + "/" + str(denominator) + " = " + formatdn(egyptify(numerator, denominator)))

def convertHzNote(freq):
  return convertMidNote(convertHzMid(freq))

def convertHzMid(freq):
  import math
  return 12*math.log(freq/440,2) + 69 #nice

def convertMidHz(no):
  return 2**((no - 69)/12) * 440

def convertMidNote(no):
  import math
  noteletters = "C C#/Db D D#/Eb E F F#/Gb G G#/Ab A A#/Bb B".split()
  centsdeviation = (no - math.floor(no))*100
  octaveno = math.floor(no/12) - 1
  if centsdeviation >= 50:
    centsdeviation -= 100
    noteletter = noteletters[int((no%12+1)%12)]
    if noteletter == "C":
      octaveno += 1
  else:
    noteletter = noteletters[int(no%12)]
  if centsdeviation == 0:
    return noteletter + str(octaveno)
  elif centsdeviation > 0:
    return noteletter + str(octaveno) + " + " + str(centsdeviation) + " cents"
  else:
    return noteletter + str(octaveno) + " - " + str(-1*centsdeviation) + " cents"

@slash.slash(name="midi", description = "Convert frequency (Hz) to note", guild_ids=guild_ids, options=[
               create_option(
                 name="freq",
                 description="Frequency in Hertz",
                 option_type=4,
                 required=True
               ), create_option(
                 name="power",
                 description="*10^",
                 option_type=4,
                 required=False
               )
             ])
async def _midi(ctx, freq, power=0):
    nf = freq*(10**power)
    await ctx.send(str(nf) + " Hz = " + convertHzNote(nf))

@slash.slash(name="forloop", description = "Sends output of Python expression inside a \"for i in range\" loop. Parameters are those of range()", guild_ids=guild_ids, options=[
                create_option(
                 name="expression",
                 description="Python expression that can use i as a variable",
                 option_type=3,
                 required=True
               ), create_option(
                 name="stop",
                 description="Stop parameter in range()",
                 option_type=4,
                 required=True
               ), create_option(
                 name="start",
                 description="Start parameter in range()",
                 option_type=4,
                 required=False
               ), create_option(
                 name="step",
                 description="Step parameter in range()",
                 option_type=4,
                 required=False
               )
    ])
async def _forloop(ctx, expression, stop, start=0, step=1):
    await ctx.send(f"```python\nfor i in range({start},{stop},{step}):\n    print({expression})\n```")
    try:
        for i in range(start, stop, step):
            await ctx.channel.send(str(eval(expression)))
    except:
        try:
            for i in range(start, stop, step):
                await ctx.send(str(eval(expression)))
        except Exception as e:
            try:
                await ctx.channel.send("Exception: " + str(e))
            except:
                await ctx.send("Exception: " + str(e))

@slash.slash(name="oldmap", description = "Sends a random page from old Singapore maps archive", guild_ids=guild_ids, options=[
                create_option(
                 name="year",
                 description="Year (optional)",
                 option_type=4,
                 required=False
               ), create_option(
                 name="page",
                 description="Page number (optional). Enter 0 for indexmap",
                 option_type=4,
                 required=False
               )
    ])
async def _oldmap(ctx, year=-1, page=-1):
    channel = ctx.channel
    years = [1954, 1955, 1956, 1957, 1958, 1961, 1963, 1966, 1969, 1972, 1975, 1978, 1981, 1984, 1988, 1991, 1993, 1995, 1998, 2000, 2007, 2008, 2009]
    y = random.choice(years)
    if year != -1:
        if year not in years:
            await ctx.send("No map exists for {}. Available years: ".format(year) + str(years))
            return
        else:
            await ctx.send("Finding map...")
            y = year
            if page != -1:
                p = page
                if p == 0:
                    p = "indexmap"
                url = "https://onemap.gov.sg/hm/{0}/{0}%20({1}).jpg".format(y, p)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        if "</script>" in requests.get(url).text:
                            await ctx.send("Invalid page.")
                            return
                        data = io.BytesIO(await resp.read())
                        await channel.send("{}, page {}".format(y, p), file=discord.File(data,"map.jpg"))
                        print(url)
                        return
    temp = True
    await ctx.send("Finding map...")
    while temp:
        p = random.randrange(500)
        url = "https://onemap.gov.sg/hm/{0}/{0}%20({1}).jpg".format(y, p)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if "</script>" in requests.get(url).text:
                    continue
                temp = False
                data = io.BytesIO(await resp.read())
                if p == "indexmap":
                    await channel.send("{}, indexmap".format(y), file=discord.File(data,"map.jpg"))
                else:
                    await channel.send("{}, page {}".format(y, p), file=discord.File(data,"map.jpg"))
                print(url)


def translate(s, fr='', to=''):
    if fr == '' and to == '':
        fr, to = 'en', 'zh'
    elif fr != '' and to == '':
        to = 'en'
    elif fr == '' and to != '':
        fr = 'en'
    if fr == to:
        return s
    if fr != 'en' and to != 'en':
        return translate(translate(s, fr=fr), to=to)
    return '\n'.join([i['translatedText'] for i in requests.post("https://www.sgtranslatetogether.gov.sg/api/translate?source={}_SG&target={}_SG".format(fr,to), json={"query": s}).json()['data']['translations']])


@slash.slash(name="sgtt", description = "Translate using SG Translate Together API", guild_ids=guild_ids, options=[
                create_option(
                 name="text",
                 description="Original text",
                 option_type=3,
                 required=True
               ), create_option(
                 name="fr",
                 description="Language code from (en zh ms ta). Defaults to en",
                 option_type=3,
                 required=False
               ), create_option(
                 name="to",
                 description="Language code to (en zh ms ta). Returns all if not specified",
                 option_type=3,
                 required=False
               )
    ])
async def _sgtt(ctx, text, fr='', to=''):
    cha = ctx.channel

    if to == '':
        if fr == '':
            fr = 'en'
        masdfasdf = await ctx.send(text+"\n...")
        asdfa = [text]
        langcodes = "en zh ms ta".split()
        langcodes.remove(fr)
        for to in langcodes:
            asdfa.append(translate(text, fr=fr, to=to)[:1996])
            try:
                await masdfasdf.edit(content='\n'.join(asdfa) + ("\n..." if to != "ta" else ""))
            except:
                await masdfasdf.edit(content='\n'.join(asdfa[:-1]))
                asdfa = [asdfa[-1]]
                masdfasdf = await cha.send(asdfa[0] + ("\n..." if to != "ta" else ""))
    else:
        masdfasdf = await ctx.send(text[:1996]+"\n...")
        trertert = translate(text, fr=fr, to=to)
        try:
            await masdfasdf.edit(content=text + "\n" + trertert)
        except:
            await masdfasdf.edit(content=text)
            await cha.send(trertert[:2000])

@slash.slash(name="badtranslate", description = "Translate to another language and back many times", guild_ids=guild_ids, options=[
                create_option(
                 name="text",
                 description="Text in English",
                 option_type=3,
                 required=True
               )
    ])
async def _badtranslate(ctx, text):
    s = text
    madffffff = await ctx.channel.send(s)
    for i in range(100):
        for j in "zh ms ta".split():
            s = translate(translate(s, to=j), fr=j)
            await madffffff.edit(content=s[:2000])



# @bot.command(brief="Deliberately bad calculation")
# async def add(ctx, arg):
#     try:
#         await ctx.message.channel.send(str(eval(arg)))
#     except Exception as e:
#         await ctx.message.channel.send(str(e))

bot.run(os.environ.get("TOKEN"))

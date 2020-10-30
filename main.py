import discord, random, keep_alive, json#, collections
from discord.ext import commands
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://old.randomtriviagenerator.com/"

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix, help_command = None)

@client.command()
async def help(context):
  embed=discord.Embed(title="**Command Summary**", description=None, color=discord.Colour.orange())
  embed.add_field(name="**ping**", value="Returns bot latency", inline=True)
  embed.add_field(name="**changeprefix (new prefix)**", value="Changes prefix to argument", inline=True)
  embed.add_field(name="**freq**" , value="Returns chance of sending a question on each non-command message", inline=True)
  embed.add_field(name="**changefreq (new frequency)**", value="Changes frequeny to argument", inline=True)
  embed.add_field(name="**testconnect**", value="Attempts to connect to trivia site and returns result", inline=True)
  embed.add_field(name="**category (category)**", value="Returns of which categories trivia questions will be", inline=True)
  embed.add_field(name="**changecategory (category)**", value="Limits trivia questions to the following category or categories. Category options are: arts & lit, geography, entertainment, history, science & nature, misc, or all", inline=True)
  embed.add_field(name="**question (category)**", value="Returns a trivia question. Category can be of any of the above listed or blank for random", inline=True)
  embed.add_field(name="**ans (answer)**", value="Answers previous question with argument", inline=True)
  embed.add_field(name="**rightanswer**", value="Returns the correct answer to the previous question", inline=True)
  embed.add_field(name="**myscore**", value="Returns author's score", inline=True)
  embed.add_field(name="**serverscores**", value="Returns the scores for all server members", inline=True)
  embed.add_field(name="**credits**", value="Returns who I owe this bot's existence to :)", inline=True)
  await context.send(embed=embed)

@client.event
async def on_guild_join(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  with open('answers.json', 'r') as f:
    answers = json.load(f)

  with open('frequencies.json', 'r') as f:
    frequencies = json.load(f)
  
  with open('scores.json', 'r') as f:
    scores = json.load(f)

  with open('categories.json', 'r') as f:
    categories = json.load(f)
  
  prefixes[str(guild.id)] = '$'
  answers[str(guild.id)] = None
  frequencies[str(guild.id)] = .04
  categories[str(guild.id)] = [4, 7, 10, 13, 16, 19]
  scores[str(guild.id)] = {}

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=2)

  with open('answers.json', 'w') as f:
    json.dump(answers, f, indent=2)

  with open('frequencies.json', 'w') as f:
    json.dump(frequencies, f, indent=2)

  with open('scores.json', 'w') as f:
    json.dump(scores, f, indent=2)

  with open('categories.json', 'w') as f:
    json.dump(categories, f, indent=2)

@client.event
async def on_guild_remove(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  with open('answers.json', 'r') as f:
    answers = json.load(f)

  with open('frequencies.json', 'r') as f:
    frequencies = json.load(f)

  with open('scores.json', 'r') as f:
    scores = json.load(f)

  with open('categories.json', 'r') as f:
    categories = json.load(f)

  prefixes.pop(str(guild.id))
  answers.pop(str(guild.id))
  frequencies.pop(str(guild.id))
  scores.pop(str(guild.id))
  categories.pop(str(guild.id))

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=2)

  with open('answers.json', 'w') as f:
    json.dump(answers, f, indent=2)

  with open('frequencies.json', 'w') as f:
    json.dump(frequencies, f, indent=2)

  with open('scores.json', 'w') as f:
    json.dump(scores, f, indent=2)

  with open('categories.json', 'w') as f:
    json.dump(categories, f, indent=2)

@client.event
async def on_command_error(context, *args):
  None

@client.event
async def on_ready():
    print("Bot is ready.")

@client.command()
async def ping(context):
  await context.send(f'bot latency = {round(client.latency * 1000)}ms')

@client.command()
async def changeprefix(context, prefix):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

    prefixes[str(context.guild.id)] = prefix

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=2)

  await context.send("Prefix is now " + prefix)

@client.command()
async def freq(context):
  with open('frequencies.json', 'r') as f:
    frequencies = json.load(f)

  freq = frequencies[str(context.guild.id)]
  await context.send(freq)

@client.command()
async def changefreq(context, arg):
    try:
        if 0<=float(arg)<=1:
            with open('frequencies.json', 'r') as f:
              frequencies = json.load(f)

              frequencies[str(context.guild.id)] = float(arg)

            with open('frequencies.json', 'w') as f:
              json.dump(frequencies, f, indent=2)

            await context.send("frequency is now " + arg)
        else:
            await context.send("Sorry, the frequency must be a real number between 0 and 1")
    except:
        await context.send("Incompatible frequency")

@client.command()
async def testconnect(context):
  try:
    urlopen(url)
    await context.send("Able to connect to trivia site")
  except:
    await context.send("Could not connect to trivia site")

@client.command()
async def category(context):
  with open('categories.json', 'r') as f:
    categories = json.load(f)

  category = categories[str(context.guild.id)]
  if category != None:
    string = "your categories are: "
    for i in category:
      if i == 4:
        string = string + 'arts & lit, '
      if i == 7:
        string = string + 'geography, '
      if i == 10:
        string = string + 'entertainment, '
      if i == 13:
        string = string + 'history, '
      if i == 16:
        string = string + 'science & nature, '
      if i == 19:
        string = string + 'miscellaneous, '
    await context.send(string[:-2])
  else:
    await context.send("Questions can be of any category!")

@client.command()
async def changecategory(context, *category):
  with open('categories.json', 'r') as f:
    categories = json.load(f)

  l = []
  category = ''.join(category).lower()
  if 'arts' in category or 'lit' in category:
    l.append(4)
  if 'geo' in category:
    l.append(7)
  if 'ent' in category:
    l.append(10)
  if 'hist' in category:
    l.append(13)
  if 'sci' in category or 'nat' in category:
    l.append(16)
  if 'misc' in category:
    l.append(19)

  if len(l) == 0:
    l = [4,7,10,13,16,19]
    await context.send("Trivia questions can now be of any category!")
  else:
    string = "your new categories are: "
    for i in l:
      if i == 4:
        string = string + 'arts & lit, '
      if i == 7:
        string = string + 'geography, '
      if i == 10:
        string = string + 'entertainment, '
      if i == 13:
        string = string + 'history, '
      if i == 16:
        string = string + 'science & nature, '
      if i == 19:
        string = string + 'miscellaneous, '
    await context.send(string[:-2])

  categories[str(context.guild.id)] = l

  with open('categories.json', 'w') as f:
    json.dump(categories, f, indent=2)

@client.command()
async def question(context, *category):
  try:
    page = urlopen(url)
  except:
    print("Error opening the URL")

  soup = BeautifulSoup(page, 'html.parser')

  l = []
  category = ''.join(category).lower()
  if 'arts' in category or 'lit' in category:
    l.append(4)
  if 'geo' in category:
    l.append(7)
  if 'ent' in category:
    l.append(10)
  if 'hist' in category:
    l.append(13)
  if 'sci' in category or 'nat' in category:
    l.append(16)
  if 'misc' in category:
    l.append(19)

  if len(l) == 0:
    with open('categories.json', 'r') as f:
      categories = json.load(f)
    l=categories[str(context.guild.id)]
  
  n=random.choice(l)

  string = str(soup.findAll('td')[n])
  string = string[string.index('>', 17)+1:-9]
  embed=discord.Embed(title="**Question**", description=string, color=discord.Colour.orange())
  await context.send(embed=embed)
  anser = str(soup.findAll('td')[n+1])[17:-5]

  with open('answers.json', 'r') as f:
    answers = json.load(f)

  answers[str(context.guild.id)] = anser

  with open('answers.json', 'w') as f:
    json.dump(answers, f, indent=2)

@client.command()
async def ans(context, *message):
  message = " ".join(message[:])
  message = message.lower()

  with open('answers.json', 'r') as f:
    answers = json.load(f)

  temp = answers[str(context.guild.id)].lower()
  if message==temp:                
    answers[str(context.guild.id)] = None
    with open('answers.json', 'w') as f:
      json.dump(answers, f, indent=2)

    with open('scores.json', 'r') as f:
      scores = json.load(f)
    if str(context.author.id) in scores[str(context.guild.id)]:
      scores[str(context.guild.id)][str(context.author.id)] = scores[str(context.guild.id)][str(context.author.id)]+1
    else:
      scores[str(context.guild.id)][str(context.author.id)] = 1
    with open('scores.json', 'w') as f:
      json.dump(scores, f, indent=2)

    with open('scores.json', 'r') as f:
      scores = json.load(f)
    await context.send(f"That's right! Your score is now {scores[str(context.guild.id)][str(context.author.id)]}")
  else:
      await context.send("Sorry, that's incorrect")

@client.command()
async def rightanswer(context):
  with open('answers.json', 'r') as f:
    answers = json.load(f)

  anser = answers[str(context.guild.id)]

  if anser != None:
    await context.send("The correct answer was: " + anser)
        
    answers[str(context.guild.id)] = None

    with open('answers.json', 'w') as f:
      json.dump(answers, f, indent=2)
  else:
    await context.send("No question has been asked.")

@client.command()
async def myscore(context):
  with open('scores.json', 'r') as f:
    scores = json.load(f)

  if(str(context.author.id) in scores[str(context.guild.id)]):
    await context.send(f"Your score is {scores[str(context.guild.id)][str(context.author.id)]}")
  else:
    scores[str(context.guild.id)][str(context.author.id)] = 0
    await context.send("Your score is 0")

  with open('scores.json', 'w') as f:
      json.dump(scores, f, indent=2)

@client.command()
async def serverscores(context):
  with open('scores.json', 'r') as f:
    scores = json.load(f)

  if(str(context.author.id) not in scores[str(context.guild.id)]):
    scores[str(context.guild.id)][str(context.author.id)] = 0
  else:
    scores[str(context.guild.id)][str(context.author.id)] = 0

  with open('scores.json', 'w') as f:
      json.dump(scores, f, indent=2)
  
  embed=discord.Embed(title="**Top Server Scores**", description=None, color=discord.Colour.orange())

  for i in scores[str(context.guild.id)]:
    a=scores[str(context.guild.id)][i]
    for j in scores[str(context.guild.id)]:
      b=scores[str(context.guild.id)][j]
      if b<a:
        temp = scores[str(context.guild.id)][j]
        scores[str(context.guild.id)][j] = scores[str(context.guild.id)][i]
        scores[str(context.guild.id)][i] = temp
  
  i=0
  for member in scores[str(context.guild.id)]:
    i=i+1
    user = await client.fetch_user(int(member))
    embed.add_field(name=f"**{user}**", value=scores[str(context.guild.id)][member], inline=False)
    if i==10:
      break

  await context.send(embed=embed)
'''
@client.command()
async def globalscores(context):
  with open('scores.json', 'r') as f:
    scores = json.load(f)

  if(str(context.author.id) not in scores[str(context.guild.id)]):
    scores[str(context.guild.id)][str(context.author.id)] = 0
  else:
    scores[str(context.guild.id)][str(context.author.id)] = 0

  with open('scores.json', 'w') as f:
      json.dump(scores, f, indent=2)
  
  embed=discord.Embed(title="**Top Global Scores**", description=None, color=discord.Colour.orange())

  d = {}
  for guild in scores.values():
    if guild == "data":
      continue
    print(guild)
    try:
      d.update(guild)
    except:
      None

  for i in d:
    a=i
    for j in d:
      b=d[j]
      if b<a:
        temp = d[j]
        d[j] = d[i]
        d[i] = temp

  i=0
  for member in d:
    i=i+1
    user = await client.fetch_user(int(member))
    embed.add_field(name=f"**{user}**", value=d[member], inline=False)
    if i==10:
      break

  await context.send(embed=embed)


  top = collections.deque([], maxlen = 10)

  id = list(scores.keys())[1]

  for i in scores[id]:
    a=scores[str(context.guild.id)][i]
    for j in scores[id]:
      b=scores[id][j]
      if b<a:
        temp = scores[id][j]
        scores[id][j] = scores[id][i]
        scores[id][i] = temp
  i=0
  for member in scores[id]:
    i=i+1
    top.append({member: scores[id][member]})
    if i==10:
      break

  for guild in scores:
    if guild == "data" or guild == scores[id]:
      continue
    for member in scores[guild]:
      a=scores[guild][member]
      for i in top:
        print(a)
        print(list(i.values())[0])
        if a<list(i.values())[0]:
          try:
            print(a>list(i.values())[0])
            top.insert(i+1, {member, scores[guild][member]})
            print('hi')
            break
          except:
            None
  
  n=0
  for i in top:
    n=n+1
    user = await client.fetch_user(int(list(i.keys())[0]))
    embed.add_field(name=f"**{user}**", value=str(i[list(i.keys())[0]]), inline=False)
    if n==10:
      break
  
  await context.send(embed=embed)
  '''

@client.command()
async def credits(context):
  embed=discord.Embed(title="**Credits**", description=None, color=discord.Colour.orange())
  embed.add_field(name="**Trivia Source: **", value="old.randomtriviagenerator.com", inline=True)
  embed.add_field(name="**Bot Hosting: **", value="Repl.it", inline=True)
  embed.add_field(name="**Bot Pinging: **", value="uptimerobot.com", inline=True)
  embed.add_field(name="\u200b", value="**Thank you to all these amazing sites for making this bot possible!!**", inline=False)
  
  await context.send(embed=embed)
    
@client.event
async def on_message(message):
  context = await client.get_context(message)

  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefix = prefixes[str(context.guild.id)]
      
  with open('frequencies.json', 'r') as f:
    frequencies = json.load(f)

  freq = frequencies[str(context.guild.id)]

  if random.random() < float(freq) and str(message.content).startswith(prefix) == False and message.author != client.user:
    try:
        page = urlopen(url)
    except:
        print("Error opening the URL")

    soup = BeautifulSoup(page, 'html.parser')
            
    with open('categories.json', 'r') as f:
      categories = json.load(f)

    n=random.choice(categories[str(context.guild.id)])
    string = str(soup.findAll('td')[n])
    string = string[string.index('>', 17)+1:-9]
    embed=discord.Embed(title="**Question**", description=string, color=discord.Colour.orange())
    await context.send(embed=embed)
    anser = str(soup.findAll('td')[n+1])[17:-5]

    with open('answers.json', 'r') as f:
      answers = json.load(f)

    answers[str(context.guild.id)] = anser

    with open('answers.json', 'w') as f:
      json.dump(answers, f, indent=2)

  await client.process_commands(message)

keep_alive.keep_alive()
client.run('Njk3MjQyNTIzMzI3OTIyMTg2.Xo0bsw.0R_nXIxQAfVnWnDYvqZjAEmGr3I')

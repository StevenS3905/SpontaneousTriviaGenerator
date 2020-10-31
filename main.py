import discord, random, keep_alive, json, collections
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
  embed.add_field(name="**ping**", value="Returns bot latency", inline=False)
  embed.add_field(name="**changeprefix (new prefix)**", value="Changes prefix to argument", inline=False)
  embed.add_field(name="**freq**" , value="Returns chance of sending a question on each non-command message", inline=False)
  embed.add_field(name="**changefreq (new frequency)**", value="Changes frequeny to argument", inline=False)
  embed.add_field(name="**testconnect**", value="Attempts to connect to trivia site and returns result", inline=False)
  embed.add_field(name="**category (category)**", value="Returns of which categories trivia questions will be", inline=False)
  embed.add_field(name="**changecategory (category)**", value="Limits trivia questions to the following category or categories. Category options are: arts & lit, geography, entertainment, history, science & nature, misc, or all", inline=False)
  embed.add_field(name="**question (category)**", value="Returns a trivia question. Category can be of any of the above listed or blank for random", inline=False)
  embed.add_field(name="**ans (answer)**", value="Answers previous question with argument", inline=False)
  embed.add_field(name="**rightanswer**", value="Returns the correct answer to the previous question", inline=False)
  embed.add_field(name="**myscore**", value="Returns author's score", inline=False)
  embed.add_field(name="**serverscores**", value="Returns the scores for all server members", inline=False)
  embed.add_field(name="**credits**", value="Returns who I owe this bot's existence to :)", inline=False)
  embed.add_field(name="**Github: https://github.com/StevenS3905/SpontaneousTriviaGenerator.git**", value="\u200b", inline=False)
  await context.send(embed=embed)

@client.event
async def on_guild_join(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  with open('answers.json', 'r') as f:
    answers = json.load(f)

  with open('frequencies.json', 'r') as f:
    frequencies = json.load(f)
  
  with open('servers.json', 'r') as f:
    servers = json.load(f)

  with open('categories.json', 'r') as f:
    categories = json.load(f)
  
  prefixes[str(guild.id)] = '$'
  answers[str(guild.id)] = None
  frequencies[str(guild.id)] = .04
  categories[str(guild.id)] = [4, 7, 10, 13, 16, 19]
  servers[str(guild.id)] = {}

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=2)

  with open('answers.json', 'w') as f:
    json.dump(answers, f, indent=2)

  with open('frequencies.json', 'w') as f:
    json.dump(frequencies, f, indent=2)

  with open('servers.json', 'w') as f:
    json.dump(servers, f, indent=2)

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

  with open('servers.json', 'r') as f:
    servers = json.load(f)

  with open('categories.json', 'r') as f:
    categories = json.load(f)

  prefixes.pop(str(guild.id))
  answers.pop(str(guild.id))
  frequencies.pop(str(guild.id))
  servers.pop(str(guild.id))
  categories.pop(str(guild.id))

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=2)

  with open('answers.json', 'w') as f:
    json.dump(answers, f, indent=2)

  with open('frequencies.json', 'w') as f:
    json.dump(frequencies, f, indent=2)

  with open('servers.json', 'w') as f:
    json.dump(servers, f, indent=2)

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

  await context.send(frequencies[str(context.guild.id)])

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
  if len(category) != 6:
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
  string = "your new categories are: "
  if 'arts' in category or 'lit' in category:
    l.append(4)
    string = string + 'arts & lit, '    
  if 'geo' in category:
    l.append(7)
    string = string + 'geography, '
  if 'ent' in category:
    l.append(10)
    string = string + 'entertainment, '
  if 'hist' in category:
    l.append(13)
    string = string + 'history, '
  if 'sci' in category or 'nat' in category:
    l.append(16)
    string = string + 'science & nature, '
  if 'misc' in category:
    l.append(19)
    string = string + 'miscellaneous, '

  if len(l) == 0:
    l = [4,7,10,13,16,19]
    await context.send("Trivia questions can now be of any category!")
  else:
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
    

    with open('users.json', 'r') as f:
      users = json.load(f)

    with open('servers.json', 'r') as f:
      servers = json.load(f)

    if str(context.author.id) in users.keys():
      users[str(context.author.id)] = users[str(context.author.id)]+1
    else:
      users[str(context.author.id)] = 1

    if str(context.author.id) not in servers[str(context.guild.id)]:
      servers[str(context.guild.id)].append(str(context.author.id))

    with open('servers.json', 'w') as f:
      json.dump(servers, f, indent=2)

    with open('users.json', 'w') as f:
      json.dump(users, f, indent=2)

    await context.send(f"That's right! Your score is now {users[str(context.author.id)]}")

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
  with open('servers.json', 'r') as f:
    servers = json.load(f)

  with open('users.json', 'r') as f:
    users = json.load(f)

  if str(context.author.id) in users.keys():
    await context.send(f"Your score is {users[str(context.author.id)]}")
  else:
    users[str(context.author.id)] = 0
    await context.send("Your score is 0")
    
  if str(context.author.id) not in servers[str(context.guild.id)]:
    servers[str(context.guild.id)].append(str(context.author.id))
  
  with open('users.json', 'w') as f:
    json.dump(users, f, indent=2)

  with open('servers.json', 'w') as f:
    json.dump(servers, f, indent=2)

@client.command()
async def serverscores(context):
  with open('servers.json', 'r') as f:
    servers = json.load(f)
  
  with open('users.json', 'r') as f:
    users = json.load(f)

  if(str(context.author.id) not in users.keys()):
    users[str(context.author.id)] = 0

  if str(context.author.id) not in servers[str(context.guild.id)]:
    servers[str(context.guild.id)].append(str(context.author.id))

  with open('users.json', 'w') as f:
    json.dump(users, f, indent=2)

  with open('servers.json', 'w') as f:
    json.dump(servers, f, indent=2)

  embed=discord.Embed(title="**Top Server servers**", description=None, color=discord.Colour.orange())

  l=collections.deque([servers[str(context.guild.id)][0]], maxlen=10)
  for i in servers[str(context.guild.id)][1:]:
    print(l)
    print(i)
    n=0
    for j in l:
      if users[i] < users[j]:
        if len(l) == 10:
          del l[0]
          l.insert(n-1, i)
        else:
          l.insert(n, i)
        break
      n=n+1
      if n==len(l) and users[i] >= users[j]:
        if len(l) == 10:
          del l[0]
        l.insert(len(l), i)
        break

  l.reverse()

  for member in l:
    user = await client.fetch_user(int(member))
    embed.add_field(name=f"**{user}**", value=users[str(member)], inline=False)

  await context.send(embed=embed)

@client.command()
async def globalscores(context):
  with open('users.json', 'r') as f:
    users = json.load(f)

  with open('servers.json', 'r') as f:
    servers = json.load(f)

  if str(context.author.id) not in users.keys():
    users[str(context.author.id)] = 0

  if str(context.author.id) not in servers[str(context.guild.id)]:
    servers[str(context.guild.id)].append(str(context.author.id))

  with open('users.json', 'w') as f:
    json.dump(users, f, indent=2)

  with open('servers.json', 'w') as f:
    json.dump(servers, f, indent=2)
  
  embed=discord.Embed(title="**Top Global servers**", description=None, color=discord.Colour.orange())

  l=collections.deque([], maxlen=10)

  l.append(list(users.keys())[1])

  for i in list(users.keys())[2:]:
    n=0
    for j in l:
      if users[i] < users[j]:
        if len(l) == 10:
          del l[0]
          l.insert(n-1, i)
        else:
          l.insert(n, i)
        break
      n=n+1
      if n==len(l) and users[i] >= users[j]:
        if len(l) == 10:
          del l[0]
        l.insert(len(l), i)
        break

  l.reverse()

  for member in l:
    user = await client.fetch_user(member)
    embed.add_field(name=f"**{user}**", value=users[member], inline=False)
  
  await context.send(embed=embed)

@client.command()
async def credits(context):
  embed=discord.Embed(title="**Credits**", description=None, color=discord.Colour.orange())
  embed.add_field(name="**Trivia Source: **", value="old.randomtriviagenerator.com", inline=False)
  embed.add_field(name="**Bot Hosting: **", value="Repl.it", inline=False)
  embed.add_field(name="**Bot Pinging: **", value="uptimerobot.com", inline=False)
  embed.add_field(name="\u200b", value="**Thank you to all these amazing sites for making this bot possible!!**", inline=False)
  
  await context.send(embed=embed)
    
@client.event
async def on_message(message):
  context = await client.get_context(message)

  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  if context.guild.id in prefixes.keys():
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
client.run('''token''')

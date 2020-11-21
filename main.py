import discord, random, json, collections, string, math
from discord.ext import commands
from discord.utils import find
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://old.randomtriviagenerator.com/"

def get_prefix(client, message):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix, help_command = None)
errorclient = discord.Client()

@client.command()
async def help(context):
  embed=discord.Embed(title="**Command Summary**", description=None, color=discord.Colour.orange())
  embed.add_field(name="**ping**", value="Returns bot latency", inline=False)
  embed.add_field(name="**changeprefix (prefix)**", value="Changes prefix to the given prefix", inline=False)
  embed.add_field(name="**freq**" , value="Returns chance of sending a question on each non-command message", inline=False)
  embed.add_field(name="**changefreq (frequency)**", value="Changes frequeny to the given frequency", inline=False)
  embed.add_field(name="**direct (channel)**", value="Future spontaneous trivia will be sent to the specified channel", inline=False)
  embed.add_field(name="**testconnect**", value="Attempts to connect to trivia site and returns result", inline=False)
  embed.add_field(name="**category**", value="Returns of which categories trivia questions will be", inline=False)
  embed.add_field(name="**changecategory (category/categories)**", value="Limits trivia questions to the following category or categories. Category options are: arts & lit, geography, entertainment, history, science & nature, misc, or all", inline=False)
  embed.add_field(name="**question (category/categories)**", value="Returns a trivia question. Category/ies will follow the server default unless category/ies are given", inline=False)
  embed.add_field(name="**hint (additional hint level 1-5)**", value="First level shows how many words in the answer and how many letters in each word. Each higher level reveals ~1/5 of the letters in the word. With each level of hint, the points awarded from a correct answer decrease by 1. The default hint level is 1.", inline=False)
  embed.add_field(name="**ans (answer)**", value="Answers previous question with given answer", inline=False)
  embed.add_field(name="**rightans**", value="Returns the correct answer to the previous question", inline=False)
  embed.add_field(name="**myscore**", value="Returns author's score", inline=False)
  embed.add_field(name="**serverscores**", value="Returns the scores for all server members", inline=False)
  embed.add_field(name="**credits**", value="Returns who I owe this bot's existence to :)", inline=False)
  embed.add_field(name="**Github: https://github.com/StevenS3905/SpontaneousTriviaGenerator.git**", value="\u200b", inline=False)
  await context.send(embed=embed)

@client.event
async def on_guild_join(guild):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  with open("answers.json", "r") as f:
    answers = json.load(f)

  with open("frequencies.json", "r") as f:
    frequencies = json.load(f)
  
  with open("servers.json", "r") as f:
    servers = json.load(f)

  with open("categories.json", "r") as f:
    categories = json.load(f)

  with open("hints.json", "r") as f:
    hints = json.load(f)

  with open("points.json", "r") as f:
    points = json.load(f)
  
  with open("channels.json", "r") as f:
    channels = json.load(f)
  
  prefixes[str(guild.id)] = "$"
  answers[str(guild.id)] = None
  frequencies[str(guild.id)] = .04
  categories[str(guild.id)] = [4, 7, 10, 13, 16, 19]
  servers[str(guild.id)] = {}
  hints[str(guild.id)] = None
  points[str(guild.id)] = 5
  channels[str(guild.id)] = None

  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f, indent=2)

  with open("answers.json", "w") as f:
    json.dump(answers, f, indent=2)

  with open("frequencies.json", "w") as f:
    json.dump(frequencies, f, indent=2)

  with open("servers.json", "w") as f:
    json.dump(servers, f, indent=2)

  with open("categories.json", "w") as f:
    json.dump(categories, f, indent=2)

  with open("hints.json", "w") as f:
    json.dump(hints, f, indent=2)

  with open("points.json", "w") as f:
    json.dump(points, f, indent=2)
    
  with open("channels.json", "w") as f:
    json.dump(channels, f, indent=2)

  general = find(lambda x: x.name == "general",  guild.text_channels)
  if general and general.permissions_for(guild.me).send_messages:
    embed=discord.Embed(title="**Hello!**", description="Thank you for inviting me to your server! I'm still in my developmental stages so if you find any bugs, have any suggestions, or would like some help, please join my support server. Any input would be greatly appreciated! https://discord.gg/cBNQpV6rwh", color=discord.Colour.orange())
    await general.send(embed=embed)

@client.event
async def on_guild_remove(guild):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  with open("answers.json", "r") as f:
    answers = json.load(f)

  with open("frequencies.json", "r") as f:
    frequencies = json.load(f)

  with open("servers.json", "r") as f:
    servers = json.load(f)

  with open("categories.json", "r") as f:
    categories = json.load(f)

  with open("hints.json", "r") as f:
    hints = json.load(f)

  with open("points.json", "r") as f:
    points = json.load(f)
    
  with open("channels.json", "r") as f:
    channels = json.load(f)

  prefixes.pop(str(guild.id))
  answers.pop(str(guild.id))
  frequencies.pop(str(guild.id))
  servers.pop(str(guild.id))
  categories.pop(str(guild.id))
  hints.pop(str(guild.id))
  points.pop(str(guild.id))
  channels.pop(str(guild.id))

  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f, indent=2)

  with open("answers.json", "w") as f:
    json.dump(answers, f, indent=2)

  with open("frequencies.json", "w") as f:
    json.dump(frequencies, f, indent=2)

  with open("servers.json", "w") as f:
    json.dump(servers, f, indent=2)

  with open("categories.json", "w") as f:
    json.dump(categories, f, indent=2)

  with open("hints.json", "w") as f:
    json.dump(hints, f, indent=2)

  with open("points.json", "w") as f:
    json.dump(points, f, indent=2)
    
  with open("channels.json", "w") as f:
    json.dump(channels, f, indent=2)

@client.event
async def on_command_error(context, error):
  pass

@client.event
async def on_ready():
  print("Bot is ready.")

@client.command()
async def ping(context):
  await context.send(f"bot latency = {round(client.latency * 1000)}ms")

@client.command()
async def changeprefix(context, prefix):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  prefixes[str(context.guild.id)] = prefix

  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f, indent=2)

  await context.send("Prefix is now " + prefix)

@client.command()
async def freq(context):
  with open("frequencies.json", "r") as f:
    frequencies = json.load(f)

  await context.send(frequencies[str(context.guild.id)])

@client.command()
async def changefreq(context, arg):
  try:
    if 0<=float(arg)<=1:
      with open("frequencies.json", "r") as f:
        frequencies = json.load(f)

      frequencies[str(context.guild.id)] = float(arg)

      with open("frequencies.json", "w") as f:
        json.dump(frequencies, f, indent=2)

      await context.send("frequency is now " + arg)
    else:
      await context.send("Sorry, the frequency must be a real number between 0 and 1")
  except:
    await context.send("Incompatible frequency")

@client.command()
async def direct(context, id):
  channel = context.guild.get_channel(int(id[2:-1]))
  if channel == None:
    await context.send("Specificied channel could not be found")
  elif channel.permissions_for(context.guild.me).send_messages and channel.permissions_for(context.guild.me).read_messages:

    with open("channels.json", "r") as f:
      channels = json.load(f)

    channels[str(context.guild.id)] = int(id[2:-1])

    with open("channels.json", "w") as f:
      json.dump(channels, f, indent=2)

    await context.send("Future spontaneous trivia questions will be sent to "+id)
  else:
    await context.send("I am not permitted to send and receive messages in this channel")

@client.command()
async def testconnect(context):
  try:
    urlopen(url)
    await context.send("Able to connect to trivia site")
  except:
    await context.send("Could not connect to trivia site")

@client.command()
async def category(context):
  with open("categories.json", "r") as f:
    categories = json.load(f)

  category = categories[str(context.guild.id)]
  if len(category) != 6:
    strng = "your categories are: "
    for i in category:
      if i == 4:
        strng = strng + "arts & lit, "
      if i == 7:
        strng = strng + "geography, "
      if i == 10:
        strng = strng + "entertainment, "
      if i == 13:
        strng = strng + "history, "
      if i == 16:
        strng = strng + "science & nature, "
      if i == 19:
        strng = strng + "miscellaneous, "
    await context.send(strng[:-2])
  else:
    await context.send("Questions can be of any category!")

@client.command()
async def changecategory(context, *category):
  with open("categories.json", "r") as f:
    categories = json.load(f)

  l = []
  category = "".join(category).lower()
  strng = "your new categories are: "
  if "arts" in category or "lit" in category:
    l.append(4)
    strng = strng + "arts & lit, "    
  if "geo" in category:
    l.append(7)
    strng = strng + "geography, "
  if "ent" in category:
    l.append(10)
    strng = strng + "entertainment, "
  if "hist" in category:
    l.append(13)
    strng = strng + "history, "
  if "sci" in category or "nat" in category:
    l.append(16)
    strng = strng + "science & nature, "
  if "misc" in category:
    l.append(19)
    strng = strng + "miscellaneous, "

  if len(l) == 0:
    l = [4,7,10,13,16,19]
    await context.send("Trivia questions can now be of any category!")
  else:
    await context.send(strng[:-2])

  categories[str(context.guild.id)] = l

  with open("categories.json", "w") as f:
    json.dump(categories, f, indent=2)

@client.command()
async def question(context, *category):
  try:
    page = urlopen(url)
  except:
    await context.send("Error opening the URL")

  soup = BeautifulSoup(page, "html.parser")

  l = []
  category = "".join(category).lower()
  if "arts" in category or "lit" in category:
    l.append(4)
  if "geo" in category:
    l.append(7)
  if "ent" in category:
    l.append(10)
  if "hist" in category:
    l.append(13)
  if "sci" in category or "nat" in category:
    l.append(16)
  if "misc" in category:
    l.append(19)

  if len(l) == 0:
    with open("categories.json", "r") as f:
      categories = json.load(f)
    l=categories[str(context.guild.id)]
  
  n=random.choice(l)

  strng = str(soup.findAll("td")[n])
  strng = strng[strng.index(">", 17)+1:-9]
  embed=discord.Embed(title="**Question**", description=strng, color=discord.Colour.orange())
  await context.send(embed=embed)
  anser = str(soup.findAll("td")[n+1])[17:-5]

  with open("points.json", "r") as f:
    points = json.load(f)

  with open("answers.json", "r") as f:
    answers = json.load(f)

  answers[str(context.guild.id)] = anser.replace("&amp;", "&")
  points[str(context.guild.id)] = 5

  with open("answers.json", "w") as f:
    json.dump(answers, f, indent=2)

  with open("points.json", "w") as f:
    json.dump(points, f, indent=2)

  with open("hints.json", "r") as f:
    hints = json.load(f)

  hints[str(context.guild.id)] = None

  with open("hints.json", "w") as f:
    json.dump(hints, f, indent=2)

  with open("data.json", "r") as f:
    data = json.load(f)

  data["5questions"] = data["5questions"] + 1

  with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

@client.command()
async def hint(context, n=1):
  with open("points.json", "r") as f:
    points = json.load(f)
  
  with open("answers.json", "r") as f:
    answers = json.load(f)

  with open("hints.json", "r") as f:
    hints = json.load(f)

  if answers[str(context.guild.id)] == None:
    await context.send("No question has been asked")
  elif points[str(context.guild.id)] == 1:
    s = hints[str(context.guild.id)]
    for i in range(len(s)):
      s = s[:i*2] + " " + s[i*2:]
    await context.send("No more hints are available for this question\nThe answer looks like: " + s.replace("_", "\_"))
  else:
    if hints[str(context.guild.id)] == None:
      s = ""
      for i in answers[str(context.guild.id)]:
        if i in string.punctuation or i == " ":
          s = s + i
        else:
          s = s + "_"
      n = n-1
      points[str(context.guild.id)] = points[str(context.guild.id)]-1
      hints[str(context.guild.id)] = s

    while n != 0 and points[str(context.guild.id)] != 1:
      s = hints[str(context.guild.id)]
      if s.count("_") <= math.ceil(1/5 * len(answers[str(context.guild.id)])):
        await context.send("No more hints are available for this question")
        break
      p = 1/5 * len(answers[str(context.guild.id)])
      if bool(random.getrandbits(1)) == True and s.count("_") > points[str(context.guild.id)] * math.ceil(p) or math.floor(p) == 0:
        p = math.ceil(p)
      else:
        p = math.floor(p)
      for i in range(p):
        index=random.choice(range(s.count("_")))
        undcounter = -1
        charcounter = -1
        for j in s:
          charcounter = charcounter + 1
          if j == "_":
            undcounter = undcounter + 1
          if undcounter == index:
            s = s[:charcounter] + answers[str(context.guild.id)][charcounter] + s[charcounter + 1:]
            break
      points[str(context.guild.id)] = points[str(context.guild.id)]-1
      n=n-1
      hints[str(context.guild.id)] = s

    for i in range(len(s)):
      s = s[:i*2] + " " + s[i*2:]
    await context.send("The answer looks like: " + s.replace("_", "\_"))
    
    with open("data.json", "r") as f:
      data = json.load(f)

    data[str(points[str(context.guild.id)])+"questions"] = data[str(points[str(context.guild.id)])+"questions"] + 1

    with open("data.json", "w") as f:
      json.dump(data, f, indent=2)

    with open("hints.json", "w") as f:
      json.dump(hints, f, indent=2)

    with open("points.json", "w") as f:
      json.dump(points, f, indent=2)

@client.command()
async def ans(context, *message):
  with open("answers.json", "r") as f:
    answers = json.load(f)

  if answers[str(context.guild.id)] != None:
    message = " ".join(message[:])
    message = message.lower()

    with open("points.json", "r") as f:
      points = json.load(f)

    temp = answers[str(context.guild.id)].lower()

    if message==temp:                
      answers[str(context.guild.id)] = None

      with open("answers.json", "w") as f:
        json.dump(answers, f, indent=2)

      with open("users.json", "r") as f:
        users = json.load(f)

      with open("servers.json", "r") as f:
        servers = json.load(f)

      if str(context.author.id) in users.keys():
        users[str(context.author.id)] = users[str(context.author.id)]+points[str(context.guild.id)]
      else:
        users[str(context.author.id)] = points[str(context.guild.id)]

      if str(context.author.id) not in servers[str(context.guild.id)]:
        servers[str(context.guild.id)].append(str(context.author.id))

      with open("data.json", "r") as f:
        data = json.load(f)

      data[str(points[str(context.guild.id)])] = data[str(points[str(context.guild.id)])] + 1

      with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

      with open("servers.json", "w") as f:
        json.dump(servers, f, indent=2)

      with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

      points[str(context.guild.id)] = 5

      with open("points.json", "w") as f:
        json.dump(points, f, indent=2)

      with open("hints.json", "r") as f:
        hints = json.load(f)

      hints[str(context.guild.id)] = None

      with open("hints.json", "w") as f:
        json.dump(hints, f, indent=2)

      await context.send(f"That's right! Your score is now {users[str(context.author.id)]}")
    else:
        await context.send("Sorry, that's incorrect")
  else:
    await context.send("No question has been asked")

@client.command()
async def rightans(context):
  with open("points.json", "r") as f:
    points = json.load(f)
  
  with open("answers.json", "r") as f:
    answers = json.load(f)

  anser = answers[str(context.guild.id)]

  if anser != None:
    await context.send("The correct answer was: " + anser)
        
    answers[str(context.guild.id)] = None

    with open("answers.json", "w") as f:
      json.dump(answers, f, indent=2)

    with open("points.json", "r") as f:
      points = json.load(f)
    
    points[str(context.guild.id)] = 5

    with open("points.json", "w") as f:
      json.dump(points, f, indent=2)  

    with open("hints.json", "r") as f:
      hints = json.load(f)

    hints[str(context.guild.id)] = None

    with open("hints.json", "w") as f:
      json.dump(hints, f, indent=2)
  else:
    await context.send("No question has been asked.")

@client.command()
async def myscore(context):
  with open("servers.json", "r") as f:
    servers = json.load(f)

  with open("users.json", "r") as f:
    users = json.load(f)

  if str(context.author.id) in users.keys():
    await context.send(f"Your score is {users[str(context.author.id)]}")
  else:
    users[str(context.author.id)] = 0
    await context.send("Your score is 0")
    
  if str(context.author.id) not in servers[str(context.guild.id)]:
    servers[str(context.guild.id)].append(str(context.author.id))
  
  with open("users.json", "w") as f:
    json.dump(users, f, indent=2)

  with open("servers.json", "w") as f:
    json.dump(servers, f, indent=2)

@client.command()
async def serverscores(context):
  with open("servers.json", "r") as f:
    servers = json.load(f)
  
  with open("users.json", "r") as f:
    users = json.load(f)

  if(str(context.author.id) not in users.keys()):
    users[str(context.author.id)] = 0

  if str(context.author.id) not in servers[str(context.guild.id)]:
    servers[str(context.guild.id)].append(str(context.author.id))

  with open("users.json", "w") as f:
    json.dump(users, f, indent=2)

  with open("servers.json", "w") as f:
    json.dump(servers, f, indent=2)

  embed=discord.Embed(title="**Top Server servers**", description=None, color=discord.Colour.orange())

  l=collections.deque([servers[str(context.guild.id)][0]], maxlen=10)
  for i in servers[str(context.guild.id)][1:]:
    n=0
    for j in l:
      if users[i] < users[j] and n==0:
        break
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
  with open("users.json", "r") as f:
    users = json.load(f)

  with open("servers.json", "r") as f:
    servers = json.load(f)

  if str(context.author.id) not in users.keys():
    users[str(context.author.id)] = 0

  if str(context.author.id) not in servers[str(context.guild.id)]:
    servers[str(context.guild.id)].append(str(context.author.id))

  with open("users.json", "w") as f:
    json.dump(users, f, indent=2)

  with open("servers.json", "w") as f:
    json.dump(servers, f, indent=2)
  
  embed=discord.Embed(title="**Top Global servers**", description=None, color=discord.Colour.orange())

  l=collections.deque([], maxlen=10)

  l.append(list(users.keys())[1])

  for i in list(users.keys())[2:]:
    n=0
    for j in l:
      if users[i] < users[j] and n==0:
        break
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
  embed.add_field(name="**Bot Hosting: **", value="cp.something.host", inline=False)
  embed.add_field(name="\u200b", value="**Thank you to both these amazing sites for making this bot possible!!**", inline=False)
  await context.send(embed=embed)
    
@client.event
async def on_message(message):
  context = await client.get_context(message)
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  if str(context.guild.id) in prefixes.keys():
    prefix = prefixes[str(context.guild.id)]
        
    with open("frequencies.json", "r") as f:
      frequencies = json.load(f)

    freq = frequencies[str(context.guild.id)]

    if random.random() < float(freq) and str(message.content).startswith(prefix) == False and message.author != client.user:
      with open("channels.json", "r") as f:
        channels = json.load(f)

      changed = False
      if channels[str(context.guild.id)] !="inactive" and channels[str(context.guild.id)] != None:
        context = context.guild.get_channel(channels[str(context.guild.id)])
      elif context.channel.permissions_for(context.guild.me).send_messages == False or context.channel.permissions_for(context.guild.me).read_messages == False:
        for i in context.guild.text_channels:
          if "general" in i.name and i.permissions_for(i.guild.me).send_messages and i.permissions_for(i.guild.me).read_messages:
            channels[str(context.guild.id)] = i
            context = i
            changed = True
            break
        print(context.guild.get_channel.name)
        if changed == False:
          for i in context.guild.text_channels:
            if i.permissions_for(i.guild.me).send_messages and i.permissions_for(i.guild.me).read_messages:
              channels[str(context.guild.id)] = i
              context = i
              changed = True
              break
          print(context.guild.get_channel.name)
          if changed == False and channels[str(context.guild.id)] !="inactive":
            owner = await client.fetch_user(context.guild.owner_id)
            await owner.send("Hi there! It seems I'm not able to send and read messages in any of "+context.guild.name+"'s channels. Please change this or I won't be able to share trivia with your server :)")
            channels[str(context.guild.id)] = "inactive"

        with open("channels.json", "w") as f:
          json.dump(channels, f, indent=2)
      try:
        page = urlopen(url)
      except:
        print("Error opening the URL")

      soup = BeautifulSoup(page, "html.parser")
              
      with open("categories.json", "r") as f:
        categories = json.load(f)

      n=random.choice(categories[str(context.guild.id)])
      strng = str(soup.findAll("td")[n])
      strng = strng[strng.index(">", 17)+1:-9]
      embed=discord.Embed(title="**Question**", description=strng, color=discord.Colour.orange())
      await context.send(embed=embed)
      anser = str(soup.findAll("td")[n+1])[17:-5]

      with open("answers.json", "r") as f:
        answers = json.load(f)

      answers[str(context.guild.id)] = anser.replace("&amp;", "&")

      with open("answers.json", "w") as f:
        json.dump(answers, f, indent=2)

      with open("points.json", "r") as f:
        points = json.load(f)

      points[str(context.guild.id)] = 5

      with open("points.json", "w") as f:
        json.dump(points, f, indent=2)

      with open("hints.json", "r") as f:
        hints = json.load(f)

      hints[str(context.guild.id)] = None

      with open("hints.json", "w") as f:
        json.dump(hints, f, indent=2)

      with open("data.json", "r") as f:
        data = json.load(f)

      data["5questions"] = data["5questions"] + 1

      with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

  await client.process_commands(message)

client.run('''token''')

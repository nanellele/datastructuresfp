import os
import discord
from discord.ext import commands
import requests

token = os.environ['TOKEN']

# Used to store all of the current unadopted dogs
notAdopted = []

# Keep track of all the dogs a user has adopted
adopted = {}
channelID = 1101255593651617826
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix='!')


@bot.event
async def on_ready():
  global channelID
  print("Bot is ready!")
  await bot.get_channel(channelID).send("READY")


# Generate a new picture of a dog with a name every 15 seconds


# Check when a user reacts with the correct emoji and then allow them to adopt the dog
# delete the message
@bot.event
async def on_reaction_add(reaction, user):
  global adopted
  global notAdopted
  if (user == bot.user):
    return
  if reaction.emoji == '👍':
    split = reaction.message.content.replace("\n", " ").split(" ")
    length = len(split)
    name = split[length - 2]
    image = split[length - 1]
    tuple = (name, image)

    # Prevent dogs that have already been adopted by the !adopt command from getting adopted once the message is reacted to, as the message only gets deleted if the user reacts to the message
    if tuple not in notAdopted:
      await bot.get_channel(channelID).send(
        f"Sorry {user.mention}, {name} has already been adopted!")
      await reaction.message.delete()
      return
    notAdopted.remove(tuple)
    if (user.name not in adopted):
      adopted[user.name] = {}
    adopted[user.name][name] = image
    await reaction.message.channel.send(f"{user.mention} has adopted {name}!")
    await reaction.message.delete()


@bot.command()
async def generate(self):
  global channelID
  global notAdopted
  # Two API calls to generate a name and a picture of the dog
  res = requests.get("https://dog.ceo/api/breeds/image/random")
  image = res.json()["message"]
  nameRes = requests.get("https://randomuser.me/api/")
  name = nameRes.json()["results"][0]["name"]["first"]
  message = f"The dog's name is {name}\n{image}"
  sentMsg = await bot.get_channel(channelID).send(message)
  notAdopted.append((name, image))
  print(notAdopted)
  await sentMsg.add_reaction('👍')


# Used to list all of the unadopted dogs - the runtime of this function is O(n)
# n is the length of the names in the notAdopted list
@bot.command()
async def unadopted(self):
  global channelID
  global notAdopted
  if (len(notAdopted) == 0):
    await bot.get_channel(channelID).send("No dogs are unadopted currently!")
  for dog in notAdopted:
    await bot.get_channel(channelID).send(
      f"{dog[0]} has still not been adopted!")


# Find the first name that matches
# This method is O(n) worst case, as the for loop would have to iterate over the entire unadopted dogs list
@bot.command()
async def adopt(ctx, name=""):
  global channelID
  global adopted
  global notAdopted
  user = ctx.author
  # Validate that user has provided a name argument
  if (name == ""):
    await bot.get_channel(channelID).send(
      f"{user.mention}, please provide a name!")
    return

  # Iterate through all of the unadopted dogs to see if the name field matches
  for dog in notAdopted:
    if (dog[0].lower() == name.lower()):
      notAdopted.remove(dog)
      if (user.name not in adopted):
        adopted[user.name] = {}
      adopted[user.name][dog[0]] = dog[1]
      await bot.get_channel(channelID).send(
        f"{user.mention} has adopted {name}!")
      return

  await bot.get_channel(channelID).send(
    f"{user.mention}, there are currently no unadopted dogs with that name!")


# Used to help list all of the dog's that a user has currently adopted
@bot.command()
async def myadoptions(ctx):
  global channelID
  global adopted
  user = ctx.author
  if user.name not in adopted:
    await bot.get_channel(channelID).send(
      f"{user.mention}, you do not have any dogs adopted yet!")
  else:
    userAdoptions = adopted[user.name]
    await bot.get_channel(channelID).send(f"{user.mention}, you have adopted:")
    for name, image in userAdoptions.items():
      await bot.get_channel(channelID).send(f"{name}\n{image}")


bot.run(token)
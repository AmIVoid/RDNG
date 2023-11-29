import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='$', intents=intents)

def generate_string():
    with open('Adjectives.txt', 'r') as adj_file, open('Nouns.txt', 'r') as noun_file:
        adjectives = adj_file.read().splitlines()
        nouns = noun_file.read().splitlines()

    random_number = random.randint(1000, 9999)
    random_adjective = random.choice(adjectives)
    random_noun = random.choice(nouns)
    result = random_adjective.capitalize() + random_noun.capitalize()
    result += str(random_number)

    return result

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="$gen"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg_parts = message.content.split()
    if len(msg_parts) > 0 and msg_parts[0] == '$gen':
        num = 1
        if len(msg_parts) > 1 and msg_parts[1].isdigit():
            num = int(msg_parts[1])

        result = ''
        for _ in range(num):
            result += generate_string() + '\n'

        await message.channel.send(result)

load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
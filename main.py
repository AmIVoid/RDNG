import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='$', intents=intents)
counter_file = 'counter.txt'

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

def read_counter():
    try:
        with open(counter_file, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def update_counter(count):
    with open(counter_file, 'w') as file:
        file.write(str(count))

def save_to_file(text):
    with open('generated_responses.txt', 'a') as file:
        file.write(text + '\n')

def split_messages(message, max_length=2000):
    if len(message) <= max_length:
        return [message]

    messages = []
    current_message = ""
    for line in message.split('\n'):
        if len(current_message) + len(line) + 1 > max_length:
            messages.append(current_message)
            current_message = line
        else:
            current_message += (line + '\n')

    messages.append(current_message)  # Append any remaining text in current_message
    return messages

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    counter = read_counter()
    await client.change_presence(activity=discord.Game(name=f"Generated {counter} names"))

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
            generated_string = generate_string()
            result += generated_string + '\n'
            save_to_file(generated_string)

        counter = read_counter() + num
        update_counter(counter)
        await client.change_presence(activity=discord.Game(name=f"Generated {counter} names"))

        # Split and send message if it's too long
        if len(result) > 2000:
            for part in split_messages(result):
                await message.channel.send(part)
        else:
            await message.channel.send(result)

load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
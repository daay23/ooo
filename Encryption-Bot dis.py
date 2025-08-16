import random
import string
import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()
bot = commands.Bot(command_prefix = '/', intents=discord.Intents.all())

class Encryption:
    encrypted = []
    def __init__(self):
        x = list(string.ascii_letters+string.digits+string.punctuation+" ")
        random.shuffle(x)
        self.encrypter = list(x)
        
encrypted_list = [Encryption]

@bot.event
async def on_ready():
    print(f"We are logged in as {bot.user}")
    
@bot.tree.command(name="encrypt", description="encrypt a message")
@app_commands.describe(message="message to encrypt")
async def encrypt(interaction: discord.Interaction, message: str):
    x = Encryption()
    x.encrypted=list(message)
    for i in range(len(x.encrypted)):
        x.encrypted[i], x.encrypter[i] = x.encrypter[i], x.encrypted[i]
    x.encrypted = "".join(map(str, x.encrypted))
    encrypted_list.append(x)
    await interaction.response.send_message((x.encrypted))
        
@bot.tree.command(name="decrypt", description="decrypt a message")
@app_commands.describe(message="message to decrypt")
async def decrypt(interaction: discord.Interaction, message: str):
    index = -1
    for i in range(len(encrypted_list)):
        if encrypted_list[i].encrypted == message:
            index=i
    if (index == -1):
        await interaction.response.send_message("Decryption not found.")
        return
    inputList = list(message)
    for i in range(len(inputList)):
        inputList[i] = encrypted_list[index].encrypter[i]
    encrypted_list.pop(index)
    await interaction.response.send_message("".join(map(str, inputList)))

@bot.tree.command(name="sync")
async def sync(interaction: discord.Interaction):
    try: 
        await bot.tree.sync()
        await interaction.response.send_message('Command tree synced.')
    except Exception as e:
        print(e)
        
bot.run(os.environ.get("BOT_TOKEN"))


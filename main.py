import discord
import os
from discord import app_commands
from PIL import Image
from discord import File
import glob

token_bot = "ENTER_TOKEN_HERE"


guildID = discord.Object(id=ENTER_HERE_DISCORD_SERVER_ID_WITHOUT_QUOTES)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_console() # Only for live Console 

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
            

@tree.command(
    name="gif",
    description="Convert an image to a gif",
    guild=guildID
)
async def gif_command(interaction, file: discord.Attachment):
    files = glob.glob("./gifs/*")
    for f in files:
        os.remove(f)
    if file.filename.lower().endswith(".png") or file.filename.lower().endswith(".jpg"):
        save_path_raw = os.path.join("images", file.filename.lower())
        await file.save(save_path_raw)
        img = Image.open(save_path_raw)
        if file.filename.lower().endswith(".png"):
            gif_name = file.filename.lower().replace(".png", ".gif")
        else:
            gif_name = file.filename.lower().replace(".jpg", ".gif")
        save_path_gif = os.path.join("gifs", gif_name)
        img.save(save_path_gif, format='GIF')
        os.remove(save_path_raw)
        imgFile = File(save_path_gif)
        await interaction.response.send_message(file=imgFile)
    else:
        await interaction.response.send_message("Please use a .jpg or .png file")

if not os.path.exists("images"):
    os.makedirs("images")
if not os.path.exists("gifs"):
    os.makedirs("gifs")

@client.event
async def on_ready():
    await tree.sync(guild=guildID)
    print('Command Tree synced!')
    print('Ready!')


client.run(token_bot)

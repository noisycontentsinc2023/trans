import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os
import googletrans 
from discord import Embed
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType 

translator = googletrans.Translator()
intents = discord.Intents.default()
intents.members = True

# Create a dictionary of flag emojis and their corresponding language codes
flag_emoji_dict = {
"🇺🇸": "en",
"🇩🇪": "de",
"🇫🇷": "fr",
"🇪🇸": "es",
"🇮🇹": "it",
"🇵🇹": "pt",
"🇷🇺": "ru",
"🇦🇱": "sq",
"🇸🇦": "ar",
"🇧🇦": "bs",
"🇨🇳": "zh-CN",
"🇹🇷": "tr",
"🇵🇱": "pl",
"🇳🇴": "no",
"🇸🇬": "sv",
"🇯🇵": "ja",
"🇰🇷": "ko",
}

TOKEN = os.environ['TOKEN']
PREFIX = os.environ['PREFIX']

intents=discord.Intents.all()
prefix = '!'
bot = commands.Bot(command_prefix=prefix, intents=intents)
translator = googletrans.Translator()

# Create a dictionary of flag emojis and their corresponding language codes
flag_emoji_dict = {
"🇺🇸": "en",
"🇩🇪": "de",
"🇫🇷": "fr",
"🇪🇸": "es",
"🇮🇹": "it",
"🇵🇹": "pt",
"🇷🇺": "ru",
"🇦🇱": "sq",
"🇸🇦": "ar",
"🇧🇦": "bs",
"🇨🇳": "zh-CN",
"🇹🇷": "tr",
"🇵🇱": "pl",
"🇳🇴": "no",
"🇸🇬": "sv",
"🇯🇵": "ja",
"🇰🇷": "ko",
}

#For a more secure, we loaded the .env file and assign the token value to a variable 
load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

#Intents are permissions for the bot that are enabled based on the features necessary to run the bot.
intents=discord.Intents.all()

#Comman prefix is setup here, this is what you have to type to issue a command to the bot
prefix = './'
bot = commands.Bot(command_prefix=prefix, intents=intents)

#------------------------------------------------Events------------------------------------------------------#

@bot.event
async def on_reaction_add(reaction, user):
  
    # Check if the reaction is a flag emoji
    if reaction.emoji in flag_emoji_dict:
        # Get the language code corresponding to the flag emoji
        lang_code = flag_emoji_dict[reaction.emoji]
        # Get the original message
        message = reaction.message
        # Translate the message to the desired language
        detected_lang = translator.detect(message.content)
        translated_message = translator.translate(message.content, dest=lang_code).text
        pronunciation_message =translator.translate(message.content, dest=lang_code).pronunciation

        embed = Embed(title='번역된 문장', description=f'{translated_message}', color=0x00ff00)
        embed.add_field(name="원문", value=message.content, inline=False)
        embed.add_field(name="발음", value=pronunciation_message, inline=False)
       # await reaction.message.channel.send(content=f'{reaction.user.mention}',embed=embed)
        await reaction.message.channel.send(content=f'{user.mention}',embed=embed)
        
#------------------------------------------------말하------------------------------------------------------#

@bot.command()
async def speak(ctx):
    embed = discord.Embed(title="Language roles", description="Click a button to get the role")

    buttons = [
        Button(style=ButtonStyle.blue, label="German"),
        Button(style=ButtonStyle.blue, label="Japanese"),
        Button(style=ButtonStyle.blue, label="English"),
        Button(style=ButtonStyle.blue, label="Chinese"),
        Button(style=ButtonStyle.blue, label="Spanish"),
        Button(style=ButtonStyle.blue, label="French"),
    ]

    await ctx.send(embed=embed, components=[buttons])

@bot.event
async def on_button_click(res):
    member = res.guild.get_member(res.user.id)
    role_id = 1076005878290989097
    role = res.guild.get_role(role_id)
    role_name = res.component.label

    if role in member.roles:
        await member.remove_roles(role)
        action = "removed"
    else:
        await member.add_roles(role)
        action = "added"

    embed = discord.Embed(title=f"{role_name} role {action}", description=f"{res.user.mention} just {action} the {role_name} role")
    await res.respond(type=InteractionType.ChannelMessageWithSource, embed=embed)  
        

#Run the bot
bot.run(TOKEN)

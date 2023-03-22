import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os
import googletrans 
from discord import Embed

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

# Define the embed message with the 6 clickable buttons
embed = discord.Embed(title='Choose a language:', description='Click one of the buttons below to get the role!', color=0x00ff00)
embed.add_field(name='German', value=':flag_de:', inline=True)
embed.add_field(name='Japanese', value=':flag_jp:', inline=True)
embed.add_field(name='English', value=':flag_gb:', inline=True)
embed.add_field(name='Chinese', value=':flag_cn:', inline=True)
embed.add_field(name='Spanish', value=':flag_es:', inline=True)
embed.add_field(name='French', value=':flag_fr:', inline=True)

# Define the role for the language buttons
language_role_id = 1076005878290989097

# Define the click event for each button
@bot.event
async def on_raw_reaction_add(payload):
    # Get the user who clicked the button
    user = await bot.fetch_user(payload.user_id)
    # Check if the reaction is on the embed message and the user is not a bot
    if payload.message_id == embed_msg.id and not user.bot:
        # Give the user the language role
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(language_role_id)
        member = guild.get_member(payload.user_id)
        await member.add_roles(role)
        # Send a message to confirm the role was given
        language = payload.emoji.name
        message = f"You now have the '{language}' role!"
        await bot.get_channel(payload.channel_id).send(message)

# Define the double-click event for each button
@bot.event
async def on_raw_reaction_remove(payload):
    # Check if the reaction is on the embed message
    if payload.message_id == embed_msg.id:
        # Remove the language role from the user
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(language_role_id)
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)
        # Send a message to confirm the role was removed
        language = payload.emoji.name
        message = f"The '{language}' role has been removed."
        await bot.get_channel(payload.channel_id).send(message)        
        

#Run the bot
bot.run(TOKEN)

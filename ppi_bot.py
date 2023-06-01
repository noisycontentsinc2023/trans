import discord
import json
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
"🇻🇳": "vi",
"🇮🇩": "id",
}

TOKEN = os.environ['TOKEN']
PREFIX = os.environ['PREFIX']

intents=discord.Intents.all()
prefix = '!'
bot = commands.Bot(command_prefix=prefix, intents=intents)


#------------------------------------------------번역기------------------------------------------------------#

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
        pronunciation_message = translator.translate(message.content, dest=lang_code).pronunciation

        embed = Embed(title='번역 translate', description=f'{translated_message}', color=0x00ff00)
        embed.add_field(name="원문 original text", value=message.content, inline=False)
        embed.add_field(name="발음 pronunciation", value=pronunciation_message, inline=False)
       # await reaction.message.channel.send(content=f'{reaction.user.mention}',embed=embed)
        await reaction.message.channel.send(content=f'{user.mention}',embed=embed)
    
#------------------------------------------------Events------------------------------------------------------#


@bot.command(name='복제')
async def replicate(ctx, role_id: int):
    role_to_replicate = discord.utils.get(ctx.guild.roles, id=role_id)

    if not role_to_replicate:
        await ctx.send(f"Could not find the role with ID '{role_id}'.")
        return

    new_role = await ctx.guild.create_role(name=f"{role_to_replicate.name} (Replicate)", permissions=role_to_replicate.permissions)

    for member in role_to_replicate.members:
        await member.add_roles(new_role)

    await ctx.send(f"Role '{role_to_replicate.name}' has been replicated, and the new role has been assigned to the members with the original role.")
    
#Run the bot
bot.run(TOKEN)

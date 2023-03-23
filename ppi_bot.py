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

        embed = Embed(title='번역된 문장', description=f'{translated_message}', color=0x00ff00)
        embed.add_field(name="원문", value=message.content, inline=False)
        embed.add_field(name="발음", value=pronunciation_message, inline=False)
       # await reaction.message.channel.send(content=f'{reaction.user.mention}',embed=embed)
        await reaction.message.channel.send(content=f'{user.mention}',embed=embed)



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


class MyButton(discord.ui.Button):
    def __init__(self, label, language):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.language = language
    
    async def callback(self, interaction: discord.Interaction):
        # Get the user who clicked the button
        user = interaction.user
        
        # Get the message that the button was clicked on
        message = interaction.message
        
        # Update the embed message with the selected language
        embed = message.embeds[0]
        embed.set_footer(text=f"Selected language: {self.language}")
        await message.edit(embed=embed)
        
        # Disable the button and remove the user ID if the button is clicked again
        self.disabled = True
        self.style = discord.ButtonStyle.green
        await interaction.response.edit_message(view=None)


@bot.command(name='말하기')
async def speak(ctx):
    # Create the embed message
    embed = discord.Embed(title='Choose a language:', color=discord.Color.blue())
    embed.set_footer(text="Selected language: None")
    
    # Create the buttons and add them to a view
    view = discord.ui.View(timeout=None)  # Persist view after a button is clicked
    languages = ['Chinese', 'Japanese', 'Spanish', 'English', 'German', 'French']
    for lang in languages:
        button = MyButton(lang, lang)
        view.add_item(button)
    
    # Send the message with the embed and the buttons
    message = await ctx.send(embed=embed, view=view)
        

#Run the bot
bot.run(TOKEN)

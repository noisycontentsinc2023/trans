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
intents.typing = False
intents.presences = False

class ButtonClick(discord.ui.Button):
    def __init__(self, label, user_mentions, button_view):
        super().__init__(label=label)
        self.user_mentions = user_mentions
        self.button_view = button_view

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        if user in self.user_mentions:
            self.user_mentions.remove(user)
        else:
            self.user_mentions.append(user)

        embed = discord.Embed(title="말하기 스터디 참여 현황")
        for button in self.button_view.children:
            mentions_str = " ".join([f"{user.mention}" for user in button.user_mentions])
            embed.add_field(name=button.label, value=mentions_str if mentions_str else "No one has clicked yet!", inline=True)
        await interaction.response.edit_message(embed=embed)

@bot.command(name='말하기')
async def speak(ctx):
    user_mentions = []
    button_view = discord.ui.View()

    buttons = [
        ButtonClick("스페인어", user_mentions, button_view),
        ButtonClick("중국어", user_mentions, button_view),
        ButtonClick("일본어", user_mentions, button_view),
        ButtonClick("영어", user_mentions, button_view),
        ButtonClick("프랑스어", user_mentions, button_view),
        ButtonClick("독일어", user_mentions, button_view),
    ]

    for button in buttons:
        button_view.add_item(button)

    embed = discord.Embed(title="말하기 스터디 참여 현황")
    for button in buttons:
        embed.add_field(name=button.label, value="No one has clicked yet!", inline=True)
    await ctx.send(embed=embed, view=button_view)


        
#Run the bot
bot.run(TOKEN)

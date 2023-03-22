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
        
#------------------------------------------------말하------------------------------------------------------#

@bot.command(name='말하기')
async def speak(ctx):
    # Create the embed message
    embed = discord.Embed(title='Choose a language:', color=discord.Color.blue())
    
    # Add the clickable buttons
    buttons = ['Spanish', 'French', 'Chinese', 'Japanese', 'English', 'German']
    components = []
    for button in buttons:
        components.append(
            Button(style=ButtonStyle.gray, label=button, custom_id=button)
        )
    action_row = ActionRow(*components)
    
    # Send the message with the buttons
    message = await ctx.send(embed=embed, components=[action_row])
    
    # Define a callback function to handle button clicks
    async def callback(interaction: Interaction):
        # Get the user who clicked the button
        user = interaction.user
        
        # Get the button that was clicked
        button = interaction.data['custom_id']
        
        # Get the message that the button was clicked on
        message = interaction.message
        
        # Update the embed message with the user who clicked the button
        embed = message.embeds[0]
        embed.add_field(name=button, value=user.mention)
        await message.edit(embed=embed)
        
        # Disable the button and remove the user ID if the button is clicked again
        button_component = [c for c in interaction.message.components[0].components if c.custom_id == button][0]
        if button_component.disabled:
            embed = message.embeds[0]
            for i, field in enumerate(embed.fields):
                if field.name == button:
                    embed.remove_field(i)
                    break
            await message.edit(embed=embed, components=[action_row])
        else:
            button_component.disabled = True
            button_component.style = ButtonStyle.green
            await interaction.response.edit_message(components=[action_row])
    
    # Wait for button clicks and handle them with the callback function
    bot.add_callback(callback)
        

#Run the bot
bot.run(TOKEN)

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

async def load_user_mentions(guild):
    try:
        with open("user_mentions.json", "r") as f:
            user_mentions_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    user_mentions = {}
    for key, user_ids in user_mentions_data.items():
        user_mentions[key] = [await guild.fetch_member(user_id) for user_id in user_ids]
    return user_mentions

def save_user_mentions(user_mentions):
    serializable_user_mentions = {k: [user.id for user in users] for k, users in user_mentions.items()}
    with open("user_mentions.json", "w") as f:
        json.dump(serializable_user_mentions, f)

class CustomView(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=None)
        self.message_id = None

        async def init_user_mentions():
            self.user_mentions = await load_user_mentions(guild)
        
        asyncio.ensure_future(init_user_mentions())

    def add_button(self, button):
        self.add_item(button)
        self.user_mentions[button.custom_id] = []
        
class ButtonClick(discord.ui.Button):
    def __init__(self, label, view):
        super().__init__(label=label, custom_id=label)
        self.parent_view = view

    async def callback(self, interaction: discord.Interaction):
        view = self.parent_view
        view.message_id = interaction.message.id
        user = interaction.user
        user_mentions = view.user_mentions[self.custom_id]
        guild = interaction.guild
        role_id = 1011867929375146054
        role = guild.get_role(role_id)

        if not role:
            await interaction.response.send_message("Role not found. Please check if the role ID is correct.", ephemeral=True)
            return

        if user in user_mentions:
            user_mentions.remove(user)
            await interaction.user.remove_roles(role)
        else:
            user_mentions.append(user)
            await interaction.user.add_roles(role)

        embed = discord.Embed(title="말하기 스터디 참여 현황")
        for button in view.children:
            mentions_str = " ".join([f"{user.mention}" for user in view.user_mentions[button.custom_id]])
            embed.add_field(name=button.label, value=mentions_str if mentions_str else "No one has clicked yet!", inline=True)
        await interaction.response.edit_message(embed=embed)
        
        # Save the updated user_mentions data
        save_user_mentions(view.user_mentions)
        
@bot.command(name='말하기')
async def speak(ctx, message_id: int = None):
    view = CustomView(ctx.guild)
    buttons = [
        ButtonClick("스페인어", view),
        ButtonClick("중국어", view),
        ButtonClick("일본어", view),
        ButtonClick("영어", view),
        ButtonClick("프랑스어", view),
        ButtonClick("독일어", view),
    ]

    for button in buttons:
        view.add_button(button)

    view.user_mentions = await load_user_mentions(ctx.guild.id)

    embed = discord.Embed(title="말하기 스터디 참여 현황")
    for button in buttons:
        embed.add_field(name=button.label, value="아직 아무도 신청하지 않았어요 :(", inline=True)
    await ctx.send(embed=embed, view=view)
    
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

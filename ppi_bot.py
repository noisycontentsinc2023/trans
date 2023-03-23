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

def load_user_mentions():
    try:
        with open("user_mentions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_mentions(user_mentions):
    with open("user_mentions.json", "w") as f:
        json.dump(user_mentions, f)

class CustomView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.user_mentions = load_user_mentions()
        self.message_id = None

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
    view = CustomView()
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

    embed = discord.Embed(title="말하기 스터디 참여 현황")
    for button in buttons:
        embed.add_field(name=button.label, value="No one has clicked yet!", inline=True)
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


@bot.command()
async def image(ctx):
    message = ctx.message
    Text = ""
    learn = message.content.split(" ")
    vrsize = len(learn)  # array size
    vrsize = int(vrsize)
    for i in range(1, vrsize):  # Recognize text with spaces
        Text = Text + " " + learn[i]
    print(Text.strip())  # command entered

    randomNum = random.randrange(0, 40)  # random image number

    location = Text
    enc_location = urllib.parse.quote(location)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query=' + enc_location
    print(url)
    req = Request(url, headers=hdr)
    html = urllib.request.urlopen(req)
    bsObj = bs4.BeautifulSoup(html, "html.parser")
    imgfind1 = bsObj.find('div', {'class': 'photo_grid _box'})
    imgfind2 = imgfind1.findAll('a', {'class': 'thumb _thumb'})
    imgfind3 = imgfind2[randomNum]
    imgfind4 = imgfind3.find('img')
    imgsrc = imgfind4.get('data-source')
    print(imgsrc)
    embed = discord.Embed(
        color=discord.Colour.green()
    )
    embed.set_image(url=imgsrc)
    await ctx.send(embed=embed)
    
#Run the bot
bot.run(TOKEN)

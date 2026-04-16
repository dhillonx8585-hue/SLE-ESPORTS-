import discord
from discord import ui, app_commands
from discord.ext import commands
import datetime

# --- नया टोकन यहाँ डाल दिया है ---
TOKEN = "MTQ5Mzk2Mjk1MjM3NjcxNzM1Mw.GNDFVf.roQoI4jBiJZut6rTYL369lukGMjvdTG-lYlm5Y"

class MasterBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="s", intents=intents, help_command=None)

    async def setup_hook(self):
        print("🔄 Syncing commands...")
        await self.tree.sync()
        print("✅ Commands Synced Successfully!")

bot = MasterBot()

# --- REGISTRATION MODAL (Registration Form) ---
class RegModal(ui.Modal, title='🎮 T3 REGISTRATION FORM'):
    team = ui.TextInput(label='Team Name', placeholder='Team Name लिखें...', required=True)
    p1 = ui.TextInput(label='Player 1 (IGN | UID)', required=True)
    p2 = ui.TextInput(label='Player 2 (IGN | UID)', required=True)
    p3 = ui.TextInput(label='Player 3 (IGN | UID)', required=True)
    p4 = ui.TextInput(label='Player 4 (IGN | UID)', required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"✅ {self.team.value}, स्लॉट बुक हो गया!", ephemeral=True)

class RegView(ui.View):
    def __init__(self): super().__init__(timeout=None)
    @ui.button(label="📝 Register Now", style=discord.ButtonStyle.green, custom_id="reg_btn")
    async def reg_callback(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(RegModal())

# --- EVENTS ---
@bot.event
async def on_ready():
    print(f'🚀 {bot.user} IS ONLINE!')

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.content.lower() == 'shelp':
        embed = discord.Embed(title="🏆 T3 MASTER MENU", color=0xff0000)
        embed.add_field(name="Commands", value="`/setup` - Reg Panel\n`/idp` - Send IDP\n`/clear` - Chat Clean", inline=False)
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

# --- SLASH COMMANDS ---
@bot.tree.command(name="setup", description="रजिस्ट्रेशन पैनल भेजें")
async def setup(interaction: discord.Interaction):
    embed = discord.Embed(title="🎮 T3 SCREAMS SLE", description="नीचे बटन दबाकर रजिस्टर करें", color=0x00ff00)
    await interaction.response.send_message(embed=embed, view=RegView())

@bot.tree.command(name="idp", description="ID पासवर्ड भेजें")
async def idp(interaction: discord.Interaction, info: str):
    embed = discord.Embed(title="🔐 IDP ARRIVED", description=f"```{info}```", color=0xffff00)
    await interaction.channel.send("@everyone", embed=embed)
    await interaction.response.send_message("IDP Sent!", ephemeral=True)

bot.run(TOKEN)


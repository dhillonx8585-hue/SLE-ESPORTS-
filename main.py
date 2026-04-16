import discord
from discord import ui, app_commands
from discord.ext import commands
import datetime

# --- BOT SETUP ---
TOKEN = "MTQ5Mzk2Mjk1MjM3NjcxNzM1Mw.GI_v-B.xP0xxK8m3fI5D64BVz3LX8mFUMC5kZs-fm6YCI"

class MasterBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="s", intents=intents, help_command=None)

    async def setup_hook(self):
        print("🔄 Commands Sync कर रहा हूँ...")
        await self.tree.sync()
        print("✅ सब कुछ सिंक हो गया!")

bot = MasterBot()

# --- REGISTRATION MODAL (वो फॉर्म जो तूने बोला था) ---
class RegModal(ui.Modal, title='🎮 T3 REGISTRATION FORM'):
    team = ui.TextInput(label='Team Name', placeholder='यहाँ टीम का नाम लिखें', required=True)
    p1 = ui.TextInput(label='Player 1 (IGN | UID)', required=True)
    p2 = ui.TextInput(label='Player 2 (IGN | UID)', required=True)
    p3 = ui.TextInput(label='Player 3 (IGN | UID)', required=True)
    p4 = ui.TextInput(label='Player 4 (IGN | UID)', required=True)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="✅ Registration Successful", color=discord.Color.green())
        embed.add_field(name="Team", value=self.team.value, inline=False)
        embed.add_field(name="Lineup", value=f"1. {self.p1}\n2. {self.p2}\n3. {self.p3}\n4. {self.p4}")
        await interaction.response.send_message(f"✅ {self.team.value}, आपका स्लॉट बुक हो गया!", ephemeral=True)

class RegView(ui.View):
    def __init__(self): super().__init__(timeout=None)
    @ui.button(label="📝 Register Now", style=discord.ButtonStyle.green, custom_id="reg_btn")
    async def reg_btn(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(RegModal())

# --- EVENTS ---
@bot.event
async def on_ready():
    print(f'🔥 {bot.user} Online है और तैयार है!')

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.content.lower() == 'shelp':
        embed = discord.Embed(title="🏆 T3 MASTER MENU", color=0xff0000)
        embed.add_field(name="Commands", value="`/setup` - Reg Panel\n`/idp` - Send IDP\n`/clear` - Chat Clean", inline=False)
        await message.channel.send(embed=embed)

# --- SLASH COMMANDS (Features) ---
@bot.tree.command(name="setup", description="रजिस्ट्रेशन पैनल भेजें")
async def setup(interaction: discord.Interaction):
    embed = discord.Embed(title="🎮 T3 SCREAMS SLE", description="रजिस्टर करने के लिए नीचे बटन दबाएं", color=0x00ff00)
    await interaction.response.send_message(embed=embed, view=RegView())

@bot.tree.command(name="idp", description="ID पासवर्ड भेजें")
async def idp(interaction: discord.Interaction, info: str):
    embed = discord.Embed(title="🔐 IDP ARRIVED", description=f"```{info}```", color=0xffff00)
    await interaction.channel.send("@everyone", embed=embed)
    await interaction.response.send_message("IDP भेज दिया गया!", ephemeral=True)

@bot.tree.command(name="clear", description="चैट साफ़ करें")
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"🧹 {amount} मैसेज साफ़!", ephemeral=True)

bot.run(TOKEN)


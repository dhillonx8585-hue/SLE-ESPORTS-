import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio

# --- बोट को 24/7 जगाए रखने के लिए Web Server ---
app = Flask('')
@app.route('/')
def home():
    return "SLE BOT IS ONLINE"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- बोट सेटअप ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ आपका टोकन यहाँ डाल दिया गया है
TOKEN = "MTQ4ODE2NTkyODE2MzIxNzQyOQ.Gw2owN.GkulN3Lf5zSkbESwKBhfSUTkDXxvoePN2hDjcQ" 

@bot.event
async def on_ready():
    print(f'{bot.user} ऑनलाइन है और SLE ESPORTS के लिए तैयार है!')

@bot.command()
async def register(ctx):
    # ⚠️ यहाँ अपने उस चैनल की ID डालें जहाँ आप रजिस्ट्रेशन डेटा देखना चाहते हैं
    # अभी मैंने 000... रखा है, इसे बदल लेना
    ADMIN_CHANNEL_ID = 123456789012345678 
    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # स्टेप-बाय-स्टेप सवाल पूछना
        await ctx.send("📝 **SLE ESPORTS - रजिस्ट्रेशन फॉर्म**\n\n1️⃣ **अपनी टीम का नाम लिखें:**")
        team_name = await bot.wait_for('message', check=check, timeout=180.0)

        await ctx.send("2️⃣ **प्लेयर 1 का नाम और ID लिखें:**")
        p1 = await bot.wait_for('message', check=check, timeout=180.0)

        await ctx.send("3️⃣ **प्लेयर 2 का नाम और ID लिखें:**")
        p2 = await bot.wait_for('message', check=check, timeout=180.0)

        await ctx.send("4️⃣ **प्लेयर 3 का नाम और ID लिखें:**")
        p3 = await bot.wait_for('message', check=check, timeout=180.0)

        await ctx.send("5️⃣ **प्लेयर 4 का नाम और ID लिखें:**")
        p4 = await bot.wait_for('message', check=check, timeout=180.0)

        await ctx.send("6️⃣ **टीम ओनर (Owner) का नाम लिखें:**")
        owner_name = await bot.wait_for('message', check=check, timeout=180.0)

        # एडमिन के लिए प्रोफेशनल कार्ड (Embed)
        embed = discord.Embed(title="🚀 New Registration: SLE ESPORTS", color=0xff0000)
        embed.add_field(name="🏆 Team Name", value=team_name.content, inline=False)
        embed.add_field(name="👤 Owner Name", value=owner_name.content, inline=False)
        embed.add_field(name="🎮 Player 1", value=p1.content, inline=True)
        embed.add_field(name="🎮 Player 2", value=p2.content, inline=True)
        embed.add_field(name="🎮 Player 3", value=p3.content, inline=True)
        embed.add_field(name="🎮 Player 4", value=p4.content, inline=True)
        embed.set_footer(text=f"By: {ctx.author}")

        if admin_channel:
            await admin_channel.send(embed=embed)
            await ctx.send(f"✅ **{team_name.content}**, आपका रजिस्ट्रेशन फॉर्म एडमिन को भेज दिया गया है!")
        else:
            # अगर एडमिन चैनल ID नहीं मिली, तो वहीं भेज देगा
            await ctx.send(embed=embed)
            await ctx.send("✅ रजिस्ट्रेशन सफल! (नोट: एडमिन चैनल ID सही नहीं थी, इसलिए यहाँ भेजा गया)")

    except asyncio.TimeoutError:
        await ctx.send("❌ समय समाप्त! आपने जवाब देने में बहुत देर कर दी। फिर से `!register` लिखें।")

keep_alive()
bot.run(TOKEN)

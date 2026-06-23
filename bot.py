import os
import discord
from discord.ext import commands
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# 1. Configuring Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# 2. Creating Bot Instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'======================================')
    print(f'Success! {bot.user.name} is now online.')
    print(f'Listening with the correct Channel IDs!')
    print(f'======================================')

# 3. Welcome Event (👥-users)
@bot.event
async def on_member_join(member):
    WELCOME_CHANNEL_ID = 1518949506656505876  
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    
    if channel:
        print(f"[INFO] Sending welcome embed to 👥-users channel...")
        real_member_count = len(member.guild.members)
        embed = discord.Embed(
            title="🎉 Welcome to StreamVault! 🎉",
            description=f"Hey {member.mention}, welcome to our community!\nWe are absolutely thrilled to have you here.",
            color=discord.Color.from_rgb(114, 137, 218)
        )
        if member.display_avatar:
            embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"You are our {real_member_count}th member! • Enjoy your stay ✨")
        await channel.send(embed=embed)

# 4. Leave Event (🧱-members-left)
@bot.event
async def on_member_remove(member):
    LEAVE_CHANNEL_ID = 1518949510687232073  
    channel = bot.get_channel(LEAVE_CHANNEL_ID)
    
    if channel:
        print(f"[INFO] Sending goodbye embed to 🧱-members-left channel...")
        remaining_members = len(member.guild.members)
        embed = discord.Embed(
            title="👋 Goodbye Member! 👋",
            description=f"**{member.name}** just left the server.\nWe are sad to see you go!",
            color=discord.Color.red()
        )
        if member.display_avatar:
            embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"We now have {remaining_members} members remaining.")
        await channel.send(embed=embed)

# 5. TEST COMMANDS
@bot.command()
async def testjoin(ctx): await on_member_join(ctx.author)
@bot.command()
async def testleave(ctx): await on_member_remove(ctx.author)

# ==================== WEB SERVER FOR UPTIMEROBOT ====================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is active and running 24/7!")

def run_health_server():
    # Render default port 10000 use karta hai web services ke liye
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Background thread mein web server run karna taaki discord bot block na ho
threading.Thread(target=run_health_server, daemon=True).start()
# =====================================================================

# 6. Securely run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
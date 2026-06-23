import os
import asyncio
import discord
from discord.ext import commands
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# 1. Configuring Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'======================================')
    print(f'Success! {bot.user.name} is now online on Vercel.')
    print(f'======================================')

# Welcome Event
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1518949506656505876)
    if channel:
        real_member_count = len(member.guild.members)
        embed = discord.Embed(
            title="🎉 Welcome to StreamVault! 🎉",
            description=f"Hey {member.mention}, welcome to our community!",
            color=discord.Color.from_rgb(114, 137, 218)
        )
        embed.set_footer(text=f"You are our {real_member_count}th member! • ✨")
        await channel.send(embed=embed)

# Leave Event
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1518949510687232073)
    if channel:
        remaining_members = len(member.guild.members)
        embed = discord.Embed(
            title="👋 Goodbye Member! 👋",
            description=f"**{member.name}** just left the server.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"We now have {remaining_members} members remaining.")
        await channel.send(embed=embed)

# 2. Fake Web Server for Vercel (Timeout se bachne ke liye)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_server():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

# Background thread mein server chalana
threading.Thread(target=run_health_server, daemon=True).start()

# 3. Running Bot Securely
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
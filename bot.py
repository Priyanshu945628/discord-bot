import os
import discord
from discord.ext import commands

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

# 3. Welcome Event (users)
@bot.event
async def on_member_join(member):
    WELCOME_CHANNEL_ID = 1518949506656505876

    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    if channel:
        print(f"[INFO] Sending welcome embed to users channel...")
        real_member_count = len(member.guild.members)

        embed = discord.Embed(
            title="🎉 Welcome to StreamVault! 🎉",
            description=f"Hey {member.mention}, welcome to our community!\nWe are absolutely thrilled to have you here.",
            color=discord.Color.from_rgb(114, 137, 218)
        )

        if member.display_avatar:
            embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="📜 Quick Reminder",
            value="Please take a moment to look around and check out our server channels.",
            inline=False
        )
        embed.set_footer(text=f"You are our {real_member_count}th member! • Enjoy your stay ✨")
        await channel.send(embed=embed)
    else:
        print("[ERROR] Welcome Channel ID is invalid or bot cannot see it!")

# 4. Leave Event (members-left)
@bot.event
async def on_member_remove(member):
    LEAVE_CHANNEL_ID = 1518949510687232073

    channel = bot.get_channel(LEAVE_CHANNEL_ID)

    if channel:
        print(f"[INFO] Sending goodbye embed to members-left channel...")
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
    else:
        print("[ERROR] Leave Channel ID is invalid or bot cannot see it!")

# 5. TEST COMMANDS
@bot.command()
async def testjoin(ctx):
    await on_member_join(ctx.author)

@bot.command()
async def testleave(ctx):
    await on_member_remove(ctx.author)

# 6. Securely load token from environment variables
bot.run(os.getenv('DISCORD_TOKEN'))
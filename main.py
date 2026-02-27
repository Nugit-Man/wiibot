import backend
import discord #upm package(py-cord)
from discord.ext import commands #upm package(py-cord)

bot = commands.Bot(command_prefix="w!", intents=discord.Intents.all())

class ChangelogButton(discord.ui.View):
    @discord.ui.button(label="Get a list of previous versions here!", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        try:
            await interaction.user.send("# WiiBot v0.1 - 02/25/2026\n- Introduced three new commands: `/help`, `/ping`, and `/changelog`\n\n# WiiBot v0.0 - 02/23/2026\n- I was born today! Isn't that cool?")
            await interaction.response.send_message("DMed you a list of all previous versions!",ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Something went wrong trying to send you a DM. Have you enabled DMs from this server?",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("An error occurred. Please try again.",ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("v0.1"))
    print("welcome to the wii zone")

'''
@bot.slash_command(description="test", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def test(ctx):
    await ctx.send_response("test")
'''
    
@bot.slash_command(name="help", description="Get a list of Wiibot's commands", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def commands(ctx):
    await ctx.send_response(embed = discord.Embed(description="# WiiBot Commands\n- `/help` - Gives a list of commands WiiBot can run\n- `/ping` - Tests WiiBot's latency\n- `/changelog` - Gets a summary of the newest WiiBot version",colour=0x4ebcff))
    
@bot.slash_command(description="Test WiiBot's latency", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def ping(ctx):
    await ctx.send_response("Pong! ({0}ms)".format(round(bot.latency * 1000, 3)))
    
@bot.slash_command(description="Get a summary of WiiBot's newest update, or look at old WiiBot versions", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def changelog(ctx):
    await ctx.send_response(embed = discord.Embed(description="# WiiBot v0.1 - 02/25/2026\n- Introduced three new commands: `/help`, `/ping`, and `/changelog`",colour=0xf4f4f4),view=ChangelogButton())
    



fin = open(".env","r")
TOKEN = fin.readline().strip()
fin.close()
bot.run(TOKEN)
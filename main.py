import backend
import discord #upm package(py-cord)
from discord.ext import commands #upm package(py-cord)

errorMessage = "This is an admin-only command!"

bot = commands.Bot(command_prefix="w!", intents=discord.Intents.all())

admin = bot.create_group(name="admin", description="admin commands", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})

class ChangelogButton(discord.ui.View):
    @discord.ui.button(label="Get a list of previous versions here!", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        try:
            await interaction.user.send("# WiiBot v0.3 - 03/24/2026\n- Ranked functionality has been added\n- Added four new admin-only commands: `/admin register`, `/admin startranked`, `/admin endranked`, and `/admin gamelog`\n- Backend bugfixes\n\n# WiiBot v0.2 - 03/18/2026\n- Completed backend\n- Finished two commands: `/register`, and `/joingame`\n- Backend bugfixes\n\n# WiiBot v0.1 - 02/25/2026\n- Introduced three new commands: `/help`, `/ping`, and `/changelog`\n\n# WiiBot v0.0 - 02/23/2026\n- I was born today! Isn't that cool?")
            await interaction.response.send_message("DMed you a list of all previous versions!",ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Something went wrong trying to send you a DM. Have you enabled DMs from this server?",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("An error occurred. Please try again.",ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("v0.3"))
    print("welcome to the wii zone")

'''
@bot.slash_command(description="test", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def test(ctx):
    await ctx.send_response("test")
'''
    
@bot.slash_command(name="help", description="Get a list of Wiibot's commands", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def commands(ctx):
    await ctx.send_response(embed = discord.Embed(description="# WiiBot Commands\n- `/help` - Gives a list of commands WiiBot can run\n- `/ping` - Tests WiiBot's latency\n- `/changelog` - Gets a summary of the newest WiiBot version\n- `/register` - Registers you into the bot for ranked matches\n- `/joingame` - Enters you into the ranked group for a specific game",colour=0x4ebcff))
   
@bot.slash_command(description="Test WiiBot's latency", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def ping(ctx):
    await ctx.send_response("Pong! ({0}ms)".format(round(bot.latency * 1000, 3)))
    
@bot.slash_command(description="Get a summary of WiiBot's newest update, or look at old WiiBot versions", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def changelog(ctx):
    await ctx.send_response(embed = discord.Embed(description="# WiiBot v0.3 - 03/24/2026\n- Ranked functionality has been added\n- Added four new admin-only commands: `/admin register`, `/admin startranked`, `/admin endranked`, and `/admin gamelog`\n- Backend bugfixes",colour=0xf4f4f4),view=ChangelogButton())

@bot.slash_command(description="Register with the bot", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def register(ctx, name:str):
    registration = backend.register(ctx.author.id,name)
    if registration == 0:
        await ctx.send_response("You have been successfully registered!")
    elif registration == 1:
        await ctx.send_response("You are already registered!", ephemeral=True)

@bot.slash_command(description="Join a ranked game", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def joingame(ctx, game:discord.Option(choices=["Mario Kart Wii","Eat Fat Fight","Super Smash Bros. Brawl","Wii Sports Resort Swordfighting","Wii Sports Boxing","Mario Super Sluggers"])):
    if game == "Mario Kart Wii":
        gameid = 1
    elif game == "Eat Fat Fight":
        gameid = 2
    elif game == "Super Smash Bros. Brawl":
        gameid = 3
    elif game == "Wii Sports Resort Swordfighting":
        gameid = 4
    elif game == "Wii Sports Boxing":
        gameid = 5
    elif game == "Mario Super Sluggers":
        gameid = 6
    else:
        await ctx.send_response("Something went wrong trying to fetch the game ID.", ephemeral=True)

    name = backend.get_name(ctx.author.id)
    registration = backend.unrated(ctx.author.id,name,gameid)
    if registration == 0:
        await ctx.send_response("You have successfully joined " + game + " with a skill rating of 1500!")
    elif registration == 1:
        await ctx.send_response("You are not registered with the bot yet! Please register using `/register` first.")
    elif registration == 2:
        await ctx.send_response("You have already joined that game!", ephemeral=True)

@admin.command(name="help", description="Get a list of Wiibot's commands", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def commands(ctx):
    if backend.is_admin(ctx.author.id):
        await ctx.send_response(embed = discord.Embed(description="# WiiBot Admin Commands\n- `/admin help` - Gives a list of admin commands WiiBot can run\n- `/admin register` - Registers a new admin to use the admin commands\n- `/admin startranked` - Opens the ranked period\n- `/admin endranked` - Closes the ranked period and calculates ratings\n- `/admin gamelog` - Logs a game during the ranked period",colour=0x4ebcff))
    else:
        await ctx.send_response(errorMessage, ephemeral=True)

@admin.command(description="Register a user as an admin", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def register(ctx, user:discord.User):
    if backend.is_admin(ctx.author.id):
        registration = backend.add_admin(user.id)
        if registration == 0:
            await ctx.send_response(user.name + " has been added as an admin!")
        elif registration == 1:
            await ctx.send_response("This user is already an admin!", ephemeral=True)
    else:
        await ctx.send_response(errorMessage, ephemeral=True)

@admin.command(description="Begin a new ranked period", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def startranked(ctx):
    if backend.is_admin(ctx.author.id):
        check = backend.new_day()
        if check == 0:
            await ctx.send_response("A new ranked period has begun!")
        else:
            await ctx.send_response("Something went wrong.", ephemeral=True)
    else:
        await ctx.send_response(errorMessage, ephemeral=True)

@admin.command(description="End the ranked period", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def endranked(ctx):
    if backend.is_admin(ctx.author.id):
        check = backend.end_day()
        if check == 0:
            await ctx.send_response("The ranked period has ended! Everyone's ratings have been updated.")
        else:
            await ctx.send_response("Something went wrong.", ephemeral=True)
    else:
        await ctx.send_response(errorMessage, ephemeral=True)

@admin.command(description="End the ranked period", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def gamelog(ctx, game:discord.Option(choices=["Mario Kart Wii","Eat Fat Fight","Super Smash Bros. Brawl","Wii Sports Resort Swordfighting","Wii Sports Boxing","Mario Super Sluggers"]), winner:discord.User, loser:discord.User, tie:discord.Option(choices=["Yes","No"])):
    if backend.is_admin(ctx.author.id):
        if game == "Mario Kart Wii":
            gameid = 1
        elif game == "Eat Fat Fight":
            gameid = 2
        elif game == "Super Smash Bros. Brawl":
            gameid = 3
        elif game == "Wii Sports Resort Swordfighting":
            gameid = 4
        elif game == "Wii Sports Boxing":
            gameid = 5
        elif game == "Mario Super Sluggers":
            gameid = 6
        else:
            await ctx.send_response("Something went wrong trying to fetch the game ID.", ephemeral=True)

        winnerid = winner.id
        loserid = loser.id
        check = backend.add_game(gameid,winnerid,loserid,tie)
        if check == 0:
            if tie == "Yes":
                await ctx.send_response("Ranked game has been successfully logged!\n\nThe game ended in a tie.\nPlayers: <@" + str(winnerid) + ">, <@" + str(loserid) + ">")
            else:
                await ctx.send_response("Ranked game has been successfully logged!\n\n<@" + str(winnerid) + "> won the match.\nPlayers: <@" + str(winnerid) + ">, <@" + str(loserid) + ">")
        else:
            await ctx.send_response("Something went wrong.", ephemeral=True)

    else:
        await ctx.send_response(errorMessage, ephemeral=True)

fin = open(".env","r")
TOKEN = fin.readline().strip()
fin.close()
bot.run(TOKEN)
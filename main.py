import backend
import discord #upm package(py-cord)
from discord.ext import commands #upm package(py-cord)
import datetime

# FOR ADDING NEW RANKED GAMES, UPDATE ALL CODE WITH THE TAG "ADDHERE"

errorMessage = "This is an admin-only command!"

bot = commands.Bot(command_prefix="w!", intents=discord.Intents.all())

admin = bot.create_group(name="admin", description="admin commands", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})

class ChangelogButton(discord.ui.View):
    @discord.ui.button(label="Get a list of previous versions here!", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        try:
            await interaction.user.send("# WiiBot v0.3.1 - 03/24/2026\n- Added which game was played to the `/admin gamelog` output\n- Fixed the `/admin gamelog` command description\n\n# WiiBot v0.3 - 03/24/2026\n- Ranked functionality has been added\n- Added four new admin-only commands: `/admin register`, `/admin startranked`, `/admin endranked`, and `/admin gamelog`\n- Backend bugfixes\n\n# WiiBot v0.2 - 03/18/2026\n- Completed backend\n- Finished two commands: `/register`, and `/joingame`\n- Backend bugfixes\n\n# WiiBot v0.1 - 02/25/2026\n- Introduced three new commands: `/help`, `/ping`, and `/changelog`\n\n# WiiBot v0.0 - 02/23/2026\n- I was born today! Isn't that cool?")
            await interaction.response.send_message("DMed you a list of all previous versions!",ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Something went wrong trying to send you a DM. Have you enabled DMs from this server?",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("An error occurred. Please try again.",ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("v1.0 (WIP)"))
    print("welcome to the wii zone")

'''
@bot.slash_command(description="test", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def test(ctx):
    await ctx.send_response("test")
'''
    
@bot.slash_command(name="help", description="Get a list of Wiibot's commands", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def commands(ctx):
    await ctx.send_response(embed = discord.Embed(description="# WiiBot Commands\n- `/help` - Gives a list of commands WiiBot can run\n- `/ping` - Tests WiiBot's latency\n- `/changelog` - Gets a summary of the newest WiiBot version\n- `/register` - Registers you into the bot for ranked matches\n- `/joingame` - Enters you into the ranked group for a specific game\n- `/profile` - Gets the rankings of you or another person (COMING SOON)\n- `/leaderboard` - Shows the top standings in a specific ranked game (COMING SOON)",colour=0x4ebcff))
   
@bot.slash_command(description="Test WiiBot's latency", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def ping(ctx):
    await ctx.send_response("Pong! ({0}ms)".format(round(bot.latency * 1000, 3)))
    
@bot.slash_command(description="Get a summary of WiiBot's newest update, or look at old WiiBot versions", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def changelog(ctx):
    await ctx.send_response(embed = discord.Embed(description="# WiiBot v1.0 - XX/XX/XXXX\n- The first official release!\n- Added `/profile` and `/leaderboard`\n- Changed `/admin gamelog` output to an embed\n- Removed unused name feature\n- Backend bugfixes",colour=0xf4f4f4),view=ChangelogButton())

@bot.slash_command(description="Register with the bot", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def register(ctx):
    registration = backend.register(ctx.author.id)
    if registration == 0:
        await ctx.send_response("You have been successfully registered!")
    elif registration == 1:
        await ctx.send_response("You are already registered!", ephemeral=True)

@bot.slash_command(description="Join a ranked game", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def joingame(ctx, game:discord.Option(choices=["Mario Kart Wii","Eat Fat Fight","Super Smash Bros. Brawl","Wii Sports Resort Swordfighting","Wii Sports Boxing","Mario Super Sluggers"])): # ADDHERE
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
    # ADDHERE
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

@admin.command(description="Add a ranked game", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def gamelog(ctx, game:discord.Option(choices=["Mario Kart Wii","Eat Fat Fight","Super Smash Bros. Brawl","Wii Sports Resort Swordfighting","Wii Sports Boxing","Mario Super Sluggers"]), winner:discord.User, loser:discord.User, tie:discord.Option(choices=["Yes","No"])): # ADDHERE
    if backend.is_admin(ctx.author.id):
        if game == "Mario Kart Wii":
            gameid = 1
            gameicon = "https://files.catbox.moe/bqtkc8.png"
        elif game == "Eat Fat Fight":
            gameid = 2
            gameicon = "https://files.catbox.moe/j1qmri.png"
        elif game == "Super Smash Bros. Brawl":
            gameid = 3
            gameicon = "https://files.catbox.moe/6zwuul.png"
        elif game == "Wii Sports Resort Swordfighting":
            gameid = 4
            gameicon = "https://files.catbox.moe/ndwd9e.png"
        elif game == "Wii Sports Boxing":
            gameid = 5
            gameicon = "https://files.catbox.moe/rcsgnq.png"
        elif game == "Mario Super Sluggers":
            gameid = 6
            gameicon = "https://files.catbox.moe/cce7gw.png"
        # ADDHERE
        else:
            await ctx.send_response("Something went wrong trying to fetch the game ID.", ephemeral=True)

        winnerid = winner.id
        loserid = loser.id
        check = backend.add_game(gameid,winnerid,loserid,tie)
        if check == 0:
            if tie == "Yes":
                embed = discord.Embed(title="Ranked game has been successfully logged!",description="The game ended in a tie.\nPlayers: <@" + str(winnerid) + ">, <@" + str(loserid) + ">",timestamp=datetime.datetime.now())
                embed.set_author(name=game, icon_url=gameicon)
                await ctx.send_response(embed=embed)
            else:
                embed = discord.Embed(title="Ranked game has been successfully logged!",description="<@" + str(winnerid) + "> won the match.\nPlayers: <@" + str(winnerid) + ">, <@" + str(loserid) + ">",timestamp=datetime.datetime.now())
                embed.set_author(name=game, icon_url=gameicon)
                await ctx.send_response(embed=embed)
        else:
            await ctx.send_response("Something went wrong.", ephemeral=True)
    else:
        await ctx.send_response(errorMessage, ephemeral=True)

@bot.slash_command(description="See the profile of you or someone else", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def profile(ctx, user:discord.Option(discord.User,default=None)):
    if user == None:
        user = ctx.author
    
    game1 = backend.get_rating(user.id,1)
    game2 = backend.get_rating(user.id,2)
    game3 = backend.get_rating(user.id,3)
    game4 = backend.get_rating(user.id,4)
    game5 = backend.get_rating(user.id,5)
    game6 = backend.get_rating(user.id,6)
    # ADDHERE
    
    if game1 == "-1":
        game1 = "N/A"
    if game2 == "-1":
        game2 = "N/A"
    if game3 == "-1":
        game3 = "N/A"
    if game4 == "-1":
        game4 = "N/A"
    if game5 == "-1":
        game5 = "N/A"
    if game6 == "-1":
        game6 = "N/A"
    # ADDHERE

    if game1 != "N/A":
        rank1 = str(backend.get_rank_leaderboard(1,user.id))
        outof1 = str(backend.get_players(1))
    else:
        rank1 = "X"
        outof1 = str(backend.get_players(1))
    if game2 != "N/A":
        rank2 = str(backend.get_rank_leaderboard(2,user.id))
        outof2 = str(backend.get_players(2))
    else:
        rank2 = "X"
        outof2 = str(backend.get_players(2))
    if game3 != "N/A":
        rank3 = str(backend.get_rank_leaderboard(3,user.id))
        outof3 = str(backend.get_players(3))
    else:
        rank3 = "X"
        outof3 = str(backend.get_players(3))
    if game4 != "N/A":
        rank4 = str(backend.get_rank_leaderboard(4,user.id))
        outof4 = str(backend.get_players(4))
    else:
        rank4 = "X"
        outof4 = str(backend.get_players(4))
    if game5 != "N/A":
        rank5 = str(backend.get_rank_leaderboard(5,user.id))
        outof5 = str(backend.get_players(5))
    else:
        rank5 = "X"
        outof5 = str(backend.get_players(5))
    if game6 != "N/A":
        rank6 = str(backend.get_rank_leaderboard(6,user.id))
        outof6 = str(backend.get_players(6))
    else:
        rank6 = "X"
        outof6 = str(backend.get_players(6))
    # ADDHERE

    if rank1 == "1":
        trophy1 = "🥇"
    elif rank1 == "2":
        trophy1 = "🥈"
    elif rank1 == "3":
        trophy1 = "🥉"
    else:
        trophy1 = ""
    if rank2 == "1":
        trophy2 = "🥇"
    elif rank2 == "2":
        trophy2 = "🥈"
    elif rank2 == "3":
        trophy2 = "🥉"
    else:
        trophy2 = ""
    if rank3 == "1":
        trophy3 = "🥇"
    elif rank3 == "2":
        trophy3 = "🥈"
    elif rank3 == "3":
        trophy3 = "🥉"
    else:
        trophy3 = ""
    if rank4 == "1":
        trophy4 = "🥇"
    elif rank4 == "2":
        trophy4 = "🥈"
    elif rank4 == "3":
        trophy4 = "🥉"
    else:
        trophy4 = ""
    if rank5 == "1":
        trophy5 = "🥇"
    elif rank5 == "2":
        trophy5 = "🥈"
    elif rank5 == "3":
        trophy5 = "🥉"
    else:
        trophy5 = ""
    if rank6 == "1":
        trophy6 = "🥇"
    elif rank6 == "2":
        trophy6 = "🥈"
    elif rank6 == "3":
        trophy6 = "🥉"
    else:
        trophy6 = ""
    # ADDHERE

    embed = discord.Embed(description="## <@" + str(user.id) + ">'s profile\n​\n<:mkwii:1516487193307254955> **Mario Kart Wii**\nRating: " + str(game1) + "\nRanking: **#" + rank1 + "**/" + outof1 + " " + trophy1 + "\n\n<:eatfatfight:1516487268624371887> **Eat Fat Fight**\nRating: " + str(game2) + "\nRanking: **#" + rank2 + "**/" + outof2 + " " + trophy2 + "\n\n<:brawl:1516487351134847078> **Super Smash Bros. Brawl**\nRating: " + str(game3) + "\nRanking: **#" + rank3 + "**/" + outof3 + " " + trophy3 + "\n\n<:resort:1516487437243777187> **Wii Sports Resort Swordfighting**\nRating: " + str(game4) + "\nRanking: **#" + rank4 + "**/" + outof4 + " " + trophy4 + "\n\n<:wiisports:1516487495905448137> **Wii Sports Boxing**\nRating: " + str(game5) + "\nRanking: **#" + rank5 + "**/" + outof5 + " " + trophy5 + "\n\n<:sluggers:1516487555431010456> **Mario Super Sluggers**\nRating: " + str(game6) + "\nRanking: **#" + rank6 + "**/" + outof6 + " " + trophy6,colour=0x4ebcff) # ADDHERE
    embed.set_thumbnail(url=user.display_avatar.url)
    await ctx.send_response(embed=embed)

fin = open(".env","r")
TOKEN = fin.readline().strip()
fin.close()
bot.run(TOKEN)
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)
ongoing_games = {}

# Bot events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

# Start command
@bot.command()
async def start(ctx):
    if ctx.channel.id not in ongoing_games:
        ongoing_games[ctx.channel.id] = {
            "channel": ctx.channel,
            "players": [],
            "current_player": 0,
            "turn": 1,
        }
        await ctx.reply("Starting a new bowling game! Type `!join` to join the game.")
    else:
        await ctx.reply("A game is already in progress in this channel. Please wait for it to finish or use another channel.")

# Join command
@bot.command()
async def join(ctx):
    game = ongoing_games.get(ctx.channel.id)
    if game:
        if ctx.author not in game["players"]:
            game["players"].append(ctx.author)
            await ctx.send(f"{ctx.author.name} has joined the game!")
        else:
            await ctx.send("You're already in the game!")
    else:
        await ctx.send("No game is currently running in this channel. Start a new game with `!start`.")

# Add more commands for the game's logic, such as !bowl, !score, !end, etc.

# Run the bot
TOKEN = 'your-bot-token-here'
bot.run(TOKEN)

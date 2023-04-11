import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

class BowlingGame:
    def __init__(self):
        self.rolls = []
        self.current_roll = 0

    def roll(self, pins):
        self.rolls.append(pins)
        self.current_roll += 1

    def score(self):
        score = 0
        frame_index = 0
        for _ in range(10):
            if self.is_strike(frame_index):
                score += 10 + self.strike_bonus(frame_index)
                frame_index += 1
            elif self.is_spare(frame_index):
                score += 10 + self.spare_bonus(frame_index)
                frame_index += 2
            else:
                score += self.sum_of_balls_in_frame(frame_index)
                frame_index += 2
        return score

    def is_spare(self, frame_index):
        return self.rolls[frame_index] + self.rolls[frame_index + 1] == 10

    def is_strike(self, frame_index):
        return self.rolls[frame_index] == 10

    def sum_of_balls_in_frame(self, frame_index):
        return self.rolls[frame_index] + self.rolls[frame_index + 1]

    def spare_bonus(self, frame_index):
        return self.rolls[frame_index + 2]

    def strike_bonus(self, frame_index):
        return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]

bowling_games = {}

@bot.command()
async def start(ctx):
    if ctx.author.id not in bowling_games:
        bowling_games[ctx.author.id] = BowlingGame()
        await ctx.send(f'{ctx.author.mention}, your bowling game has started! Use !roll [number of pins] to play.')
    else:
        await ctx.send(f'{ctx.author.mention}, you already have an ongoing bowling game.')

@bot.command()
async def roll(ctx, pins: int):
    if ctx.author.id in bowling_games:
        if 0 <= pins <= 10:
            bowling_games[ctx.author.id].roll(pins)
            await ctx.send(f'{ctx.author.mention}, you rolled {pins} pins!')
        else:
            await ctx.send(f'{ctx.author.mention}, please enter a valid number of pins (0-10).')
    else:
        await ctx.send(f'{ctx.author.mention}, you have not started a game yet. Use !start to begin.')

@bot.command()
async def score(ctx):
    if ctx.author.id in bowling_games:
        total_score = bowling_games[ctx.author.id].score()
        await ctx.send(f'{ctx.author.mention}, your current score is: {total_score}')
    else:
        await ctx.send(f'{ctx.author.mention}, you have not started a game yet. Use !start to begin.')

@bot.command()
async def end(ctx):
    if ctx.author.id in bowling_games:
        del bowling_games[ctx.author.id]
        await ctx.send(f'{ctx.author.mention}, your game has ended.')
    else:
        await ctx.send(f'{ctx.author.mention}, you have not started a game yet. Use !start to begin.')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.author.mention}, command not found. Please check your input.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, you are missing a required argument. Please check your input.')
    else:
        raise error

bot.run('Insert Token here') 

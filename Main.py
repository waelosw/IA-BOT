import discord
from discord.ext import commands
import os
import google.generativeai as genai

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

@bot.command()
async def ia(ctx, *, message):
    await ctx.send("Je réfléchis...")

    response = model.generate_content(message)
    await ctx.send(response.text)

bot.run(os.getenv("DISCORD_TOKEN"))

import discord
from discord.ext import commands
import os
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "mistral-small-latest"

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

@bot.command()
async def ia(ctx, *, message):
    await ctx.send("Je réfléchis...")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": message}]
    }

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers=headers,
        json=data
    )

    answer = response.json()["choices"][0]["message"]["content"]
    await ctx.send(answer)

bot.run(os.getenv("DISCORD_TOKEN"))

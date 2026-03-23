import discord
from discord import app_commands
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client_ai = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# Fonction IA (OpenAI)
# -----------------------------
async def ask_ai(question: str) -> str:
    response = client_ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es une IA utile et concise."},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content

# -----------------------------
# Bot Discord
# -----------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(e)

# -----------------------------
# Commande /ia
# -----------------------------
@bot.tree.command(name="ia", description="Pose une question à l'IA OpenAI")
@app_commands.describe(question="La question que tu veux poser")
async def ia(interaction: discord.Interaction, question: str):
    await interaction.response.defer()

    response = await ask_ai(question)
    await interaction.followup.send(response)

# -----------------------------
# Lancement du bot
# -----------------------------
bot.run(DISCORD_TOKEN)

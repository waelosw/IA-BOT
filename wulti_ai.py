import discord
from discord import app_commands
import requests
import os

TOKEN = os.getenv("TOKEN")  # Sur Replit, tu mettras ton token dans les Secrets

intents = discord.Intents.default()
intents.message_content = True


class WultiClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synchronisées.")


client = WultiClient()


def ask_ollama(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "wulti-8b",
        "prompt": prompt,
        "stream": False
    }

    try:
        r = requests.post(url, json=data, timeout=120)
        r.raise_for_status()
    except Exception as e:
        print("Erreur de connexion à Ollama :", e)
        return "Impossible de contacter Ollama."

    try:
        j = r.json()
        return j.get("response", "Aucune réponse d’Ollama.").strip()
    except Exception as e:
        print("Erreur JSON :", e)
        return "Réponse d’Ollama illisible."


@client.event
async def on_ready():
    print(f"Wulti connecté en tant que {client.user}")


@client.tree.command(name="ia", description="Parle avec Wulti (Ollama)")
@app_commands.describe(question="Ta question pour l'IA")
async def ia(interaction: discord.Interaction, question: str):

    print(f"[{interaction.user}] /ia {question}")

    await interaction.response.send_message("Wulti réfléchit...")

    response = ask_ollama(question)

    print(f"Wulti → {response}")

    await interaction.followup.send(response)


client.run(TOKEN)

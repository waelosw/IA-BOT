const { Client, GatewayIntentBits, REST, Routes, SlashCommandBuilder, Events } = require("discord.js");
const fetch = require("node-fetch");

// ------------------------------
// CONFIG
// ------------------------------
const TOKEN = "TON_TOKEN_ICI";
const CLIENT_ID = "TON_CLIENT_ID"; // ID de ton bot
const API_URL = "http://127.0.0.1:8000/chat";

// ------------------------------
// CLIENT DISCORD
// ------------------------------
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

// ------------------------------
// COMMANDE /ask
// ------------------------------
const commands = [
  new SlashCommandBuilder()
    .setName("ask")
    .setDescription("Pose une question à ton IA locale")
    .addStringOption(option =>
      option.setName("prompt")
        .setDescription("Ta question")
        .setRequired(true)
    )
].map(cmd => cmd.toJSON());

// ------------------------------
// DEPLOIEMENT AUTOMATIQUE DES COMMANDES
// ------------------------------
const rest = new REST({ version: "10" }).setToken(TOKEN);

(async () => {
  try {
    console.log("🚀 Déploiement de /ask...");
    await rest.put(
      Routes.applicationCommands(CLIENT_ID),
      { body: commands }
    );
    console.log("✅ Commande /ask prête !");
  } catch (error) {
    console.error(error);
  }
})();

// ------------------------------
// BOT READY
// ------------------------------
client.once(Events.ClientReady, c => {
  console.log(`🤖 Bot connecté en tant que ${c.user.tag}`);
});

// ------------------------------
// LOGIQUE DE /ask
// ------------------------------
client.on(Events.InteractionCreate, async interaction => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === "ask") {
    const prompt = interaction.options.getString("prompt");

    await interaction.reply("⏳ Je réfléchis...");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });

      const data = await response.json();

      await interaction.editReply(data.response || "Erreur API");
    } catch (err) {
      await interaction.editReply("❌ Impossible de contacter l'API locale.");
    }
  }
});

// ------------------------------
// LANCEMENT DU BOT
// ------------------------------
client.login(TOKEN);

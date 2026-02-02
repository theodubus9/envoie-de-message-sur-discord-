import discord
from discord.ext import tasks
import os

# ==================== TA CONFIGURATION ====================
# 1. Colle ton TOKEN entre les guillemets
TOKEN = "TON TOKEN ICI"

# 2. Tes IDs de salons
CHANNELS_IDS = [1431010690835156992, 123456789012345678]

# 3. Tes réglages
PHOTOS = ["1.jpg", "2.jpg", "3.jpg"]
MESSAGE = "Dm me (only duel)  !"
DELAI = 60  # Secondes
# ==========================================================

# Configuration des permissions (Intents)
intents = discord.Intents.default()
intents.message_content = True 

bot_actif = True

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'✅ Connecté en tant que : {self.user}')
        if not self.envoi_auto.is_running():
            self.envoi_auto.start()

    @tasks.loop(seconds=DELAI)
    async def envoi_auto(self):
        if not bot_actif:
            return
        
        for channel_id in CHANNELS_IDS:
            channel = self.get_channel(channel_id)
            if channel:
                try:
                    # On vérifie si les photos existent avant d'essayer de les envoyer
                    files_to_send = []
                    for p in PHOTOS:
                        if os.path.exists(p):
                            files_to_send.append(discord.File(p))
                    
                    await channel.send(MESSAGE, files=files_to_send)
                    print(f"✅ Envoyé dans : {channel_id}")
                except Exception as e:
                    print(f"❌ Erreur salon {channel_id} : {e}")

    async def on_message(self, message):
        global bot_actif
        # On n'écoute que tes propres messages pour les commandes
        if message.author.id != self.user.id:
            return

        if message.content == "!off":
            bot_actif = False
            await message.channel.send("🛑 **Bot mis en PAUSE.**")
        
        elif message.content == "!on":
            bot_actif = True
            await message.channel.send("▶️ **Bot RÉACTIVÉ.**")

client = MyClient(intents=intents)
client.run(TOKEN)

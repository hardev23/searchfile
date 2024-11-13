import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer el contenido de los mensajes

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Indica que el bot está en línea."""
    print(f'Conectado como {bot.user}')

@bot.command()
async def buscar(ctx, *, query):
    """Comando para buscar un archivo EPUB en el servidor y enviarlo por mensaje privado."""
    results = []

    channel = discord.utils.get(ctx.guild.text_channels, name='libros')  # Cambia esto si es necesario
    if not channel:
        await ctx.send("No pude encontrar el canal para buscar los archivos.")
        return

    async for message in channel.history(limit=None):
        for attachment in message.attachments:
            if attachment.filename.lower().endswith('.epub'):
                if query.lower() in attachment.filename.lower():
                    results.append(attachment.url)

    if results:
        for result_url in results:
            try:
                await ctx.author.send(f"¡He encontrado tu libro! Aquí está el enlace: {result_url}")
            except discord.Forbidden:
                await ctx.author.send("No puedo enviarte el archivo porque tienes los mensajes privados desactivados.")
    else:
        await ctx.author.send('No se encontraron archivos que coincidan con tu búsqueda.')

# Cargar el token desde las variables de entorno
token = os.getenv("DISCORD_TOKEN")
if token is None:
    print("Error: No se encontró el token de Discord en las variables de entorno.")
else:
    bot.run(token)

# Aquí Vercel requiere que devolvamos algo, así que utilizamos un endpoint vacío.
def handler(request):
    return "Bot funcionando..."

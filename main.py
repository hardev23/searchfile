import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import unicodedata

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
    # Inicializa una lista para almacenar los archivos encontrados
    results = []

    # Asegúrate de que el bot está buscando en el canal correcto
    channel = discord.utils.get(ctx.guild.text_channels, name='libros')  # Cambia esto si es necesario
    if not channel:
        await ctx.send("No pude encontrar el canal para buscar los archivos.")
        return

    # Normaliza la consulta para manejar acentos y convertir todo a minúsculas
    query = unicodedata.normalize('NFKD', query).encode('ascii', 'ignore').decode('ascii').lower()

    # Recorre todos los mensajes del canal
    async for message in channel.history(limit=None):  # Recorre todo el historial del canal
        for attachment in message.attachments:
            # Asegúrate de que el archivo tiene la extensión .epub
            if attachment.filename.lower().endswith('.epub'):
                # Normaliza el nombre del archivo
                filename = unicodedata.normalize('NFKD', attachment.filename).encode('ascii', 'ignore').decode('ascii').lower()
                
                # Realiza la búsqueda considerando todas las palabras de la consulta
                if all(word in filename for word in query.split()):
                    results.append(attachment.url)

    # Si se encuentran resultados, envíalos por mensaje privado
    if results:
        for result_url in results:
            try:
                # Enviar el archivo por mensaje privado
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

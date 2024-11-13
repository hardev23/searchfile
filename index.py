import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask
import threading

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer el contenido de los mensajes

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")
    print(f"ID del bot: {bot.user.id}")


@bot.command()
async def buscar(ctx, *, query):
    """Comando para buscar un archivo EPUB en el servidor y enviarlo por mensaje privado."""
    results = []

    # Buscar en un canal específico
    channel = discord.utils.get(ctx.guild.text_channels, name='libros')  # Cambia esto si es necesario
    if not channel:
        await ctx.send("No pude encontrar el canal para buscar los archivos.")
        return

    async for message in channel.history(limit=None):  # Recorre todo el historial del canal
        for attachment in message.attachments:
            if attachment.filename.lower().endswith('.epub') and query.lower() in attachment.filename.lower():
                results.append(attachment.url)

    if results:
        for result_url in results:
            try:
                await ctx.author.send(f"¡He encontrado tu libro! Aquí está el enlace: {result_url}")
            except discord.Forbidden:
                await ctx.author.send("No puedo enviarte el archivo porque tienes los mensajes privados desactivados.")
    else:
        await ctx.author.send('No se encontraron archivos que coincidan con tu búsqueda.')

# Crear un servidor Flask para el endpoint HTTP
app = Flask("")

@app.route("/")
def home():
    return "Bot funcionando correctamente"

# Función para ejecutar el servidor Flask en un hilo
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Iniciar el bot y Flask
def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    if not token:  # Verificar si el token está definido
        print("Error: DISCORD_TOKEN no está definido.")
        exit(1)  # Terminar el programa
    bot.run(token)


    

if __name__ == "__main__":
    # Crear un hilo para ejecutar Flask
    threading.Thread(target=run_flask).start()
    # Ejecutar el bot en el hilo principal
    run_bot()

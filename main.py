import os
import time
import random
import requests
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Загрузка настроек
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

client = TelegramClient("weather_userbot", API_ID, API_HASH)

# Переменные режимов
auto_reply_text = None
pickme_mode = False

# Функция погоды (через wttr.in)
def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+(ощущается+как+%f)&lang=ru"
        r = requests.get(url, timeout=5)
        if r.status_code == 200 and "Unknown location" not in r.text:
            return f"🏙 **Погода в {city.capitalize()}:**\n☁️ {r.text}"
        return f"❌ Город **{city}** не найден."
    except:
        return "❌ Ошибка сервиса погоды."

# --- ОБРАБОТКА КОМАНД ---

@client.on(events.NewMessage(pattern=r"\.погода (.*)", outgoing=True))
async def weather_handler(event):
    city = event.pattern_match.group(1)
    await event.edit(f"🔍 Ищу погоду: {city}...")
    await event.edit(get_weather(city))

@client.on(events.NewMessage(pattern=r"\.пинг", outgoing=True))
async def ping_handler(event):
    start = time.time()
    await event.edit("🚀")
    ms = round((time.time() - start) * 1000)
    await event.edit(f"🚀 **Понг!** | `{ms}мс`")

@client.on(events.NewMessage(pattern=r"\.автовкл (.+)", outgoing=True))
async def auto_on(event):
    global auto_reply_text
    auto_reply_text = event.pattern_match.group(1)
    await event.edit(f"✅ **Автоответчик активирован!**")

@client.on(events.NewMessage(pattern=r"\.автовыкл", outgoing=True))
async def auto_off(event):
    global auto_reply_text
    auto_reply_text = None
    await event.edit("❌ **Автоответчик выключен.**")

@client.on(events.NewMessage(pattern=r"\.пикми", outgoing=True))
async def pickme_toggle(event):
    global pickme_mode
    pickme_mode = not pickme_mode
    status = "АКТИВИРОВАН 💦" if pickme_mode else "ВЫКЛЮЧЕН"
    await event.edit(f"🤡 **Pick-me режим:** `{status}`")

@client.on(events.NewMessage(pattern=r"\.помощь|\.хелп", outgoing=True))
async def help_handler(event):
    await event.edit("⚙️ **Команды:**\n.погода <город>\n.пикми\n.автовкл <текст>\n.автовыкл\n.пинг")

# --- ЛОГИКА РАБОТЫ ---

@client.on(events.NewMessage(incoming=True))
async def incoming_handler(event):
    if event.is_private and auto_reply_text:
        await event.reply(auto_reply_text)

@client.on(events.NewMessage(outgoing=True))
async def outgoing_handler(event):
    global pickme_mode
    if pickme_mode and not event.text.startswith("."):
        suffixes = [" а-а д..а?~", " ой.. я аж потекла..", " ах..~", " м-м..~"]
        await event.edit(event.text + random.choice(suffixes))

print("Бот запущен!")
client.start()
client.run_until_disconnected()
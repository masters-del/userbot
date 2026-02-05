import os
import asyncio
from telethon import TelegramClient, events
import requests
from dotenv import load_dotenv

# --- БЛОК АВТОМАТИЧЕСКОЙ НАСТРОЙКИ ---
def initial_setup():
    if not os.path.exists('.env'):
        print("=== ПЕРВАЯ НАСТРОЙКА ЮЗЕРБОТА ===")
        print("Файл .env не найден. Давай создадим его прямо сейчас.")
        api_id = input("Введите ваш API ID (с сайта my.telegram.org): ").strip()
        api_hash = input("Введите ваш API HASH: ").strip()
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f"API_ID={api_id}\n")
            f.write(f"API_HASH={api_hash}\n")
        print("=== НАСТРОЙКА ЗАВЕРШЕНА! Файл .env создан. ===\n")

# Запускаем проверку перед основным кодом
initial_setup()
load_dotenv()

# Подгружаем переменные
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Проверка, что ID — это число
try:
    API_ID = int(API_ID)
except (TypeError, ValueError):
    print("Ошибка: API_ID должен быть числом. Проверьте файл .env")
    exit()

client = TelegramClient('weather_userbot', API_ID, API_HASH)

# --- ПЕРЕМЕННЫЕ РЕЖИМОВ ---
pick_me_mode = False

# --- КОМАНДЫ ---

@client.on(events.NewMessage(pattern=r'\.хелп', outgoing=True))
async def help_command(event):
    help_text = (
        "**Меню команд юзербота:**\n\n"
        "`.погода [город]` — Узнать погоду\n"
        "`.пикми` — Включить/выключить режим Pick-me\n"
        "`.пинг` — Проверить скорость\n"
        "`.хелп` — Показать это меню"
    )
    await event.edit(help_text)

@client.on(events.NewMessage(pattern=r'\.пинг', outgoing=True))
async def ping(event):
    await event.edit("🚀 Понг! Бот работает как часы.")

@client.on(events.NewMessage(pattern=r'\.пикми', outgoing=True))
async def toggle_pick_me(event):
    global pick_me_mode
    pick_me_mode = not pick_me_mode
    status = "ВКЛЮЧЕН" if pick_me_mode else "ВЫКЛЮЧЕН"
    await event.edit(f"💅 Режим Pick-me **{status}**")

@client.on(events.NewMessage(outgoing=True))
async def pick_me_handler(event):
    if pick_me_mode and not event.text.startswith('.'):
        await event.edit(f"{event.text} а-а д..а?~")

@client.on(events.NewMessage(pattern=r'\.погода (.+)', outgoing=True))
async def get_weather(event):
    city = event.pattern_match.group(1)
    await event.edit(f"☁️ Ищу погоду для города: {city}...")
    
    try:
        # Используем бесплатное API без ключа (wttr.in)
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            await event.edit(f"📍 Погода: {response.text}")
        else:
            await event.edit("❌ Не удалось найти такой город.")
    except Exception as e:
        await event.edit(f"❌ Ошибка: {e}")

# --- ЗАПУСК ---
print("--- Юзербот запускается... ---")
client.start()
print("--- Юзербот запущен! Напиши .хелп в любом чате ---")
client.run_until_disconnected()
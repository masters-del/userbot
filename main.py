import os
import sys
import time
import asyncio
import random
from dotenv import load_dotenv
from telethon import TelegramClient, events
from gtts import gTTS
from colorama import Fore, Style, init
import google.generativeai as genai

# --- Инициализация ---
init(autoreset=True)
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# --- Настройка Gemini AI ---
GEMINI_KEY = os.getenv("GEMINI_KEY") or "AIzaSyD2MnB0xP7gslNIeHalUEW9DAm1xNcHKKc"
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-pro')
    print(Fore.CYAN + "Gemini AI настроен успешно!" + Style.RESET_ALL)
else:
    model = None
    print(Fore.YELLOW + "⚠️ GEMINI_KEY не найден, команды .ai и автоответчик работать не будут" + Style.RESET_ALL)

# --- Инициализация Telethon ---
client = TelegramClient('stupid_session', API_ID, API_HASH)

# --- Баннер ---
banner = f"""
{Fore.MAGENTA}
╔═════════════════════════════════════════════╗
║      🧬 STUPID USERBOT v9.3 ELITE          ║
╠═════════════════════════════════════════════╣
║  Бот успешно запущен!                       ║
║  Напиши .help в Telegram для команд         ║
║                                             ║
║  ⚠️ ВНИМАНИЕ: Мы не несем ответственности ║
║      за использование бота                  ║
╚═════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

print(Fore.MAGENTA + "Запуск STUPID USERBOT v9.3", end="")
for _ in range(3):
    print(".", end="", flush=True)
    time.sleep(0.3)
print(Style.RESET_ALL)
print(banner)

# --- Глобальные переменные ---
AUTO_REPLY_ENABLED = True
AFK_MESSAGE = None
AUTO_REPLY_INTRO = True

LOVE_EMOJIS = ["❤️","💛","💚","💙","💜","🖤","💘","💖","💌","🌹","💐"]
FLIRT_MESSAGES = [
    "💖 Ты выглядишь потрясающе сегодня!",
    "💌 Каждое твоё сообщение радует меня!",
    "🌹 Твои глаза сияют как звёзды!",
    "💞 Ты моя радость этого дня!",
    "💘 С тобой всегда весело и уютно!"
]

# --- Вспомогательные функции ---
async def print_animated(event, message):
    current = ""
    for char in message:
        current += char
        await event.edit(current + random.choice(LOVE_EMOJIS))
        await asyncio.sleep(0.02 + random.random()*0.03)
    await event.edit(current)

# --- Команды ---

# 1. Помощь
@client.on(events.NewMessage(pattern=r'\.help', outgoing=True))
async def help_cmd(event):
    help_text = (
        "🧬 STUPID USERBOT v9.3 Elite\n\n"
        "✨ Команды:\n"
        "• .ping — Пинг\n"
        "• .type [текст] — Эффект печати\n"
        "• .ai [вопрос] — Спросить AI\n"
        "• .tts [текст] — Голосовое сообщение\n"
        "• .heart — Анимация любви\n"
        "• .restart — Перезагрузка\n"
        "• .afk [текст] — Установить AFK статус\n"
        "• .autoreply on/off — Включить/выключить автоответчик\n"
        "• .love [имя] — Любовное сообщение\n"
        "• .hug [имя] — Объятия\n"
        "• .kiss [имя] — Поцелуй\n"
        "• .flowers [имя] — Виртуальные цветы\n"
        "• .flirt — Случайный комплимент\n"
        "⚠️ Не несем ответственности за использование\n"
    )
    current = ""
    for char in help_text:
        current += char
        await event.edit(current + "▒")
        await asyncio.sleep(0.02 + random.random()*0.03)
    await event.edit(current)

# 2. Пинг
@client.on(events.NewMessage(pattern=r'\.ping', outgoing=True))
async def ping(event):
    start = time.time()
    await event.edit("<b>🏓 Понг...</b>", parse_mode='html')
    end = time.time()
    await event.edit(f"<b>🏓 Понг! ({(end - start):.3f} сек)</b>", parse_mode='html')

# 3. Печатная машинка
@client.on(events.NewMessage(pattern=r'\.type (.*)', outgoing=True))
async def typewriter(event):
    text = event.pattern_match.group(1)
    current = ""
    for char in text:
        current += char
        await event.edit(current + "▒")
        await asyncio.sleep(0.05)
    await event.edit(current)

# 4. AI запрос
@client.on(events.NewMessage(pattern=r'\.ai (.*)', outgoing=True))
async def ai_query(event):
    if not model:
        return await event.edit("❌ Ключ AI не найден, команда .ai не работает")
    prompt = event.pattern_match.group(1)
    await event.edit("🤖 <i>Думаю...</i>", parse_mode='html')
    try:
        response = model.generate_content(prompt)
        await event.edit(f"<b>🤖 Ответ AI:</b>\n\n{response.text}", parse_mode='html')
    except Exception as e:
        await event.edit(f"❌ Ошибка AI: {e}")

# 5. TTS
@client.on(events.NewMessage(pattern=r'\.tts (.*)', outgoing=True))
async def tts(event):
    text = event.pattern_match.group(1)
    await event.edit("🎙 <i>Записываю голос...</i>", parse_mode='html')
    tts_obj = gTTS(text=text, lang='ru')
    tts_obj.save("voice.mp3")
    await client.send_file(event.chat_id, "voice.mp3", voice_note=True)
    await event.delete()
    os.remove("voice.mp3")

# 6. Сердца
@client.on(events.NewMessage(pattern=r'\.heart', outgoing=True))
async def hearts(event):
    for h in LOVE_EMOJIS:
        await event.edit(h)
        await asyncio.sleep(0.3)

# 7. Перезапуск
@client.on(events.NewMessage(pattern=r'\.restart', outgoing=True))
async def restart(event):
    await event.edit("🔄 <b>Перезапуск системы...</b>", parse_mode='html')
    os.execl(sys.executable, sys.executable, *sys.argv)

# 8. AFK
@client.on(events.NewMessage(pattern=r'\.afk (.+)', outgoing=True))
async def set_afk(event):
    global AFK_MESSAGE
    AFK_MESSAGE = event.pattern_match.group(1)
    await event.edit(f"💤 AFK статус установлен:\n\n{AFK_MESSAGE}")

# 9. Auto-reply
@client.on(events.NewMessage(pattern=r'\.autoreply (on|off)', outgoing=True))
async def toggle_autoreply(event):
    global AUTO_REPLY_ENABLED
    status = event.pattern_match.group(1).lower()
    if status == "on":
        AUTO_REPLY_ENABLED = True
        await event.edit("✅ Автоответчик включен")
    else:
        AUTO_REPLY_ENABLED = False
        await event.edit("❌ Автоответчик выключен")

# 10. Автоответчик с приветствием + AI
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    global AUTO_REPLY_ENABLED, AFK_MESSAGE, AUTO_REPLY_INTRO
    if event.out or not AUTO_REPLY_ENABLED:
        return
    sender = await event.get_sender()
    user_name = sender.first_name or "Пользователь"
    text = event.message.message.strip()
    if len(text) == 0:
        return
    if AFK_MESSAGE:
        await event.respond(f"💤 Я сейчас AFK:\n{AFK_MESSAGE}")
        return
    if AUTO_REPLY_INTRO:
        intro_text = (
            f"👋 Привет {user_name}! Сейчас я занят, но вам поможет мой AI-агент!\n"
            "❗ Пишите только реплаем на мои сообщения вопросы и он даст вам ответ!"
        )
        await event.respond(intro_text)
        AUTO_REPLY_INTRO = False
        return
    if event.is_reply:
        replied = await event.get_reply_message()
        if replied.from_id == (await client.get_me()).id:
            if model:
                await event.respond("🤖 <i>Думаю...</i>", parse_mode='html')
                try:
                    response = model.generate_content(text)
                    reply_text = ""
                    for char in response.text:
                        reply_text += char
                        await event.reply(reply_text + "▒")
                        await asyncio.sleep(0.01 + random.random()*0.02)
                except Exception as e:
                    await event.respond(f"❌ Ошибка AI: {e}")

# --- Любовный модуль ---
@client.on(events.NewMessage(pattern=r'\.love (.+)', outgoing=True))
async def love_msg(event):
    name = event.pattern_match.group(1)
    message = f"💖 {name}, ты особенная! 💖\nМой AI-агент готов поддержать переписку! 😘"
    await print_animated(event, message)

@client.on(events.NewMessage(pattern=r'\.hug (.+)', outgoing=True))
async def hug(event):
    name = event.pattern_match.group(1)
    message = f"🤗 Обнимаю тебя, {name}! 💞"
    await print_animated(event, message)

@client.on(events.NewMessage(pattern=r'\.kiss (.+)', outgoing=True))
async def kiss(event):
    name = event.pattern_match.group(1)
    message = f"😘 Целую тебя, {name}! 💋💖"
    await print_animated(event, message)

@client.on(events.NewMessage(pattern=r'\.flowers (.+)', outgoing=True))
async def flowers(event):
    name = event.pattern_match.group(1)
    message = f"🌹 {name}, получай виртуальные цветы! 🌺💐"
    await print_animated(event, message)

@client.on(events.NewMessage(pattern=r'\.flirt', outgoing=True))
async def flirt(event):
    message = random.choice(FLIRT_MESSAGES)
    await print_animated(event, message)

# --- Старт ---
client.start()
print(Fore.GREEN + "Бот запущен! Жди команд в Telegram." + Style.RESET_ALL)
client.run_until_disconnected()
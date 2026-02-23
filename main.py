import os
import sys
import time
import asyncio
import random
from telethon import TelegramClient, events
from gtts import gTTS
from colorama import Fore, Style, init
import google.generativeai as genai

init(autoreset=True)

# ===== CONFIG =====
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# ===== GEMINI (ВШИТЫЙ КЛЮЧ) =====
GEMINI_KEY = "AIzaSyD2MnB0xP7gslNIeHalUEW9DAm1xNcHKKc"

try:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-pro")
    print("🤖 Gemini подключен")
except Exception as e:
    print(f"❌ Gemini error: {e}")
    model = None

client = TelegramClient('stupid_session', API_ID, API_HASH)

# ===== STATE =====
AFK = False
AFK_TEXT = ""
AUTO_REPLY = False

# ===== БАННЕР =====
print(Fore.MAGENTA + "Запуск STUPID USERBOT...", end="")
for _ in range(3):
    print(".", end="", flush=True)
    time.sleep(0.3)

print(f"""{Fore.MAGENTA}

╔══════════════════════════════════╗
║  🧬 STUPID USERBOT v9.3 ELITE  ║
╠══════════════════════════════════╣
║     Система успешно запущена     ║
║  Мы не несем ответственности 😈  ║
╚══════════════════════════════════╝

{Style.RESET_ALL}""")

# ===== HELP =====
@client.on(events.NewMessage(pattern=r'\.help', outgoing=True))
async def help_cmd(event):
    text = (
        "<b>🧬 STUPID USERBOT</b>\n\n"
        "• .ping\n"
        "• .type текст\n"
        "• .ai вопрос\n"
        "• .tts текст\n"
        "• .restart\n\n"
        "💤 .afk текст / off\n"
        "🤖 .autoreply on/off\n\n"
        "💖 .love / .hug / .kiss / .flowers / .flirt"
    )
    await event.edit(text, parse_mode='html')

# ===== PING =====
@client.on(events.NewMessage(pattern=r'\.ping', outgoing=True))
async def ping(event):
    start = time.time()
    await event.edit("🏓...")
    await asyncio.sleep(0.2)
    ms = round((time.time()-start)*1000)
    await event.edit(f"🏓 {ms}ms")

# ===== TYPE =====
@client.on(events.NewMessage(pattern=r'\.type (.*)', outgoing=True))
async def type_cmd(event):
    text = event.pattern_match.group(1)
    msg = ""
    for c in text:
        msg += c
        await event.edit(msg + "▒")
        await asyncio.sleep(0.03)
    await event.edit(msg)

# ===== AI =====
@client.on(events.NewMessage(pattern=r'\.ai (.*)', outgoing=True))
async def ai(event):
    if not model:
        return await event.edit("❌ AI недоступен")

    q = event.pattern_match.group(1)
    await event.edit("🤖 Думаю...")

    try:
        r = model.generate_content(q)
        await event.edit(r.text[:4000])
    except Exception as e:
        await event.edit(f"Ошибка: {e}")

# ===== TTS =====
@client.on(events.NewMessage(pattern=r'\.tts (.*)', outgoing=True))
async def tts(event):
    text = event.pattern_match.group(1)
    tts = gTTS(text=text, lang='ru')
    tts.save("voice.mp3")
    await client.send_file(event.chat_id, "voice.mp3", voice_note=True)
    await event.delete()
    os.remove("voice.mp3")

# ===== AFK =====
@client.on(events.NewMessage(pattern=r'\.afk(?: (.*))?', outgoing=True))
async def afk(event):
    global AFK, AFK_TEXT
    arg = event.pattern_match.group(1)

    if arg == "off":
        AFK = False
        return await event.edit("✅ AFK OFF")

    AFK = True
    AFK_TEXT = arg or "Я отошел"
    await event.edit(f"💤 AFK:\n{AFK_TEXT}")

# ===== AUTOREPLY =====
@client.on(events.NewMessage(pattern=r'\.autoreply (on|off)', outgoing=True))
async def ar(event):
    global AUTO_REPLY
    AUTO_REPLY = event.pattern_match.group(1) == "on"
    await event.edit(f"🤖 AUTO: {AUTO_REPLY}")

# ===== INCOMING =====
@client.on(events.NewMessage(incoming=True))
async def incoming(event):
    global AFK, AUTO_REPLY

    sender = await event.get_sender()
    name = sender.first_name

    if AFK:
        await event.reply(
            f'Привет "{name}" сейчас я занят но вам поможет мой AI-агент!\n'
            f'Пишите реплаем.'
        )

    if AUTO_REPLY and event.is_reply and model:
        try:
            r = model.generate_content(event.raw_text)
            await event.reply(r.text[:1000])
        except:
            pass

# ===== LOVE =====
async def love_anim(event, text):
    msg = ""
    for c in text:
        msg += c
        await event.edit(msg + random.choice(["❤️","💖","💘"]))
        await asyncio.sleep(0.03)
    await event.edit(msg)

@client.on(events.NewMessage(pattern=r'\.love (.*)', outgoing=True))
async def love(event):
    await love_anim(event, f"{event.pattern_match.group(1)}, ты топ 💖")

@client.on(events.NewMessage(pattern=r'\.hug (.*)', outgoing=True))
async def hug(event):
    await love_anim(event, f"Обнимаю {event.pattern_match.group(1)} 🤗")

@client.on(events.NewMessage(pattern=r'\.kiss (.*)', outgoing=True))
async def kiss(event):
    await love_anim(event, f"Целую {event.pattern_match.group(1)} 😘")

@client.on(events.NewMessage(pattern=r'\.flowers (.*)', outgoing=True))
async def flowers(event):
    await love_anim(event, f"{event.pattern_match.group(1)}, цветы 🌹")

@client.on(events.NewMessage(pattern=r'\.flirt', outgoing=True))
async def flirt(event):
    msgs = ["Ты кайф 😏","Ты космос 🚀","Ты лучшая 💖"]
    await love_anim(event, random.choice(msgs))

# ===== RESTART =====
@client.on(events.NewMessage(pattern=r'\.restart', outgoing=True))
async def restart(event):
    await event.edit("🔄...")
    os.execl(sys.executable, sys.executable, *sys.argv)

# ===== START =====
client.start()
client.run_until_disconnected()
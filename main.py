import os, asyncio, random, requests, sys, io, traceback
from telethon import TelegramClient, events, functions, types
from dotenv import load_dotenv
from gtts import gTTS

# ========================================================
# [ ⚙️ КОНФИГУРАЦИЯ ]
# ========================================================
def setup_env():
    if not os.path.exists('.env'):
        print("⚠️ Файл .env не найден! Настраиваем...")
        api_id = input("Введите API_ID: ").strip()
        api_hash = input("Введите API_HASH: ").strip()
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\n")

setup_env()
load_dotenv()

client = TelegramClient('stupid_session', int(os.getenv("API_ID")), os.getenv("API_HASH"))

class State:
    shavka = False
    troll = False
    reactions = False
    afk = False
    afk_reason = ""

# ========================================================
# [ 📝 БАЗА ДАННЫХ ]
# ========================================================
trolls = [
    "Дед в канаве медь доедает, а ты тут пишешь?",
    "Мать твою в ломбард сдал, за неё даже сотку не дали.",
    "Батя твой админ гей-клуба.",
    "Твоя родословная — это ошибка пьяного зоолога.",
    "Твое лицо — аргумент в пользу абортов.",
    "Ты как демо-версия человека: вроде похоже, но функций ноль."
]

shavka_suffixes = [
    " (⁄ ⁄•⁄ω⁄•⁄ ⁄) ..да, хозяин..~",
    " ..а-а.. м..ожно ещё?~ 💦",
    " *дрожу* ..с..лушаюсь.. ✨",
    " (｡◕‿◕｡) ..я хорошая девочка?~",
    " ..т-теку.. только не бросай меня.. 🎀",
    " ..х..очу наказания..~ ⛓️",
    " *тихо скулю* ..б..ольше внимания..~ ❤️",
    " (⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄) ..в..аша навсегда..~",
    " ..о..шейник такой холодный..~ ✨",
    " *прикусила губку* ..м..ожно ещё боли?~ 😈",
    " ..г..отова на всё.. только прикажите.. 💍",
    " ..м..яу.. погладьте меня..~ 🐱",
    " *опустила глазки* ..п..ростите за всё.. ✨",
    " ..а..х.. как горячо..~ 🔥",
    " (｡♥‿♥｡) ..б..оготворю вас..~",
    " *встала на четвереньки* ..ж..ду приказов.. ⛓️",
    " ..м..ожно лизнуть сапог?~ 👅",
    " ..т..олько не бейте сильно сегодня..~ 🐾"
]

# ========================================================
# [ 🛠 СЛУЖЕБНЫЕ ФУНКЦИИ ]
# ========================================================
async def send_log(error_text, cmd_name="SYSTEM"):
    try: await client.send_message("me", f"❌ **[ ОШИБКА ]**\n**Команда:** `{cmd_name}`\n`{error_text[-3000:]}`")
    except: pass

def error_handler(func):
    async def wrapper(e):
        try: await func(e)
        except Exception: await send_log(traceback.format_exc(), func.__name__)
    return wrapper

# ========================================================
# [ 📜 КОМАНДЫ ]
# ========================================================

@client.on(events.NewMessage(pattern=r'\.хелп', outgoing=True))
@error_handler
async def cmd_help(e):
    m = (
        "**[ 🧬 Stupid Userbot v6.2 ]**\n\n"
        "── **АВТООТВЕТЧИК** ──\n"
        "`.авто [текст]` — ВКЛ\n"
        "`.автостоп` — ВЫКЛ\n\n"
        "── **ЭФФЕКТЫ** ──\n"
        "`.печать [текст]` | `.реверс` | `.взлом`\n"
        "`.кость [1-6]` — Чит\n\n"
        "── **РЕЖИМЫ** ──\n"
        "`.шавка` | `.тролль` | `.реак` (🤡)\n\n"
        "── **ИНСТРУМЕНТЫ** ──\n"
        "`.все` | `.дел [n]` | `.гс [текст]` | `.пинг`"
    )
    await e.edit(m)

# --- АВТООТВЕТЧИК (ПРОВЕРЕННЫЙ) ---

@client.on(events.NewMessage(pattern=r'\.авто (.+)', outgoing=True))
@error_handler
async def cmd_afk_on(e):
    State.afk = True
    State.afk_reason = e.pattern_match.group(1)
    await e.edit(f"✅ **Автоответчик ВКЛ!**\nТекст: `{State.afk_reason}`")

@client.on(events.NewMessage(pattern=r'\.автостоп', outgoing=True))
@error_handler
async def cmd_afk_off(e):
    State.afk = False
    await e.edit("❌ **Автоответчик ВЫКЛ.**")

@client.on(events.NewMessage(incoming=True))
async def handle_afk_logic(e):
    if State.afk and e.is_private:
        me = await client.get_me()
        if e.sender_id == me.id: return
        sender = await e.get_sender()
        if sender and getattr(sender, 'bot', False): return
        await asyncio.sleep(1)
        await e.reply(f"**[🤖 Автоответчик]**\n{State.afk_reason}")

# --- ЭФФЕКТЫ ---

@client.on(events.NewMessage(pattern=r'\.печать (.+)', outgoing=True))
@error_handler
async def cmd_typewriter(e):
    text = e.pattern_match.group(1)
    curr = ""
    for char in text:
        curr += char
        try: await e.edit(f"**{curr}▒**"); await asyncio.sleep(0.15)
        except: pass
    await e.edit(f"**{curr}**")

@client.on(events.NewMessage(pattern=r'\.реверс ?(.*)', outgoing=True))
@error_handler
async def cmd_reverse(e):
    r = await e.get_reply_message()
    t = e.pattern_match.group(1) or (r.text if r else None)
    if t: await e.edit(t[::-1])

@client.on(events.NewMessage(pattern=r'\.кость (\d+)', outgoing=True))
@error_handler
async def cmd_dice(e):
    v = int(e.pattern_match.group(1))
    if not (1 <= v <= 6): return await e.edit("1-6!")
    await e.delete()
    while True:
        res = await client(functions.messages.SendDiceRequest(peer=e.chat_id, emoji="🎲"))
        if res.updates[0].message.media.value == v: break
        await client.delete_messages(e.chat_id, [res.updates[0].message.id])

# --- РЕЖИМЫ (ШАВКА С СУФФИКСАМИ) ---

@client.on(events.NewMessage(pattern=r'\.(шавка|тролль|реак)', outgoing=True))
@error_handler
async def cmd_toggle(e):
    c = e.pattern_match.group(1)
    if c == "шавка": State.shavka = not State.shavka; State.troll = False; s = State.shavka
    elif c == "тролль": State.troll = not State.troll; State.shavka = False; s = State.troll
    else: State.reactions = not State.reactions; s = State.reactions
    await e.edit(f"**{c.upper()}**: {'✅' if s else '❌'}")

@client.on(events.NewMessage(outgoing=True))
async def handle_modes(e):
    if not e.text or e.text.startswith('.'): return
    if State.shavka: await e.edit(f"{e.text}{random.choice(shavka_suffixes)}")
    elif State.troll: await e.edit(f"{e.text}\n\n**[!]** {random.choice(trolls)}")

@client.on(events.NewMessage(incoming=True))
async def handle_auto_react(e):
    if State.reactions and not e.is_private:
        try: await client(functions.messages.SendReactionRequest(peer=e.chat_id, msg_id=e.id, reaction=[types.ReactionEmoji(emoticon='🤡')]))
        except: pass

# --- ИНСТРУМЕНТЫ ---

@client.on(events.NewMessage(pattern=r'\.гс (.+)', outgoing=True))
@error_handler
async def cmd_tts(e):
    t = e.pattern_match.group(1); tts = gTTS(t, lang='ru'); out = io.BytesIO()
    tts.write_to_fp(out); out.name = "v.mp3"; out.seek(0)
    await e.delete(); await client.send_file(e.chat_id, out, voice=True)

@client.on(events.NewMessage(pattern=r'\.пинг', outgoing=True))
async def cmd_ping(e): await e.edit("`БОТ ЛЕТИТ: 0.01ms` ⚡")

@client.on(events.NewMessage(pattern=r'\.дел (\d+)', outgoing=True))
@error_handler
async def cmd_del(e):
    n = int(e.pattern_match.group(1)); await e.delete()
    async for m in client.iter_messages(e.chat_id, limit=n, from_user='me'): await m.delete()

# ========================================================
# [ 🚀 ЗАПУСК ]
# ========================================================
async def main():
    await client.start()
    await client.send_message("me", "✅ **Бот v6.2 FINAL запущен!**\nШавка, Автоответчик и Кости в норме.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
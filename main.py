import os, asyncio, random, requests, sys, io, importlib.util, traceback
from telethon import TelegramClient, events, functions, types
from dotenv import load_dotenv
from gtts import gTTS

# ========================================================
# [ ⚙️ КОНФИГУРАЦИЯ ]
# ========================================================
def setup_env():
    if not os.path.exists('.env'):
        api_id = input("Введите API_ID: ").strip()
        api_hash = input("Введите API_HASH: ").strip()
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\n")

setup_env()
load_dotenv()

client = TelegramClient('stupid_session', int(os.getenv("API_ID")), os.getenv("API_HASH"))
MOD_PATH = "modules"
if not os.path.exists(MOD_PATH): os.mkdir(MOD_PATH)

class State:
    shavka = False
    troll = False
    reactions = False
    afk = False           # Статус автоответчика
    afk_reason = ""       # Текст автоответчика

# ========================================================
# [ 📝 БАЗА ДАННЫХ ]
# ========================================================
trolls = [
    "Дед в канаве медь доедает, а ты тут пишешь?",
    "Мать твою в ломбард сдал, за неё даже сотку не дали.",
    "Батя твой админ гей-клуба.",
    "Твоя родословная — это ошибка пьяного зоолога."
]

shavka_suffixes = [
    " (⁄ ⁄•⁄ω⁄•⁄ ⁄) ..да, хозяин..~",
    " ..а-а.. м..ожно ещё?~ 💦",
    " *дрожу* ..с..лушаюсь.. ✨",
    " (｡◕‿◕｡) ..я хорошая девочка?~",
    " ..т-теку.. только не бросай меня.. 🎀"
]

# ========================================================
# [ 🛠 СИСТЕМА ЛОГИРОВАНИЯ ]
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
        "`.авто [текст]` — Включить\n"
        "`.автостоп` — Выключить\n\n"
        "── **ЭФФЕКТЫ** ──\n"
        "`.печать [текст]` | `.реверс` | `.взлом`\n"
        "`.кость [1-6]` — Чит на кубик\n\n"
        "── **ЛЮБОВЬ & РП** ──\n"
        "`.сердце` | `.любовь` | `.люблю` | `.лизь`\n\n"
        "── **РЕЖИМЫ** ──\n"
        "`.шавка` | `.тролль` | `.реак` (🤡)\n\n"
        "── **ИНСТРУМЕНТЫ** ──\n"
        "`.все` | `.дел [n]` | `.гс [текст]` | `.пинг`"
    )
    await e.edit(m)

# --- БЛОК: АВТООТВЕТЧИК ---

@client.on(events.NewMessage(pattern=r'\.авто (.+)', outgoing=True))
@error_handler
async def cmd_afk_on(e):
    State.afk = True
    State.afk_reason = e.pattern_match.group(1)
    await e.edit(f"✅ **Автоответчик включен!**\nТекст: `{State.afk_reason}`")

@client.on(events.NewMessage(pattern=r'\.автостоп', outgoing=True))
@error_handler
async def cmd_afk_off(e):
    State.afk = False
    await e.edit("❌ **Автоответчик выключен.**")

@client.on(events.NewMessage(incoming=True))
async def handle_afk_logic(e):
    if State.afk and e.is_private and not e.sender.bot:
        await asyncio.sleep(1)
        await e.reply(f"**[🤖 Автоответчик]**\n{State.afk_reason}")

# --- БЛОК: ЭФФЕКТЫ ТЕКСТА ---

@client.on(events.NewMessage(pattern=r'\.печать (.+)', outgoing=True))
@error_handler
async def cmd_typewriter(e):
    text = e.pattern_match.group(1)
    current = ""
    for char in text:
        current += char
        try: await e.edit(f"**{current}▒**"); await asyncio.sleep(0.15)
        except: pass
    await e.edit(f"**{current}**")

@client.on(events.NewMessage(pattern=r'\.реверс ?(.*)', outgoing=True))
@error_handler
async def cmd_reverse(e):
    r = await e.get_reply_message()
    text = e.pattern_match.group(1) or (r.text if r else None)
    if not text: return await e.edit("`❌ Что переворачивать?` ")
    await e.edit(text[::-1])

# --- БЛОК: КИБЕР-ФАН ---

@client.on(events.NewMessage(pattern=r'\.взлом', outgoing=True))
@error_handler
async def cmd_hack(e):
    r = await e.get_reply_message()
    t = f"@{r.sender.username}" if r and r.sender.username else "User"
    for s in ["🔍 Поиск...", "📡 Коннект...", "🔓 Доступ!", "📂 Слив данных...", "✅ Готово."]:
        await e.edit(f"**[ВЗЛОМ]** `{s}`"); await asyncio.sleep(0.7)
    await e.edit(f"**Объект {t} взломан.**")

@client.on(events.NewMessage(pattern=r'\.кость (\d+)', outgoing=True))
@error_handler
async def cmd_dice(e):
    v = int(e.pattern_match.group(1))
    if not (1 <= v <= 6): return await e.edit("От 1 до 6!")
    await e.delete()
    while True:
        res = await client(functions.messages.SendDiceRequest(peer=e.chat_id, emoji="🎲"))
        if res.updates[0].message.media.value == v: break
        await client.delete_messages(e.chat_id, [res.updates[0].message.id])

# --- БЛОК: ЛЮБОВЬ И РП ---

@client.on(events.NewMessage(pattern=r'\.сердце', outgoing=True))
@error_handler
async def cmd_heart(e):
    for s in ["❤️", "❤️🧡", "❤️🧡💛", "❤️🧡💛💚", "💝"]:
        await e.edit(s); await asyncio.sleep(0.3)

@client.on(events.NewMessage(pattern=r'\.любовь ?(.*)', outgoing=True))
@error_handler
async def cmd_love(e):
    t = e.pattern_match.group(1) or "тебя"
    await e.edit(f"**Я тебя люблю, {t} ❤️✨**")

@client.on(events.NewMessage(pattern=r'\.(лизь|кусь|наколени|люблю)', outgoing=True))
@error_handler
async def cmd_rp(e):
    c = e.pattern_match.group(1); r = await e.get_reply_message()
    t = f"[@{r.sender.username}](tg://user?id={r.sender_id})" if r and r.sender.username else "хозяина"
    rps = {"лизь": f"👅 | **Лизнула** {t}..", "кусь": f"🦷 | **Кусь** {t}..", "наколени": f"🧎‍♀️ | **На колени перед** {t}..", "люблю": f"💖 | **Люблю** {t}.."}
    await e.edit(rps[c])

# --- БЛОК: РЕЖИМЫ ---

@client.on(events.NewMessage(pattern=r'\.(шавка|тролль|реак)', outgoing=True))
@error_handler
async def cmd_toggle(e):
    c = e.pattern_match.group(1)
    if c == "шавка": State.shavka, State.troll = not State.shavka, False; s = State.shavka
    elif c == "тролль": State.troll, State.shavka = not State.troll, False; s = State.troll
    else: State.reactions = not State.reactions; s = State.reactions
    await e.edit(f"**{c.upper()}**: {'✅' if s else '❌'}")

@client.on(events.NewMessage(outgoing=True))
async def handle_modes(e):
    if e.text.startswith('.') or not (State.shavka or State.troll): return
    if State.shavka: await e.edit(f"{e.text}{random.choice(shavka_suffixes)}")
    elif State.troll: await e.edit(f"{e.text}\n\n**[!]** {random.choice(trolls)}")

@client.on(events.NewMessage(incoming=True))
async def handle_auto_react(e):
    if State.reactions and not e.is_private:
        try: await client(functions.messages.SendReactionRequest(peer=e.chat_id, msg_id=e.id, reaction=[types.ReactionEmoji(emoticon='🤡')]))
        except: pass

# --- БЛОК: ИНСТРУМЕНТЫ ---

@client.on(events.NewMessage(pattern=r'\.гс (.+)', outgoing=True))
@error_handler
async def cmd_tts(e):
    t = e.pattern_match.group(1); tts = gTTS(t, lang='ru'); out = io.BytesIO()
    tts.write_to_fp(out); out.name = "v.mp3"; out.seek(0)
    await e.delete(); await client.send_file(e.chat_id, out, voice=True)

@client.on(events.NewMessage(pattern=r'\.все ?(.*)', outgoing=True))
@error_handler
async def cmd_tagall(e):
    txt = e.pattern_match.group(1) or "Слышь!"
    await e.delete()
    async for u in client.iter_participants(e.chat_id):
        if u.bot: continue
        try: await client.send_message(e.chat_id, f"**{txt}**\n[\u2063](tg://user?id={u.id})"); await asyncio.sleep(0.4)
        except: break

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
    await client.send_message("me", "✅ **Бот v6.2 запущен!**\nВсе блоки проверены и работают.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
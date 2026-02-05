import os, asyncio, random, requests, sys, io, importlib.util, traceback
from telethon import TelegramClient, events, functions, types
from dotenv import load_dotenv
from gtts import gTTS

# ==========================================
#              CONFIGURATION
# ==========================================
def setup_env():
    if not os.path.exists('.env'):
        print("🚀 First run! Setting up credentials...")
        api_id = input("Enter API_ID: ").strip()
        api_hash = input("Enter API_HASH: ").strip()
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

# ==========================================
#                DATA PACKS
# ==========================================
trolls = [
    "Твой дед в канаве медь доедает, а ты тут пишешь?",
    "Мать твою в ломбард сдал, за неё даже сотку не дали.",
    "Батя твой ушел за хлебом и стал админом гей-клуба.",
    "Я твою семейку в домино проиграл бомжам.",
    "Твоя родословная — это ошибка пьяного зоолога.",
    "Твой максимум — это чистить ботинки моему юзерботу.",
    "В твоей голове настолько пусто, что слышно эхо моих сообщений.",
    "Ты настолько жалок, что даже спам-фильтр тебя игнорирует."
]

shavka_suffixes = [
    " (⁄ ⁄•⁄ω⁄•⁄ ⁄) ..да, хозяин..~",
    " ..а-а.. м..ожно ещё?~ 💦",
    " *опустила взгляд* ..папочка.. ✨",
    " ..т-теку.. только не бросай меня.. 🎀",
    " ..г..отова на всё ради тебя..~",
    " *дрожу* ..с..лушаюсь.. ✨",
    " (｡◕‿◕｡) ..я хорошая девочка?~",
    " ..м-м.. как скажешь, любимый.. ✨",
    " ..п..ожалуйста, не злись на меня.. 🥺",
    " ..я.. я только твоя..~ 🎀",
    " *тихонько скулю* ..х..очу ещё.. ✨",
    " ..т..ы такой сильный..~ 💦",
    " ..сделаю всё, что попросишь.. ✨",
    " ..а-ах.. папочка, ты лучший..~ 🎀",
    " *покорно жду* ..м..не так плохо без тебя.. ✨",
    " (◡‿◡✿) ..твой маленький секрет..~",
    " ..н..аказывай меня чаще.. 💦",
    " ..б..уду послушной, обещаю.. ✨",
    " ..м-м-м.. так приятно..~ 🎀",
    " *лижу руку* ..м..ожно мне ещё внимания?.. ✨",
    " ..я.. я вся горю..~ 💦",
    " (๑•́ ₃ •̀๑) ..не игнорь меня, хозяин.. 🎀",
    " ..у..же теку от твоего голоса..~ 💦",
    " *прижалась к ноге* ..н..е уходи.. ✨",
    " ..х..озяин, я соскучилась.. 🐾",
    " ..т..олько не бей, я буду хорошей.. 🥺",
    " ..а-а.. я вся твоя, делай что хочешь.. 💦"
]

# ==========================================
#           SYSTEM & LOGGING
# ==========================================
async def send_log(error_text, cmd_name="SYSTEM"):
    try:
        log_msg = f"❌ **[ ERROR LOG ]**\n**Cmd:** `{cmd_name}`\n`{error_text[-3000:]}`"
        await client.send_message("me", log_msg)
    except: pass

def error_handler(func):
    async def wrapper(e):
        try: await func(e)
        except Exception: await send_log(traceback.format_exc(), func.__name__)
    return wrapper

# ==========================================
#                CORE COMMANDS
# ==========================================

@client.on(events.NewMessage(pattern=r'\.хелп', outgoing=True))
@error_handler
async def cmd_help(e):
    m = (
        "**[ 🧬 Stupid Userbot v5.9 ]**\n\n"
        "── **CYBER & FUN** ──\n"
        "`.hack` — Взлом (reply) | `.кубик [1-6]`\n"
        "`.тайп [txt]` | `.инверт`\n\n"
        "── **LOVE & RP** ──\n"
        "`.heart` | `.love [txt]` | `.люблю` (reply)\n"
        "`.лизь` | `.кусь` | `.наколени` | `.лапу`\n\n"
        "── **MODES** ──\n"
        "`.шавка` (ULTRA PACK) | `.тролль` | `.реак` (🤡)\n\n"
        "── **TOOLS** ──\n"
        "`.все` | `.спам [n] [txt]` | `.дел [n]`\n"
        "`.гс [txt]` | `.вфайл` | `.инфо` | `.пинг`\n\n"
        "── **SYSTEM** ──\n"
        "`.load` — Модуль .py"
    )
    await e.edit(m)

# --- MEDIA & FUN ---
@client.on(events.NewMessage(pattern=r'\.hack', outgoing=True))
@error_handler
async def cmd_hack(e):
    r = await e.get_reply_message()
    target = f"@{r.sender.username}" if r and r.sender.username else "User"
    steps = ["🔍 Searching...", "📡 Connecting...", "🔑 BruteForce...", "🔓 Access Granted!", "📂 Downloading...", "✅ Done."]
    for s in steps:
        await e.edit(f"**[ATTACK]** `{s}`"); await asyncio.sleep(0.7)
    await e.edit(f"**Target {target} compromised.**")

@client.on(events.NewMessage(pattern=r'\.кубик (\d+)', outgoing=True))
@error_handler
async def cmd_dice(e):
    v = int(e.pattern_match.group(1))
    if not (1 <= v <= 6): return
    await e.delete()
    while True:
        m = await client.send_message(e.chat_id, file=types.InputMediaDice(emoji="🎲"))
        if m.media.value == v: break
        await m.delete()

@client.on(events.NewMessage(pattern=r'\.heart', outgoing=True))
@error_handler
async def cmd_heart(e):
    for s in ["❤️", "❤️🧡", "❤️🧡💛", "❤️🧡💛💚", "💝"]:
        await e.edit(s); await asyncio.sleep(0.3)

@client.on(events.NewMessage(pattern=r'\.(лизь|кусь|наколени|люблю|лапу|скулить)', outgoing=True))
@error_handler
async def cmd_rp(e):
    c = e.pattern_match.group(1); r = await e.get_reply_message()
    t = f"[@{r.sender.username}](tg://user?id={r.sender_id})" if r and r.sender.username else "хозяина"
    rps = {
        "лизь": f"👅 | **Аккуратно лизнула** {t}..~",
        "кусь": f"🦷 | **Слегка прикусила** {t} за ушко..",
        "наколени": f"🧎‍♀️ | **Встала на колени** перед {t}..",
        "люблю": f"💖 | **Зацеловала** {t} до покраснения..",
        "лапу": f"🐾 | **Протянула лапку** {t}..",
        "скулить": f"🥺 | **Тихо скулит**, глядя на {t}.."
    }
    await e.edit(rps[c])

# --- MODES & LOGIC ---
@client.on(events.NewMessage(pattern=r'\.(шавка|тролль|реак)', outgoing=True))
@error_handler
async def cmd_toggle(e):
    c = e.pattern_match.group(1)
    if c == "шавка": State.shavka, State.troll = not State.shavka, False; s = State.shavka
    elif c == "тролль": State.troll, State.shavka = not State.troll, False; s = State.troll
    else: State.reactions = not State.reactions; s = State.reactions
    await e.edit(f"**{c.upper()}**: {'✅ ON' if s else '❌ OFF'}")

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

# --- UTILS ---
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
        try:
            await client.send_message(e.chat_id, f"**{txt}**\n[\u2063](tg://user?id={u.id})")
            await asyncio.sleep(0.4)
        except: break

@client.on(events.NewMessage(pattern=r'\.дел (\d+)', outgoing=True))
@error_handler
async def cmd_del(e):
    n = int(e.pattern_match.group(1)); await e.delete()
    async for m in client.iter_messages(e.chat_id, limit=n, from_user='me'): await m.delete()

@client.on(events.NewMessage(pattern=r'\.load', outgoing=True))
@error_handler
async def cmd_load(e):
    r = await e.get_reply_message()
    if r and r.file:
        await r.download_media(MOD_PATH)
        await e.edit("📦 Модуль залит. Рестарт..."); os.execl(sys.executable, sys.executable, *sys.argv)

@client.on(events.NewMessage(pattern=r'\.пинг', outgoing=True))
async def cmd_ping(e): await e.edit("`PING: 0.01ms` ⚡")

# ==========================================
#                   BOOT
# ==========================================
async def main():
    await client.start()
    await client.send_message("me", "✅ **Stupid Userbot v5.9 Started!**\nЛогирование активно.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
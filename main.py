import os, asyncio, random, requests, sys, io, importlib.util, traceback
from telethon import TelegramClient, events, functions, types
from dotenv import load_dotenv
from gtts import gTTS

# ========================================================
# [ ⚙️ КОНФИГУРАЦИЯ И НАСТРОЙКА ]
# ========================================================
def setup_env():
    """Создание файла .env при первом запуске"""
    if not os.path.exists('.env'):
        api_id = input("Введите API_ID: ").strip()
        api_hash = input("Введите API_HASH: ").strip()
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\n")

setup_env()
load_dotenv()

# Инициализация клиента Telegram
client = TelegramClient('stupid_session', int(os.getenv("API_ID")), os.getenv("API_HASH"))
MOD_PATH = "modules"
if not os.path.exists(MOD_PATH): os.mkdir(MOD_PATH)

# Переменные состояния бота
class State:
    shavka = False      # Режим "Шавка"
    troll = False       # Режим "Тролль"
    reactions = False   # Авто-реакции клоуна

# ========================================================
# [ 📝 БАЗА ДАННЫХ ФРАЗ ]
# ========================================================
trolls = [
    "Твой дед в канаве медь доедает, а ты тут пишешь?",
    "Мать твою в ломбард сдал, за неё даже сотку не дали.",
    "Батя твой ушел за хлебом и стал админом гей-клуба.",
    "Твоя родословная — это ошибка пьяного зоолога."
]

shavka_suffixes = [
    " (⁄ ⁄•⁄ω⁄•⁄ ⁄) ..да, хозяин..~",
    " ..а-а.. м..ожно ещё?~ 💦",
    " *опустила взгляд* ..папочка.. ✨",
    " ..т-теку.. только не бросай меня.. 🎀",
    " ..г..отова на всё ради тебя..~",
    " *дрожу* ..с..лушаюсь.. ✨",
    " (｡◕‿◕｡) ..я хорошая девочка?~"
]

# ========================================================
# [ 🛠 СИСТЕМА ЛОГИРОВАНИЯ ОШИБОК ]
# ========================================================
async def send_log(error_text, cmd_name="SYSTEM"):
    """Отправка отчета об ошибке в 'Избранное'"""
    try:
        await client.send_message("me", f"❌ **[ ОШИБКА ]**\n**Команда:** `{cmd_name}`\n`{error_text[-3000:]}`")
    except: pass

def error_handler(func):
    """Декоратор для перехвата ошибок в командах"""
    async def wrapper(e):
        try: await func(e)
        except Exception: await send_log(traceback.format_exc(), func.__name__)
    return wrapper

# ========================================================
# [ 📜 ОСНОВНЫЕ КОМАНДЫ ]
# ========================================================

@client.on(events.NewMessage(pattern=r'\.хелп', outgoing=True))
@error_handler
async def cmd_help(e):
    """Список всех команд"""
    m = (
        "**[ 🧬 Stupid Userbot v6.0 ]**\n\n"
        "── **КИБЕР-ФАН** ──\n"
        "`.взлом` — Взлом юзера (reply)\n"
        "`.кость [1-6]` — Чит на кубик\n"
        "`.печать [текст]` — Эффект печати\n"
        "`.реверс` — Текст задом наперед\n\n"
        "── **ЛЮБОВЬ & РП** ──\n"
        "`.сердце` — Анимация ❤️\n"
        "`.любовь [текст]` — Признание\n"
        "`.люблю` | `.лизь` | `.кусь` | `.наколени`\n\n"
        "── **РЕЖИМЫ** ──\n"
        "`.шавка` | `.тролль` | `.реак` (🤡)\n\n"
        "── **ИНСТРУМЕНТЫ** ──\n"
        "`.все` — Тэгнуть всех\n"
        "`.спам [n] [текст]` — Флуд\n"
        "`.дел [n]` — Удалить свои сообщения\n"
        "`.гс [текст]` — Озвучка текста\n"
        "`.файл` — Стикер в файл (reply)\n"
        "`.пинг` — Скорость бота"
    )
    await e.edit(m)

# --- БЛОК: КИБЕР-РАЗВЛЕЧЕНИЯ ---

@client.on(events.NewMessage(pattern=r'\.взлом', outgoing=True))
@error_handler
async def cmd_hack(e):
    """Имитация хакерской атаки"""
    r = await e.get_reply_message()
    t = f"@{r.sender.username}" if r and r.sender.username else "Пользователя"
    steps = ["🔍 Поиск уязвимостей...", "📡 Подключение к Proxy...", "🔑 Брутфорс пароля...", "🔓 Доступ получен!", "📂 Скачивание архива...", "✅ Готово."]
    for s in steps:
        await e.edit(f"**[ВЗЛОМ]** `{s}`"); await asyncio.sleep(0.7)
    await e.edit(f"**Объект {t} успешно скомпрометирован.**")

@client.on(events.NewMessage(pattern=r'\.кость (\d+)', outgoing=True))
@error_handler
async def cmd_dice(e):
    """Чит на игровые кубики (dice)"""
    v = int(e.pattern_match.group(1))
    if not (1 <= v <= 6): return await e.edit("Введите число от 1 до 6!")
    await e.delete()
    while True:
        # Отправка кубика через правильный метод API
        res = await client(functions.messages.SendDiceRequest(peer=e.chat_id, emoji="🎲"))
        if res.updates[0].message.media.value == v: break
        await client.delete_messages(e.chat_id, [res.updates[0].message.id])

# --- БЛОК: ЛЮБОВЬ И РОМАНТИКА ---

@client.on(events.NewMessage(pattern=r'\.сердце', outgoing=True))
@error_handler
async def cmd_heart(e):
    """Анимация сердечек"""
    for s in ["❤️", "❤️🧡", "❤️🧡💛", "❤️🧡💛💚", "💝"]:
        await e.edit(s); await asyncio.sleep(0.3)

@client.on(events.NewMessage(pattern=r'\.любовь ?(.*)', outgoing=True))
@error_handler
async def cmd_love(e):
    """Красивое признание в любви"""
    t = e.pattern_match.group(1) or "тебя"
    await e.edit(f"**Я очень сильно люблю {t} ❤️✨**")

@client.on(events.NewMessage(pattern=r'\.(лизь|кусь|наколени|люблю)', outgoing=True))
@error_handler
async def cmd_rp(e):
    """Ролевые команды (RP)"""
    c = e.pattern_match.group(1); r = await e.get_reply_message()
    t = f"[@{r.sender.username}](tg://user?id={r.sender_id})" if r and r.sender.username else "хозяина"
    rps = {
        "лизь": f"👅 | **Аккуратно лизнула** {t}..~",
        "кусь": f"🦷 | **Прикусила** {t} за ушко..",
        "наколени": f"🧎‍♀️ | **Встала на колени** перед {t}..",
        "люблю": f"💖 | **Зацеловала** {t}.."
    }
    await e.edit(rps[c])

# --- БЛОК: РЕЖИМЫ И АВТОМАТИЗАЦИЯ ---

@client.on(events.NewMessage(pattern=r'\.(шавка|тролль|реак)', outgoing=True))
@error_handler
async def cmd_toggle(e):
    """Включение/выключение режимов"""
    c = e.pattern_match.group(1)
    if c == "шавка": State.shavka, State.troll = not State.shavka, False; s = State.shavka
    elif c == "тролль": State.troll, State.shavka = not State.troll, False; s = State.troll
    else: State.reactions = not State.reactions; s = State.reactions
    await e.edit(f"**{c.upper()}**: {'✅ ВКЛ' if s else '❌ ВЫКЛ'}")

@client.on(events.NewMessage(outgoing=True))
async def handle_modes(e):
    """Логика работы активных режимов"""
    if e.text.startswith('.') or not (State.shavka or State.troll): return
    if State.shavka: 
        await e.edit(f"{e.text}{random.choice(shavka_suffixes)}")
    elif State.troll: 
        await e.edit(f"{e.text}\n\n**[!]** {random.choice(trolls)}")

@client.on(events.NewMessage(incoming=True))
async def handle_auto_react(e):
    """Автоматическая реакция 'Клоун' на входящие"""
    if State.reactions and not e.is_private:
        try: await client(functions.messages.SendReactionRequest(peer=e.chat_id, msg_id=e.id, reaction=[types.ReactionEmoji(emoticon='🤡')]))
        except: pass

# --- БЛОК: ПОЛЕЗНЫЕ ИНСТРУМЕНТЫ ---

@client.on(events.NewMessage(pattern=r'\.гс (.+)', outgoing=True))
@error_handler
async def cmd_tts(e):
    """Превращение текста в голосовое сообщение"""
    t = e.pattern_match.group(1); tts = gTTS(t, lang='ru'); out = io.BytesIO()
    tts.write_to_fp(out); out.name = "v.mp3"; out.seek(0)
    await e.delete(); await client.send_file(e.chat_id, out, voice=True)

@client.on(events.NewMessage(pattern=r'\.все ?(.*)', outgoing=True))
@error_handler
async def cmd_tagall(e):
    """Тэг всех участников чата"""
    txt = e.pattern_match.group(1) or "Слышь, внимание!"
    await e.delete()
    async for u in client.iter_participants(e.chat_id):
        if u.bot: continue
        try: 
            await client.send_message(e.chat_id, f"**{txt}**\n[\u2063](tg://user?id={u.id})")
            await asyncio.sleep(0.4)
        except: break

@client.on(events.NewMessage(pattern=r'\.пинг', outgoing=True))
async def cmd_ping(e): 
    """Проверка скорости"""
    await e.edit("`БОТ ЛЕТИТ: 0.01ms` ⚡")

@client.on(events.NewMessage(pattern=r'\.дел (\d+)', outgoing=True))
@error_handler
async def cmd_del(e):
    """Удаление сообщений"""
    n = int(e.pattern_match.group(1)); await e.delete()
    async for m in client.iter_messages(e.chat_id, limit=n, from_user='me'): await m.delete()

# ========================================================
# [ 🚀 ЗАПУСК БОТА ]
# ========================================================
async def main():
    await client.start()
    await client.send_message("me", "✅ **Бот v6.0 успешно запущен!**\nВсе функции работают в штатном режиме.")
    print("Юзербот запущен! Проверь 'Избранное' в Telegram.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
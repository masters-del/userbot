import os, asyncio, random, sys, io
from telethon import TelegramClient, events, functions, types, errors
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import UserAlreadyParticipantError, FloodWaitError
from dotenv import load_dotenv
from gtts import gTTS
import google.generativeai as genai
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

# Очередь задач и потоки для ИИ
task_queue = asyncio.Queue()
_executor = ThreadPoolExecutor(max_workers=5)
me = None

# Твой ключ Gemini (вшит)
BUILT_IN_AI_KEY = "AIzaSyD2MnB0xP7gslNIeHalUEW9DAm1xNcHKKc"

def setup_env():
    if not os.path.exists('.env'):
        api_id = input("Введите API_ID: ").strip()
        api_hash = input("Введите API_HASH: ").strip()
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\n")

setup_env()
load_dotenv()

api_id, api_hash = os.getenv("API_ID"), os.getenv("API_HASH")
client = TelegramClient('stupid_session', int(api_id), api_hash)
genai.configure(api_key=BUILT_IN_AI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

class State:
    shavka = False
    ai_help = False
    afk = False
    afk_reason = ""

# --- SAFE SEND ---
async def safe_send(entity, message):
    for _ in range(5): 
        try:
            await client.send_message(entity, message)
            await asyncio.sleep(random.uniform(1.5, 3.5))
            return True
        except FloodWaitError as f:
            await asyncio.sleep(f.seconds + 2)
        except Exception: return False
    return False

# --- WORKER ---
async def worker():
    while True:
        task = await task_queue.get()
        try: await task()
        except Exception: pass
        await asyncio.sleep(random.uniform(2, 5))
        task_queue.task_done()

# ========================================================
# [ ❤️ ЛЮБОВНЫЙ БЛОК ]
# ========================================================

@client.on(events.NewMessage(pattern=r'\.сердце', outgoing=True))
async def cmd_heart_anim(e):
    # Анимация пульсирующего сердца
    hearts = ["❤️", "💖", "💗", "💓", "💝", "💞", "💟", "❤️"]
    for h in hearts:
        await e.edit(h)
        await asyncio.sleep(0.5)
    await e.edit("❤️ **Люблю тебя до луны и обратно!** ❤️")

@client.on(events.NewMessage(pattern=r'\.love', outgoing=True))
async def cmd_love_text(e):
    # Красивая анимация текста
    msg = "Я тебя люблю"
    out = ""
    for char in msg:
        out += char
        await e.edit(f"✨ {out} ✨")
        await asyncio.sleep(0.3)
    await e.edit(f"❤️ **{msg}** ❤️")

@client.on(events.NewMessage(pattern=r'\.признание', outgoing=True))
async def cmd_confess(e):
    # ИИ пишет глубокое и красивое признание
    await e.edit("💌 **Пишу самое красивое признание...**")
    try:
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(_executor, lambda: ai_model.generate_content("Напиши очень трогательное, глубокое и короткое признание в любви для девушки. Используй метафоры про космос или океан. Без пошлости."))
        if res and res.text:
            await e.edit(f"📜 **Послание для тебя:**\n\n{res.text.strip()}\n\n❤️✨")
    except:
        await e.edit("❤️ Ты — мой весь мир.")

# ========================================================
# [ 📜 ОСТАЛЬНЫЕ КОМАНДЫ (v9.2 БАЗА) ]
# ========================================================

@client.on(events.NewMessage(pattern=r'\.ai (.+)', outgoing=True))
async def cmd_ai(e):
    await e.edit("🤔 **ИИ анализирует...**")
    try:
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(_executor, lambda: ai_model.generate_content(e.pattern_match.group(1)))
        if res and res.text: await e.edit(f"🤖 **AI:**\n\n{res.text.strip()[:4000]}")
    except: await e.edit("❌ Ошибка.")

@client.on(events.NewMessage(pattern=r'\.рейд (\d+) (.+)', outgoing=True))
async def cmd_raid(e):
    count, text = min(int(e.pattern_match.group(1)), 30), e.pattern_match.group(2)
    await e.delete()
    async def raid_task():
        for _ in range(count): await safe_send(e.chat_id, text)
    await task_queue.put(raid_task)

@client.on(events.NewMessage(pattern=r'\.рассылка (.+)', outgoing=True))
async def cmd_broadcast(e):
    msg = e.pattern_match.group(1)
    try:
        async with client.conversation("me", timeout=60) as conv:
            await conv.send_message("📝 **Ссылки:**")
            r = await conv.get_response()
            links = [l.strip() for l in r.text.split('\n') if l.strip()]
    except: return await e.edit("❌ Отмена.")
    await e.edit("🚀 **В очереди...**")
    async def broadcast_task():
        for link in links:
            try:
                target = link.replace("https://t.me/", "").replace("@", "").split('/')[0]
                try: await client(JoinChannelRequest(target))
                except UserAlreadyParticipantError: pass
                except: continue
                await asyncio.sleep(random.uniform(15, 30))
                await safe_send(target, msg)
            except: continue
    await task_queue.put(broadcast_task)

@client.on(events.NewMessage(pattern=r'\.пинг', outgoing=True))
async def cmd_p(e): await e.edit("`v9.3 LOVELY ACTIVE ❤️`")

@client.on(events.NewMessage(pattern=r'\.шавка', outgoing=True))
async def cmd_sh(e):
    State.shavka = not State.shavka
    await e.edit(f"🐶 Шавка: {'✅' if State.shavka else '❌'}")

@client.on(events.NewMessage(outgoing=True))
async def sh_l(e):
    if State.shavka and e.text and not e.text.startswith('.'):
        await e.edit(f"{e.text} ~ня", parse_mode=None)

async def main():
    global me
    try:
        await client.start()
        me = await client.get_me()
        asyncio.create_task(worker())
        print(Fore.MAGENTA + f"[+] v9.3 Lovely запущен! Любимая, я в сети.")
        await client.run_until_disconnected()
    except Exception as ex: print(ex)

if __name__ == '__main__':
    client.loop.run_until_complete(main())
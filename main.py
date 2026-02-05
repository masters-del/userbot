import os, asyncio, random, requests
from telethon import TelegramClient, events, functions, types
from dotenv import load_dotenv

def _setup():
    if not os.path.exists('.env'):
        aid = input("ID: ").strip()
        ah = input("HASH: ").strip()
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f"API_ID={aid}\nAPI_HASH={ah}\n")

_setup()
load_dotenv()

client = TelegramClient('anon', int(os.getenv("API_ID")), os.getenv("API_HASH"))

st = {"sh": False, "tr": False, "auto": None, "rk": False}

trolls = [
    "Твой дед в канаве медь доедает, а ты тут пишешь?",
    "Мать твою в ломбард сдал, за неё даже сотку не дали.",
    "Батя твой ушел за хлебом и стал админом гей-клуба.",
    "Я твою семейку в домино проиграл бомжам.",
    "Твоя родословная — это ошибка пьяного зоолога."
]

@client.on(events.NewMessage(pattern=r'\.хелп', outgoing=True))
async def h(e):
    m = (
        "**[ Custom Userbot by Stupid ]**\n\n"
        "── **Modes** ──\n"
        "`.шавка` | `.тролль` | `.реак` (🤡)\n\n"
        "── **Abuse** ──\n"
        "`.все [txt]` — Tag all⚡\n"
        "`.спам [n] [txt]` | `.дел [n]`\n\n"
        "── **Info/Stolen** ──\n"
        "`.докс` | `.тыбзи` (reply)\n\n"
        "── **Utils** ──\n"
        "`.авто [txt]` | `.автовыкл`\n"
        "`.пинг` | `.погода [city]`"
    )
    await e.edit(m)

@client.on(events.NewMessage(pattern=r'\.все ?(.*)', outgoing=True))
async def tagall(e):
    msg = e.pattern_match.group(1) or "Внимание!"
    await e.delete()
    async for u in client.iter_participants(e.chat_id):
        if not st: break
        if u.bot: continue
        try:
            await client.send_message(e.chat_id, f"**{msg}**\n[\u2063](tg://user?id={u.id})")
            await asyncio.sleep(0.3)
        except: pass

@client.on(events.NewMessage(pattern=r'\.дел (\d+)', outgoing=True))
async def d(e):
    n = int(e.pattern_match.group(1))
    await e.delete()
    async for m in client.iter_messages(e.chat_id, limit=n, from_user='me'):
        await m.delete()

@client.on(events.NewMessage(pattern=r'\.тыбзи', outgoing=True))
async def g(e):
    r = await e.get_reply_message()
    if r:
        await e.delete()
        await client.send_message('me', r)

@client.on(events.NewMessage(pattern=r'\.докс', outgoing=True))
async def dx(e):
    r = await e.get_reply_message()
    if not r: return await e.edit("Reply needed")
    u = await client.get_entity(r.sender_id)
    c = await client(functions.messages.GetCommonChatsRequest(user_id=r.sender_id, max_id=0, limit=100))
    await e.edit(f"**DOCS:**\nID: `{u.id}`\nName: {u.first_name}\nCommon: {c.count}")

@client.on(events.NewMessage(pattern=r'\.реак', outgoing=True))
async def rk(e):
    st["rk"] = not st["rk"]
    await e.edit(f"**Reactions**: {'ON' if st['rk'] else 'OFF'}")

@client.on(events.NewMessage(incoming=True))
async def react_h(e):
    if st["rk"] and not e.is_private:
        try:
            await client(functions.messages.SendReactionRequest(
                peer=e.chat_id, msg_id=e.id, 
                reaction=[types.ReactionEmoji(emoticon='🤡')]
            ))
        except: pass

@client.on(events.NewMessage(pattern=r'\.спам (\d+) (.+)', outgoing=True))
async def s(e):
    n, t = int(e.pattern_match.group(1)), e.pattern_match.group(2)
    await e.delete()
    for _ in range(n):
        await e.respond(t)
        await asyncio.sleep(0.08)

@client.on(events.NewMessage(pattern=r'\.(шавка|тролль)', outgoing=True))
async def md(e):
    cmd = e.pattern_match.group(1)
    if cmd == "шавка": st["sh"], st["tr"] = not st["sh"], False
    else: st["tr"], st["sh"] = not st["tr"], False
    await e.edit(f"**{cmd.upper()}**: {'ON' if st['sh'] or st['tr'] else 'OFF'}")

@client.on(events.NewMessage(outgoing=True))
async def h_out(e):
    if e.text.startswith('.') or not (st["sh"] or st["tr"]): return
    if st["sh"]:
        await e.edit(f"{e.text}{random.choice([' а-а.. д..а?~ 💦', ' папочка.. ✨', ' м-м..~'])}")
    elif st["tr"]:
        await e.edit(f"{e.text}\n\n**[!]** {random.choice(trolls)}")

@client.on(events.NewMessage(pattern=r'\.авто (.+)', outgoing=True))
async def a_on(e):
    st["auto"] = e.pattern_match.group(1)
    await e.edit(f"**Auto**: {st['auto']}")

@client.on(events.NewMessage(pattern=r'\.автовыкл', outgoing=True))
async def a_off(e):
    st["auto"] = None
    await e.edit("**Auto OFF**")

@client.on(events.NewMessage(incoming=True))
async def h_in(e):
    if st["auto"] and e.is_private: await e.reply(st["auto"])

@client.on(events.NewMessage(pattern=r'\.пинг', outgoing=True))
async def p(e): await e.edit("`PONG`")

@client.on(events.NewMessage(pattern=r'\.погода (.+)', outgoing=True))
async def w(e):
    r = requests.get(f"https://wttr.in/{e.pattern_match.group(1)}?format=3")
    await e.edit(r.text if r.status_code == 200 else "Err")

@client.on(events.NewMessage(pattern=r'\.рассылка (-?\d+) (.+)', outgoing=True))
async def b(e):
    try:
        await client.send_message(int(e.pattern_match.group(1)), e.pattern_match.group(2))
        await e.edit("OK")
    except: await e.edit("FAIL")

if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
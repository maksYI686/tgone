import os
import asyncio
from telethon import TelegramClient
from feedgen.feed import FeedGenerator
from binascii import unhexlify
from datetime import datetime

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session_hex = os.environ.get("TG_SESSION_HEX", "")

print("Starting script...")  # Лог для Actions

if session_hex:
    with open("session_user.session", "wb") as f:
        f.write(unhexlify(session_hex))
    print("Session loaded from hex.")
else:
    print("No session hex — will try to auth (but needs phone/code, skip for now).")

client = TelegramClient("session_user", api_id, api_hash)
CHANNEL = "news_cryptod"

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Logged in as: {me.username or me.first_name}")  # Проверка авторизации

    fg = FeedGenerator()
    fg.title("Crypto News Mirror")
    fg.link(href="https://maksyI686.github.io/tgone/rss.xml", rel="self")
    fg.description("Автоматический RSS из @news_cryptod")
    fg.language("ru")
    fg.lastBuildDate(datetime.now())

    message_count = 0
    async for msg in client.iter_messages(CHANNEL, limit=50):
        if not msg.message:
            continue
        message_count += 1
        fe = fg.add_entry()
        fe.id(f"https://t.me/{CHANNEL}/{msg.id}")
        title = msg.message.split('\n', 1)[0][:120] + "..." if len(msg.message.split('\n', 1)[0]) > 120 else msg.message.split('\n', 1)[0]
        fe.title(title)
        fe.link(href=f"https://t.me/{CHANNEL}/{msg.id}")
        fe.description(msg.message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        fe.pubDate(msg.date)
        print(f"Added message {message_count}: {title[:50]}...")  # Лог

    fg.rss_file("rss.xml", pretty=True)
    print(f"RSS generated with {message_count} entries.")

    await client.disconnect()

asyncio.run(main())

import os
import asyncio
from telethon import TelegramClient
from feedgen.feed import FeedGenerator
from binascii import unhexlify

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session_hex = os.environ.get("TG_SESSION_HEX", "")

# Если сессия уже есть — используем её, если нет — создаём из hex
if session_hex:
    with open("session_user.session", "wb") as f:
        f.write(unhexlify(session_hex))

client = TelegramClient("session_user", api_id, api_hash)
CHANNEL = "news_cryptod"  # можно вынести в env, если нужно несколько каналов

async def main():
    await client.start()
    fg = FeedGenerator()
    fg.title("Crypto News Mirror")
    fg.link(href="https://maksy1686.github.io/НАЗВАНИЕ_РЕПО/rss.xml", rel="self")
    fg.description("Автоматическая RSS-лента из Telegram-канала @news_cryptod")
    fg.language("ru")

    async for msg in client.iter_messages(CHANNEL, limit=50):
        if not msg.message:
            continue
        fe = fg.add_entry(order='append')  # новые сверху
        fe.id(f"t.me/{CHANNEL}/{msg.id}")
        fe.title(msg.message.split("\n")[0][:100])
        fe.link(href=f"https://t.me/{CHANNEL}/{msg.id}")
        fe.description(msg.message.replace("&", "&amp;"))  # фикс XML-ошибок
        fe.pubDate(msg.date)

    fg.rss_file("rss.xml", pretty=True)
    print("RSS успешно обновлён, записей:", len(fg.entry()))

asyncio.run(client.loop.run_until_complete(main()))

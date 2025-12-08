import os
from telethon import TelegramClient
from feedgen.feed import FeedGenerator
from binascii import unhexlify

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]

hexdata = os.environ.get("TG_SESSION_HEX","")
open("session_user","wb").write(unhexlify(hexdata))

client = TelegramClient("session_user", api_id, api_hash)
CHANNEL = "news_cryptod"

async def main():
    await client.start()
    fg = FeedGenerator()
    fg.title("Crypto News Mirror")
    fg.link(href="rss.xml")
    fg.description("Auto Telegram RSS feed")

    async for msg in client.iter_messages(CHANNEL, limit=20):
        if msg.message:
            fe = fg.add_entry()
            fe.id(str(msg.id))
            fe.title(msg.message[:40])
            fe.link(href=f"https://t.me/{CHANNEL}/{msg.id}")
            fe.description(msg.message or "")

    fg.rss_file("rss.xml")

with client:
    client.loop.run_until_complete(main())

import os
import asyncio
from datetime import datetime, timezone
from telethon import TelegramClient
from feedgen.feed import FeedGenerator

print("=== RSS GENERATOR STARTED ===")

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]

client = TelegramClient("session_user", api_id, api_hash)
CHANNEL = "news_cryptod"

async def main():
    print("Connecting to Telegram...")
    await client.start()
    me = await client.get_me()
    print(f"Logged in as: {me.first_name} (@{me.username or 'no username'})")

    fg = FeedGenerator()
    fg.title("Crypto News Mirror")
    fg.description("Автоматическая RSS-лента из @news_cryptod")
    fg.link(href="https://maksyI686.github.io/tgone/rss.xml", rel="self")
    fg.language("ru")
    fg.lastBuildDate(datetime.now(timezone.utc))

    count = 0
    async for message in client.iter_messages(CHANNEL, limit=50):
        if not message.message:
            continue
        count += 1
        entry = fg.add_entry(order="prepend")
        entry.id(f"https://t.me/{CHANNEL}/{message.id}")
        title = message.message.split("\n", 1)[0][:100]
        if len(message.message.split("\n", 1)[0]) > 100:
            title += "..."
        entry.title(title)
        entry.link(href=f"https://t.me/{CHANNEL}/{message.id}")
        entry.description(message.message.replace("&", "&").replace("<", "<").replace(">", ">"))
        entry.pubDate(message.date.replace(tzinfo=timezone.utc))

    fg.rss_file("rss.xml", pretty=True)
    print(f"RSS created: {count} entries, {os.path.getsize('rss.xml')} bytes")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

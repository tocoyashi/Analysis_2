"""
Channel Discovery Bot
Discovers all channels where the bot is an admin and saves them to channels.json
Run this manually or via workflow_dispatch to update the channel list.
"""

import os
import json
import logging
import asyncio
from telegram import Bot

BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def load_existing_channels():
    """Load existing channels from channels.json"""
    try:
        with open('channels.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return set(data.get('channels', []))
    except Exception:
        return set()


def save_channels(channels):
    """Save channels to channels.json"""
    data = {
        'channels': sorted(list(channels)),
        'last_updated': asyncio.get_event_loop().time()
    }
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(channels)} channels to channels.json")


async def discover_channels():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN missing!")
        return

    bot = Bot(token=BOT_TOKEN)

    # Get existing channels
    existing = load_existing_channels()
    logger.info(f"Found {len(existing)} existing channels")

    # Get bot info
    me = await bot.get_me()
    bot_id = me.id
    logger.info(f"Bot ID: {bot_id} (@{me.username})")

    # Discover new channels from recent updates
    # This catches when bot was added to channels
    new_channels = set()
    try:
        updates = await bot.get_updates(limit=100, timeout=10)
        for update in updates:
            # Check my_chat_member updates (bot added/removed from chat)
            if update.my_chat_member:
                chat = update.my_chat_member.chat
                if chat.type == 'channel':
                    new_id = str(chat.id)
                    status = update.my_chat_member.new_chat_member.status
                    if status in ['administrator', 'member']:
                        new_channels.add(new_id)
                        logger.info(f"Found channel from update: {chat.title} ({new_id})")
                    elif status in ['left', 'kicked'] and new_id in existing:
                        existing.discard(new_id)
                        logger.info(f"Removed channel: {chat.title} ({new_id})")
    except Exception as e:
        logger.warning(f"Could not get updates: {e}")

    # Also try to verify admin status for existing channels
    verified = set()
    for channel_id in existing | new_channels:
        try:
            admins = await bot.get_chat_administrators(chat_id=int(channel_id))
            is_admin = any(admin.user.id == bot_id for admin in admins)
            if is_admin:
                verified.add(channel_id)
                logger.info(f"Verified admin in: {channel_id}")
            else:
                logger.warning(f"Bot is NOT admin in: {channel_id}")
        except Exception as e:
            logger.warning(f"Could not verify {channel_id}: {e}")
            # Keep it if it was already in the list (might be temporary error)
            if channel_id in existing:
                verified.add(channel_id)

    all_channels = verified
    save_channels(all_channels)
    logger.info(f"Total active channels: {len(all_channels)}")


if __name__ == '__main__':
    asyncio.run(discover_channels())

# -*- coding: utf-8 -*-
from pyrogram.errors import FloodWait, PeerIdInvalid, ChannelInvalid
from database import chat_table
from logs.logger import logger
from pyrogram import Client
from asyncio import sleep

## LOCAL CONFIG
archive_batch_size = 10
archive_sleep = 5
delete_sleep = 5


async def delete_chats(client: Client) -> None:
    """Удаление чатов со сном"""
    chat_data = [ch for ch in chat_table.get_all_data() if ch.is_leave]

    for chat in chat_data:
        try:
            if chat.chat_type == "private":
                await client.delete_chat_history(chat_id=chat.chat_id, revoke=True)
                logger.success(f"[+] Deleted private: {chat.chat_id} {chat.chat_name}")

            else:
                await client.leave_chat(chat_id=int(f"-100{chat.chat_id}"))
                logger.success(f"[+] Left from {chat.chat_type}: {chat.chat_id} {chat.chat_name}")

        except FloodWait as e:
            logger.warning(f"[~] FloodWait | Sleep {e.value}s | {e}")
            await sleep(e.value)

        except (PeerIdInvalid, ChannelInvalid) as e:
            logger.warning(f"[~] PeerIdInvalid | Skipped chat {chat.chat_id} {chat.chat_name} {chat.chat_type} | {e}")

        except Exception as e:
            logger.exception(f"[!] UnknownError | {chat.chat_id} {chat.chat_name} {chat.chat_type}| {e}")

        await sleep(delete_sleep)


async def archive_chats(client: Client) -> None:
    """Архивация чатов батчами со сном"""
    chat_data = [ch for ch in chat_table.get_all_data() if ch.is_leave]

    for i in range(0, len(chat_data), archive_batch_size):
        batch_chats = chat_data[i:i + archive_batch_size]
        batch_ids = [ch.chat_id for ch in batch_chats]

        try:
            await client.archive_chats(chat_ids=batch_ids)
            chat_names = [ch.chat_name for ch in batch_chats]
            logger.success(f"[+] Archived {len(batch_ids)} chats:\n{', '.join(chat_names)}")

        except FloodWait as e:
            logger.warning(f"[~] FloodWait | Sleep {e.value}s | {e}")
            await sleep(e.value)

        except (PeerIdInvalid, ChannelInvalid) as e:
            logger.warning(f"[~] PeerIdInvalid | Unknown chat, batch skipped | ID: {batch_ids} | {e}")

        except Exception as e:
            logger.exception(f"[!] UnknownError | ID: {batch_ids} | {e}")

        await sleep(archive_sleep)

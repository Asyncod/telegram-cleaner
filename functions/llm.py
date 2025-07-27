# -*- coding: utf-8 -*-
from config import providers, author_promt, theme_promt
from g4f.client import Client as g4fClient
from pyrogram import Client as pyroClient
from json.decoder import JSONDecodeError
from g4f.Provider import RetryProvider
from pyrogram.types import Dialog
from logs.logger import logger
from functions import util
from asyncio import sleep
from json import loads

g4f_client = g4fClient(provider=RetryProvider(providers=providers, shuffle=False))


async def defining_author(dialog: Dialog, client: pyroClient) -> str | None:
    """Определение автора из BIO"""
    if dialog.chat.type.value == "private": return dialog.chat.username

    chat = await client.get_chat(chat_id=dialog.chat.id)

    description = chat.description or chat.bio
    if description is None: return None

    response = g4f_client.chat.completions.create(messages=[{"role": "user", "content": author_promt + description}])

    await sleep(1)  # flood error prevention

    try:
        author = loads(response.choices[0].message.content)["author"]
        return author.replace("@", "") if author else None
    except JSONDecodeError:
        logger.error(f"[!] Defining author: {response.choices[0].message}")
        return None


async def defining_theme(dialog: Dialog, client: pyroClient) -> list[str] | None:
    """Определение тематики из 10 сообщений"""
    if dialog.chat.type.value != "channel": return None

    message_history = await util.get_message_history(dialog=dialog, client=client)
    if message_history == None: return None

    numbered_history = "\n".join(f"{i}) {text}" for i, text in enumerate(message_history, 1))
    response = g4f_client.chat.completions.create(messages=[{"role": "user", "content": theme_promt + numbered_history}])

    await sleep(1)  # flood error prevention

    try:
        theme: str = loads(response.choices[0].message.content)["theme"]
        return theme if theme else None
    except JSONDecodeError:
        logger.error(f"[!] Defining theme: {response.choices[0].message}")
        return None

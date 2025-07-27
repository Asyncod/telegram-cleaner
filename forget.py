# -*- coding: utf-8 -*-
from config import API_ID, API_HASH, PHONE_NUMBER, WORKDIR, forgot_method
from pyrogram.errors import PeerIdInvalid
from asyncio import get_event_loop
from functions import pyro, util
from database import chat_table
from logs.logger import logger
from pyrogram import Client

# client
client = Client(name="telegram-cleaner", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER, workdir=WORKDIR)


# main
async def main():
    async with client:

        if forgot_method == "del":
            await pyro.delete_chats(client=client)

        elif forgot_method == "arch":
            await pyro.archive_chats(client=client)


# init
if __name__ == '__main__':
    logger.warning(f"[~] Start Forget | Selected method: {'chat deleting' if forgot_method == 'del' else 'chat to archive'}")
    loop = get_event_loop()
    loop.run_until_complete(main())

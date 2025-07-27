# -*- coding: utf-8 -*-
from config import API_ID, API_HASH, PHONE_NUMBER, WORKDIR
from pyrogram.errors import ChannelPrivate
from asyncio import get_event_loop, sleep
from functions import util, llm
from database import chat_table
from logs.logger import logger
from pyrogram import Client

# client
client = Client(name="telegram-cleaner", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER, workdir=WORKDIR)


# main
async def main():
    async with client:
        async for dialog in client.get_dialogs():
            if chat_table.get_data(chat_id=dialog.chat.id) is not None:
                logger.success(f"[~] Already in DB {dialog.chat.id} - {dialog.chat.type.value}")
                continue

            logger.info(f"[~] Processing {dialog.chat.id} - {dialog.chat.type.value}")

            # get base info
            chat_id = dialog.chat.id
            chat_type = dialog.chat.type.value
            chat_name = dialog.chat.title if dialog.chat.title != None else dialog.chat.full_name
            chat_handler = dialog.chat.username if dialog.chat.username else None
            chat_date = int(dialog.top_message.date.timestamp())  # last message date
            chat_subscribers = dialog.chat.members_count if dialog.chat.members_count else 0
            is_admin = (dialog.chat.is_admin or dialog.chat.is_creator) or 0


            logger.info(f"[~] {chat_name} - {chat_handler}")

            # get additional info
            chat_author = await llm.defining_author(dialog=dialog, client=client)
            chat_theme = await llm.defining_theme(dialog=dialog, client=client)
            is_leave = util.is_leave_defining(dialog=dialog, chat_date=chat_date, is_admin=is_admin)

            logger.info(f"""\n
            ID:        {chat_id}
            TYPE:      {chat_type}
            NAME:      {chat_name}
            LINK:      {chat_handler}
            AUTHOR:    {chat_author}
            LAST DATE: {chat_date}
            THEME:     {chat_theme}
            SUBS:      {chat_subscribers}
            IS ADMIN:  {is_admin}
            IS LEAVE:  {is_leave}
            """)

            if chat_table.get_data(chat_id=chat_id) is None:
                logger.success(f"[+] {chat_name} added to database\n"
                               f"------------------------------------")
                chat_table.add(chat_id=chat_id,
                               chat_type=chat_type,
                               chat_name=chat_name,
                               chat_handler=chat_handler,
                               chat_author=chat_author,
                               chat_date=chat_date,
                               chat_theme=chat_theme,
                               chat_subscribers=chat_subscribers,
                               is_admin=is_admin,
                               is_leave=is_leave)


# init
if __name__ == '__main__':
    logger.info("[~] Start Analysis")
    chat_table.create_db()
    loop = get_event_loop()
    loop.run_until_complete(main())

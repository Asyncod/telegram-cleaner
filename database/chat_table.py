# -*- coding: utf-8 -*-
from dataclasses import dataclass
from logs.logger import logger
from config import DATABASE
from sqlite3 import connect
from json import dumps


#### TABLE MODEL ####
@dataclass
class ChatModel:
    """
    Параметры:
        chat_id: (int) - айди чата (-100)
        chat_type: (str) - канал, чат, личка, бот, форум
        chat_name: (str) - название чата
        chat_handler: (str) - ссылка на чат (NULL если нет)
        chat_author: (str) - автор канала
        chat_date: (int) - дата последнего актива (unix)
        chat_theme: (str) - список тематик (JSON)
        chat_subscribers: (int) - кол-во подписчиков
        is_admin: (int) - являюсь ли админом (0/1)
        is_leave: (int) - надо ли ливнуть (по параметрам) (0/1)
    """
    chat_id: int
    chat_type: str
    chat_name: str
    chat_handler: str
    chat_author: str
    chat_date: int
    chat_theme: str
    chat_subscribers: int
    is_admin: int
    is_leave: int


#### BASE CREATING ####
def create_db() -> None:
    with connect(DATABASE) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS chat_table(
                        chat_id INTEGER,
                        chat_type TEXT,
                        chat_name TEXT,
                        chat_handler TEXT,
                        chat_author TEXT,
                        chat_date INTEGER,
                        chat_theme TEXT,
                        chat_subscribers INTEGER,
                        is_admin INTEGER,
                        is_leave INTEGER)""")


#### DATA ADDING ####
def add(
        chat_id: int,
        chat_type: str,
        chat_name: str,
        chat_handler: str,
        chat_author: str,
        chat_date: int,
        chat_theme: list,
        chat_subscribers: int,
        is_admin: int,
        is_leave: int
) -> None:
    with connect(DATABASE) as db:
        chat_theme = dumps(chat_theme)
        db.execute("""INSERT INTO chat_table(chat_id, chat_type, chat_name, chat_handler, chat_author,
                    chat_date, chat_theme, chat_subscribers, is_admin, is_leave) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                   (chat_id, chat_type, chat_name, chat_handler, chat_author,
                    chat_date, chat_theme, chat_subscribers, is_admin, is_leave))


### DATA UPDATING ####
def update(field: str, data: int, chat_id: int) -> None:
    if field not in ChatModel.__annotations__:
        return logger.error(f"Invalid field name: {field}")

    with connect(DATABASE) as db:
        db.execute(f"UPDATE chat_table SET {field} = ? WHERE chat_id = ?", (data, chat_id))


#### DATA GETTING ####
def get_all_data() -> list[ChatModel]:
    with connect(DATABASE) as db:
        cursor = db.execute("SELECT * FROM chat_table")
        data = cursor.fetchall()
        return [ChatModel(*row) for row in data] if data else []


def get_data(chat_id: int) -> ChatModel | None:
    with connect(DATABASE) as db:
        cursor = db.execute("SELECT * FROM chat_table WHERE chat_id = ?", (chat_id,))
        data = cursor.fetchone()
        return ChatModel(*data) if data else None

# #### DATA DELETING ####
# def delete_all() -> None:
#     with connect(DATABASE) as db:
#         db.execute("DELETE FROM chat_table")

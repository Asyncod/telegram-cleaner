# -*- coding: utf-8 -*-
from config import unread_message_field, last_active_field, forgot_method
from datetime import datetime, timedelta
from pyrogram.types import Dialog
from logs.logger import logger
from pyrogram import Client


async def get_message_history(dialog: Dialog, client: Client) -> list[str]:
    """Получение 10 сообщений для анализа тематики"""
    message_slice = []
    async for message in client.get_chat_history(chat_id=dialog.chat.id, limit=10):
        if message.text:
            message_slice.append(message.text)
        elif message.caption:
            message_slice.append(message.caption)

    return message_slice


def date_filter(chat_date: int, chat_type: str) -> bool:
    """Проверяет по месяцам когда была последняя активность"""
    last_message = datetime.fromtimestamp(timestamp=chat_date)
    months = last_active_field.get(chat_type, 6)
    cutoff = datetime.now() - timedelta(days=30 * months)
    return last_message < cutoff


def unread_filter(unread_messages_count: int, chat_type: str) -> bool:
    """Проверка по кол-ву непрочитанных сообщений"""
    unread_limit = unread_message_field.get(chat_type)
    if unread_limit is None: return False
    return unread_messages_count > unread_limit  # 23 > 50 => False


def is_leave_defining(dialog: Dialog, chat_date: int, is_admin: bool) -> bool:
    """Определяем нужно ли удалять диалог | True => выходим, False => не выходим"""
    # на ботов похуй
    if dialog.chat.type.value == "bot": return False

    # если админ, то ливать не надо
    if is_admin: return False

    # если удаленный пользователь, то удаляем
    if dialog.chat.full_name is None: return True

    chat_type = dialog.chat.type.value
    unread_messages_count = dialog.unread_messages_count

    return (
            date_filter(chat_date=chat_date, chat_type=chat_type) or
            unread_filter(unread_messages_count=unread_messages_count, chat_type=chat_type)
    )

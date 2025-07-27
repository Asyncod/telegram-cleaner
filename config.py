# -*- coding: utf-8 -*-
import g4f.Provider as prov
from os import path

core = path.dirname(path.abspath(__file__))

# ==== USERBOT DATA ====

# From https://my.telegram.org/apps
API_HASH = "123123123asdasdasdasdas"
PHONE_NUMBER = "+70001234567"
API_ID = 123456

## === CLEANUP SETTINGS ===

# What to do with dialogs:
# "del" = leave the dialog
# "arch" = archive it
forgot_method = "arch"

# last active in months
last_active_field = {
    "channel": 6,
    "private": 3,
    "group": 1,
    "supergroup": 1
}

# unread messages
unread_message_field = {
    "channel": 50,
    "group": 1000,
    "supergroup": 1000
}

## === TOPICS ===

topic_list = [
    # Alpha channels
    "calls", "alpha", "airdrops", "presales", "retrodrops",
    # Coder's channels
    "devs", "botdev", "tools", "automation", "scripting",
    # All blockchain
    "solana", "ethereum", "ton", "zk", "layer2", "testnets",
    # P2E shit
    "nft", "gamefi",
    # Trading
    "trading", "onchain", "analytics",
    # Other
    "education", "news", "shitpost", "shitcoins", "memecoins"
]

## === PATH CONFIGURATION ===

DATABASE = f'{core}/database/base/data.db'
WORKDIR = f"{core}/sessions/"

## === PROVIDER SETTINGS ===

providers = [
    prov.Chatai,
    prov.Blackbox,
    prov.Cloudflare,
    prov.TeachAnything,
    prov.CohereForAI_C4AI_Command,
    prov.LegacyLMArena,
    prov.Copilot
]

# === PROMPTS ===

author_promt = """Here's the raw prompt as a plain English string with text-based numbering:

I will send you a BIO text from a Telegram channel. Your task is to extract the username of the person or group most likely to be the channel's author or creator.

The username may appear in the following formats:
1) @username (e.g. @asynco)
2) username.t.me
3) https://t.me/username

Guidelines:
– First, prefer usernames labeled as: creator, author, admin, owner, founder, создатель, основатель, админ, владелец, etc.
– Second, ignore usernames clearly marked for support, bots, ads, managers, or unrelated projects.
– Third, if no label is present, choose the most likely author based on context, wording, or position in the text.
– Fourth, even if there are multiple usernames, return the one that is most likely to be the channel owner.
– Fifth, if all usernames clearly belong to non-owners (e.g. support bots or ad contacts), return: {"author": null}

Return the result as a plain JSON string with no formatting or extra text.

Examples:
{"author": "asynco"}
{"author": null}

BIO text to analyze:
"""

theme_promt = f"""Analyze the following 10 messages from a Telegram channel and select 1 to 6 of the most relevant topics from the list below. If none of the topics are suitable, return the one that is most suitable.

Topics: {topic_list}

Return the result strictly as a single JSON string, without formatting or comments.

Example: {{"theme": ["solana", "retrodrops"]}}

Here is the list of messages, numbered from 1 to 10: 
"""

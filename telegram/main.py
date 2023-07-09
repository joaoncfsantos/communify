#!/usr/bin/env python
# pylint: disable=unused-argument,wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple example of a Telegram WebApp which displays a color picker.
The static website for this website is hosted by the PTB team for your convenience.
Currently only showcases starting the WebApp via a KeyboardButton, as all other methods would
require a bot token.
"""
import json
import logging
import webbrowser
from web3 import Web3
from eth_account import Account
from flask import Flask, redirect, url_for
import json
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo, Bot, \
    InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler

from telegram import __version__ as TG_VER
import time
from flask import Flask, jsonify, request
import json


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Variables
STATE_0 = 0
STATE_1 = 1
STATE_2 = 2

async def login_metamask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message.chat.type == "private":
        buttons = [
            InlineKeyboardButton("Quests", callback_data="quests"),
            InlineKeyboardButton("Donations", callback_data="donations"),
            InlineKeyboardButton("Create Quest", callback_data="create_quest"),
        ]
    else:
        buttons = [
            InlineKeyboardButton("Join Quest", callback_data="join_quest"),
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))

    await update.message.reply_text(
        "Chose a command to continue:",
        reply_markup=reply_markup
    )

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=f"You selected the color with the HEX value <code>{data['hex']}</code>. The "
             f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>.",
        reply_markup=ReplyKeyboardRemove(),
    )


async def create_quest_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    chat_id = update.message.chat_id
    # Check the chat type
    if message.chat.type == "private":
        await update.message.reply_text("Creating a new Quest! Please enter the quest title")
        return STATE_0

async def create_quest_step_1(update, context):
    text = update.message.text
    context.user_data['title'] = text
    reply_text = "Please enter the description"
    await update.message.reply_text(reply_text)
    return STATE_1

async def create_quest_step_2(update, context):
    text = update.message.text
    context.user_data['description'] = text
    reply_text = "Please enter the group name"
    await update.message.reply_text(reply_text)
    return STATE_2

async def join_quest_step_1(update, context):
    message = update.message
    if message.chat.type == "supergroup" or message.chat.type == "group":
        await update.message.reply_text("Insert the quest title")
    return STATE_0

async def join_quest_step_2(update, context):
    message = update.message
    if message.chat.type == "supergroup" or message.chat.type == "group":
        await update.message.reply_text("Confirmed. Let's do the quest!")
    return ConversationHandler.END

async def quest(update, context):
    message = update.message
    if message.chat.type == "private":
        await update.message.reply_text(
            "Please press the button to open quests",
            reply_markup=ReplyKeyboardMarkup.from_button(
                KeyboardButton(
                    text="Quests",
                    web_app=WebAppInfo(url="https://ethbcn-communify.vercel.app/"),
                )
            ),
        )

async def donations(update, context):
    message = update.message
    if message.chat.type == "private":
        await update.message.reply_text(
            "Please press the button to open donations",
            reply_markup=ReplyKeyboardMarkup.from_button(
                KeyboardButton(
                    text="Donations",
                    web_app=WebAppInfo(url="https://ethbcn-communify.vercel.app/"),
                )
            ),
        )

async def submit_quest(update, context):
    text = update.message.text
    context.user_data['groupId'] = text
    quest = f"New Quest Created \nTitle: {context.user_data['title']}\nDescription: {context.user_data['description']}\nGroupId: {context.user_data['groupId']}\n"
    await update.message.reply_text(quest)
    await context.bot.send_message(chat_id=-922731086, text=quest)
    return ConversationHandler.END

async def button_callback(update, context):
    query = update.callback_query
    command = query.data
    chat_id = query.message.chat_id

    # Handle the selected command
    if command == "quests":
        await context.bot.send_message(chat_id=chat_id, text="/quests")
    elif command == "create_quest":
        await context.bot.send_message(chat_id=chat_id, text="/create_quest")
    elif command == "join_quest":
        await context.bot.send_message(chat_id=chat_id, text="/join_quest")
    elif command == "donations":
        await context.bot.send_message(chat_id=chat_id, text="/donations")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6069789184:AAECHOy_SdBooMy7tzTlCIIHSY6qBB0yDUw").build()

    application.add_handler(CommandHandler("start", login_metamask))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    application.add_handler(CommandHandler("quests", quest))

    application.add_handler(CommandHandler("donations", donations))


    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('join_quest', join_quest_step_1)],
        states={
            STATE_0: [MessageHandler(filters.TEXT, join_quest_step_2)],
        },
        fallbacks=[]
    ))

    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('create_quest', create_quest_start)],
        states={
            STATE_0: [MessageHandler(filters.TEXT, create_quest_step_1)],
            STATE_1: [MessageHandler(filters.TEXT, create_quest_step_2)],
            STATE_2: [MessageHandler(filters.TEXT, submit_quest)],
        },
        fallbacks=[]
    ))
    application.add_handler(CallbackQueryHandler(button_callback))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
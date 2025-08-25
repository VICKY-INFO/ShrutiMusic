import asyncio
import importlib
from threading import Thread
from flask import Flask
from pyrogram import idle
from pyrogram.types import BotCommand
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ShrutiMusic import LOGGER, app, userbot
from ShrutiMusic.core.call import Aviax
from ShrutiMusic.misc import sudo
from ShrutiMusic.plugins import ALL_MODULES
from ShrutiMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# ---------------------- Flask Server ----------------------
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8000)

# ---------------------- Bot Commands ----------------------
COMMANDS = [
    BotCommand("start", "🚀 Start bot"),
    BotCommand("help", "❓ Help menu"),
    BotCommand("ping", "📡 Ping and system stats"),
    BotCommand("play", "🎵 Start streaming the requested track"),
    BotCommand("vplay", "📹 Start video streaming"),
    BotCommand("playforce", "⚠️ Force play audio track"),
    BotCommand("vplayforce", "⚠️ Force play video track"),
    BotCommand("pause", "⏸ Pause the stream"),
    BotCommand("resume", "▶️ Resume the stream"),
    BotCommand("skip", "⏭ Skip the current track"),
    BotCommand("end", "🛑 End the stream"),
    BotCommand("stop", "🛑 Stop the stream"),
    BotCommand("player", "🎛 Get interactive player panel"),
    BotCommand("queue", "📄 Show track queue"),
    BotCommand("auth", "➕ Add a user to auth list"),
    BotCommand("unauth", "➖ Remove a user from auth list"),
    BotCommand("authusers", "👥 Show list of auth users"),
    BotCommand("cplay", "📻 Channel audio play"),
    BotCommand("cvplay", "📺 Channel video play"),
    BotCommand("cplayforce", "🚨 Channel force audio play"),
    BotCommand("cvplayforce", "🚨 Channel force video play"),
    BotCommand("channelplay", "🔗 Connect group to channel"),
    BotCommand("loop", "🔁 Enable/disable loop"),
    BotCommand("stats", "📊 Bot stats"),
    BotCommand("shuffle", "🔀 Shuffle the queue"),
    BotCommand("seek", "⏩ Seek forward"),
    BotCommand("seekback", "⏪ Seek backward"),
    BotCommand("song", "🎶 Download song (mp3/mp4)"),
    BotCommand("speed", "⏩ Adjust audio playback speed (group)"),
    BotCommand("cspeed", "⏩ Adjust audio speed (channel)"),
    BotCommand("tagall", "📢 Tag everyone"),
    BotCommand("admins", "🛡 Tag all admins"),
    BotCommand("tgm", "🖼 Convert image to URL"),
    BotCommand("vid", "🎞 Download video from social media"),
    BotCommand("dice", "🎲 Roll a dice"),
    BotCommand("ludo", "🎲 Play ludo"),
    BotCommand("dart", "🎯 Throw a dart"),
    BotCommand("basket", "🏀 Play basketball"),
    BotCommand("football", "⚽ Play football"),
    BotCommand("slot", "🎰 Play slot"),
    BotCommand("jackpot", "🎰 Play jackpot"),
    BotCommand("bowling", "🎳 Play bowling"),
    BotCommand("ban", "🚫 Ban a user"),
    BotCommand("banall", "⚠️ Ban all users"),
    BotCommand("sban", "🧹 Delete & ban user"),
    BotCommand("tban", "⏳ Temporary ban"),
    BotCommand("unban", "✅ Unban a user"),
    BotCommand("warn", "⚠️ Warn a user"),
    BotCommand("swarn", "🧹 Delete & warn user"),
    BotCommand("rmwarns", "🗑 Remove all warnings"),
    BotCommand("warns", "📋 Show user warnings"),
    BotCommand("kick", "👢 Kick user"),
    BotCommand("skick", "🧹 Delete msg & kick"),
    BotCommand("purge", "🧽 Purge messages"),
    BotCommand("del", "❌ Delete message"),
    BotCommand("promote", "⬆️ Promote member"),
    BotCommand("fullpromote", "🚀 Full promote"),
    BotCommand("demote", "⬇️ Demote member"),
    BotCommand("pin", "📌 Pin message"),
    BotCommand("unpin", "❎ Unpin message"),
    BotCommand("unpinall", "🧹 Unpin all"),
    BotCommand("mute", "🔇 Mute user"),
    BotCommand("tmute", "⏱ Temp mute"),
    BotCommand("unmute", "🔊 Unmute"),
    BotCommand("zombies", "💀 Ban deleted accounts"),
    BotCommand("report", "🚨 Report to admins"),
    BotCommand("markdownhelp", "📖 Help about Markdown"),
    BotCommand("tts", "🗣 Convert text to speech"),
    BotCommand("givelink", "🔗 Get invite link for current chat"),
    BotCommand("link", "🔗 Get invite link for specified group"),
    BotCommand("fsub", "🔒 Set/disable force subscription"),
    BotCommand("info", "ℹ️ Get detailed user information"),
    BotCommand("userinfo", "ℹ️ Get user information (alias)"),
    BotCommand("downloadrepo", "📥 Download GitHub repository"),
    BotCommand("truth", "🤔 Get random truth question"),
    BotCommand("dare", "💪 Get random dare challenge"),
    BotCommand("mongochk", "🗃 Check MongoDB URL validity"),
    BotCommand("font", "🎨 Convert text to beautiful fonts"),
    BotCommand("gali", "😤 Send random gali"),
    BotCommand("bots", "🤖 Get list of bots in group")
]

# ---------------------- Setup Bot Commands ----------------------
async def setup_bot_commands():
    try:
        await app.set_bot_commands(COMMANDS)
        LOGGER("ShrutiMusic").info("Bot commands set successfully!")
    except Exception as e:
        LOGGER("ShrutiMusic").error(f"Failed to set bot commands: {str(e)}")

# ---------------------- Bot Initialization ----------------------
async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    await setup_bot_commands()

    for all_module in ALL_MODULES:
        try:
            importlib.import_module(f"ShrutiMusic.plugins.{all_module}")
        except Exception as e:
            LOGGER("ShrutiMusic.plugins").error(f"Failed to import {all_module}: {e}")

    LOGGER("ShrutiMusic.plugins").info("Successfully Imported Modules...")

    await userbot.start()
    await Aviax.start()

    try:
        await Aviax.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ShrutiMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass

    await Aviax.decorators()

    LOGGER("ShrutiMusic").info(
        "Shruti Music Started Successfully.\n\nDon't forget to visit @ShrutiBots"
    )

    try:
        await idle()
    finally:
        await app.stop()
        await userbot.stop()
        LOGGER("ShrutiMusic").info("Stopping Shruti Music Bot...🥺")

# ---------------------- Main Entry Point ----------------------
if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.get_event_loop().run_until_complete(init())

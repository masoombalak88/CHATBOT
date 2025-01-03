from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("message_handler_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(bot, message):
    try:
        await message.reply_video(
            video="https://files.catbox.moe/qdtfhq.mp4",
            caption=(
                "🌟 Welcome to Healix AI – Your Virtual Health Companion! 🌟\n\n👨‍⚕️ What Can I Do?\n"
                "🔹 Analyze your symptoms\n"
                "🔹 Predict potential diseases\n🔹 Provide remedies, precautions, and wellness tips\n\n🔹 Provide remedies, precautions, and wellness tips\n\n"
                "✨ How Does It Work?\n✅ Simple & Quick! Just type in your symptoms, and I'll provide accurate, AI-powered health insights instantly!\n\n"
                "Let’s make your health journey smarter, faster, and easier! 💖\n\n🌐 Stay Connected with Us!\n[🌍 Website](https://healixai.tech) | [💬 Telegram](https://t.me/HealixAi) | [🐦 Twitter](https://x.com/Healix__AI)."
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        print(f"Error in /start command: {e}")
        await message.reply_text("❍ ᴇʀʀᴏʀ: Unable to process the command.")

@app.on_message(filters.text & ~filters.group)
async def handle_private_query(client, message):
    # Get the message text
    query = message.text

    if not query:
        await message.reply_text("I didn't receive any text to process.")
        return

    # Send typing action to indicate bot is working
    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Use the API to get response
    api_url = f"https://chatwithai.codesearch.workers.dev/?chat={query}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            reply = response.text.strip()  # Process API response
        else:
            reply = "Failed to fetch data from the API. Please try again later."
    except Exception as e:
        reply = f"An error occurred: {e}"

    # Reply to the user
    await message.reply_text(reply)

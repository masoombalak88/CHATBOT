from pyrogram import Client, filters
import requests

# Bot configuration
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# Define the API URL
BASE_URL = "https://chatwithai.codesearch.workers.dev/?chat="

# Initialize the bot
app = Client("reply_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start_command(bot, message):
    try:
        
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add Me to Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
                ],
                [
                    InlineKeyboardButton("👥 Support", url=SUPPORT_LINK),
                    InlineKeyboardButton("📢 Updates", url=UPDATES_LINK),
                ],
            ]
        )

        
        await message.reply_text(
            "👋 **Welcome to AI Bot!**\n\n"
            "I can answer your queries and assist you. Just type your message to get started.\n\n"
            "Use me wisely and have fun!\n\n"
            f"🔹 Maintained by [Baby-Music]({SUPPORT_LINK})",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        print(f"Error in /start command: {e}")
        await message.reply_text("❍ ᴇʀʀᴏʀ: Unable to process the command.")
        

@app.on_message(filters.text & ~filters.bot)
def reply_to_message(client, message):
    user_message = message.text
    try:
        # Fetch the response from the API
        response = requests.get(BASE_URL + user_message)
        if response.status_code == 200:
            reply = response.text
        else:
            reply = "I'm having trouble connecting to my AI brain right now. Please try again later."
    except Exception as e:
        reply = f"An error occurred: {str(e)}"

    # Reply to the user
    message.reply_text(reply)

# Start the bot
print("Bot is running...")
app.run()

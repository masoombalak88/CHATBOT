from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests


from config import API_ID, API_HASH, BOT_TOKEN, API_KEY, BASE_URL, SUPPORT_LINK, UPDATES_LINK, BOT_USERNAME


app = Client("message_handler_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


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


@app.on_message(filters.text)
async def handle_messages(bot, message):
    try:
        unwanted_symbols = ["/", ":", ";", "*", "?"]

        
        if message.text[0] in unwanted_symbols:
            print(f"Ignored message: {message.text}")
            return

        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        query = message.text
        print(f"Processing query: {query}")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)

        if response.status_code == 200 and response.text.strip():
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                result = response_data["choices"][0]["message"]["content"]
                await message.reply_text(
                    f"{result} \n\nＡɴsᴡᴇʀᴇᴅ ʙʏ➛[Baby-Music]({SUPPORT_LINK})",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await message.reply_text("❍ ᴇʀʀᴏʀ: No response from API.")
        else:
            await message.reply_text(f"❍ ᴇʀʀᴏʀ: API request failed. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")
        await message.reply_text(f"❍ ᴇʀʀᴏʀ: {e}")


from pyrogram import Client, filters
import requests

@app.on_message(filters.text)
async def venom(client, message):
    # Get the message text
    query = message.text

    if not query:
        await message.reply_text("I didn't receive any text to process.")
        return

    # Send typing action to indicate bot is working
    await client.send_chat_action(chat_id=message.chat.id, action="typing")

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



if __name__ == "__main__":
    print("Bot is running...")
    app.run()

import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import yt_dlp

# Replace these with your actual credentials
API_ID = 23592879
API_HASH = "3721d1ed9dc1ba208f01df0830c3bddf"
BOT_TOKEN = "7631986963:AAFBSq-q4CLfDAyVcKKyzUeFf7XYLlrobos"
SESSION_STRING = "BQFn_68ACOq8XKZYvmat298EZ2e8tAeMTbLdCyCjtye1yROXY9FY_LwPaeWJ7qV0ftqR_9wi5q_XJ2thaKwQtA_DbSbhJQ2ADlOwK0oR_9vFfGi1BLWiJy0tlEdw7DZDniZKn-qtso1bCCUPrxDnYWXxIxKuyEHLu67tJ1rouHZMuDE_3g4mR15ON3HVzZjZ1VQ3pNU9Y3_0oSThNC73sWEAJKHvCmhg7PYThS0FaJrmz_oVnRaHQrQlrnWD8xaDjOEWN802_zAZ18rh3BH-4dgj_QriMCJ7DyGAWAs3CaG95o16zW5bSCyK7nqrCdL85R9e8YBgc9nGAbzbygwQoEtqnN3PpgAAAAHG5uETAQ"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("user_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call = PyTgCalls(user)

# Function to extract direct audio URL from YouTube
def get_audio_url(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info['url']

@app.on_message(filters.command("play"))
async def play(client, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a song name or YouTube URL.")
        return
    
    query = message.command[1]
    await message.reply_text("🔍 Searching for song...")
    
    try:
        audio_url = get_audio_url(query)
        await call.join_group_call(chat_id, AudioPiped(audio_url))
        await message.reply_text("🎶 Now streaming: " + query)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("stop"))
async def stop(client, message):
    chat_id = message.chat.id
    await call.leave_group_call(chat_id)
    await message.reply_text("⏹ Music stopped!")

async def main():
    await app.start()
    await user.start()
    await call.start()
    print("✅ Music bot is running!")
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())

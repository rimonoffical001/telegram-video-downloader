import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yt_dlp

BOT_TOKEN = '7613320210:AAE8dbthYmLpMHeBrXMkYJAqC2sNk4Ozm9A'

def start(update, context):
    update.message.reply_text("Welcome! Send me a video link (YouTube, TikTok, Facebook) and I'll download it for you.")

def download_video(update, context):
    url = update.message.text.strip()
    update.message.reply_text(f"Downloading your video from: {url}")

    try:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as f:
            update.message.reply_video(f)
        
        os.remove(filename)

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

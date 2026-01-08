import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Koyeb env variable
CHANNEL_ID = --1002346456370         # Replace with your channel numeric ID
ADMIN_IDS = [6394992325, 2059727537]  # Replace with your admin numeric IDs

video_storage = {}  # link_id : file_id

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if args:
        link_id = args[0]
        try:
            member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
            if member.status in ["left", "kicked"]:
                keyboard = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Channel", url="https://t.me/laptoplinkshere")]]
                )
                await update.message.reply_text(
                    "⚠️ You must join the channel to access this video.", reply_markup=keyboard
                )
                return
        except:
            await update.message.reply_text("⚠️ Error checking channel membership.")
            return

        if link_id in video_storage:
            await context.bot.send_video(chat_id=user_id, video=video_storage[link_id])
        else:
            await update.message.reply_text("❌ Invalid video link.")
    else:
        await update.message.reply_text("👋 Hello! Only admins can upload videos.")

# Video upload (admin only)
async def upload_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You are not allowed to upload videos.")
        return

    if update.message.video:
        file_id = update.message.video.file_id
        link_id = str(len(video_storage) + 1)
        video_storage[link_id] = file_id
        await update.message.reply_text(
            f"✅ Video uploaded!\nUser link:\nhttps://t.me/{context.bot.username}?start={link_id}"
        )
    else:
        await update.message.reply_text("❌ Please send a video file.")

# Unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Unknown command.")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, upload_video))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    app.run_polling()

if __name__ == "__main__":
    main()

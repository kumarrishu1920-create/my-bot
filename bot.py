import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8955451526:AAE4aCJvWElPVqRDidEKWxH_hl3ggflo9J0"
STORAGE_CHANNEL_ID = -1002340619256

# Dono required channels ki Details
CHANNEL_1_ID = -1003712791002
CHANNEL_1_LINK = "https://t.me/+QyaE1JF3ECs4NmVl"

CHANNEL_2_ID = -1002530222523
CHANNEL_2_LINK = "https://t.me/+d5YwXxXXUgA0NjY1"
# ========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def is_member(context: ContextTypes.DEFAULT_TYPE, channel_id: int, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        print(f"Error checking channel {channel_id}: {e}")
        return False

async def delete_messages_later(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_ids: list, delay: int):
    await asyncio.sleep(delay)
    for msg_id in message_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            print(f"Failed to delete message {msg_id}: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    if context.args:
        file_id = context.args[0]
        
        joined_c1 = await is_member(context, CHANNEL_1_ID, user.id)
        joined_c2 = await is_member(context, CHANNEL_2_ID, user.id)
        
        if not (joined_c1 and joined_c2):
            try_again_url = f"https://t.me/{context.bot.username}?start={file_id}"
            
            keyboard = [
                [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1_LINK)],
                [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2_LINK)],
                [InlineKeyboardButton("🔄 Try Again", url=try_again_url)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "⚠️ **Access Denied!**\n\n"
                "You must join both of our official channels to access this video.\n"
                "Please click the **Join Channel** buttons below, join both channels, and then click **Try Again**.",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            return

        try:
            msg_id = int(file_id)
            
            warning_msg = await context.bot.send_message(
                chat_id=chat_id,
                text="⏳ **Important Notice:**\n\n"
                     "This video will be automatically deleted in **10 minutes** due to copyright protection.\n"
                     "Please forward this video to your **Saved Messages** immediately if you wish to keep it!",
                parse_mode="Markdown"
            )

            video_msg = await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=msg_id
            )

            asyncio.create_task(
                delete_messages_later(
                    context=context,
                    chat_id=chat_id,
                    message_ids=[warning_msg.message_id, video_msg.message_id],
                    delay=600
                )
            )
            return

        except Exception as e:
            await update.message.reply_text("❌ Video not found or link has expired.")
            print(f"Error sending video: {e}")
            return

    await update.message.reply_text(
        f"Hello {user.first_name}!\n\nWelcome to File Store Bot. Click on any valid video link to request content."
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

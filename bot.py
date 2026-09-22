import os
import logging
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ----------------------------------------------------
# 1. RENDER PORT ERROR FIX (DUMMY WEB SERVER)
# ----------------------------------------------------
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is live and running 24/7!")

def start_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyServer)
    server.serve_forever()

# Dummy server ko background thread me start karein
Thread(target=start_server, daemon=True).start()

# ----------------------------------------------------
# 2. TELEGRAM BOT HANDLERS & LOGIC
# ----------------------------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    
    # Agar start command me koi file/video ID aayi hai (Jaise /start 24)
    if context.args:
        file_id = context.args[0]
        await update.message.reply_text(f"Hello {user_first_name}! Processing your request for file ID: {file_id}...")
        # Yahan aapki file/video sending ki specific logic aayegi
    else:
        await update.message.reply_text(f"Hello {user_first_name}! Welcome to the File Store Bot.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a valid file link or command to get files.")

# ----------------------------------------------------
# 3. MAIN BOT EXECUTION
# ----------------------------------------------------
if __name__ == '__main__':
    # Apne Bot Token ko yahan replace karein agar Environment Variable use nahi kar rahe hain
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8955451526:AAE4aCJvWE1PVqRDidEKWxH_hl3ggflo9J0")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers add karein
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot starting polling...")
    app.run_polling()

            

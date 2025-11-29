import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import logging
import time
from pyrogram import Client, enums
from pyrogram.errors import FloodWait
from bot import APP_ID, API_HASH, BOT_TOKEN, DOWNLOAD_DIRECTORY

# ---------------- Health Check Server ---------------- #
class HealthHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # Suppress default logging

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    server = HTTPServer(("0.0.0.0", 8000), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# ---------------- Logging ---------------- #
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# ---------------- Bot Setup ---------------- #
if not os.path.isdir(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

plugins = dict(root="bot/plugins")
app = Client(
    "G-DriveBot",
    bot_token=BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    plugins=plugins,
    parse_mode=enums.ParseMode.MARKDOWN,
    workdir=DOWNLOAD_DIRECTORY,
)

# ---------------- Run Bot with FloodWait Handling ---------------- #
def run_bot():
    while True:
        try:
            LOGGER.info("Starting Bot !")
            app.run()
            LOGGER.info("Bot Stopped !")
            break  # Stop the loop if app.run() finishes normally
        except FloodWait as e:
            wait_time = e.x
            LOGGER.warning(f"Flood wait detected. Sleeping for {wait_time} seconds...")
            time.sleep(wait_time)

if __name__ == "__main__":
    run_bot()

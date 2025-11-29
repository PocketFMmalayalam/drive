import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

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



import os
import logging
from pyrogram import Client
from pyrogram import enums
from bot import APP_ID, API_HASH, BOT_TOKEN, DOWNLOAD_DIRECTORY

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


if __name__ == "__main__":
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
    LOGGER.info("Starting Bot !")
    app.run()
    LOGGER.info("Bot Stopped !")

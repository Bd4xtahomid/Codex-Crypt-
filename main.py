import os
import time
import config
from src.gui_mode import run_gui
from src.terminal_mode import run_terminal_mode
import logging

if not os.path.exists('Secret'):
    os.makedirs('Secret/phrases', exist_ok=True)
    os.makedirs('Secret/images', exist_ok=True)
    os.makedirs('Secret/keys', exist_ok=True)
    os.makedirs('Secret/logs', exist_ok=True)
if not os.path.exists('Decrypt'):
    os.makedirs('Decrypt', exist_ok=True)

logging.basicConfig(filename='Secret/logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    logging.info("App started")
    if config.MODE == "gui":
        run_gui()
    else:
        run_terminal_mode(config.MODE)
    logging.info("App ended")

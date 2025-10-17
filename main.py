
import os
import time
import config
from src.gui_mode import run_gui
from src.terminal_mode import run_terminal_mode
import logging

logging.basicConfig(filename='Secret/logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if not os.path.exists('Secret'):
    os.mkdir('Secret')
if not os.path.exists('Secret/phrases'):
    os.mkdir('Secret/phrases')
if not os.path.exists('Secret/images'):
    os.mkdir('Secret/images')
if not os.path.exists('Secret/keys'):
    os.mkdir('Secret/keys')
if not os.path.exists('Secret/logs'):
    os.mkdir('Secret/logs')

subfolder = time.strftime("%Y%m%d_%H%M%S")
sub_path = os.path.join('Secret', subfolder)
os.mkdir(sub_path)
os.mkdir(os.path.join(sub_path, 'images'))
os.mkdir(os.path.join(sub_path, 'keys'))

if __name__ == "__main__":
    logging.info("App started")
    if config.MODE == "gui":
        run_gui()
    else:
        run_terminal_mode(config.MODE)
    logging.info("App ended")
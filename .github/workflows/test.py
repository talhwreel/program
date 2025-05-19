import os
import time
import datetime
import sys
import subprocess
import random
import string
import threading
import ctypes

# Lisanslar
LICENSES = {
    "kaancalismayan31": {"username": "Kaan", "expiration_date": "2025-12-31"},
    "berkayfull31de": {"username": "Berkay Çalışkan", "expiration_date": "2027-05-06"},
    "EAGLE-0NE1-M0NT4H": {"username": "Byghostking", "expiration_date": "2025-06-10"},
    "PRKS-EAGLE-S0FTW4RE": {"username": "SYX", "expiration_date": "2025-06-12"},
    "RJEH-EAJLE-S07TW4RE": {"username": "Enes", "expiration_date": "2025-06-13"},
    "DHWR-KTHE-S01M0NTH": {"username": "Cankong", "expiration_date": "2025-06-13"},
}

LOG_DIR = "C:\\EagleLog"
LOG_FILE = os.path.join(LOG_DIR, "log.txt")

def colored_text(text, color):
    colors = {
        'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m',
        'blue': '\033[94m', 'magenta': '\033[95m', 'cyan': '\033[96m',
        'white': '\033[97m', 'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_license(license_key):
    license_info = LICENSES.get(license_key)
    if not license_info:
        print(colored_text("❌ Invalid license key! Try again.\n", 'red'))
        return None
    expiration_date = datetime.datetime.strptime(license_info["expiration_date"], "%Y-%m-%d")
    if expiration_date < datetime.datetime.now():
        print(colored_text("❌ License expired! Please renew.\n", 'red'))
        return None
    remaining_days = (expiration_date - datetime.datetime.now()).days
    print(f"{colored_text('🔐 License valid for:', 'yellow')} {remaining_days} days.\n")
    return license_info

def get_license():
    return input(colored_text("🔑 Enter your license key: ", 'green'))

def save_license(license_key):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    with open(LOG_FILE, "w") as file:
        file.write(license_key)

def load_license():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            return file.read().strip()
    return None

def random_title_updater(stop_event):
    while not stop_event.is_set():
        random_title = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        if os.name == 'nt':
            os.system(f"title {random_title}")
            ctypes.windll.kernel32.SetConsoleTitleW(random_title)
        time.sleep(1)

def eagle_loading_sequence():
    print(colored_text("\n🦅 Eagle loading...\n", 'yellow'))
    total_duration = random.randint(5, 20)
    steps = 50  # Bar steps
    interval = total_duration / steps

    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        bar = '█' * (i // 2) + '-' * ((50 - i) // 2)
        print(colored_text(f"\r[{bar}] {percent}%", 'cyan'), end='', flush=True)
        time.sleep(interval)

    print(colored_text("\n✅ Eagle successfully loaded!", 'green'))
    time.sleep(2)
    clear_console()

def wait_for_valorant():
    print(colored_text("🕹 Please start Valorant", 'cyan'))
    while True:
        try:
            output = subprocess.check_output('tasklist', shell=True).decode(errors='ignore')
            if "VALORANT.exe" in output or "valorant.exe" in output:
                output_pid = subprocess.check_output('tasklist /FI "IMAGENAME eq VALORANT.exe" /FO LIST', shell=True).decode(errors='ignore')
                beep_success()
                screen_flash()
                clear_console()
                print(colored_text("🟢 Successfully Injected!", 'green'))
                print(colored_text(output_pid.strip(), 'yellow'))
                break
            time.sleep(1)
        except subprocess.CalledProcessError:
            time.sleep(1)

def splash_intro():
    print(colored_text("Welcome to Eagle Loader", 'cyan'))
    print(colored_text("=======================", 'cyan'))
    time.sleep(1)

def license_check_flow():
    while True:
        saved_license = load_license()
        if saved_license:
            license_info = validate_license(saved_license)
            if license_info:
                return license_info
            else:
                os.remove(LOG_FILE)  # Hatalıysa sil
        else:
            license_key = get_license()
            license_info = validate_license(license_key)
            if license_info:
                save_license(license_key)
                return license_info

def log_user_info(username):
    print(colored_text(f"👤 Welcome {username}", 'cyan'))
    time.sleep(1)

def start_discord_rpc(username):
    print(colored_text("💬 [Discord RPC] Valorant ile bağlantı bekleniyor...", 'magenta'))

def beep_success():
    if os.name == 'nt':
        import winsound
    ctypes.windll.user32.MessageBeep(0)
    else:
        print('\a')

def screen_flash():
    clear_console()
    print(colored_text("█" * 60, 'black'))
    time.sleep(0.2)
    clear_console()

def main():
    stop_event = threading.Event()
    threading.Thread(target=random_title_updater, args=(stop_event,), daemon=True).start()

    clear_console()
    splash_intro()
    license_info = license_check_flow()
    log_user_info(license_info["username"])
    start_discord_rpc(license_info["username"])
    eagle_loading_sequence()
    wait_for_valorant()

    stop_event.set()
    input(colored_text("\nPress Enter to close...", 'magenta'))
    sys.exit()

if __name__ == "__main__":
    main()

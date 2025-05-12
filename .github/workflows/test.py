import os
import time
import datetime
import sys
import msvcrt
import subprocess
from pypresence import Presence

LICENSES = {
    "kaancalismayan31": {"username": "Kaan", "expiration_date": "2025-12-31"},
    "berkayfull31de": {"username": "Berkay Çalışkan", "expiration_date": "2027-05-06"},
    "EAGLE-0NE1-M0NT4H": {"username": "Byghostking", "expiration_date": "2025-06-10"},
    "PRKS-EAGLE-S0FTW4RE": {"username": "SYX", "expiration_date": "2025-06-12"},
    "RJEH-EAJLE-S07TW4RE": {"username": "Enes", "expiration_date": "2025-06-13"},
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

def start_discord_presence():
    try:
        client_id = "1368588698148671488"
        rpc = Presence(client_id)
        rpc.connect()
        rpc.update(
            state="Developed by kaancaliskan",
            details="Bende Eagle Software'nin valorant yazılımını kullanıyorum, sende kullanmaya ne dersin?",
            large_image="eagle",
            start=time.time(),
            buttons=[{"label": "Telegram", "url": "https://t.me/eaglesoftwar2"}]
        )
    except:
        pass

def validate_license(license_key):
    license_info = LICENSES.get(license_key)
    if not license_info:
        print(colored_text("Geçersiz lisans anahtarı!", 'red'))
        return None
    expiration_date = datetime.datetime.strptime(license_info["expiration_date"], "%Y-%m-%d")
    if expiration_date < datetime.datetime.now():
        print(colored_text("Lisansınızın süresi dolmuş! Yenileyin.", 'red'))
        return None
    remaining_days = (expiration_date - datetime.datetime.now()).days
    print(f"\n{colored_text('Lisans süreniz:', 'yellow')} {remaining_days} gün kaldı.\n")
    return license_info

def display_ascii_art():
    art = r"""
                      .__                               
  ____ _____     ____ |  |   ____                       
_/ __ \\__  \   / ___\|  | _/ __ \                      
\  ___/ / __ \_/ /_/  >  |_\  ___/                       
 \___  >____  /\___  /|____/\___  >                      
     \/     \//_____/           \/                       
              _____  __                                
  ___________/ ____\/  |___  _  _______ _______   ____  
 /  ___/  _ \   __\\   __\ \/ \/ /\__  \\_  __ \_/ __ \ 
 \___ (  <_> )  |   |  |  \     /  / __ \|  | \/\  ___/ 
/____  >____/|__|   |__|   \/\_/  (____  /__|    \___  >
     \/                                \/            \/ 
"""
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    for i in range(3):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colored_text(art, colors[i % len(colors)]))
        time.sleep(0.5)

def get_license():
    return input(colored_text("Lisans anahtarınızı girin: ", 'green'))

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

def flashing_text(text, duration=3, delay=0.3):
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    end_time = time.time() + duration
    while time.time() < end_time:
        for color in colors:
            print(f"\r{colored_text(text, color)}", end="", flush=True)
            time.sleep(delay)
    print(f"\r{colored_text(text, 'green')}")

def is_valorant_running():
    try:
        output = subprocess.check_output('tasklist', shell=True).decode()
        return "VALORANT.exe" in output or "valorant.exe" in output
    except subprocess.CalledProcessError:
        return False

def show_menu(username):
    print(f"\n{colored_text('Hoş geldiniz,', 'green')} {colored_text(username, 'cyan')}!")
    flashing_text("1. Hileyi aktif et " + colored_text("(Aktif)", 'green'), duration=2)
    print(colored_text("\n2. Çıkış", 'red'))
    choice = input(colored_text("\nSeçiminizi yapınız: ", 'yellow'))
    
    if choice == "1":
        print(colored_text("\nValorant bekleniyor...", 'yellow'))
        if is_valorant_running():
            print(colored_text("Valorant algılandı!", 'green'))
        else:
            print(colored_text("Lütfen valorantı başlatın!", 'red'))
            time.sleep(5)
            sys.exit()

        time.sleep(3)
        print(colored_text("Hile aktif edildi. Insert ile menüye ulaşabilirsiniz.", 'green'))
        time.sleep(5)
        sys.exit()

    elif choice == "2":
        print(colored_text("Çıkış yapılıyor...", 'red'))
        sys.exit()
    else:
        print(colored_text("Geçersiz seçim! Tekrar deneyin.", 'red'))
        show_menu(username)

def main():
    if os.name == 'nt':
        os.system("title Eagle Software")
        os.system("color 0f")
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                GWL_EXSTYLE = -20
                WS_EX_LAYERED = 0x80000
                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
                ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 220, 0x2)
        except:
            pass
    else:
        os.system("echo -e '\033]0;Eagle Software\007'")

    display_ascii_art()

    saved_license = load_license()
    if saved_license:
        print(colored_text(f"OTO GİRİŞ: Hesabınıza otomatik olarak giriş sağladınız.", 'green'))
        license_info = validate_license(saved_license)
        if license_info:
            start_discord_presence()
            show_menu(license_info["username"])
        else:
            print(colored_text("HATA! Lisansınız geçersiz veya süresi dolmuş. Yenileyin.", 'red'))
            license_key = get_license()
            license_info = validate_license(license_key)
            if license_info:
                save_license(license_key)
                start_discord_presence()
                show_menu(license_info["username"])
            else:
                print(colored_text("Geçersiz lisans!", 'red'))
    else:
        license_key = get_license()
        license_info = validate_license(license_key)
        if license_info:
            save_license(license_key)
            start_discord_presence()
            show_menu(license_info["username"])
        else:
            print(colored_text("Geçersiz lisans!", 'red'))

    print(colored_text("Bizi tercih ettiğiniz için teşekkürler!", 'blue'))
    msvcrt.getch()

if __name__ == "__main__":
    main()

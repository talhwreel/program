import os
import time
import datetime
import msvcrt
from pypresence import Presence

LICENSES = {
    "talhatester": {"username": "Talha", "expiration_date": "2025-12-31"},
    "woozie": {"username": "Rawien", "expiration_date": "2026-12-31"},
    "croismisin": {"username": "Crois", "expiration_date": "2025-06-30"},
}

def colored_text(text, color):
    colors = {
        'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m',
        'blue': '\033[94m', 'magenta': '\033[95m', 'cyan': '\033[96m',
        'white': '\033[97m', 'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"

def start_discord_presence():
    try:
        client_id = "1352643025288953938"
        rpc = Presence(client_id)
        rpc.connect()
        rpc.update(
            state="Developed by talhw",
            details="Bende Dark Loader kullanıyorum, sende kullanmaya ne dersin?",
            large_image="dark",
            start=time.time(),
            buttons=[
                {"label": "Discord'a Katıl", "url": "https://discord.gg/wYwKZ2gQk8"},
            ]
        )
        print(colored_text("", 'green'))
    except Exception as e:
        print(colored_text(f"Hata: {e}", 'red'))

def validate_license(license_key):
    license_info = LICENSES.get(license_key)
    
    if not license_info:
        print(colored_text("Geçersiz lisans anahtarı!", 'red'))
        return None
    
    expiration_date = datetime.datetime.strptime(license_info["expiration_date"], "%Y-%m-%d")
    if expiration_date < datetime.datetime.now():
        print(colored_text("Lisans süresi dolmuş! Discord'dan yenileyin!", 'red'))
        return None
    
    remaining_days = (expiration_date - datetime.datetime.now()).days
    print(f"\n{colored_text('Lisans süreniz:', 'yellow')} {remaining_days} gün kaldı.\n")
    return license_info

def display_ascii_art():
    art = r"""
________                __    
\______ \ _____ _______|  | __
 |    |  \\__  \\_  __ \  |/ /
 |    `   \/ __ \|  | \/    < 
/_______  (____  /__|  |__|_ \
        \/     \/           \/    
.__                    .___            
|  |   _________     __| _/___________ 
|  |  /  _ \__  \   / __ |/ __ \_  __ \
|  |_(  <_> ) __ \_/ /_/ \  ___/|  | \/
|____/\____(____  /\____ |\___  >__|   
                \/      \/    \/      
"""
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    for i in range(3):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colored_text(art, colors[i % len(colors)]))
        time.sleep(0.5)

def get_license():
    return input(colored_text("Lisans anahtarınızı girin: ", 'green'))

def flashing_text(text, duration=3, delay=0.3):
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    end_time = time.time() + duration

    while time.time() < end_time:
        for color in colors:
            print(f"\r{colored_text(text, color)}", end="", flush=True)
            time.sleep(delay)
    
    print(f"\r{colored_text(text, 'green')}")

def show_menu(username):
    print(f"\n{colored_text('Hoş geldiniz,', 'green')} {colored_text(username, 'cyan')}!")
    
    flashing_text("1. Hile menüsüne giriş sağla", duration=2)
    
    print(colored_text("\n2. Çıkış", 'red'))
    
    choice = input(colored_text("\nSeçiminizi yapınız: ", 'yellow'))
    
    if choice == "1":
        print(colored_text("\nHile menüsüne güncelleme gelmedi, güncelleme bekleniyor...", 'red'))
        time.sleep(5) 
        print(colored_text("Program kapatılıyor...", 'red'))
        exit()
    elif choice == "2":
        print(colored_text("Çıkış yapılıyor...", 'red'))
        exit()
    else:
        print(colored_text("Geçersiz seçim! Tekrar deneyin.", 'red'))
        show_menu(username) 

def main():
    if os.name == 'nt':
        os.system("title Dark Proxy V1")
        os.system("color 0f")
    else:
        os.system("echo -e '\033]0;Dark Proxy V1\007'")

    display_ascii_art()

    license_key = get_license()
    license_info = validate_license(license_key)

    if license_info:
        start_discord_presence()
        show_menu(license_info["username"])
    else:
        print(colored_text("HATA! Geçerli lisans girilmedi.", 'red'))

    print(colored_text("Bizi tercih ettiğiniz için teşekkürler!", 'blue'))
    msvcrt.getch()

if __name__ == "__main__":
    main()

import os
import hashlib
import datetime
import msvcrt
import time

licenses = {
    "talhatester": {
        "username": "Talha",
        "expiration_date": "2025-12-31"
    },
        "woozie": {
        "username": "Rawien",
        "expiration_date": "2026-12-31"
    },
    "croismisin": {
        "username": "Crois",
        "expiration_date": "2025-06-30"
    }
}

def validate_license(license_key):
    try:
        license_info = licenses.get(license_key)
        
        if not license_info:
            print(colored_text("Geçersiz lisans anahtarı!", 'red'))
            return None
        
        expiration_date = datetime.datetime.strptime(license_info["expiration_date"], "%Y-%m-%d")
        if expiration_date < datetime.datetime.now():
            print(colored_text("Lisans anahtarınızın süresi dolmuş! discord adresinden yenileyin!", 'red'))
            return None
        

        remaining_time = expiration_date - datetime.datetime.now()
        print(f"\n{colored_text('Lisansınızın geçerlilik süresi:', 'yellow')} {remaining_time.days} gün kaldı.\n")
        
        return license_info
    except Exception as e:
        print(f"{colored_text('Hata oluştu:', 'red')} {e}")
        input("Hata oluştu. Kapanmadan önce Enter'a basın...")
        return None

def colored_text(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"


def display_ascii_art():
    art = '''\033[94m
 ██████████                       █████                
░░███░░░░███                     ░░███                 
 ░███   ░░███  ██████   ████████  ░███ █████           
 ░███    ░███ ░░░░░███ ░░███░░███ ░███░░███            
 ░███    ░███  ███████  ░███ ░░░  ░██████░             
 ░███    ███  ███░░███  ░███      ░███░░███            
 ██████████  ░░████████ █████     ████ █████           
░░░░░░░░░░    ░░░░░░░░ ░░░░░     ░░░░ ░░░░░      
 ███████████                                           
░░███░░░░░███                                          
 ░███    ░███ ████████   ██████  █████ █████ █████ ████
 ░██████████ ░░███░░███ ███░░███░░███ ░░███ ░░███ ░███ 
 ░███░░░░░░   ░███ ░░░ ░███ ░███ ░░░█████░   ░███ ░███ 
 ░███         ░███     ░███ ░███  ███░░░███  ░███ ░███ 
 █████        █████    ░░██████  █████ █████ ░░███████ 
░░░░░        ░░░░░      ░░░░░░  ░░░░░ ░░░░░   ░░░░░███ 
                                              ███ ░███ 
                                             ░░██████  
                                              ░░░░░░       
\033[0m'''


    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'] 
    for i in range(10):
        color = colors[i % len(colors)]
        print(colored_text(art, color))
        time.sleep(0.5) 
        os.system('cls' if os.name == 'nt' else 'clear') 


def get_license():
    license_key = input(colored_text("Lisans anahtarınızı girin: ", 'green'))
    return license_key


def show_menu(username):
    print(f"\n{colored_text('Hoş geldiniz,', 'green')} {colored_text(username, 'cyan')}!")
    print(colored_text("1. Proxy'i çalıştır", 'green'))
    print(colored_text("2. Çıkış", 'red'))
    choice = input(colored_text("Seçim yapınız: ", 'yellow'))
    if choice == "1":
        print(colored_text("Proxy başlatılamadı, güncelleme bekleniyor.", 'red'))
    elif choice == "2":
        print(colored_text("Çıkış yapılıyor...", 'red'))
    else:
        print(colored_text("Geçersiz seçim!", 'red'))


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
        show_menu(license_info["username"])
    else:
        print(colored_text("HATA!", 'red'))

    print(colored_text("Bizi tercih ettiğiniz için teşekkür ederiz..", 'blue'))
    msvcrt.getch()

if __name__ == "__main__":
    main()

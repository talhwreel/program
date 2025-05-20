import sys
import os
import datetime
import subprocess
import threading
import time
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QSize, QPoint
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QProgressBar, QFrame
)
from PyQt5.QtGui import QColor, QPainter, QFont, QIcon, QCursor

LICENSES = {
    "k44ncal1smayan36": {"username": "Kaan", "expiration_date": "2025-12-31"},
    "berkayfull31de": {"username": "Berkay Çalışkan", "expiration_date": "2027-05-06"},
    "EAGLE-0NE1-M0NT4H": {"username": "Byghostking", "expiration_date": "2025-06-10"},
    "PRKS-EAGLE-S0FTW4RE": {"username": "SYX", "expiration_date": "2025-06-12"},
    "RJEH-EAJLE-S07TW4RE": {"username": "Enes", "expiration_date": "2025-06-13"},
    "DHWR-KTHE-S01M0NTH": {"username": "Cankong", "expiration_date": "2025-06-13"},
    "FO36-LAHI-IPFYC6DA": {"username": "Abc12", "expiration_date": "2025-06-19"},
    "7YRA-2NKT-YPN4KLYR": {"username": "Demir", "expiration_date": "2025-06-20"},
}

class ValorantWatcher(QObject):
    valorant_found = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._running = False
        self._thread = None

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._watch, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def _watch(self):
        while self._running:
            try:
                output = subprocess.check_output('tasklist', shell=True).decode(errors='ignore')
                if "VALORANT.exe" in output or "valorant.exe" in output:
                    self.valorant_found.emit()
                    break
            except subprocess.CalledProcessError:
                pass
            time.sleep(1)

class FramelessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._old_pos = None

        self.resize(420, 320)
        self.setStyleSheet("""
            QWidget#MainFrame {
                background-color: #121212;
                border-radius: 12px;
            }
            QLabel {
                color: #eee;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #222;
                border: 2px solid #333;
                border-radius: 6px;
                padding: 6px;
                color: #eee;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #00aaff;
                background-color: #1a1a1a;
            }
            QPushButton {
                background-color: #00aaff;
                border-radius: 8px;
                color: #fff;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 18px;
                border: none;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #999;
            }
            QPushButton:hover:!disabled {
                background-color: #0099dd;
                cursor: pointer;
            }
            QProgressBar {
                border: 2px solid #333;
                border-radius: 8px;
                background-color: #222;
                color: #eee;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00aaff;
                border-radius: 8px;
            }
        """)

        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setGeometry(0, 0, 420, 320)

        # Custom title bar (üst çubuk)
        self.title_bar = QFrame(self.main_frame)
        self.title_bar.setGeometry(0, 0, 420, 40)
        self.title_bar.setStyleSheet("background-color: #1a1a1a; border-top-left-radius:12px; border-top-right-radius:12px;")
        self.title_bar.mousePressEvent = self.title_mouse_press
        self.title_bar.mouseMoveEvent = self.title_mouse_move

        # Title Label
        self.title_label = QLabel("Eagle Loader", self.title_bar)
        self.title_label.setGeometry(12, 7, 200, 25)
        self.title_label.setStyleSheet("color:#00aaff; font-weight: bold; font-size: 16px;")

        # Close Button
        self.btn_close = QPushButton("✕", self.title_bar)
        self.btn_close.setGeometry(380, 5, 35, 30)
        self.btn_close.setStyleSheet("""
            QPushButton {
                color: #eee;
                background-color: transparent;
                border: none;
                font-size: 20px;
            }
            QPushButton:hover {
                color: red;
                background-color: #330000;
                border-radius: 6px;
            }
        """)
        self.btn_close.clicked.connect(self.close)

        # Lisans giriş
        self.license_label = QLabel("Lisans Anahtarı:", self.main_frame)
        self.license_label.setGeometry(20, 60, 200, 25)
        self.license_input = QLineEdit(self.main_frame)
        self.license_input.setGeometry(20, 90, 380, 30)
        self.license_input.setEchoMode(QLineEdit.Password)

        # Giriş butonu
        self.login_button = QPushButton("Giriş Yap", self.main_frame)
        self.login_button.setGeometry(20, 130, 180, 38)

        # Load Cheat butonu
        self.load_button = QPushButton("Load Cheat", self.main_frame)
        self.load_button.setGeometry(220, 130, 180, 38)
        self.load_button.setEnabled(False)

        # Durum Label
        self.status_label = QLabel("", self.main_frame)
        self.status_label.setGeometry(20, 180, 380, 40)
        self.status_label.setWordWrap(True)

        # Progress Bar
        self.progress_bar = QProgressBar(self.main_frame)
        self.progress_bar.setGeometry(20, 220, 380, 25)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        # Sinyaller
        self.login_button.clicked.connect(self.handle_login)
        self.load_button.clicked.connect(self.handle_load_cheat)

        self.license_info = None
        self.valorant_watcher = ValorantWatcher()
        self.valorant_watcher.valorant_found.connect(self.valorant_detected)

        self.loading = False
        self.cheat_loaded = False

    def title_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.globalPos()

    def title_mouse_move(self, event):
        if self._old_pos:
            delta = QPoint(event.globalPos() - self._old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPos()

    def validate_license(self, license_key):
        license_info = LICENSES.get(license_key)
        if not license_info:
            QMessageBox.warning(self, "Hata", "❌ Geçersiz lisans anahtarı!")
            return None
        expiration_date = datetime.datetime.strptime(license_info["expiration_date"], "%Y-%m-%d")
        if expiration_date < datetime.datetime.now():
            QMessageBox.warning(self, "Hata", "❌ Lisans süresi dolmuş!")
            return None
        return license_info

    def handle_login(self):
        key = self.license_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Uyarı", "Lütfen lisans anahtarını girin.")
            return
        license_info = self.validate_license(key)
        if license_info:
            self.license_info = license_info
            remaining_days = (datetime.datetime.strptime(license_info["expiration_date"], "%Y-%m-%d") - datetime.datetime.now()).days
            self.status_label.setText(f"Hoşgeldin {license_info['username']}! Lisans süresi: {remaining_days} gün.")
            self.load_button.setEnabled(True)
            self.login_button.setEnabled(False)
            self.license_input.setEnabled(False)

    def handle_load_cheat(self):
        if self.loading or self.cheat_loaded:
            return

        self.loading = True
        self.load_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("🦅 Eagle yükleniyor...")

        threading.Thread(target=self.load_sequence, daemon=True).start()

    def load_sequence(self):
        steps = 50
        for i in range(steps + 1):
            time.sleep(0.07)
            percent = int((i / steps) * 100)
            # GUI güncellemesi ana thread'de olmalı, QTimer kullanalım:
            QTimer.singleShot(0, lambda p=percent: self.progress_bar.setValue(p))

        QTimer.singleShot(0, self.loading_done)

    def loading_done(self):
        self.status_label.setText("🕹 Valorant bekleniyor..")
        self.progress_bar.setVisible(False)
        self.valorant_watcher.start()

    def valorant_detected(self):
        self.cheat_loaded = True
        self.loading = False
        self.status_label.setText("🟢 Valorant bulundu! Inject başarılı.")
        self.load_button.setText("Already Loaded")
        self.load_button.setEnabled(False)
        self.valorant_watcher.stop()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Eagle Loader")
    window = FramelessWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

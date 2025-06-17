import sys
import os
import datetime
import subprocess
import threading
import time
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QSize, QPoint, QEasingCurve, QPropertyAnimation, QRect
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QProgressBar, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QColor, QPainter, QFont, QIcon, QCursor

LICENSES = {
    "kaancalismayan31": {"username": "Kaan", "expiration_date": "2025-12-31"},
    "berkayfull31de": {"username": "Berkay Çalışkan", "expiration_date": "2027-05-06"},
    "EAGLE-0NE1-M0NT4H": {"username": "Byghostking", "expiration_date": "2025-06-10"},
    "PRKS-EAGLE-S0FTW4RE": {"username": "SYX", "expiration_date": "2025-06-12"},
    "RJEH-EAJLE-S07TW4RE": {"username": "Enes", "expiration_date": "2025-06-13"},
    "DHWR-KTHE-S01M0NTH": {"username": "Cankong", "expiration_date": "2025-06-13"},
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

        self.resize(520, 450) # Increased window size for a more spacious layout
        self.setStyleSheet("""
            /* General Styling for the Main Frame */
            QWidget#MainFrame {
                background-color: #1a1a2e; /* Dark deep blue */
                border-radius: 20px;
                border: 2px solid #3a3a50; /* Subtle but visible border */
            }

            /* Global Label Styling */
            QLabel {
                color: #e0e0e0;
                font-size: 16px;
                font-family: 'Inter', 'Segoe UI', sans-serif; /* Modern sans-serif font */
                padding: 2px;
            }

            /* Line Edit (Input Field) Styling */
            QLineEdit {
                background-color: #2b2b40;
                border: 1px solid #4a4a6e; /* Slightly darker border */
                border-radius: 12px; /* Softer rounded corners */
                padding: 12px; /* More padding */
                color: #e0e0e0;
                font-size: 16px;
                font-family: 'Inter', 'Segoe UI', sans-serif;
            }
            QLineEdit:focus {
                border-color: #7b42f6; /* Vibrant purple focus color */
                background-color: #3a3a50;
            }

            /* Push Button Styling */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7b42f6, stop:1 #a238ed); /* Dynamic purple gradient */
                border-radius: 15px; /* More rounded buttons */
                color: #ffffff;
                font-weight: bold;
                font-size: 18px;
                padding: 14px 30px; /* Increased padding for larger touch area */
                border: none;
                /* box-shadow doesn't work directly via stylesheet for all widgets in PyQt */
                /* For visual depth, rely on QGraphicsDropShadowEffect */
            }
            QPushButton:disabled {
                background: #555;
                color: #ccc;
            }
            QPushButton:hover:!disabled {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6a2ceb, stop:1 #8c26d2); /* Darker gradient on hover */
                cursor: pointer;
            }

            /* Progress Bar Styling */
            QProgressBar {
                border: 2px solid #4a4a6e;
                border-radius: 12px;
                background-color: #2b2b40;
                color: #e0e0e0;
                text-align: center;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 15px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7b42f6, stop:1 #a238ed); /* Match button gradient */
                border-radius: 10px; /* Slightly smaller to fit within main bar radius */
            }

            /* Close Button Specific Styling */
            QPushButton#btnClose {
                color: #e0e0e0;
                background-color: transparent;
                border: none;
                font-size: 26px; /* Larger icon */
                font-weight: bold;
                padding: 0px;
                border-radius: 0px;
            }
            QPushButton#btnClose:hover {
                color: #ff5757; /* Brighter red on hover */
                background-color: #3a3a50;
                border-radius: 8px;
            }

            /* Title Bar Styling */
            QFrame#titleBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33334d, stop:1 #4a4a6e); /* Darker gradient for title bar */
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
            }
        """)

        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setGeometry(0, 0, self.width(), self.height())

        # Add shadow effect to the main frame
        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.shadow_effect.setBlurRadius(30) # More pronounced shadow
        self.shadow_effect.setXOffset(0)
        self.shadow_effect.setYOffset(0)
        self.shadow_effect.setColor(QColor(0, 0, 0, 200)) # Darker shadow
        self.main_frame.setGraphicsEffect(self.shadow_effect)

        # Custom title bar
        self.title_bar = QFrame(self.main_frame)
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setGeometry(0, 0, self.width(), 55) # Taller title bar
        self.title_bar.mousePressEvent = self.title_mouse_press
        self.title_bar.mouseMoveEvent = self.title_mouse_move

        # Title Label
        self.title_label = QLabel("Eagle Loader", self.title_bar)
        self.title_label.setGeometry(30, 15, 200, 25) # Adjusted position
        self.title_label.setStyleSheet("color:#a238ed; font-weight: bold; font-size: 22px; font-family: 'Inter', sans-serif;") # Brighter purple title

        # Close Button
        self.btn_close = QPushButton("✕", self.title_bar)
        self.btn_close.setObjectName("btnClose")
        self.btn_close.setGeometry(self.width() - 55, 12, 45, 40) # Adjusted position and size
        self.btn_close.clicked.connect(self.close)

        # Main layout for content
        self.content_layout = QVBoxLayout(self.main_frame)
        self.content_layout.setContentsMargins(50, 90, 50, 50) # Increased margins for spaciousness
        self.content_layout.setSpacing(25) # Increased spacing between widgets

        # License input
        self.license_label = QLabel("License Key:", self.main_frame)
        self.license_input = QLineEdit(self.main_frame)
        self.license_input.setPlaceholderText("Enter your license key here...")

        # Buttons layout
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(20) # Spacing between buttons
        self.login_button = QPushButton("Login", self.main_frame)
        self.load_button = QPushButton("Load Cheat", self.main_frame)
        self.load_button.setEnabled(False)
        self.button_layout.addWidget(self.login_button)
        self.button_layout.addWidget(self.load_button)

        # Status Label
        self.status_label = QLabel("", self.main_frame)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Progress Bar
        self.progress_bar = QProgressBar(self.main_frame)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True) # Show percentage text

        self.content_layout.addWidget(self.license_label)
        self.content_layout.addWidget(self.license_input)
        self.content_layout.addLayout(self.button_layout)
        self.content_layout.addWidget(self.status_label)
        self.content_layout.addWidget(self.progress_bar)
        self.content_layout.addStretch()

        # Signals
        self.login_button.clicked.connect(self.handle_login)
        self.load_button.clicked.connect(self.handle_load_cheat)

        self.license_info = None
        self.valorant_watcher = ValorantWatcher()
        self.valorant_watcher.valorant_found.connect(self.valorant_detected)

        self.loading = False
        self.cheat_loaded = False

        # Animations
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(500) # Slower fade-in for elegance
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutQuad)

        self.shake_anim = QPropertyAnimation(self, b"pos")
        self.shake_anim.setDuration(250) # Shake duration
        self.shake_anim.setLoopCount(4) # More shakes
        self.shake_anim.setEasingCurve(QEasingCurve.InOutSine)

    def showEvent(self, event):
        self.fade_anim.start()
        super().showEvent(event)

    def title_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.globalPos()

    def title_mouse_move(self, event):
        if self._old_pos:
            delta = QPoint(event.globalPos() - self._old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPos()

    def shake_window(self):
        original_pos = self.pos()
        self.shake_anim.setStartValue(original_pos)
        self.shake_anim.setKeyValueAt(0.1, QPoint(original_pos.x() - 10, original_pos.y()))
        self.shake_anim.setKeyValueAt(0.2, QPoint(original_pos.x() + 10, original_pos.y()))
        self.shake_anim.setKeyValueAt(0.3, QPoint(original_pos.x() - 10, original_pos.y()))
        self.shake_anim.setKeyValueAt(0.4, QPoint(original_pos.x() + 10, original_pos.y()))
        self.shake_anim.setKeyValueAt(0.5, QPoint(original_pos.x() - 10, original_pos.y()))
        self.shake_anim.setKeyValueAt(0.6, QPoint(original_pos.x() + 10, original_pos.y()))
        self.shake_anim.setEndValue(original_pos)
        self.shake_anim.start()

    def validate_license(self, license_key):
        license_info = LICENSES.get(license_key)
        if not license_info:
            QMessageBox.warning(self, "Error", "❌ Invalid license key!")
            self.shake_window()
            return None
        expiration_date = datetime.datetime.strptime(license_info["expiration_date"], "%Y-%m-%d")
        current_time = datetime.datetime.now()
        if expiration_date < current_time:
            QMessageBox.warning(self, "Error", "❌ License expired!")
            self.shake_window()
            return None
        return license_info

    def handle_login(self):
        key = self.license_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Warning", "Please enter your license key.")
            self.shake_window()
            return
        license_info = self.validate_license(key)
        if license_info:
            self.license_info = license_info
            remaining_days = (datetime.datetime.strptime(license_info["expiration_date"], "%Y-%m-%d") - datetime.datetime.now()).days
            self.status_label.setText(f"Welcome {license_info['username']}! License expires in: {remaining_days} days.")
            self.load_button.setEnabled(True)
            self.login_button.setEnabled(False)
            self.license_input.setEnabled(False)
            self.animate_login_success()
        else:
            self.status_label.setText("Login Failed.")

    def animate_login_success(self):
        login_btn_original_geom = self.login_button.geometry()
        load_btn_original_geom = self.load_button.geometry()

        # Animate Login button to slide out and hide
        anim_login_move = QPropertyAnimation(self.login_button, b"pos")
        anim_login_move.setDuration(400)
        anim_login_move.setEasingCurve(QEasingCurve.InQuad)
        anim_login_move.setStartValue(login_btn_original_geom.topLeft())
        # Move it off to the left, and slightly up
        anim_login_move.setEndValue(login_btn_original_geom.topLeft() + QPoint(-self.login_button.width() - 100, -30))
        anim_login_move.start()
        # Hide the button after its animation completes
        anim_login_move.finished.connect(lambda: self.login_button.setVisible(False))

        # Animate Load button to grow and take the full width
        anim_load_geom = QPropertyAnimation(self.load_button, b"geometry")
        anim_load_geom.setDuration(600) # Slower and more prominent
        anim_load_geom.setEasingCurve(QEasingCurve.OutElastic)

        # Calculate the target geometry for the load button
        # It should move to the start X of the button_layout
        # and span the entire width of the content area.
        target_width = self.main_frame.width() - self.content_layout.contentsMargins().left() - self.content_layout.contentsMargins().right()
        
        # The Y position should remain the same as the original button's Y.
        button_y = load_btn_original_geom.y() 
        
        # The new X position will be the left margin of the content layout.
        new_x = self.content_layout.contentsMargins().left()
        
        new_geometry = QRect(new_x, button_y, target_width, load_btn_original_geom.height())

        anim_load_geom.setStartValue(load_btn_original_geom)
        anim_load_geom.setEndValue(new_geometry)
        anim_load_geom.start()


    def handle_load_cheat(self):
        if self.loading or self.cheat_loaded:
            return

        self.loading = True
        self.load_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0) # Ensure it starts from 0
        self.status_label.setText("🦅 Loading Eagle...")

        # Apply a prominent shadow effect to the progress bar
        self.progress_bar.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=20, xOffset=5, yOffset=5, color=QColor(0,0,0,150)))

        threading.Thread(target=self.load_sequence, daemon=True).start()

    def load_sequence(self):
        steps = 100
        for i in range(steps + 1):
            percent = int((i / steps) * 100)
            # Crucially, update the progress bar on the main UI thread.
            # Using QTimer.singleShot(0, ...) ensures this.
            QTimer.singleShot(0, lambda p=percent: self.progress_bar.setValue(p))
            time.sleep(0.04) # Slower loading to see animation clearly

        QTimer.singleShot(0, self.loading_done)

    def loading_done(self):
        self.status_label.setText("🕹 Waiting for Valorant to start...")
        self.progress_bar.setVisible(False)
        self.valorant_watcher.start()

    def valorant_detected(self):
        self.cheat_loaded = True
        self.loading = False
        self.status_label.setText("🟢 Valorant detected! Inject successful.")
        self.load_button.setText("Already Loaded")
        self.load_button.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Eagle Loader")
    window = FramelessWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from ui.dashboard import Dashboard
from ui.app_list import AppList
from ui.styles import ModernStyles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DustOff - Windows Manager")
        self.resize(1100, 800)
        self.setStyleSheet(ModernStyles.get_main_style())
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left Side (Dashboard & Quick Info)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title/Logo
        title = QLabel("DustOff")
        title.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {ModernStyles.accent_color}; margin-bottom: 20px;")
        left_layout.addWidget(title)
        
        # Dashboard Component
        self.dashboard = Dashboard()
        left_layout.addWidget(self.dashboard)
        
        left_layout.addStretch()
        
        # Motivation/Info
        info_card = QLabel("Clean your system\nBoost performance")
        info_card.setStyleSheet("color: #808080; font-style: italic;")
        left_layout.addWidget(info_card)

        # Right Side (App List)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.app_list = AppList()
        # Wrap in card style
        app_list_container = QFrame()
        app_list_container.setStyleSheet(ModernStyles.card_style())
        cont_layout = QVBoxLayout(app_list_container)
        cont_layout.addWidget(self.app_list)
        
        right_layout.addWidget(app_list_container)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1) # 1/3 width
        main_layout.addWidget(right_panel, 2) # 2/3 width

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

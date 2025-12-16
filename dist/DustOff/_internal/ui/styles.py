from PySide6.QtGui import QColor, QPalette

class ModernStyles:
    # Trend colors (Fluent-ish)
    bg_color = "#f3f3f3"
    card_color = "#ffffff"
    text_primary = "#202020"
    text_secondary = "#606060"
    accent_color = "#0067c0" # Windows 11 Blue
    accent_hover = "#1975d1"
    danger_color = "#d13438"
    
    FONT_FAMILY = "Pretendard, 'Segoe UI Variable Display', 'Segoe UI', sans-serif"
    
    @staticmethod
    def get_main_style():
        return f"""
            QMainWindow {{
                background-color: {ModernStyles.bg_color};
            }}
            QWidget {{
                font-family: "{ModernStyles.FONT_FAMILY}";
                font-size: 12px;
                color: {ModernStyles.text_primary};
            }}
            QLabel {{
                color: {ModernStyles.text_primary};
            }}
            QPushButton {{
                background-color: {ModernStyles.card_color};
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #f9f9f9;
                border-color: #d0d0d0;
            }}
            QPushButton:pressed {{
                background-color: #f0f0f0;
                border-color: #c0c0c0;
            }}
            QHeaderView::section {{
                background-color: {ModernStyles.bg_color};
                padding: 6px;
                border: none;
                font-weight: bold;
                color: {ModernStyles.text_secondary};
            }}
            QTableWidget {{
                background-color: {ModernStyles.card_color};
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                selection-background-color: {ModernStyles.accent_color};
                selection-color: white;
                gridline-color: #f0f0f0;
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """

    @staticmethod
    def card_style():
        return f"""
            QFrame {{
                background-color: {ModernStyles.card_color};
                border-radius: 12px;
                border: 1px solid #e5e5e5;
            }}
        """

    @staticmethod
    def primary_btn_style():
        return f"""
            QPushButton {{
                background-color: {ModernStyles.accent_color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {ModernStyles.accent_hover};
            }}
        """

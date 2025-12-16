from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                                 QHeaderView, QPushButton, QLabel, QHBoxLayout, QMessageBox, QFrame, QStyle)
from PySide6.QtCore import Qt, QTimer, QFileInfo
from PySide6.QtGui import QIcon
import os
import subprocess
import psutil
from core.app_scanner import AppScanner
from core.process_matcher import ProcessMatcher
from core.icon_extractor import IconExtractor
from ui.styles import ModernStyles

class AppList(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # Timer to update status potentially? For now manual refresh is safer for perf
        # But we can update status of existing rows
        self.load_apps()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Installed Applications")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; font-family: {ModernStyles.FONT_FAMILY};")
        header_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh List")
        refresh_btn.setStyleSheet(ModernStyles.primary_btn_style())
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_apps)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        # Columns: Name, Status, Version, Size, Date, Stop, Uninstall
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Name", "Status", "Version", "Size (MB)", "Date", "Stop", "Del"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)      # Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) # Status
        header.setSectionResizeMode(5, QHeaderView.Fixed) # Stop
        header.setSectionResizeMode(6, QHeaderView.Fixed) # Uninstall
        self.table.setColumnWidth(5, 50)
        self.table.setColumnWidth(6, 50)
        
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Remove Context Menu Context
        self.table.setContextMenuPolicy(Qt.NoContextMenu)
        
        layout.addWidget(self.table)
        
        # Stats Label
        self.stats_label = QLabel("Loading...")
        self.stats_label.setStyleSheet(f"color: {ModernStyles.text_secondary}; margin-top: 10px;")
        layout.addWidget(self.stats_label)

    def load_apps(self):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        self.stats_label.setText("Scanning apps...")
        QFrame.repaint(self) # Force update
        
        apps = AppScanner.get_installed_apps()
        running_procs = ProcessMatcher.get_running_processes()
        
        self.table.setRowCount(len(apps))
        
        total_size = 0
        
        for row, app in enumerate(apps):
            # 0. Name with Icon
            name_item = QTableWidgetItem(app['name'])
            name_item.setData(Qt.UserRole, app)
            
            # Extract icon from executable or use fallback
            icon_path = app.get('icon_path', '')
            if icon_path:
                icon = IconExtractor.get_icon_for_exe(icon_path, use_fallback=True)
            else:
                # No icon path in registry, use fallback
                icon = IconExtractor.get_fallback_icon()
            
            if not icon.isNull():
                name_item.setIcon(icon)
            
            self.table.setItem(row, 0, name_item)
            
            # Check if running
            pids = ProcessMatcher.find_pids_for_app(app['name'], running_procs)
            is_running = len(pids) > 0
            
            # 1. Status
            status_item = QTableWidgetItem()
            if is_running:
                status_text = f"Running ({len(pids)})"
                status_item.setText("🟢 " + status_text)
                status_item.setForeground(Qt.darkGreen)
            else:
                status_item.setText("")
            self.table.setItem(row, 1, status_item)
            
            # 2. Version
            self.table.setItem(row, 2, QTableWidgetItem(str(app.get('version', ''))))
            
            # 3. Size with comma formatting
            size = app.get('size_mb', 0)
            total_size += size
            size_item = QTableWidgetItem()
            size_item.setData(Qt.DisplayRole, size)
            size_item.setText(f"{size:,.2f}" if size > 0 else "-")
            self.table.setItem(row, 3, size_item)
            
            # 4. Date
            self.table.setItem(row, 4, QTableWidgetItem(str(app.get('install_date', ''))))
            
            # Helper for icon buttons
            def create_icon_btn(icon_type, color_base, color_hover, callback):
                btn = QPushButton()
                btn.setIcon(self.style().standardIcon(icon_type))
                btn.setFixedSize(30, 24)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color_base};
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        padding-bottom: 2px;
                    }}
                    QPushButton:hover {{ background-color: {color_hover}; }}
                """)
                btn.clicked.connect(callback)
                
                w = QWidget()
                l = QHBoxLayout(w)
                l.setContentsMargins(0, 0, 0, 0)
                l.setAlignment(Qt.AlignCenter)
                l.addWidget(btn)
                return w

            # 5. Stop Column
            if is_running:
                # SP_MediaStop or SP_DialogCloseButton
                stop_widget = create_icon_btn(QStyle.SP_MediaStop, "#fff0f0", "#ffcdd2", 
                                            lambda checked=False, p=pids: self.kill_app(p))
                self.table.setCellWidget(row, 5, stop_widget)
            
            # 6. Uninstall Column
            # SP_TrashIcon
            uninstall_widget = create_icon_btn(QStyle.SP_TrashIcon, "transparent", "#eee", 
                                             lambda checked=False, a=app: self.uninstall_app(a))
            self.table.setCellWidget(row, 6, uninstall_widget)
            
        self.stats_label.setText(f"Total Apps: {len(apps):,} | Estimated Total Size: {int(total_size):,} MB")
        self.table.setSortingEnabled(True)

    def kill_app(self, pids):
        confirm = QMessageBox.question(self, "Stop Application", 
                                     f"Are you sure you want to force stop {len(pids)} process(es)?",
                                     QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            killed = 0
            for pid in pids:
                try:
                    p = psutil.Process(pid)
                    p.terminate()
                    killed += 1
                except:
                    pass
            QMessageBox.information(self, "Result", f"Stopped {killed} processes.")
            # Refresh to update status
            self.load_apps()

    def uninstall_app(self, app_data):
        cmd = app_data.get('uninstall_string')
        if not cmd:
            QMessageBox.warning(self, "Error", "No uninstall command found for this app.")
            return
            
        confirm = QMessageBox.question(self, "Confirm Uninstall", 
                                     f"Are you sure you want to uninstall {app_data['name']}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                subprocess.Popen(cmd, shell=True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to start uninstaller: {str(e)}")

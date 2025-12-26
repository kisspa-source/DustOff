from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QProgressBar, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt, QTimer
import psutil
from core.system_info import SystemInfo
from core.memory_opt import MemoryOptimizer
from ui.styles import ModernStyles

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self._current_bar_color = None
        self._last_mem_details = None
        self._refresh_counter = 0
        self._top_process_snapshot = ([], 0)
        self.init_ui()
        
        # Timer for auto-refresh
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(3000) # Every 3 seconds

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # Memory Card
        mem_card = QFrame()
        mem_card.setFrameShape(QFrame.StyledPanel)
        mem_card.setStyleSheet(ModernStyles.card_style())
        
        card_layout = QVBoxLayout(mem_card)
        
        # Title
        title_lbl = QLabel("Memory Usage")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; border: none;")
        card_layout.addWidget(title_lbl)
        
        # Progress Bar / Gauge
        self.mem_bar = QProgressBar()
        self.mem_bar.setRange(0, 100)
        self.mem_bar.setTextVisible(True)
        self.mem_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                text-align: center;
                height: 24px;
                background-color: #f0f0f0;
            }}
            QProgressBar::chunk {{
                background-color: {ModernStyles.accent_color};
                border-radius: 5px;
            }}
        """)
        card_layout.addWidget(self.mem_bar)
        
        # Details label
        self.mem_details = QLabel("Total: - GB | Available: - GB")
        self.mem_details.setStyleSheet("color: #606060; border: none; font-size: 11px;")
        card_layout.addWidget(self.mem_details)
        
        # Optimize Button
        self.opt_btn = QPushButton("🚀 Optimize Memory")
        self.opt_btn.setStyleSheet(ModernStyles.primary_btn_style())
        self.opt_btn.setCursor(Qt.PointingHandCursor)
        self.opt_btn.clicked.connect(self.run_optimization)
        card_layout.addWidget(self.opt_btn)
        
        layout.addWidget(mem_card)
        
        # Running Apps Card
        running_card = QFrame()
        running_card.setFrameShape(QFrame.StyledPanel)
        running_card.setStyleSheet(ModernStyles.card_style())
        running_card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        running_layout = QVBoxLayout(running_card)
        
        # Title
        running_title = QLabel("Running Apps (Top Memory)")
        running_title.setStyleSheet("font-size: 14px; font-weight: bold; border: none;")
        running_layout.addWidget(running_title)
        
        # Scroll Area for list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        self.running_list_widget = QWidget()
        self.running_list_layout = QVBoxLayout(self.running_list_widget)
        self.running_list_layout.setSpacing(4)
        self.running_list_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll.setWidget(self.running_list_widget)
        running_layout.addWidget(scroll)
        
        # Total memory usage label
        self.total_mem_label = QLabel("Total: - MB")
        self.total_mem_label.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {ModernStyles.text_secondary}; border: none; padding-top: 8px; border-top: 1px solid #e0e0e0;")
        self.total_mem_label.setAlignment(Qt.AlignRight)
        running_layout.addWidget(self.total_mem_label)
        
        layout.addWidget(running_card)
        
        self.refresh_stats()

    def refresh_stats(self):
        self._refresh_counter += 1
        try:
            info = SystemInfo.get_memory_info()
            percent = int(info['percent'])
            total_gb = round(info['total'] / (1024**3), 2)
            avail_gb = round(info['available'] / (1024**3), 2)
             
            self.mem_bar.setValue(percent)
            details_text = f"Total: {total_gb} GB  |  Available: {avail_gb} GB"
            if details_text != self._last_mem_details:
                self.mem_details.setText(details_text)
                self._last_mem_details = details_text
            
            # Change color if high usage
            if percent > 80:
                color = ModernStyles.danger_color
            else:
                color = ModernStyles.accent_color
                
            if color != self._current_bar_color:
                self.mem_bar.setStyleSheet(f"""
                    QProgressBar {{
                        border: 1px solid #e0e0e0;
                        border-radius: 6px;
                        text-align: center;
                        height: 24px;
                        background-color: #f0f0f0;
                    }}
                    QProgressBar::chunk {{
                        background-color: {color};
                        border-radius: 5px;
                    }}
                """)
                self._current_bar_color = color
            
            # Update running apps list every other tick to reduce overhead
            if self._refresh_counter == 1 or self._refresh_counter % 2 == 0:
                self._update_running_apps()
            
        except Exception:
            pass

    def _update_running_apps(self):
        """Update the running apps memory list"""
        # Clear existing items
        while self.running_list_layout.count():
            child = self.running_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Get top memory-consuming processes
        try:
            procs = []
            for p in psutil.process_iter(['name', 'memory_info'], ad_value=None):
                mem_info = p.info.get('memory_info')
                name = p.info.get('name')
                if not mem_info or not name:
                    continue

                mem_mb = mem_info.rss / (1024 * 1024)
                if mem_mb > 10:  # Only show apps using > 10 MB
                    procs.append({
                        'name': name,
                        'mem_mb': mem_mb
                    })
            
            # Sort by memory and take top 10
            procs.sort(key=lambda x: x['mem_mb'], reverse=True)
            top_procs = procs[:10]

            snapshot = ([(p['name'], round(p['mem_mb'], 1)) for p in top_procs], round(sum(p['mem_mb'] for p in top_procs), 1))
            if snapshot == self._top_process_snapshot:
                return
            self._top_process_snapshot = snapshot
            
            for proc in top_procs:
                row = QWidget()
                row_layout = QHBoxLayout(row)
                row_layout.setContentsMargins(4, 2, 4, 2)
                row_layout.setSpacing(8)
                
                name_lbl = QLabel(proc['name'])
                name_lbl.setStyleSheet("border: none; font-size: 11px;")
                name_lbl.setFixedWidth(120)
                name_lbl.setToolTip(proc['name'])
                row_layout.addWidget(name_lbl)
                
                mem_lbl = QLabel(f"{proc['mem_mb']:,.0f} MB")
                mem_lbl.setStyleSheet(f"border: none; color: {ModernStyles.accent_color}; font-size: 11px; font-weight: bold;")
                mem_lbl.setAlignment(Qt.AlignRight)
                row_layout.addWidget(mem_lbl)
                
                self.running_list_layout.addWidget(row)
            
            # Calculate total memory from top 10
            total_mem = sum(p['mem_mb'] for p in top_procs)
            self.total_mem_label.setText(f"Top 10 Total: {total_mem:,.0f} MB")
            
            # Add stretch at the end
            self.running_list_layout.addStretch()
            
        except Exception:
            pass

    def run_optimization(self):
        self.opt_btn.setEnabled(False)
        self.opt_btn.setText("Optimizing...")
        QTimer.singleShot(100, self._optimize_task)
        
    def _optimize_task(self):
        success, fail = MemoryOptimizer.optimize_memory()
        self.opt_btn.setText(f"Done! ({success} apps optimized)")
        self.refresh_stats()
        QTimer.singleShot(2000, lambda: self.opt_btn.setText("🚀 Optimize Memory"))
        self.opt_btn.setEnabled(True)

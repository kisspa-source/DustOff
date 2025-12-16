# DustOff - Windows App Manager & Memory Optimizer

![Platform](https://img.shields.io/badge/platform-Windows%2011-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A modern Windows 11 application manager and memory optimizer with a clean, trendy UI.

## Features

### 📊 Memory Dashboard
- Real-time memory usage monitoring
- Visual progress bar with color indicators (blue/red)
- One-click memory optimization
- Top 10 memory-consuming processes list

### 📦 Application Manager  
- Scan and list all installed applications
- Display app icons extracted from executables
- Show version, size, and install date
- Detect running applications with process count
- Sort by any column
- Quick uninstall option

### ⚡ Memory Optimization
- Clear working set for all processes
- Instant RAM recovery
- Visual feedback on optimization results

## Screenshots

*Application interface with memory dashboard and app list*

## Installation

### From Source
```bash
# Clone the repository
git clone https://github.com/yourusername/DustOff.git
cd DustOff

# Install dependencies
pip install PySide6 psutil wmi pywin32

# Run the application
python main.py
```

### Standalone Executable
Download the latest release from the `dist/DustOff` folder and run `DustOff.exe`.

## Building the Executable

```bash
pip install pyinstaller
pyinstaller --noconfirm --clean --windowed --name DustOff --add-data "ui;ui" --add-data "core;core" main.py
```

The executable will be created in `dist/DustOff/DustOff.exe`.

## Project Structure

```
DustOff/
├── main.py                 # Application entry point
├── core/
│   ├── app_scanner.py      # Windows registry app scanner
│   ├── icon_extractor.py   # Windows icon extraction
│   ├── memory_opt.py       # Memory optimization logic
│   ├── process_matcher.py  # Running process matcher
│   └── system_info.py      # System information retrieval
├── ui/
│   ├── app_list.py         # Application list widget
│   ├── dashboard.py        # Memory dashboard widget
│   ├── main_window.py      # Main window container
│   └── styles.py           # UI styles and themes
└── dist/
    └── DustOff/
        └── DustOff.exe     # Standalone executable
```

## Requirements

- Windows 10/11
- Python 3.10+ (for source)
- Dependencies:
  - PySide6
  - psutil
  - pywin32
  - wmi

## Tech Stack

- **GUI Framework**: PySide6 (Qt for Python)
- **System APIs**: psutil, win32gui, winreg
- **Packaging**: PyInstaller

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

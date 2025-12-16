import os
import tempfile
from PySide6.QtGui import QIcon, QPixmap, QImage
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QStyle, QApplication

try:
    import win32gui
    import win32ui
    import win32con
    import win32api
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

class IconExtractor:
    _cache = {}  # Cache extracted icons
    _fallback_icon = None  # Cached fallback icon
    
    @staticmethod
    def get_fallback_icon() -> QIcon:
        """Get a standard application icon as fallback"""
        if IconExtractor._fallback_icon is None:
            # Use standard Windows application icon
            app = QApplication.instance()
            if app:
                IconExtractor._fallback_icon = app.style().standardIcon(QStyle.SP_ComputerIcon)
        return IconExtractor._fallback_icon or QIcon()
    
    @staticmethod
    def get_icon_for_exe(exe_path: str, use_fallback: bool = True) -> QIcon:
        """
        Extract icon from an executable file.
        Returns a QIcon object, or fallback icon if extraction fails.
        
        Reasons for missing icons:
        1. No DisplayIcon in registry
        2. Path doesn't exist (uninstalled/moved)
        3. Not an exe/ico file
        4. Icon extraction API failure
        """
        if not exe_path:
            return IconExtractor.get_fallback_icon() if use_fallback else QIcon()
        
        if not HAS_WIN32:
            return IconExtractor.get_fallback_icon() if use_fallback else QIcon()
        
        # Clean path
        exe_path = exe_path.strip('"').strip()
        
        # Remove icon index if present (e.g., "C:\path\app.exe,0")
        icon_index = 0
        if ',' in exe_path:
            parts = exe_path.rsplit(',', 1)
            exe_path = parts[0]
            try:
                icon_index = int(parts[1])
            except ValueError:
                icon_index = 0
        
        # Check cache
        cache_key = f"{exe_path}:{icon_index}"
        if cache_key in IconExtractor._cache:
            return IconExtractor._cache[cache_key]
        
        if not os.path.exists(exe_path):
            result = IconExtractor.get_fallback_icon() if use_fallback else QIcon()
            IconExtractor._cache[cache_key] = result
            return result
        
        try:
            # Extract icon at specified index
            large_icons, small_icons = win32gui.ExtractIconEx(exe_path, icon_index, 1)
            
            if large_icons and large_icons[0]:
                icon_handle = large_icons[0]
                
                # Convert to QIcon via QPixmap
                qicon = IconExtractor._hicon_to_qicon(icon_handle)
                
                # Destroy icon handles
                for ico in large_icons:
                    if ico:
                        win32gui.DestroyIcon(ico)
                for ico in small_icons:
                    if ico:
                        win32gui.DestroyIcon(ico)
                
                if not qicon.isNull():
                    IconExtractor._cache[cache_key] = qicon
                    return qicon
            
            # If extraction failed, try index 0 as fallback
            if icon_index != 0:
                large_icons, small_icons = win32gui.ExtractIconEx(exe_path, 0, 1)
                if large_icons and large_icons[0]:
                    qicon = IconExtractor._hicon_to_qicon(large_icons[0])
                    for ico in large_icons:
                        if ico:
                            win32gui.DestroyIcon(ico)
                    for ico in small_icons:
                        if ico:
                            win32gui.DestroyIcon(ico)
                    if not qicon.isNull():
                        IconExtractor._cache[cache_key] = qicon
                        return qicon
            
            # Fallback
            result = IconExtractor.get_fallback_icon() if use_fallback else QIcon()
            IconExtractor._cache[cache_key] = result
            return result
            
        except Exception:
            result = IconExtractor.get_fallback_icon() if use_fallback else QIcon()
            IconExtractor._cache[cache_key] = result
            return result
    
    @staticmethod
    def _hicon_to_qicon(hicon) -> QIcon:
        """Convert Windows HICON to QIcon"""
        try:
            # Get icon info
            icon_info = win32gui.GetIconInfo(hicon)
            hbmColor = icon_info[4]  # Color bitmap
            
            # Get bitmap info
            bmp = win32ui.CreateBitmapFromHandle(hbmColor)
            bmp_info = bmp.GetInfo()
            width = bmp_info['bmWidth']
            height = bmp_info['bmHeight']
            
            # Create device context
            hdc = win32gui.GetDC(0)
            dc = win32ui.CreateDCFromHandle(hdc)
            memdc = dc.CreateCompatibleDC()
            
            # Create bitmap
            bitmap = win32ui.CreateBitmap()
            bitmap.CreateCompatibleBitmap(dc, width, height)
            memdc.SelectObject(bitmap)
            
            # Draw icon
            memdc.DrawIcon((0, 0), hicon)
            
            # Get bitmap bits
            bmpstr = bitmap.GetBitmapBits(True)
            
            # Create QImage from bitmap data
            qimage = QImage(bmpstr, width, height, QImage.Format_ARGB32)
            qimage = qimage.mirrored(False, True)  # Flip vertically
            
            # Clean up
            memdc.DeleteDC()
            win32gui.ReleaseDC(0, hdc)
            win32gui.DeleteObject(icon_info[3])  # hbmMask
            win32gui.DeleteObject(hbmColor)
            
            return QIcon(QPixmap.fromImage(qimage))
            
        except Exception:
            return QIcon()
    
    @staticmethod
    def _get_shell_icon(path: str) -> QIcon:
        """Get shell icon for a file"""
        try:
            import win32com.shell.shell as shell
            import win32com.shell.shellcon as shellcon
            
            # This is a fallback, less reliable but sometimes works
            return QIcon()
        except:
            return QIcon()

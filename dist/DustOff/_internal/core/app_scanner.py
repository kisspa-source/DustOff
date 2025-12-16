import winreg
import datetime

class AppScanner:
    @staticmethod
    def get_installed_apps():
        """
        Scans Windows Registry for installed applications.
        Returns a list of dictionaries with app details.
        """
        apps = []
        uninstall_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        # HKLM scanning
        for path in uninstall_paths:
            AppScanner._scan_key(winreg.HKEY_LOCAL_MACHINE, path, apps)
            
        # HKCU scanning (for per-user apps)
        AppScanner._scan_key(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", apps)
        
        # Remove duplicates based on DisplayName and verify essential data
        unique_apps = {}
        for app in apps:
            name = app.get("name")
            if name and name not in unique_apps:
                unique_apps[name] = app
                
        return list(unique_apps.values())

    @staticmethod
    def _scan_key(hive, subkey_path, apps_list):
        try:
            with winreg.OpenKey(hive, subkey_path, 0, winreg.KEY_READ) as key:
                count = winreg.QueryInfoKey(key)[0]
                for i in range(count):
                    try:
                        sub_key_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sub_key_name) as sub_key:
                            try:
                                display_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                            except FileNotFoundError:
                                continue # Name is mandatory

                            app_data = {"name": display_name}
                            
                            # Optional fields
                            try:
                                app_data["version"] = winreg.QueryValueEx(sub_key, "DisplayVersion")[0]
                            except FileNotFoundError:
                                app_data["version"] = "N/A"
                                
                            try:
                                app_data["publisher"] = winreg.QueryValueEx(sub_key, "Publisher")[0]
                            except FileNotFoundError:
                                app_data["publisher"] = "Unknown"
                                
                            try:
                                app_data["install_date"] = winreg.QueryValueEx(sub_key, "InstallDate")[0]
                                # Format YYYYMMDD to YYYY-MM-DD
                                if len(app_data["install_date"]) == 8:
                                    d = app_data["install_date"]
                                    app_data["install_date"] = f"{d[0:4]}-{d[4:6]}-{d[6:8]}"
                            except FileNotFoundError:
                                app_data["install_date"] = "Unknown"
                                
                            try:
                                app_data["uninstall_string"] = winreg.QueryValueEx(sub_key, "UninstallString")[0]
                            except FileNotFoundError:
                                app_data["uninstall_string"] = ""

                            try:
                                # EstimatedSize is usually in KB
                                size_kb = winreg.QueryValueEx(sub_key, "EstimatedSize")[0]
                                app_data["size_mb"] = round(size_kb / 1024, 2)
                            except FileNotFoundError:
                                app_data["size_mb"] = 0

                            try:
                                # DisplayIcon contains exe path, sometimes with index
                                app_data["icon_path"] = winreg.QueryValueEx(sub_key, "DisplayIcon")[0]
                            except FileNotFoundError:
                                app_data["icon_path"] = ""

                            apps_list.append(app_data)
                    except OSError:
                        continue
        except OSError:
            pass

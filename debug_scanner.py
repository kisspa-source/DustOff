from core.app_scanner import AppScanner
import sys

print("Starting scan...", file=sys.stderr)
apps = AppScanner.get_installed_apps()
print(f"Total apps found: {len(apps)}", file=sys.stderr)
for app in apps[:5]:
    print(app, file=sys.stderr)

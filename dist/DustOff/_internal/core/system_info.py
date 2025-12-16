import psutil
import platform

class SystemInfo:
    @staticmethod
    def get_memory_info():
        """
        Returns a dictionary containing memory information:
        - total: Total physical memory in bytes
        - available: Available memory in bytes
        - percent: Percentage of memory used
        """
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent
        }

    @staticmethod
    def get_os_info():
        """Returns basic OS information string"""
        return f"{platform.system()} {platform.release()} ({platform.version()})"

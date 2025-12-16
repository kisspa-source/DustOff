import psutil
import ctypes
from ctypes import wintypes

# Define necessary Windows API structures and constants
PROCESS_SET_QUOTA = 0x0100
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

class MemoryOptimizer:
    @staticmethod
    def optimize_memory():
        """
        Attempts to reduce memory usage by emptying the working set 
        for all accessible processes.
        Returns a tuple: (freed_memory_estimate_mb, success_count, fail_count)
        Note: Exact freed memory is hard to calculate without snapshots, 
        so we'll return the number of processes optimized.
        """
        success_count = 0
        fail_count = 0
        
        # Helper to call EmptyWorkingSet
        def empty_working_set(pid):
            try:
                handle = ctypes.windll.kernel32.OpenProcess(
                    PROCESS_SET_QUOTA | PROCESS_QUERY_INFORMATION, False, pid
                )
                if not handle:
                    return False
                
                result = ctypes.windll.psapi.EmptyWorkingSet(handle)
                ctypes.windll.kernel32.CloseHandle(handle)
                return result != 0
            except Exception:
                return False

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pid = proc.info['pid']
                if pid == 0 or pid == 4: # Skip System Idle and System
                    continue
                
                if empty_working_set(pid):
                    success_count += 1
                else:
                    fail_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                fail_count += 1
                continue
                
        return success_count, fail_count

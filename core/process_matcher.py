import psutil

class ProcessMatcher:
    @staticmethod
    def get_running_processes():
        """
        Returns a dictionary of {process_name_lower: [pid, ...]}
        """
        procs = {}
        for p in psutil.process_iter(['pid', 'name']):
            try:
                name = p.info['name'].lower().replace('.exe', '')
                pid = p.info['pid']
                if name in procs:
                    procs[name].append(pid)
                else:
                    procs[name] = [pid]
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return procs

    @staticmethod
    def find_pids_for_app(app_name, running_procs):
        """
        Tries to find pids for a given app name (registry display name).
        Simple heuristic: check if process name is part of app name or vice versa.
        """
        app_name_clean = app_name.lower()
        matched_pids = []
        
        # Common mappings (manual overrides for popular apps)
        mappings = {
            'google chrome': 'chrome',
            'microsoft edge': 'msedge',
            'firefox': 'firefox',
            'discord': 'discord',
            'spotify': 'spotify',
            'notepad': 'notepad',
            'calculator': 'calculator',
            'visual studio code': 'code',
            'vlc media player': 'vlc',
        }
        
        # Check explicit mapping first
        for key, val in mappings.items():
            if key in app_name_clean:
                if val in running_procs:
                    matched_pids.extend(running_procs[val])
        
        # If found via mapping, return
        if matched_pids:
            return list(set(matched_pids))

        # Fallback: Fuzzy match
        # This can be risky (false positives), so we be conservative.
        # We check if strict words match.
        app_words = set(app_name_clean.split())
        
        for proc_name, pids in running_procs.items():
            # Check for exact word match
            # e.g. proc="code" -> app="Visual Studio Code" (Code is in app name)
            # e.g. proc="slack" -> app="Slack"
            if proc_name in app_words:
                 matched_pids.extend(pids)
            # Check if proc name is the app name (minus spaces)
            elif proc_name == app_name_clean.replace(" ", ""):
                matched_pids.extend(pids)

        return list(set(matched_pids))

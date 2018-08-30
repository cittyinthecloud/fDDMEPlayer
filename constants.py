from pathlib import Path

modspath = Path.cwd()/"mods"
PATTERNS = ("options.rpyc", "*.rpa", "options.rpy")

class InvalidModError(Exception):
    pass

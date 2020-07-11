import sys
from pathlib import Path

ROOT = str((Path('..')).absolute().parent)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

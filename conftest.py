"""Put the repo root on sys.path so tests import src/ without an install step.

An editable install is not durable here: a hidden .pth file has gone missing on
this machine more than once. This is the fix that stays fixed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

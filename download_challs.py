"""
SIMPLE SCRIPT TO DOWNLOAD CHALLENGES FROM VM.
(RUN IT ON YOUR PC)
"""

import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent
CHALLS_DIR = BASE_DIR / "challs"


def main():
    subprocess.run(["scp", "-r",  "root@10.60.11.1", str(CHALLS_DIR)])

if __name__ == "__main__":
    main()

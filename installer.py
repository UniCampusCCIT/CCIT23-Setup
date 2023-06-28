import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent
TOOLS_DIR = BASE_DIR / "UnicampusTools"

TOOLS = ["https://github.com/eciavatta/caronte"]


def install_github_repo(repo_url: str, install_path: Path):
    # Clone the GitHub repository
    subprocess.run(["git", "clone", repo_url, str(install_path)])

    # Change to the installation directory
    os.chdir(str(install_path))

    # Install the repository's content
    subprocess.run(["pip", "install", "-r", "requirements.txt"])  # Assuming a requirements.txt file is present
    subprocess.run(["python", "setup.py", "install"])  # Assuming a setup.py file is present


    # Build containers
    subprocess.run(["docker-compose", "up", "-d"])


if __name__ == "__main__":
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script")

    for repo_url in TOOLS:
        install_github_repo(repo_url, TOOLS_DIR)

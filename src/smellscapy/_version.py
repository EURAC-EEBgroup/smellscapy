# smellscapy/version.py
from pathlib import Path
import tomllib as tomli  

pyproject_path = Path(__file__).resolve().parent.parent.parent / "pyproject.toml"

with pyproject_path.open("rb") as f:
    pyproject_data = tomli.load(f)

__version__ = pyproject_data["project"]["version"]

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'solar_ems.db'}")
APP_NAME = "Solar ESS EMS Local API"

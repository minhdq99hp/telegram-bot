import os
from pathlib import Path
from dotenv import load_dotenv
from pytz import timezone
from app.utilities.file_util import load_yaml


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.join(BASE_DIR, "data")

load_dotenv(os.path.join(BASE_DIR, '.env'))

TIMEZONE = timezone('Asia/Ho_Chi_Minh')

CONFIG = load_yaml(os.path.join(DATA_DIR, 'config.yaml'))

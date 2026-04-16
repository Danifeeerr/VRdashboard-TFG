import os
import sys
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(base_path, ".env"))
API_BASE = os.getenv("API_BASE", "http://localhost:8000")
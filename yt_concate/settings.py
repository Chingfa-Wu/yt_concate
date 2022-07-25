from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

DOWNLOADS_DIR = 'downloads'
CAPTIONS_DIR = os.path.join(DOWNLOADS_DIR, 'caption')
VIDEOS_DIR = os.path.join(DOWNLOADS_DIR, "videos")

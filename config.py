from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / 'kimstudy_state.json'
DEBUG_DIR = BASE_DIR / 'debug'
SEARCH_URL = 'https://kimstudy.com/tutee/list?subject=d09bcf02-4b96-e811-a6f8-66f24638ceae&subject=27757807-614d-4956-819f-eba0a08a0ab0&subject=0906b1e7-ba45-40e3-81a8-6b5685a7af35&subject=17c705fc-36d1-e411-9018-cafe0600b00b&subject=f89b04a0-7fbf-47a7-a61a-c62f976f0d4b&subject=51822a75-1b27-4940-8ab7-d6eb663fc6df&subject=904a322b-f955-e511-9d0a-66f24638ceae&subject=b5e9b782-8609-4f0a-a211-b8005aef72b2&subject=d1ce8878-c519-4642-9623-32f805daf060&subject=3006f536-4a96-e811-a6f8-66f24638ceae&subject=21267109-4b96-e811-a6f8-66f24638ceae&method=online&keyword=%ED%95%99%EC%A2%85&page=1'
NOTION_TOKEN = os.getenv('NOTION_TOKEN','')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID','2a2fb348-a48a-4f71-a812-27a5169d599a')
NOTION_DATA_SOURCE_ID = os.getenv('NOTION_DATA_SOURCE_ID','')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN','')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID','')
POLL_SECONDS = int(os.getenv('POLL_SECONDS','600'))

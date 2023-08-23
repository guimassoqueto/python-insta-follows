from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOFOLLOW_FILE = "tofollow.txt"
FOLLOWING_FILE = "following.txt"

INSTAGRAM_USER = getenv("INSTAGRAM_USER") or ""
INSTAGRAM_PASSWORD = getenv("INSTAGRAM_PASSWORD") or ""
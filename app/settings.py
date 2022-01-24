import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), verbose=True)

FILE_STORAGE = os.getenv("FILE_STORAGE")

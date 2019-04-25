from app import app

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
print(f'Loading environment from: {find_dotenv()}')

from os import getenv

from dotenv import load_dotenv

load_dotenv()

executable_path = getenv("EXECUTABLE_PATH")
login = getenv("LOGIN")
password = getenv("PASSWORD")
token = getenv("TOKEN")

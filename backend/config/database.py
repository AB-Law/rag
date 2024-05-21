from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

class dbConfig:
    SERVER_HOST = os.getenv('SERVER_HOST')
    SERVER_DATABASE = os.getenv('SERVER_DATABASE')
    SERVER_USERNAME = os.getenv('SERVER_USERNAME')
    SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')
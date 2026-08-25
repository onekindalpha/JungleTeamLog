import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DB_NAME", "jungle_teamlog")]

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_teamlog"]

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
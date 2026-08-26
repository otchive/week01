import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-temp-key")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/wardrobe")

    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
    AWS_REGION = os.environ.get("AWS_REGION", "ap-northeast-2")
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

import os
import pytz
from dotenv import load_dotenv

load_dotenv()

TIMEZONE = pytz.timezone(os.getenv('TIMEZONE'))
REFRESH_TIME = int(os.getenv('REFRESH_TIME'))
ACCESS_TIME = int(os.getenv('ACCESS_TIME'))
SECRET_KEY =  os.getenv('SECRET_KEY')

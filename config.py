import datetime
from dotenv import load_dotenv
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

# .envファイルのパスを作成
dotenv_path = os.path.join(script_dir, '.env')

# .envファイルを読み込む
load_dotenv(dotenv_path)
URL = os.getenv('URL')
USER_ID = os.getenv('USER_ID')
PASSWORD = os.getenv('PASSWORD')
MENU = os.getenv('MENU')
LOGIN_BUTTON = os.getenv('LOGIN_BUTTON')
TUTORIAL_START = os.getenv('TUTORIAL_START')
TUTORIAL_SKIP = os.getenv('TUTORIAL_SKIP')
SHADOW_ROOT = os.getenv('SHADOW_ROOT')
END_GUIDE = os.getenv('END_GUIDE')
EXPORT = os.getenv('EXPORT')
TIME_CARD = os.getenv('TIME_CARD')
SCHEDULE = os.getenv('SCHEDULE')
CARD_EXPORT = os.getenv('CARD_EXPORT')
CARD_RESULT = os.getenv('CARD_RESULT')
MONTHLY_DATA = os.getenv('MONTHLY_DATA')
MONTHLY_DATA_EXPORT = os.getenv('MONTHLY_DATA_EXPORT')
DATA_DISPLAY = os.getenv('DATA_DISPLAY')
MONTHLY_DATA_CSV = os.getenv('MONTHLY_DATA_CSV')
SCHEDULE_PRINT = os.getenv('SCHEDULE_PRINT')
RESULT_BUTTON = os.getenv('RESULT_BUTTON')
SELECT_LAYOUT = os.getenv('SELECT_LAYOUT')


# window.py
select_list = ['一括',"タイムカード", "月別予定(XLS)", "月別予定(CSV)",'スケジュール']
month_list = [f"{month}月" for month in range(1,13)]
year_list = [f"{year}年" for year in range(2020, int(datetime.datetime.now().year + 1))]

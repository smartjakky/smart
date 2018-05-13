import os
import logging

console = logging.StreamHandler()
fomatter = logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(message)s')
console.setFormatter(fomatter)
console.setLevel(logging.INFO)
logger = logging.getLogger()
logger.addHandler(console)
logger.setLevel(logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
HEADERS = {
        'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/61.0.3163.100 Safari/537.36',
        'Cache-Control': 'no-cache'
}
LOCATIONS = {
    '0_0_0_0_0_0_289_0_0_2': '广州',
    '0_0_0_0_0_0_291_0_0_2': '深圳',
    '0_0_0_0_0_0_310_0_0_2': '南宁'
}
ROOT_URL = 'http://y.soyoung.com/hospital/'
LEVEL_1_DIR = os.path.join(DOWNLOAD_DIR, 'level-1')
LEVEL_2_DIR = os.path.join(DOWNLOAD_DIR, 'level-2')

if not os.path.exists(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)

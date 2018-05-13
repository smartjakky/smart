import os

from lxml.html import etree
from pymongo import MongoClient
from config import LEVEL_2_DIR, logger


def get_path_and_name(abspath):
    path = os.path.dirname(abspath)
    name = abspath.split(path)[-1]
    name = name.strip('\\\\')
    name = name.strip('/')
    return path, name


class Parser(object):
    def __init__(self):
        self.client = MongoClient(host='localhost', port=27017)
        self.db = self.client.get_database('app')
        self.db.drop_collection('hospital')
        self.db.create_collection('hospital')
        self.collection = self.db.get_collection('hospital')

    def parse(self):
        for abspath, dirs, files in list(os.walk(LEVEL_2_DIR))[1:]:
            foldername = get_path_and_name(abspath)[1]
            for file in files:
                logger.info('解析文件(%s)中....' % file)
                file_abspath = os.path.join(abspath, file)
                with open(file_abspath, 'r', encoding='utf-8') as f:
                    html = f.read()
                self.parse_page_and_save_to_mongo(area=foldername, html=html)

    def parse_page_and_save_to_mongo(self, area, html):
        tree = etree.HTML(html)
        history_lis = tree.xpath("//ul[@class='filter_list narrow_filter']/li")
        for history_li in history_lis:
            name = history_li.xpath("div[@class='content']/div[@class='name']/a/text()")[0]
            qualification = history_li.xpath("div[@class='content']/p[1]/text()")[0]
            if history_li.xpath("div[@class='content']/p[@class='text arrDivShow']/text()"):
                address = history_li.xpath("div[@class='content']/p[@class='text arrDivShow']/text()")[0]
            else:
                address = None
            good_at = []
            for item in history_li.xpath("div[@class='content']/p[3]/a/text()"):
                good_at.append(item.strip())
            data = dict(
                area=area,
                name=name,
                qualification=qualification,
                address=address,
                good_at=good_at
            )
            logger.info(data)
            self.collection.insert(data)

    def __del__(self):
        self.client.close()

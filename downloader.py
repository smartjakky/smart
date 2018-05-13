import requests
import os

from urllib.parse import urljoin
from lxml.html import etree
from config import (HEADERS, LOCATIONS, ROOT_URL, LEVEL_1_DIR, LEVEL_2_DIR, logger)


class DownLoader(object):

    def __init__(self):
        if not os.path.exists(LEVEL_1_DIR):
            os.mkdir(LEVEL_1_DIR)
        if not os.path.exists(LEVEL_2_DIR):
            os.mkdir(LEVEL_2_DIR)

    @property
    def client(self):
        c = requests.session()
        c.headers.update(HEADERS)
        return c

    @staticmethod
    def _get_page_count(area):
        filename = os.path.join(LEVEL_1_DIR, area + '.html')
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        html = etree.HTML(content)
        count = html.xpath("//div[@id='yw0']/a[last()-1]/text()")[0]
        return int(count)

    def download_level_1_page(self, path, area):
        filename = os.path.join(LEVEL_1_DIR, area + '.html')
        url = urljoin(ROOT_URL, path)
        logger.info(
            '页面链接: %s\n'
            '保存路径: %s\n' % (url, filename)
        )
        html = self.client.get(url, timeout=5).content.decode()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

    def download_all_level_1(self):
        logger.info('-=-=-=-=--=-=-=-=-开始抓取一级页面-=-=-=-=--=-=-=-=-')
        for path, area in LOCATIONS.items():
            self.download_level_1_page(path, area)
        logger.info('-=-=-=-=--=-=-=-=-一级页面抓取完毕-=-=-=-=--=-=-=-=-')

    def download_level_2_page(self, path, area, page):
        if not os.path.exists(os.path.join(LEVEL_2_DIR, area)):
            os.mkdir(os.path.join(LEVEL_2_DIR, area))
        filename = os.path.join(LEVEL_2_DIR, area, '%s_%s.html' % (area, page))
        url = urljoin(ROOT_URL, path)
        logger.info(
            '页面链接: %s\n'
            '保存路径: %s\n' % (url, filename)
        )
        html = self.client.get(url, timeout=5).content.decode()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

    def download_all_level_2(self):
        logger.info('-=-=-=-=--=-=-=-=-开始抓取二级页面-=-=-=-=--=-=-=-=-\n')
        for path, area in LOCATIONS.items():
            count = self._get_page_count(area)
            for page in range(1, count + 1):
                new_path = path + '/' + str(page)
                self.download_level_2_page(new_path, area, page)
        logger.info('-=-=-=-=--=-=-=-=-二级页面抓取完毕-=-=-=-=--=-=-=-=-\n')

    def download(self):
        self.download_all_level_1()
        self.download_all_level_2()

from downloader import DownLoader
from level_parser import Parser


class Scheduler(object):
    def __init__(self):
        self.downloader = DownLoader()
        self.parser = Parser()

    def download_page(self):
        self.downloader.download()

    def parse_and_save(self):
        self.parser.parse()

    def run(self):
        self.download_page()
        self.parse_and_save()


def main():
    scheduler = Scheduler()
    scheduler.run()


if __name__ == '__main__':
    main()

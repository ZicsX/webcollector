from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .async_spider import AsyncSpider

def run_spider(url):
    process = CrawlerProcess(get_project_settings())
    process.crawl(AsyncSpider, url=url)
    process.start()

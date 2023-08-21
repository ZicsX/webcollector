# async_crawler/spiders/async_spider.py

import scrapy
import aiohttp

class AsyncSpider(scrapy.Spider):
    name = 'async_spider'
    custom_settings = {
        'CONCURRENT_REQUESTS': 100,  # Adjust as needed
    }

    def __init__(self, url=None, *args, **kwargs):
        super(AsyncSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]

    async def fetch(self, url, spider):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def parse(self, response):
        # Sample extraction of all links from a page
        for link in response.css('a::attr(href)').extract():
            yield {
                'link': link
            }
            next_page = response.urljoin(link)
            yield scrapy.Request(next_page, callback=self.parse)

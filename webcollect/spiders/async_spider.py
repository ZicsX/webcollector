import scrapy
from urllib.parse import urlparse
import os
import trafilatura
import uuid
import csv


class AsyncSpider(scrapy.Spider):
    name = "async_spider"

    custom_settings = {
        "CONCURRENT_REQUESTS": 100,
        "DOWNLOAD_DELAY": 0.1,
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def __init__(self, url=None, *args, **kwargs):
        super(AsyncSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        parsed_uri = urlparse(url)
        self.domain = "{uri.netloc}".format(uri=parsed_uri)  # Extract domain
        self.folder_path = os.path.join(os.getcwd(),'collect_data', self.domain)  # Folder path
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        self.csv_file_path = os.path.join(self.folder_path, "links.csv")
        with open(self.csv_file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["URL", "Filename"])  # Writing headers

    def parse(self, response):

        extracted_data = trafilatura.extract(response.text)
        if extracted_data:
            filename = f"{uuid.uuid4()}.txt"
            file_path = os.path.join(self.folder_path, filename)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(extracted_data)

            with open(self.csv_file_path, "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([link, filename])
    
        for link in response.css("a::attr(href)").getall():
            link = response.urljoin(link)
            if urlparse(link).netloc == self.domain:
                yield scrapy.Request(link, callback=self.parse)

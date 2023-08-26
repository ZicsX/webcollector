from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webscraper.spiders.spider import WebsiteCrawlerSpider
from urllib.parse import urlparse


def run_spider(target_url):
    domain_name = urlparse(target_url).netloc
    job_dir = f"jobs/{domain_name}"

    process = CrawlerProcess(get_project_settings())
    process.settings.set("JOBDIR", job_dir)
    process.settings.setdict(
        {
            "CONCURRENT_REQUESTS": 100,
            "DOWNLOAD_DELAY": 0,
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "ROBOTSTXT_OBEY": True,
            "ITEM_PIPELINES": {
                "webscraper.extraction_pipeline.ExtractionPipeline": 100,
                "webscraper.save_text_pipeline.SaveTextPipeline": 200,
                "webscraper.log_csv_pipeline.LogToCsvPipeline": 300,
            },
        }
    )

    # Initialize and start the spider
    process.crawl(WebsiteCrawlerSpider, target_url=target_url)
    process.start()


if __name__ == "__main__":
    target_url = "https://example.com"
    run_spider(target_url)

import trafilatura
from scrapy.exceptions import DropItem
from concurrent.futures import ProcessPoolExecutor


class ExtractionPipeline:
    def __init__(self):
        self.executor = ProcessPoolExecutor(max_workers=2)

    def open_spider(self, spider):
        spider.logger.info("Initialized ExtractionPipeline")

    def close_spider(self, spider):
        self.executor.shutdown()
        spider.logger.info("Closed ExtractionPipeline")

    def process_item(self, item, spider):
        try:
            # Execute the trafilatura.extract function in parallel
            future = self.executor.submit(trafilatura.extract, item["html_content"])
            extracted_data = future.result()

            if extracted_data:
                item["extracted_data"] = extracted_data
            else:
                raise DropItem(f"Missing content in: {item['url']}")

            return item
        except Exception as e:
            spider.logger.error(f"Error processing {item['url']}: {e}")
            raise DropItem(f"Error processing {item['url']}: {e}")

import os
import uuid


class SaveTextPipeline:
    def open_spider(self, spider):
        self.domain_folder = os.path.join("output", spider.domain)
        if not os.path.exists(self.domain_folder):
            os.makedirs(self.domain_folder)

        spider.logger.info("Initialized SaveTextPipeline")

    def close_spider(self, spider):
        spider.logger.info("Closed SaveTextPipeline")

    def process_item(self, item, spider):
        file_name = str(uuid.uuid4()) + ".txt"
        with open(
            os.path.join(self.domain_folder, file_name), "w", encoding="utf-8"
        ) as f:
            f.write(item["extracted_data"])

        item["file_name"] = file_name
        return item

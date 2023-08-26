import csv
import os


class LogToCsvPipeline:
    def open_spider(self, spider):
        domain_folder = os.path.join("output", spider.domain)

        if not os.path.exists(domain_folder):
            os.makedirs(domain_folder)

        csv_path = os.path.join(domain_folder, "log.csv")

        self.csvfile = open(csv_path, "a", newline="")
        self.csvwriter = csv.writer(self.csvfile)

        # Write if the file is empty
        if os.path.getsize(csv_path) == 0:
            self.csvwriter.writerow(["URL", "File Name"])

        spider.logger.info("Initialized LogToCsvPipeline")

    def close_spider(self, spider):
        self.csvfile.close()
        spider.logger.info("Closed LogToCsvPipeline")

    def process_item(self, item, spider):
        self.csvwriter.writerow([item["url"], item["file_name"]])
        self.csvfile.flush()
        return item

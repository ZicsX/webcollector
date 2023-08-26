import boto3
import uuid
from scrapy.exceptions import DropItem
from concurrent.futures import ThreadPoolExecutor


class S3StoragePipeline:
    def __init__(self):
        self.s3_client = boto3.client("s3")
        self.bucket_name = "YOUR_S3_BUCKET_NAME"
        self.executor = ThreadPoolExecutor(
            max_workers=30
        )  # Adjust max_workers as needed

    def open_spider(self, spider):
        spider.logger.info("Initialized S3StoragePipeline")

    def close_spider(self, spider):
        self.executor.shutdown(wait=True)
        spider.logger.info("Closed S3StoragePipeline")

    def process_item(self, item, spider):
        file_name = str(uuid.uuid4()) + ".txt"
        s3_path = f"{spider.domain}/{file_name}"
        item["file_name"] = file_name

        future = self.executor.submit(
            self.upload_to_s3, file_name, s3_path, item["extracted_data"], spider
        )

        try:
            future.result()
            return item
        except Exception as e:
            spider.logger.error(f"Error uploading {file_name} to S3: {e}")
            raise DropItem(f"Error uploading {file_name} to S3: {e}")

    def upload_to_s3(self, file_name, s3_path, content, spider):
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_path,
                Body=content,
                ContentType="text/plain; charset=utf-8",
            )
            # spider.logger.info(f"Successfully saved file {file_name} to S3 bucket {self.bucket_name}")
        except Exception as e:
            spider.logger.error(f"Error uploading {file_name} to S3: {e}")
            raise Exception(f"Error uploading {file_name} to S3: {e}")

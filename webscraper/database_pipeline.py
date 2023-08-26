from concurrent.futures import ThreadPoolExecutor
from webscraper.models import Session, Website, WebPage
from sqlalchemy.exc import IntegrityError, OperationalError


class DatabasePipeline:
    def open_spider(self, spider):
        self.executor = ThreadPoolExecutor(max_workers=30)
        with Session() as session:  # Start a new session
            domain = spider.domain
            website = session.query(Website).filter_by(domain=domain).first()
            if not website:
                website = Website(domain=domain)
                session.add(website)
                session.commit()
            self.website_id = website.id

            spider.logger.info(f"Database initialized for domain: {domain}")
        spider.logger.info("Initialized DatabasePipeline")

    def close_spider(self, spider):
        self.executor.shutdown(wait=True)
        spider.logger.info("Closed DatabasePipeline")

    def process_item(self, item, spider):
        self.executor.submit(self._insert_item, item, spider)

        return item

    def _insert_item(self, item, spider):
        with Session() as session:
            try:
                new_page = WebPage(
                    url=item["url"],
                    file_name=item["file_name"],
                    website_id=self.website_id,
                )
                session.add(new_page)
                session.commit()
            except IntegrityError:
                spider.logger.error(
                    f"IntegrityError: Possible duplicate or constraint violation for item {item}"
                )
                session.rollback()
            except OperationalError:
                spider.logger.error(
                    f"OperationalError: Database operation error for item {item}"
                )
                session.rollback()
            except Exception as e:
                spider.logger.error(f"An unexpected error occurred: {e}")
                session.rollback()

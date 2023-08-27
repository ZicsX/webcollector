from celery import shared_task
from urllib.parse import urlparse
from collector.models import DomainCrawl
import subprocess


@shared_task
def run_spider(target_url, hash_value):
    domain_name = urlparse(target_url).netloc

    subprocess.run(
        [
            "scrapy",
            "crawl",
            "website_crawler",
            "-a",
            f"target_url={target_url}",
            "-s",
            f"JOBDIR=jobs/{domain_name}",
        ]
    )

    # Update the status to COMPLETED once crawling finishes
    crawl_instance = DomainCrawl.objects.get(hash_value=hash_value)
    crawl_instance.status = "COMPLETED"
    crawl_instance.save()

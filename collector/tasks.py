from __future__ import absolute_import, unicode_literals
from celery import shared_task
from webcollect.spiders.run_spider import run_spider
from collector.models import DomainCrawl

@shared_task
def scrape_website(domain, hash_value):
    url = f'https://{domain}'
    run_spider(url)
    
    # Update the status to COMPLETED once crawling finishes
    crawl_instance = DomainCrawl.objects.get(hash_value=hash_value)
    crawl_instance.status = 'COMPLETED'
    crawl_instance.save()

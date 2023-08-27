import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webcollector.settings")
django.setup()

from collector.models import DomainCrawl


def reset_domain_crawl():
    DomainCrawl.objects.all().delete()
    print("All rows from DomainCrawl model have been deleted.")


if __name__ == "__main__":
    reset_domain_crawl()

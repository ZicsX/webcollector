from django.http import JsonResponse, HttpResponse
from collector.models import DomainCrawl
import hashlib
import os
import zipfile
from .tasks import run_spider
from django.shortcuts import render
from django.conf import settings
from urllib.parse import urlparse


def index(request):
    return render(request, "index.html")


def start_crawl(request):
    target_url = request.GET.get("domain")
    domain = urlparse(target_url).netloc
    hash_value = hashlib.sha256(target_url.encode()).hexdigest()

    try:
        crawl_instance = DomainCrawl.objects.get(hash_value=hash_value)

        # If instance exists and completed
        if crawl_instance.status == "COMPLETED":
            # Prepare the zip and return
            zip_filename = os.path.join(settings.BASE_DIR, "output", f"{domain}.zip")
            if not os.path.exists(zip_filename):
                folder_path = os.path.join(settings.BASE_DIR, "output", domain)
                with zipfile.ZipFile(zip_filename, "w") as zipf:
                    for foldername, subfolders, filenames in os.walk(folder_path):
                        for filename in filenames:
                            file_path = os.path.join(foldername, filename)
                            arcname = os.path.relpath(file_path, folder_path)
                            zipf.write(file_path, arcname=arcname)

            with open(zip_filename, "rb") as zipf:
                response = HttpResponse(zipf.read(), content_type="application/zip")
                response["Content-Disposition"] = f"attachment; filename={domain}.zip"
                return response

        # If instance exists but still running
        return JsonResponse({"status": "RUNNING", "message": "Crawl is still running."})

    except DomainCrawl.DoesNotExist:
        # Create a new crawl instance and start Scrapy
        crawl_instance = DomainCrawl.objects.create(
            domain=domain, hash_value=hash_value
        )
        # Start Scrapy spider via Celery
        run_spider.delay(target_url, hash_value)

    return JsonResponse({"status": "RUNNING", "message": "Crawl started."})


def check_status(request, hash_value):
    try:
        crawl_instance = DomainCrawl.objects.get(hash_value=hash_value)
        return JsonResponse({"status": crawl_instance.status})

    except DomainCrawl.DoesNotExist:
        return JsonResponse(
            {"status": "ERROR", "message": "No such domain crawl found."}
        )

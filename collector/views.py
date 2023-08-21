from django.http import JsonResponse, HttpResponse
from collector.models import DomainCrawl
import hashlib
import os
import zipfile
from .tasks import scrape_website
from django.shortcuts import render
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def start_crawl(request):
    domain = request.GET.get('domain')
    hash_value = hashlib.sha256(domain.encode()).hexdigest()

    try:
        crawl_instance = DomainCrawl.objects.get(hash_value=hash_value)

        # If instance exists and completed
        if crawl_instance.status == 'COMPLETED':
            # Prepare the zip and return
            zip_filename = os.path.join(settings.BASE_DIR, 'collect_data', f"{domain}.zip")
            if not os.path.exists(zip_filename):
                folder_path = os.path.join(settings.BASE_DIR, 'collect_data', domain)
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    for foldername, subfolders, filenames in os.walk(folder_path):
                        for filename in filenames:
                            file_path = os.path.join(foldername, filename)
                            zipf.write(file_path, os.path.relpath(file_path, settings.BASE_DIR))
            
            with open(zip_filename, 'rb') as zipf:
                response = HttpResponse(zipf.read(), content_type="application/zip")
                response['Content-Disposition'] = f'attachment; filename={domain}.zip'
                return response

        # If instance exists but still running
        return JsonResponse({"status": "RUNNING", "message": "Crawl is still running."})

    except DomainCrawl.DoesNotExist:
        # Create a new crawl instance and start Scrapy
        crawl_instance = DomainCrawl.objects.create(domain=domain, hash_value=hash_value)
        # Start Scrapy spider via Celery
        scrape_website.delay(domain, hash_value)

    return JsonResponse({"status": "RUNNING", "message": "Crawl started."})

def check_status(request, hash_value):
    try:
        crawl_instance = DomainCrawl.objects.get(hash_value=hash_value)
        return JsonResponse({"status": crawl_instance.status})

    except DomainCrawl.DoesNotExist:
        return JsonResponse({"status": "ERROR", "message": "No such domain crawl found."})

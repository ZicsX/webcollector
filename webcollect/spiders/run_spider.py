import subprocess
from scrapy.utils.project import get_project_settings

def run_spider(url):
    spider_name = "async_spider"
    cmd = ['scrapy', 'crawl', spider_name, '-a', f'url={url}']
    
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e.output.decode('utf-8'))

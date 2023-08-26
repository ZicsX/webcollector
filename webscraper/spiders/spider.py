import scrapy
from webscraper.items import WebScraperItem
from urllib.parse import urlparse, urlsplit, urlunsplit


class WebsiteCrawlerSpider(scrapy.Spider):
    name = "website_crawler"

    def __init__(self, target_url, *args, **kwargs):
        super(WebsiteCrawlerSpider, self).__init__(*args, **kwargs)
        self.start_urls = [target_url]
        self.allowed_domains = [urlparse(target_url).netloc]
        self.domain = self.allowed_domains[0]
        self.path = urlparse(target_url).path

    def parse(self, response):
        if response.status >= 400:
            self.logger.error(f"HTTP Error {response.status} for URL: {response.url}")
            return  # Skip processing for non-success status codes

        # Avoid parsing non-HTML content, mailto links, and non-text files
        if (
            response.headers.get("content-type", "")
            .decode("utf-8")
            .startswith("text/html")
        ):
            # Yield the item for pipelines
            item = WebScraperItem()
            item["url"] = response.url
            item["html_content"] = response.text

            yield item

        # Follow links for further crawling within the domain
        for link in response.css("a::attr(href)").getall():
            link = response.urljoin(link)
            split_url = urlsplit(link)
            link = urlunsplit(
                (
                    split_url.scheme,
                    split_url.netloc,
                    split_url.path,
                    split_url.query,
                    "",
                )
            )

            if split_url.netloc == self.domain and split_url.path.startswith(self.path):
                if not self._is_non_text_url(link):
                    yield response.follow(link, self.parse)

    def _is_non_text_url(self, url):
        """
        Check if the URL is likely to point to a non-textual resource.
        """
        NON_TEXT_EXTENSIONS = [
        ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv", ".zip", ".rar", ".7z", ".tar", ".gz",
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".ico", ".psd", ".ai", ".svg", ".mp3", ".wav", ".m4a",
        ".ogg", ".flac", ".mp4", ".mov", ".avi", ".wmv", ".flv", ".mkv", ".webm", ".m4v", ".exe", ".dll", ".bat",
        ".sh", ".app", ".dmg", ".pkg", ".iso", ".img", ".vhd", ".vhdx", ".xml", ".json", ".css",".bak", ".tmp",
        ".js", ".swf", ".fla", ".unity3d", ".ps", ".eps", ".indd", ".ai", ".torrent", ".magnet", ".sql", ".db",
        ".sqlite", ".mdb", ".rvt", ".dwg", ".dxf", ".stl", ".obj", ".3ds", ".blend", ".ma", ".mb", ".mpg", ".mpeg",
        ".webp", ".woff", ".woff2", ".ttf", ".otf", ".vcf", ".ics", ".atom", ".pem", ".cer", ".crt"
        ]

        return any(url.endswith(ext) for ext in NON_TEXT_EXTENSIONS)

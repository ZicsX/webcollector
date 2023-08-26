# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebScraperItem(scrapy.Item):
    url = scrapy.Field()
    html_content = scrapy.Field()
    extracted_data = scrapy.Field()
    file_name = scrapy.Field()

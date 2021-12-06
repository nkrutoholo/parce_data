# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# import scrapy
#
#
# class AlloUaItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     scanned_time = scrapy.Field()
#     url = scrapy.Field()

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    scanned_time = scrapy.Field()
    product_url = scrapy.Field()
    product_title = scrapy.Field()
    product_SKU = scrapy.Field()
    product_category = scrapy.Field()
    product_availability = scrapy.Field()
    product_price = scrapy.Field()
    product_price_regular = scrapy.Field()
    product_seller = scrapy.Field()
    product_offers = scrapy.Field()

import scrapy
import datetime
import json
import struct
from inline_requests import inline_requests
from scrapy import Spider, Request


class ProductSpider(Spider):
    name = 'product'
    allowed_domains = ['allo.ua']
    start_urls = ['https://allo.ua/']

    def parse(self, response):
        for url_catalog in response.xpath('//a[@class="sub__link arrow-icon"]/@href').getall():
            yield response.follow(url_catalog, callback=self.parse_catalog)

    def parse_catalog(self, response):
        catalog = response.xpath('//a[@class="portal-group__image-link"]/@href').getall()
        if catalog:
            for link in catalog:
                yield response.follow(link, callback=self.parse_products)

    def parse_products(self, response):
        products = response.xpath('//a[@class="product-card__title"]/@href').getall()
        if products:
            for link in products:
                yield response.follow(link, callback=self.parse_item)
            next_page = response.xpath('//a[@class="pagination__next__link"]/@href').get()
            if not (next_page is None):
                yield response.follow(next_page, callback=self.parse_products)

    def casting_price(self, price):
        try:
            price = float(price)
        except Exception:
            self.logger.info(f"Failed convert {price} to float. Assign to None")
            price = None
        return price

    @inline_requests
    def parse_item(self, response):
        uniq_title = set()
        product = {
            'scanned_time': datetime.datetime.now(),
            'product_url': response.url,
            'product_title': response.xpath('//h1[@class ="p-view__header-title"]/text()').get(),
            'product_SKU': response.xpath('//span[@class ="p-tabs__sku-value"]/text()').get(),
            'product_category': response.xpath('//li/a[@class ="breadcrumbs__link"]/text()').getall(),
            'product_availability': True if response.xpath(
                '//span[@class ="p-trade__stock-label-icon"]'
            ).get() else False,
            'product_price': str(response.xpath(
                '//div[contains(@class, "p-trade-price__current")]/span/text()'
            ).extract_first()).encode("ascii", "ignore").strip(),
            'product_price_regular': str(response.xpath(
                '//div[@class ="p-trade-price__old"]/span[@class="sum"]/text()'
            ).extract_first()).encode("ascii", "ignore").strip(),
            'product_seller': response.xpath(
                '//span[@class="shipping-brand__name"]/text()'
            ).get() or 'allo_ua',
            'product_offers': None,
        }

        uniq_title.add(product['product_title'])

        #ajax request
        try:
            url = f'https://allo.ua/ua/discounts/product/items/?sku={product["product_SKU"]}&isAjax=1&currentLocale=uk_UA'
            headers = {
                'accept': 'application/json, text/plain, */*',
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
                'content-type': 'text/plain',
                'x-use-nuxt': '1',
            }
            resp = yield Request(
                url,
                self.parse_details,
                headers=headers,
            )
            data = json.loads(resp.text)
            for el in data:
                del el['img']
            product['product_offers'] = data
        except:
            self.logger.info(f"Failed request {url}")

        product['product_price'] = self.casting_price(product['product_price'])
        product['product_price_regular'] = self.casting_price(product['product_price_regular'])

        for el in uniq_title:
            if product['product_title'] == el:
                yield None

        yield product

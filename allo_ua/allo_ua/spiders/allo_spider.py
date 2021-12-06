# from scrapy import Spider, Request
# import os
# import json
#
#
# class AlloSpider(Spider):
#     name = "allo"
#
#     custom_settings = {
#         'CONCURRENT_REQUESTS': os.getenv('CONCURRENT_REQUESTS', 1),
#         'CONCURRENT_REQUESTS_PER_DOMAIN': os.getenv('CONCURRENT_REQUESTS', 1),
#         'CONCURRENT_REQUESTS_PER_IP': os.getenv('CONCURRENT_REQUESTS', 1),
#         'DOWNLOAD_DELAY': os.getenv('DOWNLOAD_DELAY', 3),
#         'ROBOTSTXT_OBEY': False,
#         'RETRY_TIMES': os.getenv('RETRY_TIMES', 10),
#     }
#
#     def start_requests(self):
# #\https://allo.ua/ua/catalog/product/getServices/?id=8516437&isAjax=1&currentLocale=uk_UA
#         url = 'https://allo.ua/ua/discounts/product/items/?sku=868298&isAjax=1&currentLocale=uk_UA'
#         headers = {
#             'accept': 'application/json, text/plain, */*',
#             'x-requested-with': 'XMLHttpRequest',
#             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
#             'content-type': 'text/plain',
#             'x-use-nuxt': '1',
#         }
#         yield Request(
#             url,
#             self.parse_details,
#             headers=headers,
#             meta={'product': {'name': 'test'}}
#         )
#
#     def parse_details(self, response):
#         product = response.request.meta['product']
#         try:
#             data = json.loads(response.text)
#             for el in data:
#                 del el['img']
#
#         except:
#             pass
#
#         self.logger.info(data)
#

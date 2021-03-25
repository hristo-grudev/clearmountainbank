import scrapy

from scrapy.loader import ItemLoader

from ..items import ClearmountainbankItem
from itemloaders.processors import TakeFirst


class ClearmountainbankSpider(scrapy.Spider):
	name = 'clearmountainbank'
	start_urls = ['https://www.clearmountainbank.com/resources/news/']

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="prev"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h3/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::h3 | ancestor::p[@class="date-time"] | ancestor::div[@class="share-these-manual"] | ancestor::script | ancestor::font)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="date-time"]/text()[normalize-space()]').get()

		item = ItemLoader(item=ClearmountainbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from fivepointsbank.items import Article


class fivepointsbankSpider(scrapy.Spider):
    name = 'fivepointsbank'
    start_urls = ['https://www.5pointsbank.com/Blog']

    def parse(self, response):
        links = response.xpath('//a[text()="Read more>>"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

        archive = 'https://www.5pointsbank.com/Blog%20Archives'
        yield response.follow(archive, self.parse)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//td/h2/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('(//table[@class="Subsection-Table"])[2]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()

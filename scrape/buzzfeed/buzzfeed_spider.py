import urllib.parse as urlparse
from urllib.parse import urlencode
import scrapy, logging

NUM_PAGES = 200

class BuzzfeedSpider(scrapy.Spider):
    name = "buzzfeed"
    start_urls = [
        'https://www.buzzfeed.com/entertainment',
        'https://www.buzzfeed.com/health',
        'https://www.buzzfeed.com/science',
        'https://www.buzzfeed.com/science',
    ]


    def parse(self, response):
        params = {
            'p': 0,
            'z': '5F16K0',
            'r': 1,
        }
        for i in range(NUM_PAGES):
            params['p'] = i
            next_back = response.url + '?' +  urlencode(params)
            yield scrapy.Request(next_back, callback=self.parse_list)

    def parse_list(self, response):
        # Parse each of the articles linked from the main page
        links = response.xpath('//a[@class="lede__link"]/@href').extract()
        for link in links:
            next_page = response.urljoin(link)
            yield scrapy.Request(next_page, callback=self.parse_article)

    def parse_article(self, response):
        headline = response.xpath('//h1[@id="post-title"]/text()').extract_first()
        article = response.xpath('normalize-space(.//div[@data-print="body"])').extract_first()

        # concatenate all paragraph elements in the article body
        yield {
            'headline': headline.strip(),
            'text': article,
        }


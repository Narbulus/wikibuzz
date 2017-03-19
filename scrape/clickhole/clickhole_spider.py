import scrapy

class ClickholeSpider(scrapy.Spider):
    name = "clickhole"
    start_urls = [
        'http://www.clickhole.com/features/news/',
    ]

    def parse(self, response):
        # Parse each of the articles linked from the main page
        links = response.xpath('//article/a/@href').extract()
        for link in links:
            next_page = response.urljoin(link)
            yield scrapy.Request(next_page, callback=self.parse_article)
        # Attempt to smash that next button
        next_button = response.xpath('//a[@title="Next"]/@href').extract_first()
        if next_button is not None:
            next_page = response.urljoin(next_button)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_article(self, response):
        headline = response.xpath('//h1[@class="headline"]/text()').extract_first()
        article = response.xpath('normalize-space(.//*[@class="article-text"])').extract_first()

        # concatenate all paragraph elements in the article body
        yield {
            'headline': headline.strip(),
            'text': article,
        }


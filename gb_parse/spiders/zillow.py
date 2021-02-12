import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/san-francisco-ca/']
    x_pats = {
        'pagination': '//div[@class="search-pagination"]/nav/ul/li/a/@href',
        'ads': '//article[contains(@class, "list-card")]//a[contains(@class, "list-card-link ")]/@href',
    }
    browser = webdriver.Firefox()

    def get_request(self, response, xpath, callback):
        for link in response.xpath(xpath):
            yield response.follow(link, callback=callback)

    def parse(self, response):
        yield from self.get_request(response, self.x_pats['pagination'], self.parse)
        yield from self.get_request(response, self.x_pats['ads'], self.ads_parse)

    def ads_parse(self, response):
        self.browser.get(response.url)
        media_col = self.browser.find_element_by_xpath('//div[contains(@class, "ds-media-col")]')
        len_photos = len(media_col.find_elements_by_xpath('//ul[@class="media-stream"]/li//picture'))
        while True:
            # media_col.send_keys(Keys.COMMAND + Keys.END)
            for _ in range(5):
                media_col.send_keys(Keys.PAGE_DOWN)
            photos = media_col.find_elements_by_xpath('//ul[@class="media-stream"]/li//picture')
            if len_photos == len(photos):
                break
            len_photos = len(photos)
        ps = scrapy.Selector(text=self.browser.page_source)
        print(1)

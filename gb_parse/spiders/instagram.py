import json
import scrapy


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    
    def __init__(self, login, password, *args, **kwargs):
        self.tags = ["python", "программирование", "developers"]
        self.login = login
        self.password = password
        super().__init__(*args, **kwargs)

    def parse(self, response):
        try:
            js_data = self.js_data_extract(response)
            form_data = {
                'username':self.login,
                'enc_password': self.password,
            }
            headers = {'X-CSRFToken': js_data['config']['csrf_token']}
            yield scrapy.FormRequest(
                self.login_url,
                method='POST',
                formdata=form_data,
                headers=headers,
                callback=self.parse
            )
        except AttributeError:
            if response.json()["authenticated"]:
                for tag in self.tags:
                    yield response.follow(f"/explore/tags/{tag}/", callback=self.tag_parse)
        
    def tag_parse(self, response):
        print(1)
    
    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//body/script[contains(text(), "csrf_token")]/text()').get()
        return json.loads(script.replace("window._sharedData = ", "")[:-1])

import scrapy

class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["kun.uz"]
    base_url = "https://kun.uz"
    start_urls = ['https://kun.uz/uz/news/category/uzbekiston', 'https://kun.uz/uz/news/category/jahon',
                  'https://kun.uz/uz/news/category/iktisodiet', 'https://kun.uz/uz/news/category/jamiyat',
                  'https://kun.uz/uz/news/category/tehnologia', 'https://kun.uz/uz/news/category/sport',
                  'https://kun.uz/uz/news/category/nuqtai-nazar']

    def parse(self, response):
        news_urls = response.css('a.news__img::attr(href)').getall()
        if news_urls:
            for url in news_urls:
                detail_url = self.base_url + url
                self.category = response.css('span.text-uppercase::text').get()
                yield response.follow(detail_url, callback=self.parse_detail)
        next_page = self.base_url + response.css('a.load-more__link::attr(href)').get()
        yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        date = response.css('div.date::text').get()
        title = response.css('h1.single-header__title::text').get()
        if response.css('div.single-content h4::text').get():
            content = str(response.css('div.single-content h4::text').get())+' '+' '.join(response.css('div.single-content p *::text').getall())
        else:
            content = ' '.join(response.css('div.single-content p *::text').getall())
        hashtag = response.css('a.tags-ui__link::text').getall()
        
        yield {
            'date':date,
            'title':title,
            'content':content,
            'category':self.category,
            'hashtag':hashtag
        }
import scrapy
from bs4 import BeautifulSoup

class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["uz.wikipedia.org"]
    base_url = "https://uz.wikipedia.org"
    start_urls = ['https://uz.wikipedia.org/w/index.php?title=Maxsus:AllPages&from=%21']
    x = 1

    def parse(self, response):
        news_urls = response.css('div.mw-allpages-body a::attr(href)').getall()
        if news_urls:
            for url in news_urls:
                detail_url = self.base_url + url
                yield response.follow(detail_url, callback=self.parse_detail)
                
        if self.x:
            next_page = self.base_url + response.css('div.mw-allpages-nav a::attr(href)').getall()[0]
            self.x = 0
        else:
            next_page = self.base_url + response.css('div.mw-allpages-nav a::attr(href)').getall()[1]

        yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        date = soup.find('li', id="footer-info-lastmod").text.strip()[23:-20] if soup.find('li', id="footer-info-lastmod") else None
        title = soup.find('h1', class_="firstHeading mw-first-heading").text if soup.find('h1', class_="firstHeading mw-first-heading") else None
        content = ' '.join([i for i in soup.find('div', id="bodyContent").strings]) if soup.find('div', id="bodyContent") else None
        
        yield {
            'date':date,
            'title':title,
            'content':content,
            'url': response.url
        }
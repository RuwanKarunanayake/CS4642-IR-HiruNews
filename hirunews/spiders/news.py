# -*- coding: utf-8 -*-
import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['hirunews.lk']
    start_urls = ['http://www.hirunews.lk/all-news.php']

    def parse(self, response):
        urls= response.css('div.rp-mian div.lts-cntp a::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_news_details)


        next_page_url= response.css('div.pagi_2 a[title*=next]::attr(href)').extract_first()
        if next_page_url and int(next_page_url.split('=')[1])<50:
            yield scrapy.Request(url=next_page_url, callback=self.parse)



    def parse_news_details(self, response):
        paragraphs_using_div =response.css('div.lts-txt2 div::text').extract()
        paragraphs_using_p=response.css('div.lts-txt2 p::text').extract()
        decription_p= '\n'.join(paragraphs_using_p)
        description_div= '\n'.join(paragraphs_using_div)
        description=(description_div+"\n"+decription_p)
        yield {
            'date' :response.css('div.time::text').extract_first(),
            'heading':response.css('div.lts-cntp2::text').extract_first(),
            'description':description
        }


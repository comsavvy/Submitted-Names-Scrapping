import scrapy
import requests


def all_urls(scrape_this):
    base = 'http://www.behindthename.com'
    all_page = []
    
    all_page.append(scrape_this)
    req = requests.get(scrape_this)
    r_scrape = scrapy.Selector(req)
    forwardpg = r_scrape.css('nav.pagination')
    for i in list(set(forwardpg.css('a::attr(href)').extract())):
        all_page.append(base+i)
    return all_page

class DetailsExtractSpider(scrapy.Spider):
    name = 'details_extract'
    allowed_domains = ['behindthename.com']
    start_urls = all_urls('http://www.behindthename.com/submit/names/usage/eastern-african/')


    def parse(self, response):     
         general = response.css("div.browsename")
         for gen in general:
            using = gen.xpath('.//span//text()').extract()
            name = using[0]
            gender = using[1]
            all_text = ''.join(gen.xpath('.//text()').extract())            
            yield {
            "Name": name,
            "Gender": gender,
            "Location": ''.join(gen.css("span.listusage  ::text").extract()),
            "Description": all_text[all_text.index(using[-1])+len(using[-1]):]
            }

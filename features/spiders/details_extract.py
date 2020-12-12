import scrapy


class DetailsExtractSpider(scrapy.Spider):
    name = 'details_extract'
    allowed_domains = ['behindthename.com']
    start_urls = ['http://www.behindthename.com/submit/names/usage/eastern-african/',
                    "http://www.behindthename.com//submit/names/usage/eastern-african/2",
                    "http://www.behindthename.com//submit/names/usage/eastern-african/3",
                    "http://www.behindthename.com//submit/names/usage/eastern-african/4"
                    ]


    def parse(self, response):     
         general = response.css("div.browsename")
         for gen in general:      
            yield {
            "Name": gen.css("span.listname ::text").extract_first(),
            "Gender": gen.css("span.listgender ::text").extract_first(),
            "Location": ''.join(gen.css("span.listusage  ::text").extract())
            }

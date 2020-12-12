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

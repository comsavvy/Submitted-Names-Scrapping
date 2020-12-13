import scrapy


class DetailsExtractSpider(scrapy.Spider):
    name = 'details_extract'
    allowed_domains = ['behindthename.com']
    start_urls = ['http://www.behindthename.com/submit/names/usage/eastern-african/']

    def parse(self, response):
        links = len(set(response.css('nav.pagination > a::attr(href)').extract()))
        i = 0
        while i <= links:
            yield response.follow(url=f'{response.url}/{i+1}', callback=self.page_details)
            i += 1
            
    def page_details(self, response):
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

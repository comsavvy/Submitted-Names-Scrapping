import scrapy


class DetailsExtractSpider(scrapy.Spider):
    name = 'details_extract'
    allowed_domains = ['behindthename.com']
    start_urls = ['http://www.behindthename.com/submit/names/usage/eastern-african/']        

    def parse(self, response):
        """
            Getting all the countries URL,
            And redirecting each country to 'each_page' method to confirm the pages,
            And then scrap them in 'page_details' method.
        """
        all_country = response.css('div.nb-quickfilter > select[name=usage] > option ::attr(value)').extract()[1:-1]
        for country in all_country:
            yield response.follow(url=response.urljoin(country), callback=self.each_page)
    
    def each_page(self, response):
        """
            Confirming the number of pages and also redirecting them to be scrapped.
        """
        links = len(set(response.css('nav.pagination > a::attr(href)').extract()))
        i = 0
        while i <= links:
            yield response.follow(url=f'{response.url}/{i+1}', callback=self.page_details)
            i += 1
            
    def page_details(self, response):
        """
            Getting all the information needed from all the pages here.
        """
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

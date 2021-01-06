import scrapy
from collections import OrderedDict


class DetailsExtractSpider(scrapy.Spider):
    name = 'details_extract'
    allowed_domains = ['behindthename.com']
    start_urls = ['http://www.behindthename.com/submit/names/usage/eastern-african/']
    countries_name = None
    country_count = 0

    def parse(self, response):
        """
            Getting all the countries URL,
            And redirecting each country to 'each_page' method to confirm the pages,
            And then scrap them in 'page_details' method.
        """
        
        # The class is being change several times [nb-quickfilter | nb2-quickfilter]
        all_countries_page = response.css('div.nb-quickfilter > select[name=usage] > option')
        
        # If all_countries_page is [], try other method
        if not all_countries_page:
            all_countries_page = response.css('div.nb2-quickfilter > select[name=usage] > option')
        
        DetailsExtractSpider.countries_name = all_countries_page.css(' ::text').extract()[2:] # This contains 
                                                                                          # all the countries name
        all_country = all_countries_page.css(' ::attr(value)').extract()[2:]        
            
        for country in all_country:
            yield scrapy.Request(url=response.urljoin(country), callback=self.each_page)
    
    def each_page(self, response):
        """
            Confirming the number of pages and also redirecting them to be scrapped.
        """
        links = list(OrderedDict.fromkeys(response.css('nav.pagination > a::attr(href)').extract()).keys())
        
        for link in links:
            yield response.follow(url=response.urljoin(link), callback=self.page_details)
        
            
    def page_details(self, response):
        """
            Getting all the information needed from all the pages here.
        """
        general = response.css("div.browsename")
        country_name = DetailsExtractSpider.countries_name[DetailsExtractSpider.country_count]
        for gen in general:
            using = gen.xpath('.//span//text()').extract()
            name = using[0]
            gender = using[1]
            all_text = ''.join(gen.xpath('.//text()').extract())            
            yield {
            "Name": name,
            "Gender": gender,
            "Countries": country_name,
            "Location": ''.join(gen.css("span.listusage  ::text").extract()),
            "Description": all_text[all_text.index(using[-1])+len(using[-1]):]
            }
        DetailsExtractSpider.country_count += 1

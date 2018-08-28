from scrapy import Spider, Request
from scrapy.selector import Selector
from icd10.items import *


class IcdSpider(Spider):
    name = "icd10"
    allowed_domains = ["icd10data.com"]
    start_urls = ["https://www.icd10data.com/ICD10CM/Codes", ]

    def parse(self, response):
        with open("/Users/sdash/Desktop/icd10/icd_codes.csv", 'a+') as f:
            all_div = Selector(response).xpath('/html/body/div')
            for div in all_div:
                codes = div.xpath('.//div/ul')

                for code in codes.xpath('.//li'):
                    try:
                        code_description = code.xpath('.//text()').extract()
                        item = Icd10Item()
                        code_name = code_description[1]
                        if ("-" in code_name) or (" " in code_name):
                            pass
                        else:
                            item['code'] = code_name
                            description = ' '.join(code_description[2:])
                            description = description.replace('\\r\\n', '')
                            description = ' '.join(description.split())
                            item['description'] = description
                            f.write(code_name + ', ' + description + '\n')
                        next_page = code.xpath('.//a/@href')
                        next_page = next_page[0].extract()
                        if next_page is not None:
                            next_page = response.urljoin(next_page)
                        yield Request(next_page, callback=self.parse)
                    except:
                        pass

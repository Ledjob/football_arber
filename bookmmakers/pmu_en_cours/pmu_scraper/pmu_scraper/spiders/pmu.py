import scrapy

class PmuSpider(scrapy.Spider):
    name = 'pmu'
    allowed_domains = ['pmu.fr']
    start_urls = ['https://parisportif.pmu.fr/home/wrapper/events?activeSportId=1&leagues=%5B123%5D']

    def parse(self, response):
        # Save the HTML content to a file
        with open('pmu_page.html', 'wb') as f:
            f.write(response.body)
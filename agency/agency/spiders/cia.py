import scrapy

# links = //a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href
# title = //h1[@class="documentFirstHeading"]/text()
# paragraph = //div[@class="field-item even"]//p[not(@class)]/text()

# API_KEY = El apikey que te da Scrapyhub
# PROJECT_ID = El id del proyecto que te da junto con el API_KEY
# NAME_SPIDER = Es el nombre que tu le pusiste al spider en su variable name.
# SPIDER_ID = Es el numero de lz izquieda de la columna job del spider en este caso de la cia solo tenemos 1 spider, tipo 1/2 significa 1 spider / 2 jobs
# SPIDER_NUMBER = Es el numero de job del spider en este caso nos traeriamos el 2, tipo 1/2

# Para ejecutar el spider que esta alojado dentro de scrapyhub se ejecuta el siguiente comando en la consola o tambien se puede dejar programado con un cronjob en algun servidor.
# curl -u API_KEY: https://app.scrapinghub.com/api/run.json -d project=PROJECT_ID -d spider=NAME_SPIDER

# Se ejecuta y traer los datos del spider dependiendo de los parametros entregados.
# curl -u API_KEY: https://storage.scrapinghub.com/items/PROJECT_ID/SPIDER_ID/SPIDER_NUMBER


class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/library/readingroom/historical-collections'
    ]
    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'UTF-8'
    }

    def parse(self, response):
        links_declassified = response.xpath(
            '//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(
            '//h1[@class="documentFirstHeading"]/text()').get()
        paragraph = response.xpath(
            '//div[@class="field-item even"]//p[not(@class)]/text()').get()

        yield {
            'url': link,
            'title': title,
            'body': paragraph
        }

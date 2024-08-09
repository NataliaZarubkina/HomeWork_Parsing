import scrapy


class FilmScraperSpider(scrapy.Spider):
    name = "film_scraper"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/250_%D0%BB%D1%83%D1%87%D1%88%D0%B8%D1%85_%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D0%BE%D0%B2_%D0%BF%D0%BE_%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B8_IMDb"]

    def parse(self, response):
        rows = response.xpath('//table[contains(@class,"sortable mw-collapsible standard jquery-tablesorter mw-made-collapsible")][1]/tbody/tr')        
        for row in rows:
            film_name = row.xpath(".//td[2]/a/text()").get()
            year = row.xpath('.//td[3]/a/text()').get()
            director = row.xpath('.//td[4]/a/text()').get()
            genre = row.xpath('.//td[5]/a/text()').get()
            link = row.xpath(".//td[2]/a/@href").get()
            yield response.follow(url=link, callback=self.parse_films,
                                  meta={
                                      'film_name': film_name,
                                      'year': year,
                                      'director': director,
                                      'genre' : genre
                                  })

    def parse_films(self, response):
        rows = response.xpath("//table[contains(@class,'wikitable sortable jquery-tablesorter')]/tbody/tr/td[1]")
        for row in rows:            
            film_name = response.request.meta['film_name']
            actor = row.xpath('.//a[1]/text()').get()
            year = response.request.meta['year']
            director = response.request.meta['director']
            genre = response.request.meta['genre']
            yield {
                'film_name': film_name.strip() if film_name else '',
                'actor': actor.strip() if actor else '',
                'year': year.strip() if year else '',
                'director': director.strip() if director else '',
                'genre': genre.strip() if genre else ''
            }
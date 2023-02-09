# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    start_urls = ['https://www.themoviedb.org/tv/1411-person-of-interest/']
    
    def parse(self, response):
        next_page = response.css('p.new_button a::attr(href)').get()
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page, callback=self.parse_full_credits)
    
    def parse_full_credits(self,response):
        # select the entire crew
        credits = response.css('ol.people.credits')
        # select the actors only
        actors = credits.css('div.info')
        # get a list of URL's to only the actors :)
        links = actors.css('a::attr(href)').getall()
        # go to every link!!!
        for link in links:
            next_page = response.urljoin(link)
            yield scrapy.Request(next_page, callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        # get the name :)
        name = response.css('h2.title a::text').get()

        # select the card that has all their credits
        card_credits = response.css('table.card.credits')
        # get all the names of the movies they've acted in into list of strings!
        movies = card_credits.css('a.tooltip bdi::text').getall()
        # last step is to yield the actor and one movie into a dictionary
        for movie in movies:
            pair = {'actor':name,
                   'movie_or_TV_name': movie}
            yield pair





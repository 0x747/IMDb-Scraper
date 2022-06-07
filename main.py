import IMDbScraper
import random
import time

movie = IMDbScraper.IMDb_Scraper()

while(1):
    user_input = input("IMDb URL or Title: ")

    if (user_input):
        movie.scrape(user_input)
        movie.print_metadata()
        movie.generate_webpage()

        delay = random.randint(696,1337) / 100
        print("Please wait", str(delay) + "s", end = "\r")
        time.sleep(delay)
    else:
        break
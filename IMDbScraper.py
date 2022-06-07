from bs4 import BeautifulSoup 
import requests
import json 
import re
import random
import time
import useragents

class IMDb_Scraper(): 

    def __init__(self) -> None:
        pass

    def scrape(self, user_input: str) -> dict:

        metadata = {}
        temp_dict = {}
        temp_list = [] 
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        if ("https://www.imdb.com/title/" not in user_input):
            user_input = user_input.replace(" ", "+")

            # Google search query URL
            google_url = "https://www.google.com/search?q=" + user_input + "+IMDb"

            # Fetches the HTML code of the google search
            temp = requests.get(google_url)
            google_doc = BeautifulSoup(temp.text, "html.parser")
            if(google_doc):
                print("\n[1/2] Fecthed HTML from Google", end = "\r")

            # Fecthed the IMDb link
            raw_url = google_doc.find(href=re.compile("https://www.imdb.com/title"))
            raw_url = raw_url.get("href")[7:]
            imdb_url = raw_url[:37]
            delay = random.randint(69, 197) / 100
            print("[...] Fetching IMDb page in", str(delay) + "s...", end = "\r")
            time.sleep(delay)
        else:
            imdb_url = user_input

        self.url = metadata["imdb_url"] = imdb_url

        # Picks a random user agent for every scrape
        random_user_agent = random.choice(useragents.user_agents)

        # Sends a request to get the HTML code of the IMDb page and then BS parses the HTML
        html_doc = requests.get(imdb_url, headers = random_user_agent)
        soup = BeautifulSoup(html_doc.text, "html.parser")

        # Looks for the script tag which has the JSON information about the title
        raw_json = soup.find("script", {"id": "__NEXT_DATA__"}).string
        if(raw_json):
            print("[2/2] Fetched JSON string from IMDb", end="\r")

        # Converts JSON to iterable Python dictionary
        my_dict = json.loads(raw_json)

        # Title and Original Title 
        try:
           self.title = metadata["title"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["titleText"]["text"]
        except KeyError:
            self.title = metadata["title"] = ""
            pass

        try:
            self.original_title = metadata["original_title"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["originalTitleText"]["text"]
        except KeyError:
            self.original_title = metadata["original_title"] = ""
            pass

        # Title Type
        try:
            self.title_type = metadata["title_type"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["titleType"]["text"]
        except KeyError:
            self.title_type = metadata["title_type"] = ""
            pass

        # Rating 
        try:
            self.age_rating = metadata["age_rating"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["certificate"]["rating"]
        except (KeyError, TypeError):
            self.age_rating = metadata["age_rating"] = ""
            pass

        # Release Date Timeline/Range
        try:
            self.year = metadata["year"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["releaseYear"]["year"]
        except KeyError:
            self.year = metadata["year"] = ""
            pass

        try:
            self.end_year = metadata["end_year"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["releaseYear"]["endYear"]
        except KeyError:
            self.end_year = metadata["end_year"] = ""
            pass
        
        try:
            self.day = metadata["day"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["releaseDate"]["day"]
        except KeyError:
            self.day = metadata["day"] = ""
            pass

        try:
            self.month = metadata["month"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["releaseDate"]["month"]
        except KeyError:
            self.month = metadata["month"] = ""
            pass

        self.date = months[self.month - 1] + " " + str(self.day) + ", " + str(self.year)

        # Runtime 
        try:
            self.runtime = metadata["runtime"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["runtime"]["seconds"]
        except (KeyError, TypeError):
            self.runtime = metadata["runtime"] = ""
            pass

        # Plot Summary
        try:
            self.plot = metadata["plot"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["plot"]["plotText"]["plainText"]
        except KeyError:
            self.plot = metadata["plot"] = ""
            pass

        # IMDb Rating and Vote Count
        try:
            self.imdb_rating = metadata["imdb_rating"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["ratingsSummary"]["aggregateRating"]
        except KeyError:
            self.imdb_rating = metadata["imdb_rating"] = ""
            pass

        try:
            self.votes = metadata["votes"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["ratingsSummary"]["voteCount"]
        except KeyError:
            self.votes = metadata["votes"] = ""
            pass

        # Poster
        try:
            self.poster_url = metadata["poster_url"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["primaryImage"]["url"]
        except KeyError:
            self.poster_url = metadata["poster_url"] = ""
            pass

        # Trailer
        try:
            self.trailer_url = metadata["trailer_url"] = my_dict["props"]["pageProps"]["aboveTheFoldData"]["primaryVideos"]["edges"][0]["node"]["playbackURLs"][0]["url"]
        except (IndexError, KeyError):
            self.trailer_url = metadata["trailer_url"] = ""
            pass

        # Genres
        try:
            temp_dict = my_dict["props"]["pageProps"]["aboveTheFoldData"]["genres"]["genres"]
            for i in range(len(temp_dict)):
                temp_list.append(temp_dict[i]["text"])
            
            self.genre = metadata["genre"] = temp_list
            temp_dict = {}
            temp_list = []
        except KeyError:
            self.genre = metadata["genre"] = []
            pass

        # Cast
        try:
            temp_dict = my_dict["props"]["pageProps"]["aboveTheFoldData"]["castPageTitle"]["edges"]
            for i in range(len(temp_dict)):
                temp_list.append(temp_dict[i]["node"]["name"]["nameText"]["text"])
            
            self.cast = metadata["cast"] = temp_list
            temp_dict = {}
            temp_list = []
        except KeyError:
            self.cast = metadata["cast"] = []
            pass

        # Directors
        try:
            temp_dict = my_dict["props"]["pageProps"]["aboveTheFoldData"]["directorsPageTitle"][0]["credits"]
            for i in range(len(temp_dict)):
                temp_list.append(temp_dict[i]["name"]["nameText"]["text"])
            
            self.directors = metadata["directors"] = temp_list
            temp_dict = {}
            temp_list = []
        except (KeyError, IndexError):
            self.directors = metadata["directors"] = []
            pass

        # Writers
        try:
            temp_dict = my_dict["props"]["pageProps"]["mainColumnData"]["writers"][0]["credits"]
            for i in range(len(temp_dict)):
                temp_list.append(temp_dict[i]["name"]["nameText"]["text"])

            self.writers = metadata["writers"] = temp_list
            temp_dict = {}
            temp_list = []
        except (KeyError, IndexError):
            self.writers = metadata["writers"] = []
            pass

        # Keywords
        try:
            temp_dict = my_dict["props"]["pageProps"]["aboveTheFoldData"]["keywords"]["edges"]
            for i in range(len(temp_dict)):
                temp_list.append(temp_dict[i]["node"]["text"])

            self.keywords = metadata["keywords"] = temp_list
            temp_dict = {}
            temp_list = []
        except KeyError:
            self.keywords = metadata["keywords"] = []
            pass

        return metadata
    
    def format_runtime(self, seconds: int) -> str:

        minutes = int(seconds / 60)
        sub_minutes = int(minutes % 60)
        hours = int((minutes - sub_minutes) / 60)

        return str(hours) + "h " + str(sub_minutes) + "m"

    def to_string(self, user_list: list) -> str:

        bad_chars = "[']"
        string = str(user_list)

        for char in bad_chars:
            string = string.replace(char, "")
        
        return string

    def print_metadata(self):

        print("\nTitle:", self.title)
        if (self.title != self.original_title):
            print("Original Title:", self.original_title)
        print("Type:", self.title_type)
        print("Year:", self.year)
        print("Runtime:", self.format_runtime(self.runtime))
        print("Date: ", self.date)
        print("Age Rating:", self.age_rating)
        print("Genre:", self.to_string(self.genre))
        print("Cast:", self.to_string(self.cast))
        print("Directed by:", self.to_string(self.directors))
        print("Writers:", self.to_string(self.writers))
        print("Keywords:", self.to_string(self.keywords), "\n")

    def generate_webpage(self):

        raw_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" type="text/css" href="style.css">
            <title>IMDb Scraper</title>
        </head>
        <body>
            <div class="container">
                <div class="poster" style="background-image: url("""+ self.poster_url +""");"></div>
                <video src="""+ self.trailer_url +""" controls type="video/mp4" height="500px"></video>
                <div class="information">
                    <p id="title"><b>Name:</b> """+ self.title +"""</p>
                    <p id=alttitle><b>Alternate Name:</b> """+ self.original_title +"""</p>
                    <p id="type"><b>Type:</b> """+ self.title_type +"""</p>
                    <p id="year"><b>Year:</b> """+ str(self.year) +"""</p>
                    <p id="duration"><b>Duration:</b> """+ self.format_runtime(self.runtime) +"""</p>
                    <p id="releasedate"><b>Release Date:</b> """+ self.date +"""</p>
                    <p id="filmrating"><b>Age Rating:</b> """+ self.age_rating +"""</p>
                    <p id="genre"><b>Genre:</b> """+ self.to_string(self.genre) +"""</p>
                    <p id="actors"><b>Cast:</b> """+ self.to_string(self.cast) +"""</p>
                    <p id="directors"><b>Directors:</b> """+ self.to_string(self.directors) +"""</p>
                    <p id="writers"><b>Writers:</b> """+ self.to_string(self.writers) +"""</p>
                    <p id="imdbrating"><b>IMDb Rating:</b> """+ str(self.imdb_rating) +""" / 10 ("""+ str(self.votes) +""" ratings)</p>
                    <p id="plot"><b>Plot:</b> """+ self.plot +"""</p>
                    <p id="keywords"><b>Keywords:</b> """+ self.to_string(self.keywords) +"""</p>
                    <a href="""+ self.poster_url +""" target="_blank" download>
                        <button class="posterdownload">Download Poster</button>
                    </a>
                    <a href="""+ self.trailer_url +""" target="_blank" download="Trailer">
                        <button class="trailerdownload">Download Trailer</button>
                    </a>
                </div>
            </div>
        </body>
        </html>
        """
        html_file = open("index.html", "w")
        html_file.write(raw_html)

    
        
from bs4 import BeautifulSoup
import requests
import json
import re

print('''Enter an IMDb link or simply write the name of the movie or show

See examples below:

URL or Name: https://www.imdb.com/title/tt0114709 
URL or Name: Zero Days\n\n''')

def scrape_data():

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    jsondata = doc.find("script").string
    mydict = json.loads(jsondata)

    # Movie Title
    # title = doc.find("h1").string
    title = mydict["name"]
    alt_title = "None"
    try:
        alt_title = mydict["alternateName"]
    except KeyError:
        pass
    
    # Year and Age Rating 
    #year_and_rating = doc.find_all("span", {"class": "sc-8c396aa2-2"})
    #year = year_and_rating[0].string
    # age_rating = year_and_rating[1].string
    release_date = "Not Available"
    year = "Not Available"
    try:
        release_date = mydict["datePublished"]
        year = release_date[:4]
    except KeyError:
        year = doc.find("a", {"class": "ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh"}).string
        release_date = year[:4]

    age_rating = "Not Rated"
    try:
        age_rating = mydict["contentRating"]
    except KeyError:
        pass

    # Type 
    type = mydict["@type"]

    if (type == "TVSeries"):
        type = "TV Series"

    # Genre
    bad_chars = "[']"
    genre = str(mydict["genre"])

    for char in bad_chars:
        genre = genre.replace(char, "")

    # Runtime
    runtime = "Not Available"
    try:
        runtime = mydict["duration"]
    except KeyError:
        pass
    runtime = runtime.lstrip("PT").replace("H", "h ").replace("M", "m")

    # Directors
    raw_directors_list = ""
    try:
        raw_directors_list = mydict["director"]
    except KeyError:
        pass

    directors = ""
    for i in range(len(raw_directors_list)):
        try:
            directors += mydict["director"][i]["name"] + ", "
        except KeyError:
            pass
    
    directors = directors[:-2]

    # Actors
    raw_actors_list = mydict["actor"]
    actors = ""
    for i in range(len(raw_actors_list)):
        actors += mydict["actor"][i]["name"] + ", "

    actors = actors[:-2]

    # Writers 
    raw_writers_list = ""
    try:
        raw_writers_list = mydict["creator"]
    except KeyError:
        pass
    writers = ""
    for i in range(1, len(raw_writers_list)):
        try:
            writers += mydict["creator"][i]["name"] + ", "
        except KeyError:
            pass

    writers = writers[:-2]
    
    # Poster Image
    # poster = doc.find("meta", {"property": "og:image"})['content']
    try:
        poster = mydict["image"]
    except KeyError:
        pass

    # Plot Summary 
    # summary = doc.find("span", {"class": "sc-16ede01-2 gXUyNh"}).string
    summary = ""
    try:
        summary = mydict["description"]
    except KeyError:
        pass

    # IMDb Rating 
    # rating = doc.find("span", {"class": "sc-7ab21ed2-1 jGRxWM"}).string
    rating = ""
    rating_count = ""
    try:
        rating = str(mydict["aggregateRating"]["ratingValue"])
        rating_count = str(mydict["aggregateRating"]["ratingCount"])
    except KeyError:
        pass

    # Keywords 
    keywords = ""
    try:
        keywords = mydict["keywords"]
        keywords = keywords.replace(",", ", ")
    except KeyError:
        pass

    # Trailer
    # x.props.pageProps.aboveTheFoldData.primaryVideos.edges[0].node.playbackURLs[0].url
    raw_json = doc.find("script", {"id": "__NEXT_DATA__"}).string
    mydict2 = json.loads(raw_json)

    trailer = ""
    try:
        trailer = mydict2["props"]["pageProps"]["aboveTheFoldData"]["primaryVideos"]["edges"][0]["node"]["playbackURLs"][0]["url"]
    except (IndexError, KeyError):
        pass

    print("IMDb URL Found:", url)
    print("\nTitle:", title)
    print("Alternate Title:", alt_title)
    print("Type:", type)
    print("Year:", year)
    print("Duration:", runtime)
    print("Release Date:", release_date)
    print("Age Rating:", age_rating)
    print("Genre:", genre)
    print("Directors:", directors)
    print("Actors:", actors)
    print("Writers:", writers)
    print("Poster URL:", poster)
    print("Plot:", summary)
    print("IMDb Rating:", rating, "/ 10", "(" + rating_count + " ratings)")
    print("Keywords:", keywords, "\n")

    htmltext = """
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
            <div class="poster" style="background-image: url("""+poster+""");"></div>
            <video src="""+trailer+""" controls type="video/mp4" height="500px"></video>
            <div class="information">
                <p id="title"><b>Name:</b> """+title+"""</p>
                <p id=alttitle><b>Alternate Name:</b> """+alt_title+"""</p>
                <p id="type"><b>Type:</b> """+type+"""</p>
                <p id="year"><b>Year:</b> """+year+"""</p>
                <p id="duration"><b>Duration:</b> """+runtime+"""</p>
                <p id="releasedate"><b>Release Date:</b> """+release_date+"""</p>
                <p id="filmrating"><b>Age Rating:</b> """+age_rating+"""</p>
                <p id="genre"><b>Genre:</b> """+genre+"""</p>
                <p id="actors"><b>Actors:</b> """+actors+"""</p>
                <p id="directors"><b>Directors:</b> """+directors+"""</p>
                <p id="writers"><b>Writers:</b> """+writers+"""</p>
                <p id="imdbrating"><b>IMDb Rating:</b> """+rating+""" / 10 ("""+rating_count+""" ratings)</p>
                <p id="plot"><b>Plot:</b> """+summary+"""</p>
                <p id="keywords"><b>Keywords:</b> """+keywords+"""</p>
                <a href="""+poster+""" target="_blank" download>
                    <button class="posterdownload">Download Poster</button>
                </a>
                <a href="""+trailer+""" target="_blank" download="Trailer">
                    <button class="trailerdownload">Download Trailer</button>
                </a>
            </div>
        </div>
    </body>
    </html>
    """

    htmlfile = open("index.html", "w")
    htmlfile.write(htmltext)

loop = True;
while(loop):
    user_input = input("URL or Name: ")

    if(user_input):
        if ("https://www.imdb.com/title/" not in user_input):
            user_input = user_input.replace(" ", "+")
            google_url = "https://www.google.com/search?q=" + user_input + "+IMDb"
            temp = requests.get(google_url)
            goog_doc = BeautifulSoup(temp.text, "html.parser")

            raw_url = goog_doc.find_all(href=re.compile("https://www.imdb.com/title"))
            raw_url = raw_url[0].get("href")[7:]
            url = raw_url[:37]
        else:
            url = user_input
        scrape_data()
    else:
        break;
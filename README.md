# IMDb Scraper [BETA]
A simple webscraper which can extract metadata from a movie or show's IMDb page

## Getting Started 
**[ ! ] Before you begin**
1. Make sure all files are in the same directory 
2. Do not try to scrape multiple films in a short amount of time. IMDb will throttle your connection or ban your IP. Add a random time delay using `time.sleep()` as seen in `main.py` 
```
import IMDbScraper

# Create an instance 
movie = IMDbScraper.IMDb_Scraper()

# Start scraping
movie.scrape("Morbius")
movie.scrape("https://www.imdb.com/title/tt5108870/?ref_=fn_al_tt_1")

# Output
> Title: Morbius
> Type: Movie
> Year: 2022
> Runtime: 1h 44m
> Date:  April 1, 2022
> Age Rating: PG-13
> Genre: Action, Adventure, Horror, Sci-Fi, Thriller
> Cast: Jared Leto, Matt Smith, Adria Arjona, Jared Harris
> Directed by: Daniel Espinosa
> Writers: Matt Sazama, Burk Sharpless
> Keywords: vampire, based on comic, marvel comics, superhero, blood
```

![Command Line Interface](/assets/console.PNG "Terminal")

## Attributes

|  **Attribute** |**Data type**|
|:-------------- |:-----------:|
| title          | str         |
| original_title | str         |
| title_type     | str         |
| year           | int         |
| end_year       | int         |
| day            | int         |
| month          | int         |
| date           | str         |
| runtime        | int         |
| age_rating     | str         |
| imdb_rating    | int         |
| votes          | int         |
| plot           | str         |
| poster_url     | str         |
| trailer_url    | str         |
| url            | str         |
| genre          | list        |
| cast           | list        |
| directors      | list        |
| writers        | list        |
| keywords       | list        |

## Functions

### 1. scrape(str)
Takes the name of a movie/show or an IMDb title page URL (https://www.imdb.com/title/tt0111161). Returns a dictionary with all extracted metadata.

### 2. format_runtime(int)
Converts seconds to equivalent hours and minutes and formats them into a string, which is returned.
```
format_runtime(5570)

# Returns 
> 1h 32m
```

### 3. print_metadata()
Prints the metadata in a readable format

### 4. to_string(list)
Returns a formatted string from list
```
my_list = ["spam", "eggs", "foo", "bar"]
to_string(my_list)

# Returns 
> spam, eggs, foo, bar
```

### 5. generate_webpage() 
Creates a simple webpage using the scraped data with the poster and trailer

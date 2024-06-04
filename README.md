# IMDB_scraper
IMDB_scraper will genrate a database containing page dumps for all the URL links mentioned in film_scraper.py file.
It will create the films.db file which can be further used for scraping using SQLITE and beautifulsoup.
It consists of 4 files mentioned below:

db.py:
This file contains code for db management.

film_scraper.py:
This file contains code for reading and dumping imdb links into the database (films.db)

film_preprocess.ipynb:
This file process creates the csv file (films_to_scrape.csv) containing list of films to scrape from web filtered by numofvotes in decreasing order.

film_postprocess.ipynb:
This file is executed after film_scraper.py is finished and films.db is completed.	
It contains code to scrape the dump pages for the required information and create relevant CSV/TSV files like, keywords, locations etc.

# Steps to follow:
## pre-processing
Step-1: execute film_preprocess.ipynb file in jupyter
Result: films_to_scrape.csv file created under folder data/

## Requirements
Step-2: Open anaconda command prompt and execute below requirements.
Requirements (Anaconda):
$ conda install pandas scrapy beautifulsoup4
or (Other)
$ pip install pandas scrapy beautifulsoup4

## Run scraper
Step-3: execute film_scraper python script
(in conda or other env)
$ python3 film_scraper.py

## Monitoring
Step-4: Keep checking the terminal. If script is stopped due to any failure, restart the script. It will resume further.
As the list contains million of films, it will take approximately two weeks time. Be patient :)

Result: films.db file under folder data/

## post-processing
Step-5: Once film_scraper.py is finished. Execute film_postprocess file to extract csv/tsv files from page dumps in films.db
execute film_postprocess.ipynb in jupyter.
## WFP VAM API Scraper
Scraper for the [WFP VAM API](http://reporting.vam.wfp.org/api/).

## Usage

If you are on an Unix machine run:
```bash
$ bash run.sh
```

Or you can run directly using Python:
```bash
$ python code/scraper.py
```
The results will be stored in CSV files, JSON files, and / or a SQLite database called "scraperwiki.sqlite".


## Making Queries
The queries seem to be unique. That is, an user will have to make a large number of queries (i.e. *hundreds of thousands*) in order to collect the complete database. The scraper was designed to make those queries automatically and store the resulting data.


## Parallel Processing
To be written.
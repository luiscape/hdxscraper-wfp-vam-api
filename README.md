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

## Cleaning Data
The modified GAUL boundary set provided by the VAM unit contains around 50k administrative codes. However, the provision starts at the admin 2 level, meaning that codes for amin 0 and admin 1 don't have individual records. We need those records in order to query for admin 1 units or admin 0 units without specifying a further level of disaggregation. The `clean_admin_codes.R` script solves that issue by creating those missing records. To run do:

```bash 
$ Rscript code/clean_admin_codes.R
```

A new CSV file titled `modified_admin_units.csv` will be generated to the [config](config/) directory.

## Making Queries
The queries seem to be unique. That is, an user will have to make a large number of queries (i.e. *hundreds of thousands*) in order to collect the complete database. The scraper was designed to make those queries automatically and store the resulting data.

## Parallel Processing
To be written.
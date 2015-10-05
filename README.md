## WFP VAM API Collector
Collector for the [WFP VAM API](http://reporting.vam.wfp.org/api/).

[![Build Status](https://travis-ci.org/luiscape/hdxscraper-wfp-vam-api.svg?branch=master)](https://travis-ci.org/luiscape/hdxscraper-wfp-vam-api) [![Coverage Status](https://coveralls.io/repos/luiscape/hdxscraper-wfp-vam-api/badge.svg)](https://coveralls.io/r/luiscape/hdxscraper-wfp-vam-api)


## Usage

If you are on an Unix machine, you can use the Makefile to run this collector:
```makefile
test:
  bash bin/test.sh;

setup:
  bash bin/setup.sh;

run:
  bash bin/run.sh;

```

Or you can run directly using Python:
```bash
$ python scripts/wfp_collect/
```
The results will be stored in CSV files, JSON files, and / or a SQLite database called "scraperwiki.sqlite".


## Cleaning Data
The modified GAUL boundary set provided by the VAM unit contains around 50k administrative codes. However, the provision starts at the admin 2 level, meaning that codes for amin 0 and admin 1 don't have individual records. We need those records in order to query for admin 1 units or admin 0 units without specifying a further level of disaggregation. The `clean_admin_codes.R` script solves that issue by creating those missing records. To run do:

```bash
$ Rscript code/clean_admin_codes.R
```

A new CSV file titled `modified_admin_units.csv` will be generated to the [config](config/) directory.

## Making Queries
The queries seem to be unique. That is, an user will have to make a large number of queries (*hundreds of thousands*) in order to collect the complete database. This scraper was designed to make those queries automatically and store the resulting data.

# API Design
The current API design imposes on the user the assumption that he knows a considerable amount of information before issuing queries. Users have to know exactly the combination of administrative units, indicator type IDs, and other variables in order to get the series she is interested on. In sum, the API isn't designed for exploration.

To go around this issue, this scraper issues queries using the combination of available query parameters. Considering that there are around 60 thousand locations available, the combination of variables result in nearly one million queries. This is inefficient and costly in computational terms.

## Parallel Requests
This collector makes `N` number of parallel requests to the WFP API. Inside the `__main__` script of the `wfp_collect` module, you can tweek that parameter as follows:

```python
kwargs = {'query_limit': 50}
```
There are a number of considerations including system resources (i.e. memory), bandwidth, and server status that may affect the maximum number of parallel requests allowed. We've had mixed results, but have settled in 50 requests at a time.
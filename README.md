# KindleScrape
A collection of python scripts for scraping the German Amazon ebook store, using keywords and metrics.


# Scrape

Used to fetch books for certain keywords and genres from Amazon.

Usage: `python scrape.py [search name] [keyword 1] [keyword 2] [keyword 3] (etc)`

Example: `python scrape.py krimisuche kriminalroman detektiv mord`

The following infos about the books are collected: title, author, blurb (description), price, if the book is enrolled in the Kindle Unlimited program, number of reviews, average rating, number of pages, ranking and categories in which it is ranked, keywords, url.

The config file parameter "result pages" specifies how many pages of results for every keyword should be scraped for books. The default is currently set to 6.

Because of small variations in the amazon interface, some data can not always be fetched. E.g. the page number is not displayed for freshly published books and can therefore not be scraped. The script is quite resilient against scraping errors, it just carries on with the next book.

![example 1](https://github.com/LauraWartschinski/KindleScrape/blob/master/example.png)

The output is stored in a csv file. JSON files are created to save the progress.



# Keyword Checker

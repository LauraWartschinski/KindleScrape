# KindleScrape
A collection of python scripts for scraping the German Amazon ebook store, using keywords and metrics. The main purpose is to easily collect data on books in certain topics, genres or niches for further evaluation. 

# Scrape

Used to fetch books for certain keywords and genres from Amazon.

Usage: `python scrape.py [search name] [keyword 1] [keyword 2] [keyword 3] (etc)`

Example: `python scrape.py krimisuche kriminalroman detektiv mord`

The following infos about the books are collected: title, author, blurb (description), price, if the book is enrolled in the Kindle Unlimited program, number of reviews, average rating, number of pages, ranking and categories in which it is ranked, keywords, url.

The config file parameter "result pages" specifies how many pages of results for every keyword should be scraped for books. The default is currently set to 6.

Because of small variations in the amazon interface, some data can not always be fetched. E.g. the page number is not displayed for freshly published books and can therefore not be scraped. The script is quite resilient against scraping errors, it just carries on with the next book.

![example 1](https://github.com/LauraWartschinski/KindleScrape/blob/master/example.png)

The output is stored in a csv file. JSON files are created to save the progress. When an URL is encountered for which the content of the book is already scraped, it will not be loaded again, but the keywords will be updated. This is to reduce the total number of requests and to prolong the time the script can run without excessive captcha problems. Also, different host headers are used to migitate the problem some more.



![example 2](https://github.com/LauraWartschinski/KindleScrape/blob/master/example2.png)


![example 3](https://github.com/LauraWartschinski/KindleScrape/blob/master/example3.png)

If the script is interrupted, it will reload the progress since the last completed searched keyword and resume from there. If captcha problems arise, there will be a warning message. To circumvent captchas, consider using a proxy.





# Verify

Usage: `python verify.py [search name]`
With the same parameter that was used as a search name before.

Sometimes, books end up in the wrong categories or show up under wrong search terms. Maybe amazon or the author miscategorized them, or maybe we just didn't pick perfect search keywords. With the verification script, you can specifiy which words MUST be in the title or MUST be in the description of the book to keep it as a book with a certain keyword. Also, you can specify which words will cause a book to be considered NOT an example of the keyword, as well as required categories it must have a rated placement in.


![example 4](https://github.com/LauraWartschinski/KindleScrape/blob/master/example4.png)

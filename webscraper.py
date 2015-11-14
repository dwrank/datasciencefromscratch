#!/usr/bin/env python

from __future__ import division

import sys
import re
import requests
import csv
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from collections import Counter
from time import sleep
from pprint import pprint


def is_video(td):
    '''it's a video if it has exactly one procelabel, and if
    the stripped text inside starts with Video'''
    pricelabels = td('span', 'pricelabel')
    return (len(pricelabels) == 1 and
            (pricelabels[0].text.strip().startswith('Video') or
             pricelabels[0].text.strip().startswith('Early Release Video')))


def book_info(td):
    '''given a BeautifulSoup <td> tag representing a book,
    extract the book's details and return a dict'''
    
    title = td.find('div', 'thumbheader').a.text
    author_name = td.find('div', 'AuthorName').text
    authors = [x.strip() for x in re.sub('^By ', '', author_name).split(',')]
    isbn_link = td.find('div', 'thumbheader').a.get('href')
    isbn = re.match('/product/(.*)\.do', isbn_link).group(1)
    date = td.find('span', 'directorydate').text.strip()

    return {
            'title' : title.encode("utf-8"),
            'authors' : [author.encode("utf-8") for author in authors],
            'isbn' : isbn.encode("utf-8"),
            'date' : date.encode("utf-8")
            }


def get_year(book):
    '''book['date'] looks like 'November 2014', so we need to
    split on the space and then take the second piece'''
    
    # \xa0 is a non-breaking space (\xc2\xa0 in utf-8)
    date = book['date'].replace('\xc2\xa0', ' ').split()
    return int(date[1])


def get_books(csvfile):
    books = []
    NUM_PAGES = 39
    
    base_url = 'http://shop.oreilly.com/category/browse-subjects/' + \
          'data.do?sortby=publicationDate&page='
    
    for page_num in range(1, NUM_PAGES + 1):
        print('souping page %d, %d books found so far' % (page_num, len(books)))
        sys.stdout.flush()
        url = base_url + str(page_num)
        soup = BeautifulSoup(requests.get(url).text, 'html5lib')
        
        # each book is in <td class="thumbtext">
        for td in soup('td', 'thumbtext'):
            if not is_video(td):
                books.append(book_info(td))
    
        # respect the robots.txt policy
        if page_num < NUM_PAGES:
            sleep(30)
    
    with open(csvfile, 'wb') as f:
        csvwriter = csv.DictWriter(f, delimiter='\t',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL,
                                  fieldnames=books[0].keys())
        
        csvwriter.writeheader()
        csvwriter.writerows(books)
        f.flush()


def plot_books(csvfile):
    books = []
    
    with open(csvfile, 'rb') as f:
        csvreader = csv.DictReader(f, delimiter='\t', quotechar='|')
        for row in csvreader:
            books.append(row)
            
    # returns dict{<year>:<book_counts>}
    year_counts = Counter(get_year(book) for book in books if get_year(book) <= 2015)
    pprint(year_counts)
    years = sorted(year_counts)  # returns dict keys in ascending order
    pprint(years)
    book_counts = [year_counts[year] for year in years]
    pprint(book_counts)
    plt.plot(years, book_counts)
    plt.ylabel("# of data books")
    plt.title("Data is Big!")
    # map years to string values for explicit labels
    plt.xticks(years, map(lambda x: "%g" % x, years))
    pprint(map(lambda x: "%g" % x, years))
    plt.show()


csvfile = 'books.csv'
#get_books(csvfile)
plot_books(csvfile)

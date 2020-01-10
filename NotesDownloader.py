import requests
import validators
import sys
from bs4 import BeautifulSoup as bs
from urlparse import urlparse
import wget
import urllib2

def check_validity(my_url):
    try:
        urllib2.urlopen(my_url)
        print("Valid URL")
    except IOError:
        print ("Invalid URL")
        sys.exit()


def get_pdfs(my_url):
    links = []
    html = urllib2.urlopen(my_url).read()
    html_page = bs(html, features="lxml")   
    og_url = html_page.find("meta",  property = "og:url")
    base = urlparse(my_url)
    for link in html_page.find_all('a'):
        current_link = link.get('href')
        if current_link.endswith('pdf'):
            if og_url:
                links.append(og_url["content"] + current_link)
            else:
                links.append(base.scheme + "://" + base.netloc + current_link)
    for link in links:
        wget.download(link)


def main():
    print("Enter Link: ")
    my_url = raw_input()
    check_validity(my_url)
    get_pdfs(my_url)

main()


# https://grader.eecs.jacobs-university.de/courses/320241/2019_2
# https://cnds.jacobs-university.de/courses/os-2019/

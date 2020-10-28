import requests
import validators
import sys
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import wget
from urllib.request import urlopen
import urllib.request 

def check_validity(my_url):
    try:
        urlopen(my_url)
        print("Valid URL")
    except IOError:
        print ("Invalid URL")
        sys.exit()


def get_pdfs(my_url):
    links = []
    html = urlopen(my_url).read()
    html_page = bs(html, features="lxml") 
    og_url = html_page.find("meta",  property = "og:url")
    base = urlparse(my_url)
    print("base",base)
    for link in html_page.find_all('a'):
        current_link = link.get('href')
        if current_link.endswith('pdf'):
            if og_url:
                print("currentLink",current_link)
                links.append(og_url["content"] + current_link)
            else:
                links.append(base.scheme + "://" + base.netloc + current_link)

    for link in links:
        try: 
            wget.download(link)
        except:
            print(" \n \n Unable to Download A File \n")
    print('\n')


def main():
    print("Enter Link: ")
    my_url = input()
    check_validity(my_url)
    get_pdfs(my_url)

main()


# https://grader.eecs.jacobs-university.de/courses/320241/2019_2
# https://cnds.jacobs-university.de/courses/os-2019/

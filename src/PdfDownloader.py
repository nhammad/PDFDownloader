import requests
import validators
import sys
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import wget
from urllib.request import urlopen
import urllib.request
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def check_validity(my_url):
    try:
        urlopen(my_url)
        print("Valid URL")
    except IOError:
        print ("Invalid URL")
        sys.exit()

def extract_text(my_url):
    html = urlopen(my_url).read()
    html_page = bs(html, features="lxml")
    text = html_page.get_text()
    return text

def train_model():
    # Load training data
    training_data = []
    with open('training_data.txt', 'r') as f:
        for line in f:
            training_data.append(line.strip())

    # Vectorize training data
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(training_data)

    # Train model
    y_train = np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 0])
    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    return vectorizer, clf

def predict_relevant_pdfs(my_url, vectorizer, clf):
    # Extract text from webpage
    text = extract_text(my_url)

    # Vectorize text
    X_test = vectorizer.transform([text])

    # Predict relevance of PDFs
    y_pred = clf.predict(X_test)

    # Search for PDFs based on relevance
    if y_pred == 1:
        search_query = 'related: ' + my_url + ' filetype:pdf'
    else:
        search_query = 'filetype:pdf'
    search_url = 'https://www.google.com/search?q=' + search_query
    search_results = requests.get(search_url)
    search_results_page = bs(search_results.text, 'html.parser')
    pdf_links = []
    for link in search_results_page.find_all('a'):
        href = link.get('href')
        if href.startswith('/url?q='):
            url = href.split('=')[1].split('&')[0]
            if url.endswith('.pdf'):
                pdf_links.append(url)
    return pdf_links

def download_pdfs(pdf_links):
    for link in pdf_links:
        try:
            wget.download(link)
        except:
            print(" \n \n Unable to Download A File \n")
    print('\n')

def main():
    print("Enter Link: ")
    my_url = input()
    check_validity(my_url)
    vectorizer, clf = train_model()
    pdf_links = predict_relevant_pdfs(my_url, vectorizer, clf)
    download_pdfs(pdf_links)

main()

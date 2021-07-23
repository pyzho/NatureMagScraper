import os
import re
import requests
import string
from bs4 import BeautifulSoup

punct = string.punctuation+'’'
replace = {}

for symbol in punct:
    replace.update({symbol: ''})
replace.update({' ': '_'})

n_pages = int(input('Place number of pages to parse'))
art_type = str(input('Choose topic'))

for i in range(n_pages):

    page = requests.get('https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page=' + str(i+1))

    soup = BeautifulSoup(page.content, 'html.parser')

    articles = soup.find_all('article')
    new_dir = 'Page_' + str(i+1)

    if os.access(new_dir, os.F_OK):
        pass
    else:
        os.mkdir(new_dir)
    os.chdir(new_dir)

    print('create and move to ' + new_dir)

    for tag in articles:
        spans = tag.find_all('span', {'class': "c-meta__type"})
        for p in spans:
            if p.text == art_type:
                name = tag.a.text.maketrans(replace)
                name = tag.a.text.translate(name) + '.txt'
                file = open(name, 'w', encoding='utf-8')
                link = tag.find('a', {'data-track-action': "view article"})
                article = requests.get('https://www.nature.com' + link.get('href'))
                soup_article = BeautifulSoup(article.content, 'html.parser')

                body = soup_article.find("div", class_=re.compile(".*body.*")).text.strip()

                file.write(body)
                file.close()

    os.chdir(os.path.dirname(os.getcwd()))

print('completed')

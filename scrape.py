import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urls = [
    "https://english.onlinekhabar.com/",
    "https://kathmandupost.com/",
    "https://english.nepalpress.com/",   
]
fileName = 'politicalNews.json'
links = []
electionLingo = ['election', 'vote', 'voting', 'pm karki', 'nepali congress','hor election']
badLingo = ['tag','category']
allData = []

def crawlForLinks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href: 
            continue
        href = urljoin(url, href)
        if href.startswith(url) and  any(word in href.lower() for word in electionLingo) and href not in links and not any(badLingo in href.lower() for badLingo in badLingo):
            links.append(href)


def crawlForArticle(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text.strip() if soup.find('title') else 'No Title'
    content = soup.find_all('p')
    content = ' '.join([p.text.strip() for p in content])
    article_data = {
        'url': url,
        'title': title,
        'content': content
    }
    allData.append(article_data)
    
for url in urls:
    crawlForLinks(url)
for link in links:
    crawlForArticle(link)

with open(fileName, 'w') as f:
    json.dump(allData, f, indent=4)
print(f"Scraped {len(allData)} articles from {len(links)} links.") 
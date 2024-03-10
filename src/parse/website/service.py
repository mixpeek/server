import sys
import json
import socket
import requests
import traceback
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebScraper():

    def __init__(self, url, maxDepth) -> None:
        url = url.strip()
        if not 'http' in url:
            if not 'www.' in url:
                url = 'www.'+url
            url = 'http://'+url
        self.url = url
        self.maxDepth = maxDepth
        self.data = {
            'Image': [],
            'Video': [],
            'Audio': [],
            'PDF': [],
            'HTML': [],
            'Internal': [self.url, ]
        }

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)

    @staticmethod
    def isConnected():
        # Function to check internet connection
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("1.1.1.1", 53))
            return True
        except OSError:
            pass
        return False

    def isValid(self, url):
        # Checks whether `url` is a valid URL.
        parsed = urlparse(url)

        if not bool(parsed.netloc) or not bool(parsed.scheme):
            return False

        # Check if the same URL already exists in the Internal list
        stripped_url = parsed.netloc + parsed.path
        # remove www
        stripped_url = stripped_url.lstrip('www.')
        # remove backslash
        stripped_url = stripped_url.rstrip('/')
        if any(stripped_url in s for s in self.data['Internal']):
            return False
        return True

    def extractImageUrls(self, soup, site):
        # Function to extract image urls from the site
        img_tags = soup.find_all('img')
        urls = [img['src'] for img in img_tags]
        for url in urls:
            if '.png' or '.gif' or '.jpg' in url:
                if 'http' not in url:
                    # Format the url correctly if http or https not found
                    url = '{}{}'.format(site, url)
                if url not in self.data['Image']:
                    self.data['Image'].append(url)

    def getData(self, url, soup):
        def addType(href):
            # Add passed url to the correct dictonary type
            if '.png' in href or '.gif' in href or '.jpg' in href and href not in self.data['Image']:
                self.data['Image'].append(href)
            elif '.html' in href and href not in self.data['HTML']:
                self.data['HTML'].append(href)
            elif '.pdf' in href and href not in self.data['PDF']:
                self.data['PDF'].append(href)
            elif '.mp3' in href and href not in self.data['Audio']:
                self.data['Audio'].append(href)
            elif '.mp4' in href or '.mpeg' in href or '.wov' in href or '.avi' in href or '.mkv' in href and href not in self.data['Video']:
                self.data['Video'].append(href)

        domainName = urlparse(url).netloc
        for tag in soup.findAll("a"):
            href = tag.attrs.get("href")
            if href == "" or href is None:
                # href empty tag
                continue
            href = urljoin(url, href)

            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not self.isValid(href):
                # not a valid URL
                continue
            addType(href)
            if domainName in href and href not in self.data['Internal']:
                self.data['Internal'].append(href)

    def recursiveScrap(self, i):
        def getPage(url):
            oddUrl = ['.jpg', '.jpeg', '.png', '.pdf', '.xlsx']
            for i in oddUrl:
                if i in url:
                    return 'XXX', None
            htmlHeaders = ['text/css', 'text/csv', 'text/html',
                           'text/javascript (obsolete)', 'text/plain', 'text/xml']
            try:
                self.driver.get(url)

                soup = BeautifulSoup(self.driver.page_source, "html.parser")

                for htmlHeader in htmlHeaders:
                    if htmlHeader in soup.prettify():
                        return '', soup
            except:
                pass
                # Exception occurred, not checking internet connection
                if not WebScraper.isConnected():
                    # No internet connection
                    return 'III', None
            return 'XXX', None

        if i > self.maxDepth:
            return
        res, soup = getPage(self.data['Internal'][i])
        if not res:
            try:
                self.extractImageUrls(soup, self.data['Internal'][i])
            except:
                pass
            self.getData(self.data['Internal'][i], soup)
        print(i)
        i += 1
        self.recursiveScrap(i)

    def scrapeData(self):
        try:
            # Call the recursive scrapper function
            self.recursiveScrap(0)
        except:
            traceback.print_exc()
        self.driver.quit()
        return self.data

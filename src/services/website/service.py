import sys
import json
import asyncio
from playwright.async_api import async_playwright
import socket
import traceback
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from _utils import create_success_response



class WebScraper:

    def __init__(self, url, maxDepth) -> None:
        url = url.strip()
        if not "http" in url:
            if not "www." in url:
                url = "www." + url
            url = "http://" + url
        self.url = url
        self.maxDepth = maxDepth
        self.data = {
            "image": [],
            "video": [],
            "audio": [],
            "pdf": [],
            "html": [],
            "internal": [
                self.url,
            ],
        }
        self.browser = None
        self.page = None

    async def setup_playwright(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

    @staticmethod
    async def isConnected():
        # Function to check internet connection asynchronously
        try:
            _, writer = await asyncio.open_connection("1.1.1.1", 53)
            writer.close()
            return True
        except OSError:
            pass
        return False

    def isValid(self, url):
        # Checks whether `url` is a valid URL.
        parsed = urlparse(url)

        if not bool(parsed.netloc) or not bool(parsed.scheme):
            return False

        # Check if the same URL already exists in the internal list
        stripped_url = parsed.netloc + parsed.path
        stripped_url = stripped_url.lstrip("www.")  # remove www
        stripped_url = stripped_url.rstrip("/")  # remove backslash
        if any(stripped_url in s for s in self.data["internal"]):
            return False
        return True

    def extractImageUrls(self, soup, site):
        img_tags = soup.find_all("img")
        urls = [img["src"] for img in img_tags]
        for url in urls:
            if ".png" or ".gif" or ".jpg" in url:
                if "http" not in url:
                    url = "{}{}".format(site, url)
                if url not in self.data["image"]:
                    self.data["image"].append(url)

    def getData(self, url, soup):
        def addType(href):
            if (
                ".png" in href
                or ".gif" in href
                or ".jpg" in href
                and href not in self.data["image"]
            ):
                self.data["image"].append(href)
            elif ".html" in href and href not in self.data["html"]:
                self.data["html"].append(href)
            elif ".pdf" in href and href not in self.data["pdf"]:
                self.data["pdf"].append(href)
            elif ".mp3" in href and href not in self.data["audio"]:
                self.data["audio"].append(href)
            elif (
                ".mp4" in href
                or ".mpeg" in href
                or ".wov" in href
                or ".avi" in href
                or ".mkv" in href
                and href not in self.data["video"]
            ):
                self.data["video"].append(href)

        domainName = urlparse(url).netloc
        for tag in soup.findAll("a"):
            href = tag.attrs.get("href")
            if href == "" or href is None:
                continue
            href = urljoin(url, href)

            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not self.isValid(href):
                continue
            addType(href)
            if domainName in href and href not in self.data["internal"]:
                self.data["internal"].append(href)

    async def recursiveScrap(self, i):
        async def getPage(url):
            oddUrl = [".jpg", ".jpeg", ".png", ".pdf", ".xlsx"]
            for i in oddUrl:
                if i in url:
                    return "XXX", None
            htmlHeaders = [
                "text/css",
                "text/csv",
                "text/html",
                "text/javascript (obsolete)",
                "text/plain",
                "text/xml",
            ]
            try:
                await self.page.goto(url)
                content = await self.page.content()
                soup = BeautifulSoup(content, "html.parser")
                for htmlHeader in htmlHeaders:
                    if htmlHeader in soup.prettify():
                        return "", soup
            except:
                pass
                if not await WebScraper.isConnected():
                    return "III", None
            return "XXX", None

        if i > self.maxDepth:
            return
        res, soup = await getPage(self.data["internal"][i])
        if not res:
            try:
                self.extractImageUrls(soup, self.data["internal"][i])
            except:
                pass
            self.getData(self.data["internal"][i], soup)
        print(i)
        i += 1
        await self.recursiveScrap(i)

    async def scrapeData(self):
        await self.setup_playwright()
        try:
            await self.recursiveScrap(0)
        except Exception as e:
            return create_success_response(self.data)
        await self.browser.close()
        return create_success_response(self.data)


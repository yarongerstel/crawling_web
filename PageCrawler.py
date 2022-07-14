import re
from bs4 import BeautifulSoup
import requests


class PageCrawler:
    """
    the class Gets a URL that saves the information from that site and uses it
    """

    def __init__(self, url):
        """
        Gets a URL and extracts the data from it.
        :param url: URL to extract the data
        """
        self._url = url
        req = requests.get(self._url)
        req = req.text
        self._response = re.sub(r"\s+", " ", req)

    def crawl(self, regex):
        """
        The function gets a regular expression and returns a list of all matches from the given URL
        :param regex: A regular expression used to search for MAC addresses
        :return: list of all matches. If no match is found returns an empty list
        """
        return re.findall(regex, self._response)

    def findlinks(self):
        """
        The function returns all links from this web page
        :return: List of all links from this web page
        """
        soup = BeautifulSoup(self._response, "html.parser")
        links = []
        for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
            links.append(link.get('href'))
        return list(dict.fromkeys(links)) # Deletes a double link



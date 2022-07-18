import re
from bs4 import BeautifulSoup
import requests


class PageCrawler:
    """
    The class receives a URL and extracts the information from this site and uses it
    """

    def __init__(self, url):
        """
        Gets url and extracts data from it.
        :param url: URL to extract data
        """
        # regex of MAC address
        self._regex = r"(?:[0-9A-Fa-f]{2}[:]){5}(?:[0-9A-Fa-f]){2}"
        self._url = url
        try:
            res = requests.get(self._url)
            res = res.text
            self._response = re.sub(r"\s+", " ", res)
        except Exception as e:
            print("failed to get response to: " + self._url, type(e))

    def crawl(self):
        """
        The function returns a list of all mac address from the given URL
        :return: list of all matches. If no match is found returns an empty list
        """
        return re.findall(self._regex, self._response)

    def findlinks(self):
        """
        The function returns all links from this url
        :return: List of all links from this web page
        """
        soup = BeautifulSoup(self._response, "html.parser")
        links = []
        for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
            links.append(link.get('href'))
        return list(dict.fromkeys(links))  # Deletes a double link

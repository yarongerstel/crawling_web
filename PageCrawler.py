import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


class PageCrawler:
    """
    the class Gets a URL that saves the information from that site and uses it
    """

    def __init__(self, url):
        self._url = url
        # we need to override the user-agent with Mozilla.
        req = Request(self._url, headers={'User-Agent': 'Mozilla/5.0'})
        self._response = urlopen(req).read()

    def crawl(self, regex):
        """
        The function gets a regular expression and returns a list of all matches from the given URL
        :param regex: A regular expression used to search for MAC addresses
        :return: list of all matches. If no match is found returns an empty list
        """
        return re.findall(regex, str(self._response))

    def findlinks(self):
        """
        The function returns all links from this web page
        :return: List of all links from this web page
        """
        soup = BeautifulSoup(self._response, "html.parser")
        links = []
        for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
            links.append(link.get('href'))
        print(links)
        print(list(dict.fromkeys(links)))

#
# p = PageCrawler('https://www.smarttechvillas.com/new-stalker-iptv-codes-portal-url-and-mac-address-for-nov-2021/')
# regex = r"00:..:..:.8:..:.."
# print(p.crawl(regex))
# print(p.findlinks())

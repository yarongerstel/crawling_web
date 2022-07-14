import json
from PageCrawler import PageCrawler
from HistoryCrawler import HistoryCrawler


class WebsiteCrawler:
    """
    A class that receives a URL, a maximum number of tests to perform and regular expression.
    Performs a scan to find the regular value in the given domain.
    is limited by a maximum number of web addresses to check
    """

    crawlinghistory = {"url": []}
    mac_addersses = {"addresses": []}

    def __init__(self, root_url, max_page, regex):
        """
        :param root_url: The domain to be crawled
        :param max_page: Some URLs to check
        :param regex: What to look for - appears as a regular phrase
        """
        self._root_url = root_url
        self._max_page = max_page
        self._regex = regex
        self._domain = "https://" + root_url.split('/')[2]

    def start_crawler(self):
        """
        A function that activates the actual crawl of websites
        :return:
        """
        history = HistoryCrawler(self._root_url)
        self.crawl_link(self._root_url)
        for link in history:
            if self._max_page > 0:
                self.crawl_link(link)
            else:  # limit by max
                break
        self.refreshing_unscanned()
        self.add_unscanned_to_crawlinghistory()
        self.json_dumps()
        print("finish")

    def crawl_link(self, link):
        """
        A function that triggers a scan on a specific URL
        :param link: The URL where we will crawl
        :return:
        """
        if self._domain in link:
            try:
                crawling = PageCrawler(link)
                matched_mac = crawling.crawl(self._regex)
                for mac in matched_mac:
                    WebsiteCrawler.mac_addersses["addresses"].append({"mac_address": mac, "origin_url": link})
                print(link, matched_mac)
                HistoryCrawler.register_dict["scanned"].append(link)
                WebsiteCrawler.crawlinghistory["url"].append({"url": link, "crawl_status": "True"})
                self._max_page -= 1
            except Exception as e:
                print("can't crawler into " + link, type(e))

    @staticmethod
    def refreshing_unscanned():
        """
        Function responsible for deleting all domains already scanned from the waiting list to crawling
        :return:
        """
        # delete all scanned from the non scanned list
        for scanned in HistoryCrawler.register_dict["scanned"]:
            if scanned in HistoryCrawler.register_dict["non_scanned"]:
                HistoryCrawler.register_dict["non_scanned"].remove(scanned)

    @staticmethod
    def add_unscanned_to_crawlinghistory():
        """
        Function that adds the domains that have not been scanned to the crawlinghistory dictionary
        :return:
        """
        # add all non_scanned to the crawlinghistory
        for non_scanned in HistoryCrawler.register_dict["non_scanned"]:
            WebsiteCrawler.crawlinghistory["url"].append({"url": non_scanned, "crawl_status": "False"})

    @staticmethod
    def json_dumps():
        """
        Function responsible for creating JSON files from data dictionaries
        :return:
        """
        with open('crawling_history.json', 'w') as j:
            j.write(json.dumps(WebsiteCrawler.crawlinghistory))
        with open('mac_addresses.json', 'w') as j:
            j.write(json.dumps(WebsiteCrawler.mac_addersses))


c = WebsiteCrawler("https://www.smarttechvillas.com/new-stalker-iptv-codes-portal-url-and-mac-address-for-nov-2021/",
                   206, r"..:..:..:..:..:..")
c.start_crawler()

import json
from PageCrawler import PageCrawler
from HistoryCrawler import HistoryCrawler


class WebsiteCrawler:
    """
    A class that receives a URL, a maximum number of tests to perform.
    Performs a scan to find the regular value in the given domain.
    is limited by a maximum number of web addresses to check.
    """

    crawling_history = []
    mac_addresses = []

    def __init__(self, root_url, max_page):
        """
        :param root_url: The root url to be crawled
        :param max_page: Some URLs to check
        """
        self._root_url = root_url
        self._max_page = max_page
        try:
            self._domain = "https://" + root_url.split('/')[2]
        except IndexError:
            print('Invalid address, the address need start with "https://" or "http://" ')
            return

    def start_crawler(self):
        """
        A function that activates the actual crawl of websites
        :return:
        """
        HistoryCrawler(self._root_url)  # Initializes the static values in HistoryCrawler class
        self.crawl_link(self._root_url)  # Scans and moves the root to the scanned list
        counter = 0

        while self._max_page > 0:
            if counter < len(HistoryCrawler.register_dict["scanned"]):  # have more links to scann
                print("scanning links in: "+HistoryCrawler.register_dict["scanned"][counter])
                branch = HistoryCrawler(HistoryCrawler.register_dict["scanned"][counter])
                # iterator ran on the non_scanned list. (According the _ether_ function in HistoryCrawler class)
                for link in branch:
                    if self._max_page > 0:
                        self.crawl_link(link)
                    else:  # limit by max
                        break
                counter += 1
            else:  # all links scanned.
                break

        self.refreshing_unscanned()
        self.add_unscanned_to_crawling_history()
        self.json_dumps()
        print("finish. number of matched: ", len(WebsiteCrawler.mac_addresses))

    def crawl_link(self, link):
        """
        A function that triggers a scan on a specific url, and adds the url to the scanned list
        :param link: The URL where we will crawl
        :return:
        """
        if self._domain in link:
            try:
                # Prevents duplicate crawling of the same URL
                if link in HistoryCrawler.register_dict["scanned"]:
                    return

                crawl_url = PageCrawler(link)
                matched_mac = crawl_url.crawl()

                for mac in matched_mac:
                    WebsiteCrawler.mac_addresses.append({"mac_address": mac, "origin_url": link})

                print(link, matched_mac)  # debugging

                HistoryCrawler.register_dict["scanned"].append(link)

                WebsiteCrawler.crawling_history.append({"url": link, "crawl_status": "True"})
                self._max_page -= 1
            except Exception as e:
                print("Can't crawl URL: " + link, type(e))

    def add_unscanned_to_crawling_history(self):
        """
        A function that adds the unscanned links to crawling_history dictionary
        :return:
        """
        # add all non_scanned to the crawling_history
        for non_scanned in HistoryCrawler.register_dict["non_scanned"]:
            if self._domain in non_scanned:  # What is outside the domain is not registered
                WebsiteCrawler.crawling_history.append({"url": non_scanned, "crawl_status": "False"})

    @staticmethod
    def refreshing_unscanned():
        """
        A function responsible for deleting all domains already scanned from the waiting list to crawling
        :return:
        """
        # delete all scanned from the non scanned list
        for scanned in HistoryCrawler.register_dict["scanned"]:
            if scanned in HistoryCrawler.register_dict["non_scanned"]:
                HistoryCrawler.register_dict["non_scanned"].remove(scanned)

    @staticmethod
    def json_dumps():
        """
        A function responsible for creating JSON files from data dictionaries
        :return:
        """
        with open('crawling_history.json', 'w') as j:
            j.write(json.dumps(WebsiteCrawler.crawling_history))
        with open('mac_addresses.json', 'w') as j:
            j.write(json.dumps(WebsiteCrawler.mac_addresses))


c = WebsiteCrawler("https://www.smarttechvillas.com/new-stalker-iptv-codes-portal-url-and-mac-address-for-nov-2021/"
                   , 300)
c.start_crawler()

import json
from PageCrawler import PageCrawler
from HistoryCrawler import HistoryCrawler


class WebsiteCrawler:
    def __init__(self, root_url, max_page, regex):
        self._root_url = root_url
        self._max_page = max_page
        self._regex = regex
        self._domain = "https://" + root_url.split('/')[2]

    def start_crawler(self):
        history = HistoryCrawler(self._root_url)
        crawlinghistory = {"url": []}
        mac_addersses = {"addresses": []}

        crawling = PageCrawler(self._root_url)
        matched_mac = crawling.crawl(self._regex)
        for mac in matched_mac:
            mac_addersses["addresses"].append({"mac_address": mac, "origin_url": self._root_url})
        print(self._root_url, matched_mac)
        HistoryCrawler.register_dict["scanned"].append(self._root_url)

        for link in history:
            if self._max_page > 0:
                if self._domain not in link:
                    continue
                try:
                    crawling = PageCrawler(link)
                    matched_mac = crawling.crawl(self._regex)
                    for mac in matched_mac:
                        mac_addersses["addresses"].append({"mac_address":mac,"origin_url":link})
                    print (link, matched_mac)
                    HistoryCrawler.register_dict["scanned"].append(link)
                    crawlinghistory["url"].append({"url": link, "crawl_status": "True"})
                    self._max_page -= 1
                except Exception as e:
                    print("can't crawler into " + link, type(e))
            else:  # limit by max
                break

        # delete all scanned from the non scanned list
        for scanned in HistoryCrawler.register_dict["scanned"]:
            if scanned in HistoryCrawler.register_dict["non_scanned"]:
                HistoryCrawler.register_dict["non_scanned"].remove(scanned)

        # add all non_scanned to the crawlinghistory
        for non_scanned in HistoryCrawler.register_dict["non_scanned"]:
            crawlinghistory["url"].append({"url": non_scanned, "crawl_status": "False"})

        with open('crawling_history.json', 'w') as j:
            j.write(json.dumps(crawlinghistory))
        with open('mac_addresses.json', 'w') as j:
            j.write(json.dumps(mac_addersses))

        print("finish")


c = WebsiteCrawler("https://webloadedtech.com/ott-navigator-free-iptv-login-and-mac-address/",
                   206, r"..:..:..:..:..:..")
c.start_crawler()

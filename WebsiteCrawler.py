from PageCrawler import PageCrawler
from HistoryCrawler import HistoryCrawler


class WebsiteCrawler:
    def __init__(self, root_url, max_page, regex):
        self._root_url = root_url
        self._max_page = max_page
        self._regex = regex
        self._domain = root_url.split('/')[2]

    def start_crawler(self):
        history = HistoryCrawler(self._root_url)
        crawling = PageCrawler(self._root_url)
        print(crawling.crawl(self._regex))
        history.reg_dict["scanned"].append(self._root_url)

        for link in history:
            if self._max_page > 1:
                if self._domain not in link:
                    continue
                try:
                    crawling = PageCrawler(link)
                    print(link, crawling.crawl(self._regex))
                    history.reg_dict["scanned"].append(link)
                    self._max_page -= 1
                except:
                    print("can't crawler into " + link)
            else:
                break
        # delete all scanned from the non scanned list
        for scanned in history.reg_dict["scanned"]:
            history.reg_dict["non_scanned"].remove(scanned)
        print("finish")


c = WebsiteCrawler("https://webloadedtech.com/ott-navigator-free-iptv-login-and-mac-address/",
                   50, r"..:..:..:..:..:..")
c.start_crawler()

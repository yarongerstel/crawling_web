from PageCrawler import PageCrawler


class HistoryCrawler:
    def __init__(self, url):
        root_page = PageCrawler(url)
        self.reg_dict = {"scanned": [], "non_scanned" : root_page.findlinks()}
        self._index = 0
        self._max_index = len(self.reg_dict["non_scanned"])
        self._link = self.reg_dict["non_scanned"][self._index]

    def __iter__(self):
        return iter(self.reg_dict["non_scanned"])

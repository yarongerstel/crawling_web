from PageCrawler import PageCrawler


class HistoryCrawler:
    """
    A class that contains information for crawled sites that have not yet been crawled
    """

    register_dict = {"scanned": [], "non_scanned": []}

    def __init__(self, url):
        root_page = PageCrawler(url)
        HistoryCrawler.register_dict["non_scanned"] = HistoryCrawler.register_dict["non_scanned"] + root_page.findlinks()
        self.register_dict = {"scanned": [], "non_scanned": root_page.findlinks()}

    def __iter__(self):
        """
        A function that allows to use the list of sites that have not been crawled as an iterator
        :return: Iterator for all unscanned sites
        """
        return iter(self.register_dict["non_scanned"])

from PageCrawler import PageCrawler


class HistoryCrawler:
    """
    Class that contains information about sites that have already been crawled and those that have not yet been crawled
    """
    register_dict = {"scanned": [], "non_scanned": []}

    def __init__(self, url):
        """
        gets a URL and adds to "HistoryCrawler.register_dict["non_scanned"]" all unscanned links that appear
        at this address
        :param url: The root URL crawling
        """
        root_page = PageCrawler(url)
        self._register_dict = {"scanned": [], "non_scanned": root_page.findlinks()}
        self.delete_duplicate()

    def __iter__(self):
        """
        A function that allows to use the list of sites that have not been crawled as an iterator
        :return: Iterator for all unscanned sites
        """
        return iter(self._register_dict["non_scanned"])

    def __add__(self, url):
        """
        Add address to local scan list
        *** Should do this before turning on the iteration otherwise it will not scan it! ***
        :param url: new address add to local scan list
        :return:
        """
        self._register_dict["non_scanned"] = [url] + self._register_dict["non_scanned"]

    def delete_duplicate(self):
        """
        A function that removes from the local list "non_scanned" all the already scanned links
        and adds this list to the static "non_scanned" list.
        :return:
        """
        temp = self._register_dict["non_scanned"]
        # Delete links that have already been scanned
        for link in self._register_dict["non_scanned"]:
            if link in HistoryCrawler.register_dict["scanned"]:
                temp.remove(link)
        HistoryCrawler.register_dict["non_scanned"] = HistoryCrawler.register_dict["non_scanned"] + temp
        self._register_dict["non_scanned"] = temp

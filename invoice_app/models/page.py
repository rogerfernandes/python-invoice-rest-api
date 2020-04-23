class Page:
    def __init__(self, total_items, page_size: 20, page_number: 1, last_page, data: []):
        self._total_items = total_items,
        self._page_size = page_size
        self._page_number = page_number
        self._last_page = last_page,
        self._data = data

    def to_json(self):
        return {
            "page_size": int(self._page_size),
            "page_number": int(self._page_number),
            "total_items": self._total_items[0],
            "last_page": self._last_page[0],
            "data": self._data
        }

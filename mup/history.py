class HistoryItem(object):
    def __init__(self, filename, converter, scrollPos=None):
        self.filename = filename
        self.converter = converter
        self.scrollPos = scrollPos


class History(object):
    def __init__(self):
        self._lst = []
        self._index = -1

    def push(self, historyItem):
        """
        Discard items after _index and add our item
        """
        self._index += 1
        self._lst = self._lst[:self._index]
        self._lst.append(historyItem)

    def canGoBack(self):
        return self._index > 0

    def canGoForward(self):
        return self._index < len(self._lst) - 1

    def goBack(self):
        self._index -= 1
        assert self._index >= 0

    def goForward(self):
        self._index += 1
        assert self._index < len(self._lst)

    def current(self):
        return self._lst[self._index] if self._index != -1 else None

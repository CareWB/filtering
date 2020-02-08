from datetime import datetime

class news:
    def __init__(self, title, link, time = datetime.now(), other = None):
        self.title = title
        self.link = link
        self.time = time
        self.other = other

    def __str__(self):
        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()]) 
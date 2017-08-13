import time
import datetime

import pevy.models

class Time:
    def __init__(self, logger, config):
        self.logger = logger
        self.interval = int(config['interval'])
        self.last_update = None

    def poll(self):
        self.logger.info(time.ctime())

        now = datetime.datetime.now()
        if self.last_update:
            delta = now - self.last_update
            if delta.total_seconds() > self.interval:
                self.last_update = now
                yield self.__time_item()
        else:
            self.last_update = now
            yield self.__time_item()

    def __time_item(self):
        id = 'time/' + str(time.time())
        text = time.ctime()
        return pevy.models.Item(id=id, author=None, text=text, image=None)

    def __str__(self):
        return 'time'

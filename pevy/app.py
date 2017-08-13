from optparse import OptionParser
import logging
import sys
import time
import yaml

import pevy.database
import pevy.printer
import pevy.resolve
import pevy.sources

class App:
    def __init__(self):
        parser = OptionParser()
        parser.add_option("-c", "--config", dest="config",
                help="Configuration file", metavar="CONFIG")

        (options, args) = parser.parse_args()

        if not options.config:
            parser.error("-c CONFIG is required")

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('pevy')

        with open(options.config, 'r') as config_file:
            config = yaml.load(config_file)

        database_path = config['database_path']
        self.database = pevy.database.Database(self.logger, database_path)

        self.printer = pevy.printer.Printer(self.logger)

        self.sources = []

        for section in config['sources']:
            k = section['type']
            constructor = pevy.sources.sources[k]
            source = constructor(self.logger, section)
            self.sources += [source]

    def run(self):
        while True:
            pevy.resolve.reset()
            self.__poll_for_items()
            self.__print_items()
            self.logger.info('Sleeping for some time...')
            time.sleep(40)

    def __poll_for_items(self):
        for source in self.sources:
            try:
                self.logger.info('Polling source {}...'.format(str(source)))
                items = source.poll()
                if items:
                    for item in items:
                        self.database.queue_item(item)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                self.logger.error(e)

    def __print_items(self):
        for item in self.database.get_unprinted_items():
            try:
                self.printer.print_item(item)
                self.database.mark_item_as_printed(item)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                self.logger.error(e)

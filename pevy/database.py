import sqlite3

import pevy.models

class Database:
    def __init__(self, logger, filepath):
        self.logger = logger
        self.conn = sqlite3.connect(filepath)
        self.__setup_database()

    def __setup_database(self):
        self.logger.info('Setting up database...')
        self.conn.execute("""CREATE TABLE IF NOT EXISTS items (
                id      STRING PRIMARY KEY NOT NULL,
                text    STRING,
                image   BLOB,
                printed INT
        )""")

        self.conn.execute("""CREATE INDEX IF NOT EXISTS items_printed
                ON items (printed)""")

        self.conn.commit()

    def queue_item(self, item):
        self.conn.execute("""INSERT OR IGNORE INTO items
                (id, text, image, printed) VALUES (?, ?, ?, ?)""",
                (item.id, item.text, item.image, 0))
        self.conn.commit()

    def get_unprinted_items(self):
        cur = self.conn.cursor()
        result = cur.execute("""SELECT id, text, image FROM items
                WHERE printed = 0""")
        for row in result:
            item = pevy.models.Item(id=row[0], text=row[1], image=row[2])
            yield item

    def mark_item_as_printed(self, item):
        self.conn.execute(
                "UPDATE items SET printed = 1, image = NULL WHERE id = ?",
                [item.id])
        self.conn.commit()
